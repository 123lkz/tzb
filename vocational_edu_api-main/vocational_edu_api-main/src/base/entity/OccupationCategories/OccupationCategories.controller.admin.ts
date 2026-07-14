import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQueryWithPaging } from '@havenzhang/clover'
import { OccupationCategoriesCombinedId, AdminGetOccupationCategoriesResult, AdminListOccupationCategoriesResult, AdminUpdateOccupationCategories, AdminCreateOccupationCategories, AdminOccupationCategoriesListQueryValidator } from './OccupationCategories.dto'
import { OccupationCategoriesEntity } from '../../../entity/OccupationCategories/OccupationCategories'

@CloverController(OccupationCategoriesEntity)
@ApiTags('标准职业分类')
@UseGuards(CloverAPIAccountGuard)
export class OccupationCategoriesControllerAdmin {
  private readonly occupationCategories = OccupationCategoriesEntity

  @Get('/OccupationCategories')
  @ApiResponse({ type: () => AdminListOccupationCategoriesResult })
  @Description('获取标准职业分类列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.occupationCategories.query({}, listQuery, { queryValidator: AdminOccupationCategoriesListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/OccupationCategories')
  @ApiResponse({ type: MutateResult })
  @Description('创建标准职业分类')
  create(@Body() input: AdminCreateOccupationCategories): Promise<MutateResult> {
    return this.occupationCategories.create({}, input)
  }

  @Patch('/OccupationCategories/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新标准职业分类')
  update(@CombinedId() combinedId: OccupationCategoriesCombinedId, @Body() input: AdminUpdateOccupationCategories, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.occupationCategories.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/OccupationCategories/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换标准职业分类')
  replace(@CombinedId() combinedId: OccupationCategoriesCombinedId, @Body() input: AdminCreateOccupationCategories, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.occupationCategories.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/OccupationCategories/:combinedId')
  @ApiResponse({ type: () => AdminGetOccupationCategoriesResult })
  @Description('获取标准职业分类')
  getOne(@CombinedId() combinedId: OccupationCategoriesCombinedId) {
    return this.occupationCategories.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/OccupationCategories/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除标准职业分类')
  remove(@CombinedId() combinedId: OccupationCategoriesCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.occupationCategories.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/OccupationCategories/_collection_stat')
  @Description('Stat标准职业分类')
  async statCollection() {
    const ret = (await this.occupationCategories.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
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

