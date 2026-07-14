import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { SchoolControllerBase } from '../../base/entity/School/School.controller'
import { ProvinceSchoolResult, SchoolNumResult, SchoolParams } from './School.dto'
import { SchoolService } from './School.service'

@CloverController()
@ApiTags('学校')
export class SchoolController extends SchoolControllerBase {
  @Get('/Schools/getByProvince')
  @Description('获取各省学校数量')
  @ApiResponse({ type: ProvinceSchoolResult })
  async getSchoolNumByProvince(@Query() params?: SchoolParams): Promise<ProvinceSchoolResult> {
    try {
      return await SchoolService.getByProvince(params)
    } catch (error) {
      throw new BadRequestException(`获取学校省份统计失败: ${error.message}`)
    }
  }

  @Get('/Schools/getSchoolNum')
  @Description('查询院校数量')
  @ApiResponse({ type: SchoolNumResult })
  async getSchoolNum(): Promise<SchoolNumResult> {
    try {
      return await SchoolService.getSchoolNum()
    } catch (error) {
      throw new BadRequestException(`查询双高院校比较失败: ${error.message}`)
    }
  }

  @Get('/Schools/updateDoubleHighStatus')
  @Description('更新双高院校标识')
  @ApiResponse({
    description: '更新结果',
    schema: {
      type: 'object',
      properties: { updated: { type: 'number' }, total: { type: 'number' } }
    }
  })
  async updateDoubleHighStatus(): Promise<{ updated: number; total: number }> {
    try {
      return await SchoolService.updateDoubleHighStatus()
    } catch (error) {
      throw new BadRequestException(`更新双高院校标识失败: ${error.message}`)
    }
  }
}
