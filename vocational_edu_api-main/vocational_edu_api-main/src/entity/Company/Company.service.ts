import { Injectable } from '@nestjs/common'
import { CompanyEntity } from './Company'
import { CompanyParams, CompanyTrendParams } from './Company.dto'

@Injectable()
export class CompanyService {
  // 简单的内存缓存
  private static memoryCache: { [key: string]: { data: any; timestamp: number } } | null = null
  private static readonly CACHE_DURATION = 300000 // 5分钟缓存

  /**
   * 获取公司趋势统计 - 按时间维度的公司数量统计
   */
  static async getTrendStats(params: CompanyTrendParams) {
    const cacheKey = `company_trend_${this.generateCacheKey(params)}`
    return this.getCachedOrExecute(cacheKey, () => this.executeTrendQuery(params))
  }

  /**
   * 获取省份公司统计
   */
  static async getProvinceStats(params: CompanyParams) {
    const cacheKey = `company_province_${this.generateCacheKey(params)}`
    return this.getCachedOrExecute(cacheKey, () => this.executeProvinceQuery(params))
  }

  /**
   * 获取公司规模统计
   */
  static async getSizeStats(params: CompanyParams) {
    const cacheKey = `company_size_${this.generateCacheKey(params)}`
    return this.getCachedOrExecute(cacheKey, () => this.executeSizeQuery(params))
  }

  /**
   * 获取公司职位统计 - 关联公司表和职位表
   */
  static async getPositionStats(params: CompanyParams) {
    const cacheKey = `company_position_${this.generateCacheKey(params)}`
    return this.getCachedOrExecute(cacheKey, () => this.executePositionStatsQuery(params))
  }

  /**
   * 统一的缓存处理逻辑
   */
  private static async getCachedOrExecute(cacheKey: string, executor: () => Promise<any>) {
    // 检查缓存
    if (this.memoryCache && this.memoryCache[cacheKey]) {
      const cached = this.memoryCache[cacheKey]
      if (Date.now() - cached.timestamp < this.CACHE_DURATION) {
        return cached.data
      }
    }

    // 执行查询
    const data = await executor()

    // 存储到内存缓存
    if (!this.memoryCache) {
      this.memoryCache = {}
    }
    this.memoryCache[cacheKey] = {
      data,
      timestamp: Date.now()
    }

    // 清理过期缓存
    this.cleanExpiredCache()

    return data
  }

  /**
   * 构建基础查询条件
   */
  private static buildBaseQuery(params: any): any {
    const baseQuery: any = {}
    if (params.province) {
      baseQuery.province = params.province
    }
    if (params.city) {
      baseQuery.city = params.city
    }
    if (params.industryCategory) {
      baseQuery.industry_category = params.industryCategory
    }
    if (params.companySize) {
      baseQuery.company_size = params.companySize
    }
    return baseQuery
  }

  /**
   * 构建时间查询条件
   */
  private static buildTimeQuery(params: any, trendType?: 'year' | 'month', useStringRange: boolean = false): any {
    const currentDate = new Date()
    const currentYear = currentDate.getFullYear()
    const currentMonth = currentDate.getMonth() + 1

    const toLower = (s: string) => (useStringRange ? s : new Date(s))

    // 根据 trendType 设置时间范围
    if (trendType) {
      if (trendType === 'year') {
        return {
          $gte: toLower('2020-01-01'),
          $lte: toLower(`${currentYear}-12-31 23:59:59`)
        }
      }
      return {
        $gte: toLower(`${currentYear}-01-01`),
        $lte: toLower(`${currentYear}-12-31 23:59:59`)
      }
    }

    // 根据参数设置时间范围，默认当前月
    if (params.selectedDate) {
      if (params.trendType === 'year') {
        const selectedYear = parseInt(params.selectedDate)
        return {
          $gte: toLower(`${selectedYear}-01-01`),
          $lte: toLower(`${selectedYear}-12-31 23:59:59`)
        }
      }
      return {
        $gte: toLower(`${params.selectedDate}-01`),
        $lte: toLower(`${params.selectedDate}-31 23:59:59`)
      }
    }

    // 默认当前月
    const currentMonthStr = `${currentYear}-${currentMonth.toString().padStart(2, '0')}`
    return {
      $gte: toLower(`${currentMonthStr}-01`),
      $lte: toLower(`${currentMonthStr}-31 23:59:59`)
    }
  }

  /**
   * 执行公司趋势统计查询
   */
  private static async executeTrendQuery(params: any) {
    const trendType: 'year' | 'month' = params.trendType || 'month'
    const baseQuery = this.buildBaseQuery(params)
    // 公司表 create_time 为 Date，维持 Date 过滤
    const timeQuery = this.buildTimeQuery(params, trendType, false)
    const query = { ...baseQuery, created_at: timeQuery }

    // 公司趋势统计的聚合管道
    const pipeline: any[] = [
      { $match: query },
      {
        $addFields: {
          timeKey:
            trendType === 'year'
              ? { $substr: [{ $dateToString: { date: '$created_at', format: '%Y-%m-%d' } }, 0, 4] }
              : { $substr: [{ $dateToString: { date: '$created_at', format: '%Y-%m-%d' } }, 0, 7] }
        }
      },
      {
        $group: {
          _id: '$timeKey',
          count: { $sum: 1 }
        }
      },
      { $sort: { _id: 1 } },
      { $limit: trendType === 'year' ? 10 : 24 }
    ]

    const result = await CompanyEntity.model.aggregate(pipeline)

    // 转换为返回格式
    const trend = result.map((item: any) => ({
      name: item._id,
      value: item.count
    }))

    return { trend }
  }

  /**
   * 执行省份公司统计查询
   */
  private static async executeProvinceQuery(params: any) {
    const baseQuery = this.buildBaseQuery(params)
    // 公司表 create_time 为 Date，维持 Date 过滤
    const timeQuery = this.buildTimeQuery(params, undefined, false)
    const query = { ...baseQuery, created_at: timeQuery }

    // 省份公司统计的聚合管道
    const pipeline: any[] = [
      { $match: query },
      {
        $group: {
          _id: '$province',
          count: { $sum: 1 }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 50 }
    ]

    const result = await CompanyEntity.model.aggregate(pipeline)

    // 转换为返回格式，添加排名
    const provinceDistribution = result.map((item: any, index: number) => ({
      name: item._id,
      value: item.count,
      rank: index + 1
    }))

    return { provinceDistribution }
  }

  /**
   * 执行公司规模统计查询
   */
  private static async executeSizeQuery(params: any) {
    const baseQuery = this.buildBaseQuery(params)
    // 公司表 create_time 为 Date，维持 Date 过滤
    const timeQuery = this.buildTimeQuery(params, undefined, false)
    const query = { ...baseQuery, created_at: timeQuery }

    // 公司规模统计的聚合管道
    const pipeline: any[] = [
      { $match: query },
      {
        $group: {
          _id: '$company_size',
          count: { $sum: 1 }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 20 }
    ]

    const result = await CompanyEntity.model.aggregate(pipeline)

    // 转换为返回格式，添加排名
    const sizeDistribution = result.map((item: any, index: number) => ({
      name: item._id || '未知',
      value: item.count,
      rank: index + 1
    }))

    return { sizeDistribution }
  }

  /**
   * 执行公司职位统计查询 - 关联公司表和职位表
   */
  private static async executePositionStatsQuery(params: any) {
    const baseQuery = this.buildBaseQuery(params)
    // Position 表 create_time 为字符串，改为字符串范围过滤
    const timeQuery = this.buildTimeQuery(params, undefined, true)
    const query = { ...baseQuery, create_time: timeQuery }

    // 并行执行三个统计查询
    const [positionCountResult, hiringCountResult, salaryMedianResult] = await Promise.all([
      this.getTopCompaniesByPositionCount(query),
      this.getTopCompaniesByHiringCount(query),
      this.getTopCompaniesBySalaryMedian(query)
    ])

    return {
      topCompaniesByPositionCount: positionCountResult,
      topCompaniesByHiringCount: hiringCountResult,
      topCompaniesBySalaryMedian: salaryMedianResult
    }
  }

  /**
   * 获取发布职位最多的公司前100
   */
  private static async getTopCompaniesByPositionCount(query: any) {
    const pipeline: any[] = [
      { $match: query },
      {
        $group: {
          _id: '$brandName',
          positionCount: { $sum: 1 }
        }
      },
      { $sort: { positionCount: -1 } },
      { $limit: 100 }
    ]
    console.log('pipeline', pipeline)
    const result = await CompanyEntity.model.aggregate(pipeline)
    // console.log('发布职位最多的公司前100', result);

    return result.map((item: any, index: number) => ({
      name: item._id,
      value: item.positionCount,
      rank: index + 1
    }))
  }

  /**
   * 获取按招聘人数最多的公司前100
   */
  private static async getTopCompaniesByHiringCount(query: any) {
    const pipeline: any[] = [
      { $match: query },
      {
        $group: {
          _id: '$brandName',
          hiringCount: { $sum: '$bossCert' }
        }
      },
      { $sort: { hiringCount: -1 } },
      { $limit: 100 }
    ]

    const result = await CompanyEntity.model.aggregate(pipeline)

    return result.map((item: any, index: number) => ({
      name: item._id,
      value: item.hiringCount,
      rank: index + 1
    }))
  }

  /**
   * 获取按薪资中位数最高的公司前100
   */
  private static async getTopCompaniesBySalaryMedian(query: any) {
    const pipeline: any[] = [
      { $match: query },
      {
        $addFields: {
          // 统一薪资单位为 千元/月 (K/月)
          normalizedSalaryK: {
            $let: {
              vars: {
                desc: { $toLower: { $toString: '$salaryDesc' } },
                num: {
                  $let: {
                    vars: {
                      m: {
                        $regexFind: {
                          input: { $toString: '$salaryDesc' },
                          regex: '([0-9]+\\.?[0-9]*)'
                        }
                      }
                    },
                    in: {
                      $convert: {
                        input: { $ifNull: ['$$m.match', null] },
                        to: 'double',
                        onError: 0,
                        onNull: 0
                      }
                    }
                  }
                }
              },
              in: {
                $switch: {
                  branches: [
                    // 元/天 -> 千元/月 (num * 22 / 1000)
                    {
                      case: { $regexMatch: { input: '$$desc', regex: '元/天|元每天' } },
                      then: { $divide: [{ $multiply: ['$$num', 22] }, 1000] }
                    },
                    // 元/小时 -> 千元/月 (num * 22 * 8 / 1000)
                    {
                      case: { $regexMatch: { input: '$$desc', regex: '元/小时|元每小时' } },
                      then: { $divide: [{ $multiply: ['$$num', 22, 8] }, 1000] }
                    },
                    // 万/年 -> 千元/月 (num * 10 / 12)
                    {
                      case: { $regexMatch: { input: '$$desc', regex: '万/年|万年薪|万每年' } },
                      then: { $divide: [{ $multiply: ['$$num', 10] }, 12] }
                    },
                    // 万/月 -> 千元/月 (num * 10)
                    {
                      case: { $regexMatch: { input: '$$desc', regex: '万/月|万每月' } },
                      then: { $multiply: ['$$num', 10] }
                    },
                    // 元/月 -> 千元/月 (num / 1000)
                    {
                      case: { $regexMatch: { input: '$$desc', regex: '元/月|元每月' } },
                      then: { $divide: ['$$num', 1000] }
                    },
                    // K/千/月 -> 直接使用
                    {
                      case: { $regexMatch: { input: '$$desc', regex: 'k|千|/月' } },
                      then: '$$num'
                    }
                  ],
                  default: 0
                }
              }
            }
          }
        }
      },
      {
        $group: {
          _id: '$brandName',
          salaries: { $push: '$normalizedSalaryK' }
        }
      },
      { $limit: 100 }
    ]

    const result = await CompanyEntity.model.aggregate(pipeline)

    // 在应用层计算中位数并排序
    const companiesWithMedian = result
      .map((item: any) => {
        const validSalaries = item.salaries
          .filter((s: number) => s > 0.5 && s <= 200) // 过滤异常薪资，范围 0.5K - 200K/月
          .sort((a: number, b: number) => a - b)

        if (validSalaries.length === 0) {
          return { name: item._id, median: 0, rank: 0 }
        }

        const median = this.calculateMedian(validSalaries)
        return { name: item._id, median, rank: 0 }
      })
      .filter((item: any) => item.median > 0)
      .sort((a: any, b: any) => b.median - a.median)
      .slice(0, 100)
      .map((item: any, index: number) => ({
        name: item.name,
        value: item.median,
        rank: index + 1
      }))

    return companiesWithMedian
  }

  /**
   * 计算中位数
   */
  private static calculateMedian(numbers: number[]): number {
    const sorted = numbers.sort((a, b) => a - b)
    const middle = Math.floor(sorted.length / 2)

    if (sorted.length % 2 === 0) {
      return (sorted[middle - 1] + sorted[middle]) / 2
    }
    return sorted[middle]
  }

  /**
   * 清理过期缓存
   */
  private static cleanExpiredCache() {
    if (!this.memoryCache) return

    const now = Date.now()
    const expiredKeys = Object.keys(this.memoryCache).filter(
      (key) => now - this.memoryCache![key].timestamp > this.CACHE_DURATION
    )

    expiredKeys.forEach((key) => delete this.memoryCache![key])
  }

  /**
   * 生成缓存键
   */
  private static generateCacheKey(params: any): string {
    return `company_data:${JSON.stringify(params)}`
  }
}
