import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'OccupationCategories',
  description: '标准职业分类',
  collectionName: 'occupation_categories',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    code: {
      description: '标准职业编码',
      type: 'string',
      readonly: true,
      index: true,
      lookup: true,
      validator: Joi.string().max(50).required()
    },

    gbm_code: {
      description: '国标码',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(50).allow('').optional()
    },

    name: {
      description: '名称',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(200).required()
    },

    level: {
      description: '级别',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer().min(1).max(4).required()
    },

    parent_code: {
      description: '父级编码',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(50).allow('').optional()
    },

    parent_gbm_code: {
      description: '父级国标码（可选）',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(50).allow('').optional()
    },

    path: {
      description: '自顶向下编码路径',
      type: 'array',
      item: {
        type: 'string'
      },
      readonly: true,
      validator: Joi.array().items(Joi.string().max(50)).required()
    },

    description: {
      description: '职责描述',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(5000).allow('').optional()
    },

    tasks: {
      description: '主要任务',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(5000).allow('').optional()
    },

    suffix: {
      description: '后缀',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100).allow('').optional()
    }

    // subspecialties: {
    //   description: '专业细分列表',
    //   type: 'array',
    //   readonly: true,
    //   validator: Joi.array().items(Joi.string().max(200)).default([]),
    // },
  },

  flags: {
    enablePaging: true
  },

  methods: {
    list: { plugins: {}, description: '获取职业分类列表' }
  },
  plugins: {
    CheckRoles: {}
  }
})
