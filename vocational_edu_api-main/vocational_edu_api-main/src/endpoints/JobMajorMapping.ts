import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'JobMajorMapping',
  description: '职业-专业对应表',
  collectionName: 'job_major_mapping',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    job_code: {
      description: '职业编码',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    job_name: {
      description: '职业名称',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(200).required()
    },

    major_code: {
      description: '专业代码',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    major_name: {
      description: '专业名称',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(200).required()
    },

    education_level: {
      description: '学历层次',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(50).required()
    }
  },

  flags: {
    enablePaging: true
  },

  methods: {
    list: { plugins: {}, description: '获取职业对应专业列表' }
  },
  plugins: {
    CheckRoles: {},
    CheckSchoolOwner: {}
  }
})
