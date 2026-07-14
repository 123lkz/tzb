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
  SchoolEnrollmentCombinedId,
  AdminGetSchoolEnrollmentResult,
  AdminListSchoolEnrollmentResult,
  AdminUpdateSchoolEnrollment,
  AdminCreateSchoolEnrollment,
  AdminSchoolEnrollmentListQueryValidator
} from './SchoolEnrollment.dto'
import { SchoolEnrollmentEntity } from '../../../entity/SchoolEnrollment/SchoolEnrollment'

@CloverController(SchoolEnrollmentEntity)
@ApiTags('学校招生')
@UseGuards(CloverAPIAccountGuard)
export class SchoolEnrollmentControllerAdmin {
  private readonly schoolEnrollment = SchoolEnrollmentEntity

  @Get('/SchoolEnrollment')
  @ApiResponse({ type: () => AdminListSchoolEnrollmentResult })
  @Description('获取学校招生列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.schoolEnrollment.query(
      {},
      listQuery,
      { queryValidator: AdminSchoolEnrollmentListQueryValidator },
      { skipSoftDelete: true, skipProjectionCheck: true }
    )
  }

  @Post('/SchoolEnrollment')
  @ApiResponse({ type: MutateResult })
  @Description('创建学校招生')
  create(@Body() input: AdminCreateSchoolEnrollment): Promise<MutateResult> {
    return this.schoolEnrollment.create({}, input)
  }

  @Patch('/SchoolEnrollment/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新学校招生')
  update(
    @CombinedId() combinedId: SchoolEnrollmentCombinedId,
    @Body() input: AdminUpdateSchoolEnrollment,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.schoolEnrollment.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/SchoolEnrollment/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换学校招生')
  replace(
    @CombinedId() combinedId: SchoolEnrollmentCombinedId,
    @Body() input: AdminCreateSchoolEnrollment,
    @Headers('If-Match') etag: string
  ): Promise<MutateResult> {
    return this.schoolEnrollment.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/SchoolEnrollment/:combinedId')
  @ApiResponse({ type: () => AdminGetSchoolEnrollmentResult })
  @Description('获取学校招生')
  getOne(@CombinedId() combinedId: SchoolEnrollmentCombinedId) {
    return this.schoolEnrollment.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/SchoolEnrollment/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除学校招生')
  remove(
    @CombinedId() combinedId: SchoolEnrollmentCombinedId,
    @Headers('If-Match') etag: string,
    @Query('force') force?: boolean
  ): Promise<RemoveResult> {
    return this.schoolEnrollment.remove(
      {},
      combinedId,
      etag,
      force ? { skipSoftDelete: true, skipEtagCheck: true } : {}
    )
  }

  @Get('/SchoolEnrollment/_collection_stat')
  @Description('Stat学校招生')
  async statCollection() {
    const ret = (
      await this.schoolEnrollment.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true })
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
