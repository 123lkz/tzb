import { ObjectIdString, Joi, ListResultPageInfo, ArraySchemaProperty, CloverApiProperty, ObjectSchemaProperty } from '@havenzhang/clover'
import endpoint from '../../../endpoints/Position'
export const Position_idValidator = Joi.objectId()
export const Position_idValidatorOptional = Joi.objectId().optional()
export const PositionJobNameValidator = endpoint['schema']['jobName'].validator
export const PositionJobNameValidatorOptional = endpoint['schema']['jobName'].validator.optional()
export const PositionBossCertValidator = endpoint['schema']['bossCert'].validator
export const PositionBossCertValidatorOptional = endpoint['schema']['bossCert'].validator.optional()
export const PositionBrandNameValidator = endpoint['schema']['brandName'].validator
export const PositionBrandNameValidatorOptional = endpoint['schema']['brandName'].validator.optional()
export const PositionJobDegreeValidator = endpoint['schema']['jobDegree'].validator
export const PositionJobDegreeValidatorOptional = endpoint['schema']['jobDegree'].validator.optional()
export const PositionJobExperienceValidator = endpoint['schema']['jobExperience'].validator
export const PositionJobExperienceValidatorOptional = endpoint['schema']['jobExperience'].validator.optional()
export const PositionSalaryDescValidator = endpoint['schema']['salaryDesc'].validator
export const PositionSalaryDescValidatorOptional = endpoint['schema']['salaryDesc'].validator.optional()
export const PositionCityNameValidator = endpoint['schema']['cityName'].validator
export const PositionCityNameValidatorOptional = endpoint['schema']['cityName'].validator.optional()
export const PositionSkillsValidator = endpoint['schema']['skills'].validator
export const PositionSkillsValidatorOptional = endpoint['schema']['skills'].validator.optional()
export const PositionBrandIndustryValidator = endpoint['schema']['brandIndustry'].validator
export const PositionBrandIndustryValidatorOptional = endpoint['schema']['brandIndustry'].validator.optional()
export const PositionBrandScaleNameValidator = endpoint['schema']['brandScaleName'].validator
export const PositionBrandScaleNameValidatorOptional = endpoint['schema']['brandScaleName'].validator.optional()
export const PositionBusinessDistrictValidator = endpoint['schema']['businessDistrict'].validator
export const PositionBusinessDistrictValidatorOptional = endpoint['schema']['businessDistrict'].validator.optional()
export const PositionCreate_timeValidator = Joi.date()
export const PositionCreate_timeValidatorOptional = Joi.date().optional()
export const Position_etagValidator = endpoint['schema']['_etag'].validator
export const Position_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const Position_updatedValidator = endpoint['schema']['_updated'].validator
export const Position_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const Position_createdValidator = endpoint['schema']['_created'].validator
export const Position_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const PositionListQueryValidator = Joi.object().keys({
  _id: Position_idValidator.optional(),
  jobName: PositionJobNameValidator.optional(),
  bossCert: PositionBossCertValidator.optional(),
  brandName: PositionBrandNameValidator.optional(),
  jobDegree: PositionJobDegreeValidator.optional(),
  jobExperience: PositionJobExperienceValidator.optional(),
  salaryDesc: PositionSalaryDescValidator.optional(),
  cityName: PositionCityNameValidator.optional(),
  skills: PositionSkillsValidator.optional(),
  brandIndustry: PositionBrandIndustryValidator.optional(),
  brandScaleName: PositionBrandScaleNameValidator.optional(),
  businessDistrict: PositionBusinessDistrictValidator.optional(),
  create_time: PositionCreate_timeValidator.optional()
})
export const AdminPositionListQueryValidator = Joi.object().keys({
  _id: Position_idValidator.optional(),
  jobName: PositionJobNameValidator.optional(),
  bossCert: PositionBossCertValidator.optional(),
  brandName: PositionBrandNameValidator.optional(),
  jobDegree: PositionJobDegreeValidator.optional(),
  jobExperience: PositionJobExperienceValidator.optional(),
  salaryDesc: PositionSalaryDescValidator.optional(),
  cityName: PositionCityNameValidator.optional(),
  skills: PositionSkillsValidator.optional(),
  brandIndustry: PositionBrandIndustryValidator.optional(),
  brandScaleName: PositionBrandScaleNameValidator.optional(),
  businessDistrict: PositionBusinessDistrictValidator.optional(),
  create_time: PositionCreate_timeValidator.optional(),
  _etag: Position_etagValidator.optional(),
  _updated: Position_updatedValidator.optional(),
  _created: Position_createdValidator.optional()
})

export class PositionLookupFields {
  _id?: string
  bossCert?: number
  brandIndustry?: string
  brandName?: string
  brandScaleName?: string
  businessDistrict?: string
  cityName?: string
  create_time?: Date
  jobDegree?: string
  jobExperience?: string
  jobName?: string
  salaryDesc?: string
  skills?: string
}

export class PositionAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  bossCert?: number
  brandIndustry?: string
  brandName?: string
  brandScaleName?: string
  businessDistrict?: string
  cityName?: string
  create_time?: Date
  jobDegree?: string
  jobExperience?: string
  jobName?: string
  salaryDesc?: string
  skills?: string
}

export class AdminCreatePosition {
  @CloverApiProperty({ required: false, validator: Position_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Position_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: Position_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: Position_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '招聘人数', validator: PositionBossCertValidator })
  bossCert: number
  @CloverApiProperty({ description: '公司行业', validator: PositionBrandIndustryValidator })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称', validator: PositionBrandNameValidator })
  brandName: string
  @CloverApiProperty({ description: '公司规模', validator: PositionBrandScaleNameValidator })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质', validator: PositionBusinessDistrictValidator })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点', validator: PositionCityNameValidator })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: PositionCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求', validator: PositionJobDegreeValidator })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验', validator: PositionJobExperienceValidator })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称', validator: PositionJobNameValidator })
  jobName: string
  @CloverApiProperty({ description: '薪资', validator: PositionSalaryDescValidator })
  salaryDesc: string
  @CloverApiProperty({ description: '标签', validator: PositionSkillsValidator })
  skills: string
}

export class AdminUpdatePosition {
  @CloverApiProperty({ required: false, validator: Position_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Position_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: Position_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: Position_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '招聘人数', required: false, validator: PositionBossCertValidatorOptional })
  bossCert?: number
  @CloverApiProperty({ description: '公司行业', required: false, validator: PositionBrandIndustryValidatorOptional })
  brandIndustry?: string
  @CloverApiProperty({ description: '公司名称', required: false, validator: PositionBrandNameValidatorOptional })
  brandName?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: PositionBrandScaleNameValidatorOptional })
  brandScaleName?: string
  @CloverApiProperty({ description: '公司性质', required: false, validator: PositionBusinessDistrictValidatorOptional })
  businessDistrict?: string
  @CloverApiProperty({ description: '工作地点', required: false, validator: PositionCityNameValidatorOptional })
  cityName?: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: PositionCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求', required: false, validator: PositionJobDegreeValidatorOptional })
  jobDegree?: string
  @CloverApiProperty({ description: '工作经验', required: false, validator: PositionJobExperienceValidatorOptional })
  jobExperience?: string
  @CloverApiProperty({ description: '职位名称', required: false, validator: PositionJobNameValidatorOptional })
  jobName?: string
  @CloverApiProperty({ description: '薪资', required: false, validator: PositionSalaryDescValidatorOptional })
  salaryDesc?: string
  @CloverApiProperty({ description: '标签', required: false, validator: PositionSkillsValidatorOptional })
  skills?: string
}

export class AdminListPositionItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '招聘人数' })
  bossCert: number
  @CloverApiProperty({ description: '公司行业' })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称' })
  brandName: string
  @CloverApiProperty({ description: '公司规模' })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质' })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点' })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求' })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验' })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称' })
  jobName: string
  @CloverApiProperty({ description: '薪资' })
  salaryDesc: string
  @CloverApiProperty({ description: '标签' })
  skills: string
}

export class AdminGetPositionResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '招聘人数' })
  bossCert: number
  @CloverApiProperty({ description: '公司行业' })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称' })
  brandName: string
  @CloverApiProperty({ description: '公司规模' })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质' })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点' })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求' })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验' })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称' })
  jobName: string
  @CloverApiProperty({ description: '薪资' })
  salaryDesc: string
  @CloverApiProperty({ description: '标签' })
  skills: string
}

export class ReplacePosition {
  @CloverApiProperty({ required: false, validator: Position_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '招聘人数', validator: PositionBossCertValidator })
  bossCert: number
  @CloverApiProperty({ description: '公司行业', validator: PositionBrandIndustryValidator })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称', validator: PositionBrandNameValidator })
  brandName: string
  @CloverApiProperty({ description: '公司规模', validator: PositionBrandScaleNameValidator })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质', validator: PositionBusinessDistrictValidator })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点', validator: PositionCityNameValidator })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: PositionCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求', validator: PositionJobDegreeValidator })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验', validator: PositionJobExperienceValidator })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称', validator: PositionJobNameValidator })
  jobName: string
  @CloverApiProperty({ description: '薪资', validator: PositionSalaryDescValidator })
  salaryDesc: string
  @CloverApiProperty({ description: '标签', validator: PositionSkillsValidator })
  skills: string
}

export class CreatePosition {
  @CloverApiProperty({ required: false, validator: Position_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '招聘人数', validator: PositionBossCertValidator })
  bossCert: number
  @CloverApiProperty({ description: '公司行业', validator: PositionBrandIndustryValidator })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称', validator: PositionBrandNameValidator })
  brandName: string
  @CloverApiProperty({ description: '公司规模', validator: PositionBrandScaleNameValidator })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质', validator: PositionBusinessDistrictValidator })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点', validator: PositionCityNameValidator })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: PositionCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求', validator: PositionJobDegreeValidator })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验', validator: PositionJobExperienceValidator })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称', validator: PositionJobNameValidator })
  jobName: string
  @CloverApiProperty({ description: '薪资', validator: PositionSalaryDescValidator })
  salaryDesc: string
  @CloverApiProperty({ description: '标签', validator: PositionSkillsValidator })
  skills: string
}

export class ListPositionItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '招聘人数' })
  bossCert: number
  @CloverApiProperty({ description: '公司行业' })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称' })
  brandName: string
  @CloverApiProperty({ description: '公司规模' })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质' })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点' })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求' })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验' })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称' })
  jobName: string
  @CloverApiProperty({ description: '薪资' })
  salaryDesc: string
  @CloverApiProperty({ description: '标签' })
  skills: string
}

export class GetPositionResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '招聘人数' })
  bossCert: number
  @CloverApiProperty({ description: '公司行业' })
  brandIndustry: string
  @CloverApiProperty({ description: '公司名称' })
  brandName: string
  @CloverApiProperty({ description: '公司规模' })
  brandScaleName: string
  @CloverApiProperty({ description: '公司性质' })
  businessDistrict: string
  @CloverApiProperty({ description: '工作地点' })
  cityName: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '学历要求' })
  jobDegree: string
  @CloverApiProperty({ description: '工作经验' })
  jobExperience: string
  @CloverApiProperty({ description: '职位名称' })
  jobName: string
  @CloverApiProperty({ description: '薪资' })
  salaryDesc: string
  @CloverApiProperty({ description: '标签' })
  skills: string
}

export interface PositionCombinedId {
  _id?: string
}

export class ListPositionResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListPositionItem] })
  _items: ListPositionItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListPositionResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListPositionItem] })
  _items: AdminListPositionItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertPosition {
}

export class UpdatePosition {
}

export class RemovePosition {
}

export class PositionCombinedId {
}

export interface PositionDtoType {
  item: GetPositionResult
  create: CreatePosition
  replace: ReplacePosition
  update: UpdatePosition
}
