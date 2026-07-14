import { Schema, model } from 'mongoose'
import { SchoolDtoType } from './School.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface SchoolModel {
  _id: ObjectIdType
  school: string
  schoolCode: number
  manager: string
  location: string
  province: string
  level: string
  note: string
  type: string
  is985: number
  is211: number
  updateDate: Date
  isCenter: number
  isLocal: number
  isDoubleTop: number
  isDoubleHigh: number
  openState: number
  _etag: string
  _updated: Date
  _created: Date
}

export const SchoolSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  school: {
    type: String
  },
  schoolCode: {
    type: Number
  },
  manager: {
    type: String
  },
  location: {
    type: String
  },
  province: {
    index: true,
    type: String
  },
  level: {
    type: String
  },
  note: {
    type: String
  },
  type: {
    type: String
  },
  is985: {
    type: Number
  },
  is211: {
    type: Number
  },
  updateDate: {
    type: Date
  },
  isCenter: {
    type: Number
  },
  isLocal: {
    type: Number
  },
  isDoubleTop: {
    type: Number
  },
  isDoubleHigh: {
    type: Number
  },
  openState: {
    type: Number
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
export const SchoolSchema = createRestSchema<SchoolModel, SchoolDtoType>(
  new Schema<SchoolModel>(SchoolSchemaDefine, { collection: 'Schools' })
)

export function createSchoolModel(schema: Schema, options?: CompileModelOptions) {
  return model<SchoolModel, RestModel<SchoolModel, SchoolDtoType>>('School', schema, 'Schools', options)
}
