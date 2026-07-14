import { createEntityService } from '@havenzhang/clover'
import { JobMajorMappingDtoType } from '../../base/entity/JobMajorMapping/JobMajorMapping.dto'
import {
  createJobMajorMappingModel,
  JobMajorMappingModel,
  JobMajorMappingSchema
} from '../../base/entity/JobMajorMapping/JobMajorMapping.model'
import endpoint from '../../endpoints/JobMajorMapping'
const jobMajorMappingModel = createJobMajorMappingModel(JobMajorMappingSchema)
export const JobMajorMappingEntity = createEntityService<JobMajorMappingModel, JobMajorMappingDtoType>(
  endpoint,
  jobMajorMappingModel
)
