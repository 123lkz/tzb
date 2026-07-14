import { CloverController, Description } from '@havenzhang/clover'
import { Get, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { OccupationCategoriesControllerBase } from '../../base/entity/OccupationCategories/OccupationCategories.controller'
import {
  GradeTreeItem,
  OccupationDownQuery,
  OccupationDownResult,
  OccupationUpQuery,
  OccupationUpResult
} from './OccupationCategories.dto'
import { OccupationCategoriesService } from './OccupationCategories.service'

@CloverController()
@ApiTags('标准职业分类')
export class OccupationCategoriesController extends OccupationCategoriesControllerBase {
  @Get('/occupationCategories/standard/all')
  @Description('返回分级数据')
  @ApiResponse({ type: [GradeTreeItem] })
  async getGradeList(): Promise<GradeTreeItem[]> {
    return await OccupationCategoriesService.getGradeList()
  }

  @Get('/occupationCategories/standard/up')
  @Description('返回当前级别及其上层的数据')
  @ApiResponse({ type: OccupationUpResult })
  async getUpByLevel(@Query() query: OccupationUpQuery): Promise<OccupationUpResult> {
    return await OccupationCategoriesService.getUpByLevel(query)
  }

  @Get('/occupationCategories/standard/down')
  @Description('返回当前级别及其下属数据')
  @ApiResponse({ type: OccupationDownResult })
  async getDownByLevel(@Query() query: OccupationDownQuery): Promise<OccupationDownResult> {
    return await OccupationCategoriesService.getDownByLevel(query)
  }
}
