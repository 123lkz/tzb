import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQueryWithPaging } from '@havenzhang/clover'
import { JobMajorMappingCombinedId, AdminGetJobMajorMappingResult, AdminListJobMajorMappingResult, AdminUpdateJobMajorMapping, AdminCreateJobMajorMapping, AdminJobMajorMappingListQueryValidator } from './JobMajorMapping.dto'
import { JobMajorMappingEntity } from '../../../entity/JobMajorMapping/JobMajorMapping'

@CloverController(JobMajorMappingEntity)
@ApiTags('职业-专业对应表')
@UseGuards(CloverAPIAccountGuard)
export class JobMajorMappingControllerAdmin {
  private readonly jobMajorMapping = JobMajorMappingEntity

  @Get('/JobMajorMapping')
  @ApiResponse({ type: () => AdminListJobMajorMappingResult })
  @Description('获取职业-专业对应表列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.jobMajorMapping.query({}, listQuery, { queryValidator: AdminJobMajorMappingListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/JobMajorMapping')
  @ApiResponse({ type: MutateResult })
  @Description('创建职业-专业对应表')
  create(@Body() input: AdminCreateJobMajorMapping): Promise<MutateResult> {
    return this.jobMajorMapping.create({}, input)
  }

  @Patch('/JobMajorMapping/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新职业-专业对应表')
  update(@CombinedId() combinedId: JobMajorMappingCombinedId, @Body() input: AdminUpdateJobMajorMapping, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.jobMajorMapping.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/JobMajorMapping/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换职业-专业对应表')
  replace(@CombinedId() combinedId: JobMajorMappingCombinedId, @Body() input: AdminCreateJobMajorMapping, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.jobMajorMapping.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/JobMajorMapping/:combinedId')
  @ApiResponse({ type: () => AdminGetJobMajorMappingResult })
  @Description('获取职业-专业对应表')
  getOne(@CombinedId() combinedId: JobMajorMappingCombinedId) {
    return this.jobMajorMapping.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/JobMajorMapping/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除职业-专业对应表')
  remove(@CombinedId() combinedId: JobMajorMappingCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.jobMajorMapping.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/JobMajorMapping/_collection_stat')
  @Description('Stat职业-专业对应表')
  async statCollection() {
    const ret = (await this.jobMajorMapping.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
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

