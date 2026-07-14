import { ObjectIdString, Joi, ListResultPageInfo, ArraySchemaProperty, CloverApiProperty, ObjectSchemaProperty } from '@havenzhang/clover'
import endpoint from '../../../endpoints/JobOccupationMapping'
export const JobOccupationMapping_idValidator = Joi.objectId()
export const JobOccupationMapping_idValidatorOptional = Joi.objectId().optional()
export const JobOccupationMappingPosition_nameValidator = endpoint['schema']['position_name'].validator
export const JobOccupationMappingPosition_nameValidatorOptional = endpoint['schema']['position_name'].validator.optional()
export const JobOccupationMappingSourceNameValidator = endpoint['schema']['source']['schema']['name'].validator
export const JobOccupationMappingSourceNameValidatorOptional = endpoint['schema']['source']['schema']['name'].validator.optional()
export const JobOccupationMappingSourceOriginal_hierarchyLevel_1Validator = endpoint['schema']['source']['schema']['original_hierarchy']['schema']['level_1'].validator
export const JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional = endpoint['schema']['source']['schema']['original_hierarchy']['schema']['level_1'].validator.optional()
export const JobOccupationMappingSourceOriginal_hierarchyLevel_2Validator = endpoint['schema']['source']['schema']['original_hierarchy']['schema']['level_2'].validator
export const JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional = endpoint['schema']['source']['schema']['original_hierarchy']['schema']['level_2'].validator.optional()
export const JobOccupationMappingSourceOriginal_hierarchyValidator = Joi.object().keys({
  level_1: JobOccupationMappingSourceOriginal_hierarchyLevel_1Validator,
  level_2: JobOccupationMappingSourceOriginal_hierarchyLevel_2Validator
})
export const JobOccupationMappingSourceOriginal_hierarchyValidatorOptional = Joi.object().keys({
  level_1: JobOccupationMappingSourceOriginal_hierarchyLevel_1Validator,
  level_2: JobOccupationMappingSourceOriginal_hierarchyLevel_2Validator
}).optional()
export const JobOccupationMappingSourceValidator = Joi.object().keys({
  name: JobOccupationMappingSourceNameValidator,
  original_hierarchy: JobOccupationMappingSourceOriginal_hierarchyValidator
})
export const JobOccupationMappingSourceValidatorOptional = Joi.object().keys({
  name: JobOccupationMappingSourceNameValidator,
  original_hierarchy: JobOccupationMappingSourceOriginal_hierarchyValidator
}).optional()
export const JobOccupationMappingStandard_classificationXileiPrimaryNameValidator = endpoint['schema']['standard_classification']['schema']['xilei']['schema']['primary']['schema']['name'].validator
export const JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional = endpoint['schema']['standard_classification']['schema']['xilei']['schema']['primary']['schema']['name'].validator.optional()
export const JobOccupationMappingStandard_classificationXileiPrimaryCodeValidator = endpoint['schema']['standard_classification']['schema']['xilei']['schema']['primary']['schema']['code'].validator
export const JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional = endpoint['schema']['standard_classification']['schema']['xilei']['schema']['primary']['schema']['code'].validator.optional()
export const JobOccupationMappingStandard_classificationXileiPrimaryValidator = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationXileiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidator
})
export const JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationXileiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidator
}).optional()
export const JobOccupationMappingStandard_classificationXileiValidator = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationXileiPrimaryValidator
})
export const JobOccupationMappingStandard_classificationXileiValidatorOptional = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationXileiPrimaryValidator
}).optional()
export const JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidator = endpoint['schema']['standard_classification']['schema']['xiaoli']['schema']['primary']['schema']['name'].validator
export const JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional = endpoint['schema']['standard_classification']['schema']['xiaoli']['schema']['primary']['schema']['name'].validator.optional()
export const JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidator = endpoint['schema']['standard_classification']['schema']['xiaoli']['schema']['primary']['schema']['code'].validator
export const JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional = endpoint['schema']['standard_classification']['schema']['xiaoli']['schema']['primary']['schema']['code'].validator.optional()
export const JobOccupationMappingStandard_classificationXiaoliPrimaryValidator = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidator
})
export const JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidator
}).optional()
export const JobOccupationMappingStandard_classificationXiaoliValidator = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationXiaoliPrimaryValidator
})
export const JobOccupationMappingStandard_classificationXiaoliValidatorOptional = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationXiaoliPrimaryValidator
}).optional()
export const JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidator = endpoint['schema']['standard_classification']['schema']['zhonglei']['schema']['primary']['schema']['name'].validator
export const JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional = endpoint['schema']['standard_classification']['schema']['zhonglei']['schema']['primary']['schema']['name'].validator.optional()
export const JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidator = endpoint['schema']['standard_classification']['schema']['zhonglei']['schema']['primary']['schema']['code'].validator
export const JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional = endpoint['schema']['standard_classification']['schema']['zhonglei']['schema']['primary']['schema']['code'].validator.optional()
export const JobOccupationMappingStandard_classificationZhongleiPrimaryValidator = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidator
})
export const JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidator
}).optional()
export const JobOccupationMappingStandard_classificationZhongleiValidator = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationZhongleiPrimaryValidator
})
export const JobOccupationMappingStandard_classificationZhongleiValidatorOptional = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationZhongleiPrimaryValidator
}).optional()
export const JobOccupationMappingStandard_classificationDaleiPrimaryNameValidator = endpoint['schema']['standard_classification']['schema']['dalei']['schema']['primary']['schema']['name'].validator
export const JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional = endpoint['schema']['standard_classification']['schema']['dalei']['schema']['primary']['schema']['name'].validator.optional()
export const JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidator = endpoint['schema']['standard_classification']['schema']['dalei']['schema']['primary']['schema']['code'].validator
export const JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional = endpoint['schema']['standard_classification']['schema']['dalei']['schema']['primary']['schema']['code'].validator.optional()
export const JobOccupationMappingStandard_classificationDaleiPrimaryValidator = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidator
})
export const JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional = Joi.object().keys({
  name: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidator,
  code: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidator
}).optional()
export const JobOccupationMappingStandard_classificationDaleiValidator = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationDaleiPrimaryValidator
})
export const JobOccupationMappingStandard_classificationDaleiValidatorOptional = Joi.object().keys({
  primary: JobOccupationMappingStandard_classificationDaleiPrimaryValidator
}).optional()
export const JobOccupationMappingStandard_classificationValidator = Joi.object().keys({
  xilei: JobOccupationMappingStandard_classificationXileiValidator,
  xiaoli: JobOccupationMappingStandard_classificationXiaoliValidator,
  zhonglei: JobOccupationMappingStandard_classificationZhongleiValidator,
  dalei: JobOccupationMappingStandard_classificationDaleiValidator
})
export const JobOccupationMappingStandard_classificationValidatorOptional = Joi.object().keys({
  xilei: JobOccupationMappingStandard_classificationXileiValidator,
  xiaoli: JobOccupationMappingStandard_classificationXiaoliValidator,
  zhonglei: JobOccupationMappingStandard_classificationZhongleiValidator,
  dalei: JobOccupationMappingStandard_classificationDaleiValidator
}).optional()
export const JobOccupationMappingVersionValidator = endpoint['schema']['version'].validator
export const JobOccupationMappingVersionValidatorOptional = endpoint['schema']['version'].validator.optional()
export const JobOccupationMappingStatusValidator = endpoint['schema']['status'].validator
export const JobOccupationMappingStatusValidatorOptional = endpoint['schema']['status'].validator.optional()
export const JobOccupationMapping_etagValidator = endpoint['schema']['_etag'].validator
export const JobOccupationMapping_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const JobOccupationMapping_updatedValidator = endpoint['schema']['_updated'].validator
export const JobOccupationMapping_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const JobOccupationMapping_createdValidator = endpoint['schema']['_created'].validator
export const JobOccupationMapping_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const JobOccupationMappingListQueryValidator = Joi.object().keys({
  _id: JobOccupationMapping_idValidator.optional(),
  position_name: JobOccupationMappingPosition_nameValidator.optional()
})
export const AdminJobOccupationMappingListQueryValidator = Joi.object().keys({
  _id: JobOccupationMapping_idValidator.optional(),
  position_name: JobOccupationMappingPosition_nameValidator.optional(),
  source: JobOccupationMappingSourceValidator.optional(),
  standard_classification: JobOccupationMappingStandard_classificationValidator.optional(),
  version: JobOccupationMappingVersionValidator.optional(),
  status: JobOccupationMappingStatusValidator.optional(),
  _etag: JobOccupationMapping_etagValidator.optional(),
  _updated: JobOccupationMapping_updatedValidator.optional(),
  _created: JobOccupationMapping_createdValidator.optional()
})

export class JobOccupationMappingStandard_classificationZhongleiPrimaryAdminLookupFields {
  code?: string
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationZhongleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminUpdateJobOccupationMappingStandard_classificationZhongleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminListJobOccupationMappingStandard_classificationZhongleiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminGetJobOccupationMappingStandard_classificationZhongleiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class ReplaceJobOccupationMappingStandard_classificationZhongleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional })
  name?: string
}

export class CreateJobOccupationMappingStandard_classificationZhongleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional })
  name?: string
}

export class UpdateJobOccupationMappingStandard_classificationZhongleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryNameValidatorOptional })
  name?: string
}

export class ListJobOccupationMappingStandard_classificationZhongleiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class GetJobOccupationMappingStandard_classificationZhongleiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationZhonglei {
  @CloverApiProperty({ description: '主匹配', type: AdminCreateJobOccupationMappingStandard_classificationZhongleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional })
  primary?: AdminCreateJobOccupationMappingStandard_classificationZhongleiPrimary
}

export class AdminUpdateJobOccupationMappingStandard_classificationZhonglei {
  @CloverApiProperty({ description: '主匹配', type: AdminUpdateJobOccupationMappingStandard_classificationZhongleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional })
  primary?: AdminUpdateJobOccupationMappingStandard_classificationZhongleiPrimary
}

export class AdminListJobOccupationMappingStandard_classificationZhongleiItem {
  @CloverApiProperty({ description: '主匹配', type: AdminListJobOccupationMappingStandard_classificationZhongleiPrimaryItem, required: false })
  primary?: AdminListJobOccupationMappingStandard_classificationZhongleiPrimaryItem
}

export class AdminGetJobOccupationMappingStandard_classificationZhongleiResult {
  @CloverApiProperty({ description: '主匹配', type: AdminGetJobOccupationMappingStandard_classificationZhongleiPrimaryResult, required: false })
  primary?: AdminGetJobOccupationMappingStandard_classificationZhongleiPrimaryResult
}

export class ReplaceJobOccupationMappingStandard_classificationZhonglei {
  @CloverApiProperty({ description: '主匹配', type: ReplaceJobOccupationMappingStandard_classificationZhongleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional })
  primary?: ReplaceJobOccupationMappingStandard_classificationZhongleiPrimary
}

export class CreateJobOccupationMappingStandard_classificationZhonglei {
  @CloverApiProperty({ description: '主匹配', type: CreateJobOccupationMappingStandard_classificationZhongleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional })
  primary?: CreateJobOccupationMappingStandard_classificationZhongleiPrimary
}

export class UpdateJobOccupationMappingStandard_classificationZhonglei {
  @CloverApiProperty({ description: '主匹配', type: UpdateJobOccupationMappingStandard_classificationZhongleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationZhongleiPrimaryValidatorOptional })
  primary?: UpdateJobOccupationMappingStandard_classificationZhongleiPrimary
}

export class ListJobOccupationMappingStandard_classificationZhongleiItem {
  @CloverApiProperty({ description: '主匹配', type: ListJobOccupationMappingStandard_classificationZhongleiPrimaryItem, required: false })
  primary?: ListJobOccupationMappingStandard_classificationZhongleiPrimaryItem
}

export class GetJobOccupationMappingStandard_classificationZhongleiResult {
  @CloverApiProperty({ description: '主匹配', type: GetJobOccupationMappingStandard_classificationZhongleiPrimaryResult, required: false })
  primary?: GetJobOccupationMappingStandard_classificationZhongleiPrimaryResult
}

export class JobOccupationMappingStandard_classificationXileiPrimaryAdminLookupFields {
  code?: string
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationXileiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminUpdateJobOccupationMappingStandard_classificationXileiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminListJobOccupationMappingStandard_classificationXileiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminGetJobOccupationMappingStandard_classificationXileiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class ReplaceJobOccupationMappingStandard_classificationXileiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional })
  name?: string
}

export class CreateJobOccupationMappingStandard_classificationXileiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional })
  name?: string
}

export class UpdateJobOccupationMappingStandard_classificationXileiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryNameValidatorOptional })
  name?: string
}

export class ListJobOccupationMappingStandard_classificationXileiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class GetJobOccupationMappingStandard_classificationXileiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationXilei {
  @CloverApiProperty({ description: '主匹配', type: AdminCreateJobOccupationMappingStandard_classificationXileiPrimary, required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional })
  primary?: AdminCreateJobOccupationMappingStandard_classificationXileiPrimary
}

export class AdminUpdateJobOccupationMappingStandard_classificationXilei {
  @CloverApiProperty({ description: '主匹配', type: AdminUpdateJobOccupationMappingStandard_classificationXileiPrimary, required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional })
  primary?: AdminUpdateJobOccupationMappingStandard_classificationXileiPrimary
}

export class AdminListJobOccupationMappingStandard_classificationXileiItem {
  @CloverApiProperty({ description: '主匹配', type: AdminListJobOccupationMappingStandard_classificationXileiPrimaryItem, required: false })
  primary?: AdminListJobOccupationMappingStandard_classificationXileiPrimaryItem
}

export class AdminGetJobOccupationMappingStandard_classificationXileiResult {
  @CloverApiProperty({ description: '主匹配', type: AdminGetJobOccupationMappingStandard_classificationXileiPrimaryResult, required: false })
  primary?: AdminGetJobOccupationMappingStandard_classificationXileiPrimaryResult
}

export class ReplaceJobOccupationMappingStandard_classificationXilei {
  @CloverApiProperty({ description: '主匹配', type: ReplaceJobOccupationMappingStandard_classificationXileiPrimary, required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional })
  primary?: ReplaceJobOccupationMappingStandard_classificationXileiPrimary
}

export class CreateJobOccupationMappingStandard_classificationXilei {
  @CloverApiProperty({ description: '主匹配', type: CreateJobOccupationMappingStandard_classificationXileiPrimary, required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional })
  primary?: CreateJobOccupationMappingStandard_classificationXileiPrimary
}

export class UpdateJobOccupationMappingStandard_classificationXilei {
  @CloverApiProperty({ description: '主匹配', type: UpdateJobOccupationMappingStandard_classificationXileiPrimary, required: false, validator: JobOccupationMappingStandard_classificationXileiPrimaryValidatorOptional })
  primary?: UpdateJobOccupationMappingStandard_classificationXileiPrimary
}

export class ListJobOccupationMappingStandard_classificationXileiItem {
  @CloverApiProperty({ description: '主匹配', type: ListJobOccupationMappingStandard_classificationXileiPrimaryItem, required: false })
  primary?: ListJobOccupationMappingStandard_classificationXileiPrimaryItem
}

export class GetJobOccupationMappingStandard_classificationXileiResult {
  @CloverApiProperty({ description: '主匹配', type: GetJobOccupationMappingStandard_classificationXileiPrimaryResult, required: false })
  primary?: GetJobOccupationMappingStandard_classificationXileiPrimaryResult
}

export class JobOccupationMappingStandard_classificationXiaoliPrimaryAdminLookupFields {
  code?: string
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationXiaoliPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional })
  name?: string
}

export class AdminUpdateJobOccupationMappingStandard_classificationXiaoliPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional })
  name?: string
}

export class AdminListJobOccupationMappingStandard_classificationXiaoliPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminGetJobOccupationMappingStandard_classificationXiaoliPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class ReplaceJobOccupationMappingStandard_classificationXiaoliPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional })
  name?: string
}

export class CreateJobOccupationMappingStandard_classificationXiaoliPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional })
  name?: string
}

export class UpdateJobOccupationMappingStandard_classificationXiaoliPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryNameValidatorOptional })
  name?: string
}

export class ListJobOccupationMappingStandard_classificationXiaoliPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class GetJobOccupationMappingStandard_classificationXiaoliPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationXiaoli {
  @CloverApiProperty({ description: '主匹配', type: AdminCreateJobOccupationMappingStandard_classificationXiaoliPrimary, required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional })
  primary?: AdminCreateJobOccupationMappingStandard_classificationXiaoliPrimary
}

export class AdminUpdateJobOccupationMappingStandard_classificationXiaoli {
  @CloverApiProperty({ description: '主匹配', type: AdminUpdateJobOccupationMappingStandard_classificationXiaoliPrimary, required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional })
  primary?: AdminUpdateJobOccupationMappingStandard_classificationXiaoliPrimary
}

export class AdminListJobOccupationMappingStandard_classificationXiaoliItem {
  @CloverApiProperty({ description: '主匹配', type: AdminListJobOccupationMappingStandard_classificationXiaoliPrimaryItem, required: false })
  primary?: AdminListJobOccupationMappingStandard_classificationXiaoliPrimaryItem
}

export class AdminGetJobOccupationMappingStandard_classificationXiaoliResult {
  @CloverApiProperty({ description: '主匹配', type: AdminGetJobOccupationMappingStandard_classificationXiaoliPrimaryResult, required: false })
  primary?: AdminGetJobOccupationMappingStandard_classificationXiaoliPrimaryResult
}

export class ReplaceJobOccupationMappingStandard_classificationXiaoli {
  @CloverApiProperty({ description: '主匹配', type: ReplaceJobOccupationMappingStandard_classificationXiaoliPrimary, required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional })
  primary?: ReplaceJobOccupationMappingStandard_classificationXiaoliPrimary
}

export class CreateJobOccupationMappingStandard_classificationXiaoli {
  @CloverApiProperty({ description: '主匹配', type: CreateJobOccupationMappingStandard_classificationXiaoliPrimary, required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional })
  primary?: CreateJobOccupationMappingStandard_classificationXiaoliPrimary
}

export class UpdateJobOccupationMappingStandard_classificationXiaoli {
  @CloverApiProperty({ description: '主匹配', type: UpdateJobOccupationMappingStandard_classificationXiaoliPrimary, required: false, validator: JobOccupationMappingStandard_classificationXiaoliPrimaryValidatorOptional })
  primary?: UpdateJobOccupationMappingStandard_classificationXiaoliPrimary
}

export class ListJobOccupationMappingStandard_classificationXiaoliItem {
  @CloverApiProperty({ description: '主匹配', type: ListJobOccupationMappingStandard_classificationXiaoliPrimaryItem, required: false })
  primary?: ListJobOccupationMappingStandard_classificationXiaoliPrimaryItem
}

export class GetJobOccupationMappingStandard_classificationXiaoliResult {
  @CloverApiProperty({ description: '主匹配', type: GetJobOccupationMappingStandard_classificationXiaoliPrimaryResult, required: false })
  primary?: GetJobOccupationMappingStandard_classificationXiaoliPrimaryResult
}

export class JobOccupationMappingStandard_classificationDaleiPrimaryAdminLookupFields {
  code?: string
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationDaleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminUpdateJobOccupationMappingStandard_classificationDaleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional })
  name?: string
}

export class AdminListJobOccupationMappingStandard_classificationDaleiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminGetJobOccupationMappingStandard_classificationDaleiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class ReplaceJobOccupationMappingStandard_classificationDaleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional })
  name?: string
}

export class CreateJobOccupationMappingStandard_classificationDaleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional })
  name?: string
}

export class UpdateJobOccupationMappingStandard_classificationDaleiPrimary {
  @CloverApiProperty({ description: '编码', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '名称', required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryNameValidatorOptional })
  name?: string
}

export class ListJobOccupationMappingStandard_classificationDaleiPrimaryItem {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class GetJobOccupationMappingStandard_classificationDaleiPrimaryResult {
  @CloverApiProperty({ description: '编码', required: false })
  code?: string
  @CloverApiProperty({ description: '名称', required: false })
  name?: string
}

export class AdminCreateJobOccupationMappingStandard_classificationDalei {
  @CloverApiProperty({ description: '主匹配', type: AdminCreateJobOccupationMappingStandard_classificationDaleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional })
  primary?: AdminCreateJobOccupationMappingStandard_classificationDaleiPrimary
}

export class AdminUpdateJobOccupationMappingStandard_classificationDalei {
  @CloverApiProperty({ description: '主匹配', type: AdminUpdateJobOccupationMappingStandard_classificationDaleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional })
  primary?: AdminUpdateJobOccupationMappingStandard_classificationDaleiPrimary
}

export class AdminListJobOccupationMappingStandard_classificationDaleiItem {
  @CloverApiProperty({ description: '主匹配', type: AdminListJobOccupationMappingStandard_classificationDaleiPrimaryItem, required: false })
  primary?: AdminListJobOccupationMappingStandard_classificationDaleiPrimaryItem
}

export class AdminGetJobOccupationMappingStandard_classificationDaleiResult {
  @CloverApiProperty({ description: '主匹配', type: AdminGetJobOccupationMappingStandard_classificationDaleiPrimaryResult, required: false })
  primary?: AdminGetJobOccupationMappingStandard_classificationDaleiPrimaryResult
}

export class ReplaceJobOccupationMappingStandard_classificationDalei {
  @CloverApiProperty({ description: '主匹配', type: ReplaceJobOccupationMappingStandard_classificationDaleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional })
  primary?: ReplaceJobOccupationMappingStandard_classificationDaleiPrimary
}

export class CreateJobOccupationMappingStandard_classificationDalei {
  @CloverApiProperty({ description: '主匹配', type: CreateJobOccupationMappingStandard_classificationDaleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional })
  primary?: CreateJobOccupationMappingStandard_classificationDaleiPrimary
}

export class UpdateJobOccupationMappingStandard_classificationDalei {
  @CloverApiProperty({ description: '主匹配', type: UpdateJobOccupationMappingStandard_classificationDaleiPrimary, required: false, validator: JobOccupationMappingStandard_classificationDaleiPrimaryValidatorOptional })
  primary?: UpdateJobOccupationMappingStandard_classificationDaleiPrimary
}

export class UpdateJobOccupationMappingStandard_classification {
  @CloverApiProperty({ description: '大类（第一级）', type: UpdateJobOccupationMappingStandard_classificationDalei, required: false, validator: JobOccupationMappingStandard_classificationDaleiValidatorOptional })
  dalei?: UpdateJobOccupationMappingStandard_classificationDalei
  @CloverApiProperty({ description: '小类（第三级）', type: UpdateJobOccupationMappingStandard_classificationXiaoli, required: false, validator: JobOccupationMappingStandard_classificationXiaoliValidatorOptional })
  xiaoli?: UpdateJobOccupationMappingStandard_classificationXiaoli
  @CloverApiProperty({ description: '细类（第四级）', type: UpdateJobOccupationMappingStandard_classificationXilei, required: false, validator: JobOccupationMappingStandard_classificationXileiValidatorOptional })
  xilei?: UpdateJobOccupationMappingStandard_classificationXilei
  @CloverApiProperty({ description: '中类（第二级）', type: UpdateJobOccupationMappingStandard_classificationZhonglei, required: false, validator: JobOccupationMappingStandard_classificationZhongleiValidatorOptional })
  zhonglei?: UpdateJobOccupationMappingStandard_classificationZhonglei
}

export class ListJobOccupationMappingStandard_classificationDaleiItem {
  @CloverApiProperty({ description: '主匹配', type: ListJobOccupationMappingStandard_classificationDaleiPrimaryItem, required: false })
  primary?: ListJobOccupationMappingStandard_classificationDaleiPrimaryItem
}

export class GetJobOccupationMappingStandard_classificationDaleiResult {
  @CloverApiProperty({ description: '主匹配', type: GetJobOccupationMappingStandard_classificationDaleiPrimaryResult, required: false })
  primary?: GetJobOccupationMappingStandard_classificationDaleiPrimaryResult
}

export class AdminCreateJobOccupationMappingStandard_classification {
  @CloverApiProperty({ description: '大类（第一级）', type: AdminCreateJobOccupationMappingStandard_classificationDalei, required: false, validator: JobOccupationMappingStandard_classificationDaleiValidatorOptional })
  dalei?: AdminCreateJobOccupationMappingStandard_classificationDalei
  @CloverApiProperty({ description: '小类（第三级）', type: AdminCreateJobOccupationMappingStandard_classificationXiaoli, required: false, validator: JobOccupationMappingStandard_classificationXiaoliValidatorOptional })
  xiaoli?: AdminCreateJobOccupationMappingStandard_classificationXiaoli
  @CloverApiProperty({ description: '细类（第四级）', type: AdminCreateJobOccupationMappingStandard_classificationXilei, required: false, validator: JobOccupationMappingStandard_classificationXileiValidatorOptional })
  xilei?: AdminCreateJobOccupationMappingStandard_classificationXilei
  @CloverApiProperty({ description: '中类（第二级）', type: AdminCreateJobOccupationMappingStandard_classificationZhonglei, required: false, validator: JobOccupationMappingStandard_classificationZhongleiValidatorOptional })
  zhonglei?: AdminCreateJobOccupationMappingStandard_classificationZhonglei
}

export class AdminUpdateJobOccupationMappingStandard_classification {
  @CloverApiProperty({ description: '大类（第一级）', type: AdminUpdateJobOccupationMappingStandard_classificationDalei, required: false, validator: JobOccupationMappingStandard_classificationDaleiValidatorOptional })
  dalei?: AdminUpdateJobOccupationMappingStandard_classificationDalei
  @CloverApiProperty({ description: '小类（第三级）', type: AdminUpdateJobOccupationMappingStandard_classificationXiaoli, required: false, validator: JobOccupationMappingStandard_classificationXiaoliValidatorOptional })
  xiaoli?: AdminUpdateJobOccupationMappingStandard_classificationXiaoli
  @CloverApiProperty({ description: '细类（第四级）', type: AdminUpdateJobOccupationMappingStandard_classificationXilei, required: false, validator: JobOccupationMappingStandard_classificationXileiValidatorOptional })
  xilei?: AdminUpdateJobOccupationMappingStandard_classificationXilei
  @CloverApiProperty({ description: '中类（第二级）', type: AdminUpdateJobOccupationMappingStandard_classificationZhonglei, required: false, validator: JobOccupationMappingStandard_classificationZhongleiValidatorOptional })
  zhonglei?: AdminUpdateJobOccupationMappingStandard_classificationZhonglei
}

export class AdminListJobOccupationMappingStandard_classificationItem {
  @CloverApiProperty({ description: '大类（第一级）', type: AdminListJobOccupationMappingStandard_classificationDaleiItem, required: false })
  dalei?: AdminListJobOccupationMappingStandard_classificationDaleiItem
  @CloverApiProperty({ description: '小类（第三级）', type: AdminListJobOccupationMappingStandard_classificationXiaoliItem, required: false })
  xiaoli?: AdminListJobOccupationMappingStandard_classificationXiaoliItem
  @CloverApiProperty({ description: '细类（第四级）', type: AdminListJobOccupationMappingStandard_classificationXileiItem, required: false })
  xilei?: AdminListJobOccupationMappingStandard_classificationXileiItem
  @CloverApiProperty({ description: '中类（第二级）', type: AdminListJobOccupationMappingStandard_classificationZhongleiItem, required: false })
  zhonglei?: AdminListJobOccupationMappingStandard_classificationZhongleiItem
}

export class AdminGetJobOccupationMappingStandard_classificationResult {
  @CloverApiProperty({ description: '大类（第一级）', type: AdminGetJobOccupationMappingStandard_classificationDaleiResult, required: false })
  dalei?: AdminGetJobOccupationMappingStandard_classificationDaleiResult
  @CloverApiProperty({ description: '小类（第三级）', type: AdminGetJobOccupationMappingStandard_classificationXiaoliResult, required: false })
  xiaoli?: AdminGetJobOccupationMappingStandard_classificationXiaoliResult
  @CloverApiProperty({ description: '细类（第四级）', type: AdminGetJobOccupationMappingStandard_classificationXileiResult, required: false })
  xilei?: AdminGetJobOccupationMappingStandard_classificationXileiResult
  @CloverApiProperty({ description: '中类（第二级）', type: AdminGetJobOccupationMappingStandard_classificationZhongleiResult, required: false })
  zhonglei?: AdminGetJobOccupationMappingStandard_classificationZhongleiResult
}

export class ReplaceJobOccupationMappingStandard_classification {
  @CloverApiProperty({ description: '大类（第一级）', type: ReplaceJobOccupationMappingStandard_classificationDalei, required: false, validator: JobOccupationMappingStandard_classificationDaleiValidatorOptional })
  dalei?: ReplaceJobOccupationMappingStandard_classificationDalei
  @CloverApiProperty({ description: '小类（第三级）', type: ReplaceJobOccupationMappingStandard_classificationXiaoli, required: false, validator: JobOccupationMappingStandard_classificationXiaoliValidatorOptional })
  xiaoli?: ReplaceJobOccupationMappingStandard_classificationXiaoli
  @CloverApiProperty({ description: '细类（第四级）', type: ReplaceJobOccupationMappingStandard_classificationXilei, required: false, validator: JobOccupationMappingStandard_classificationXileiValidatorOptional })
  xilei?: ReplaceJobOccupationMappingStandard_classificationXilei
  @CloverApiProperty({ description: '中类（第二级）', type: ReplaceJobOccupationMappingStandard_classificationZhonglei, required: false, validator: JobOccupationMappingStandard_classificationZhongleiValidatorOptional })
  zhonglei?: ReplaceJobOccupationMappingStandard_classificationZhonglei
}

export class CreateJobOccupationMappingStandard_classification {
  @CloverApiProperty({ description: '大类（第一级）', type: CreateJobOccupationMappingStandard_classificationDalei, required: false, validator: JobOccupationMappingStandard_classificationDaleiValidatorOptional })
  dalei?: CreateJobOccupationMappingStandard_classificationDalei
  @CloverApiProperty({ description: '小类（第三级）', type: CreateJobOccupationMappingStandard_classificationXiaoli, required: false, validator: JobOccupationMappingStandard_classificationXiaoliValidatorOptional })
  xiaoli?: CreateJobOccupationMappingStandard_classificationXiaoli
  @CloverApiProperty({ description: '细类（第四级）', type: CreateJobOccupationMappingStandard_classificationXilei, required: false, validator: JobOccupationMappingStandard_classificationXileiValidatorOptional })
  xilei?: CreateJobOccupationMappingStandard_classificationXilei
  @CloverApiProperty({ description: '中类（第二级）', type: CreateJobOccupationMappingStandard_classificationZhonglei, required: false, validator: JobOccupationMappingStandard_classificationZhongleiValidatorOptional })
  zhonglei?: CreateJobOccupationMappingStandard_classificationZhonglei
}

export class ListJobOccupationMappingStandard_classificationItem {
  @CloverApiProperty({ description: '大类（第一级）', type: ListJobOccupationMappingStandard_classificationDaleiItem, required: false })
  dalei?: ListJobOccupationMappingStandard_classificationDaleiItem
  @CloverApiProperty({ description: '小类（第三级）', type: ListJobOccupationMappingStandard_classificationXiaoliItem, required: false })
  xiaoli?: ListJobOccupationMappingStandard_classificationXiaoliItem
  @CloverApiProperty({ description: '细类（第四级）', type: ListJobOccupationMappingStandard_classificationXileiItem, required: false })
  xilei?: ListJobOccupationMappingStandard_classificationXileiItem
  @CloverApiProperty({ description: '中类（第二级）', type: ListJobOccupationMappingStandard_classificationZhongleiItem, required: false })
  zhonglei?: ListJobOccupationMappingStandard_classificationZhongleiItem
}

export class GetJobOccupationMappingStandard_classificationResult {
  @CloverApiProperty({ description: '大类（第一级）', type: GetJobOccupationMappingStandard_classificationDaleiResult, required: false })
  dalei?: GetJobOccupationMappingStandard_classificationDaleiResult
  @CloverApiProperty({ description: '小类（第三级）', type: GetJobOccupationMappingStandard_classificationXiaoliResult, required: false })
  xiaoli?: GetJobOccupationMappingStandard_classificationXiaoliResult
  @CloverApiProperty({ description: '细类（第四级）', type: GetJobOccupationMappingStandard_classificationXileiResult, required: false })
  xilei?: GetJobOccupationMappingStandard_classificationXileiResult
  @CloverApiProperty({ description: '中类（第二级）', type: GetJobOccupationMappingStandard_classificationZhongleiResult, required: false })
  zhonglei?: GetJobOccupationMappingStandard_classificationZhongleiResult
}

export class JobOccupationMappingSourceOriginal_hierarchyAdminLookupFields {
  level_1?: string
  level_2?: string
}

export class AdminCreateJobOccupationMappingSourceOriginal_hierarchy {
  @CloverApiProperty({ description: '一级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional })
  level_2?: string
}

export class AdminUpdateJobOccupationMappingSourceOriginal_hierarchy {
  @CloverApiProperty({ description: '一级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional })
  level_2?: string
}

export class AdminListJobOccupationMappingSourceOriginal_hierarchyItem {
  @CloverApiProperty({ description: '一级类目', required: false })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false })
  level_2?: string
}

export class AdminGetJobOccupationMappingSourceOriginal_hierarchyResult {
  @CloverApiProperty({ description: '一级类目', required: false })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false })
  level_2?: string
}

export class ReplaceJobOccupationMappingSourceOriginal_hierarchy {
  @CloverApiProperty({ description: '一级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional })
  level_2?: string
}

export class CreateJobOccupationMappingSourceOriginal_hierarchy {
  @CloverApiProperty({ description: '一级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional })
  level_2?: string
}

export class UpdateJobOccupationMappingSourceOriginal_hierarchy {
  @CloverApiProperty({ description: '一级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_1ValidatorOptional })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false, validator: JobOccupationMappingSourceOriginal_hierarchyLevel_2ValidatorOptional })
  level_2?: string
}

export class ListJobOccupationMappingSourceOriginal_hierarchyItem {
  @CloverApiProperty({ description: '一级类目', required: false })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false })
  level_2?: string
}

export class GetJobOccupationMappingSourceOriginal_hierarchyResult {
  @CloverApiProperty({ description: '一级类目', required: false })
  level_1?: string
  @CloverApiProperty({ description: '二级类目', required: false })
  level_2?: string
}

export class JobOccupationMappingSourceAdminLookupFields {
  name?: string
}

export class UpdateJobOccupationMappingSource {
  @CloverApiProperty({ description: '来源名称', required: false, validator: JobOccupationMappingSourceNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: UpdateJobOccupationMappingSourceOriginal_hierarchy, required: false, validator: JobOccupationMappingSourceOriginal_hierarchyValidatorOptional })
  original_hierarchy?: UpdateJobOccupationMappingSourceOriginal_hierarchy
}

export class AdminCreateJobOccupationMappingSource {
  @CloverApiProperty({ description: '来源名称', required: false, validator: JobOccupationMappingSourceNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: AdminCreateJobOccupationMappingSourceOriginal_hierarchy, required: false, validator: JobOccupationMappingSourceOriginal_hierarchyValidatorOptional })
  original_hierarchy?: AdminCreateJobOccupationMappingSourceOriginal_hierarchy
}

export class AdminUpdateJobOccupationMappingSource {
  @CloverApiProperty({ description: '来源名称', required: false, validator: JobOccupationMappingSourceNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: AdminUpdateJobOccupationMappingSourceOriginal_hierarchy, required: false, validator: JobOccupationMappingSourceOriginal_hierarchyValidatorOptional })
  original_hierarchy?: AdminUpdateJobOccupationMappingSourceOriginal_hierarchy
}

export class AdminListJobOccupationMappingSourceItem {
  @CloverApiProperty({ description: '来源名称', required: false })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: AdminListJobOccupationMappingSourceOriginal_hierarchyItem, required: false })
  original_hierarchy?: AdminListJobOccupationMappingSourceOriginal_hierarchyItem
}

export class AdminGetJobOccupationMappingSourceResult {
  @CloverApiProperty({ description: '来源名称', required: false })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: AdminGetJobOccupationMappingSourceOriginal_hierarchyResult, required: false })
  original_hierarchy?: AdminGetJobOccupationMappingSourceOriginal_hierarchyResult
}

export class ReplaceJobOccupationMappingSource {
  @CloverApiProperty({ description: '来源名称', required: false, validator: JobOccupationMappingSourceNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: ReplaceJobOccupationMappingSourceOriginal_hierarchy, required: false, validator: JobOccupationMappingSourceOriginal_hierarchyValidatorOptional })
  original_hierarchy?: ReplaceJobOccupationMappingSourceOriginal_hierarchy
}

export class CreateJobOccupationMappingSource {
  @CloverApiProperty({ description: '来源名称', required: false, validator: JobOccupationMappingSourceNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: CreateJobOccupationMappingSourceOriginal_hierarchy, required: false, validator: JobOccupationMappingSourceOriginal_hierarchyValidatorOptional })
  original_hierarchy?: CreateJobOccupationMappingSourceOriginal_hierarchy
}

export class ListJobOccupationMappingSourceItem {
  @CloverApiProperty({ description: '来源名称', required: false })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: ListJobOccupationMappingSourceOriginal_hierarchyItem, required: false })
  original_hierarchy?: ListJobOccupationMappingSourceOriginal_hierarchyItem
}

export class GetJobOccupationMappingSourceResult {
  @CloverApiProperty({ description: '来源名称', required: false })
  name?: string
  @CloverApiProperty({ description: '来源原始层级', type: GetJobOccupationMappingSourceOriginal_hierarchyResult, required: false })
  original_hierarchy?: GetJobOccupationMappingSourceOriginal_hierarchyResult
}

export class JobOccupationMappingLookupFields {
  _id?: string
  position_name?: string
}

export class JobOccupationMappingAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  position_name?: string
  status?: string
  version?: string
}

export class AdminCreateJobOccupationMapping {
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: JobOccupationMapping_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '职位名称', validator: JobOccupationMappingPosition_nameValidator })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: AdminCreateJobOccupationMappingSource, required: false, validator: JobOccupationMappingSourceValidatorOptional })
  source?: AdminCreateJobOccupationMappingSource
  @CloverApiProperty({ description: '标准职业分类映射', type: AdminCreateJobOccupationMappingStandard_classification, required: false, validator: JobOccupationMappingStandard_classificationValidatorOptional })
  standard_classification?: AdminCreateJobOccupationMappingStandard_classification
  @CloverApiProperty({ description: '状态', required: false, validator: JobOccupationMappingStatusValidatorOptional })
  status?: string
  @CloverApiProperty({ description: '版本', required: false, validator: JobOccupationMappingVersionValidatorOptional })
  version?: string
}

export class AdminUpdateJobOccupationMapping {
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: JobOccupationMapping_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '职位名称', required: false, validator: JobOccupationMappingPosition_nameValidatorOptional })
  position_name?: string
  @CloverApiProperty({ description: '来源信息', type: AdminUpdateJobOccupationMappingSource, required: false, validator: JobOccupationMappingSourceValidatorOptional })
  source?: AdminUpdateJobOccupationMappingSource
  @CloverApiProperty({ description: '标准职业分类映射', type: AdminUpdateJobOccupationMappingStandard_classification, required: false, validator: JobOccupationMappingStandard_classificationValidatorOptional })
  standard_classification?: AdminUpdateJobOccupationMappingStandard_classification
  @CloverApiProperty({ description: '状态', required: false, validator: JobOccupationMappingStatusValidatorOptional })
  status?: string
  @CloverApiProperty({ description: '版本', required: false, validator: JobOccupationMappingVersionValidatorOptional })
  version?: string
}

export class AdminListJobOccupationMappingItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '职位名称' })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: AdminListJobOccupationMappingSourceItem, required: false })
  source?: AdminListJobOccupationMappingSourceItem
  @CloverApiProperty({ description: '标准职业分类映射', type: AdminListJobOccupationMappingStandard_classificationItem, required: false })
  standard_classification?: AdminListJobOccupationMappingStandard_classificationItem
  @CloverApiProperty({ description: '状态', required: false })
  status?: string
  @CloverApiProperty({ description: '版本', required: false })
  version?: string
}

export class AdminGetJobOccupationMappingResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '职位名称' })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: AdminGetJobOccupationMappingSourceResult, required: false })
  source?: AdminGetJobOccupationMappingSourceResult
  @CloverApiProperty({ description: '标准职业分类映射', type: AdminGetJobOccupationMappingStandard_classificationResult, required: false })
  standard_classification?: AdminGetJobOccupationMappingStandard_classificationResult
  @CloverApiProperty({ description: '状态', required: false })
  status?: string
  @CloverApiProperty({ description: '版本', required: false })
  version?: string
}

export class ReplaceJobOccupationMapping {
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '职位名称', validator: JobOccupationMappingPosition_nameValidator })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: ReplaceJobOccupationMappingSource, required: false, validator: JobOccupationMappingSourceValidatorOptional })
  source?: ReplaceJobOccupationMappingSource
  @CloverApiProperty({ description: '标准职业分类映射', type: ReplaceJobOccupationMappingStandard_classification, required: false, validator: JobOccupationMappingStandard_classificationValidatorOptional })
  standard_classification?: ReplaceJobOccupationMappingStandard_classification
  @CloverApiProperty({ description: '状态', required: false, validator: JobOccupationMappingStatusValidatorOptional })
  status?: string
  @CloverApiProperty({ description: '版本', required: false, validator: JobOccupationMappingVersionValidatorOptional })
  version?: string
}

export class CreateJobOccupationMapping {
  @CloverApiProperty({ required: false, validator: JobOccupationMapping_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '职位名称', validator: JobOccupationMappingPosition_nameValidator })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: CreateJobOccupationMappingSource, required: false, validator: JobOccupationMappingSourceValidatorOptional })
  source?: CreateJobOccupationMappingSource
  @CloverApiProperty({ description: '标准职业分类映射', type: CreateJobOccupationMappingStandard_classification, required: false, validator: JobOccupationMappingStandard_classificationValidatorOptional })
  standard_classification?: CreateJobOccupationMappingStandard_classification
  @CloverApiProperty({ description: '状态', required: false, validator: JobOccupationMappingStatusValidatorOptional })
  status?: string
  @CloverApiProperty({ description: '版本', required: false, validator: JobOccupationMappingVersionValidatorOptional })
  version?: string
}

export class ListJobOccupationMappingItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '职位名称' })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: ListJobOccupationMappingSourceItem, required: false })
  source?: ListJobOccupationMappingSourceItem
  @CloverApiProperty({ description: '标准职业分类映射', type: ListJobOccupationMappingStandard_classificationItem, required: false })
  standard_classification?: ListJobOccupationMappingStandard_classificationItem
  @CloverApiProperty({ description: '状态', required: false })
  status?: string
  @CloverApiProperty({ description: '版本', required: false })
  version?: string
}

export class GetJobOccupationMappingResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '职位名称' })
  position_name: string
  @CloverApiProperty({ description: '来源信息', type: GetJobOccupationMappingSourceResult, required: false })
  source?: GetJobOccupationMappingSourceResult
  @CloverApiProperty({ description: '标准职业分类映射', type: GetJobOccupationMappingStandard_classificationResult, required: false })
  standard_classification?: GetJobOccupationMappingStandard_classificationResult
  @CloverApiProperty({ description: '状态', required: false })
  status?: string
  @CloverApiProperty({ description: '版本', required: false })
  version?: string
}

export interface JobOccupationMappingCombinedId {
  _id?: string
}

export class ListJobOccupationMappingResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListJobOccupationMappingItem] })
  _items: ListJobOccupationMappingItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListJobOccupationMappingResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListJobOccupationMappingItem] })
  _items: AdminListJobOccupationMappingItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertJobOccupationMapping {
}

export class UpdateJobOccupationMapping {
}

export class RemoveJobOccupationMapping {
}

export class JobOccupationMappingCombinedId {
}

export interface JobOccupationMappingDtoType {
  item: GetJobOccupationMappingResult
  create: CreateJobOccupationMapping
  replace: ReplaceJobOccupationMapping
  update: UpdateJobOccupationMapping
}
