import { createEntityService } from '@havenzhang/clover'
import { SchoolEnrollmentDtoType } from '../../base/entity/SchoolEnrollment/SchoolEnrollment.dto'
import {
  createSchoolEnrollmentModel,
  SchoolEnrollmentModel,
  SchoolEnrollmentSchema
} from '../../base/entity/SchoolEnrollment/SchoolEnrollment.model'
import endpoint from '../../endpoints/SchoolEnrollment'
const schoolEnrollmentModel = createSchoolEnrollmentModel(SchoolEnrollmentSchema)
export const SchoolEnrollmentEntity = createEntityService<SchoolEnrollmentModel, SchoolEnrollmentDtoType>(
  endpoint,
  schoolEnrollmentModel
)
