import { Schema, model } from 'mongoose'
import { IndustryDtoType } from './Industry.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface IndustryModel {
  _id: ObjectIdType
  code: string
  name: string
  level: number
  parent_code: string
  path: string
  description: string
  _etag: string
  _updated: Date
  _created: Date
}

export const IndustrySchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  code: {
    index: true,
    type: String
  },
  name: {
    type: String
  },
  level: {
    type: Number
  },
  parent_code: {
    type: String
  },
  path: {
    type: String
  },
  description: {
    type: String
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
export const IndustrySchema = createRestSchema<IndustryModel, IndustryDtoType>(
  new Schema<IndustryModel>(IndustrySchemaDefine, { collection: 'industry' })
)

export function createIndustryModel(schema: Schema, options?: CompileModelOptions) {
  return model<IndustryModel, RestModel<IndustryModel, IndustryDtoType>>('Industry', schema, 'industry', options)
}
