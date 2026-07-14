# 招聘数据爬虫平台

## 项目简介
本项目是一个专门用于抓取各大招聘网站数据的爬虫平台，支持智联招聘、BOSS直聘、应届生求职网等多个招聘网站的数据采集、清洗、存储和分析。

## 功能特性
- 多平台数据采集
  - 智联招聘（职位搜索与详情）
  - BOSS直聘（职位搜索与详情）
  - 应届生求职网（校招信息）
- 浏览器自动化爬取（基于Playwright）
- 统一的数据标准化处理
- 强大的错误处理与重试机制
- 反爬虫策略（UA随机、代理IP支持）
- 自动化日志管理（含时间戳）
- 错误截图保存功能
- MongoDB异步存储

## 技术架构
### 核心技术栈
- Python 3.11+
- Playwright 1.50.0（浏览器自动化）
- MongoDB（Motor 3.7.0 异步驱动）
- Pandas/NumPy（数据分析）

### 系统架构
```bash
recruitment_spider/
├── spiders/                  # 爬虫实现
│   ├── base_spider.py        # 基础爬虫类（浏览器管理、数据库操作）
│   ├── zhilian_spider.py     # 智联招聘爬虫
│   ├── boss_spider.py        # BOSS直聘爬虫
│   └── yingjiesheng_spider.py # 应届生求职网爬虫
├── utils/                    # 工具函数
│   ├── log_manager.py        # 日志管理（支持时间戳日志文件）
│   ├── proxy_manager.py      # 代理IP管理
│   ├── parser.py             # 通用解析工具
│   └── data_cleaner.py       # 数据清洗器
├── data/                     # 数据目录
│   ├── zhilian/              # 智联招聘数据
│   ├── bosszhipin/           # BOSS直聘数据
│   └── yingjieshengqiuzhiwang/ # 应届生求职网数据
├── logs/                     # 日志目录（自动创建）
├── screenshots/              # 错误截图保存目录
├── run_recruitment_spider.py # 统一启动脚本
├── run_boss_spider.py        # BOSS直聘单独启动脚本
├── run_zhilian_spider.py     # 智联招聘单独启动脚本
└── requirements.txt          # 项目依赖
```

### 爬虫实现特点

#### 基础架构（base_spider.py）
- 统一的浏览器管理（Playwright）
- MongoDB异步连接管理
- 反爬措施（UA随机、请求头定制）
- 资源拦截（提高爬取速度）
- 错误页面截图功能
- 页面可用性检查

#### 爬虫特性
1. **BOSS直聘爬虫**
   - 支持基于职位分类的爬取
   - 多版本解析器适配页面变化
   - 智能等待与重试机制
   - 数据清洗与标准化

2. **智联招聘爬虫**
   - 支持基于职位层级的爬取
   - 多策略数据提取
   - 薪资范围标准化

3. **应届生求职网爬虫**
   - 针对校园招聘数据
   - 支持城市和职位过滤
   - 特定页面结构解析

### 核心功能实现

#### 错误处理机制
- 多层重试策略
- 超时错误智能处理
- 浏览器状态检测
- 错误自动截图
- 异常分类与记录

#### 日志管理
- 带时间戳的日志文件
- 不同模块独立日志
- 多级日志（DEBUG/INFO/WARNING/ERROR/CRITICAL）
- 控制台和文件双输出

#### 数据处理流程

```
[爬虫采集] -> [原始数据(jobs_raw)] -> [数据清洗器] -> [清洗数据(jobs_clean)]
     │              │                      │                    │
     │              │                      │                    │
     └─► 多平台采集  └─► 保留原始格式        └─► 统一字段标准      └─► 支持查询分析
         自动更新        数据追溯             数据清洗             数据存储
         反爬处理        源数据备份           字段提取             唯一索引
```

## 安装与配置
### 环境要求
- Python 3.11+
- MongoDB

### 安装步骤
1. 克隆项目
   ```bash
   git clone <项目地址>
   cd recruitment_spider
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 安装Playwright浏览器
   ```bash
   playwright install
   ```

4. 配置MongoDB
   - 复制.env.example为.env
   - 修改MongoDB连接信息

### 运行爬虫
1. 运行所有爬虫
   ```bash
   python run_recruitment_spider.py
   ```

2. 运行特定爬虫
   ```bash
   python run_boss_spider.py
   python run_zhilian_spider.py
   ```

3. 参数说明
   ```
   --headless       无头模式（默认：否）
   --city           城市（默认：全国）
   --browser-count  浏览器数量（默认：1）
   --tabs-per-browser 每个浏览器的标签页数（默认：1）
   --debug          调试模式
   ```

## 开发指南

### 添加新爬虫
1. 在spiders目录创建新的爬虫文件，继承BaseSpider
2. 实现必要的方法：process_job_type, get_job_list, process_job_data
3. 添加启动脚本或在统一脚本中注册

### 常见问题
- **爬虫被封禁**：调整请求间隔，更换代理IP
- **解析失败**：检查页面结构是否变化，更新选择器
- **MongoDB连接问题**：检查.env配置和网络连接
