# 数据库字段文档 v1.0

## 1. 原始数据集合 (jobs_raw)

原始数据集合用于存储直接从招聘网站爬取的数据，保持原始格式。

### 索引设计
- 主索引: `{ job_id: 1, source: 1 }` (唯一索引)

### 字段说明
| 字段名 | 类型 | 描述 | 来源 | 示例值 |
|--------|------|------|------|---------|
| job_id | String | 职位ID | 爬虫 | "12345678" |
| title | String | 职位名称 | 爬虫 | "Python开发工程师" |
| company | String | 公司名称 | 爬虫 | "阿里巴巴" |
| salary | String | 薪资描述 | 爬虫 | "15k-25k" |
| city | String | 城市 | 爬虫 | "北京" |
| district | String | 区域 | 爬虫 | "海淀区" |
| experience | String | 经验要求 | 爬虫 | "3-5年" |
| education | String | 学历要求 | 爬虫 | "本科" |
| company_type | String | 公司类型 | 爬虫 | "外企" |
| company_size | String | 公司规模 | 爬虫 | "500-1000人" |
| company_industry | String | 公司行业 | 爬虫 | "互联网" |
| job_type | String | 职位类型 | 爬虫 | "全职" |
| job_tags | Array | 职位标签 | 爬虫 | ["五险一金", "年终奖"] |
| job_url | String | 职位链接 | 爬虫 | "https://www.zhaopin.com/job/12345678" |
| hr_name | String | HR姓名 | 爬虫 | "王小影" |
| hr_position | String | HR职位 | 爬虫 | "行政人事" |
| hr_active | String | HR活跃状态 | 爬虫 | "昨日活跃" |
| publish_time | String | 发布时间 | 爬虫 | "2024-02-17" |
| update_time | String | 更新时间 | 爬虫 | "2024-02-17" |
| source | String | 数据来源 | 爬虫 | "zhilian" |
| crawl_time | DateTime | 爬取时间 | 系统 | "2024-02-17 10:00:00" |
| company_url | String | 公司链接 | 爬虫 | "https://company.zhilian.com/12345" |
| uploader | String | 上传人 | 系统 | "developer1" |

## 2. 清洗后数据集合 (jobs_clean)

清洗后的数据集合用于存储经过标准化和清洗的职位数据，用于后续分析。

### 索引设计
- 主索引: `{ unified_job_id: 1 }` (唯一索引)
- 查询索引: `{ title: 1, city: 1, salary_min: 1, salary_max: 1 }`

### 字段说明
| 字段名 | 类型 | 描述 | 来源 | 示例值 | 更新说明 |
|--------|------|------|------|---------|----------|
| unified_job_id | String | 统一职位ID | 生成 | "zhilian_12345678" | 首次生成后不更新 |
| title | String | 职位名称 | 清洗 | "Python开发工程师" | 每次爬取更新 |
| company_name | String | 公司名称 | 清洗 | "阿里巴巴" | 每次爬取更新 |
| city | String | 城市 | 清洗 | "北京" | 每次爬取更新 |
| district | String | 区域 | 清洗 | "海淀区" | 每次爬取更新 |
| salary_raw | String | 原始薪资描述 | 爬虫 | "15k-25k" | 每次爬取更新 |
| salary_min | Number | 最低月薪(元) | 计算 | 15000 | 每次爬取更新 |
| salary_max | Number | 最高月薪(元) | 计算 | 25000 | 每次爬取更新 |
| experience | String | 经验要求 | 清洗 | "3-5年" | 每次爬取更新 |
| education | String | 学历要求 | 清洗 | "本科" | 每次爬取更新 |
| skills | Array | 技能要求 | 提取 | ["Python", "Django"] | 每次爬取更新 |
| company_type | String | 公司类型 | 清洗 | "外企" | 每次爬取更新 |
| company_size | String | 公司规模 | 清洗 | "500-1000人" | 每次爬取更新 |
| company_industry | String | 公司行业 | 清洗 | "互联网" | 每次爬取更新 |
| job_type | String | 职位类型 | 清洗 | "全职" | 每次爬取更新 |
| job_tags | Array | 职位标签 | 提取 | ["五险一金", "年终奖"] | 每次爬取更新 |
| job_description | String | 职位描述 | 清洗 | "负责公司核心系统..." | 每次爬取更新 |
| job_highlights | Array | 职位亮点 | 提取 | ["发展空间大", "团队氛围好"] | 每次爬取更新 |
| work_address | String | 详细地址 | 清洗 | "北京市海淀区西二旗" | 每次爬取更新 |
| location | Object | 地理位置 | 生成 | `{"type": "Point", "coordinates": [116.3, 40.1]}` | 地址变更时更新 |
| source | String | 数据来源 | 爬虫 | "zhilian" | 首次生成后不更新 |
| source_job_id | String | 原始职位ID | 爬虫 | "12345678" | 首次生成后不更新 |
| job_url | String | 职位链接 | 爬虫 | "https://..." | 每次爬取更新 |
| company_url | String | 公司链接 | 爬虫 | "https://company.zhilian.com/12345" | 每次爬取更新 |
| uploader | String | 上传人 | 系统 | "developer1" | 首次生成后不更新 |
| publish_time | DateTime | 发布时间 | 清洗 | "2024-02-17 10:00:00" | 每次爬取更新 |
| update_time | DateTime | 更新时间 | 清洗 | "2024-02-17 10:00:00" | 每次爬取更新 |
| crawl_time | DateTime | 爬取时间 | 系统 | "2024-02-17 10:00:00" | 每次爬取更新 |
| status | String | 数据状态 | 系统 | "active" | 状态变更时更新 |
| is_verified | Boolean | 是否验证 | 系统 | false | 验证后更新 |
| verification_time | DateTime | 验证时间 | 系统 | null | 验证后更新 |
| verification_note | String | 验证备注 | 系统 | "" | 验证后更新 |

### 数据来源说明
- 爬虫：直接从网站爬取的数据
- 清洗：对爬取数据进行清洗和标准化
- 提取：从描述或其他字段中提取的数据
- 计算：通过计算或转换得到的数据
- 生成：系统自动生成的数据
- 系统：系统运行时产生的数据

### 更新策略说明
1. 唯一标识字段（unified_job_id, source, source_job_id）：首次生成后不更新
2. 基础信息字段：每次爬取时更新
3. 计算字段：相关数据更新时重新计算
4. 系统状态字段：根据具体操作更新
5. 地理位置信息：地址变更时更新

## 3. 岗位明细数据集合 (jobs_detail)

岗位明细数据集合用于存储从职位详情页爬取的详细信息，包含完整的职位描述、职责要求和公司详情等。

### 索引设计
- 主索引: `{ detail_id: 1 }` (唯一索引)
- 关联索引: `{ unified_job_id: 1 }` (与jobs_clean表关联)
- 查询索引: `{ source_job_id: 1, source: 1 }`

### 字段说明
| 字段名 | 类型 | 描述 | 来源 | 示例值 | 更新说明 |
|--------|------|------|------|---------|----------|
| detail_id | String | 明细ID | 生成 | "detail_12345678" | 首次生成后不更新 |
| unified_job_id | String | 统一职位ID | 关联 | "zhilian_12345678" | 首次生成后不更新 |
| source_job_id | String | 原始职位ID | 爬虫 | "12345678" | 首次生成后不更新 |
| source | String | 数据来源 | 爬虫 | "zhilian" | 首次生成后不更新 |
| job_url | String | 职位链接 | 爬虫 | "https://www.zhaopin.com/jobdetail/12345678" | 每次爬取更新 |
| title | String | 职位名称 | 爬虫 | "Python开发工程师" | 每次爬取更新 |
| salary | String | 薪资描述 | 爬虫 | "15k-25k" | 每次爬取更新 |
| company_name | String | 公司名称 | 爬虫 | "阿里巴巴" | 每次爬取更新 |
| work_location | String | 工作地点 | 爬虫 | "北京市海淀区西二旗" | 每次爬取更新 |
| location_detail | String | 详细地址 | 爬虫 | "西城区德胜门外大街13号院1号楼合生财富广场4L" | 每次爬取更新 |
| experience | String | 经验要求 | 爬虫 | "3-5年" | 每次爬取更新 |
| education | String | 学历要求 | 爬虫 | "本科" | 每次爬取更新 |
| headcount | String | 招聘人数 | 爬虫 | "招1人" | 每次爬取更新 |
| job_type | String | 职位类型 | 爬虫 | "全职" | 每次爬取更新 |
| job_description | String | 职位描述 | 爬虫 | "1、负责公司核心系统的设计和开发...\n2、参与项目需求分析..." | 每次爬取更新 |
| job_responsibility | String | 岗位职责 | 爬虫 | "1、寻找和筛选有发展潜力和投资价值的项目机会..." | 每次爬取更新 |
| job_requirement | String | 任职要求 | 爬虫 | "1、本科以上学历...\n2、2年以上相关工作经验..." | 每次爬取更新 |
| job_benefits | Array | 职位福利 | 爬虫 | ["五险一金", "带薪年假", "全额公积金", "项目奖金"] | 每次爬取更新 |
| job_highlights | Array | 职位亮点 | 爬虫 | ["创业公司", "大牛带队", "周末双休"] | 每次爬取更新 |
| skills_required | Array | 技能要求 | 提取 | ["Python", "Django", "MySQL"] | 每次爬取更新 |
| company_url | String | 公司链接 | 爬虫 | "https://company.zhilian.com/12345" | 每次爬取更新 |
| company_industry | String | 公司行业 | 爬虫 | "证券/期货,基金" | 每次爬取更新 |
| company_size | String | 公司规模 | 爬虫 | "20-99人" | 每次爬取更新 |
| company_type | String | 公司类型 | 爬虫 | "国企" | 每次爬取更新 |
| company_financing | String | 融资阶段 | 爬虫 | "未融资" | 每次爬取更新 |
| company_description | String | 公司描述 | 爬虫 | "京津曹海（天津）股权投资基金管理有限公司，2016年06月16日成立..." | 每次爬取更新 |
| hr_name | String | HR姓名 | 爬虫 | "王小影" | 每次爬取更新 |
| hr_position | String | HR职位 | 爬虫 | "行政人事" | 每次爬取更新 |
| hr_active | String | HR活跃状态 | 爬虫 | "三日内活跃" | 每次爬取更新 |
| publish_time | String | 发布时间 | 爬虫 | "2024-02-17" | 每次爬取更新 |
| update_time | String | 更新时间 | 爬虫 | "今天" | 每次爬取更新 |
| similar_jobs | Array | 相似职位 | 爬虫 | [{"title": "投资经理", "salary": "1.2-1.5万", "company": "北京旭辉投资管理有限公司"}] | 每次爬取更新 |
| crawl_time | DateTime | 爬取时间 | 系统 | "2024-02-17 10:00:00" | 每次爬取更新 |
| crawl_status | String | 爬取状态 | 系统 | "success" | 每次爬取更新 |
| uploader | String | 上传人 | 系统 | "developer1" | 首次生成后不更新 |
| is_verified | Boolean | 是否验证 | 系统 | false | 验证后更新 |
| verification_time | DateTime | 验证时间 | 系统 | null | 验证后更新 |
| verification_note | String | 验证备注 | 系统 | "" | 验证后更新 |

### 数据来源说明
- 爬虫：直接从职位详情页爬取的数据
- 关联：从其他表关联获取的数据
- 提取：从描述或其他字段中提取的数据
- 生成：系统自动生成的数据
- 系统：系统运行时产生的数据

### 更新策略说明
1. 唯一标识字段（detail_id, unified_job_id, source_job_id, source）：首次生成后不更新
2. 详情信息字段：每次爬取时更新
3. 系统状态字段：根据具体操作更新

## 后续版本计划
1. 添加更多的数据清洗规则
2. 完善薪资解析算法
3. 添加职位分类标准化
4. 增加公司信息关联
5. 添加数据质量评分
6. 实现地理编码功能 