import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { CompanyCombinedId, AdminGetCompanyResult, AdminListCompanyResult, AdminUpdateCompany, AdminCreateCompany, AdminCompanyListQueryValidator } from './Company.dto'
import { CompanyEntity } from '../../../entity/Company/Company'

@CloverController(CompanyEntity)
@ApiTags('公司')
@UseGuards(CloverAPIAccountGuard)
export class CompanyControllerAdmin {
  private readonly company = CompanyEntity

  @Get('/Company')
  @ApiResponse({ type: () => AdminListCompanyResult })
  @Description('获取公司列表')
  list(@Query() listQuery: ListQuery) {
    return this.company.query({}, listQuery, { queryValidator: AdminCompanyListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/Company')
  @ApiResponse({ type: MutateResult })
  @Description('创建公司')
  create(@Body() input: AdminCreateCompany): Promise<MutateResult> {
    return this.company.create({}, input)
  }

  @Patch('/Company/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新公司')
  update(@CombinedId() combinedId: CompanyCombinedId, @Body() input: AdminUpdateCompany, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.company.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/Company/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换公司')
  replace(@CombinedId() combinedId: CompanyCombinedId, @Body() input: AdminCreateCompany, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.company.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/Company/:combinedId')
  @ApiResponse({ type: () => AdminGetCompanyResult })
  @Description('获取公司')
  getOne(@CombinedId() combinedId: CompanyCombinedId) {
    return this.company.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/Company/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除公司')
  remove(@CombinedId() combinedId: CompanyCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.company.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/Company/_collection_stat')
  @Description('Stat公司')
  async statCollection() {
    const ret = (await this.company.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
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

