import { Schema, model } from 'mongoose'
import { JobOccupationMappingDtoType } from './JobOccupationMapping.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface JobOccupationMappingModel {
  _id: ObjectIdType
  position_name: string
  source: {
    name: string
    original_hierarchy: {
      level_1: string
      level_2: string
    }
  }
  standard_classification: {
    xilei: {
      primary: {
        name: string
        code: string
      }
    }
    xiaoli: {
      primary: {
        name: string
        code: string
      }
    }
    zhonglei: {
      primary: {
        name: string
        code: string
      }
    }
    dalei: {
      primary: {
        name: string
        code: string
      }
    }
  }
  version: string
  status: string
  _etag: string
  _updated: Date
  _created: Date
}

export const JobOccupationMappingSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  position_name: {
    type: String
  },
  source: {
    name: {
      type: String
    },
    original_hierarchy: {
      level_1: {
        type: String
      },
      level_2: {
        type: String
      }
    }
  },
  standard_classification: {
    xilei: {
      primary: {
        name: {
          type: String
        },
        code: {
          type: String
        }
      }
    },
    xiaoli: {
      primary: {
        name: {
          type: String
        },
        code: {
          type: String
        }
      }
    },
    zhonglei: {
      primary: {
        name: {
          type: String
        },
        code: {
          type: String
        }
      }
    },
    dalei: {
      primary: {
        name: {
          type: String
        },
        code: {
          type: String
        }
      }
    }
  },
  version: {
    type: String
  },
  status: {
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
export const JobOccupationMappingSchema = createRestSchema<JobOccupationMappingModel, JobOccupationMappingDtoType>(new Schema<JobOccupationMappingModel>(JobOccupationMappingSchemaDefine, { collection: 'job_occupation_mapping' }))

export function createJobOccupationMappingModel(schema: Schema, options?: CompileModelOptions) {
  return model<JobOccupationMappingModel, RestModel<JobOccupationMappingModel, JobOccupationMappingDtoType>>('JobOccupationMapping', schema, 'job_occupation_mapping', options)
}
