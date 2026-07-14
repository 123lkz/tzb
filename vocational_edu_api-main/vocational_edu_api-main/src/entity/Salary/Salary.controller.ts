import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { BaseQueryParams } from '../Base/Base.dto'
import {
  SalaryScreenCareerResult,
  SalaryScreenDistributionResult,
  SalaryScreenIndustryResult,
  SalaryScreenProvinceResult,
  SalaryScreenTotalResult
} from './Salary.dto'
import { SalaryService } from './Salary.service'

@CloverController()
@ApiTags('薪酬')
export class SalaryController {
  @Get('/salary/screen/total/data')
  @Description('数据大屏：获取薪资总数据概览')
  @ApiResponse({ type: SalaryScreenTotalResult })
  async getScreenTotalData(@Query() params: BaseQueryParams): Promise<SalaryScreenTotalResult> {
    try {
      return await SalaryService.getScreenTotalData(params)
    } catch (error) {
      throw new BadRequestException(`获取薪资总数据概览失败: ${error.message}`)
    }
  }

  @Get('/salary/screen/province/data')
  @Description('数据大屏：获取薪资省份排行数据')
  @ApiResponse({ type: SalaryScreenProvinceResult })
  async getScreenProvinceData(@Query() params: BaseQueryParams): Promise<SalaryScreenProvinceResult> {
    try {
      return await SalaryService.getScreenProvinceData(params)
    } catch (error) {
      throw new BadRequestException(`获取薪资省份排行数据失败: ${error.message}`)
    }
  }

  @Get('/salary/screen/career/data')
  @Description('数据大屏：获取薪资职业排行数据')
  @ApiResponse({ type: SalaryScreenCareerResult })
  async getScreenCareerData(@Query() params: BaseQueryParams): Promise<SalaryScreenCareerResult> {
    try {
      return await SalaryService.getScreenCareerData(params)
    } catch (error) {
      throw new BadRequestException(`获取薪资职业排行数据失败: ${error.message}`)
    }
  }

  @Get('/salary/screen/industry/data')
  @Description('数据大屏：获取薪资行业排行数据')
  @ApiResponse({ type: SalaryScreenIndustryResult })
  async getScreenIndustryData(@Query() params: BaseQueryParams): Promise<SalaryScreenIndustryResult> {
    try {
      return await SalaryService.getScreenIndustryData(params)
    } catch (error) {
      throw new BadRequestException(`获取薪资行业排行数据失败: ${error.message}`)
    }
  }

  @Get('/salary/screen/distribution/data')
  @Description('数据大屏：获取薪资分布数据')
  @ApiResponse({ type: SalaryScreenDistributionResult })
  async getScreenDistributionData(@Query() params: BaseQueryParams): Promise<SalaryScreenDistributionResult> {
    try {
      return await SalaryService.getScreenDistributionData(params)
    } catch (error) {
      throw new BadRequestException(`获取薪资分布数据失败: ${error.message}`)
    }
  }
}
