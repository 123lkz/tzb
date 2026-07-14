import { Schema, model } from 'mongoose'
import { SchoolEnrollmentDtoType } from './SchoolEnrollment.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface SchoolEnrollmentModel {
  _id: ObjectIdType
  source_region: string
  school_location: string
  year: number
  category: string
  batch: string
  subject_type: string
  major: string
  average_score: number
  min_score: number
  max_score: number
  min_rank: number
  school: number
  enrollment_count: number
  school_name: string
  school_code: string
  _etag: string
  _updated: Date
  _created: Date
}

export const SchoolEnrollmentSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  source_region: {
    type: String
  },
  school_location: {
    type: String
  },
  year: {
    type: Number
  },
  category: {
    type: String
  },
  batch: {
    type: String
  },
  subject_type: {
    type: String
  },
  major: {
    type: String
  },
  average_score: {
    type: Number
  },
  min_score: {
    type: Number
  },
  max_score: {
    type: Number
  },
  min_rank: {
    type: Number
  },
  school: {
    type: Number
  },
  enrollment_count: {
    type: Number
  },
  school_name: {
    type: String
  },
  school_code: {
    index: true,
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
export const SchoolEnrollmentSchema = createRestSchema<SchoolEnrollmentModel, SchoolEnrollmentDtoType>(
  new Schema<SchoolEnrollmentModel>(SchoolEnrollmentSchemaDefine, { collection: 'xuexiaozhaosheng' })
)

export function createSchoolEnrollmentModel(schema: Schema, options?: CompileModelOptions) {
  return model<SchoolEnrollmentModel, RestModel<SchoolEnrollmentModel, SchoolEnrollmentDtoType>>(
    'SchoolEnrollment',
    schema,
    'xuexiaozhaosheng',
    options
  )
}
