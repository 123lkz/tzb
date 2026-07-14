import { Injectable } from '@nestjs/common'
import * as fs from 'fs'
import * as tmp from 'tmp'
import { connections } from '../../utils/DatabaseUtils'
import { BaseQueryParams } from '../Base/Base.dto'
import { BaseService } from '../Base/Base.service'
import {
  PositionDistributionResult,
  PositionListParams,
  PositionListResult,
  PositionScreenCareerRankResult,
  PositionScreenProvinceResult,
  PositionScreenTotalResult,
  PositionScreenTrendResult
} from './Position.dto'

@Injectable()
export class PositionService {
  /**
   * 获取职位趋势数据
   * @param params 查询参数
   * @returns 职位趋势数据：招聘单位数、招聘人数、职位数、环比增长率
   */
  static async getScreenTrendData(params: BaseQueryParams): Promise<PositionScreenTrendResult> {
    console.log('📊 开始获取趋势数据...')

    const base = await BaseService.getBase(params)

    if (base && base.trendData) {
      return {
        months: base.trendData.months,
        positions: base.trendData.positions,
        recruitment: base.trendData.recruitment,
        companies: base.trendData.companies,
        positionChangeRate: base.trendData.positionChangeRate,
        recruitmentChangeRate: base.trendData.recruitmentChangeRate,
        companyChangeRate: base.trendData.companyChangeRate
      }
    }

    // 如果没有缓存数据，返回空数据而不是重新计算
    console.warn('⚠️ 没有找到缓存的趋势数据，请先执行缓存任务')
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

  /**
   * 获取总数量统计
   * @param params 查询参数
   * @returns 总数量统计：上一个月/今年总职位数、总招聘人数、总招聘单位数
   */
  static async getScreenTotalData(params: BaseQueryParams): Promise<PositionScreenTotalResult> {
    console.log('📊 开始获取总数量统计...')
    const base = await BaseService.getBase(params)

    if (base && base.totalStats) {
      return {
        totalPositions: base.totalStats.totalPositions || 0,
        totalRecruitment: base.totalStats.totalRecruitNumber || 0,
        totalCompanies: base.totalStats.totalCompanies || 0
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的总数量统计，请先执行缓存任务')
    return {
      totalPositions: 0,
      totalRecruitment: 0,
      totalCompanies: 0
    }
  }

  /**
   * 获取省份数据
   * @param params 查询参数
   * @returns 省份数据统计
   */
  static async getScreenProvinceData(params: BaseQueryParams): Promise<PositionScreenProvinceResult> {
    console.log('📊 开始获取省份数据...')
    const base = await BaseService.getBase(params)

    if (base && base.provinceStats) {
      // 从 Base 中获取省份统计数据
      const provinceRecruitRank = base.provinceStats.byRecruitNumber || []
      return {
        provinceData: provinceRecruitRank,
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的省份数据，请先执行缓存任务')
    return {
      provinceData: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取分布数据（学历要求分布、经验要求分布）
   * @param params 查询参数
   * @returns 分布数据统计
   */
  /**
   * 获取薪资分布数据
   * @param params 查询参数
   * @returns 薪资分布数据
   */
  static async getScreenDistributionData(params: BaseQueryParams): Promise<PositionDistributionResult> {
    console.log('📊 开始获取薪资分布数据...')
    const base = await BaseService.getBase(params)

    if (base) {
      return {
        companySizeDistribution: base.companySizeDistribution || [],
        workingExpRequirement: base.workingExpDistribution || [],
        educationRequirement: base.educationDistribution || [],
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的分布数据，请先执行缓存任务')
    return {
      companySizeDistribution: [],
      workingExpRequirement: [],
      educationRequirement: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取标准职业排行数据
   * @param params 查询参数
   * @returns 职业排行数据
   */
  static async getScreenCareerRank(params: BaseQueryParams): Promise<PositionScreenCareerRankResult> {
    console.log('📊 开始获取标准职业排行数据...')
    const base = await BaseService.getBase(params)

    if (base && base.careerStats) {
      return {
        xiaoleiByRecruitNumber: base.careerStats.xiaoleiByRecruitNumber || [],
        xileiByRecruitNumber: base.careerStats.xileiByRecruitNumber || [],
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的职业排行数据，请先执行缓存任务')
    return {
      xiaoleiByRecruitNumber: [],
      xileiByRecruitNumber: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取职位列表（支持分页和排序）
   * 优先从临时表查询，如果临时表不存在则回退到多表查询
   * @param params 查询参数
   * @returns 分页职位列表
   */
  static async getPositionList(params: PositionListParams): Promise<PositionListResult> {
    console.log('🔍 开始获取职位列表... 查询参数:', params)
    const page = Number(params.page)
    const pageSize = Number(params.pageSize)

    // 构建查询条件
    const matchConditions: any = {}

    // 添加过滤条件
    if (params.province) {
      matchConditions.province = params.province
    }

    if (params.companyName) {
      matchConditions.companyName = { $regex: params.companyName, $options: 'i' }
    }

    if (params.name) {
      matchConditions.name = { $regex: params.name, $options: 'i' }
    }

    if (params.classify) {
      matchConditions.classify = params.classify
    }

    if (params.date) {
      // 按月份过滤，支持 YYYY-MM 格式
      const dateRegex = /^\d{4}-\d{2}$/
      if (dateRegex.test(params.date)) {
        // 构建月份范围查询
        const year = params.date.split('-')[0]
        const month = params.date.split('-')[1]
        const startDate = `${year}-${month}-01`
        const endDate = `${year}-${month}-31`

        matchConditions.publishTime = {
          $gte: startDate,
          $lte: endDate
        }
      } else {
        console.warn(`⚠️ 无效的日期格式: ${params.date}，应为 YYYY-MM 格式`)
      }
    }

    if (params.education) {
      // 学历条件映射
      const educationMapping: { [key: string]: string[] } = {
        学历不限: ['学历不限'],
        高中及以下: ['高中', '中专/中技', '中技', '初中及以下', '其他'],
        大专: ['大专'],
        本科: ['本科'],
        研究生及以上: ['EMBA', 'MBA/EMBA', '硕士', '博士']
      }

      const mappedValues = educationMapping[params.education]
      if (mappedValues) {
        matchConditions.education = { $in: mappedValues }
      } else {
        // 如果没有找到映射，使用原始值
        matchConditions.education = params.education
      }
    }

    if (params.workingExp) {
      // 工作经验条件映射
      const workingExpMapping: { [key: string]: string[] } = {
        '1年以下': ['1年以下', '无经验', '经验不限'],
        '1-3年': ['1-3年'],
        '3-5年': ['3-5年'],
        '5-10年': ['5-10年'],
        '10年以上': ['10年以上']
      }

      const mappedValues = workingExpMapping[params.workingExp]
      if (mappedValues) {
        matchConditions.workingExp = { $in: mappedValues }
      } else {
        // 如果没有找到映射，使用原始值
        matchConditions.workingExp = params.workingExp
      }
    }

    // 构建排序条件
    const sortConditions: any = {}
    const sortField = params.sortField || 'publishTime' // 默认按发布时间排序
    const sortOrder = params.sortOrder || 'desc' // 默认降序
    sortConditions[sortField] = sortOrder === 'asc' ? 1 : -1

    // 计算分页参数
    const skip = (page - 1) * pageSize

    try {
      // 首先尝试从临时表查询（性能更优）
      const result = await this.getPositionListFromTempTable(params, matchConditions, sortConditions, skip, pageSize)
      if (result) {
        return result
      }
    } catch (error) {
      return {
        items: [],
        total: 0,
        page,
        pageSize,
        totalPages: 0,
        hasNext: false,
        hasPrev: false
      }
    }
  }

  /**
   * 从临时表获取职位列表（高性能版本）
   * 只从 temp_base_data_all_year 临时表查询
   */
  private static async getPositionListFromTempTable(
    params: PositionListParams,
    matchConditions: any,
    sortConditions: any,
    skip: number,
    pageSize: number
  ): Promise<PositionListResult | null> {
    const mainConnection = connections.main
    const tempTableName = 'temp_base_data_all_year'

    try {
      // 检查临时表是否存在
      const collections = await mainConnection.db.listCollections({ name: tempTableName }).toArray()

      if (collections.length === 0) {
        console.log(`⚠️ 临时表 ${tempTableName} 不存在`)
        return null
      }

      // 直接使用数据库连接查询临时表
      const db = mainConnection.db
      const collection = db.collection(tempTableName)
      const totalCountInTable = await collection.countDocuments()

      // 如果临时表为空，直接返回null，让系统回退到多表查询
      if (totalCountInTable === 0) {
        return null
      }

      // 构建查询管道
      const pipeline = [
        { $match: matchConditions },
        {
          $project: {
            _id: 1,
            name: 1,
            classify: 1,
            province: 1,
            companyName: 1,
            education: 1,
            workingExp: 1,
            publishTime: 1,
            recruitNumber: 1,
            salary60: 1,
            salaryReal: 1,
            salary: 1,
            positionUrl: 1
          }
        },
        { $sort: sortConditions },
        { $skip: skip },
        { $limit: pageSize }
      ]

      // 构建计数管道
      const countPipeline = [{ $match: matchConditions }, { $count: 'total' }]

      // 并行查询数据和总数
      const [items, countResults] = await Promise.all([
        collection.aggregate(pipeline).toArray(),
        collection.aggregate(countPipeline).toArray()
      ])

      const totalCount = countResults[0]?.total || 0
      const totalPages = Math.ceil(totalCount / pageSize)
      const hasNext = params.page < totalPages
      const hasPrev = params.page > 1

      return {
        items: items as any,
        total: totalCount,
        page: Number(params.page),
        pageSize: Number(params.pageSize),
        totalPages,
        hasNext,
        hasPrev
      }
    } catch (error) {
      console.warn(`⚠️ 临时表 ${tempTableName} 查询失败:`, error.message)
      return null
    }
  }

  /**
   * 获取PM2应用日志
   * @param lines 返回的行数，默认1000行
   * @returns 日志内容
   */
  static async getPositionLog(lines: number = 1000): Promise<string> {
    const logPath = '/app/vocational_edu/log/pm2/vocational_edu_api_out.log'

    try {
      // 检查文件是否存在
      if (!fs.existsSync(logPath)) {
        throw new Error(`日志文件不存在: ${logPath}`)
      }

      // 获取文件信息
      const stats = fs.statSync(logPath)
      const fileSize = stats.size

      // 如果文件为空，返回空字符串
      if (fileSize === 0) {
        return '日志文件为空'
      }

      // 读取文件内容
      const content = fs.readFileSync(logPath, 'utf-8')
      const allLines = content.split('\n')

      // 如果请求的行数大于等于总行数，返回所有内容
      if (lines >= allLines.length) {
        return content
      }

      // 返回最后N行
      const lastLines = allLines.slice(-lines)
      return lastLines.join('\n')
    } catch (error) {
      throw new Error(`读取日志文件失败: ${error.message}`)
    }
  }

  /**
   * 获取PM2应用错误日志
   * @param lines 返回的行数，默认1000行
   * @returns 错误日志内容
   */
  static async getPositionErrorLog(lines: number = 1000): Promise<string> {
    const errorLogPath = '/app/vocational_edu/log/pm2/vocational_edu_api_err.log'

    try {
      // 检查文件是否存在
      if (!fs.existsSync(errorLogPath)) {
        throw new Error(`错误日志文件不存在: ${errorLogPath}`)
      }

      // 获取文件信息
      const stats = fs.statSync(errorLogPath)
      const fileSize = stats.size

      // 如果文件为空，返回空字符串
      if (fileSize === 0) {
        return '错误日志文件为空'
      }

      // 读取文件内容
      const content = fs.readFileSync(errorLogPath, 'utf-8')
      const allLines = content.split('\n')

      // 如果请求的行数大于等于总行数，返回所有内容
      if (lines >= allLines.length) {
        return content
      }

      // 返回最后N行
      const lastLines = allLines.slice(-lines)
      return lastLines.join('\n')
    } catch (error) {
      throw new Error(`读取错误日志文件失败: ${error.message}`)
    }
  }

  /**
   * 导出职位列表为Excel文件
   * @param params 查询参数
   * @returns Excel文件Buffer
   */
  static async exportPositionListToExcel(params: PositionListParams): Promise<Buffer> {
    console.log('📊 开始导出职位列表为Excel...')

    try {
      // 直接获取所有数据（不分页）
      const allItems = await this.getAllPositionData(params)

      if (!allItems || allItems.length === 0) {
        throw new Error('没有数据可导出')
      }

      // 创建Excel内容
      const excelContent = this.createExcelContent(allItems)

      // 生成Excel文件
      const excelBuffer = await this.generateExcelBuffer(excelContent)

      console.log(`✅ Excel导出完成，共导出 ${allItems.length} 条数据`)
      return excelBuffer
    } catch (error) {
      console.error('❌ Excel导出失败:', error.message)
      throw new Error(`导出Excel失败: ${error.message}`)
    }
  }

  /**
   * 获取所有职位数据（不分页）
   */
  private static async getAllPositionData(params: PositionListParams): Promise<any[]> {
    const page = 1
    const pageSize = 20

    // 构建查询条件
    const matchConditions: any = {}

    // 添加过滤条件
    if (params.province) {
      matchConditions.province = params.province
    }

    if (params.companyName) {
      matchConditions.companyName = { $regex: params.companyName, $options: 'i' }
    }

    if (params.name) {
      matchConditions.name = { $regex: params.name, $options: 'i' }
    }

    if (params.classify) {
      matchConditions.classify = params.classify
    }

    if (params.date) {
      // 按月份过滤，支持 YYYY-MM 格式
      const dateRegex = /^\d{4}-\d{2}$/
      if (dateRegex.test(params.date)) {
        // 构建月份范围查询
        const year = params.date.split('-')[0]
        const month = params.date.split('-')[1]
        const startDate = `${year}-${month}-01`
        const endDate = `${year}-${month}-31`

        matchConditions.publishTime = {
          $gte: startDate,
          $lte: endDate
        }
        console.log(`🔍 导出月份过滤: ${params.date} -> ${startDate} 到 ${endDate}`)
      } else {
        console.warn(`⚠️ 无效的日期格式: ${params.date}，应为 YYYY-MM 格式`)
      }
    }

    if (params.education) {
      // 学历条件映射
      const educationMapping: { [key: string]: string[] } = {
        学历不限: ['学历不限'],
        高中及以下: ['高中', '中专/中技', '中技', '初中及以下', '其他'],
        大专: ['大专'],
        本科: ['本科'],
        研究生及以上: ['EMBA', 'MBA/EMBA', '硕士', '博士']
      }

      const mappedValues = educationMapping[params.education]
      if (mappedValues) {
        matchConditions.education = { $in: mappedValues }
      } else {
        matchConditions.education = params.education
      }
    }

    if (params.workingExp) {
      // 工作经验条件映射
      const workingExpMapping: { [key: string]: string[] } = {
        '1年以下': ['1年以下', '无经验', '经验不限'],
        '1-3年': ['1-3年'],
        '3-5年': ['3-5年'],
        '5-10年': ['5-10年'],
        '10年以上': ['10年以上']
      }

      const mappedValues = workingExpMapping[params.workingExp]
      if (mappedValues) {
        matchConditions.workingExp = { $in: mappedValues }
      } else {
        matchConditions.workingExp = params.workingExp
      }
    }

    // 构建排序条件
    const sortConditions: any = {}
    const sortField = params.sortField || 'publishTime'
    const sortOrder = params.sortOrder || 'desc'
    sortConditions[sortField] = sortOrder === 'asc' ? 1 : -1

    try {
      // 尝试从临时表获取所有数据
      const result = await this.getAllPositionDataFromTempTable(matchConditions, sortConditions)
      if (result) {
        return result
      }
    } catch (error) {
      console.warn('⚠️ 从临时表获取数据失败:', error.message)
    }

    // 如果临时表失败，返回空数组
    return []
  }

  /**
   * 从临时表获取所有职位数据
   */
  private static async getAllPositionDataFromTempTable(
    matchConditions: any,
    sortConditions: any
  ): Promise<any[] | null> {
    const mainConnection = connections.main
    const tempTableName = 'temp_base_data_all_year'

    try {
      // 检查临时表是否存在
      const collections = await mainConnection.db.listCollections({ name: tempTableName }).toArray()
      if (collections.length === 0) {
        return null
      }

      // 直接使用数据库连接查询临时表
      const db = mainConnection.db
      const collection = db.collection(tempTableName)
      const totalCountInTable = await collection.countDocuments()

      if (totalCountInTable === 0) {
        return null
      }

      // 构建查询管道（不分页）
      const pipeline = [
        { $match: matchConditions },
        {
          $project: {
            _id: 1,
            name: 1,
            classify: 1,
            province: 1,
            companyName: 1,
            education: 1,
            workingExp: 1,
            publishTime: 1,
            recruitNumber: 1,
            salary60: 1,
            salaryReal: 1,
            salary: 1,
            positionUrl: 1
          }
        },
        { $sort: sortConditions }
      ]

      // 查询所有数据
      const items = await collection.aggregate(pipeline).toArray()
      return items as any[]
    } catch (error) {
      console.warn(`⚠️ 临时表 ${tempTableName} 查询失败:`, error.message)
      return null
    }
  }

  /**
   * 创建Excel内容
   */
  private static createExcelContent(items: any[]): any[] {
    const headers = [
      '职位名称',
      '智联职位分类',
      '招聘省份',
      '公司名称',
      '学历要求',
      '工作经验',
      '发布时间',
      '招聘人数',
      '薪资区间+薪酬倍数',
      '薪资区间',
      '薪资中间值',
      '职位链接'
    ]

    const rows = items.map((item) => [
      item.jobName || item.name || '',
      item.jobClassify || item.classify || '',
      item.province || '',
      item.companyName || '',
      item.education || '',
      item.workingExp || '',
      item.publishTime || '',
      item.recruitNumber || '',
      item.salary60 || '',
      item.salaryReal || '',
      item.salary || '',
      item.positionUrl || ''
    ])

    return [headers, ...rows]
  }

  /**
   * 生成Excel Buffer
   */
  private static async generateExcelBuffer(data: any[]): Promise<Buffer> {
    return new Promise((resolve, reject) => {
      try {
        // 创建临时文件
        const tmpFile = tmp.fileSync({ postfix: '.xlsx' })

        // 简单的CSV格式转换为Excel兼容格式
        const csvContent = data
          .map((row) => row.map((cell: any) => `"${String(cell).replace(/"/g, '""')}"`).join(','))
          .join('\n')

        // 添加BOM以支持中文
        const bom = Buffer.from('\uFEFF', 'utf8')
        const csvBuffer = Buffer.from(csvContent, 'utf8')
        const finalBuffer = Buffer.concat([bom, csvBuffer])

        // 写入临时文件
        fs.writeFileSync(tmpFile.name, finalBuffer)

        // 读取文件内容
        const buffer = fs.readFileSync(tmpFile.name)

        // 清理临时文件
        tmpFile.removeCallback()

        resolve(buffer)
      } catch (error) {
        reject(error)
      }
    })
  }
}
