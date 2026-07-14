import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import {
  Description,
  CloverAPIAccountGuard,
  CloverController,
  CombinedId,
  RemoveResult,
  MutateResult,
  ListQueryWithPaging
} from '@havenzhang/clover'
import {
  IndustryCombinedId,
  AdminGetIndustryResult,
  AdminListIndustryResult,
  AdminUpdateIndustry,
  AdminCreateIndustry,
  AdminIndustryListQueryValidator
} from './Industry.dto'
import { IndustryEntity } from '../../../entity/Industry/Industry'

@CloverController(IndustryEntity)
@ApiTags('标准行业')
@UseGuards(CloverAPIAccountGuard)
export class IndustryControllerAdmin {
  private readonly industry = IndustryEntity

  @Get('/Industry')
  @ApiResponse({ type: () => AdminListIndustryResult })
  @Description('获取标准行业列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.industry.query(
      {},
      listQuery,
      { queryValidator: AdminIndustryListQueryValidator },
      { skipSoftDelete: true, skipProjectionCheck: true }
    )
  }

  @Post('/Industry')
  @ApiResponse({ type: MutateResult })
  @Description('创建标准行业')
  create(@Body() input: AdminCreateIndustry): Promise<MutateResult> {
    return this.industry.create({}, input)
  }

  @Patch('/Industry/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新标准行业')
  update(
    @CombinedId() combinedId: IndustryCombinedId,
    @Body() input: AdminUpdateIndustry,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.industry.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/Industry/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换标准行业')
  replace(
    @CombinedId() combinedId: IndustryCombinedId,
    @Body() input: AdminCreateIndustry,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.industry.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/Industry/:combinedId')
  @ApiResponse({ type: () => AdminGetIndustryResult })
  @Description('获取标准行业')
  getOne(@CombinedId() combinedId: IndustryCombinedId) {
    return this.industry.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/Industry/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除标准行业')
  remove(
    @CombinedId() combinedId: IndustryCombinedId,
    @Headers('If-Match') etag: string,
    @Query('force') force?: boolean
  ): Promise<RemoveResult> {
    return this.industry.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/Industry/_collection_stat')
  @Description('Stat标准行业')
  async statCollection() {
    const ret = (
      await this.industry.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true })
    )[0]
    return {
      size: ret.storageStats.size,
      count: ret.storageStats.count,
      avgObjSize: ret.storageStats.avgObjSize,
      storageSize: ret.storageStats.storageSize,
      totalSize: ret.storageStats.totalSize,
      totalIndexSize: ret.storageStats.totalIndexSize,
      indexSizes: ret.storageStats.indexSizes
    }
  }
}
