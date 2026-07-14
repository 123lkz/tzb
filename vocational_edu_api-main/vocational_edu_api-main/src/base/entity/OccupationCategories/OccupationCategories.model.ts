import { Schema, model } from 'mongoose'
import { OccupationCategoriesDtoType } from './OccupationCategories.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface OccupationCategoriesModel {
  _id: ObjectIdType
  code: string
  gbm_code: string
  name: string
  level: number
  parent_code: string
  parent_gbm_code: string
  path: string[]
  description: string
  tasks: string
  suffix: string
  _etag: string
  _updated: Date
  _created: Date
}

export const OccupationCategoriesSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  code: {
    index: true,
    type: String
  },
  gbm_code: {
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
  parent_gbm_code: {
    type: String
  },
  path: {
    type: [
      {
        type: String
      }
    ]
  },
  description: {
    type: String
  },
  tasks: {
    type: String
  },
  suffix: {
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
export const OccupationCategoriesSchema = createRestSchema<OccupationCategoriesModel, OccupationCategoriesDtoType>(
  new Schema<OccupationCategoriesModel>(OccupationCategoriesSchemaDefine, { collection: 'occupation_categories' })
)

export function createOccupationCategoriesModel(schema: Schema, options?: CompileModelOptions) {
  return model<OccupationCategoriesModel, RestModel<OccupationCategoriesModel, OccupationCategoriesDtoType>>(
    'OccupationCategories',
    schema,
    'occupation_categories',
    options
  )
}
