import { createEndpoint } from '@havenzhang/clover'

export default createEndpoint({
  name: 'Company',
  description: '公司',
  collectionName: 'zhilian_companies',
  schema: {
    _id: {
      description: 'ID',
      type: 'ObjectId',
      readonly: true
    },

    company_id: {
      description: '唯一公司ID',
      type: 'string',
      index: true
    },

    credit_code: {
      description: '统一社会信用代码',
      type: 'string',
      index: true
    },

    registration_number: {
      description: '工商注册号',
      type: 'string',
      index: true
    },

    company_name: {
      description: '公司全称',
      type: 'string',
      index: true,
      lookup: true
    },

    english_name: {
      description: '公司英文名称',
      type: 'string'
    },

    former_names: {
      description: '曾用名列表',
      type: 'array',
      item: {
        type: 'string'
      }
    },

    legal_representative: {
      description: '法定代表人',
      type: 'string'
    },

    company_type: {
      description: '公司类型',
      type: 'string'
    },

    organization_code: {
      description: '组织机构代码',
      type: 'string'
    },

    company_size: {
      description: '公司规模',
      type: 'string'
    },

    business_status: {
      description: '经营状态',
      type: 'string'
    },

    industry_category: {
      description: '行业大类',
      type: 'string',
      index: true
    },

    industry_major: {
      description: '行业中类',
      type: 'string'
    },

    industry_medium: {
      description: '行业小类',
      type: 'string'
    },

    industry_minor: {
      description: '行业细类',
      type: 'string'
    },

    industry_code: {
      description: '行业编码',
      type: 'string'
    },

    business_scope: {
      description: '经营范围',
      type: 'string'
    },

    registered_capital: {
      description: '注册资本(万元)',
      type: 'number'
    },

    paid_capital: {
      description: '实缴资本(万元)',
      type: 'number'
    },

    establishment_date: {
      description: '成立日期',
      type: 'Date'
    },

    approval_date: {
      description: '最近核准日期',
      type: 'Date'
    },

    business_term: {
      description: '营业期限',
      type: 'string'
    },

    social_security_count: {
      description: '社保缴纳人数',
      type: 'number'
    },

    province: {
      description: '省份',
      type: 'string',
      index: true
    },

    city: {
      description: '城市',
      type: 'string',
      index: true
    },

    district: {
      description: '区县',
      type: 'string'
    },

    registered_address: {
      description: '注册地址',
      type: 'string'
    },

    current_address: {
      description: '实际经营地址',
      type: 'string'
    },

    business_phone: {
      description: '主要联系电话',
      type: 'string'
    },

    additional_phones: {
      description: '备用电话列表',
      type: 'array',
      item: {
        type: 'string'
      }
    },

    parent_group: {
      description: '母公司/集团',
      type: 'string'
    },

    shareholders: {
      description: '股东列表',
      type: 'array',
      item: {
        type: 'string'
      }
    },

    registration_authority: {
      description: '登记机关',
      type: 'string'
    },

    has_dishonest_record: {
      description: '失信记录',
      type: 'boolean'
    },

    has_execution_record: {
      description: '被执行记录',
      type: 'boolean'
    },

    registered_email: {
      description: '注册邮箱',
      type: 'string'
    },

    verified_email: {
      description: '验证邮箱',
      type: 'string'
    },

    import_date: {
      description: '导入日期',
      type: 'Date'
    },

    data_source: {
      description: '数据来源',
      type: 'string'
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
    list: { plugins: {}, description: '获取公司列表' }
  },
  plugins: {
    CheckOwner: {},
    CheckRoles: {}
  }
})
