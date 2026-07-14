import { Injectable } from '@nestjs/common'
import { BaseQueryParams } from '../Base/Base.dto'
import { BaseService } from '../Base/Base.service'
import {
  SalaryScreenCareerResult,
  SalaryScreenDistributionResult,
  SalaryScreenIndustryResult,
  SalaryScreenProvinceResult,
  SalaryScreenTotalResult
} from './Salary.dto'

@Injectable()
export class SalaryService {
  /**
   * 获取薪资总数据概览
   * @param params 查询参数
   * @returns 薪资总数据概览
   */
  static async getScreenTotalData(params: BaseQueryParams): Promise<SalaryScreenTotalResult> {
    console.log('📊 开始获取薪资总数据概览...')
    const base = await BaseService.getBase(params)

    if (base && base.salaryQuantiles) {
      console.log('✅ 薪资总数据概览获取完成')
      return {
        p25Salary: base.salaryQuantiles.p25 || 0,
        p50Salary: base.salaryQuantiles.p50 || 0,
        p75Salary: base.salaryQuantiles.p75 || 0,
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的薪资总数据，请先执行缓存任务')
    return {
      p25Salary: 0,
      p50Salary: 0,
      p75Salary: 0,
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取薪资省份排行数据
   * @param params 查询参数
   * @returns 薪资省份排行数据
   */
  static async getScreenProvinceData(params: BaseQueryParams): Promise<SalaryScreenProvinceResult> {
    console.log('📊 开始获取薪资省份排行数据...')
    const base = await BaseService.getBase(params)

    if (base && base.provinceStats) {
      // 从 Base 中获取省份薪资排行数据
      const provinceSalaryRank = base.provinceStats.bySalary || []
      return {
        provinceData: provinceSalaryRank,
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的薪资省份数据，请先执行缓存任务')
    return {
      provinceData: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取薪资职业排行数据
   * @param params 查询参数
   * @returns 薪资职业排行数据
   */
  static async getScreenCareerData(params: BaseQueryParams): Promise<SalaryScreenCareerResult> {
    console.log('📊 开始获取薪资职业排行数据...')
    const base = await BaseService.getBase(params)

    if (base && base.careerStats) {
      // 从 Base 中获取标准职业统计数据
      const standardXiaoleiStats = base.careerStats.xiaoleiBySalary || []
      const standardXileiStats = base.careerStats.xileiBySalary || []

      return {
        standardXiaoleiRanking: standardXiaoleiStats,
        standardXileiRanking: standardXileiStats,
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的薪资职业数据，请先执行缓存任务')
    return {
      standardXiaoleiRanking: [],
      standardXileiRanking: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取薪资行业排行数据
   * @param params 查询参数
   * @returns 薪资行业排行数据
   */
  static async getScreenIndustryData(params: BaseQueryParams): Promise<SalaryScreenIndustryResult> {
    console.log('📊 开始获取薪资行业排行数据...')
    const base = await BaseService.getBase(params)

    if (base && base.industryStats) {
      // 从 Base 中获取行业统计数据
      const industryMediumStats = base.industryStats.industryMediumBySalary || []
      const threeIndustryStats = base.industryStats.threeIndustryBySalary || []

      return {
        industryRankBySalary: industryMediumStats,
        threeIndustriesBySalary: threeIndustryStats,
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的薪资行业数据，请先执行缓存任务')
    return {
      industryRankBySalary: [],
      threeIndustriesBySalary: [],
      updateTime: new Date().toISOString()
    }
  }

  /**
   * 获取薪资分布数据
   * @param params 查询参数
   * @returns 薪资分布数据
   */
  static async getScreenDistributionData(params: BaseQueryParams): Promise<SalaryScreenDistributionResult> {
    console.log('📊 开始获取薪资分布数据...')
    const base = await BaseService.getBase(params)

    if (base) {
      return {
        companySizeDistribution: base.companySizeDistribution || [],
        workingExpDistribution: base.workingExpDistribution || [],
        educationDistribution: base.educationDistribution || [],
        updateTime: new Date().toISOString()
      }
    }

    // 如果没有缓存数据，返回空数据
    console.warn('⚠️ 没有找到缓存的薪资分布数据，请先执行缓存任务')
    return {
      companySizeDistribution: [],
      workingExpDistribution: [],
      educationDistribution: [],
      updateTime: new Date().toISOString()
    }
  }
}
