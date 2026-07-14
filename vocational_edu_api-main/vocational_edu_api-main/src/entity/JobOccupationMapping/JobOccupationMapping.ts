import { createEntityService } from '@havenzhang/clover'
import { JobOccupationMappingDtoType } from '../../base/entity/JobOccupationMapping/JobOccupationMapping.dto'
import {
  createJobOccupationMappingModel,
  JobOccupationMappingModel,
  JobOccupationMappingSchema
} from '../../base/entity/JobOccupationMapping/JobOccupationMapping.model'
import endpoint from '../../endpoints/JobOccupationMapping'
const jobOccupationMappingModel = createJobOccupationMappingModel(JobOccupationMappingSchema)
export const JobOccupationMappingEntity = createEntityService<JobOccupationMappingModel, JobOccupationMappingDtoType>(
  endpoint,
  jobOccupationMappingModel
)
