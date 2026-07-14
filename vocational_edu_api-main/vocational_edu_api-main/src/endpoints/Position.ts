import { createEndpoint, Joi } from '@havenzhang/clover'

export default createEndpoint({
  name: 'Position',
  description: '职位',
  collectionName: 'boss_job_raw_part',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    jobName: {
      description: '职位名称',
      type: 'string',
      index: true,
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    bossCert: {
      description: '招聘人数',
      type: 'number',
      index: true,
      sparse: true,
      lookup: true,
      validator: Joi.number().required().min(1),
      readonly: true
    },

    brandName: {
      description: '公司名称',
      type: 'string',
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    jobDegree: {
      description: '学历要求',
      type: 'string',
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    jobExperience: {
      description: '工作经验',
      type: 'string',
      index: true,
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    salaryDesc: {
      type: 'string',
      description: '薪资',
      index: true,
      sparse: true,
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    cityName: {
      description: '工作地点',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    skills: {
      description: '标签',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    brandIndustry: {
      description: '公司行业',
      type: 'string',
      lookup: true,
      validator: Joi.string().max(100).required(),
      readonly: true
    },

    brandScaleName: {
      description: '公司规模',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    businessDistrict: {
      description: '公司性质',
      type: 'string',
      readonly: true,
      lookup: true,
      validator: Joi.string().max(100).required()
    },

    create_time: {
      description: '发布时间',
      index: true,
      lookup: true,
      readonly: true,
      type: 'Date'
    }
  },

  flags: {
    softDelete: true
  },

  methods: {
    list: { plugins: {}, description: '获取职位列表' }
  },
  plugins: {
    CheckOwner: {},
    CheckRoles: {}
  }
})
