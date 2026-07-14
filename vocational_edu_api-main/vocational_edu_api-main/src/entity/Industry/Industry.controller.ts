import { CloverController, Description } from '@havenzhang/clover'
import { Get } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { IndustryControllerBase } from '../../base/entity/Industry/Industry.controller'
import { GradeTreeItem } from './Industry.dto'
import { IndustryService } from './Industry.service'

@CloverController()
@ApiTags('标准行业')
export class IndustryController extends IndustryControllerBase {
  @Get('/industry/standard/all')
  @Description('返回分级数据（从2级开始，支持到5级）')
  @ApiResponse({ type: [GradeTreeItem] })
  async getGradeList(): Promise<GradeTreeItem[]> {
    return await IndustryService.getGradeList()
  }
}
