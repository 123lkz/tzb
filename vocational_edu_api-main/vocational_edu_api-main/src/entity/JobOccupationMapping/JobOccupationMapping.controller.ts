import { CloverController } from '@havenzhang/clover'
import { ApiTags } from '@nestjs/swagger'
import { JobOccupationMappingControllerBase } from '../../base/entity/JobOccupationMapping/JobOccupationMapping.controller'

@CloverController()
@ApiTags('职位到标准职业分类映射表')
export class JobOccupationMappingController extends JobOccupationMappingControllerBase {}
