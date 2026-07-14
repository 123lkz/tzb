import { Schema, model } from 'mongoose'
import { JobMajorMappingDtoType } from './JobMajorMapping.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface JobMajorMappingModel {
  _id: ObjectIdType
  job_code: string
  job_name: string
  major_code: string
  major_name: string
  education_level: string
  _etag: string
  _updated: Date
  _created: Date
}

export const JobMajorMappingSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  job_code: {
    type: String
  },
  job_name: {
    type: String
  },
  major_code: {
    type: String
  },
  major_name: {
    type: String
  },
  education_level: {
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
export const JobMajorMappingSchema = createRestSchema<JobMajorMappingModel, JobMajorMappingDtoType>(new Schema<JobMajorMappingModel>(JobMajorMappingSchemaDefine, { collection: 'job_major_mapping' }))

export function createJobMajorMappingModel(schema: Schema, options?: CompileModelOptions) {
  return model<JobMajorMappingModel, RestModel<JobMajorMappingModel, JobMajorMappingDtoType>>('JobMajorMapping', schema, 'job_major_mapping', options)
}
