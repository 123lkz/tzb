import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Query, Res } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { Response } from 'express'
import { BaseQueryParams } from '../Base/Base.dto'
import { BaseService } from '../Base/Base.service'
import {
  PositionDistributionResult,
  PositionListParams,
  PositionListResult,
  PositionScreenCareerRankResult,
  PositionScreenIndustryResult,
  PositionScreenProvinceResult,
  PositionScreenTotalResult,
  PositionScreenTrendResult
} from './Position.dto'
import { PositionService } from './Position.service'

@CloverController()
@ApiTags('职位')
export class PositionController {
  /* 数据大屏的接口数据 */
  @Get('/position/screen/trend/data')
  @Description('数据大屏：获取左侧职位趋势')
  @ApiResponse({ type: PositionScreenTrendResult })
  async getScreenTrendData(@Query() params: BaseQueryParams): Promise<PositionScreenTrendResult> {
    try {
      return await PositionService.getScreenTrendData(params)
    } catch (error) {
      throw new BadRequestException(`获取大屏数据失败: ${error.message}`)
    }
  }

  @Get('/position/screen/total/data')
  @Description('数据大屏：获取总数量统计')
  @ApiResponse({ type: PositionScreenTotalResult })
  async getScreenTotalData(@Query() params: BaseQueryParams): Promise<PositionScreenTotalResult> {
    try {
      return await PositionService.getScreenTotalData(params)
    } catch (error) {
      throw new BadRequestException(`获取大屏数据失败: ${error.message}`)
    }
  }

  @Get('/position/screen/province/data')
  @Description('数据大屏：获取各省份的招聘数量统计')
  @ApiResponse({ type: PositionScreenProvinceResult })
  async getScreenDataByProvince(@Query() params: BaseQueryParams): Promise<PositionScreenProvinceResult> {
    try {
      return await PositionService.getScreenProvinceData(params)
    } catch (error) {
      throw new BadRequestException(`获取大屏数据失败: ${error.message}`)
    }
  }

  @Get('/position/screen/distribution/data')
  @Description('数据大屏：获取学历要求分布、经验要求分布和公司规模分布')
  @ApiResponse({ type: PositionDistributionResult })
  async getScreenDistributionData(@Query() params: BaseQueryParams): Promise<PositionDistributionResult> {
    try {
      return await PositionService.getScreenDistributionData(params)
    } catch (error) {
      throw new BadRequestException(`获取分布数据失败: ${error.message}`)
    }
  }

  @Get('/position/screen/career/rank')
  @Description('数据大屏：获取标准职业排行前40')
  @ApiResponse({ type: PositionDistributionResult })
  async getScreenCareerRank(@Query() params: BaseQueryParams): Promise<PositionScreenCareerRankResult> {
    try {
      return await PositionService.getScreenCareerRank(params)
    } catch (error) {
      throw new BadRequestException(`获取标准职业排行前100数据失败: ${error.message}`)
    }
  }

  @Get('/position/screen/industry/data')
  @Description('数据大屏：获取标准行业前100名和三大产业数据')
  @ApiResponse({ type: PositionScreenIndustryResult })
  async getScreenIndustryData(@Query() params: BaseQueryParams): Promise<PositionScreenIndustryResult> {
    try {
      console.log('📊 开始获取行业数据...')
      const base = await BaseService.getBase(params)

      if (base && base.industryStats) {
        return {
          industryMediumByRecruitNumber: base.industryStats.industryMediumByRecruitNumber,
          threeIndustryByRecruitNumber: base.industryStats.threeIndustryByRecruitNumber,
          updateTime: new Date().toISOString()
        }
      }

      // 如果没有缓存数据，返回空数据
      console.warn('⚠️ 没有找到缓存的行业数据，请先执行缓存任务')
      return {
        industryMediumByRecruitNumber: [],
        threeIndustryByRecruitNumber: [],
        updateTime: new Date().toISOString()
      }
    } catch (error) {
      throw new BadRequestException(`获取行业相关数据失败: ${error.message}`)
    }
  }

  @Get('/position/list')
  @Description('获取职位列表（支持分页和排序）')
  @ApiResponse({ type: PositionListResult })
  async getPositionList(@Query() params: PositionListParams): Promise<PositionListResult> {
    try {
      return await PositionService.getPositionList(params)
    } catch (error) {
      throw new BadRequestException(`获取职位列表失败: ${error.message}`)
    }
  }

  @Get('/position/export')
  @Description('导出职位列表为Excel文件')
  @ApiResponse({
    description: 'Excel文件下载',
    content: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
        schema: {
          type: 'string',
          format: 'binary'
        }
      }
    }
  })
  async exportPositionList(@Query() params: PositionListParams, @Res() res: Response): Promise<void> {
    try {
      const excelBuffer = await PositionService.exportPositionListToExcel(params)

      // 设置响应头
      const filename = `职位列表_${new Date().toISOString().slice(0, 10)}.xlsx`
      res.header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
      res.header('Content-Disposition', `attachment; filename="${encodeURIComponent(filename)}"`)
      res.header('Content-Length', excelBuffer.length.toString())

      // 发送文件
      res.send(excelBuffer)
    } catch (error) {
      throw new BadRequestException(`导出职位列表失败: ${error.message}`)
    }
  }

  @Get('/position/log')
  @Description('获取职教服务端项目日志')
  @ApiResponse({
    description: 'PM2应用日志内容',
    schema: {
      type: 'string',
      example: '2025-09-29 10:00:00 [Nest] 开始执行每日基础数据缓存任务...'
    }
  })
  async getPositionLog(@Query('lines') lines?: string): Promise<string> {
    try {
      const lineCount = lines ? parseInt(lines, 10) : 800

      // 限制最大行数，避免返回过多内容
      const maxLines = Math.min(lineCount, 5000)

      return await PositionService.getPositionLog(maxLines)
    } catch (error) {
      throw new BadRequestException(`获取职位日志失败: ${error.message}`)
    }
  }

  @Get('/position/error-log')
  @Description('获取职教服务端项目错误日志')
  @ApiResponse({
    description: 'PM2应用错误日志内容',
    schema: {
      type: 'string',
      example: '2025-09-29 10:00:00 Error: Redis connection failed...'
    }
  })
  async getPositionErrorLog(@Query('lines') lines?: string): Promise<string> {
    try {
      const lineCount = lines ? parseInt(lines, 10) : 500

      // 限制最大行数，避免返回过多内容
      const maxLines = Math.min(lineCount, 5000)

      return await PositionService.getPositionErrorLog(maxLines)
    } catch (error) {
      throw new BadRequestException(`获取职位错误日志失败: ${error.message}`)
    }
  }
}
