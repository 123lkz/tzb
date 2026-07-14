import { Module } from '@nestjs/common'
import { UserControllerAdmin } from './entity/User/User.controller.admin'
import { SchoolControllerAdmin } from './entity/School/School.controller.admin'
import { SchoolEnrollmentControllerAdmin } from './entity/SchoolEnrollment/SchoolEnrollment.controller.admin'
import { PositionControllerAdmin } from './entity/Position/Position.controller.admin'
import { OccupationCategoriesControllerAdmin } from './entity/OccupationCategories/OccupationCategories.controller.admin'
import { JobOccupationMappingControllerAdmin } from './entity/JobOccupationMapping/JobOccupationMapping.controller.admin'
import { JobMajorMappingControllerAdmin } from './entity/JobMajorMapping/JobMajorMapping.controller.admin'
import { IndustryControllerAdmin } from './entity/Industry/Industry.controller.admin'
import { CompanyControllerAdmin } from './entity/Company/Company.controller.admin'

@Module({
  controllers: [
    UserControllerAdmin,
    SchoolControllerAdmin,
    SchoolEnrollmentControllerAdmin,
    PositionControllerAdmin,
    OccupationCategoriesControllerAdmin,
    JobOccupationMappingControllerAdmin,
    JobMajorMappingControllerAdmin,
    IndustryControllerAdmin,
    CompanyControllerAdmin
  ]
})
export class AdminModule {
}
