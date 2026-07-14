import { Schema, model } from 'mongoose'
import { CompanyDtoType } from './Company.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema, SoftDeletePlugin } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface CompanyModel {
  _id: ObjectIdType
  company_id: string
  credit_code: string
  registration_number: string
  company_name: string
  english_name: string
  former_names: string[]
  legal_representative: string
  company_type: string
  organization_code: string
  company_size: string
  business_status: string
  industry_category: string
  industry_major: string
  industry_medium: string
  industry_minor: string
  industry_code: string
  business_scope: string
  registered_capital: number
  paid_capital: number
  establishment_date: Date
  approval_date: Date
  business_term: string
  social_security_count: number
  province: string
  city: string
  district: string
  registered_address: string
  current_address: string
  business_phone: string
  additional_phones: string[]
  parent_group: string
  shareholders: string[]
  registration_authority: string
  has_dishonest_record: boolean
  has_execution_record: boolean
  registered_email: string
  verified_email: string
  import_date: Date
  data_source: string
  create_time: Date
  _etag: string
  _updated: Date
  _created: Date
}

export const CompanySchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  company_id: {
    index: true,
    type: String
  },
  credit_code: {
    index: true,
    type: String
  },
  registration_number: {
    index: true,
    type: String
  },
  company_name: {
    index: true,
    type: String
  },
  english_name: {
    type: String
  },
  former_names: {
    type: [{
      type: String
    }]
  },
  legal_representative: {
    type: String
  },
  company_type: {
    type: String
  },
  organization_code: {
    type: String
  },
  company_size: {
    type: String
  },
  business_status: {
    type: String
  },
  industry_category: {
    index: true,
    type: String
  },
  industry_major: {
    type: String
  },
  industry_medium: {
    type: String
  },
  industry_minor: {
    type: String
  },
  industry_code: {
    type: String
  },
  business_scope: {
    type: String
  },
  registered_capital: {
    type: Number
  },
  paid_capital: {
    type: Number
  },
  establishment_date: {
    type: Date
  },
  approval_date: {
    type: Date
  },
  business_term: {
    type: String
  },
  social_security_count: {
    type: Number
  },
  province: {
    index: true,
    type: String
  },
  city: {
    index: true,
    type: String
  },
  district: {
    type: String
  },
  registered_address: {
    type: String
  },
  current_address: {
    type: String
  },
  business_phone: {
    type: String
  },
  additional_phones: {
    type: [{
      type: String
    }]
  },
  parent_group: {
    type: String
  },
  shareholders: {
    type: [{
      type: String
    }]
  },
  registration_authority: {
    type: String
  },
  has_dishonest_record: {
    type: Boolean
  },
  has_execution_record: {
    type: Boolean
  },
  registered_email: {
    type: String
  },
  verified_email: {
    type: String
  },
  import_date: {
    type: Date
  },
  data_source: {
    type: String
  },
  create_time: {
    index: true,
    type: Date
  },
  _etag: {
    type: String
  },
  _updated: {
    type: Date
  },
  _created: {
    type: Date
  }
}
export const CompanySchema = createRestSchema<CompanyModel, CompanyDtoType>(new Schema<CompanyModel>(CompanySchemaDefine, { collection: 'zhilian_companies' }))
CompanySchema.plugin(SoftDeletePlugin)

export function createCompanyModel(schema: Schema, options?: CompileModelOptions) {
  return model<CompanyModel, RestModel<CompanyModel, CompanyDtoType>>('Company', schema, 'zhilian_companies', options)
}
