import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'JobOccupationMapping',
  description: '职位到标准职业分类映射表',
  collectionName: 'job_occupation_mapping',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    position_name: {
      description: '职位名称',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(200).required()
    },

    // aliases: {
    //   description: '职位别名集合',
    //   type: 'array',
    //   readonly: true,
    //   validator: Joi.array().items(Joi.string().max(200)).default([]),
    // },

    source: {
      description: '来源信息',
      type: 'object',
      readonly: true,
      schema: {
        name: {
          description: '来源名称',
          type: 'string',
          validator: Joi.string().max(100)
        },
        original_hierarchy: {
          description: '来源原始层级',
          type: 'object',
          schema: {
            level_1: { description: '一级类目', type: 'string', validator: Joi.string().max(100) },
            level_2: { description: '二级类目', type: 'string', validator: Joi.string().max(100) }
          }
        }
      }
    },

    standard_classification: {
      description: '标准职业分类映射',
      type: 'object',
      readonly: true,
      schema: {
        xilei: {
          description: '细类（第四级）',
          type: 'object',
          schema: {
            primary: {
              description: '主匹配',
              type: 'object',
              schema: {
                name: { description: '名称', type: 'string', validator: Joi.string().max(200) },
                code: { description: '编码', type: 'string', validator: Joi.string().max(50) }
              }
            }
            // related: {
            //   description: '相关匹配',
            //   type: 'array',
            //   validator: Joi.array()
            //     .items(
            //       Joi.object({
            //         name: Joi.string().max(200),
            //         code: Joi.string().max(50),
            //       })
            //     )
            //     .default([]),
            // },
          }
        },
        xiaoli: {
          description: '小类（第三级）',
          type: 'object',
          schema: {
            primary: {
              description: '主匹配',
              type: 'object',
              schema: {
                name: { description: '名称', type: 'string', validator: Joi.string().max(200) },
                code: { description: '编码', type: 'string', validator: Joi.string().max(50) }
              }
            }
            // related: {
            //   description: '相关匹配',
            //   type: 'array',
            //   validator: Joi.array()
            //     .items(
            //       Joi.object({
            //         name: Joi.string().max(200),
            //         code: Joi.string().max(50),
            //       })
            //     )
            //     .default([]),
            // },
          }
        },
        zhonglei: {
          description: '中类（第二级）',
          type: 'object',
          schema: {
            primary: {
              description: '主匹配',
              type: 'object',
              schema: {
                name: { description: '名称', type: 'string', validator: Joi.string().max(200) },
                code: { description: '编码', type: 'string', validator: Joi.string().max(50) }
              }
            }
            // related: {
            //   description: '相关匹配',
            //   type: 'array',
            //   validator: Joi.array()
            //     .items(
            //       Joi.object({
            //         name: Joi.string().max(200),
            //         code: Joi.string().max(50),
            //       })
            //     )
            //     .default([]),
            // },
          }
        },
        dalei: {
          description: '大类（第一级）',
          type: 'object',
          schema: {
            primary: {
              description: '主匹配',
              type: 'object',
              schema: {
                name: { description: '名称', type: 'string', validator: Joi.string().max(200) },
                code: { description: '编码', type: 'string', validator: Joi.string().max(50) }
              }
            }
            // related: {
            //   description: '相关匹配',
            //   type: 'array',
            //   validator: Joi.array()
            //     .items(
            //       Joi.object({
            //         name: Joi.string().max(200),
            //         code: Joi.string().max(50),
            //       })
            //     )
            //     .default([]),
            // },
          }
        }
      }
    },

    version: {
      description: '版本',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(50)
    },

    status: {
      description: '状态',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(50)
    }
  },

  flags: {
    enablePaging: true
  },

  methods: {
    list: { plugins: {}, description: '获取职位到标准职业映射列表' }
  },
  plugins: {
    CheckRoles: {}
  }
})
