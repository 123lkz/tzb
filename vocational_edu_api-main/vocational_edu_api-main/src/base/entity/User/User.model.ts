import { Schema, model } from 'mongoose'
import { UserDtoType } from './User.dto'
import { ObjectId, ObjectIdType, RestModel, createRestSchema, SoftDeletePlugin } from '@havenzhang/clover'
import { SchemaDefinition, CompileModelOptions } from 'mongoose'

export interface UserModel {
  _id: ObjectIdType
  phone: string
  telephone: string
  email: string
  name: string
  headImage: string
  username: string
  password: string
  roles: string[]
  lastLogin: Date
  loginLogs: {
    ip: string
    time: Date
  }[]
  lastToken: string
  tokenExp: Date
  registerAt: Date
  registerIp: string
  logoffAt: Date
  passwordLogs: {
    ip: string
    time: Date
  }[]
  phoneLogs: {
    ip: string
    time: Date
  }[]
  usernameLogs: {
    ip: string
    time: Date
    name: string
  }[]
  _etag: string
  _updated: Date
  _created: Date
}

export const UserSchemaDefine: SchemaDefinition = {
  _id: {
    type: ObjectId
  },
  phone: {
    index: true,
    sparse: true,
    type: String
  },
  telephone: {
    type: String
  },
  email: {
    type: String
  },
  name: {
    type: String
  },
  headImage: {
    type: String
  },
  username: {
    type: String
  },
  password: {
    type: String
  },
  roles: {
    index: true,
    type: [{
      type: String
    }]
  },
  lastLogin: {
    type: Date
  },
  loginLogs: {
    type: [{
      ip: {
        type: String
      },
      time: {
        type: Date
      }
    }]
  },
  lastToken: {
    type: String
  },
  tokenExp: {
    type: Date
  },
  registerAt: {
    index: true,
    type: Date
  },
  registerIp: {
    type: String
  },
  logoffAt: {
    type: Date
  },
  passwordLogs: {
    type: [{
      ip: {
        type: String
      },
      time: {
        type: Date
      }
    }]
  },
  phoneLogs: {
    type: [{
      ip: {
        type: String
      },
      time: {
        type: Date
      }
    }]
  },
  usernameLogs: {
    type: [{
      ip: {
        type: String
      },
      time: {
        type: Date
      },
      name: {
        type: String
      }
    }]
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
export const UserSchema = createRestSchema<UserModel, UserDtoType>(new Schema<UserModel>(UserSchemaDefine, { collection: 'users' }))
UserSchema.plugin(SoftDeletePlugin)

export function createUserModel(schema: Schema, options?: CompileModelOptions) {
  return model<UserModel, RestModel<UserModel, UserDtoType>>('User', schema, 'users', options)
}
