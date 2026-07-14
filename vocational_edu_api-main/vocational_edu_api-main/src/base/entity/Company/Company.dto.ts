import { ObjectIdString, Joi, ListResultPageInfo, ArraySchemaProperty, CloverApiProperty, ObjectSchemaProperty } from '@havenzhang/clover'
import endpoint from '../../../endpoints/Company'
export const Company_idValidator = Joi.objectId()
export const Company_idValidatorOptional = Joi.objectId().optional()
export const CompanyCompany_idValidator = Joi.string()
export const CompanyCompany_idValidatorOptional = Joi.string().optional()
export const CompanyCredit_codeValidator = Joi.string()
export const CompanyCredit_codeValidatorOptional = Joi.string().optional()
export const CompanyRegistration_numberValidator = Joi.string()
export const CompanyRegistration_numberValidatorOptional = Joi.string().optional()
export const CompanyCompany_nameValidator = Joi.string()
export const CompanyCompany_nameValidatorOptional = Joi.string().optional()
export const CompanyEnglish_nameValidator = Joi.string()
export const CompanyEnglish_nameValidatorOptional = Joi.string().optional()
export const CompanyFormer_namesValidator = Joi.array().items(Joi.string())
export const CompanyFormer_namesValidatorOptional = Joi.array().items(Joi.string()).optional()
export const CompanyLegal_representativeValidator = Joi.string()
export const CompanyLegal_representativeValidatorOptional = Joi.string().optional()
export const CompanyCompany_typeValidator = Joi.string()
export const CompanyCompany_typeValidatorOptional = Joi.string().optional()
export const CompanyOrganization_codeValidator = Joi.string()
export const CompanyOrganization_codeValidatorOptional = Joi.string().optional()
export const CompanyCompany_sizeValidator = Joi.string()
export const CompanyCompany_sizeValidatorOptional = Joi.string().optional()
export const CompanyBusiness_statusValidator = Joi.string()
export const CompanyBusiness_statusValidatorOptional = Joi.string().optional()
export const CompanyIndustry_categoryValidator = Joi.string()
export const CompanyIndustry_categoryValidatorOptional = Joi.string().optional()
export const CompanyIndustry_majorValidator = Joi.string()
export const CompanyIndustry_majorValidatorOptional = Joi.string().optional()
export const CompanyIndustry_mediumValidator = Joi.string()
export const CompanyIndustry_mediumValidatorOptional = Joi.string().optional()
export const CompanyIndustry_minorValidator = Joi.string()
export const CompanyIndustry_minorValidatorOptional = Joi.string().optional()
export const CompanyIndustry_codeValidator = Joi.string()
export const CompanyIndustry_codeValidatorOptional = Joi.string().optional()
export const CompanyBusiness_scopeValidator = Joi.string()
export const CompanyBusiness_scopeValidatorOptional = Joi.string().optional()
export const CompanyRegistered_capitalValidator = Joi.number()
export const CompanyRegistered_capitalValidatorOptional = Joi.number().optional()
export const CompanyPaid_capitalValidator = Joi.number()
export const CompanyPaid_capitalValidatorOptional = Joi.number().optional()
export const CompanyEstablishment_dateValidator = Joi.date()
export const CompanyEstablishment_dateValidatorOptional = Joi.date().optional()
export const CompanyApproval_dateValidator = Joi.date()
export const CompanyApproval_dateValidatorOptional = Joi.date().optional()
export const CompanyBusiness_termValidator = Joi.string()
export const CompanyBusiness_termValidatorOptional = Joi.string().optional()
export const CompanySocial_security_countValidator = Joi.number()
export const CompanySocial_security_countValidatorOptional = Joi.number().optional()
export const CompanyProvinceValidator = Joi.string()
export const CompanyProvinceValidatorOptional = Joi.string().optional()
export const CompanyCityValidator = Joi.string()
export const CompanyCityValidatorOptional = Joi.string().optional()
export const CompanyDistrictValidator = Joi.string()
export const CompanyDistrictValidatorOptional = Joi.string().optional()
export const CompanyRegistered_addressValidator = Joi.string()
export const CompanyRegistered_addressValidatorOptional = Joi.string().optional()
export const CompanyCurrent_addressValidator = Joi.string()
export const CompanyCurrent_addressValidatorOptional = Joi.string().optional()
export const CompanyBusiness_phoneValidator = Joi.string()
export const CompanyBusiness_phoneValidatorOptional = Joi.string().optional()
export const CompanyAdditional_phonesValidator = Joi.array().items(Joi.string())
export const CompanyAdditional_phonesValidatorOptional = Joi.array().items(Joi.string()).optional()
export const CompanyParent_groupValidator = Joi.string()
export const CompanyParent_groupValidatorOptional = Joi.string().optional()
export const CompanyShareholdersValidator = Joi.array().items(Joi.string())
export const CompanyShareholdersValidatorOptional = Joi.array().items(Joi.string()).optional()
export const CompanyRegistration_authorityValidator = Joi.string()
export const CompanyRegistration_authorityValidatorOptional = Joi.string().optional()
export const CompanyHas_dishonest_recordValidator = Joi.boolean()
export const CompanyHas_dishonest_recordValidatorOptional = Joi.boolean().optional()
export const CompanyHas_execution_recordValidator = Joi.boolean()
export const CompanyHas_execution_recordValidatorOptional = Joi.boolean().optional()
export const CompanyRegistered_emailValidator = Joi.string()
export const CompanyRegistered_emailValidatorOptional = Joi.string().optional()
export const CompanyVerified_emailValidator = Joi.string()
export const CompanyVerified_emailValidatorOptional = Joi.string().optional()
export const CompanyImport_dateValidator = Joi.date()
export const CompanyImport_dateValidatorOptional = Joi.date().optional()
export const CompanyData_sourceValidator = Joi.string()
export const CompanyData_sourceValidatorOptional = Joi.string().optional()
export const CompanyCreate_timeValidator = Joi.date()
export const CompanyCreate_timeValidatorOptional = Joi.date().optional()
export const Company_etagValidator = endpoint['schema']['_etag'].validator
export const Company_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const Company_updatedValidator = endpoint['schema']['_updated'].validator
export const Company_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const Company_createdValidator = endpoint['schema']['_created'].validator
export const Company_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const CompanyListQueryValidator = Joi.object().keys({
  _id: Company_idValidator.optional(),
  company_name: CompanyCompany_nameValidator.optional(),
  create_time: CompanyCreate_timeValidator.optional()
})
export const AdminCompanyListQueryValidator = Joi.object().keys({
  _id: Company_idValidator.optional(),
  company_id: CompanyCompany_idValidator.optional(),
  credit_code: CompanyCredit_codeValidator.optional(),
  registration_number: CompanyRegistration_numberValidator.optional(),
  company_name: CompanyCompany_nameValidator.optional(),
  english_name: CompanyEnglish_nameValidator.optional(),
  former_names: CompanyFormer_namesValidator.optional(),
  legal_representative: CompanyLegal_representativeValidator.optional(),
  company_type: CompanyCompany_typeValidator.optional(),
  organization_code: CompanyOrganization_codeValidator.optional(),
  company_size: CompanyCompany_sizeValidator.optional(),
  business_status: CompanyBusiness_statusValidator.optional(),
  industry_category: CompanyIndustry_categoryValidator.optional(),
  industry_major: CompanyIndustry_majorValidator.optional(),
  industry_medium: CompanyIndustry_mediumValidator.optional(),
  industry_minor: CompanyIndustry_minorValidator.optional(),
  industry_code: CompanyIndustry_codeValidator.optional(),
  business_scope: CompanyBusiness_scopeValidator.optional(),
  registered_capital: CompanyRegistered_capitalValidator.optional(),
  paid_capital: CompanyPaid_capitalValidator.optional(),
  establishment_date: CompanyEstablishment_dateValidator.optional(),
  approval_date: CompanyApproval_dateValidator.optional(),
  business_term: CompanyBusiness_termValidator.optional(),
  social_security_count: CompanySocial_security_countValidator.optional(),
  province: CompanyProvinceValidator.optional(),
  city: CompanyCityValidator.optional(),
  district: CompanyDistrictValidator.optional(),
  registered_address: CompanyRegistered_addressValidator.optional(),
  current_address: CompanyCurrent_addressValidator.optional(),
  business_phone: CompanyBusiness_phoneValidator.optional(),
  additional_phones: CompanyAdditional_phonesValidator.optional(),
  parent_group: CompanyParent_groupValidator.optional(),
  shareholders: CompanyShareholdersValidator.optional(),
  registration_authority: CompanyRegistration_authorityValidator.optional(),
  has_dishonest_record: CompanyHas_dishonest_recordValidator.optional(),
  has_execution_record: CompanyHas_execution_recordValidator.optional(),
  registered_email: CompanyRegistered_emailValidator.optional(),
  verified_email: CompanyVerified_emailValidator.optional(),
  import_date: CompanyImport_dateValidator.optional(),
  data_source: CompanyData_sourceValidator.optional(),
  create_time: CompanyCreate_timeValidator.optional(),
  _etag: Company_etagValidator.optional(),
  _updated: Company_updatedValidator.optional(),
  _created: Company_createdValidator.optional()
})

export class UpdateCompany {
  @CloverApiProperty({ description: '备用电话列表', required: false, validator: CompanyAdditional_phonesValidatorOptional })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false, validator: CompanyApproval_dateValidatorOptional })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false, validator: CompanyBusiness_phoneValidatorOptional })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false, validator: CompanyBusiness_scopeValidatorOptional })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false, validator: CompanyBusiness_statusValidatorOptional })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false, validator: CompanyBusiness_termValidatorOptional })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false, validator: CompanyCityValidatorOptional })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false, validator: CompanyCompany_idValidatorOptional })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false, validator: CompanyCompany_nameValidatorOptional })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: CompanyCompany_sizeValidatorOptional })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false, validator: CompanyCompany_typeValidatorOptional })
  company_type?: string
  @CloverApiProperty({ description: '统一社会信用代码', required: false, validator: CompanyCredit_codeValidatorOptional })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false, validator: CompanyCurrent_addressValidatorOptional })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false, validator: CompanyData_sourceValidatorOptional })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false, validator: CompanyDistrictValidatorOptional })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false, validator: CompanyEnglish_nameValidatorOptional })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false, validator: CompanyEstablishment_dateValidatorOptional })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false, validator: CompanyFormer_namesValidatorOptional })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false, validator: CompanyHas_dishonest_recordValidatorOptional })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false, validator: CompanyHas_execution_recordValidatorOptional })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false, validator: CompanyImport_dateValidatorOptional })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false, validator: CompanyIndustry_categoryValidatorOptional })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false, validator: CompanyIndustry_codeValidatorOptional })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false, validator: CompanyIndustry_majorValidatorOptional })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false, validator: CompanyIndustry_mediumValidatorOptional })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false, validator: CompanyIndustry_minorValidatorOptional })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false, validator: CompanyLegal_representativeValidatorOptional })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false, validator: CompanyOrganization_codeValidatorOptional })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false, validator: CompanyPaid_capitalValidatorOptional })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false, validator: CompanyParent_groupValidatorOptional })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false, validator: CompanyProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false, validator: CompanyRegistered_addressValidatorOptional })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false, validator: CompanyRegistered_capitalValidatorOptional })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false, validator: CompanyRegistered_emailValidatorOptional })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false, validator: CompanyRegistration_authorityValidatorOptional })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false, validator: CompanyRegistration_numberValidatorOptional })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false, validator: CompanyShareholdersValidatorOptional })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false, validator: CompanySocial_security_countValidatorOptional })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false, validator: CompanyVerified_emailValidatorOptional })
  verified_email?: string
}

export class CompanyLookupFields {
  _id?: string
  company_name?: string
  create_time?: Date
}

export class CompanyAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  additional_phones?: string[]
  approval_date?: Date
  business_phone?: string
  business_scope?: string
  business_status?: string
  business_term?: string
  city?: string
  company_id?: string
  company_name?: string
  company_size?: string
  company_type?: string
  create_time?: Date
  credit_code?: string
  current_address?: string
  data_source?: string
  district?: string
  english_name?: string
  establishment_date?: Date
  former_names?: string[]
  has_dishonest_record?: boolean
  has_execution_record?: boolean
  import_date?: Date
  industry_category?: string
  industry_code?: string
  industry_major?: string
  industry_medium?: string
  industry_minor?: string
  legal_representative?: string
  organization_code?: string
  paid_capital?: number
  parent_group?: string
  province?: string
  registered_address?: string
  registered_capital?: number
  registered_email?: string
  registration_authority?: string
  registration_number?: string
  shareholders?: string[]
  social_security_count?: number
  verified_email?: string
}

export class AdminCreateCompany {
  @CloverApiProperty({ required: false, validator: Company_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Company_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: Company_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: Company_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '备用电话列表', required: false, validator: CompanyAdditional_phonesValidatorOptional })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false, validator: CompanyApproval_dateValidatorOptional })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false, validator: CompanyBusiness_phoneValidatorOptional })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false, validator: CompanyBusiness_scopeValidatorOptional })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false, validator: CompanyBusiness_statusValidatorOptional })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false, validator: CompanyBusiness_termValidatorOptional })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false, validator: CompanyCityValidatorOptional })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false, validator: CompanyCompany_idValidatorOptional })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false, validator: CompanyCompany_nameValidatorOptional })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: CompanyCompany_sizeValidatorOptional })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false, validator: CompanyCompany_typeValidatorOptional })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: CompanyCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false, validator: CompanyCredit_codeValidatorOptional })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false, validator: CompanyCurrent_addressValidatorOptional })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false, validator: CompanyData_sourceValidatorOptional })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false, validator: CompanyDistrictValidatorOptional })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false, validator: CompanyEnglish_nameValidatorOptional })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false, validator: CompanyEstablishment_dateValidatorOptional })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false, validator: CompanyFormer_namesValidatorOptional })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false, validator: CompanyHas_dishonest_recordValidatorOptional })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false, validator: CompanyHas_execution_recordValidatorOptional })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false, validator: CompanyImport_dateValidatorOptional })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false, validator: CompanyIndustry_categoryValidatorOptional })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false, validator: CompanyIndustry_codeValidatorOptional })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false, validator: CompanyIndustry_majorValidatorOptional })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false, validator: CompanyIndustry_mediumValidatorOptional })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false, validator: CompanyIndustry_minorValidatorOptional })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false, validator: CompanyLegal_representativeValidatorOptional })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false, validator: CompanyOrganization_codeValidatorOptional })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false, validator: CompanyPaid_capitalValidatorOptional })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false, validator: CompanyParent_groupValidatorOptional })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false, validator: CompanyProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false, validator: CompanyRegistered_addressValidatorOptional })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false, validator: CompanyRegistered_capitalValidatorOptional })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false, validator: CompanyRegistered_emailValidatorOptional })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false, validator: CompanyRegistration_authorityValidatorOptional })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false, validator: CompanyRegistration_numberValidatorOptional })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false, validator: CompanyShareholdersValidatorOptional })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false, validator: CompanySocial_security_countValidatorOptional })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false, validator: CompanyVerified_emailValidatorOptional })
  verified_email?: string
}

export class AdminUpdateCompany {
  @CloverApiProperty({ required: false, validator: Company_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: Company_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: Company_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: Company_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '备用电话列表', required: false, validator: CompanyAdditional_phonesValidatorOptional })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false, validator: CompanyApproval_dateValidatorOptional })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false, validator: CompanyBusiness_phoneValidatorOptional })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false, validator: CompanyBusiness_scopeValidatorOptional })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false, validator: CompanyBusiness_statusValidatorOptional })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false, validator: CompanyBusiness_termValidatorOptional })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false, validator: CompanyCityValidatorOptional })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false, validator: CompanyCompany_idValidatorOptional })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false, validator: CompanyCompany_nameValidatorOptional })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: CompanyCompany_sizeValidatorOptional })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false, validator: CompanyCompany_typeValidatorOptional })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: CompanyCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false, validator: CompanyCredit_codeValidatorOptional })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false, validator: CompanyCurrent_addressValidatorOptional })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false, validator: CompanyData_sourceValidatorOptional })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false, validator: CompanyDistrictValidatorOptional })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false, validator: CompanyEnglish_nameValidatorOptional })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false, validator: CompanyEstablishment_dateValidatorOptional })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false, validator: CompanyFormer_namesValidatorOptional })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false, validator: CompanyHas_dishonest_recordValidatorOptional })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false, validator: CompanyHas_execution_recordValidatorOptional })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false, validator: CompanyImport_dateValidatorOptional })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false, validator: CompanyIndustry_categoryValidatorOptional })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false, validator: CompanyIndustry_codeValidatorOptional })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false, validator: CompanyIndustry_majorValidatorOptional })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false, validator: CompanyIndustry_mediumValidatorOptional })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false, validator: CompanyIndustry_minorValidatorOptional })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false, validator: CompanyLegal_representativeValidatorOptional })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false, validator: CompanyOrganization_codeValidatorOptional })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false, validator: CompanyPaid_capitalValidatorOptional })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false, validator: CompanyParent_groupValidatorOptional })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false, validator: CompanyProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false, validator: CompanyRegistered_addressValidatorOptional })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false, validator: CompanyRegistered_capitalValidatorOptional })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false, validator: CompanyRegistered_emailValidatorOptional })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false, validator: CompanyRegistration_authorityValidatorOptional })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false, validator: CompanyRegistration_numberValidatorOptional })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false, validator: CompanyShareholdersValidatorOptional })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false, validator: CompanySocial_security_countValidatorOptional })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false, validator: CompanyVerified_emailValidatorOptional })
  verified_email?: string
}

export class AdminListCompanyItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '备用电话列表', required: false })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false })
  verified_email?: string
}

export class AdminGetCompanyResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '备用电话列表', required: false })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false })
  verified_email?: string
}

export class ReplaceCompany {
  @CloverApiProperty({ required: false, validator: Company_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '备用电话列表', required: false, validator: CompanyAdditional_phonesValidatorOptional })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false, validator: CompanyApproval_dateValidatorOptional })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false, validator: CompanyBusiness_phoneValidatorOptional })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false, validator: CompanyBusiness_scopeValidatorOptional })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false, validator: CompanyBusiness_statusValidatorOptional })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false, validator: CompanyBusiness_termValidatorOptional })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false, validator: CompanyCityValidatorOptional })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false, validator: CompanyCompany_idValidatorOptional })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false, validator: CompanyCompany_nameValidatorOptional })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: CompanyCompany_sizeValidatorOptional })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false, validator: CompanyCompany_typeValidatorOptional })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: CompanyCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false, validator: CompanyCredit_codeValidatorOptional })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false, validator: CompanyCurrent_addressValidatorOptional })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false, validator: CompanyData_sourceValidatorOptional })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false, validator: CompanyDistrictValidatorOptional })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false, validator: CompanyEnglish_nameValidatorOptional })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false, validator: CompanyEstablishment_dateValidatorOptional })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false, validator: CompanyFormer_namesValidatorOptional })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false, validator: CompanyHas_dishonest_recordValidatorOptional })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false, validator: CompanyHas_execution_recordValidatorOptional })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false, validator: CompanyImport_dateValidatorOptional })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false, validator: CompanyIndustry_categoryValidatorOptional })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false, validator: CompanyIndustry_codeValidatorOptional })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false, validator: CompanyIndustry_majorValidatorOptional })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false, validator: CompanyIndustry_mediumValidatorOptional })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false, validator: CompanyIndustry_minorValidatorOptional })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false, validator: CompanyLegal_representativeValidatorOptional })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false, validator: CompanyOrganization_codeValidatorOptional })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false, validator: CompanyPaid_capitalValidatorOptional })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false, validator: CompanyParent_groupValidatorOptional })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false, validator: CompanyProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false, validator: CompanyRegistered_addressValidatorOptional })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false, validator: CompanyRegistered_capitalValidatorOptional })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false, validator: CompanyRegistered_emailValidatorOptional })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false, validator: CompanyRegistration_authorityValidatorOptional })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false, validator: CompanyRegistration_numberValidatorOptional })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false, validator: CompanyShareholdersValidatorOptional })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false, validator: CompanySocial_security_countValidatorOptional })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false, validator: CompanyVerified_emailValidatorOptional })
  verified_email?: string
}

export class CreateCompany {
  @CloverApiProperty({ required: false, validator: Company_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '备用电话列表', required: false, validator: CompanyAdditional_phonesValidatorOptional })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false, validator: CompanyApproval_dateValidatorOptional })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false, validator: CompanyBusiness_phoneValidatorOptional })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false, validator: CompanyBusiness_scopeValidatorOptional })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false, validator: CompanyBusiness_statusValidatorOptional })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false, validator: CompanyBusiness_termValidatorOptional })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false, validator: CompanyCityValidatorOptional })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false, validator: CompanyCompany_idValidatorOptional })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false, validator: CompanyCompany_nameValidatorOptional })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false, validator: CompanyCompany_sizeValidatorOptional })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false, validator: CompanyCompany_typeValidatorOptional })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false, validator: CompanyCreate_timeValidatorOptional })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false, validator: CompanyCredit_codeValidatorOptional })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false, validator: CompanyCurrent_addressValidatorOptional })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false, validator: CompanyData_sourceValidatorOptional })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false, validator: CompanyDistrictValidatorOptional })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false, validator: CompanyEnglish_nameValidatorOptional })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false, validator: CompanyEstablishment_dateValidatorOptional })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false, validator: CompanyFormer_namesValidatorOptional })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false, validator: CompanyHas_dishonest_recordValidatorOptional })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false, validator: CompanyHas_execution_recordValidatorOptional })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false, validator: CompanyImport_dateValidatorOptional })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false, validator: CompanyIndustry_categoryValidatorOptional })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false, validator: CompanyIndustry_codeValidatorOptional })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false, validator: CompanyIndustry_majorValidatorOptional })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false, validator: CompanyIndustry_mediumValidatorOptional })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false, validator: CompanyIndustry_minorValidatorOptional })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false, validator: CompanyLegal_representativeValidatorOptional })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false, validator: CompanyOrganization_codeValidatorOptional })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false, validator: CompanyPaid_capitalValidatorOptional })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false, validator: CompanyParent_groupValidatorOptional })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false, validator: CompanyProvinceValidatorOptional })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false, validator: CompanyRegistered_addressValidatorOptional })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false, validator: CompanyRegistered_capitalValidatorOptional })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false, validator: CompanyRegistered_emailValidatorOptional })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false, validator: CompanyRegistration_authorityValidatorOptional })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false, validator: CompanyRegistration_numberValidatorOptional })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false, validator: CompanyShareholdersValidatorOptional })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false, validator: CompanySocial_security_countValidatorOptional })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false, validator: CompanyVerified_emailValidatorOptional })
  verified_email?: string
}

export class ListCompanyItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '备用电话列表', required: false })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false })
  verified_email?: string
}

export class GetCompanyResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '备用电话列表', required: false })
  additional_phones?: string[]
  @CloverApiProperty({ description: '最近核准日期', required: false })
  approval_date?: Date
  @CloverApiProperty({ description: '主要联系电话', required: false })
  business_phone?: string
  @CloverApiProperty({ description: '经营范围', required: false })
  business_scope?: string
  @CloverApiProperty({ description: '经营状态', required: false })
  business_status?: string
  @CloverApiProperty({ description: '营业期限', required: false })
  business_term?: string
  @CloverApiProperty({ description: '城市', required: false })
  city?: string
  @CloverApiProperty({ description: '唯一公司ID', required: false })
  company_id?: string
  @CloverApiProperty({ description: '公司全称', required: false })
  company_name?: string
  @CloverApiProperty({ description: '公司规模', required: false })
  company_size?: string
  @CloverApiProperty({ description: '公司类型', required: false })
  company_type?: string
  @CloverApiProperty({ description: '发布时间', required: false })
  create_time?: Date
  @CloverApiProperty({ description: '统一社会信用代码', required: false })
  credit_code?: string
  @CloverApiProperty({ description: '实际经营地址', required: false })
  current_address?: string
  @CloverApiProperty({ description: '数据来源', required: false })
  data_source?: string
  @CloverApiProperty({ description: '区县', required: false })
  district?: string
  @CloverApiProperty({ description: '公司英文名称', required: false })
  english_name?: string
  @CloverApiProperty({ description: '成立日期', required: false })
  establishment_date?: Date
  @CloverApiProperty({ description: '曾用名列表', required: false })
  former_names?: string[]
  @CloverApiProperty({ description: '失信记录', required: false })
  has_dishonest_record?: boolean
  @CloverApiProperty({ description: '被执行记录', required: false })
  has_execution_record?: boolean
  @CloverApiProperty({ description: '导入日期', required: false })
  import_date?: Date
  @CloverApiProperty({ description: '行业大类', required: false })
  industry_category?: string
  @CloverApiProperty({ description: '行业编码', required: false })
  industry_code?: string
  @CloverApiProperty({ description: '行业中类', required: false })
  industry_major?: string
  @CloverApiProperty({ description: '行业小类', required: false })
  industry_medium?: string
  @CloverApiProperty({ description: '行业细类', required: false })
  industry_minor?: string
  @CloverApiProperty({ description: '法定代表人', required: false })
  legal_representative?: string
  @CloverApiProperty({ description: '组织机构代码', required: false })
  organization_code?: string
  @CloverApiProperty({ description: '实缴资本(万元)', required: false })
  paid_capital?: number
  @CloverApiProperty({ description: '母公司/集团', required: false })
  parent_group?: string
  @CloverApiProperty({ description: '省份', required: false })
  province?: string
  @CloverApiProperty({ description: '注册地址', required: false })
  registered_address?: string
  @CloverApiProperty({ description: '注册资本(万元)', required: false })
  registered_capital?: number
  @CloverApiProperty({ description: '注册邮箱', required: false })
  registered_email?: string
  @CloverApiProperty({ description: '登记机关', required: false })
  registration_authority?: string
  @CloverApiProperty({ description: '工商注册号', required: false })
  registration_number?: string
  @CloverApiProperty({ description: '股东列表', required: false })
  shareholders?: string[]
  @CloverApiProperty({ description: '社保缴纳人数', required: false })
  social_security_count?: number
  @CloverApiProperty({ description: '验证邮箱', required: false })
  verified_email?: string
}

export interface CompanyCombinedId {
  _id?: string
}

export class ListCompanyResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListCompanyItem] })
  _items: ListCompanyItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListCompanyResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListCompanyItem] })
  _items: AdminListCompanyItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertCompany {
}

export class RemoveCompany {
}

export class CompanyCombinedId {
}

export interface CompanyDtoType {
  item: GetCompanyResult
  create: CreateCompany
  replace: ReplaceCompany
  update: UpdateCompany
}
