import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'School',
  description: '学校',
  collectionName: 'Schools',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    school: {
      description: '学校名称',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    schoolCode: {
      description: '学校代码',
      type: 'number',
      readonly: true,
      lookup: true
    },

    manager: {
      description: '主管部门',
      type: 'string',
      readonly: true,
      validator: Joi.string().allow('').max(100),
      lookup: true
    },

    location: {
      description: '城市',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100),
      lookup: true
    },

    province: {
      description: '省份',
      type: 'string',
      readonly: true,
      index: true,
      validator: Joi.string().max(100),
      lookup: true
    },

    level: {
      description: '办学层次',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100),
      lookup: true
    },

    note: {
      description: '学校性质',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100),
      lookup: true
    },

    type: {
      description: '类型',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100)
    },

    is985: {
      description: '是否为985',
      type: 'number',
      readonly: true,
      lookup: true
    },
    is211: {
      description: '是否为211',
      type: 'number',
      readonly: true,
      lookup: true
    },

    updateDate: {
      description: '更新时间',
      type: 'Date',
      readonly: true
    },

    isCenter: {
      description: '是否为中央高校',
      type: 'number',
      readonly: true,
      lookup: true
    },

    isLocal: {
      description: '是否为地方高校',
      type: 'number',
      readonly: true,
      lookup: true
    },

    isDoubleTop: {
      description: '是否为双一流',
      type: 'number',
      readonly: true,
      lookup: true
    },

    isDoubleHigh: {
      description: '是否为双高院校',
      type: 'number',
      readonly: true,
      lookup: true
    },

    openState: {
      description: '状态',
      type: 'number',
      readonly: true,
      lookup: true
    }
  },

  flags: {
    enablePaging: true
  },

  methods: {
    list: { plugins: {}, description: '获取学校列表' }
  },
  plugins: {
    CheckRoles: {}
  }
})
