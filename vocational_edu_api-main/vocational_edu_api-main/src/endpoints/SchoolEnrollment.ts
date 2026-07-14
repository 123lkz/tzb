import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'SchoolEnrollment',
  description: '学校招生',
  collectionName: 'xuexiaozhaosheng',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    source_region: {
      description: '生源地',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    school_location: {
      description: '学校所在地',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    year: {
      description: '年份',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    category: {
      description: '分类',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    batch: {
      description: '批次',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    subject_type: {
      description: '文理分科',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    major: {
      description: '专业',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    average_score: {
      description: '平均分',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    min_score: {
      description: '最低分',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    max_score: {
      description: '最高分',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    min_rank: {
      description: '录取最低位次',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    school: {
      description: '学校',
      type: 'number',
      readonly: true,
      lookup: true
    },

    enrollment_count: {
      description: '录取人数',
      type: 'number',
      readonly: true,
      lookup: true,
      validator: Joi.number().integer()
    },

    school_name: {
      description: '学校名称',
      type: 'string',
      readonly: true,
      validator: Joi.string().max(100),
      lookup: true
    },

    school_code: {
      description: '学校标识码',
      type: 'string',
      readonly: true,
      index: true,
      validator: Joi.string().max(100),
      lookup: true
    }
  },

  flags: {
    enablePaging: true
  },

  methods: {},
  plugins: {
    CheckRoles: {}
  }
})
