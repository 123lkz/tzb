path = r'F:\lkz\bo\1\codex\my\agents\agent1\设计框架文档.md'

text = r"""# Agent 1 设计框架文档

> **所属项目**：多源异构数据驱动岗位和能力图谱构建与动态演化分析研究  
> **所属层级**：AI 智能体分析层（紫色层）  
> **核心职责**：新岗位发现 + 能力更新  
> **依赖**：读取 `jobs_clean`，复用 Agent2 的 LLMClient 和 ProfileStore  
> **最后更新**：2026-07-22

---

## 一、设计动机

| 问题 | 现状 | Agent1 的做法 |
|------|------|-------------|
| 岗位目录滞后 | 静态岗位分类无法覆盖新兴岗位 | 无监督聚类自动发现未被收录的新岗位 |
| 技能需求漂移 | 岗位技能需求随时间快速变化 | 时序分析检测新增/淘汰/升温/降温技能 |

```
Agent1（发现）-> MongoDB agent1_output -> Agent2（验证）-> jobs_kg -> Neo4j
```

---

## 二、系统架构

```
AI 智能体分析层（紫）
  |-> Agent1: 新岗位发现 + 能力更新  <-- 本模块
  |-> Agent2: 数据质量治理 + 幻觉防控
  |-> Agent3: 简历解析 + 人岗匹配
```

### 2.1 内部模块

```
Agent1Orchestrator (main.py)
+-- job_discovery/              新岗位发现模块
|   +-- JobClusterer            文本聚类引擎
|   +-- NoveltyDetector         新兴性检测
|   +-- LabelGenerator          LLM 辅助标注
|   +-- schemas.py              数据模型
+-- skill_evolution/            能力演化检测模块
|   +-- SkillTrendAnalyzer      技能趋势分析
|   +-- EvolutionDetector       演化检测
|   +-- schemas.py              数据模型
+-- output_adapter/             输出适配层
|   +-- ChangeRecordBuilder     变更记录组装器
|   +-- GraphInterface          图谱接口适配器
|   +-- schemas.py              统一输出模型
+-- prompt_templates.py  config.py  tests/
```

### 2.2 数据流

```
jobs_clean -> 聚类 -> 与已有PositionProfile对比 -> LLM标注 -> agent1_output
```

---

## 三、NewPositionSuggestion 数据结构

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| suggested_name | str | 建议的岗位名称 | LLM / 统计 |
| core_responsibilities | list[str] | 核心职责（3-5项）| LLM |
| suggested_required_skills | list[str] | 必需技能 | LLM / 统计 |
| suggested_optional_skills | list[str] | 加分技能 | LLM / 统计 |
| typical_applications | list[str] | 典型应用场景（1-3项）| LLM |

其他字段：cluster_size、novelty_score、evidence_samples、typical_salary_range、confidence、provenance。

### 输出示例

```
{
  "suggested_name": "大模型算法工程师",
  "core_responsibilities": [
    "负责大模型架构设计与优化",
    "实施分布式训练策略",
    "参与技术方案评审"
  ],
  "suggested_required_skills": ["Transformer", "PyTorch", "CUDA"],
  "suggested_optional_skills": ["模型量化", "数据处理"],
  "typical_applications": [
    "通用大语言模型研发与微调",
    "多模态模型预训练与部署"
  ]
}
```

---

## 四、关键技术选型

| 技术方向 | 选择 | 降级方案 |
|---------|------|---------|
| 文本向量化 | SentenceTransformer | TF-IDF |
| 聚类算法 | HDBSCAN | KMeans |
| 核心 LLM | DeepSeek | 统计规则 |
| 趋势分析 | 滑动窗口 + 频次统计 | -- |
| 数据建模 | Pydantic v2 | -- |
| 数据库 | MongoDB | -- |

### 三阶段降级

| 阶段 | 首选 | 降级条件 |
|------|------|---------|
| 向量化 | SentenceTransformer | torch 加载失败 |
| 聚类 | HDBSCAN | 未安装 hdbscan |
| 标注 | DeepSeek LLM | 网络不通 |

自动静默降级，不中断流程。

---

## 五、输入输出

### 输入数据

```
title: str        # 岗位名称
description: str  # JD 描述
skills: list      # 技能标签
pub_date: str     # 发布日期
extras: dict      # 扩展字段
```

### 输出接口

写入 MongoDB `agent1_output` 集合，状态机流转：

```
pending -> verified -> merged
```

全景图谱模块直接消费 `status: verified` 的记录。

---

## 六、协作关系

| 模块 | 关系 |
|------|------|
| Agent2 | 读取 PositionProfile 做对比，输出经 Agent2 校验 |
| Agent3 | 新岗位扩充图谱后间接扩大匹配覆盖 |
| 全景图谱 | 消费 agent1_output 中的 verified 记录 |

---

## 七、测试

| 类别 | 数量 |
|------|------|
| 数据模型 | 35 |
| 聚类引擎 | 9 |
| 新兴性检测 | 6 |
| LLM 标注 | 9 |
| 趋势分析 | 14 |
| 演化判定 | 10 |
| 输出适配 | 10 |
| **合计** | **95** |

---

## 八、运行命令

```bash
python -m agents.agent1.main
python -m agents.agent1.main --discovery-only
python -m agents.agent1.main --batch 500 --industry "人工智能"
```
"""

open(path, 'w', encoding='utf-8').write(text)
print(f'Updated: {len(text)} bytes')
import os; os.remove(__file__)
