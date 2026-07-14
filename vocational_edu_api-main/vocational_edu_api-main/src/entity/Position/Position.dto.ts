import { CloverApiProperty, Joi } from '@havenzhang/clover'

// 分页查询参数
export class PositionListParams {
  @CloverApiProperty({ description: '页码', validator: Joi.number().min(1).default(1) })
  page: number = 1

  @CloverApiProperty({
    description: '每页数量',
    validator: Joi.number().min(1).max(100).default(20)
  })
  pageSize: number = 20

  @CloverApiProperty({
    description: '排序字段',
    validator: Joi.string().valid('recruitNumber', 'publishTime').default('publishTime')
  })
  sortField: 'recruitNumber' | 'publishTime'

  @CloverApiProperty({
    description: '排序方向',
    validator: Joi.string().valid('asc', 'desc').default('desc')
  })
  sortOrder: 'asc' | 'desc' = 'desc'

  @CloverApiProperty({ description: '职位名称', validator: Joi.string().optional() })
  name?: string

  @CloverApiProperty({ description: '公司名称', validator: Joi.string().optional() })
  companyName?: string

  @CloverApiProperty({ description: '省份', validator: Joi.string().optional() })
  province?: string

  @CloverApiProperty({ description: '学历要求', validator: Joi.string().optional() })
  education?: string

  @CloverApiProperty({ description: '工作经验要求', validator: Joi.string().optional() })
  workingExp?: string

  @CloverApiProperty({ description: '职位分类', validator: Joi.string().optional() })
  classify?: string

  @CloverApiProperty({ description: '月份过滤 (格式: YYYY-MM)', validator: Joi.string().optional() })
  date?: string
}

// 职位列表项
export class PositionListItem {
  @CloverApiProperty({ description: '职位ID' })
  _id: string

  @CloverApiProperty({ description: '职位名称' })
  jobName: string

  @CloverApiProperty({ description: '省份' })
  province: string

  @CloverApiProperty({ description: '城市' })
  jobClassify: string

  @CloverApiProperty({ description: '公司名称' })
  companyName: string

  @CloverApiProperty({ description: '学历要求' })
  education: string

  @CloverApiProperty({ description: '工作经验要求' })
  workingExp: string

  @CloverApiProperty({ description: '发布时间' })
  publishTime: string

  @CloverApiProperty({ description: '招聘人数' })
  recruitNumber: number

  @CloverApiProperty({ description: '原始薪资区间和薪资倍数字符串' })
  salary60: string

  @CloverApiProperty({ description: '薪资区间和薪资字符串' })
  salaryReal: string

  @CloverApiProperty({ description: '职位URL' })
  positionUrl: string
}

// 分页结果
export class PositionListResult {
  @CloverApiProperty({ description: '职位列表', type: [PositionListItem] })
  items: PositionListItem[]

  @CloverApiProperty({ description: '总数量' })
  total: number

  @CloverApiProperty({ description: '当前页码' })
  page: number

  @CloverApiProperty({ description: '每页数量' })
  pageSize: number

  @CloverApiProperty({ description: '总页数' })
  totalPages: number

  @CloverApiProperty({ description: '是否有下一页' })
  hasNext: boolean

  @CloverApiProperty({ description: '是否有上一页' })
  hasPrev: boolean
}

// 数据大屏返回结果
export class PositionScreenTrendResult {
  @CloverApiProperty({ description: '月份/年份' })
  months: string[]
  @CloverApiProperty({ description: '职位数' })
  positions: number[]
  @CloverApiProperty({ description: '招聘人数' })
  recruitment: number[]
  @CloverApiProperty({ description: '招聘单位数' })
  companies: number[]
  @CloverApiProperty({ description: '职位数变化率' })
  positionChangeRate: number[]
  @CloverApiProperty({ description: '招聘人数变化率' })
  recruitmentChangeRate: number[]
  @CloverApiProperty({ description: '招聘单位数变化率' })
  companyChangeRate: number[]
}

export class PositionScreenTotalResult {
  @CloverApiProperty({ description: '总职位数' })
  totalPositions: number
  @CloverApiProperty({ description: '总招聘人数' })
  totalRecruitment: number
  @CloverApiProperty({ description: '总招聘单位数' })
  totalCompanies: number
}

// 数据大屏省份数据返回结果
export class PositionScreenProvinceResult {
  @CloverApiProperty({ description: '省份分布数据' })
  provinceData: {
    name: string
    value: number
    rank: number
    recruitmentRank: number
    recruitment: number
    companyCount: number
    standardJobCount: number
  }[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

// 分布数据统计结果
export class PositionDistributionResult {
  @CloverApiProperty({ description: '学历要求分布' })
  educationRequirement?: { name: string; value: number }[]

  @CloverApiProperty({ description: '经验要求分布' })
  workingExpRequirement?: { name: string; value: number }[]

  @CloverApiProperty({ description: '公司规模分布' })
  companySizeDistribution?: { name: string; value: number }[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

export class PositionScreenIndustryResult {
  @CloverApiProperty({ description: '标准行业排行前100（招聘人数）' })
  industryMediumByRecruitNumber: {
    name: string
    value: number
    rank: number
  }[]

  @CloverApiProperty({ description: '三大产业' })
  threeIndustryByRecruitNumber: {
    name: string
    value: number
  }[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

export class PositionScreenCareerRankResult {
  @CloverApiProperty({ description: '职业排行数据' })
  xiaoleiByRecruitNumber: {
    name: string
    value: number
    rank: number
  }[]
  @CloverApiProperty({ description: '职业排行数据' })
  xileiByRecruitNumber: {
    name: string
    value: number
    rank: number
  }[]
  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}
