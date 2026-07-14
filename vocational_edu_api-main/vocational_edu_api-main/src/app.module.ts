import { Module } from '@nestjs/common'
import { APP_GUARD } from '@nestjs/core'
import { ScheduleModule } from '@nestjs/schedule'
import { BaseController } from './entity/Base/Base.controller'
import { CompanyController } from './entity/Company/Company.controller'
import { IndustryController } from './entity/Industry/Industry.controller'
import { JobMajorMappingController } from './entity/JobMajorMapping/JobMajorMapping.controller'
import { JobOccupationMappingController } from './entity/JobOccupationMapping/JobOccupationMapping.controller'
import { OccupationCategoriesController } from './entity/OccupationCategories/OccupationCategories.controller'
import { PositionController } from './entity/Position/Position.controller'
import { SalaryController } from './entity/Salary/Salary.controller'
import { SchoolController } from './entity/School/School.controller'
import { SchoolEnrollmentController } from './entity/SchoolEnrollment/SchoolEnrollment.controller'
import { UserController } from './entity/User/User.controller'
import { UserGuard } from './guards/UserGuard'
import { BaseCacheTask } from './tasks/BaseCacheTask'

@Module({
  imports: [ScheduleModule.forRoot()],
  controllers: [
    UserController,
    BaseController,
    PositionController,
    SalaryController,
    CompanyController,
    SchoolController,
    SchoolEnrollmentController,
    JobMajorMappingController,
    JobOccupationMappingController,
    OccupationCategoriesController,
    IndustryController
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: UserGuard
    },
    BaseCacheTask
  ]
})
export class AppModule {}
