import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import { Description, CloverController, Etag, User, IUser, CheckRoles, RestFilter, CombinedId, RemoveResult, MutateResult, ListQueryWithPaging } from '@havenzhang/clover'
import { JobOccupationMappingEntity } from '../../../entity/JobOccupationMapping/JobOccupationMapping'
import { JobOccupationMappingCombinedId, ReplaceJobOccupationMapping, CreateJobOccupationMapping, UpdateJobOccupationMapping, GetJobOccupationMappingResult, ListJobOccupationMappingResult, JobOccupationMappingListQueryValidator } from './JobOccupationMapping.dto'

@CloverController(JobOccupationMappingEntity)
export class JobOccupationMappingControllerBase {
  protected readonly jobOccupationMapping = JobOccupationMappingEntity

  @Get('/JobOccupationMapping')
  @ApiResponse({ type: ListJobOccupationMappingResult })
  @ApiExtension('x-lookup-property', ['_id', 'position_name'])
  @Description('获取职位到标准职业映射列表')
  list(@User() user: IUser, @Query() listQuery: ListQueryWithPaging): Promise<ListJobOccupationMappingResult> {
    return this.jobOccupationMapping.query(user, listQuery, { queryValidator: JobOccupationMappingListQueryValidator })
  }
}
