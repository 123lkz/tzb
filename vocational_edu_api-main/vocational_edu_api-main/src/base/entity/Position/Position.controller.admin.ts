import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { PositionCombinedId, AdminGetPositionResult, AdminListPositionResult, AdminUpdatePosition, AdminCreatePosition, AdminPositionListQueryValidator } from './Position.dto'
import { PositionEntity } from '../../../entity/Position/Position'

@CloverController(PositionEntity)
@ApiTags('职位')
@UseGuards(CloverAPIAccountGuard)
export class PositionControllerAdmin {
  private readonly position = PositionEntity

  @Get('/Position')
  @ApiResponse({ type: () => AdminListPositionResult })
  @Description('获取职位列表')
  list(@Query() listQuery: ListQuery) {
    return this.position.query({}, listQuery, { queryValidator: AdminPositionListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/Position')
  @ApiResponse({ type: MutateResult })
  @Description('创建职位')
  create(@Body() input: AdminCreatePosition): Promise<MutateResult> {
    return this.position.create({}, input)
  }

  @Patch('/Position/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新职位')
  update(@CombinedId() combinedId: PositionCombinedId, @Body() input: AdminUpdatePosition, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.position.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/Position/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换职位')
  replace(@CombinedId() combinedId: PositionCombinedId, @Body() input: AdminCreatePosition, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.position.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/Position/:combinedId')
  @ApiResponse({ type: () => AdminGetPositionResult })
  @Description('获取职位')
  getOne(@CombinedId() combinedId: PositionCombinedId) {
    return this.position.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/Position/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除职位')
  remove(@CombinedId() combinedId: PositionCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.position.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/Position/_collection_stat')
  @Description('Stat职位')
  async statCollection() {
    const ret = (await this.position.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
    return {
      size: ret.storageStats.size,
      count: ret.storageStats.count,
      avgObjSize: ret.storageStats.avgObjSize,
      storageSize: ret.storageStats.storageSize,
      totalSize: ret.storageStats.totalSize,
      totalIndexSize: ret.storageStats.totalIndexSize,
      indexSizes: ret.storageStats.indexSizes,
    }
  }
}

