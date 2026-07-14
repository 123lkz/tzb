import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class CompanyTrendParams {
  @CloverApiProperty({ description: '省份名称', validator: Joi.string().format('text').max(50) })
  province?: string

  @CloverApiProperty({ description: '城市名称', validator: Joi.string().format('text').max(50) })
  city?: string

  @CloverApiProperty({ description: '时间类型', validator: Joi.string().format('text').max(50) })
  trendType?: 'year' | 'month'

  @CloverApiProperty({ description: '公司规模', validator: Joi.string().format('text').max(50) })
  companySize?: string
}

export class CompanyParams extends CompanyTrendParams {
  @CloverApiProperty({ description: '日期', validator: Joi.string().format('text').max(50) })
  selectedDate?: string
}

export class CompanyResultItem {
  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(50) })
  name: string

  @CloverApiProperty({ description: '数量', validator: Joi.number().min(0) })
  value: number

  @CloverApiProperty({ description: '排名', validator: Joi.number().min(0) })
  rank?: number
}

export class CompanyTrendResult {
  @CloverApiProperty({ description: '月度/年度公司数量统计', type: [CompanyResultItem] })
  trend: Array<CompanyResultItem>
}

export class CompanyProvinceResult {
  @CloverApiProperty({ description: '省份公司分布', type: [CompanyResultItem] })
  provinceDistribution: Array<CompanyResultItem>
}

export class CompanySizeResult {
  @CloverApiProperty({ description: '公司规模分布', type: [CompanyResultItem] })
  sizeDistribution: Array<CompanyResultItem>
}

export class CompanyEducationResult {
  @CloverApiProperty({ description: '学历要求分布', type: [CompanyResultItem] })
  educationDistribution: Array<CompanyResultItem>
}

export class CompanyPositionStatsResult {
  @CloverApiProperty({ description: '发布职位最多的公司前100', type: [CompanyResultItem] })
  topCompaniesByPositionCount: Array<CompanyResultItem>

  @CloverApiProperty({ description: '按招聘人数最多的公司前100', type: [CompanyResultItem] })
  topCompaniesByHiringCount: Array<CompanyResultItem>

  @CloverApiProperty({ description: '按薪资中位数最高的公司前100', type: [CompanyResultItem] })
  topCompaniesBySalaryMedian: Array<CompanyResultItem>
}
