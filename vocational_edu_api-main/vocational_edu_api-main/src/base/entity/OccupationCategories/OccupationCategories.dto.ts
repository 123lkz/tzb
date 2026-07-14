import {
  ObjectIdString,
  Joi,
  ListResultPageInfo,
  ArraySchemaProperty,
  CloverApiProperty,
  ObjectSchemaProperty
} from '@havenzhang/clover'
import endpoint from '../../../endpoints/OccupationCategories'
export const OccupationCategories_idValidator = Joi.objectId()
export const OccupationCategories_idValidatorOptional = Joi.objectId().optional()
export const OccupationCategoriesCodeValidator = endpoint['schema']['code'].validator
export const OccupationCategoriesCodeValidatorOptional = endpoint['schema']['code'].validator.optional()
export const OccupationCategoriesGbm_codeValidator = endpoint['schema']['gbm_code'].validator
export const OccupationCategoriesGbm_codeValidatorOptional = endpoint['schema']['gbm_code'].validator.optional()
export const OccupationCategoriesNameValidator = endpoint['schema']['name'].validator
export const OccupationCategoriesNameValidatorOptional = endpoint['schema']['name'].validator.optional()
export const OccupationCategoriesLevelValidator = endpoint['schema']['level'].validator
export const OccupationCategoriesLevelValidatorOptional = endpoint['schema']['level'].validator.optional()
export const OccupationCategoriesParent_codeValidator = endpoint['schema']['parent_code'].validator
export const OccupationCategoriesParent_codeValidatorOptional = endpoint['schema']['parent_code'].validator.optional()
export const OccupationCategoriesParent_gbm_codeValidator = endpoint['schema']['parent_gbm_code'].validator
export const OccupationCategoriesParent_gbm_codeValidatorOptional =
  endpoint['schema']['parent_gbm_code'].validator.optional()
export const OccupationCategoriesPathValidator = endpoint['schema']['path'].validator
export const OccupationCategoriesPathValidatorOptional = endpoint['schema']['path'].validator.optional()
export const OccupationCategoriesDescriptionValidator = endpoint['schema']['description'].validator
export const OccupationCategoriesDescriptionValidatorOptional = endpoint['schema']['description'].validator.optional()
export const OccupationCategoriesTasksValidator = endpoint['schema']['tasks'].validator
export const OccupationCategoriesTasksValidatorOptional = endpoint['schema']['tasks'].validator.optional()
export const OccupationCategoriesSuffixValidator = endpoint['schema']['suffix'].validator
export const OccupationCategoriesSuffixValidatorOptional = endpoint['schema']['suffix'].validator.optional()
export const OccupationCategories_etagValidator = endpoint['schema']['_etag'].validator
export const OccupationCategories_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const OccupationCategories_updatedValidator = endpoint['schema']['_updated'].validator
export const OccupationCategories_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const OccupationCategories_createdValidator = endpoint['schema']['_created'].validator
export const OccupationCategories_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const OccupationCategoriesListQueryValidator = Joi.object().keys({
  _id: OccupationCategories_idValidator.optional(),
  code: OccupationCategoriesCodeValidator.optional(),
  name: OccupationCategoriesNameValidator.optional(),
  level: OccupationCategoriesLevelValidator.optional()
})
export const AdminOccupationCategoriesListQueryValidator = Joi.object().keys({
  _id: OccupationCategories_idValidator.optional(),
  code: OccupationCategoriesCodeValidator.optional(),
  gbm_code: OccupationCategoriesGbm_codeValidator.optional(),
  name: OccupationCategoriesNameValidator.optional(),
  level: OccupationCategoriesLevelValidator.optional(),
  parent_code: OccupationCategoriesParent_codeValidator.optional(),
  parent_gbm_code: OccupationCategoriesParent_gbm_codeValidator.optional(),
  path: OccupationCategoriesPathValidator.optional(),
  description: OccupationCategoriesDescriptionValidator.optional(),
  tasks: OccupationCategoriesTasksValidator.optional(),
  suffix: OccupationCategoriesSuffixValidator.optional(),
  _etag: OccupationCategories_etagValidator.optional(),
  _updated: OccupationCategories_updatedValidator.optional(),
  _created: OccupationCategories_createdValidator.optional()
})

export class OccupationCategoriesLookupFields {
  _id?: string
  code?: string
  level?: number
  name?: string
}

export class OccupationCategoriesAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  code?: string
  description?: string
  gbm_code?: string
  level?: number
  name?: string
  parent_code?: string
  parent_gbm_code?: string
  path?: string[]
  suffix?: string
  tasks?: string
}

export class AdminCreateOccupationCategories {
  @CloverApiProperty({ required: false, validator: OccupationCategories_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: OccupationCategories_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: OccupationCategories_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: OccupationCategories_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '标准职业编码', validator: OccupationCategoriesCodeValidator })
  code: string
  @CloverApiProperty({
    description: '职责描述',
    required: false,
    validator: OccupationCategoriesDescriptionValidatorOptional
  })
  description?: string
  @CloverApiProperty({
    description: '国标码',
    required: false,
    validator: OccupationCategoriesGbm_codeValidatorOptional
  })
  gbm_code?: string
  @CloverApiProperty({ description: '级别', validator: OccupationCategoriesLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: OccupationCategoriesNameValidator })
  name: string
  @CloverApiProperty({
    description: '父级编码',
    required: false,
    validator: OccupationCategoriesParent_codeValidatorOptional
  })
  parent_code?: string
  @CloverApiProperty({
    description: '父级国标码（可选）',
    required: false,
    validator: OccupationCategoriesParent_gbm_codeValidatorOptional
  })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', validator: OccupationCategoriesPathValidator })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false, validator: OccupationCategoriesSuffixValidatorOptional })
  suffix?: string
  @CloverApiProperty({
    description: '主要任务',
    required: false,
    validator: OccupationCategoriesTasksValidatorOptional
  })
  tasks?: string
}

export class AdminUpdateOccupationCategories {
  @CloverApiProperty({ required: false, validator: OccupationCategories_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: OccupationCategories_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: OccupationCategories_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: OccupationCategories_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({
    description: '标准职业编码',
    required: false,
    validator: OccupationCategoriesCodeValidatorOptional
  })
  code?: string
  @CloverApiProperty({
    description: '职责描述',
    required: false,
    validator: OccupationCategoriesDescriptionValidatorOptional
  })
  description?: string
  @CloverApiProperty({
    description: '国标码',
    required: false,
    validator: OccupationCategoriesGbm_codeValidatorOptional
  })
  gbm_code?: string
  @CloverApiProperty({ description: '级别', required: false, validator: OccupationCategoriesLevelValidatorOptional })
  level?: number
  @CloverApiProperty({ description: '名称', required: false, validator: OccupationCategoriesNameValidatorOptional })
  name?: string
  @CloverApiProperty({
    description: '父级编码',
    required: false,
    validator: OccupationCategoriesParent_codeValidatorOptional
  })
  parent_code?: string
  @CloverApiProperty({
    description: '父级国标码（可选）',
    required: false,
    validator: OccupationCategoriesParent_gbm_codeValidatorOptional
  })
  parent_gbm_code?: string
  @CloverApiProperty({
    description: '自顶向下编码路径',
    required: false,
    validator: OccupationCategoriesPathValidatorOptional
  })
  path?: string[]
  @CloverApiProperty({ description: '后缀', required: false, validator: OccupationCategoriesSuffixValidatorOptional })
  suffix?: string
  @CloverApiProperty({
    description: '主要任务',
    required: false,
    validator: OccupationCategoriesTasksValidatorOptional
  })
  tasks?: string
}

export class AdminListOccupationCategoriesItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '标准职业编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '国标码', required: false })
  gbm_code?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '父级国标码（可选）', required: false })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径' })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false })
  suffix?: string
  @CloverApiProperty({ description: '主要任务', required: false })
  tasks?: string
}

export class AdminGetOccupationCategoriesResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '标准职业编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '国标码', required: false })
  gbm_code?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '父级国标码（可选）', required: false })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径' })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false })
  suffix?: string
  @CloverApiProperty({ description: '主要任务', required: false })
  tasks?: string
}

export class ReplaceOccupationCategories {
  @CloverApiProperty({ required: false, validator: OccupationCategories_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '标准职业编码', validator: OccupationCategoriesCodeValidator })
  code: string
  @CloverApiProperty({
    description: '职责描述',
    required: false,
    validator: OccupationCategoriesDescriptionValidatorOptional
  })
  description?: string
  @CloverApiProperty({
    description: '国标码',
    required: false,
    validator: OccupationCategoriesGbm_codeValidatorOptional
  })
  gbm_code?: string
  @CloverApiProperty({ description: '级别', validator: OccupationCategoriesLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: OccupationCategoriesNameValidator })
  name: string
  @CloverApiProperty({
    description: '父级编码',
    required: false,
    validator: OccupationCategoriesParent_codeValidatorOptional
  })
  parent_code?: string
  @CloverApiProperty({
    description: '父级国标码（可选）',
    required: false,
    validator: OccupationCategoriesParent_gbm_codeValidatorOptional
  })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', validator: OccupationCategoriesPathValidator })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false, validator: OccupationCategoriesSuffixValidatorOptional })
  suffix?: string
  @CloverApiProperty({
    description: '主要任务',
    required: false,
    validator: OccupationCategoriesTasksValidatorOptional
  })
  tasks?: string
}

export class CreateOccupationCategories {
  @CloverApiProperty({ required: false, validator: OccupationCategories_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '标准职业编码', validator: OccupationCategoriesCodeValidator })
  code: string
  @CloverApiProperty({
    description: '职责描述',
    required: false,
    validator: OccupationCategoriesDescriptionValidatorOptional
  })
  description?: string
  @CloverApiProperty({
    description: '国标码',
    required: false,
    validator: OccupationCategoriesGbm_codeValidatorOptional
  })
  gbm_code?: string
  @CloverApiProperty({ description: '级别', validator: OccupationCategoriesLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: OccupationCategoriesNameValidator })
  name: string
  @CloverApiProperty({
    description: '父级编码',
    required: false,
    validator: OccupationCategoriesParent_codeValidatorOptional
  })
  parent_code?: string
  @CloverApiProperty({
    description: '父级国标码（可选）',
    required: false,
    validator: OccupationCategoriesParent_gbm_codeValidatorOptional
  })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', validator: OccupationCategoriesPathValidator })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false, validator: OccupationCategoriesSuffixValidatorOptional })
  suffix?: string
  @CloverApiProperty({
    description: '主要任务',
    required: false,
    validator: OccupationCategoriesTasksValidatorOptional
  })
  tasks?: string
}

export class ListOccupationCategoriesItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '标准职业编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '国标码', required: false })
  gbm_code?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '父级国标码（可选）', required: false })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径' })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false })
  suffix?: string
  @CloverApiProperty({ description: '主要任务', required: false })
  tasks?: string
}

export class GetOccupationCategoriesResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '标准职业编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '国标码', required: false })
  gbm_code?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '父级国标码（可选）', required: false })
  parent_gbm_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径' })
  path: string[]
  @CloverApiProperty({ description: '后缀', required: false })
  suffix?: string
  @CloverApiProperty({ description: '主要任务', required: false })
  tasks?: string
}

export interface OccupationCategoriesCombinedId {
  _id?: string
}

export class ListOccupationCategoriesResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListOccupationCategoriesItem] })
  _items: ListOccupationCategoriesItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListOccupationCategoriesResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListOccupationCategoriesItem] })
  _items: AdminListOccupationCategoriesItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertOccupationCategories {}

export class UpdateOccupationCategories {}

export class RemoveOccupationCategories {}

export class OccupationCategoriesCombinedId {}

export interface OccupationCategoriesDtoType {
  item: GetOccupationCategoriesResult
  create: CreateOccupationCategories
  replace: ReplaceOccupationCategories
  update: UpdateOccupationCategories
}
