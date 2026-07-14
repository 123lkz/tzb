import { ObjectIdString, Joi, ListResultPageInfo, ArraySchemaProperty, CloverApiProperty, ObjectSchemaProperty } from '@havenzhang/clover'
import endpoint from '../../../endpoints/JobMajorMapping'
export const JobMajorMapping_idValidator = Joi.objectId()
export const JobMajorMapping_idValidatorOptional = Joi.objectId().optional()
export const JobMajorMappingJob_codeValidator = endpoint['schema']['job_code'].validator
export const JobMajorMappingJob_codeValidatorOptional = endpoint['schema']['job_code'].validator.optional()
export const JobMajorMappingJob_nameValidator = endpoint['schema']['job_name'].validator
export const JobMajorMappingJob_nameValidatorOptional = endpoint['schema']['job_name'].validator.optional()
export const JobMajorMappingMajor_codeValidator = endpoint['schema']['major_code'].validator
export const JobMajorMappingMajor_codeValidatorOptional = endpoint['schema']['major_code'].validator.optional()
export const JobMajorMappingMajor_nameValidator = endpoint['schema']['major_name'].validator
export const JobMajorMappingMajor_nameValidatorOptional = endpoint['schema']['major_name'].validator.optional()
export const JobMajorMappingEducation_levelValidator = endpoint['schema']['education_level'].validator
export const JobMajorMappingEducation_levelValidatorOptional = endpoint['schema']['education_level'].validator.optional()
export const JobMajorMapping_etagValidator = endpoint['schema']['_etag'].validator
export const JobMajorMapping_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const JobMajorMapping_updatedValidator = endpoint['schema']['_updated'].validator
export const JobMajorMapping_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const JobMajorMapping_createdValidator = endpoint['schema']['_created'].validator
export const JobMajorMapping_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const JobMajorMappingListQueryValidator = Joi.object().keys({
  _id: JobMajorMapping_idValidator.optional(),
  job_code: JobMajorMappingJob_codeValidator.optional(),
  job_name: JobMajorMappingJob_nameValidator.optional(),
  major_code: JobMajorMappingMajor_codeValidator.optional(),
  major_name: JobMajorMappingMajor_nameValidator.optional(),
  education_level: JobMajorMappingEducation_levelValidator.optional()
})
export const AdminJobMajorMappingListQueryValidator = Joi.object().keys({
  _id: JobMajorMapping_idValidator.optional(),
  job_code: JobMajorMappingJob_codeValidator.optional(),
  job_name: JobMajorMappingJob_nameValidator.optional(),
  major_code: JobMajorMappingMajor_codeValidator.optional(),
  major_name: JobMajorMappingMajor_nameValidator.optional(),
  education_level: JobMajorMappingEducation_levelValidator.optional(),
  _etag: JobMajorMapping_etagValidator.optional(),
  _updated: JobMajorMapping_updatedValidator.optional(),
  _created: JobMajorMapping_createdValidator.optional()
})

export class JobMajorMappingLookupFields {
  _id?: string
  education_level?: string
  job_code?: string
  job_name?: string
  major_code?: string
  major_name?: string
}

export class JobMajorMappingAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  education_level?: string
  job_code?: string
  job_name?: string
  major_code?: string
  major_name?: string
}

export class AdminCreateJobMajorMapping {
  @CloverApiProperty({ required: false, validator: JobMajorMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: JobMajorMapping_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: JobMajorMapping_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: JobMajorMapping_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '学历层次', validator: JobMajorMappingEducation_levelValidator })
  education_level: string
  @CloverApiProperty({ description: '职业编码', validator: JobMajorMappingJob_codeValidator })
  job_code: string
  @CloverApiProperty({ description: '职业名称', validator: JobMajorMappingJob_nameValidator })
  job_name: string
  @CloverApiProperty({ description: '专业代码', validator: JobMajorMappingMajor_codeValidator })
  major_code: string
  @CloverApiProperty({ description: '专业名称', validator: JobMajorMappingMajor_nameValidator })
  major_name: string
}

export class AdminUpdateJobMajorMapping {
  @CloverApiProperty({ required: false, validator: JobMajorMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: JobMajorMapping_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: JobMajorMapping_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: JobMajorMapping_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '学历层次', required: false, validator: JobMajorMappingEducation_levelValidatorOptional })
  education_level?: string
  @CloverApiProperty({ description: '职业编码', required: false, validator: JobMajorMappingJob_codeValidatorOptional })
  job_code?: string
  @CloverApiProperty({ description: '职业名称', required: false, validator: JobMajorMappingJob_nameValidatorOptional })
  job_name?: string
  @CloverApiProperty({ description: '专业代码', required: false, validator: JobMajorMappingMajor_codeValidatorOptional })
  major_code?: string
  @CloverApiProperty({ description: '专业名称', required: false, validator: JobMajorMappingMajor_nameValidatorOptional })
  major_name?: string
}

export class AdminListJobMajorMappingItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '学历层次' })
  education_level: string
  @CloverApiProperty({ description: '职业编码' })
  job_code: string
  @CloverApiProperty({ description: '职业名称' })
  job_name: string
  @CloverApiProperty({ description: '专业代码' })
  major_code: string
  @CloverApiProperty({ description: '专业名称' })
  major_name: string
}

export class AdminGetJobMajorMappingResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '学历层次' })
  education_level: string
  @CloverApiProperty({ description: '职业编码' })
  job_code: string
  @CloverApiProperty({ description: '职业名称' })
  job_name: string
  @CloverApiProperty({ description: '专业代码' })
  major_code: string
  @CloverApiProperty({ description: '专业名称' })
  major_name: string
}

export class ReplaceJobMajorMapping {
  @CloverApiProperty({ required: false, validator: JobMajorMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '学历层次', validator: JobMajorMappingEducation_levelValidator })
  education_level: string
  @CloverApiProperty({ description: '职业编码', validator: JobMajorMappingJob_codeValidator })
  job_code: string
  @CloverApiProperty({ description: '职业名称', validator: JobMajorMappingJob_nameValidator })
  job_name: string
  @CloverApiProperty({ description: '专业代码', validator: JobMajorMappingMajor_codeValidator })
  major_code: string
  @CloverApiProperty({ description: '专业名称', validator: JobMajorMappingMajor_nameValidator })
  major_name: string
}

export class CreateJobMajorMapping {
  @CloverApiProperty({ required: false, validator: JobMajorMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '学历层次', validator: JobMajorMappingEducation_levelValidator })
  education_level: string
  @CloverApiProperty({ description: '职业编码', validator: JobMajorMappingJob_codeValidator })
  job_code: string
  @CloverApiProperty({ description: '职业名称', validator: JobMajorMappingJob_nameValidator })
  job_name: string
  @CloverApiProperty({ description: '专业代码', validator: JobMajorMappingMajor_codeValidator })
  major_code: string
  @CloverApiProperty({ description: '专业名称', validator: JobMajorMappingMajor_nameValidator })
  major_name: string
}

export class ListJobMajorMappingItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '学历层次' })
  education_level: string
  @CloverApiProperty({ description: '职业编码' })
  job_code: string
  @CloverApiProperty({ description: '职业名称' })
  job_name: string
  @CloverApiProperty({ description: '专业代码' })
  major_code: string
  @CloverApiProperty({ description: '专业名称' })
  major_name: string
}

export class GetJobMajorMappingResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '学历层次' })
  education_level: string
  @CloverApiProperty({ description: '职业编码' })
  job_code: string
  @CloverApiProperty({ description: '职业名称' })
  job_name: string
  @CloverApiProperty({ description: '专业代码' })
  major_code: string
  @CloverApiProperty({ description: '专业名称' })
  major_name: string
}

export interface JobMajorMappingCombinedId {
  _id?: string
}

export class ListJobMajorMappingResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListJobMajorMappingItem] })
  _items: ListJobMajorMappingItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListJobMajorMappingResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListJobMajorMappingItem] })
  _items: AdminListJobMajorMappingItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertJobMajorMapping {
}

export class UpdateJobMajorMapping {
}

export class RemoveJobMajorMapping {
}

export class JobMajorMappingCombinedId {
}

export interface JobMajorMappingDtoType {
  item: GetJobMajorMappingResult
  create: CreateJobMajorMapping
  replace: ReplaceJobMajorMapping
  update: UpdateJobMajorMapping
}
