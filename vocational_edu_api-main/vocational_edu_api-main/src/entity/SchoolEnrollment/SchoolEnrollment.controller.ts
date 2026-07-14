import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import crypto from 'crypto'
import { SchoolEnrollmentControllerBase } from '../../base/entity/SchoolEnrollment/SchoolEnrollment.controller'
import { CacheService } from '../../services/CacheService'
import { BaseService } from '../Base/Base.service'
import {
  GraduateNumResult,
  MajorByPositionResult,
  ProvinceSchoolResult,
  ResultItem,
  SchoolParams,
  YearParams
} from './SchoolEnrollment.dto'
import { SchoolEnrollmentService } from './SchoolEnrollment.service'

@CloverController()
@ApiTags('学校招生')
export class SchoolEnrollmentController extends SchoolEnrollmentControllerBase {
  private static cacheService: CacheService = new CacheService()

  private generateStableKey(prefix: string, params: any) {
    const normalizedParams = params ? JSON.stringify(params) : '{}'
    const hash = crypto.createHash('md5').update(normalizedParams).digest('hex')
    const today = new Date().toISOString().split('T')[0]
    return `se_${prefix}_${today}_${hash.substring(0, 12)}`
  }
  @Get('/SchoolEnrollment/getStudentNumByProvince')
  @Description('获取各省份在校生人数2020-2022年')
  @ApiResponse({ type: ProvinceSchoolResult })
  async getStudentNumByProvince(@Query() params?: SchoolParams): Promise<ResultItem[]> {
    try {
      console.log('📊 开始获取省份学生数量数据...')

      // 先尝试从Base缓存获取
      const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      const base = await BaseService.getBase(baseParams)

      if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.studentNumByProvince) {
        console.log('✅ 从Base缓存获取省份学生数量数据')
        return base.schoolEnrollmentData.studentNumByProvince
      }

      // 如果Base缓存没有数据，回退到直接查询
      console.warn('⚠️ Base缓存中没有省份学生数量数据，直接查询数据库')
      return await SchoolEnrollmentService.getStudentNumByProvince(params)
    } catch (error: any) {
      throw new BadRequestException(`获取学校省份统计失败: ${error.message}`)
    }
  }

  @Get('/SchoolEnrollment/getSchoolNumByProvince')
  @Description('获取各省份学校数量（含双高院校数量）')
  @ApiResponse({ type: ProvinceSchoolResult })
  async getSchoolNumByProvince(@Query() params?: YearParams): Promise<ResultItem[]> {
    try {
      console.log('📊 开始获取省份学校数量数据...')

      // 先尝试从Base缓存获取
      const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      const base = await BaseService.getBase(baseParams)

      if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.schoolNumByProvince) {
        console.log('✅ 从Base缓存获取省份学校数量数据')
        return base.schoolEnrollmentData.schoolNumByProvince
      }

      // 如果Base缓存没有数据，回退到直接查询
      console.warn('⚠️ Base缓存中没有省份学校数量数据，直接查询数据库')
      return await SchoolEnrollmentService.getSchoolNumByProvince(params)
    } catch (error: any) {
      throw new BadRequestException(`获取院校数量失败: ${error.message}`)
    }
  }

  // @Get('/SchoolEnrollment/clearSchoolNumByProvinceCache')
  // @Description('清除各省份学校数量缓存（若曾启用）')
  // async clearSchoolNumByProvinceCache(@Query() params?: YearParams): Promise<{ cleared: number }> {
  //   try {
  //     const key = this.generateStableKey('school_num_province', params);
  //     const pattern = `se_school_num_province1_*`;
  //     const cleared = await SchoolEnrollmentController.cacheService.delPattern(pattern);
  //     // 兼容清单key直删
  //     await SchoolEnrollmentController.cacheService.del(key);
  //     return { cleared };
  //   } catch (error: any) {
  //     throw new BadRequestException(`清理缓存失败: ${error.message}`);
  //   }
  // }

  @Get('/SchoolEnrollment/getStudentNumByMajor')
  @Description('统计各专业学生数量2020-2022年')
  @ApiResponse({ type: ProvinceSchoolResult })
  async getStudentNumByMajor(@Query() params?: SchoolParams): Promise<ResultItem[]> {
    try {
      console.log('📊 开始获取专业学生数量数据...')

      // 先尝试从Base缓存获取
      const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      const base = await BaseService.getBase(baseParams)

      if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.studentNumByMajor) {
        console.log('✅ 从Base缓存获取专业学生数量数据')
        return base.schoolEnrollmentData.studentNumByMajor
      }

      // 如果Base缓存没有数据，回退到直接查询
      console.warn('⚠️ Base缓存中没有专业学生数量数据，直接查询数据库')
      return await SchoolEnrollmentService.getStudentNumByMajor(params)
    } catch (error: any) {
      throw new BadRequestException(`获取专业学生数量失败: ${error.message}`)
    }
  }

  @Get('/SchoolEnrollment/getStudentNumByYear')
  @Description('统计2017-2022年各年的招生、毕业、在校人数')
  @ApiResponse({ type: GraduateNumResult })
  async getStudentNumByYear(@Query() params?: SchoolParams): Promise<GraduateNumResult> {
    try {
      console.log('📊 开始获取年度学生数量数据...')

      // 先尝试从Base缓存获取
      const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      const base = await BaseService.getBase(baseParams)

      if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.studentNumByYear) {
        console.log('✅ 从Base缓存获取年度学生数量数据')
        return base.schoolEnrollmentData.studentNumByYear
      }

      // 如果Base缓存没有数据，回退到直接查询
      console.warn('⚠️ Base缓存中没有年度学生数量数据，直接查询数据库')
      return await SchoolEnrollmentService.getStudentNumByYear(params)
    } catch (error: any) {
      throw new BadRequestException(`获取年度学生数量失败: ${error.message}`)
    }
  }

  @Get('/SchoolEnrollment/getSchoolNum')
  @Description('统计专科双高/非双高院校数量')
  @ApiResponse({ type: ProvinceSchoolResult })
  async getSchoolNum(): Promise<ResultItem[]> {
    try {
      console.log('📊 开始获取学校数量数据...')

      // 先尝试从Base缓存获取
      const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      const base = await BaseService.getBase(baseParams)

      if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.schoolNum) {
        console.log('✅ 从Base缓存获取学校数量数据')
        return base.schoolEnrollmentData.schoolNum
      }

      // 如果Base缓存没有数据，回退到直接查询
      console.warn('⚠️ Base缓存中没有学校数量数据，直接查询数据库')
      return await SchoolEnrollmentService.getSchoolNum()
    } catch (error: any) {
      throw new BadRequestException(`统计专科院校数量失败: ${error.message}`)
    }
  }

  @Get('/SchoolEnrollment/getMajorByPosition')
  @Description('统计标准职业对应专业词云')
  @ApiResponse({ type: MajorByPositionResult, isArray: true })
  async getMajorByPosition(): Promise<MajorByPositionResult[]> {
    try {
      // console.log('📊 开始获取专业对应岗位数据...')

      // // 先尝试从Base缓存获取
      // const baseParams = { dateType: 'month' as const, caliberType: 'all' as const }
      // const base = await BaseService.getBase(baseParams)

      // if (base && base.schoolEnrollmentData && base.schoolEnrollmentData.majorByPosition) {
      //   console.log('✅ 从Base缓存获取专业对应岗位数据')
      //   return base.schoolEnrollmentData.majorByPosition
      // }

      // // 如果Base缓存没有数据，回退到直接查询
      // console.warn('⚠️ Base缓存中没有专业对应岗位数据，直接查询数据库')
      return await SchoolEnrollmentService.getMajorByPosition()
    } catch (error: any) {
      throw new BadRequestException(`统计标准职业对应专业失败: ${error.message}`)
    }
  }
}
