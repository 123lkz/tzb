import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { CompanyControllerBase } from '../../base/entity/Company/Company.controller'
import {
  CompanyParams,
  CompanyPositionStatsResult,
  CompanyProvinceResult,
  CompanySizeResult,
  CompanyTrendParams,
  CompanyTrendResult
} from './Company.dto'
import { CompanyService } from './Company.service'

@CloverController()
@ApiTags('公司')
export class CompanyController extends CompanyControllerBase {
  @Get('/Company/trends')
  @Description('数据中台：按时间获取公司数量趋势统计')
  @ApiResponse({ type: CompanyTrendResult })
  async getTrendStats(@Query() params: CompanyTrendParams): Promise<CompanyTrendResult> {
    try {
      return await CompanyService.getTrendStats(params)
    } catch (error) {
      throw new BadRequestException(`获取公司趋势统计失败: ${error.message}`)
    }
  }

  @Get('/Company/province')
  @Description('数据中台：按省份获取公司数量统计')
  @ApiResponse({ type: CompanyProvinceResult })
  async getProvinceStats(@Query() params: CompanyParams): Promise<CompanyProvinceResult> {
    try {
      return await CompanyService.getProvinceStats(params)
    } catch (error) {
      throw new BadRequestException(`获取省份公司统计失败: ${error.message}`)
    }
  }

  @Get('/Company/size')
  @Description('数据中台：按规模获取公司数量统计')
  @ApiResponse({ type: CompanySizeResult })
  async getSizeStats(@Query() params: CompanyParams): Promise<CompanySizeResult> {
    try {
      return await CompanyService.getSizeStats(params)
    } catch (error) {
      throw new BadRequestException(`获取公司规模统计失败: ${error.message}`)
    }
  }

  @Get('/Company/position-stats')
  @Description('数据中台：获取公司职位统计排行')
  @ApiResponse({ type: CompanyPositionStatsResult })
  async getPositionStats(@Query() params: CompanyParams): Promise<CompanyPositionStatsResult> {
    try {
      return await CompanyService.getPositionStats(params)
    } catch (error) {
      throw new BadRequestException(`获取公司职位统计失败: ${error.message}`)
    }
  }
}
