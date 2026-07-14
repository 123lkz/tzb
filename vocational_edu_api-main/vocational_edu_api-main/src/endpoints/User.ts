import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'User',
  description: '用户账户',
  collectionName: 'users',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    phone: {
      description: '手机号',
      type: 'string',
      index: true,
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    telephone: {
      type: 'string',
      description: '联系电话',
      validator: Joi.string().format('text').allow('').max(100)
    },

    email: {
      type: 'string',
      description: '邮箱',
      validator: Joi.string().format('text').allow('').max(100)
    },

    name: {
      description: '姓名',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(20)
    },

    headImage: {
      description: '头像',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(500)
    },

    username: {
      description: '用户名（昵称）',
      type: 'string',
      readonly: true,
      validator: Joi.string()
        .regex(/^[a-zA-Z0-9\u4e00-\u9fff_ ]+$/)
        .max(16)
    },

    password: {
      description: '密码',
      type: 'string',
      validator: Joi.string().min(8).max(16).required(),
      hidden: true,
      readonly: true
    },

    roles: {
      description: '角色',
      type: 'array',
      item: {
        type: 'string',
        validator: Joi.string().max(50)
      },
      index: true,
      lookup: true,
      readonly: true
    },

    lastLogin: {
      description: '上次登录时间',
      readonly: true,
      type: 'Date'
    },

    loginLogs: {
      description: '登录日志',
      type: 'array',
      readonly: true,
      item: {
        type: 'object',
        schema: {
          ip: {
            description: 'IP',
            type: 'string',
            validator: Joi.string().max(50)
          },
          time: {
            description: '时间',
            type: 'Date'
          }
        }
      }
    },

    lastToken: {
      description: '最后登录 Token',
      type: 'string',
      readonly: true,
      hidden: true,
      validator: Joi.string().max(500)
    },

    tokenExp: {
      description: 'Token 失效时间',
      type: 'Date',
      readonly: true
    },

    registerAt: {
      description: '注册时间',
      index: true,
      lookup: true,
      readonly: true,
      type: 'Date'
    },

    registerIp: {
      description: '注册 IP',
      readonly: true,
      type: 'string',
      validator: Joi.string().max(50)
    },

    logoffAt: {
      description: '注销时间',
      type: 'Date',
      readonly: true
    },

    passwordLogs: {
      description: '密码修改日志',
      type: 'array',
      readonly: true,
      item: {
        type: 'object',
        schema: {
          ip: {
            description: 'IP',
            type: 'string',
            validator: Joi.string().max(50)
          },
          time: {
            description: '时间',
            type: 'Date'
          }
        }
      }
    },

    phoneLogs: {
      description: '手机号修改日志',
      type: 'array',
      readonly: true,
      item: {
        type: 'object',
        schema: {
          ip: {
            description: 'IP',
            type: 'string',
            validator: Joi.string().max(50)
          },
          time: {
            description: '时间',
            type: 'Date'
          }
        }
      }
    },

    usernameLogs: {
      description: '用户名修改日志',
      type: 'array',
      readonly: true,
      item: {
        type: 'object',
        schema: {
          ip: {
            description: 'IP',
            type: 'string',
            validator: Joi.string().max(50)
          },
          time: {
            description: '时间',
            type: 'Date'
          },
          name: {
            description: '曾用名',
            type: 'string',
            validator: Joi.string()
              .regex(/^[a-zA-Z0-9\u4e00-\u9fff_ ]+$/)
              .max(16)
          }
        }
      }
    }
  },

  flags: {
    softDelete: true
  },

  methods: {
    list: { plugins: { CheckRoles: 'supervisor' }, description: '监管：获取用户列表' },
    update: { plugins: { CheckOwner: '_id', CheckRoles: 'user' }, description: '用户：更新信息' }
  },
  plugins: {
    CheckOwner: {},
    CheckRoles: {}
  }
})
