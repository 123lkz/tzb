import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'Industry',
  description: '标准行业',
  collectionName: 'industry',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    code: {
      description: '编码',
      type: 'string',
      readonly: true,
      index: true,
      lookup: true,
      validator: Joi.string().max(50).required()
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

    path: {
      description: '自顶向下编码路径',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(500).allow('').optional()
    },

    description: {
      description: '职责描述',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(5000).allow('').optional()
    }
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
