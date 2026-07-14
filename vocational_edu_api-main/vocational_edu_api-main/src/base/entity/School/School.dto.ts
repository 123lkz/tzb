import {
  ObjectIdString,
  Joi,
  ListResultPageInfo,
  ArraySchemaProperty,
  CloverApiProperty,
  ObjectSchemaProperty
} from '@havenzhang/clover'
import endpoint from '../../../endpoints/Schools'
export const School_idValidator = Joi.objectId()
export const School_idValidatorOptional = Joi.objectId().optional()
export const SchoolSchoolValidator = endpoint['schema']['school'].validator
export const SchoolSchoolValidatorOptional = endpoint['schema']['school'].validator.optional()
export const SchoolSchoolCodeValidator = Joi.number()
export const SchoolSchoolCodeValidatorOptional = Joi.number().optional()
export const SchoolManagerValidator = endpoint['schema']['manager'].validator
export const SchoolManagerValidatorOptional = endpoint['schema']['manager'].validator.optional()
export const SchoolLocationValidator = endpoint['schema']['location'].validator
export const SchoolLocationValidatorOptional = endpoint['schema']['location'].validator.optional()
export const SchoolProvinceValidator = endpoint['schema']['province'].validator
export const SchoolProvinceValidatorOptional = endpoint['schema']['province'].validator.optional()
export const SchoolLevelValidator = endpoint['schema']['level'].validator
export const SchoolLevelValidatorOptional = endpoint['schema']['level'].validator.optional()
export const SchoolNoteValidator = endpoint['schema']['note'].validator
export const SchoolNoteValidatorOptional = endpoint['schema']['note'].validator.optional()
export const SchoolTypeValidator = endpoint['schema']['type'].validator
export const SchoolTypeValidatorOptional = endpoint['schema']['type'].validator.optional()
export const SchoolIs985Validator = Joi.number()
export const SchoolIs985ValidatorOptional = Joi.number().optional()
export const SchoolIs211Validator = Joi.number()
export const SchoolIs211ValidatorOptional = Joi.number().optional()
export const SchoolUpdateDateValidator = Joi.date()
export const SchoolUpdateDateValidatorOptional = Joi.date().optional()
export const SchoolIsCenterValidator = Joi.number()
export const SchoolIsCenterValidatorOptional = Joi.number().optional()
export const SchoolIsLocalValidator = Joi.number()
export const SchoolIsLocalValidatorOptional = Joi.number().optional()
export const SchoolIsDoubleTopValidator = Joi.number()
export const SchoolIsDoubleTopValidatorOptional = Joi.number().optional()
export const SchoolIsDoubleHighValidator = Joi.number()
export const SchoolIsDoubleHighValidatorOptional = Joi.number().optional()
export const SchoolOpenStateValidator = Joi.number()
export const SchoolOpenStateValidatorOptional = Joi.number().optional()
export const School_etagValidator = endpoint['schema']['_etag'].validator
export const School_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const School_updatedValidator = endpoint['schema']['_updated'].validator
export const School_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const School_createdValidator = endpoint['schema']['_created'].validator
export const School_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const SchoolListQueryValidator = Joi.object().keys({
  _id: School_idValidator.optional(),
  school: SchoolSchoolValidator.optional(),
  schoolCode: SchoolSchoolCodeValidator.optional(),
  manager: SchoolManagerValidator.optional(),
  location: SchoolLocationValidator.optional(),
  province: SchoolProvinceValidator.optional(),
  level: SchoolLevelValidator.optional(),
  note: SchoolNoteValidator.optional(),
  is985: SchoolIs985Validator.optional(),
  is211: SchoolIs211Validator.optional(),
  isCenter: SchoolIsCenterValidator.optional(),
  isLocal: SchoolIsLocalValidator.optional(),
  isDoubleTop: SchoolIsDoubleTopValidator.optional(),
  isDoubleHigh: SchoolIsDoubleHighValidator.optional(),
  openState: SchoolOpenStateValidator.optional()
})
export const AdminSchoolListQueryValidator = Joi.object().keys({
  _id: School_idValidator.optional(),
  school: SchoolSchoolValidator.optional(),
  schoolCode: SchoolSchoolCodeValidator.optional(),
  manager: SchoolManagerValidator.optional(),
  location: SchoolLocationValidator.optional(),
  province: SchoolProvinceValidator.optional(),
  level: SchoolLevelValidator.optional(),
  note: SchoolNoteValidator.optional(),
  type: SchoolTypeValidator.optional(),
  is985: SchoolIs985Validator.optional(),
  is211: SchoolIs211Validator.optional(),
  updateDate: SchoolUpdateDateValidator.optional(),
  isCenter: SchoolIsCenterValidator.optional(),
  isLocal: SchoolIsLocalValidator.optional(),
  isDoubleTop: SchoolIsDoubleTopValidator.optional(),
  isDoubleHigh: SchoolIsDoubleHighValidator.optional(),
  openState: SchoolOpenStateValidator.optional(),
  _etag: School_etagValidator.optional(),
  _updated: School_updatedValidator.optional(),
  _created: School_createdValidator.optional()
})

export class SchoolLookupFields {
  _id?: string
  is211?: number
  is985?: number
  isCenter?: number
  isDoubleHigh?: number
  isDoubleTop?: number
  isLocal?: number
  level?: string
  location?: string
  manager?: string
  note?: string
  openState?: number
  province?: string
  school?: string
  schoolCode?: number
}

export class SchoolAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  is211?: number
  is985?: number
  isCenter?: number
  isDoubleHigh?: number
  isDoubleTop?: number
  isLocal?: number
  level?: string
  location?: string
  manager?: string
  note?: string
  openState?: number
  province?: string
  school?: string
  schoolCode?: number
  type?: string
  updateDate?: Date
}

export class AdminCreateSchool {
  @CloverApiProperty({ required: false, validator: School_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: School_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: School_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: School_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '是否为211', required: false, validator: SchoolIs211ValidatorOptional })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false, validator: SchoolIs985ValidatorOptional })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false, validator: SchoolIsCenterValidatorOptional })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false, validator: SchoolIsDoubleHighValidatorOptional })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false, validator: SchoolIsDoubleTopValidatorOptional })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false, validator: SchoolIsLocalValidatorOptional })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false, validator: SchoolLevelValidatorOptional })
  level?: string
  @CloverApiProperty({ description: '城市', required: false, validator: SchoolLocationValidatorOptional })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false, validator: SchoolManagerValidatorOptional })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false, validator: SchoolNoteValidatorOptional })
  note?: string
  @CloverApiProperty({ description: '状态', required: false, validator: SchoolOpenStateValidatorOptional })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false, validator: SchoolProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '学校名称', validator: SchoolSchoolValidator })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false, validator: SchoolSchoolCodeValidatorOptional })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false, validator: SchoolTypeValidatorOptional })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false, validator: SchoolUpdateDateValidatorOptional })
  updateDate?: Date
}

export class AdminUpdateSchool {
  @CloverApiProperty({ required: false, validator: School_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: School_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: School_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: School_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '是否为211', required: false, validator: SchoolIs211ValidatorOptional })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false, validator: SchoolIs985ValidatorOptional })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false, validator: SchoolIsCenterValidatorOptional })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false, validator: SchoolIsDoubleHighValidatorOptional })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false, validator: SchoolIsDoubleTopValidatorOptional })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false, validator: SchoolIsLocalValidatorOptional })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false, validator: SchoolLevelValidatorOptional })
  level?: string
  @CloverApiProperty({ description: '城市', required: false, validator: SchoolLocationValidatorOptional })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false, validator: SchoolManagerValidatorOptional })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false, validator: SchoolNoteValidatorOptional })
  note?: string
  @CloverApiProperty({ description: '状态', required: false, validator: SchoolOpenStateValidatorOptional })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false, validator: SchoolProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '学校名称', required: false, validator: SchoolSchoolValidatorOptional })
  school?: string
  @CloverApiProperty({ description: '学校代码', required: false, validator: SchoolSchoolCodeValidatorOptional })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false, validator: SchoolTypeValidatorOptional })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false, validator: SchoolUpdateDateValidatorOptional })
  updateDate?: Date
}

export class AdminListSchoolItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '是否为211', required: false })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false })
  level?: string
  @CloverApiProperty({ description: '城市', required: false })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false })
  note?: string
  @CloverApiProperty({ description: '状态', required: false })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '学校名称' })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false })
  updateDate?: Date
}

export class AdminGetSchoolResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '是否为211', required: false })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false })
  level?: string
  @CloverApiProperty({ description: '城市', required: false })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false })
  note?: string
  @CloverApiProperty({ description: '状态', required: false })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '学校名称' })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false })
  updateDate?: Date
}

export class ReplaceSchool {
  @CloverApiProperty({ required: false, validator: School_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '是否为211', required: false, validator: SchoolIs211ValidatorOptional })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false, validator: SchoolIs985ValidatorOptional })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false, validator: SchoolIsCenterValidatorOptional })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false, validator: SchoolIsDoubleHighValidatorOptional })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false, validator: SchoolIsDoubleTopValidatorOptional })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false, validator: SchoolIsLocalValidatorOptional })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false, validator: SchoolLevelValidatorOptional })
  level?: string
  @CloverApiProperty({ description: '城市', required: false, validator: SchoolLocationValidatorOptional })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false, validator: SchoolManagerValidatorOptional })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false, validator: SchoolNoteValidatorOptional })
  note?: string
  @CloverApiProperty({ description: '状态', required: false, validator: SchoolOpenStateValidatorOptional })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false, validator: SchoolProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '学校名称', validator: SchoolSchoolValidator })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false, validator: SchoolSchoolCodeValidatorOptional })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false, validator: SchoolTypeValidatorOptional })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false, validator: SchoolUpdateDateValidatorOptional })
  updateDate?: Date
}

export class CreateSchool {
  @CloverApiProperty({ required: false, validator: School_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '是否为211', required: false, validator: SchoolIs211ValidatorOptional })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false, validator: SchoolIs985ValidatorOptional })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false, validator: SchoolIsCenterValidatorOptional })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false, validator: SchoolIsDoubleHighValidatorOptional })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false, validator: SchoolIsDoubleTopValidatorOptional })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false, validator: SchoolIsLocalValidatorOptional })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false, validator: SchoolLevelValidatorOptional })
  level?: string
  @CloverApiProperty({ description: '城市', required: false, validator: SchoolLocationValidatorOptional })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false, validator: SchoolManagerValidatorOptional })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false, validator: SchoolNoteValidatorOptional })
  note?: string
  @CloverApiProperty({ description: '状态', required: false, validator: SchoolOpenStateValidatorOptional })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false, validator: SchoolProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '学校名称', validator: SchoolSchoolValidator })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false, validator: SchoolSchoolCodeValidatorOptional })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false, validator: SchoolTypeValidatorOptional })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false, validator: SchoolUpdateDateValidatorOptional })
  updateDate?: Date
}

export class ListSchoolItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '是否为211', required: false })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false })
  level?: string
  @CloverApiProperty({ description: '城市', required: false })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false })
  note?: string
  @CloverApiProperty({ description: '状态', required: false })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '学校名称' })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false })
  updateDate?: Date
}

export class GetSchoolResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '是否为211', required: false })
  is211?: number
  @CloverApiProperty({ description: '是否为985', required: false })
  is985?: number
  @CloverApiProperty({ description: '是否为中央高校', required: false })
  isCenter?: number
  @CloverApiProperty({ description: '是否为双高院校', required: false })
  isDoubleHigh?: number
  @CloverApiProperty({ description: '是否为双一流', required: false })
  isDoubleTop?: number
  @CloverApiProperty({ description: '是否为地方高校', required: false })
  isLocal?: number
  @CloverApiProperty({ description: '办学层次', required: false })
  level?: string
  @CloverApiProperty({ description: '城市', required: false })
  location?: string
  @CloverApiProperty({ description: '主管部门', required: false })
  manager?: string
  @CloverApiProperty({ description: '学校性质', required: false })
  note?: string
  @CloverApiProperty({ description: '状态', required: false })
  openState?: number
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '学校名称' })
  school: string
  @CloverApiProperty({ description: '学校代码', required: false })
  schoolCode?: number
  @CloverApiProperty({ description: '类型', required: false })
  type?: string
  @CloverApiProperty({ description: '更新时间', required: false })
  updateDate?: Date
}

export interface SchoolCombinedId {
  _id?: string
}

export class ListSchoolResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListSchoolItem] })
  _items: ListSchoolItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListSchoolResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListSchoolItem] })
  _items: AdminListSchoolItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertSchool {}

export class UpdateSchool {}

export class RemoveSchool {}

export class SchoolCombinedId {}

export interface SchoolDtoType {
  item: GetSchoolResult
  create: CreateSchool
  replace: ReplaceSchool
  update: UpdateSchool
}
