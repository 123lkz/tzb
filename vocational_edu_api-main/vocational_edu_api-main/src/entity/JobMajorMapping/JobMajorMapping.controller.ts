import { CloverController } from '@havenzhang/clover'
import { ApiTags } from '@nestjs/swagger'
import { JobMajorMappingControllerBase } from '../../base/entity/JobMajorMapping/JobMajorMapping.controller'

@CloverController()
@ApiTags('职业-专业对应表')
export class JobMajorMappingController extends JobMajorMappingControllerBase {}
