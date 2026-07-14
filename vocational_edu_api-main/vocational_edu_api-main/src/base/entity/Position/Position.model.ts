import { ObjectId, ObjectIdType, RestModel, SoftDeletePlugin, createRestSchema } from '@havenzhang/clover'
import { CompileModelOptions, Schema, SchemaDefinition, model } from 'mongoose'
import { PositionDtoType } from './Position.dto'

export interface PositionModel {
  _id: ObjectIdType
  jobName: string
  bossCert: number
  brandName: string
  jobDegree: string
  jobExperience: string
  salaryDesc: string
  cityName: string
  skills: string
  brandIndustry: string
  brandScaleName: string
  businessDistrict: string
  create_time: Date
  _etag: string
  _updated: Date
  _created: Date
}

export const PositionSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  jobName: {
    index: true,
    sparse: true,
    type: String
  },
  bossCert: {
    index: true,
    sparse: true,
    type: Number
  },
  brandName: {
    sparse: true,
    type: String
  },
  jobDegree: {
    sparse: true,
    type: String
  },
  jobExperience: {
    index: true,
    sparse: true,
    type: String
  },
  salaryDesc: {
    index: true,
    sparse: true,
    type: String
  },
  cityName: {
    type: String
  },
  skills: {
    type: String
  },
  brandIndustry: {
    type: String
  },
  brandScaleName: {
    type: String
  },
  businessDistrict: {
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
export const PositionSchema1 = createRestSchema<PositionModel, PositionDtoType>(
  new Schema<PositionModel>(PositionSchemaDefine, { collection: 'zhilian_job_raw_part1' })
)
export const PositionSchema2 = createRestSchema<PositionModel, PositionDtoType>(
  new Schema<PositionModel>(PositionSchemaDefine, { collection: 'zhilian_job_raw_part2' })
)
export const PositionSchema3 = createRestSchema<PositionModel, PositionDtoType>(
  new Schema<PositionModel>(PositionSchemaDefine, { collection: 'zhilian_job_raw_part3' })
)
export const PositionSchema4 = createRestSchema<PositionModel, PositionDtoType>(
  new Schema<PositionModel>(PositionSchemaDefine, { collection: 'zhilian_job_raw_part4' })
)

// 为所有schema添加插件
;[PositionSchema1, PositionSchema2, PositionSchema3, PositionSchema4].forEach((schema) => {
  schema.plugin(SoftDeletePlugin)
})

export function createPositionModel(schema: Schema, options?: CompileModelOptions) {
  return model<PositionModel, RestModel<PositionModel, PositionDtoType>>(
    'Position',
    schema,
    'zhilian_job_raw_part1',
    options
  )
}

export function createPositionModel1(schema: Schema, options?: CompileModelOptions) {
  return model<PositionModel, RestModel<PositionModel, PositionDtoType>>(
    'Position1',
    schema,
    'zhilian_job_raw_part1',
    options
  )
}

export function createPositionModel2(schema: Schema, options?: CompileModelOptions) {
  return model<PositionModel, RestModel<PositionModel, PositionDtoType>>(
    'Position2',
    schema,
    'zhilian_job_raw_part2',
    options
  )
}

export function createPositionModel3(schema: Schema, options?: CompileModelOptions) {
  return model<PositionModel, RestModel<PositionModel, PositionDtoType>>(
    'Position3',
    schema,
    'zhilian_job_raw_part3',
    options
  )
}

export function createPositionModel4(schema: Schema, options?: CompileModelOptions) {
  return model<PositionModel, RestModel<PositionModel, PositionDtoType>>(
    'Position4',
    schema,
    'zhilian_job_raw_part4',
    options
  )
}
