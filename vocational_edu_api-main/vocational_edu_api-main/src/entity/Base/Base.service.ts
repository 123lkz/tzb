import { Injectable } from '@nestjs/common'
import {
  createPositionModel1,
  createPositionModel2,
  createPositionModel3,
  createPositionModel4,
  PositionSchema1,
  PositionSchema2,
  PositionSchema3,
  PositionSchema4
} from '../../base/entity/Position/Position.model'
import { CacheService } from '../../services/CacheService'
import { connections } from '../../utils/DatabaseUtils'
import { PositionScreenTrendResult } from '../Position/Position.dto'
import { PositionService } from '../Position/Position.service'
import { SchoolEnrollmentService } from '../SchoolEnrollment/SchoolEnrollment.service'
import { BaseQueryParams } from './Base.dto'

/**
 * 基础数据服务
 * 统一管理 Position 和 Salary 共用的 base 缓存和查询
 * 支持4种查询条件组合的缓存管理
 * 优化 MongoDB 查询，避免重复查询相同条件的数据
 */
@Injectable()
export class BaseService {
  private static cacheService: CacheService
  private static positionService: PositionService

  constructor() {
    if (!BaseService.cacheService) {
      BaseService.cacheService = CacheService.getInstance()
    }
    if (!BaseService.positionService) {
      BaseService.positionService = new PositionService()
    }
  }

  /**
   * 获取缓存服务实例（确保单例）
   */
  public static getCacheService(): CacheService {
    if (!BaseService.cacheService) {
      BaseService.cacheService = CacheService.getInstance()
    }
    return BaseService.cacheService
  }

  /**
   * 定义4种查询条件组合
   */
  public static readonly CACHE_COMBINATIONS: BaseQueryParams[] = [
    { dateType: 'month', caliberType: 'all' }, // 月度全口径
    { dateType: 'month', caliberType: 'college' }, // 月度应届大专生
    { dateType: 'year', caliberType: 'all' }, // 年度全口径
    { dateType: 'year', caliberType: 'college' } // 年度应届大专生
  ]

  /**
   * 获取当前日期字符串 (YYYY-MM-DD)
   * 注意：使用本地时间而不是UTC时间，确保日期正确
   */
  private static getCurrentDateString(): string {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  /**
   * 生成缓存键（包含日期标识）
   */
  public static generateCacheKey(params: BaseQueryParams, date?: string): string {
    const dateStr = date || this.getCurrentDateString()
    return `base:${dateStr}:${params.dateType}:${params.caliberType}`
  }

  /**
   * 生成昨天的缓存键
   */
  private static generateYesterdayCacheKey(params: BaseQueryParams): string {
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    // 使用本地时间而不是UTC时间，确保与getCurrentDateString()保持一致
    const year = yesterday.getFullYear()
    const month = String(yesterday.getMonth() + 1).padStart(2, '0')
    const day = String(yesterday.getDate()).padStart(2, '0')
    const yesterdayStr = `${year}-${month}-${day}`
    return this.generateCacheKey(params, yesterdayStr)
  }

  /**
   * 获取基础数据（优先从今天缓存获取，如果今天缓存未命中，则从昨天缓存获取，如果昨天缓存未命中，则返回null）
   */
  static async getBase(params: BaseQueryParams): Promise<any> {
    const currentDate = this.getCurrentDateString()
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    // 使用本地时间而不是UTC时间，确保与getCurrentDateString()保持一致
    const year = yesterday.getFullYear()
    const month = String(yesterday.getMonth() + 1).padStart(2, '0')
    const day = String(yesterday.getDate()).padStart(2, '0')
    const yesterdayStr = `${year}-${month}-${day}`

    // 1. 先尝试获取今天的缓存
    const todayCacheKey = this.generateCacheKey(params, currentDate)
    console.log(`🔍 尝试获取今天缓存: ${todayCacheKey}`)
    try {
      const todayCachedData = await this.getCacheService().get(todayCacheKey)
      if (todayCachedData) {
        // todayCachedData已经是解析后的对象，不需要再次JSON.parse
        const parsedData = todayCachedData as any
        console.log('📊 今天缓存数据信息:')
        console.log(`   - 缓存key: ${parsedData.cacheKey || 'N/A'}`)
        console.log(`   - 数据键数量: ${Object.keys(parsedData).length}`)
        console.log(`   - 包含totalStats: ${!!parsedData.totalStats}`)

        // 验证缓存时间是否为今天
        if (parsedData.cacheKey && parsedData.cacheKey.includes(currentDate)) {
          console.log(`✅ 使用今天缓存数据: ${todayCacheKey}`)
          return parsedData
        }
        console.log(`⚠️ 今天缓存key不匹配，缓存key: ${parsedData.cacheKey}, 期望key日期: ${currentDate}`)
      } else {
        console.log(`📭 今天缓存不存在: ${todayCacheKey}`)
      }
    } catch (error) {
      console.warn(`❌ 获取今天缓存失败: ${error.message}`)
    }

    const yesterdayCacheKey = this.generateCacheKey(params, yesterdayStr)
    console.log(`🔍 尝试获取昨天缓存: ${yesterdayCacheKey}`)
    try {
      const yesterdayCachedData = await this.getCacheService().get(yesterdayCacheKey)
      if (yesterdayCachedData) {
        // yesterdayCachedData已经是解析后的对象，不需要再次JSON.parse
        const parsedData = yesterdayCachedData as any
        console.log('📊 昨天缓存数据信息:')
        console.log(`   - 缓存时间: ${parsedData.cacheTime || 'N/A'}`)
        console.log(`   - 数据键数量: ${Object.keys(parsedData).length}`)
        console.log(`   - 包含totalStats: ${!!parsedData.totalStats}`)

        if (parsedData.cacheTime && parsedData.cacheTime.startsWith(yesterdayStr)) {
          console.log(`✅ 使用昨天缓存数据: ${yesterdayCacheKey}`)
          return parsedData
        }
        console.log(`⚠️ 昨天缓存时间不匹配，缓存时间: ${parsedData.cacheTime}, 期望: ${yesterdayStr}`)
      } else {
        console.log(`📭 昨天缓存不存在: ${yesterdayCacheKey}`)
      }
    } catch (error) {
      console.warn(`❌ 获取昨天缓存失败: ${error.message}`)
    }

    return null
  }

  /**
   * 根据查询参数创建临时表
   */
  private static async createTempTablesByQuery(params: BaseQueryParams): Promise<boolean> {
    const startTime = Date.now()
    console.log('📊 开始根据查询参数创建临时表...')

    try {
      // 获取所有4个模型，用于从原始集合中并行读取数据
      const models = this.getPositionModels()
      const [positionModel1, positionModel2, positionModel3, positionModel4] = models
      const tempBasePipeline = this.buildTempBasePipeline(params)

      console.log('🔨 开始创建基础临时表结构...')
      await positionModel1.aggregate(tempBasePipeline).allowDiskUse(true)

      const mergePipeline = this.buildMergePipeline(params)
      const mergeResults = await Promise.allSettled([
        positionModel2.aggregate(mergePipeline).allowDiskUse(true),
        positionModel3.aggregate(mergePipeline).allowDiskUse(true),
        positionModel4.aggregate(mergePipeline).allowDiskUse(true)
      ])

      await this.cleanupTempFiles()

      const totalTime = Date.now() - startTime
      console.log(`📊 临时表创建完成，总耗时: ${totalTime}ms`)
      return true
    } catch (error) {
      const totalTime = Date.now() - startTime
      console.error(`❌ 临时表创建失败，耗时: ${totalTime}ms`, error)
      throw error
    }
  }

  /**
   * 清理临时文件
   */
  private static async cleanupTempFiles(): Promise<void> {
    try {
      const models = this.getPositionModels()
      const [positionModel1] = models
      const db = positionModel1.db

      // 获取所有临时集合
      const collections = db.collections
      const tempCollections = Object.values(collections).filter((col: any) =>
        col.collectionName.match(/^tmp\.agg_out\./)
      )

      for (const collection of tempCollections) {
        try {
          await (collection as any).drop()
          console.log(`🧹 清理临时文件: ${(collection as any).collectionName}`)
        } catch (error) {
          console.warn(`⚠️ 清理临时文件失败: ${(collection as any).collectionName}`, (error as any).message)
        }
      }
    } catch (error) {
      console.warn('⚠️ 清理临时文件过程失败:', error.message)
    }
  }

  /**
   * 使用优化的聚合方案计算并缓存基础数据
   * 性能优化：减少查询次数，简化聚合管道，优化索引使用
   */
  private static async initCacheBaseData(params: BaseQueryParams): Promise<any> {
    const cacheKey = this.generateCacheKey(params)
    const currentDate = this.getCurrentDateString()
    console.log('===> Base.service.ts:185 ~ cacheKey', cacheKey)
    console.log('===> Base.service.ts:186 ~ currentDate', currentDate)

    try {
      const [tempTableResult, trendDataResult] = await Promise.allSettled([
        this.createTempTablesByQuery(params),
        this.getLeftTrendData(params)
      ])

      // 检查趋势数据获取结果
      if (trendDataResult.status === 'rejected') {
        console.error('❌ 获取趋势数据失败:', trendDataResult.reason)
      } else {
        this.logTaskResult('职位趋势数据', trendDataResult.value)
      }

      // 检查临时表创建结果
      if (tempTableResult.status === 'rejected') {
        console.error('❌ 创建临时表失败:', tempTableResult.reason)
      } else {
        console.log('✅ 临时表创建成功')
      }

      // 从临时表获取统计数据
      const tempTableStats = await this.getStatisticsFromTempTable(params)

      // 获取学校招生数据
      const schoolEnrollmentData = await this.getSchoolEnrollmentData()

      const base = {
        trendData: trendDataResult.status === 'fulfilled' ? trendDataResult.value : {},
        schoolEnrollmentData,
        ...tempTableStats,
        params,
        cacheTime: new Date().toISOString(),
        cacheKey
      }

      // 缓存结果（永久缓存）
      try {
        const cacheResult = await this.getCacheService().set(cacheKey, base, 0)
        if (!cacheResult) {
          console.error(`❌ 缓存保存失败: ${cacheKey}`)
          throw new Error(`缓存保存失败: ${cacheKey}`)
        }
        console.log(`✅ 永久缓存保存成功: ${cacheKey}`)
      } catch (cacheError) {
        console.error(`❌ 缓存保存异常: ${cacheKey}`, cacheError)
        throw new Error(`缓存保存异常: ${cacheError.message}`)
      }
      return base
    } catch (error) {
      console.error('❌ 缓存数据初始化失败:', error)
      throw error
    }
  }

  /**
   * 从临时表获取所有统计数据
   */
  private static async getStatisticsFromTempTable(params: BaseQueryParams): Promise<{
    totalStats: {
      totalPositions: number
      totalCompanies: number
      totalRecruitNumber: number
    }
    salaryQuantiles: {
      p25: number
      p50: number
      p75: number
    }
    educationDistribution: any
    workingExpDistribution: any
    provinceStats: {
      byRecruitNumber: any[]
      bySalary: any[]
    }
    companySizeDistribution: any[]
    industryStats: {
      industryMediumByRecruitNumber: any[]
      industryMediumBySalary: any[]
      threeIndustryByRecruitNumber: any[]
      threeIndustryBySalary: any[]
    }
    careerStats: {
      xiaoleiByRecruitNumber: any[]
      xiaoleiBySalary: any[]
      xileiByRecruitNumber: any[]
      xileiBySalary: any[]
    }
  }> {
    const statisticsStartTime = Date.now()
    console.log('📊 开始从临时表获取统计数据...')

    // 创建带时间统计和重试机制的包装函数
    const withTimingAndRetry = async <T>(name: string, fn: () => Promise<T>, maxRetries: number = 1): Promise<T> => {
      let lastError: any

      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const startTime = Date.now()
        try {
          const result = await fn()
          const duration = Date.now() - startTime
          const attemptText = attempt > 0 ? ` (重试第${attempt}次)` : ''
          console.log(`✅ ${name}${attemptText}: ${duration}ms`)

          // 立即输出任务结果摘要
          this.logTaskResult(name, result)

          return result
        } catch (error) {
          const duration = Date.now() - startTime
          lastError = error
          const attemptText = attempt > 0 ? ` (重试第${attempt}次失败)` : ' (失败)'
          console.log(`❌ ${name}${attemptText}: ${duration}ms - ${error.message}`)

          if (attempt < maxRetries) {
            console.log(`🔄 ${name} 准备重试...`)
            // 等待1秒后重试
            await new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      }

      throw lastError
    }

    // 定义所有统计任务
    const statisticsTasks = [
      { name: '基础统计', fn: () => this.getTotalStats(params) },
      { name: '薪资分位数', fn: () => this.getSalaryQuantilesStats(params) },
      { name: '学历分布', fn: () => this.getEducationDistribution(params) },
      { name: '工作经验分布', fn: () => this.getWorkingExpDistribution(params) },
      { name: '省份统计', fn: () => this.getProvinceStats(params) },
      { name: '公司规模分布', fn: () => this.getCompanySizeDistribution(params) },
      { name: '行业统计', fn: () => this.getStandardIndustryStats(params) },
      { name: '职业中类、小类统计', fn: () => this.getStandardCareerStats(params) }
    ]

    // 执行基础统计和优化的关联查询
    console.log('🚀 开始并行执行所有统计查询...')
    const results = await Promise.allSettled(statisticsTasks.map((task) => withTimingAndRetry(task.name, task.fn)))

    console.log('📊 所有统计查询完成，开始处理结果...')

    // 处理结果并记录详细信息
    const processedResults = {
      totalStats:
        results[0].status === 'fulfilled'
          ? results[0].value
          : { totalPositions: 0, totalCompanies: 0, totalRecruitNumber: 0 },
      salaryQuantiles: results[1].status === 'fulfilled' ? results[1].value : { p25: 0, p50: 0, p75: 0 },
      educationDistribution: results[2].status === 'fulfilled' ? results[2].value : {},
      workingExpDistribution: results[3].status === 'fulfilled' ? results[3].value : {},
      provinceStats: results[4].status === 'fulfilled' ? results[4].value : { byRecruitNumber: [], bySalary: [] },
      companySizeDistribution: results[5].status === 'fulfilled' ? results[5].value : [],
      industryStats:
        results[6].status === 'fulfilled'
          ? results[6].value
          : {
              industryMediumByRecruitNumber: [],
              industryMediumBySalary: [],
              threeIndustryByRecruitNumber: [],
              threeIndustryBySalary: []
            },
      careerStats:
        results[7].status === 'fulfilled'
          ? results[7].value
          : {
              xiaoleiByRecruitNumber: [],
              xiaoleiBySalary: [],
              xileiByRecruitNumber: [],
              xileiBySalary: []
            }
    }

    // 统计成功和失败的任务
    const successCount = results.filter((r) => r.status === 'fulfilled').length
    const failureCount = results.filter((r) => r.status === 'rejected').length

    console.log(`📊 统计任务完成情况: ${successCount}个成功, ${failureCount}个失败`)

    // 打印最终结果摘要
    console.log('📋 最终统计结果摘要:')
    console.log(`  - 总职位数: ${processedResults.totalStats.totalPositions}`)
    console.log(`  - 总公司数: ${processedResults.totalStats.totalCompanies}`)
    console.log(`  - 总招聘数: ${processedResults.totalStats.totalRecruitNumber}`)
    console.log(`  - 薪资中位数: ${processedResults.salaryQuantiles.p50}`)
    console.log(`  - 省份统计数量: ${processedResults.provinceStats.byRecruitNumber.length}`)
    console.log(`  - 公司规模分布数量: ${processedResults.companySizeDistribution.length}`)
    console.log(`  - 行业统计数量: ${processedResults.industryStats.industryMediumByRecruitNumber.length}`)
    console.log(`  - 职业统计数量: ${processedResults.careerStats.xiaoleiByRecruitNumber.length}`)

    const statisticsTime = Date.now() - statisticsStartTime
    console.log(`📊 统计数据获取完成，总耗时: ${statisticsTime}ms`)

    return processedResults
  }

  /**
   * 输出任务结果摘要日志
   */
  private static logTaskResult(taskName: string, result: any): void {
    try {
      switch (taskName) {
        case '职位趋势数据':
          console.log(`📋 ${taskName}结果: 详情：${JSON.stringify(result)}`)
          break
        case '基础统计':
          console.log(
            `📋 ${taskName}结果: 职位数=${result.totalPositions}, 公司数=${result.totalCompanies}, 招聘数=${result.totalRecruitNumber}`
          )
          break
        case '薪资分位数':
          console.log(`📋 ${taskName}结果: P25=${result.p25}, P50=${result.p50}, P75=${result.p75}`)
          break
        case '学历分布':
          console.log(`📋 ${taskName}结果: 共${result.length}个学历分类，详情：${JSON.stringify(result)}`)
          break
        case '工作经验分布':
          console.log(`📋 ${taskName}结果: 共${result.length}个经验分类，详情：${JSON.stringify(result)}`)
          break
        case '省份统计':
          console.log(
            `📋 ${taskName}结果: 按招聘人数排序${result.byRecruitNumber.length}个省份, 按薪资中位数排序${result.bySalary.length}个省份，详情：${JSON.stringify(result)}`
          )
          break
        case '公司规模分布':
          console.log(`📋 ${taskName}结果: 共${result.length}个公司规模分类，详情：${JSON.stringify(result)}`)
          break
        case '行业统计':
          console.log(
            `📋 ${taskName}结果: 行业中类${result.industryMediumByRecruitNumber.length}个, 三大产业${result.threeIndustryByRecruitNumber.length}个，详情：${JSON.stringify(result)}`
          )
          break
        case '职业中类、小类统计':
          console.log(
            `📋 ${taskName}结果: 小类${result.xiaoleiByRecruitNumber.length}个, 中类${result.xileiByRecruitNumber.length}个，详情：${JSON.stringify(result)}`
          )
          break
        default:
          console.log(`📋 ${taskName}结果: 执行完成`)
      }
    } catch (error) {
      console.log(`📋 ${taskName}结果: 日志输出失败 - ${error.message}`)
    }
  }

  /**
   * 从临时表获取基础统计数据
   */
  private static async getTotalStats(params: BaseQueryParams): Promise<{
    totalPositions: number
    totalCompanies: number
    totalRecruitNumber: number
  }> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    const result = await db
      .collection(tempTableName)
      .aggregate([
        {
          $group: {
            _id: null,
            totalPositions: { $sum: 1 },
            totalCompanies: { $addToSet: '$companyName' },
            totalRecruitNumber: { $sum: '$recruitNumber' }
          }
        },
        {
          $project: {
            _id: 0,
            totalPositions: 1,
            totalCompanies: { $size: '$totalCompanies' },
            totalRecruitNumber: 1
          }
        }
      ])
      .toArray()

    return (result[0] as any) || { totalPositions: 0, totalCompanies: 0, totalRecruitNumber: 0 }
  }

  /**
   * 从临时表获取薪资分位数统计（使用抽样提高性能）
   */
  private static async getSalaryQuantilesStats(params: BaseQueryParams): Promise<{
    p25: number
    p50: number
    p75: number
  }> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    console.log(`📊 开始获取薪资分位数统计，临时表: ${tempTableName}`)

    try {
      // 方法1: 使用分桶聚合计算近似分位数（推荐）
      const bucketResult = await db
        .collection(tempTableName)
        .aggregate(
          [
            { $match: { salary: { $gt: 0 } } },
            {
              $bucket: {
                groupBy: '$salary',
                boundaries: [
                  0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000, 15000, 18000, 20000, 25000,
                  30000, 35000, 40000, 50000, 60000, 80000, 100000, 150000, 200000, 500000, 1000000
                ],
                default: 'other',
                output: {
                  count: { $sum: 1 },
                  minSalary: { $min: '$salary' },
                  maxSalary: { $max: '$salary' }
                }
              }
            },
            { $sort: { _id: 1 } }
          ],
          { allowDiskUse: true }
        )
        .toArray()

      console.log(`📊 薪资分桶统计完成，桶数量: ${bucketResult.length}`)

      if (bucketResult.length === 0) {
        console.log('⚠️ 没有找到有效薪资数据')
        return { p25: 0, p50: 0, p75: 0 }
      }

      // 计算总数量和累积分布
      const totalCount = bucketResult.reduce((sum: number, bucket: any) => sum + bucket.count, 0)
      console.log(`📊 总薪资记录数: ${totalCount}`)

      let cumulativeCount = 0
      const buckets = bucketResult.map((bucket: any) => {
        cumulativeCount += bucket.count
        return {
          ...bucket,
          cumulativeCount,
          cumulativePercent: cumulativeCount / totalCount
        }
      })

      // 计算分位数
      const calculateQuantile = (percentile: number): number => {
        for (let i = 0; i < buckets.length; i++) {
          if (buckets[i].cumulativePercent >= percentile) {
            const currentBucket = buckets[i] as any

            // 如果当前桶的累积百分比刚好等于目标百分位，返回桶的中位数
            if (buckets[i].cumulativePercent === percentile) {
              return Math.round((currentBucket.minSalary + currentBucket.maxSalary) / 2)
            }

            // 线性插值
            const prevBucket =
              i > 0 ? (buckets[i - 1] as any) : { cumulativePercent: 0, maxSalary: currentBucket.minSalary }

            const bucketStartPercent = prevBucket.cumulativePercent
            const bucketEndPercent = currentBucket.cumulativePercent
            const bucketRange = bucketEndPercent - bucketStartPercent
            const positionInBucket = (percentile - bucketStartPercent) / bucketRange

            // 在当前桶的薪资范围内进行线性插值
            const salaryRange = currentBucket.maxSalary - currentBucket.minSalary
            const interpolatedSalary = currentBucket.minSalary + salaryRange * positionInBucket

            return Math.round(interpolatedSalary)
          }
        }

        return Math.round((buckets[buckets.length - 1] as any).maxSalary)
      }

      const result = {
        p25: calculateQuantile(0.25),
        p50: calculateQuantile(0.5),
        p75: calculateQuantile(0.75)
      }

      console.log(`✅ 薪资分位数计算完成: P25=${result.p25}, P50=${result.p50}, P75=${result.p75}`)
      return result
    } catch (error) {
      console.error('❌ 分桶方法失败，尝试抽样方法:', error)

      // 降级方案：使用抽样方法
      try {
        const sampleResult = await db
          .collection(tempTableName)
          .aggregate(
            [
              { $match: { salary: { $gt: 0 } } },
              { $sample: { size: 100000 } },
              {
                $group: {
                  _id: null,
                  salaries: { $push: '$salary' },
                  count: { $sum: 1 }
                }
              }
            ],
            { allowDiskUse: true }
          )
          .toArray()

        if (sampleResult.length === 0) {
          return { p25: 0, p50: 0, p75: 0 }
        }

        const salaries = sampleResult[0].salaries.sort((a: number, b: number) => a - b)
        const count = salaries.length

        const calculateQuantile = (percentile: number): number => {
          const index = Math.floor(count * percentile)
          return salaries[Math.min(index, count - 1)]
        }

        const result = {
          p25: calculateQuantile(0.25),
          p50: calculateQuantile(0.5),
          p75: calculateQuantile(0.75)
        }

        console.log(`✅ 抽样方法计算完成: P25=${result.p25}, P50=${result.p50}, P75=${result.p75}`)
        return result
      } catch (sampleError) {
        console.error('❌ 抽样方法也失败了:', sampleError)
        return { p25: 0, p50: 0, p75: 0 }
      }
    }
  }

  /**
   * 从临时表获取职业中类、小类统计
   */
  private static async getStandardCareerStats(params: BaseQueryParams): Promise<{
    xiaoleiByRecruitNumber: any[]
    xiaoleiBySalary: any[]
    xileiByRecruitNumber: any[]
    xileiBySalary: any[]
  }> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    try {
      // 先获取职业映射表统计信息
      const occupationMap = await this.getOccupationMapping(db)

      // 减少批次大小，降低内存使用
      const batchSize = 20000 // 从50000减少到20000
      let skip = 0
      const xiaoleiResults: Record<
        string,
        {
          count: number
          recruitNumber: number
          salaryValues: number[]
          xiaoleiCode: string
        }
      > = {}
      const xileiResults: Record<
        string,
        {
          count: number
          recruitNumber: number
          salaryValues: number[]
          xileiCode: string
        }
      > = {}

      while (true) {
        const positions = await db
          .collection(tempTableName)
          .find({}, { projection: { classify: 1, recruitNumber: 1, salary: 1 } })
          .skip(skip)
          .limit(batchSize)
          .toArray()

        if (positions.length === 0) break

        // 在内存中关联职业分类
        positions.forEach((position: any) => {
          const occupationInfo = occupationMap[position.classify]
          if (occupationInfo) {
            const xiaoleiName = occupationInfo.xiaoleiName
            const xiaoleiCode = occupationInfo.xiaoleiCode
            const xileiName = occupationInfo.xileiName
            const xileiCode = occupationInfo.xileiCode

            // 处理 xiaolei 数据
            if (!xiaoleiResults[xiaoleiName]) {
              xiaoleiResults[xiaoleiName] = {
                count: 0,
                recruitNumber: 0,
                salaryValues: [],
                xiaoleiCode: xiaoleiCode
              }
            }
            xiaoleiResults[xiaoleiName].recruitNumber += position.recruitNumber || 0
            if (position.salary > 0) {
              xiaoleiResults[xiaoleiName].salaryValues.push(position.salary)
            }

            // 处理 xilei 数据
            if (!xileiResults[xileiName]) {
              xileiResults[xileiName] = {
                count: 0,
                recruitNumber: 0,
                salaryValues: [],
                xileiCode: xileiCode
              }
            }
            xileiResults[xileiName].recruitNumber += position.recruitNumber || 0
            if (position.salary > 0) {
              xileiResults[xileiName].salaryValues.push(position.salary)
            }
          }
        })

        skip += positions.length
      }

      // 计算薪资中位数并转换为数组格式
      const calculateMedianSalary = (salaryValues: number[]): number => {
        const sortedSalaries = salaryValues.sort((a, b) => a - b)
        if (sortedSalaries.length === 0) return 0
        const mid = Math.floor(sortedSalaries.length / 2)
        return sortedSalaries.length % 2 === 0
          ? Math.round((sortedSalaries[mid - 1] + sortedSalaries[mid]) / 2)
          : sortedSalaries[mid]
      }

      // 处理 xiaolei 数据
      const xiaoleiFinalResult = Object.entries(xiaoleiResults)
        .map(([xiaoleiName, stats]) => ({
          xiaoleiName,
          xiaoleiCode: stats.xiaoleiCode,
          totalRecruitNumber: stats.recruitNumber,
          medianSalary: calculateMedianSalary(stats.salaryValues)
        }))
        .sort((a, b) => b.totalRecruitNumber - a.totalRecruitNumber)

      // 处理 xilei 数据
      const xileiFinalResult = Object.entries(xileiResults)
        .map(([xileiName, stats]) => ({
          xileiName,
          xileiCode: stats.xileiCode,
          totalRecruitNumber: stats.recruitNumber,
          medianSalary: calculateMedianSalary(stats.salaryValues)
        }))
        .sort((a, b) => b.totalRecruitNumber - a.totalRecruitNumber)

      // xiaolei 按招聘人数排行前40
      const xiaoleiByRecruitNumber = xiaoleiFinalResult
        .map((item, index) => ({
          name: item.xiaoleiName,
          value: item.totalRecruitNumber,
          rank: index + 1
        }))
        .slice(0, 40)

      // xiaolei 按薪资中位数排行前40
      const xiaoleiBySalary = [...xiaoleiFinalResult]
        .sort((a, b) => b.medianSalary - a.medianSalary)
        .map((item, index) => ({
          name: item.xiaoleiName,
          value: item.medianSalary,
          rank: index + 1
        }))
        .slice(0, 40)

      // xilei 按招聘人数排行前40
      const xileiByRecruitNumber = xileiFinalResult
        .map((item, index) => ({
          name: item.xileiName,
          value: item.totalRecruitNumber,
          rank: index + 1
        }))
        .slice(0, 15)

      // xilei 按薪资中位数排行前40
      const xileiBySalary = [...xileiFinalResult]
        .sort((a, b) => b.medianSalary - a.medianSalary)
        .map((item, index) => ({ name: item.xileiName, value: item.medianSalary, rank: index + 1 }))
        .slice(0, 15)

      console.log('✅ 职业分类统计完成')
      return {
        xiaoleiByRecruitNumber,
        xiaoleiBySalary,
        xileiByRecruitNumber,
        xileiBySalary
      }
    } catch (error) {
      console.error('❌ 职业分类统计失败:', error.message)
      return {
        xiaoleiByRecruitNumber: [],
        xiaoleiBySalary: [],
        xileiByRecruitNumber: [],
        xileiBySalary: []
      }
    }
  }

  private static async getOccupationMapping(
    db: any
  ): Promise<Record<string, { xiaoleiName: string; xiaoleiCode: string; xileiName: string; xileiCode: string }>> {
    // 获取所有职业映射
    const occupations = await db
      .collection('job_occupation_mapping')
      .find(
        {
          'standard_classification.xiaoli.primary.name': { $exists: true, $nin: [null, ''] },
          position_name: { $exists: true, $ne: '' }
        },
        {
          projection: {
            position_name: 1,
            'standard_classification.xiaoli.primary.name': 1,
            'standard_classification.xiaoli.primary.code': 1,
            'standard_classification.xilei.primary.name': 1,
            'standard_classification.xilei.primary.code': 1
          }
        }
      )
      .toArray()

    const occupationMap: Record<
      string,
      { xiaoleiName: string; xiaoleiCode: string; xileiName: string; xileiCode: string }
    > = {}
    occupations.forEach((occupation: any) => {
      occupationMap[occupation.position_name] = {
        xiaoleiName: occupation.standard_classification.xiaoli.primary.name,
        xiaoleiCode: occupation.standard_classification.xiaoli.primary.code,
        xileiName: occupation.standard_classification.xilei.primary.name,
        xileiCode: occupation.standard_classification.xilei.primary.code
      }
    })

    return occupationMap
  }

  /**
   * 从临时表获取公司规模分布统计
   */
  private static async getCompanySizeDistribution(params: BaseQueryParams): Promise<any> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    try {
      const companySizeMap = await this.getCompanySizeMapping(db)

      // 减少批次大小，降低内存使用
      const batchSize = 20000 // 从50000减少到20000
      let skip = 0
      const results: Record<string, { count: number; recruitNumber: number }> = {}

      while (true) {
        const positions = await db
          .collection(tempTableName)
          .find({}, { projection: { companyName: 1, recruitNumber: 1 } })
          .skip(skip)
          .limit(batchSize)
          .toArray()

        if (positions.length === 0) break

        // 在内存中关联公司规模
        positions.forEach((position: any) => {
          const companySize = companySizeMap[position.companyName] || '未知'

          if (!results[companySize]) {
            results[companySize] = { count: 0, recruitNumber: 0 }
          }
          results[companySize].count += 1
          results[companySize].recruitNumber += position.recruitNumber || 0
        })

        skip += positions.length
      }

      // 转换为数组格式，只返回四种公司规模
      const validCompanySizes = ['-', '中型企业', '大型企业', '小微企业']
      const finalResult = Object.entries(results)
        .filter(([size]) => validCompanySizes.includes(size))
        .map(([companySize, stats]) => ({
          name: companySize,
          value: stats.count,
          recruitNumber: stats.recruitNumber
        }))
        .sort((a, b) => b.recruitNumber - a.recruitNumber)

      console.log('✅ 公司规模分布统计完成')
      return finalResult
    } catch (error) {
      console.error('❌ 公司规模分布统计失败:', error.message)
      return []
    }
  }

  private static async getCompanySizeMapping(db: any): Promise<Record<string, string>> {
    // 获取所有公司的规模映射
    const companies = await db
      .collection('zhilian_companies')
      .find(
        {
          company_size: { $exists: true, $nin: [null, ''] },
          original_import_name: { $exists: true, $ne: '' }
        },
        {
          projection: {
            original_import_name: 1,
            company_size: 1
          }
        }
      )
      .toArray()

    const sizeMap: Record<string, string> = {}
    companies.forEach((company: any) => {
      sizeMap[company.original_import_name] = company.company_size
    })

    return sizeMap
  }

  /**
   * 从临时表获取行业统计（中类、小类、三大产业）
   */
  private static async getStandardIndustryStats(params: BaseQueryParams): Promise<{
    industryMediumByRecruitNumber: any[]
    industryMediumBySalary: any[]
    threeIndustryByRecruitNumber: any[]
    threeIndustryBySalary: any[]
  }> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    try {
      // 先获取行业映射表统计信息
      const industryMap = await this.getIndustryMapping(db)
      // 获取行业名称到层级的映射，用于过滤仅保留5级/四级行业
      const industryLevelMap = await this.getIndustryLevelMapping(db)

      // 减少批次大小，降低内存使用
      const batchSize = 20000 // 从50000减少到20000
      let skip = 0
      const industryMediumResults: Record<
        string,
        {
          recruitNumber: number
          salaryValues: number[]
        }
      > = {}
      const threeIndustryResults: Record<
        string,
        {
          recruitNumber: number
          salaryValues: number[]
        }
      > = {}

      while (true) {
        const positions = await db
          .collection(tempTableName)
          .find({}, { projection: { companyName: 1, recruitNumber: 1, salary: 1 } })
          .skip(skip)
          .limit(batchSize)
          .toArray()

        if (positions.length === 0) break

        // 在内存中关联行业分类
        positions.forEach((position: any) => {
          const industryInfo = industryMap[position.companyName]
          if (industryInfo) {
            const industryMedium = industryInfo.industryMedium
            const threeIndustry = industryInfo.threeIndustry

            // 处理行业中类数据
            if (industryMedium) {
              // 仅统计 industry 表中 level 为 4 或 5 的行业中类名称
              const level = industryLevelMap[industryMedium]
              if (level === 4 || level === 5) {
                if (!industryMediumResults[industryMedium]) {
                  industryMediumResults[industryMedium] = {
                    recruitNumber: 0,
                    salaryValues: []
                  }
                }
                industryMediumResults[industryMedium].recruitNumber += position.recruitNumber || 0
                if (position.salary > 0) {
                  industryMediumResults[industryMedium].salaryValues.push(position.salary)
                }
              }
            }

            // 处理三大产业数据
            if (threeIndustry) {
              if (!threeIndustryResults[threeIndustry]) {
                threeIndustryResults[threeIndustry] = {
                  recruitNumber: 0,
                  salaryValues: []
                }
              }
              threeIndustryResults[threeIndustry].recruitNumber += position.recruitNumber || 0
              if (position.salary > 0) {
                threeIndustryResults[threeIndustry].salaryValues.push(position.salary)
              }
            }
          }
        })

        skip += positions.length
      }

      // 计算薪资中位数并转换为数组格式
      const calculateMedianSalary = (salaryValues: number[]): number => {
        const sortedSalaries = salaryValues.sort((a, b) => a - b)
        if (sortedSalaries.length === 0) return 0
        const mid = Math.floor(sortedSalaries.length / 2)
        return sortedSalaries.length % 2 === 0
          ? Math.round((sortedSalaries[mid - 1] + sortedSalaries[mid]) / 2)
          : sortedSalaries[mid]
      }

      // 处理行业中类数据
      const industryMediumFinalResult = Object.entries(industryMediumResults)
        // 额外保险：输出前再次按行业层级过滤，仅保留 level 5/4
        .filter(([industryMedium]) => {
          const level = industryLevelMap[industryMedium]
          return level === 4 || level === 5
        })
        .map(([industryMedium, stats]) => ({
          industryMedium,
          totalRecruitNumber: stats.recruitNumber,
          medianSalary: calculateMedianSalary(stats.salaryValues)
        }))
        .sort((a, b) => b.totalRecruitNumber - a.totalRecruitNumber)

      // 处理三大产业数据
      const threeIndustryFinalResult = Object.entries(threeIndustryResults)
        .map(([threeIndustry, stats]) => ({
          threeIndustry,
          totalRecruitNumber: stats.recruitNumber,
          medianSalary: calculateMedianSalary(stats.salaryValues)
        }))
        .sort((a, b) => b.totalRecruitNumber - a.totalRecruitNumber)

      // 统计信息
      const totalRecruitNumber = Object.values(industryMediumResults).reduce(
        (sum, stats) => sum + stats.recruitNumber,
        0
      )

      // 行业中类按招聘人数排行前100
      const industryMediumByRecruitNumber = industryMediumFinalResult
        .map((item, index) => ({
          name: item.industryMedium,
          value: item.totalRecruitNumber,
          rank: index + 1
        }))
        .slice(0, 105)
        .filter((item) => item.name !== '-')
        .slice(0, 100)

      // 行业中类按薪资中位数排行前100
      const industryMediumBySalary = [...industryMediumFinalResult]
        .sort((a, b) => b.medianSalary - a.medianSalary)
        .map((item, index) => ({
          name: item.industryMedium,
          value: item.medianSalary,
          rank: index + 1
        }))
        .slice(0, 105)
        .filter((item) => item.name !== '-')
        .slice(0, 100)

      // 三大产业按招聘人数排行前10
      const threeIndustryByRecruitNumber = threeIndustryFinalResult.map((item, index) => ({
        name: item.threeIndustry,
        value: item.totalRecruitNumber
      }))

      // 三大产业按薪资中位数排行前10
      const threeIndustryBySalary = [...threeIndustryFinalResult]
        .sort((a, b) => b.medianSalary - a.medianSalary)
        .map((item, index) => ({
          name: item.threeIndustry,
          value: item.medianSalary
        }))

      console.log('✅ 行业统计完成')
      return {
        industryMediumByRecruitNumber,
        industryMediumBySalary,
        threeIndustryByRecruitNumber,
        threeIndustryBySalary
      }
    } catch (error) {
      console.error('❌ 行业统计失败:', error.message)
      return {
        industryMediumByRecruitNumber: [],
        industryMediumBySalary: [],
        threeIndustryByRecruitNumber: [],
        threeIndustryBySalary: []
      }
    }
  }

  private static async getIndustryMapping(db: any): Promise<
    Record<
      string,
      {
        industryMedium: string
        threeIndustry: string
      }
    >
  > {
    // 获取所有行业映射
    const companies = await db
      .collection('zhilian_companies')
      .find(
        {
          original_import_name: { $exists: true, $ne: '' }
        },
        {
          projection: {
            original_import_name: 1,
            industry_medium: 1,
            three_industry: 1
          }
        }
      )
      .toArray()

    const industryMap: Record<
      string,
      {
        industryMedium: string
        threeIndustry: string
      }
    > = {}
    companies.forEach((company: any) => {
      industryMap[company.original_import_name] = {
        industryMedium: company.industry_medium || '',
        threeIndustry: company.three_industry || ''
      }
    })

    return industryMap
  }

  private static async getIndustryLevelMapping(db: any): Promise<Record<string, number>> {
    // 从标准行业表读取名称与层级映射
    const items = await db
      .collection('industry')
      .find(
        {},
        {
          projection: {
            name: 1,
            level: 1
          }
        }
      )
      .toArray()

    const levelMap: Record<string, number> = {}
    items.forEach((it: any) => {
      if (it && typeof it.name === 'string' && typeof it.level === 'number') {
        levelMap[it.name] = it.level
      }
    })

    return levelMap
  }

  /**
   * 从临时表获取学历分布统计
   */
  private static async getEducationDistribution(params: BaseQueryParams): Promise<any> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    const result = await db
      .collection(tempTableName)
      .aggregate([
        {
          $group: {
            _id: '$education',
            count: { $sum: 1 },
            recruitNumber: { $sum: '$recruitNumber' }
          }
        }
      ])
      .toArray()

    // 学历分类映射
    const educationMap = {
      高中及以下: ['高中', '中专/中技', '中技', '初中及以下', '其他'],
      研究生及以上: ['EMBA', 'MBA/EMBA', '硕士', '博士']
    }

    const distribution: any = {
      高中及以下: { count: 0, recruitNumber: 0 },
      大专: { count: 0, recruitNumber: 0 },
      本科: { count: 0, recruitNumber: 0 },
      研究生及以上: { count: 0, recruitNumber: 0 },
      其他: { count: 0, recruitNumber: 0 }
    }

    result.forEach((item: any) => {
      let category = item._id

      // 重新分类
      if (educationMap['高中及以下'].includes(item._id)) {
        category = '高中及以下'
      } else if (educationMap['研究生及以上'].includes(item._id)) {
        category = '研究生及以上'
      } else if (!distribution[category]) {
        category = '其他'
      }

      if (distribution[category]) {
        distribution[category].count += item.count
        distribution[category].recruitNumber += item.recruitNumber
      }
    })

    // 转换为数组格式
    return Object.entries(distribution).map(([name, data]: [string, any]) => ({
      name,
      value: data.count,
      recruitNumber: data.recruitNumber
    }))
  }

  /**
   * 从临时表获取工作经验分布统计
   */
  private static async getWorkingExpDistribution(params: BaseQueryParams): Promise<any> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    const result = await db
      .collection(tempTableName)
      .aggregate([
        {
          $group: {
            _id: '$workingExp',
            count: { $sum: 1 },
            recruitNumber: { $sum: '$recruitNumber' }
          }
        }
      ])
      .toArray()

    // 工作经验分类映射
    const workingExpMap = {
      '1年以下': ['1年以下', '无经验', '经验不限'],
      '1-3年': ['1-3年'],
      '3-5年': ['3-5年'],
      '5-10年': ['5-10年'],
      '10年以上': ['10年以上']
    }

    const distribution: any = {
      '1年以下': { count: 0, recruitNumber: 0 },
      '1-3年': { count: 0, recruitNumber: 0 },
      '3-5年': { count: 0, recruitNumber: 0 },
      '5-10年': { count: 0, recruitNumber: 0 },
      '10年以上': { count: 0, recruitNumber: 0 }
    }

    result.forEach((item: any) => {
      let category = item._id

      // 重新分类
      if (workingExpMap['1年以下'].includes(item._id)) {
        category = '1年以下'
      } else if (workingExpMap['1-3年'].includes(item._id)) {
        category = '1-3年'
      } else if (workingExpMap['3-5年'].includes(item._id)) {
        category = '3-5年'
      } else if (workingExpMap['5-10年'].includes(item._id)) {
        category = '5-10年'
      } else if (workingExpMap['10年以上'].includes(item._id)) {
        category = '10年以上'
      } else {
        // 未知的工作经验类型归类到"1年以下"
        category = '1年以下'
      }

      if (distribution[category]) {
        distribution[category].count += item.count
        distribution[category].recruitNumber += item.recruitNumber
      }
    })

    // 转换为数组格式
    return Object.entries(distribution).map(([name, data]: [string, any]) => ({
      name,
      value: data.count,
      recruitNumber: data.recruitNumber
    }))
  }

  /**
   * 从临时表获取省份统计信息（招聘人数、职位数、招聘单位数、薪资中位数）
   */
  private static async getProvinceStats(params: BaseQueryParams): Promise<{
    byRecruitNumber: any[]
    bySalary: any[]
  }> {
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`
    const models = this.getPositionModels()
    const [positionModel1] = models
    const db = positionModel1.db

    console.log(`📊 开始获取省份统计，临时表: ${tempTableName}`)

    try {
      // 减少批次大小，降低内存使用
      const batchSize = 20000 // 从50000减少到20000
      let skip = 0
      const provinceResults: Record<
        string,
        {
          totalRecruitNumber: number
          totalPositions: number
          uniqueCompanies: Set<string>
          salaryValues: number[]
        }
      > = {}

      while (true) {
        const positions = await db
          .collection(tempTableName)
          .find({}, { projection: { province: 1, companyName: 1, recruitNumber: 1, salary: 1 } })
          .skip(skip)
          .limit(batchSize)
          .toArray()

        if (positions.length === 0) break

        // 在内存中处理省份数据
        positions.forEach((position: any) => {
          const province = position.province || '未知'

          if (!provinceResults[province]) {
            provinceResults[province] = {
              totalRecruitNumber: 0,
              totalPositions: 0,
              uniqueCompanies: new Set(),
              salaryValues: []
            }
          }

          provinceResults[province].totalRecruitNumber += position.recruitNumber || 0
          provinceResults[province].totalPositions += 1
          provinceResults[province].uniqueCompanies.add(position.companyName)

          if (position.salary > 0) {
            provinceResults[province].salaryValues.push(position.salary)
          }
        })

        skip += positions.length
      }

      console.log(`📊 省份数据收集完成，处理了 ${Object.keys(provinceResults).length} 个省份`)

      // 计算薪资中位数
      const calculateMedianSalary = (salaryValues: number[]): number => {
        const sortedSalaries = salaryValues.sort((a, b) => a - b)
        if (sortedSalaries.length === 0) return 0
        const mid = Math.floor(sortedSalaries.length / 2)
        return sortedSalaries.length % 2 === 0
          ? Math.round((sortedSalaries[mid - 1] + sortedSalaries[mid]) / 2)
          : sortedSalaries[mid]
      }

      // 转换为数组格式
      const result = Object.entries(provinceResults).map(([province, stats]) => ({
        province,
        totalRecruitNumber: stats.totalRecruitNumber,
        totalPositions: stats.totalPositions,
        totalCompanies: stats.uniqueCompanies.size,
        medianSalary: calculateMedianSalary(stats.salaryValues)
      }))

      console.log(`📊 省份统计处理完成，结果数量: ${result.length}`)

      // 按招聘人数排行
      const byRecruitNumber = [...result]
        .sort((a, b) => b.totalRecruitNumber - a.totalRecruitNumber)
        .map((item, index) => ({ ...item, rank: index + 1 }))

      // 按薪资中位数排行
      const bySalary = [...result]
        .sort((a, b) => b.medianSalary - a.medianSalary)
        .map((item, index) => ({ ...item, rank: index + 1 }))

      console.log(
        `✅ 省份统计处理完成，按招聘人数排序: ${byRecruitNumber.length} 条，按薪资排序: ${bySalary.length} 条`
      )

      return {
        byRecruitNumber,
        bySalary
      }
    } catch (error) {
      console.error('❌ 省份统计失败:', error)
      throw error
    }
  }

  /**
   * 构建合并数据的聚合管道（用于后续模型合并数据）
   */
  private static buildMergePipeline(params: BaseQueryParams): any[] {
    const { conditions: matchConditions } = this.buildLastMonthOrYearQueryConditions(params)
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`

    return [
      // 第一阶段：匹配条件
      { $match: matchConditions },

      // 第二阶段：处理字段并计算薪资平均值，生成新的 _id
      {
        $addFields: {
          salary: {
            $cond: {
              if: { $and: [{ $ne: ['$salaryReal', null] }, { $ne: ['$salaryReal', ''] }] },
              then: {
                $let: {
                  vars: {
                    parts: {
                      $split: [{ $toString: '$salaryReal' }, '-']
                    }
                  },
                  in: {
                    $cond: {
                      if: { $eq: [{ $size: '$$parts' }, 2] },
                      then: {
                        $round: [
                          {
                            $divide: [
                              {
                                $add: [
                                  { $toInt: { $arrayElemAt: ['$$parts', 0] } },
                                  { $toInt: { $arrayElemAt: ['$$parts', 1] } }
                                ]
                              },
                              2
                            ]
                          },
                          0
                        ]
                      },
                      else: 0
                    }
                  }
                }
              },
              else: 0
            }
          }
        }
      },

      // 第三阶段：只保留必要字段
      {
        $project: {
          _id: 1,
          name: 1,
          classify: '$_job_type.name',
          province: '$_city.name',
          companyName: 1,
          education: 1,
          publishTime: 1,
          workingExp: 1,
          salary: 1,
          recruitNumber: { $ifNull: ['$recruitNumber', 1] } // 招聘人数，如果不存在则默认为1
        }
      },

      // 第四阶段：插入到临时表（使用新 _id，直接插入不合并）
      {
        $merge: {
          into: tempTableName,
          whenNotMatched: 'insert'
        }
      }
    ]
  }

  /**
   * 构建合并所有模型数据的聚合管道
   */
  private static buildTempBasePipeline(params: BaseQueryParams): any[] {
    const { conditions: matchConditions } = this.buildLastMonthOrYearQueryConditions(params)

    // 根据查询参数生成临时表名称
    const tempTableName = `temp_base_data_${params.caliberType}_${params.dateType}`

    return [
      // 第一阶段：匹配条件（使用索引优化）
      { $match: matchConditions },

      // 第二阶段：处理字段并计算薪资平均值
      {
        $addFields: {
          // 计算薪资平均值
          salary: {
            $cond: {
              if: { $and: [{ $ne: ['$salaryReal', null] }, { $ne: ['$salaryReal', ''] }] },
              then: {
                $let: {
                  vars: {
                    parts: {
                      $split: [{ $toString: '$salaryReal' }, '-']
                    }
                  },
                  in: {
                    $cond: {
                      if: { $eq: [{ $size: '$$parts' }, 2] },
                      then: {
                        $round: [
                          {
                            $divide: [
                              {
                                $add: [
                                  { $toInt: { $arrayElemAt: ['$$parts', 0] } },
                                  { $toInt: { $arrayElemAt: ['$$parts', 1] } }
                                ]
                              },
                              2
                            ]
                          },
                          0
                        ]
                      },
                      else: 0
                    }
                  }
                }
              },
              else: 0
            }
          }
        }
      },

      // 第三阶段：只保留必要字段
      {
        $project: {
          _id: 1,
          name: 1, // 职位名称
          classify: '$_job_type.name', // 职位分类
          province: '$_city.name', // 省份
          companyName: 1, // 公司名称
          education: 1, // 学历要求
          publishTime: 1, // 发布时间
          workingExp: 1, // 工作经验
          salary: 1, // 薪资平均值
          salaryReal: 1, // 薪资区间
          salary60: 1, // 薪资区间+薪酬倍数
          recruitNumber: { $ifNull: ['$recruitNumber', 1] } // 招聘人数，如果不存在则默认为1
        }
      },

      // 第四阶段：保存到临时表（使用 $out 提高性能）
      {
        $out: tempTableName
      }
    ]
  }

  /**
   * 获取职位模型（支持4个分表）
   */
  public static getPositionModels() {
    const mainConnection = connections.main
    return [
      createPositionModel1(PositionSchema1, { connection: mainConnection }),
      createPositionModel2(PositionSchema2, { connection: mainConnection }),
      createPositionModel3(PositionSchema3, { connection: mainConnection }),
      createPositionModel4(PositionSchema4, { connection: mainConnection })
    ]
  }

  /**
   * 计算日期范围（优化版本）
   */
  private static calculateDateRange(dateType: 'month' | 'year'): {
    startDate: string
    endDate: string
    dateArray: string[]
  } {
    const now = new Date()

    if (dateType === 'month') {
      // 最近7个月（不包括当前月份，第1个月作为变化率计算的基准）
      const currentYear = now.getFullYear()
      const currentMonth = now.getMonth() + 1

      // 计算7个月前的月份（第1个月，用于变化率计算）
      let startMonth = currentMonth - 7
      let startYear = currentYear
      if (startMonth <= 0) {
        startYear = currentYear - 1
        startMonth = 12 + startMonth
      }

      // 计算上一个月（最后一个月）
      let endMonth = currentMonth - 1
      let endYear = currentYear
      if (endMonth === 0) {
        endMonth = 12
        endYear = currentYear - 1
      }

      // 生成月份数组（只包含后6个月用于显示，不包含第1个月）
      const dateArray: string[] = []
      for (let i = 0; i < 7; i++) {
        // 从第2个月开始，跳过第1个月
        let targetMonth = startMonth + i
        let targetYear = startYear

        if (targetMonth > 12) {
          targetMonth -= 12
          targetYear += 1
        }

        const monthStr = `${targetYear}-${String(targetMonth).padStart(2, '0')}`
        dateArray.push(monthStr)
      }

      // 优化的日期字符串格式
      const startDate = `${startYear}-${String(startMonth).padStart(2, '0')}-01 00:00:00`
      const endDate = `${endYear}-${String(endMonth).padStart(2, '0')}-31 23:59:59`
      return { startDate, endDate, dateArray }
    }
    // 最近6年（包括今年，第1年用于变化率计算）
    const currentYear = now.getFullYear()
    const startYear = currentYear - 5 // 6年前作为基准年

    // 生成年份数组（只包含后5年用于显示，不包含第1年）
    const dateArray: string[] = []
    for (let year = startYear + 0; year <= currentYear; year++) {
      // 从第2年开始，跳过第1年
      dateArray.push(year.toString())
    }

    const startDate = `${startYear}-01-01 00:00:00`
    const endDate = `${currentYear}-12-31 23:59:59`
    return { startDate, endDate, dateArray }
  }

  /**
   * 根据查询参数构建优化的 MongoDB 查询条件
   * 性能优化：简化日期处理，优化索引使用
   */
  private static buildQueryConditions(params: BaseQueryParams): {
    conditions: any
    dates: string[]
  } {
    const conditions: any = {}
    let dates: string[] = []

    // 优化的时间条件构建
    const { startDate, endDate, dateArray } = this.calculateDateRange(params.dateType)

    // 使用更高效的日期范围查询
    conditions.publishTime = {
      $gte: startDate,
      $lte: endDate
    }

    dates = dateArray

    // 口径条件优化
    if (params.caliberType === 'college') {
      // 使用更高效的查询条件
      conditions.$and = [
        { education: { $in: ['高中', '中专/中技', '中技', '初中及以下', '其他'] } },
        { workingExp: { $in: ['1年以下', '无经验', '经验不限'] } }
      ]
    }

    return { conditions, dates }
  }

  /**
   * 计算上一个月或者今年的日期范围
   */
  private static calculateLastMonthOrYearRange(dateType: 'month' | 'year'): {
    startDate: string
    endDate: string
    dateStr: string
  } {
    const now = new Date()

    if (dateType === 'month') {
      // 上一个月的数据
      const currentYear = now.getFullYear()
      const currentMonth = now.getMonth() + 1

      // 计算上一个月
      let lastMonth = currentMonth - 1
      let lastYear = currentYear
      if (lastMonth === 0) {
        lastMonth = 12
        lastYear = currentYear - 1
      }

      const startDate = `${lastYear}-${String(lastMonth).padStart(2, '0')}-01 00:00:00`
      const endDate = `${lastYear}-${String(lastMonth).padStart(2, '0')}-31 23:59:59`
      const dateStr = `${lastYear}-${String(lastMonth).padStart(2, '0')}`

      return { startDate, endDate, dateStr }
    }

    // 今年的数据
    const currentYear = now.getFullYear()
    const startDate = `${currentYear}-01-01 00:00:00`
    const endDate = `${currentYear}-12-31 23:59:59`
    const dateStr = currentYear.toString()

    return { startDate, endDate, dateStr }
  }

  /**
   * 构建上一个月或者今年的查询条件
   */
  private static buildLastMonthOrYearQueryConditions(params: BaseQueryParams): {
    conditions: any
    dateStr: string
  } {
    const conditions: any = {}
    // 使用新的日期范围计算方法
    const { startDate, endDate, dateStr } = this.calculateLastMonthOrYearRange(params.dateType)

    // 设置时间条件
    conditions.publishTime = {
      $gte: startDate,
      $lte: endDate
    }

    // 口径条件优化
    if (params.caliberType === 'college') {
      conditions.$and = [
        { education: { $in: ['高中', '中专/中技', '中技', '初中及以下', '其他'] } },
        { workingExp: { $in: ['1年以下', '无经验', '经验不限'] } }
      ]
    }

    return { conditions, dateStr }
  }

  /**
   * 手动缓存所有4种组合的基础数据（使用聚合方案）
   */
  static async cacheAllCombinations(): Promise<{
    success: boolean
    results: Array<{
      params: BaseQueryParams
      success: boolean
      error?: string
      cacheKey: string
    }>
  }> {
    // console.log('🚀 开始手动缓存所有4种组合的基础数据（聚合方案）...');

    const results = []

    for (const params of this.CACHE_COMBINATIONS) {
      const cacheKey = this.generateCacheKey(params)
      try {
        // console.log(`📊 正在缓存: ${JSON.stringify(params)}`);
        await this.initCacheBaseData(params)
        results.push({
          params,
          success: true,
          cacheKey
        })
        // console.log(`✅ 缓存成功: ${cacheKey}`);
      } catch (error) {
        // console.error(`❌ 缓存失败: ${cacheKey}, 错误: ${error.message}`);
        results.push({
          params,
          success: false,
          error: error.message,
          cacheKey
        })
      }
    }

    const successCount = results.filter((r) => r.success).length
    // console.log(`🎯 手动缓存完成: ${successCount}/${results.length} 成功`);

    return {
      success: successCount === results.length,
      results
    }
  }

  /**
   * 手动缓存单个组合的基础数据（使用聚合方案）
   */
  static async cacheSingleCombination(params: BaseQueryParams): Promise<{
    success: boolean
    cacheKey: string
    cacheTime: string
    error?: string
  }> {
    const cacheKey = this.generateCacheKey(params)

    try {
      const baseData = await this.initCacheBaseData(params)

      return {
        success: true,
        cacheKey,
        cacheTime: baseData?.cacheTime || ''
      }
    } catch (error) {
      return {
        success: false,
        cacheKey,
        cacheTime: '',
        error: error.message
      }
    }
  }

  /**
   * 异步缓存单个组合的基础数据（不等待结果）
   */
  static async cacheSingleCombinationAsync(
    params: BaseQueryParams,
    taskId: string
  ): Promise<{
    success: boolean
    cacheKey: string
    cacheTime: string
    taskId: string
    error?: string
  }> {
    const cacheKey = this.generateCacheKey(params)
    console.log(`🚀 开始异步缓存任务: ${taskId}, 缓存键: ${cacheKey}`)

    // 记录开始时的内存使用情况
    const startMemory = process.memoryUsage()
    console.log(`📊 任务开始内存使用: ${Math.round(startMemory.heapUsed / 1024 / 1024)}MB`)

    try {
      const baseData = await this.initCacheBaseData(params)

      // 记录完成时的内存使用情况
      const endMemory = process.memoryUsage()
      console.log(`📊 任务完成内存使用: ${Math.round(endMemory.heapUsed / 1024 / 1024)}MB`)

      // 强制垃圾回收
      if (global.gc) {
        global.gc()
        const afterGcMemory = process.memoryUsage()
        console.log(`🧹 垃圾回收后内存使用: ${Math.round(afterGcMemory.heapUsed / 1024 / 1024)}MB`)
      }

      console.log(`✅ 异步缓存任务完成: ${taskId}, 缓存键: ${cacheKey}`)
      return {
        success: true,
        cacheKey,
        cacheTime: baseData?.cacheTime || '',
        taskId
      }
    } catch (error) {
      console.error(`❌ 异步缓存任务失败: ${taskId}, 缓存键: ${cacheKey}, 错误: ${error.message}`)

      // 记录失败时的内存使用情况
      const errorMemory = process.memoryUsage()
      console.log(`📊 任务失败内存使用: ${Math.round(errorMemory.heapUsed / 1024 / 1024)}MB`)

      return {
        success: false,
        cacheKey,
        cacheTime: '',
        taskId,
        error: error.message
      }
    }
  }

  /**
   * 异步缓存所有组合的基础数据（不等待结果）
   */
  static async cacheAllCombinationsAsync(taskId: string): Promise<{
    success: boolean
    successCount: number
    totalCount: number
    taskId: string
    results: any[]
  }> {
    console.log(`🚀 开始异步批量缓存任务: ${taskId}, 总任务数: ${this.CACHE_COMBINATIONS.length}`)

    const results: any[] = []
    let successCount = 0

    for (const params of this.CACHE_COMBINATIONS) {
      const cacheKey = this.generateCacheKey(params)
      try {
        console.log(`📊 正在异步缓存: ${JSON.stringify(params)}`)
        await this.initCacheBaseData(params)
        results.push({
          params,
          success: true,
          cacheKey
        })
        successCount++
        console.log(`✅ 异步缓存成功: ${cacheKey}`)
      } catch (error) {
        console.error(`❌ 异步缓存失败: ${cacheKey}, 错误: ${error.message}`)
        results.push({
          params,
          success: false,
          error: error.message,
          cacheKey
        })
      }
    }

    console.log(`🎯 异步批量缓存任务完成: ${taskId}, 成功: ${successCount}/${results.length}`)

    return {
      success: successCount === results.length,
      successCount,
      totalCount: results.length,
      taskId,
      results
    }
  }

  /**
   * 清理昨天的缓存（保留今天的缓存）
   */
  static async clearYesterdayCache(): Promise<{
    success: boolean
    clearedKeys: string[]
    errors: string[]
  }> {
    // console.log('🧹 开始清理昨天的缓存...');

    const clearedKeys: string[] = []
    const errors: string[] = []

    for (const params of this.CACHE_COMBINATIONS) {
      const yesterdayCacheKey = this.generateYesterdayCacheKey(params)
      try {
        await this.getCacheService().del(yesterdayCacheKey)
        clearedKeys.push(yesterdayCacheKey)
        // console.log(`✅ 清理昨天缓存成功: ${yesterdayCacheKey}`);
      } catch (error) {
        const errorMsg = `清理昨天缓存失败: ${yesterdayCacheKey}, 错误: ${error.message}`
        errors.push(errorMsg)
        // console.error(`❌ ${errorMsg}`);
      }
    }

    // console.log(`🎯 昨天缓存清理完成: 成功 ${clearedKeys.length} 个, 失败 ${errors.length} 个`);

    return {
      success: errors.length === 0,
      clearedKeys,
      errors
    }
  }

  /**
   * 清理今天的缓存
   */
  static async clearTodayCache(): Promise<{
    success: boolean
    clearedKeys: string[]
    errors: string[]
  }> {
    const clearedKeys: string[] = []
    const errors: string[] = []

    try {
      const currentDate = this.getCurrentDateString()

      for (const params of this.CACHE_COMBINATIONS) {
        const todayKey = this.generateCacheKey(params, currentDate)
        try {
          await this.getCacheService().del(todayKey)
          clearedKeys.push(todayKey)
        } catch (error) {
          errors.push(`清理今天缓存失败: ${todayKey}, 错误: ${error.message}`)
        }
      }
    } catch (e) {
      errors.push(`清理今天缓存过程异常: ${e.message}`)
    }

    return {
      success: errors.length === 0,
      clearedKeys,
      errors
    }
  }

  /**
   * 获取缓存状态信息
   */
  static async getCacheStatus(): Promise<{
    combinations: Array<{
      params: BaseQueryParams
      cacheKey: string
      exists: boolean
      ttl?: number
      cacheTime?: string
    }>
    summary: {
      total: number
      cached: number
      missing: number
      currentDate: string
    }
  }> {
    const combinations = []
    let cached = 0
    const currentDate = this.getCurrentDateString()

    for (const params of this.CACHE_COMBINATIONS) {
      const cacheKey = this.generateCacheKey(params)
      try {
        const exists = await this.getCacheService().exists(cacheKey)
        let ttl: number | undefined
        let cacheTime: string | undefined

        if (exists) {
          ttl = await this.getCacheService().ttl(cacheKey)
          try {
            const cachedData = await this.getCacheService().get(cacheKey)
            if (cachedData) {
              // cachedData已经是解析后的对象，不需要再次JSON.parse
              const parsedData = cachedData as any
              cacheTime = parsedData.cacheTime
            }
          } catch (error) {
            // console.warn(`获取缓存详情失败: ${cacheKey}`);
          }
        }

        combinations.push({
          params,
          cacheKey,
          exists,
          ttl,
          cacheTime
        })

        if (exists) cached++
      } catch (error) {
        combinations.push({
          params,
          cacheKey,
          exists: false
        })
      }
    }

    return {
      combinations,
      summary: {
        total: this.CACHE_COMBINATIONS.length,
        cached,
        missing: this.CACHE_COMBINATIONS.length - cached,
        currentDate
      }
    }
  }

  /**
   * 获取性能分析数据
   */
  static async getPerformanceAnalysis(): Promise<{
    queryTime: number
    cacheHitRate: number
    indexStatus: any
    recommendations: string[]
  }> {
    const startTime = Date.now()

    try {
      // 测试查询性能
      const testParams = this.CACHE_COMBINATIONS[0]
      await this.getBase(testParams)
      const queryTime = Date.now() - startTime

      // 获取缓存状态
      const cacheStatus = await this.getCacheStatus()
      const cacheHitRate = cacheStatus.summary.cached / cacheStatus.summary.total

      // 获取索引状态
      const indexStatus = await this.getIndexStatus()

      // 生成建议
      const recommendations = []
      if (queryTime > 30000) {
        recommendations.push('查询时间过长，建议检查数据库索引')
      }
      if (cacheHitRate < 0.8) {
        recommendations.push('缓存命中率较低，建议优化缓存策略')
      }
      if (!indexStatus.collections.every((c) => c.hasPerformanceIndex)) {
        recommendations.push('部分集合缺少性能优化索引，建议创建索引')
      }

      return {
        queryTime,
        cacheHitRate: Math.round(cacheHitRate * 100) / 100,
        indexStatus,
        recommendations
      }
    } catch (error) {
      return {
        queryTime: Date.now() - startTime,
        cacheHitRate: 0,
        indexStatus: { collections: [] },
        recommendations: ['性能分析失败，请检查系统状态']
      }
    }
  }

  /**
   * 创建性能优化所需的数据库索引
   * 建议在部署时执行此方法
   */
  static async createPerformanceIndexes(): Promise<{
    success: boolean
    results: Array<{
      collection: string
      success: boolean
      error?: string
    }>
  }> {
    // console.log('🔧 开始创建性能优化索引...');

    const results = []
    const collections = [
      'zhilian_job_raw_part1',
      'zhilian_job_raw_part2',
      'zhilian_job_raw_part3',
      'zhilian_job_raw_part4'
    ]

    try {
      const mainConnection = connections.main

      for (const collectionName of collections) {
        try {
          const collection = mainConnection.collection(collectionName)

          // 创建复合索引：publishTime + education + workingExp
          await collection.createIndex(
            { publishTime: 1, education: 1, workingExp: 1 },
            {
              name: 'publishTime_education_workingExp_compound',
              background: true
            }
          )

          // 创建单独的publishTime索引（如果不存在）
          await collection.createIndex(
            { publishTime: 1 },
            {
              name: 'publishTime_single',
              background: true
            }
          )

          results.push({
            collection: collectionName,
            success: true
          })

          // console.log(`✅ 索引创建成功: ${collectionName}`);
        } catch (error) {
          results.push({
            collection: collectionName,
            success: false,
            error: error.message
          })
          // console.error(`❌ 索引创建失败: ${collectionName}, 错误: ${error.message}`);
        }
      }

      const successCount = results.filter((r) => r.success).length
      // console.log(`🎯 索引创建完成: ${successCount}/${results.length} 成功`);

      return {
        success: successCount === results.length,
        results
      }
    } catch (error) {
      // console.error(`索引创建过程失败: ${error.message}`);
      return {
        success: false,
        results
      }
    }
  }

  /**
   * 获取索引状态信息
   */
  static async getIndexStatus(): Promise<{
    collections: Array<{
      name: string
      indexes: any[]
      hasPerformanceIndex: boolean
    }>
  }> {
    const collections = [
      'zhilian_job_raw_part1',
      'zhilian_job_raw_part2',
      'zhilian_job_raw_part3',
      'zhilian_job_raw_part4'
    ]
    const results = []

    try {
      const mainConnection = connections.main

      for (const collectionName of collections) {
        try {
          const collection = mainConnection.collection(collectionName)
          const indexes = await collection.indexes()

          const hasPerformanceIndex = indexes.some(
            (index) => index.name === 'publishTime_education_workingExp_compound'
          )

          results.push({
            name: collectionName,
            indexes: indexes.map((idx) => ({
              name: idx.name,
              key: idx.key
            })),
            hasPerformanceIndex
          })
        } catch (error) {
          results.push({
            name: collectionName,
            indexes: [],
            hasPerformanceIndex: false
          })
        }
      }

      return { collections: results }
    } catch (error) {
      // console.error(`获取索引状态失败: ${error.message}`);
      return { collections: results }
    }
  }

  /**
   * 获取学校招生数据
   */
  private static async getSchoolEnrollmentData(): Promise<any> {
    const startTime = Date.now()
    console.log('📊 开始获取学校招生数据...')

    try {
      const results = await Promise.allSettled([
        SchoolEnrollmentService.getSchoolNumByProvince({ category: '专科' }),
        SchoolEnrollmentService.getStudentNumByProvince({ category: '专科' }),
        SchoolEnrollmentService.getStudentNumByMajor({ category: '专科' }),
        SchoolEnrollmentService.getStudentNumByYear({ category: '专科' }),
        SchoolEnrollmentService.getSchoolNum()
        // SchoolEnrollmentService.getMajorByPosition()
      ])

      const schoolEnrollmentData = {
        schoolNumByProvince: results[0].status === 'fulfilled' ? results[0].value : [],
        studentNumByProvince: results[1].status === 'fulfilled' ? results[1].value : [],
        studentNumByMajor: results[2].status === 'fulfilled' ? results[2].value : [],
        studentNumByYear: results[3].status === 'fulfilled' ? results[3].value : { list: [] },
        schoolNum: results[4].status === 'fulfilled' ? results[4].value : []
        // majorByPosition: results[5].status === 'fulfilled' ? results[5].value : []
      }

      const totalTime = Date.now() - startTime
      console.log(`✅ 学校招生数据获取完成，总耗时: ${totalTime}ms`)

      return schoolEnrollmentData
    } catch (error) {
      const totalTime = Date.now() - startTime
      console.error(`❌ 获取学校招生数据失败，耗时: ${totalTime}ms`, error)
      return {
        schoolNumByProvince: [],
        studentNumByProvince: [],
        studentNumByMajor: [],
        studentNumByYear: { list: [] },
        schoolNum: []
        // majorByPosition: []
      }
    }
  }

  /**
   * 获取左侧趋势数据（从 Position service 提取）
   * @param params 查询参数
   * @returns 左侧趋势数据：招聘单位数、招聘人数、职位数、环比增长率
   */
  static async getLeftTrendData(params: BaseQueryParams): Promise<PositionScreenTrendResult> {
    const startTime = Date.now()
    console.log('📈 开始获取左侧趋势数据...')

    try {
      // 获取所有分表模型
      const models = this.getPositionModels()
      const results = []

      // 构建聚合管道
      const pipeline = this.buildPositionTrendPipeline(params)

      // 真正的并行查询所有分表
      const queryPromises = models.map(async (model, index) => {
        try {
          const result = await model.aggregate(pipeline).allowDiskUse(true)
          return result
        } catch (error) {
          return null
        }
      })

      // 等待所有查询完成
      const allResults = await Promise.allSettled(queryPromises)

      // 过滤有效结果（处理 Promise.allSettled 的结果）
      const validResults = allResults
        .filter((result) => result.status === 'fulfilled' && result.value && result.value.length > 0)
        .map((result) => (result as PromiseFulfilledResult<any[]>).value)

      results.push(...validResults)

      // 合并结果
      const mergedData = this.mergePositionAggregationResults(results)

      // 处理趋势数据
      const trendData = this.processPositionTrendDataFromAggregation(mergedData, params.dateType || 'month')

      const totalTime = Date.now() - startTime
      console.log(`✅ 左侧趋势数据获取完成，总耗时: ${totalTime}ms`)
      return trendData
    } catch (error) {
      const totalTime = Date.now() - startTime
      console.error(`❌ 获取左侧趋势数据失败，耗时: ${totalTime}ms`, error)
      throw error
    }
  }

  /**
   * 构建 Position 趋势数据聚合管道（从 Position service 提取，性能优化版本）
   */
  private static buildPositionTrendPipeline(params: BaseQueryParams): any[] {
    const { conditions: matchConditions } = this.buildQueryConditions(params)

    // 按时间分组的聚合管道，获取每个月的真实统计数据
    // 使用更高效的日期处理方式
    return [
      { $match: matchConditions },
      {
        $addFields: {
          // 提取年月用于分组 - 使用更精确的日期处理
          yearMonth: {
            $dateToString: {
              format: params.dateType === 'month' ? '%Y-%m' : '%Y',
              date: { $dateFromString: { dateString: '$publishTime' } }
            }
          }
        }
      },
      {
        $group: {
          _id: '$yearMonth',
          totalPositions: { $sum: 1 },
          totalRecruitment: { $sum: { $ifNull: ['$recruitNumber', 1] } },
          uniqueCompanies: { $addToSet: '$companyName' }
        }
      }
    ]
  }

  /**
   * 合并 Position 聚合结果（按时间分组）（从 Position service 提取）
   */
  private static mergePositionAggregationResults(results: any[][]): any {
    // 按时间分组合并所有分表的结果
    const timeGroupedData = new Map<
      string,
      {
        totalPositions: number
        totalRecruitment: number
        uniqueCompanies: Set<string>
      }
    >()

    // 遍历所有分表的结果
    results.forEach((result) => {
      if (result && result.length > 0) {
        result.forEach((item) => {
          const timeKey = item._id // 年月字符串，如 "2025-06"

          if (!timeGroupedData.has(timeKey)) {
            timeGroupedData.set(timeKey, {
              totalPositions: 0,
              totalRecruitment: 0,
              uniqueCompanies: new Set()
            })
          }

          const groupData = timeGroupedData.get(timeKey)
          groupData.totalPositions += item.totalPositions || 0
          groupData.totalRecruitment += item.totalRecruitment || 0

          // 合并公司名称
          if (item.uniqueCompanies && Array.isArray(item.uniqueCompanies)) {
            item.uniqueCompanies.forEach((company: string) => {
              if (company) groupData.uniqueCompanies.add(company)
            })
          }
        })
      }
    })

    // 转换为数组格式，按时间排序
    const sortedData = Array.from(timeGroupedData.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([timeKey, data]) => ({
        timeKey,
        totalPositions: data.totalPositions,
        totalRecruitment: data.totalRecruitment,
        totalCompanies: data.uniqueCompanies.size
      }))

    return sortedData
  }

  /**
   * 处理 Position 聚合趋势数据（使用真实的按时间分组数据）（从 Position service 提取）
   */
  private static processPositionTrendDataFromAggregation(
    mergedData: any[],
    dateType: 'month' | 'year'
  ): PositionScreenTrendResult {
    if (!mergedData || !Array.isArray(mergedData) || mergedData.length === 0) {
      return {
        months: [],
        positions: [],
        recruitment: [],
        companies: [],
        positionChangeRate: [],
        recruitmentChangeRate: [],
        companyChangeRate: []
      }
    }

    // 获取期望的时间范围
    const { dates } = this.buildQueryConditions({ dateType } as BaseQueryParams)

    // 创建时间到数据的映射
    const dataMap = new Map()
    mergedData.forEach((item) => {
      dataMap.set(item.timeKey, {
        positions: item.totalPositions || 0,
        recruitment: item.totalRecruitment || 0,
        companies: item.totalCompanies || 0
      })
    })

    // 按期望的时间顺序填充数据，缺失的月份用0填充
    const months: string[] = []
    const positions: number[] = []
    const recruitment: number[] = []
    const companies: number[] = []

    dates.forEach((date) => {
      months.push(date)
      const data = dataMap.get(date)
      if (data) {
        positions.push(data.positions)
        recruitment.push(data.recruitment)
        companies.push(data.companies)
      } else {
        positions.push(0)
        recruitment.push(0)
        companies.push(0)
      }
    })

    // 计算变化率
    const positionChangeRate = this.calculatePositionChangeRate(positions)
    const recruitmentChangeRate = this.calculatePositionChangeRate(recruitment)
    const companyChangeRate = this.calculatePositionChangeRate(companies)

    // 对于月度数据，直接返回6个月的数据（dateArray已经只包含6个月）
    if (dateType === 'month') {
      return {
        months: months.slice(1),
        positions: positions.slice(1),
        recruitment: recruitment.slice(1),
        companies: companies.slice(1),
        positionChangeRate: positionChangeRate.slice(1),
        recruitmentChangeRate: recruitmentChangeRate.slice(1),
        companyChangeRate: companyChangeRate.slice(1)
      }
    }

    return {
      months: months.slice(1),
      positions: positions.slice(1),
      recruitment: recruitment.slice(1),
      companies: companies.slice(1),
      positionChangeRate: positionChangeRate.slice(1),
      recruitmentChangeRate: recruitmentChangeRate.slice(1),
      companyChangeRate: companyChangeRate.slice(1)
    }
  }

  /**
   * 计算 Position 变化率（从 Position service 提取）
   * 计算相邻月份之间的变化率：(当前月 - 上一个月) / 上一个月
   */
  private static calculatePositionChangeRate(values: number[]): number[] {
    const changeRates: number[] = []

    // 如果数据不足2个月，无法计算变化率
    if (values.length < 2) {
      return values.map(() => 0)
    }

    // 第一个月的变化率为0（没有上一个月作为基准）
    changeRates.push(0)

    // 从第二个月开始计算变化率
    for (let i = 1; i < values.length; i++) {
      const current = values[i]
      const previous = values[i - 1]

      if (previous === 0) {
        changeRates.push(current > 0 ? 100 : 0)
      } else {
        const changeRate = ((current - previous) / previous) * 100
        changeRates.push(Math.round(changeRate * 100) / 100) // 保留两位小数
      }
    }

    return changeRates
  }

  /**
   * 缓存趋势数据到 base
   */
  static async cacheTrendData(params: BaseQueryParams, trendData: any): Promise<void> {
    const cacheKey = this.generateCacheKey(params)

    try {
      // 获取现有的 base 或创建新的
      let base = await this.getBase(params)

      if (!base) {
        // 如果不存在，创建一个基础结构
        base = {
          trendData: null,
          summaryData: null,
          provinceData: null,
          careerRankingData: null,
          industryRankingData: null,
          distributionData: null,
          educationData: null,
          experienceData: null,
          cacheTime: new Date().toISOString()
        }
      }

      // 更新趋势数据
      base.trendData = trendData
      base.cacheTime = new Date().toISOString()

      // 缓存更新后的数据（永久缓存）
      await this.getCacheService().set(cacheKey, base, 0) // 永久缓存
    } catch (error) {
      throw error
    }
  }
}
