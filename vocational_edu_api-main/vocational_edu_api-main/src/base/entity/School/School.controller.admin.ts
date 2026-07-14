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
  SchoolCombinedId,
  AdminGetSchoolResult,
  AdminListSchoolResult,
  AdminUpdateSchool,
  AdminCreateSchool,
  AdminSchoolListQueryValidator
} from './School.dto'
import { SchoolEntity } from '../../../entity/School/School'

@CloverController(SchoolEntity)
@ApiTags('学校')
@UseGuards(CloverAPIAccountGuard)
export class SchoolControllerAdmin {
  private readonly school = SchoolEntity

  @Get('/School')
  @ApiResponse({ type: () => AdminListSchoolResult })
  @Description('获取学校列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.school.query(
      {},
      listQuery,
      { queryValidator: AdminSchoolListQueryValidator },
      { skipSoftDelete: true, skipProjectionCheck: true }
    )
  }

  @Post('/School')
  @ApiResponse({ type: MutateResult })
  @Description('创建学校')
  create(@Body() input: AdminCreateSchool): Promise<MutateResult> {
    return this.school.create({}, input)
  }

  @Patch('/School/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新学校')
  update(
    @CombinedId() combinedId: SchoolCombinedId,
    @Body() input: AdminUpdateSchool,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.school.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/School/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换学校')
  replace(
    @CombinedId() combinedId: SchoolCombinedId,
    @Body() input: AdminCreateSchool,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.school.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/School/:combinedId')
  @ApiResponse({ type: () => AdminGetSchoolResult })
  @Description('获取学校')
  getOne(@CombinedId() combinedId: SchoolCombinedId) {
    return this.school.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/School/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除学校')
  remove(
    @CombinedId() combinedId: SchoolCombinedId,
    @Headers('If-Match') etag: string,
    @Query('force') force?: boolean
  ): Promise<RemoveResult> {
    return this.school.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/School/_collection_stat')
  @Description('Stat学校')
  async statCollection() {
    const ret = (await this.school.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
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
