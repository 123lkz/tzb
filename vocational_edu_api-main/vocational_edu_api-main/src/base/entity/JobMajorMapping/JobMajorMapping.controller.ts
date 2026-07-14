import { CloverController, Description, IUser, ListQueryWithPaging, User } from '@havenzhang/clover'
import { Get, Query } from '@nestjs/common'
import { ApiExtension, ApiResponse } from '@nestjs/swagger'
import { JobMajorMappingEntity } from '../../../entity/JobMajorMapping/JobMajorMapping'
import { JobMajorMappingListQueryValidator, ListJobMajorMappingResult } from './JobMajorMapping.dto'

@CloverController(JobMajorMappingEntity)
export class JobMajorMappingControllerBase {
  protected readonly jobMajorMapping = JobMajorMappingEntity

  @Get('/JobMajorMapping')
  @ApiResponse({ type: ListJobMajorMappingResult })
  @ApiExtension('x-lookup-property', ['_id', 'education_level', 'job_code', 'job_name', 'major_code', 'major_name'])
  @Description('获取职业对应专业列表')
  list(@User() user: IUser, @Query() listQuery: ListQueryWithPaging): Promise<ListJobMajorMappingResult> {
    return this.jobMajorMapping.query(user, listQuery, { queryValidator: JobMajorMappingListQueryValidator })
  }
}
