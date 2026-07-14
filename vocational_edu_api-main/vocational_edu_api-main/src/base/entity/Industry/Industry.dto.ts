import {
  ObjectIdString,
  Joi,
  ListResultPageInfo,
  ArraySchemaProperty,
  CloverApiProperty,
  ObjectSchemaProperty
} from '@havenzhang/clover'
import endpoint from '../../../endpoints/Industry'
export const Industry_idValidator = Joi.objectId()
export const Industry_idValidatorOptional = Joi.objectId().optional()
export const IndustryCodeValidator = endpoint['schema']['code'].validator
export const IndustryCodeValidatorOptional = endpoint['schema']['code'].validator.optional()
export const IndustryNameValidator = endpoint['schema']['name'].validator
export const IndustryNameValidatorOptional = endpoint['schema']['name'].validator.optional()
export const IndustryLevelValidator = endpoint['schema']['level'].validator
export const IndustryLevelValidatorOptional = endpoint['schema']['level'].validator.optional()
export const IndustryParent_codeValidator = endpoint['schema']['parent_code'].validator
export const IndustryParent_codeValidatorOptional = endpoint['schema']['parent_code'].validator.optional()
export const IndustryPathValidator = endpoint['schema']['path'].validator
export const IndustryPathValidatorOptional = endpoint['schema']['path'].validator.optional()
export const IndustryDescriptionValidator = endpoint['schema']['description'].validator
export const IndustryDescriptionValidatorOptional = endpoint['schema']['description'].validator.optional()
export const Industry_etagValidator = endpoint['schema']['_etag'].validator
export const Industry_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const Industry_updatedValidator = endpoint['schema']['_updated'].validator
export const Industry_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const Industry_createdValidator = endpoint['schema']['_created'].validator
export const Industry_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const IndustryListQueryValidator = Joi.object().keys({
  _id: Industry_idValidator.optional(),
  code: IndustryCodeValidator.optional(),
  name: IndustryNameValidator.optional(),
  level: IndustryLevelValidator.optional()
})
export const AdminIndustryListQueryValidator = Joi.object().keys({
  _id: Industry_idValidator.optional(),
  code: IndustryCodeValidator.optional(),
  name: IndustryNameValidator.optional(),
  level: IndustryLevelValidator.optional(),
  parent_code: IndustryParent_codeValidator.optional(),
  path: IndustryPathValidator.optional(),
  description: IndustryDescriptionValidator.optional(),
  _etag: Industry_etagValidator.optional(),
  _updated: Industry_updatedValidator.optional(),
  _created: Industry_createdValidator.optional()
})

export class IndustryLookupFields {
  _id?: string
  code?: string
  level?: number
  name?: string
}

export class IndustryAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  code?: string
  description?: string
  level?: number
  name?: string
  parent_code?: string
  path?: string
}

export class AdminCreateIndustry {
  @CloverApiProperty({ required: false, validator: Industry_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Industry_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: Industry_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: Industry_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '编码', validator: IndustryCodeValidator })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false, validator: IndustryDescriptionValidatorOptional })
  description?: string
  @CloverApiProperty({ description: '级别', validator: IndustryLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: IndustryNameValidator })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false, validator: IndustryParent_codeValidatorOptional })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false, validator: IndustryPathValidatorOptional })
  path?: string
}

export class AdminUpdateIndustry {
  @CloverApiProperty({ required: false, validator: Industry_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Industry_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({
    description: 'ID',
    required: false,
    validator: Industry_idValidatorOptional,
    format: 'objectId'
  })
  _id?: string
  @CloverApiProperty({ required: false, validator: Industry_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '编码', required: false, validator: IndustryCodeValidatorOptional })
  code?: string
  @CloverApiProperty({ description: '职责描述', required: false, validator: IndustryDescriptionValidatorOptional })
  description?: string
  @CloverApiProperty({ description: '级别', required: false, validator: IndustryLevelValidatorOptional })
  level?: number
  @CloverApiProperty({ description: '名称', required: false, validator: IndustryNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '父级编码', required: false, validator: IndustryParent_codeValidatorOptional })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false, validator: IndustryPathValidatorOptional })
  path?: string
}

export class AdminListIndustryItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false })
  path?: string
}

export class AdminGetIndustryResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false })
  path?: string
}

export class ReplaceIndustry {
  @CloverApiProperty({ required: false, validator: Industry_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '编码', validator: IndustryCodeValidator })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false, validator: IndustryDescriptionValidatorOptional })
  description?: string
  @CloverApiProperty({ description: '级别', validator: IndustryLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: IndustryNameValidator })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false, validator: IndustryParent_codeValidatorOptional })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false, validator: IndustryPathValidatorOptional })
  path?: string
}

export class CreateIndustry {
  @CloverApiProperty({ required: false, validator: Industry_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '编码', validator: IndustryCodeValidator })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false, validator: IndustryDescriptionValidatorOptional })
  description?: string
  @CloverApiProperty({ description: '级别', validator: IndustryLevelValidator })
  level: number
  @CloverApiProperty({ description: '名称', validator: IndustryNameValidator })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false, validator: IndustryParent_codeValidatorOptional })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false, validator: IndustryPathValidatorOptional })
  path?: string
}

export class ListIndustryItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false })
  path?: string
}

export class GetIndustryResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '编码' })
  code: string
  @CloverApiProperty({ description: '职责描述', required: false })
  description?: string
  @CloverApiProperty({ description: '级别' })
  level: number
  @CloverApiProperty({ description: '名称' })
  name: string
  @CloverApiProperty({ description: '父级编码', required: false })
  parent_code?: string
  @CloverApiProperty({ description: '自顶向下编码路径', required: false })
  path?: string
}

export interface IndustryCombinedId {
  _id?: string
}

export class ListIndustryResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListIndustryItem] })
  _items: ListIndustryItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListIndustryResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListIndustryItem] })
  _items: AdminListIndustryItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertIndustry {}

export class UpdateIndustry {}

export class RemoveIndustry {}

export class IndustryCombinedId {}

export interface IndustryDtoType {
  item: GetIndustryResult
  create: CreateIndustry
  replace: ReplaceIndustry
  update: UpdateIndustry
}
