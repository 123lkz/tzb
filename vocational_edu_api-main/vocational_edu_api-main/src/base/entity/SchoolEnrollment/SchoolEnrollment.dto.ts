import {
  ObjectIdString,
  Joi,
  ListResultPageInfo,
  ArraySchemaProperty,
  CloverApiProperty,
  ObjectSchemaProperty
} from '@havenzhang/clover'
import endpoint from '../../../endpoints/SchoolEnrollment'
export const SchoolEnrollment_idValidator = Joi.objectId()
export const SchoolEnrollment_idValidatorOptional = Joi.objectId().optional()
export const SchoolEnrollmentSource_regionValidator = endpoint['schema']['source_region'].validator
export const SchoolEnrollmentSource_regionValidatorOptional = endpoint['schema']['source_region'].validator.optional()
export const SchoolEnrollmentSchool_locationValidator = endpoint['schema']['school_location'].validator
export const SchoolEnrollmentSchool_locationValidatorOptional =
  endpoint['schema']['school_location'].validator.optional()
export const SchoolEnrollmentYearValidator = endpoint['schema']['year'].validator
export const SchoolEnrollmentYearValidatorOptional = endpoint['schema']['year'].validator.optional()
export const SchoolEnrollmentCategoryValidator = endpoint['schema']['category'].validator
export const SchoolEnrollmentCategoryValidatorOptional = endpoint['schema']['category'].validator.optional()
export const SchoolEnrollmentBatchValidator = endpoint['schema']['batch'].validator
export const SchoolEnrollmentBatchValidatorOptional = endpoint['schema']['batch'].validator.optional()
export const SchoolEnrollmentSubject_typeValidator = endpoint['schema']['subject_type'].validator
export const SchoolEnrollmentSubject_typeValidatorOptional = endpoint['schema']['subject_type'].validator.optional()
export const SchoolEnrollmentMajorValidator = endpoint['schema']['major'].validator
export const SchoolEnrollmentMajorValidatorOptional = endpoint['schema']['major'].validator.optional()
export const SchoolEnrollmentAverage_scoreValidator = endpoint['schema']['average_score'].validator
export const SchoolEnrollmentAverage_scoreValidatorOptional = endpoint['schema']['average_score'].validator.optional()
export const SchoolEnrollmentMin_scoreValidator = endpoint['schema']['min_score'].validator
export const SchoolEnrollmentMin_scoreValidatorOptional = endpoint['schema']['min_score'].validator.optional()
export const SchoolEnrollmentMax_scoreValidator = endpoint['schema']['max_score'].validator
export const SchoolEnrollmentMax_scoreValidatorOptional = endpoint['schema']['max_score'].validator.optional()
export const SchoolEnrollmentMin_rankValidator = endpoint['schema']['min_rank'].validator
export const SchoolEnrollmentMin_rankValidatorOptional = endpoint['schema']['min_rank'].validator.optional()
export const SchoolEnrollmentSchoolValidator = Joi.number()
export const SchoolEnrollmentSchoolValidatorOptional = Joi.number().optional()
export const SchoolEnrollmentEnrollment_countValidator = endpoint['schema']['enrollment_count'].validator
export const SchoolEnrollmentEnrollment_countValidatorOptional =
  endpoint['schema']['enrollment_count'].validator.optional()
export const SchoolEnrollmentSchool_nameValidator = endpoint['schema']['school_name'].validator
export const SchoolEnrollmentSchool_nameValidatorOptional = endpoint['schema']['school_name'].validator.optional()
export const SchoolEnrollmentSchool_codeValidator = endpoint['schema']['school_code'].validator
export const SchoolEnrollmentSchool_codeValidatorOptional = endpoint['schema']['school_code'].validator.optional()
export const SchoolEnrollment_etagValidator = endpoint['schema']['_etag'].validator
export const SchoolEnrollment_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const SchoolEnrollment_updatedValidator = endpoint['schema']['_updated'].validator
export const SchoolEnrollment_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const SchoolEnrollment_createdValidator = endpoint['schema']['_created'].validator
export const SchoolEnrollment_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const SchoolEnrollmentListQueryValidator = Joi.object().keys({
  _id: SchoolEnrollment_idValidator.optional(),
  source_region: SchoolEnrollmentSource_regionValidator.optional(),
  school_location: SchoolEnrollmentSchool_locationValidator.optional(),
  year: SchoolEnrollmentYearValidator.optional(),
  category: SchoolEnrollmentCategoryValidator.optional(),
  batch: SchoolEnrollmentBatchValidator.optional(),
  subject_type: SchoolEnrollmentSubject_typeValidator.optional(),
  major: SchoolEnrollmentMajorValidator.optional(),
  average_score: SchoolEnrollmentAverage_scoreValidator.optional(),
  min_score: SchoolEnrollmentMin_scoreValidator.optional(),
  max_score: SchoolEnrollmentMax_scoreValidator.optional(),
  min_rank: SchoolEnrollmentMin_rankValidator.optional(),
  school: SchoolEnrollmentSchoolValidator.optional(),
  enrollment_count: SchoolEnrollmentEnrollment_countValidator.optional(),
  school_name: SchoolEnrollmentSchool_nameValidator.optional(),
  school_code: SchoolEnrollmentSchool_codeValidator.optional()
})
export const AdminSchoolEnrollmentListQueryValidator = Joi.object().keys({
  _id: SchoolEnrollment_idValidator.optional(),
  source_region: SchoolEnrollmentSource_regionValidator.optional(),
  school_location: SchoolEnrollmentSchool_locationValidator.optional(),
  year: SchoolEnrollmentYearValidator.optional(),
  category: SchoolEnrollmentCategoryValidator.optional(),
  batch: SchoolEnrollmentBatchValidator.optional(),
  subject_type: SchoolEnrollmentSubject_typeValidator.optional(),
  major: SchoolEnrollmentMajorValidator.optional(),
  average_score: SchoolEnrollmentAverage_scoreValidator.optional(),
  min_score: SchoolEnrollmentMin_scoreValidator.optional(),
  max_score: SchoolEnrollmentMax_scoreValidator.optional(),
  min_rank: SchoolEnrollmentMin_rankValidator.optional(),
  school: SchoolEnrollmentSchoolValidator.optional(),
  enrollment_count: SchoolEnrollmentEnrollment_countValidator.optional(),
  school_name: SchoolEnrollmentSchool_nameValidator.optional(),
  school_code: SchoolEnrollmentSchool_codeValidator.optional(),
  _etag: SchoolEnrollment_etagValidator.optional(),
  _updated: SchoolEnrollment_updatedValidator.optional(),
  _created: SchoolEnrollment_createdValidator.optional()
})

export class SchoolEnrollmentLookupFields {
  _id?: string
  average_score?: number
  batch?: string
  category?: string
  enrollment_count?: number
  major?: string
  max_score?: number
  min_rank?: number
  min_score?: number
  school?: number
  school_code?: string
  school_location?: string
  school_name?: string
  source_region?: string
  subject_type?: string
  year?: number
}

export class SchoolEnrollmentAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  average_score?: number
  batch?: string
  category?: string
  enrollment_count?: number
  major?: string
  max_score?: number
  min_rank?: number
  min_score?: number
  school?: number
  school_code?: string
  school_location?: string
  school_name?: string
  source_region?: string
  subject_type?: string
  year?: number
}

export class AdminCreateSchoolEnrollment {
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: SchoolEnrollment_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({
    description: '平均分',
    required: false,
    validator: SchoolEnrollmentAverage_scoreValidatorOptional
  })
  average_score?: number
  @CloverApiProperty({ description: '批次', validator: SchoolEnrollmentBatchValidator })
  batch: string
  @CloverApiProperty({ description: '分类', validator: SchoolEnrollmentCategoryValidator })
  category: string
  @CloverApiProperty({
    description: '录取人数',
    required: false,
    validator: SchoolEnrollmentEnrollment_countValidatorOptional
  })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业', validator: SchoolEnrollmentMajorValidator })
  major: string
  @CloverApiProperty({ description: '最高分', required: false, validator: SchoolEnrollmentMax_scoreValidatorOptional })
  max_score?: number
  @CloverApiProperty({
    description: '录取最低位次',
    required: false,
    validator: SchoolEnrollmentMin_rankValidatorOptional
  })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false, validator: SchoolEnrollmentMin_scoreValidatorOptional })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false, validator: SchoolEnrollmentSchoolValidatorOptional })
  school?: number
  @CloverApiProperty({
    description: '学校标识码',
    required: false,
    validator: SchoolEnrollmentSchool_codeValidatorOptional
  })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地', validator: SchoolEnrollmentSchool_locationValidator })
  school_location: string
  @CloverApiProperty({
    description: '学校名称',
    required: false,
    validator: SchoolEnrollmentSchool_nameValidatorOptional
  })
  school_name?: string
  @CloverApiProperty({ description: '生源地', validator: SchoolEnrollmentSource_regionValidator })
  source_region: string
  @CloverApiProperty({ description: '文理分科', validator: SchoolEnrollmentSubject_typeValidator })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false, validator: SchoolEnrollmentYearValidatorOptional })
  year?: number
}

export class AdminUpdateSchoolEnrollment {
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: SchoolEnrollment_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({
    description: '平均分',
    required: false,
    validator: SchoolEnrollmentAverage_scoreValidatorOptional
  })
  average_score?: number
  @CloverApiProperty({ description: '批次', required: false, validator: SchoolEnrollmentBatchValidatorOptional })
  batch?: string
  @CloverApiProperty({ description: '分类', required: false, validator: SchoolEnrollmentCategoryValidatorOptional })
  category?: string
  @CloverApiProperty({
    description: '录取人数',
    required: false,
    validator: SchoolEnrollmentEnrollment_countValidatorOptional
  })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业', required: false, validator: SchoolEnrollmentMajorValidatorOptional })
  major?: string
  @CloverApiProperty({ description: '最高分', required: false, validator: SchoolEnrollmentMax_scoreValidatorOptional })
  max_score?: number
  @CloverApiProperty({
    description: '录取最低位次',
    required: false,
    validator: SchoolEnrollmentMin_rankValidatorOptional
  })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false, validator: SchoolEnrollmentMin_scoreValidatorOptional })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false, validator: SchoolEnrollmentSchoolValidatorOptional })
  school?: number
  @CloverApiProperty({
    description: '学校标识码',
    required: false,
    validator: SchoolEnrollmentSchool_codeValidatorOptional
  })
  school_code?: string
  @CloverApiProperty({
    description: '学校所在地',
    required: false,
    validator: SchoolEnrollmentSchool_locationValidatorOptional
  })
  school_location?: string
  @CloverApiProperty({
    description: '学校名称',
    required: false,
    validator: SchoolEnrollmentSchool_nameValidatorOptional
  })
  school_name?: string
  @CloverApiProperty({
    description: '生源地',
    required: false,
    validator: SchoolEnrollmentSource_regionValidatorOptional
  })
  source_region?: string
  @CloverApiProperty({
    description: '文理分科',
    required: false,
    validator: SchoolEnrollmentSubject_typeValidatorOptional
  })
  subject_type?: string
  @CloverApiProperty({ description: '年份', required: false, validator: SchoolEnrollmentYearValidatorOptional })
  year?: number
}

export class AdminListSchoolEnrollmentItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '平均分', required: false })
  average_score?: number
  @CloverApiProperty({ description: '批次' })
  batch: string
  @CloverApiProperty({ description: '分类' })
  category: string
  @CloverApiProperty({ description: '录取人数', required: false })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业' })
  major: string
  @CloverApiProperty({ description: '最高分', required: false })
  max_score?: number
  @CloverApiProperty({ description: '录取最低位次', required: false })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false })
  school?: number
  @CloverApiProperty({ description: '学校标识码', required: false })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地' })
  school_location: string
  @CloverApiProperty({ description: '学校名称', required: false })
  school_name?: string
  @CloverApiProperty({ description: '生源地' })
  source_region: string
  @CloverApiProperty({ description: '文理分科' })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false })
  year?: number
}

export class AdminGetSchoolEnrollmentResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '平均分', required: false })
  average_score?: number
  @CloverApiProperty({ description: '批次' })
  batch: string
  @CloverApiProperty({ description: '分类' })
  category: string
  @CloverApiProperty({ description: '录取人数', required: false })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业' })
  major: string
  @CloverApiProperty({ description: '最高分', required: false })
  max_score?: number
  @CloverApiProperty({ description: '录取最低位次', required: false })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false })
  school?: number
  @CloverApiProperty({ description: '学校标识码', required: false })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地' })
  school_location: string
  @CloverApiProperty({ description: '学校名称', required: false })
  school_name?: string
  @CloverApiProperty({ description: '生源地' })
  source_region: string
  @CloverApiProperty({ description: '文理分科' })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false })
  year?: number
}

export class ReplaceSchoolEnrollment {
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({
    description: '平均分',
    required: false,
    validator: SchoolEnrollmentAverage_scoreValidatorOptional
  })
  average_score?: number
  @CloverApiProperty({ description: '批次', validator: SchoolEnrollmentBatchValidator })
  batch: string
  @CloverApiProperty({ description: '分类', validator: SchoolEnrollmentCategoryValidator })
  category: string
  @CloverApiProperty({
    description: '录取人数',
    required: false,
    validator: SchoolEnrollmentEnrollment_countValidatorOptional
  })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业', validator: SchoolEnrollmentMajorValidator })
  major: string
  @CloverApiProperty({ description: '最高分', required: false, validator: SchoolEnrollmentMax_scoreValidatorOptional })
  max_score?: number
  @CloverApiProperty({
    description: '录取最低位次',
    required: false,
    validator: SchoolEnrollmentMin_rankValidatorOptional
  })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false, validator: SchoolEnrollmentMin_scoreValidatorOptional })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false, validator: SchoolEnrollmentSchoolValidatorOptional })
  school?: number
  @CloverApiProperty({
    description: '学校标识码',
    required: false,
    validator: SchoolEnrollmentSchool_codeValidatorOptional
  })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地', validator: SchoolEnrollmentSchool_locationValidator })
  school_location: string
  @CloverApiProperty({
    description: '学校名称',
    required: false,
    validator: SchoolEnrollmentSchool_nameValidatorOptional
  })
  school_name?: string
  @CloverApiProperty({ description: '生源地', validator: SchoolEnrollmentSource_regionValidator })
  source_region: string
  @CloverApiProperty({ description: '文理分科', validator: SchoolEnrollmentSubject_typeValidator })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false, validator: SchoolEnrollmentYearValidatorOptional })
  year?: number
}

export class CreateSchoolEnrollment {
  @CloverApiProperty({ required: false, validator: SchoolEnrollment_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({
    description: '平均分',
    required: false,
    validator: SchoolEnrollmentAverage_scoreValidatorOptional
  })
  average_score?: number
  @CloverApiProperty({ description: '批次', validator: SchoolEnrollmentBatchValidator })
  batch: string
  @CloverApiProperty({ description: '分类', validator: SchoolEnrollmentCategoryValidator })
  category: string
  @CloverApiProperty({
    description: '录取人数',
    required: false,
    validator: SchoolEnrollmentEnrollment_countValidatorOptional
  })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业', validator: SchoolEnrollmentMajorValidator })
  major: string
  @CloverApiProperty({ description: '最高分', required: false, validator: SchoolEnrollmentMax_scoreValidatorOptional })
  max_score?: number
  @CloverApiProperty({
    description: '录取最低位次',
    required: false,
    validator: SchoolEnrollmentMin_rankValidatorOptional
  })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false, validator: SchoolEnrollmentMin_scoreValidatorOptional })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false, validator: SchoolEnrollmentSchoolValidatorOptional })
  school?: number
  @CloverApiProperty({
    description: '学校标识码',
    required: false,
    validator: SchoolEnrollmentSchool_codeValidatorOptional
  })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地', validator: SchoolEnrollmentSchool_locationValidator })
  school_location: string
  @CloverApiProperty({
    description: '学校名称',
    required: false,
    validator: SchoolEnrollmentSchool_nameValidatorOptional
  })
  school_name?: string
  @CloverApiProperty({ description: '生源地', validator: SchoolEnrollmentSource_regionValidator })
  source_region: string
  @CloverApiProperty({ description: '文理分科', validator: SchoolEnrollmentSubject_typeValidator })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false, validator: SchoolEnrollmentYearValidatorOptional })
  year?: number
}

export class ListSchoolEnrollmentItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '平均分', required: false })
  average_score?: number
  @CloverApiProperty({ description: '批次' })
  batch: string
  @CloverApiProperty({ description: '分类' })
  category: string
  @CloverApiProperty({ description: '录取人数', required: false })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业' })
  major: string
  @CloverApiProperty({ description: '最高分', required: false })
  max_score?: number
  @CloverApiProperty({ description: '录取最低位次', required: false })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false })
  school?: number
  @CloverApiProperty({ description: '学校标识码', required: false })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地' })
  school_location: string
  @CloverApiProperty({ description: '学校名称', required: false })
  school_name?: string
  @CloverApiProperty({ description: '生源地' })
  source_region: string
  @CloverApiProperty({ description: '文理分科' })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false })
  year?: number
}

export class GetSchoolEnrollmentResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '平均分', required: false })
  average_score?: number
  @CloverApiProperty({ description: '批次' })
  batch: string
  @CloverApiProperty({ description: '分类' })
  category: string
  @CloverApiProperty({ description: '录取人数', required: false })
  enrollment_count?: number
  @CloverApiProperty({ description: '专业' })
  major: string
  @CloverApiProperty({ description: '最高分', required: false })
  max_score?: number
  @CloverApiProperty({ description: '录取最低位次', required: false })
  min_rank?: number
  @CloverApiProperty({ description: '最低分', required: false })
  min_score?: number
  @CloverApiProperty({ description: '学校', required: false })
  school?: number
  @CloverApiProperty({ description: '学校标识码', required: false })
  school_code?: string
  @CloverApiProperty({ description: '学校所在地' })
  school_location: string
  @CloverApiProperty({ description: '学校名称', required: false })
  school_name?: string
  @CloverApiProperty({ description: '生源地' })
  source_region: string
  @CloverApiProperty({ description: '文理分科' })
  subject_type: string
  @CloverApiProperty({ description: '年份', required: false })
  year?: number
}

export interface SchoolEnrollmentCombinedId {
  _id?: string
}

export class ListSchoolEnrollmentResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListSchoolEnrollmentItem] })
  _items: ListSchoolEnrollmentItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListSchoolEnrollmentResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListSchoolEnrollmentItem] })
  _items: AdminListSchoolEnrollmentItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertSchoolEnrollment {}

export class UpdateSchoolEnrollment {}

export class RemoveSchoolEnrollment {}

export class SchoolEnrollmentCombinedId {}

export interface SchoolEnrollmentDtoType {
  item: GetSchoolEnrollmentResult
  create: CreateSchoolEnrollment
  replace: ReplaceSchoolEnrollment
  update: UpdateSchoolEnrollment
}
