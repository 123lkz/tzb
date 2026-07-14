import { CloverApiProperty } from '@havenzhang/clover'

// 薪资行业排行数据项
export class SalaryIndustryRankItem {
  @CloverApiProperty({ description: '行业名称' })
  name: string

  @CloverApiProperty({ description: '薪资中位数' })
  value: number

  @CloverApiProperty({ description: '排名' })
  rank?: number
}

// 薪资行业数据结果
export class SalaryScreenIndustryResult {
  @CloverApiProperty({ description: '标准行业薪资中位数排行前100' })
  industryRankBySalary: SalaryIndustryRankItem[]

  @CloverApiProperty({ description: '三大产业薪资中位数排行' })
  threeIndustriesBySalary: SalaryIndustryRankItem[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

// 薪资总数据概览
export class SalaryScreenTotalResult {
  @CloverApiProperty({ description: '薪资25分位数' })
  p25Salary: number

  @CloverApiProperty({ description: '薪资50分位数' })
  p50Salary: number

  @CloverApiProperty({ description: '薪资75分位数' })
  p75Salary: number

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

// 薪资省份排行数据项
export class SalaryProvinceRankItem {
  @CloverApiProperty({ description: '省份名称' })
  name: string

  @CloverApiProperty({ description: '薪资中位数' })
  value: number

  @CloverApiProperty({ description: '排名' })
  rank: number
}

// 薪资省份排行结果
export class SalaryScreenProvinceResult {
  @CloverApiProperty({ description: '省份薪资中位数排行' })
  provinceData: SalaryProvinceRankItem[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

// 薪资职业排行数据项
export class SalaryCareerRankItem {
  @CloverApiProperty({ description: '职业名称' })
  name: string

  @CloverApiProperty({ description: '薪资中位数' })
  value: number

  @CloverApiProperty({ description: '排名' })
  rank: number
}

// 薪资职业排行结果
export class SalaryScreenCareerResult {
  @CloverApiProperty({ description: '小类职业薪资中位数排行' })
  standardXiaoleiRanking: SalaryCareerRankItem[]

  @CloverApiProperty({ description: '细类职业薪资中位数排行' })
  standardXileiRanking: SalaryCareerRankItem[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}

// 薪资分布数据项
export class SalaryDistributionItem {
  @CloverApiProperty({ description: '名称' })
  name: string

  @CloverApiProperty({ description: '招聘人数' })
  value: number
}

// 薪资分布结果
export class SalaryScreenDistributionResult {
  @CloverApiProperty({ description: '公司规模分布' })
  companySizeDistribution: SalaryDistributionItem[]

  @CloverApiProperty({ description: '学历要求分布' })
  educationDistribution: SalaryDistributionItem[]

  @CloverApiProperty({ description: '经验要求分布' })
  workingExpDistribution: SalaryDistributionItem[]

  @CloverApiProperty({ description: '数据更新时间' })
  updateTime: string
}
