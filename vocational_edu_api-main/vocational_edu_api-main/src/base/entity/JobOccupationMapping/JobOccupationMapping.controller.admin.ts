import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQueryWithPaging } from '@havenzhang/clover'
import { JobOccupationMappingCombinedId, AdminGetJobOccupationMappingResult, AdminListJobOccupationMappingResult, AdminUpdateJobOccupationMapping, AdminCreateJobOccupationMapping, AdminJobOccupationMappingListQueryValidator } from './JobOccupationMapping.dto'
import { JobOccupationMappingEntity } from '../../../entity/JobOccupationMapping/JobOccupationMapping'

@CloverController(JobOccupationMappingEntity)
@ApiTags('职位到标准职业分类映射表')
@UseGuards(CloverAPIAccountGuard)
export class JobOccupationMappingControllerAdmin {
  private readonly jobOccupationMapping = JobOccupationMappingEntity

  @Get('/JobOccupationMapping')
  @ApiResponse({ type: () => AdminListJobOccupationMappingResult })
  @Description('获取职位到标准职业分类映射表列表')
  list(@Query() listQuery: ListQueryWithPaging) {
    return this.jobOccupationMapping.query({}, listQuery, { queryValidator: AdminJobOccupationMappingListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/JobOccupationMapping')
  @ApiResponse({ type: MutateResult })
  @Description('创建职位到标准职业分类映射表')
  create(@Body() input: AdminCreateJobOccupationMapping): Promise<MutateResult> {
    return this.jobOccupationMapping.create({}, input)
  }

  @Patch('/JobOccupationMapping/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新职位到标准职业分类映射表')
  update(@CombinedId() combinedId: JobOccupationMappingCombinedId, @Body() input: AdminUpdateJobOccupationMapping, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.jobOccupationMapping.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/JobOccupationMapping/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换职位到标准职业分类映射表')
  replace(@CombinedId() combinedId: JobOccupationMappingCombinedId, @Body() input: AdminCreateJobOccupationMapping, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.jobOccupationMapping.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/JobOccupationMapping/:combinedId')
  @ApiResponse({ type: () => AdminGetJobOccupationMappingResult })
  @Description('获取职位到标准职业分类映射表')
  getOne(@CombinedId() combinedId: JobOccupationMappingCombinedId) {
    return this.jobOccupationMapping.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/JobOccupationMapping/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除职位到标准职业分类映射表')
  remove(@CombinedId() combinedId: JobOccupationMappingCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.jobOccupationMapping.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/JobOccupationMapping/_collection_stat')
  @Description('Stat职位到标准职业分类映射表')
  async statCollection() {
    const ret = (await this.jobOccupationMapping.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
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

