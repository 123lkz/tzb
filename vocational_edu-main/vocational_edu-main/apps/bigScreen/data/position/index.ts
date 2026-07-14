// 职位信息数据 - 包含年度和月度的全口径和应届大专生数据
export interface PositionData {
  year: {
    all: YearlyPositionAllData
    college: YearlyPositionFreshGraduateData
  }
  month: {
    all: MonthlyPositionAllData
    college: MonthlyPositionFreshGraduateData
  }
}

// 年度全口径职位数据
export interface YearlyPositionAllData {
  year: string
  provinceMapData: ProvinceMapData[] // 省份地图数据
  professionRecruitmentData: ProfessionRecruitmentData[] // 招聘总人数职业排行
  industryRecruitmentData: IndustryRecruitmentData[] // 招聘总人数行业排行
  hotWordsData: HotWordsData[] // 热门职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustryData: ThreeIndustryData[] // 三大产业招聘总人数
}

// 年度应届大专生职位数据
export interface YearlyPositionFreshGraduateData {
  year: string
  provinceMapData: ProvinceMapData[] // 省份地图数据
  professionRecruitmentData: ProfessionRecruitmentData[] // 招聘总人数职业排行
  industryRecruitmentData: IndustryRecruitmentData[] // 招聘总人数行业排行
  hotWordsData: HotWordsData[] // 热门职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustryData: ThreeIndustryData[] // 三大产业招聘总人数
}

// 月度全口径职位数据
export interface MonthlyPositionAllData {
  year: string
  month: string
  provinceMapData: ProvinceMapData[] // 省份地图数据
  professionRecruitmentData: ProfessionRecruitmentData[] // 招聘总人数职业排行
  industryRecruitmentData: IndustryRecruitmentData[] // 招聘总人数行业排行
  hotWordsData: HotWordsData[] // 热门职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustryData: ThreeIndustryData[] // 三大产业招聘总人数
}

// 月度应届大专生职位数据
export interface MonthlyPositionFreshGraduateData {
  year: string
  month: string
  provinceMapData: ProvinceMapData[] // 省份地图数据
  professionRecruitmentData: ProfessionRecruitmentData[] // 招聘总人数职业排行
  industryRecruitmentData: IndustryRecruitmentData[] // 招聘总人数行业排行
  hotWordsData: HotWordsData[] // 热门职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustryData: ThreeIndustryData[] // 三大产业招聘总人数
}

// 省份地图数据
export interface ProvinceMapData {
  name: string
  value: number | string
  totalCompanies?: number
  rank: number
  positionCount?: number
  totalCompanies?: number
}

// 招聘总人数职业排行
export interface ProfessionRecruitmentData {
  name: string
  value: number
  rank: number
}

// 招聘总人数行业排行
export interface IndustryRecruitmentData {
  name: string
  value: number
  rank: number
}

// 热门职业对应专业词云图
export interface HotWordsData {
  name: string
  value: number
  professionName: string[]
}

// 招聘单位/公司规模
export interface CompanyData {
  name: string
  value: number
}

// 工作岗位经验要求
export interface ExperienceData {
  name: string
  value: number
}

// 工作岗位学历要求
export interface EducationData {
  name: string
  value: number
}

// 三大产业招聘总人数
export interface ThreeIndustryData {
  name: string
  value: number
}

// 真实数据
export const positionData: PositionData = {
  year: {
    all: {
      year: '2025',
      // 真实数据
      provinceMapData: [
        {
          name: '广东省',
          value: 1932148,
          totalCompanies: 16472,
          group: 1
        },
        {
          name: '江苏省',
          value: 1015784,
          totalCompanies: 15221,
          group: 2
        },
        {
          name: '四川省',
          value: 878809,
          totalCompanies: 8995,
          group: 3
        },
        {
          name: '北京市',
          value: 787837,
          totalCompanies: 12233,
          group: 4
        },
        {
          name: '浙江省',
          value: 777266,
          totalCompanies: 7264,
          group: 5
        },
        {
          name: '山东省',
          value: 698636,
          totalCompanies: 13927,
          group: 6
        },
        {
          name: '河南省',
          value: 632439,
          totalCompanies: 10542,
          group: 7
        },
        {
          name: '湖北省',
          value: 545633,
          totalCompanies: 4403,
          group: 8
        },
        {
          name: '湖南省',
          value: 544517,
          totalCompanies: 4037,
          group: 9
        },
        {
          name: '上海市',
          value: 476283,
          totalCompanies: 6332,
          group: 10
        },
        {
          name: '安徽省',
          value: 446579,
          totalCompanies: 4672,
          group: 11
        },
        {
          name: '河北省',
          value: 406186,
          totalCompanies: 7424,
          group: 12
        },
        {
          name: '天津市',
          value: 371880,
          totalCompanies: 4876,
          group: 13
        },
        {
          name: '陕西省',
          value: 369866,
          totalCompanies: 5057,
          group: 14
        },
        {
          name: '辽宁省',
          value: 287764,
          totalCompanies: 6358,
          group: 15
        },
        {
          name: '福建省',
          value: 283641,
          totalCompanies: 4125,
          group: 16
        },
        {
          name: '重庆市',
          value: 267226,
          totalCompanies: 2646,
          group: 17
        },
        {
          name: '山西省',
          value: 192888,
          totalCompanies: 2613,
          group: 18
        },
        {
          name: '江西省',
          value: 190230,
          totalCompanies: 1879,
          group: 19
        },
        {
          name: '吉林省',
          value: 156908,
          totalCompanies: 2697,
          group: 20
        },
        {
          name: '云南省',
          value: 154092,
          totalCompanies: 1335,
          group: 21
        },
        {
          name: '黑龙江省',
          value: 129242,
          totalCompanies: 2184,
          group: 22
        },
        {
          name: '贵州省',
          value: 127234,
          totalCompanies: 1414,
          group: 23
        },
        {
          name: '甘肃省',
          value: 117929,
          totalCompanies: 665,
          group: 24
        },
        {
          name: '广西壮族自治区',
          value: 108103,
          totalCompanies: 814,
          group: 25
        },
        {
          name: '内蒙古自治区',
          value: 89094,
          totalCompanies: 1442,
          group: 26
        },
        {
          name: '新疆维吾尔自治区',
          value: 68912,
          totalCompanies: 1193,
          group: 27
        },
        {
          name: '海南省',
          value: 41576,
          totalCompanies: 912,
          group: 28
        },
        {
          name: '宁夏回族自治区',
          value: 34354,
          totalCompanies: 319,
          group: 29
        },
        {
          name: '青海省',
          value: 31800,
          totalCompanies: 122,
          group: 30
        },
        {
          name: '西藏自治区',
          value: 7370,
          totalCompanies: 213,
          group: 31
        },
        {
          name: '香港特别行政区',
          value: 116,
          totalCompanies: 103,
          group: 32
        },
        {
          name: '台湾省',
          value: 17,
          totalCompanies: 0,
          group: 33
        },
        {
          name: '澳门特别行政区',
          value: 17,
          totalCompanies: 0,
          group: 34
        }
      ],
      // 真实数据
      professionRecruitmentData: [
        {
          name: '网约配送员',
          value: 1722721,
          group: 1
        },
        {
          name: '营销员',
          value: 1594630,
          group: 2
        },
        {
          name: '理货员',
          value: 1490752,
          group: 3
        },
        {
          name: '客户服务管理员',
          value: 1352604,
          group: 4
        },
        {
          name: '客运车辆驾驶员',
          value: 986546,
          group: 5
        },
        {
          name: '仓储管理员',
          value: 839964,
          group: 6
        },
        {
          name: '市场营销专业人员',
          value: 284842,
          group: 7
        },
        {
          name: '秘书',
          value: 218532,
          group: 8
        },
        {
          name: '互联网营销师',
          value: 206686,
          group: 9
        },
        {
          name: '道路货运汽车驾驶员',
          value: 194485,
          group: 10
        },
        {
          name: '计算机软件工程技术人员',
          value: 173696,
          group: 11
        },
        {
          name: '人力资源管理专业人员',
          value: 165098,
          group: 12
        },
        {
          name: '装卸搬运工',
          value: 159512,
          group: 13
        },
        {
          name: '企业经理',
          value: 151841,
          group: 14
        },
        {
          name: '招聘师',
          value: 147519,
          group: 15
        },
        {
          name: '通信工程技术人员',
          value: 141000,
          group: 16
        },
        {
          name: '信息系统运行维护工程技术人员',
          value: 135345,
          group: 17
        },
        {
          name: '物流服务师',
          value: 126325,
          group: 18
        },
        {
          name: '会计专业人员',
          value: 124759,
          group: 19
        },
        {
          name: '商务策划专业人员',
          value: 117508,
          group: 20
        }
      ],
      // 真实数据
      industryRecruitmentData: [
        {
          name: '技术推广服务',
          value: 7059
        },
        {
          name: '其他科技推广服务业',
          value: 5774
        },
        {
          name: '机械设备、五金产品及电子产品批发',
          value: 5167
        },
        {
          name: '咨询与调查',
          value: 5112
        },
        {
          name: '软件开发',
          value: 4227
        },
        {
          name: '组织管理服务',
          value: 3570
        },
        {
          name: '其他批发业',
          value: 3357
        },
        {
          name: '其他商务服务业',
          value: 3186
        },
        {
          name: '工业与专业设计及其他专业技术服务',
          value: 2654
        },
        {
          name: '综合零售',
          value: 2342
        },
        {
          name: '矿产品、建材及化工产品批发',
          value: 2304
        },
        {
          name: '工程和技术研究和试验发展',
          value: 2084
        },
        {
          name: '食品、饮料及烟草制品批发',
          value: 2036
        },
        {
          name: '商务服务业',
          value: 2022
        },
        {
          name: '其他信息技术服务业',
          value: 2000
        },
        {
          name: '人力资源服务',
          value: 1941
        },
        {
          name: '纺织、服装及家庭用品批发',
          value: 1784
        },
        {
          name: '零售业',
          value: 1760
        },
        {
          name: '综合管理服务',
          value: 1740
        },
        {
          name: '软件和信息技术服务业',
          value: 1708
        },
        {
          name: '医药及医疗器材批发',
          value: 1541
        },
        {
          name: '研究和试验发展',
          value: 1540
        },
        {
          name: '信息技术咨询服务',
          value: 1493
        },
        {
          name: '货摊、无店铺及其他零售业',
          value: 1483
        },
        {
          name: '其他未列明制造业',
          value: 1453
        },
        {
          name: '工程技术与设计服务',
          value: 1440
        },
        {
          name: '汽车、摩托车、零配件和燃料及其他动力销售',
          value: 1430
        },
        {
          name: '批发业',
          value: 1429
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 1414
        },
        {
          name: '运输代理业',
          value: 1252
        },
        {
          name: '法律服务',
          value: 1199
        },
        {
          name: '房地产开发经营',
          value: 1192
        },
        {
          name: '食品、饮料及烟草制品专门零售',
          value: 1181
        },
        {
          name: '道路货物运输',
          value: 1141
        },
        {
          name: '建筑装饰和装修业',
          value: 1135
        },
        {
          name: '物业管理',
          value: 1126
        },
        {
          name: '其他未列明建筑业',
          value: 1094
        },
        {
          name: '贸易经纪与代理',
          value: 1034
        },
        {
          name: '广告业',
          value: 1018
        },
        {
          name: '其他通用设备制造业',
          value: 1016
        },
        {
          name: '五金、家具及室内装饰材料专门零售',
          value: 1000
        },
        {
          name: '纺织、服装及日用品专门零售',
          value: 987
        },
        {
          name: '其他文化艺术业',
          value: 922
        },
        {
          name: '汽车零部件及配件制造',
          value: 911
        },
        {
          name: '科技推广和应用服务业',
          value: 907
        },
        {
          name: '塑料制品业',
          value: 902
        },
        {
          name: '土木工程建筑业',
          value: 897
        },
        {
          name: '家用电器及电子产品专门零售',
          value: 840
        },
        {
          name: '专业技术服务业',
          value: 783
        },
        {
          name: '人身保险',
          value: 772
        },
        {
          name: '医院',
          value: 658
        },
        {
          name: '输配电及控制设备制造',
          value: 648
        },
        {
          name: '技能培训、教育辅助及其他教育',
          value: 628
        },
        {
          name: '其他房屋建筑业',
          value: 617
        },
        {
          name: '正餐服务',
          value: 614
        },
        {
          name: '其他食品制造',
          value: 610
        },
        {
          name: '环保、邮政、社会公共服务及其他专用设备制造',
          value: 610
        },
        {
          name: '医学研究和试验发展',
          value: 603
        },
        {
          name: '其他电子设备制造',
          value: 603
        },
        {
          name: '房地产中介服务',
          value: 601
        },
        {
          name: '质检技术服务',
          value: 593
        },
        {
          name: '医药及医疗器材专门零售',
          value: 560
        },
        {
          name: '计算机、通信和其他电子设备制造业',
          value: 554
        },
        {
          name: '电子器件制造',
          value: 537
        },
        {
          name: '通用仪器仪表制造',
          value: 533
        },
        {
          name: '医疗仪器设备及器械制造',
          value: 531
        },
        {
          name: '住宅房屋建筑',
          value: 511
        },
        {
          name: '理发及美容服务',
          value: 467
        },
        {
          name: '其他仪器仪表制造业',
          value: 461
        },
        {
          name: '电子和电工机械专用设备制造',
          value: 454
        },
        {
          name: '文化、体育用品及器材批发',
          value: 454
        },
        {
          name: '专用设备制造业',
          value: 451
        },
        {
          name: '其他土木工程建筑',
          value: 445
        },
        {
          name: '金属加工机械制造',
          value: 444
        },
        {
          name: '通用设备制造业',
          value: 440
        },
        {
          name: '机械设备经营租赁',
          value: 438
        },
        {
          name: '铁路、道路、隧道和桥梁工程建筑',
          value: 435
        },
        {
          name: '电子元件及电子专用材料制造',
          value: 407
        },
        {
          name: '其他未列明服务业',
          value: 404
        },
        {
          name: '结构性金属制品制造',
          value: 392
        },
        {
          name: '互联网信息服务',
          value: 392
        },
        {
          name: '专用化学产品制造',
          value: 390
        },
        {
          name: '文化体育娱乐活动与经纪代理服务',
          value: 384
        },
        {
          name: '基层医疗卫生服务',
          value: 383
        },
        {
          name: '房屋建筑业',
          value: 380
        },
        {
          name: '其他居民服务业',
          value: 378
        },
        {
          name: '卫生材料及医药用品制造',
          value: 371
        },
        {
          name: '教育',
          value: 367
        },
        {
          name: '化工、木材、非金属加工专用设备制造',
          value: 361
        },
        {
          name: '其他电气机械及器材制造',
          value: 360
        },
        {
          name: '自然科学研究和试验发展',
          value: 359
        },
        {
          name: '电气机械和器材制造业',
          value: 350
        },
        {
          name: '通用零部件制造',
          value: 338
        },
        {
          name: '其他建筑安装业',
          value: 331
        },
        {
          name: '文化、体育用品及器材专门零售',
          value: 330
        },
        {
          name: '采矿、冶金、建筑专用设备制造',
          value: 316
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 313
        },
        {
          name: '仪器仪表制造业',
          value: 313
        },
        {
          name: '知识产权服务',
          value: 312
        },
        {
          name: '文艺创作与表演',
          value: 302
        }
      ],
      // 真实数据
      hotWordsData: [
        {
          name: '市场调查与统计分析',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '连锁经营与管理',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '药品营销',
          value: 1594630,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '航海技术',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流管理',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '铁路物流管理',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '港口物流管理',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水路运输服务',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '外轮理货',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水运业务',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1490752,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '市场营销',
          value: 1352604,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '通信运营服务',
          value: 1352604,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '市场营销',
          value: 1352604,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '烟草栽培与加工技术',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食储运与质量安全',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '农产品营销与储运',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '烟草栽培与加工',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮油储运与检验技术',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 839964,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '行政管理',
          value: 218532,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '现代文秘',
          value: 218532,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '文秘',
          value: 218532,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '行政事务助理',
          value: 218532,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '全媒体电商运营',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销与直播电商',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络直播与运营',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '直播电商服务',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 206686,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '智能网联汽车技术',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '交通运营服务',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '国际货运代理',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '智能网联汽车技术应用',
          value: 194485,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '软件工程',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机应用工程',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '软件工程技术',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机程序设计',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '软件技术',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机程序设计',
          value: 173696,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '人力资源管理',
          value: 165098,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 165098,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '劳动与社会保障',
          value: 165098,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 165098,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '港口机械操作与维护',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械操作与维护',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 159512,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '人力资源管理',
          value: 147519,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 147519,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 147519,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 147519,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '通信工程',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络工程技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信工程',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '轨道交通通信信号设备制造与维护',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '铁道通信与信息化技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '民航通信技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代移动通信技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信软件技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信工程设计与监理',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信系统运行管理',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络规划与优化技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '电信服务与管理',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业网络技术',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信运营服务',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络与信息安全',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '云计算技术应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 141000,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '电气工程及其自动化',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '电子信息工程',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '信息管理与信息系统',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '软件工程技术',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '信息安全与管理',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '智能物流技术',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '司法信息技术',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 135345,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '道路运输管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '铁路物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流技术与管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '港口物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '工程物流管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '采购与供应管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '智能物流技术',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '供应链运营',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水路运输服务',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流服务与管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流服务与管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '国际货运代理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流设施运行与维护',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水运业务',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 126325,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '大数据与财务管理',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与会计',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与财务管理',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与会计',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '会计信息管理',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '统计与会计核算',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '会计',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '财务管理',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '农村经济综合管理',
          value: 124759,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '商务英语',
          value: 117508,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '国际商务',
          value: 117508,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '商务管理',
          value: 117508,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        }
      ],
      // 真实数据
      companyData: [
        { name: '小微企业', value: 109632 },
        { name: '中型企业', value: 14352 },
        { name: '大型企业', value: 8707 }
      ],
      // 真实数据
      experienceData: [
        { name: '经验不限', value: 376414 },
        { name: '1年及无经验', value: 58867 },
        { name: '1-3年', value: 283283 },
        { name: '3-5年', value: 193399 },
        { name: '5-10年', value: 83747 },
        { name: '10年以上', value: 10284 }
      ],
      // 真实数据
      educationData: [
        { name: '学历不限', value: 285364 },
        { name: '高中及以下', value: 80590 },
        { name: '大专', value: 354479 },
        { name: '本科', value: 272424 },
        { name: '研究生及以上', value: 13137 }
      ],
      // 真实数据
      threeIndustryData: [
        { name: '第一产业', value: 999 },
        { name: '第二产业', value: 38478 },
        { name: '第三产业', value: 108829 }
      ]
    },
    college: {
      year: '2025',
      // 真实数据
      provinceMapData: [
        {
          name: '广东省',
          value: 1478153,
          totalCompanies: 7208,
          group: 1
        },
        {
          name: '江苏省',
          value: 724074,
          totalCompanies: 6398,
          group: 2
        },
        {
          name: '四川省',
          value: 699892,
          totalCompanies: 4464,
          group: 3
        },
        {
          name: '浙江省',
          value: 565825,
          totalCompanies: 3776,
          group: 4
        },
        {
          name: '山东省',
          value: 487513,
          totalCompanies: 6868,
          group: 5
        },
        {
          name: '湖南省',
          value: 467026,
          totalCompanies: 2198,
          group: 6
        },
        {
          name: '河南省',
          value: 466889,
          totalCompanies: 5915,
          group: 7
        },
        {
          name: '湖北省',
          value: 424843,
          totalCompanies: 2886,
          group: 8
        },
        {
          name: '北京市',
          value: 402401,
          totalCompanies: 4001,
          group: 9
        },
        {
          name: '河北省',
          value: 307996,
          totalCompanies: 3797,
          group: 10
        },
        {
          name: '安徽省',
          value: 296515,
          totalCompanies: 2630,
          group: 11
        },
        {
          name: '天津市',
          value: 290923,
          totalCompanies: 2465,
          group: 12
        },
        {
          name: '陕西省',
          value: 260638,
          totalCompanies: 2653,
          group: 13
        },
        {
          name: '上海市',
          value: 246132,
          totalCompanies: 2824,
          group: 14
        },
        {
          name: '辽宁省',
          value: 207438,
          totalCompanies: 2974,
          group: 15
        },
        {
          name: '福建省',
          value: 200905,
          totalCompanies: 2066,
          group: 16
        },
        {
          name: '重庆市',
          value: 190606,
          totalCompanies: 1711,
          group: 17
        },
        {
          name: '山西省',
          value: 154742,
          totalCompanies: 1699,
          group: 18
        },
        {
          name: '江西省',
          value: 152102,
          totalCompanies: 1245,
          group: 19
        },
        {
          name: '云南省',
          value: 127896,
          totalCompanies: 1011,
          group: 20
        },
        {
          name: '吉林省',
          value: 105837,
          totalCompanies: 1589,
          group: 21
        },
        {
          name: '贵州省',
          value: 104414,
          totalCompanies: 968,
          group: 22
        },
        {
          name: '甘肃省',
          value: 101803,
          totalCompanies: 614,
          group: 23
        },
        {
          name: '黑龙江省',
          value: 95321,
          totalCompanies: 1234,
          group: 24
        },
        {
          name: '广西壮族自治区',
          value: 81267,
          totalCompanies: 808,
          group: 25
        },
        {
          name: '内蒙古自治区',
          value: 64372,
          totalCompanies: 941,
          group: 26
        },
        {
          name: '新疆维吾尔自治区',
          value: 43893,
          totalCompanies: 635,
          group: 27
        },
        {
          name: '海南省',
          value: 30727,
          totalCompanies: 418,
          group: 28
        },
        {
          name: '宁夏回族自治区',
          value: 28509,
          totalCompanies: 324,
          group: 29
        },
        {
          name: '青海省',
          value: 27947,
          totalCompanies: 228,
          group: 30
        },
        {
          name: '西藏自治区',
          value: 6049,
          totalCompanies: 115,
          group: 31
        },
        {
          name: '香港特别行政区',
          value: 29,
          totalCompanies: 7,
          group: 32
        },
        {
          name: '台湾省',
          value: 15,
          totalCompanies: 1,
          group: 33
        }
      ],
      // 真实数据
      professionRecruitmentData: [
        {
          name: '网约配送员',
          value: 1718290,
          group: 1
        },
        {
          name: '理货员',
          value: 1480033,
          group: 2
        },
        {
          name: '呼叫中心服务员',
          value: 1172644,
          group: 3
        },
        {
          name: '仓储管理员',
          value: 820571,
          group: 4
        },
        {
          name: '营销员',
          value: 811644,
          group: 5
        },
        {
          name: '客运车辆驾驶员',
          value: 808163,
          group: 6
        },
        {
          name: '秘书',
          value: 266790,
          group: 7
        },
        {
          name: '互联网营销师',
          value: 182737,
          group: 8
        },
        {
          name: '装卸搬运工',
          value: 158338,
          group: 9
        },
        {
          name: '道路货运汽车驾驶员',
          value: 151527,
          group: 10
        },
        {
          name: '通信工程技术人员',
          value: 128490,
          group: 11
        },
        {
          name: '招聘师',
          value: 114357,
          group: 12
        },
        {
          name: '人力资源管理专业人员',
          value: 103945,
          group: 13
        },
        {
          name: '客户服务管理员',
          value: 96148,
          group: 14
        },
        {
          name: '快递员',
          value: 77317,
          group: 15
        },
        {
          name: '铁路列车乘务员',
          value: 70178,
          group: 16
        },
        {
          name: '商务策划专业人员',
          value: 60709,
          group: 17
        },
        {
          name: '电子商务师',
          value: 57826,
          group: 18
        },
        {
          name: '打字员',
          value: 51165,
          group: 19
        },
        {
          name: '信息系统运行维护工程技术人员',
          value: 50394,
          group: 20
        }
      ],
      // 真实数据
      industryRecruitmentData: [
        {
          name: '人力资源服务',
          value: 1688266
        },
        {
          name: '组织管理服务',
          value: 548030
        },
        {
          name: '其他信息技术服务业',
          value: 452934
        },
        {
          name: '其他商务服务业',
          value: 379347
        },
        {
          name: '道路货物运输',
          value: 375095
        },
        {
          name: '技术推广服务',
          value: 372375
        },
        {
          name: '咨询与调查',
          value: 351561
        },
        {
          name: '综合管理服务',
          value: 327526
        },
        {
          name: '软件开发',
          value: 299268
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 285566
        },
        {
          name: '其他科技推广服务业',
          value: 226658
        },
        {
          name: '商务服务业',
          value: 219019
        },
        {
          name: '信息技术咨询服务',
          value: 198862
        },
        {
          name: '餐饮配送及外卖送餐服务',
          value: 125638
        },
        {
          name: '广告业',
          value: 112196
        },
        {
          name: '其他批发业',
          value: 107160
        },
        {
          name: '机械设备经营租赁',
          value: 105153
        },
        {
          name: '软件和信息技术服务业',
          value: 95022
        },
        {
          name: '其他文化艺术业',
          value: 88044
        },
        {
          name: '互联网信息服务',
          value: 71872
        },
        {
          name: '工业与专业设计及其他专业技术服务',
          value: 61236
        },
        {
          name: '综合零售',
          value: 58864
        },
        {
          name: '文化艺术业',
          value: 55421
        },
        {
          name: '保险业',
          value: 50977
        },
        {
          name: '水上运输辅助活动',
          value: 47314
        },
        {
          name: '财产保险',
          value: 46606
        },
        {
          name: '其他互联网服务',
          value: 45872
        },
        {
          name: '公路旅客运输',
          value: 45085
        },
        {
          name: '货摊、无店铺及其他零售业',
          value: 41161
        },
        {
          name: '文化体育娱乐活动与经纪代理服务',
          value: 39989
        },
        {
          name: '运输代理业',
          value: 37194
        },
        {
          name: '食品、饮料及烟草制品批发',
          value: 36535
        },
        {
          name: '工程和技术研究和试验发展',
          value: 36420
        },
        {
          name: '房地产中介服务',
          value: 31299
        },
        {
          name: '其他居民服务业',
          value: 30849
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 30682
        },
        {
          name: '批发业',
          value: 28322
        },
        {
          name: '道路运输业',
          value: 27442
        },
        {
          name: '食品、饮料及烟草制品专门零售',
          value: 27382
        },
        {
          name: '机械设备、五金产品及电子产品批发',
          value: 24882
        },
        {
          name: '纺织、服装及日用品专门零售',
          value: 24329
        },
        {
          name: '人身保险',
          value: 23060
        },
        {
          name: '城市公共交通运输',
          value: 21013
        },
        {
          name: '汽车、摩托车、零配件和燃料及其他动力销售',
          value: 20434
        },
        {
          name: '零售业',
          value: 19437
        },
        {
          name: '创业空间服务',
          value: 16320
        },
        {
          name: '科技推广和应用服务业',
          value: 15326
        },
        {
          name: '邮政业',
          value: 15146
        },
        {
          name: '其他仓储业',
          value: 15135
        },
        {
          name: '矿产品、建材及化工产品批发',
          value: 14899
        },
        {
          name: '餐饮业',
          value: 14181
        },
        {
          name: '其他房屋建筑业',
          value: 14118
        },
        {
          name: '信息处理和存储支持服务',
          value: 13540
        },
        {
          name: '文艺创作与表演',
          value: 12833
        },
        {
          name: '法律服务',
          value: 12738
        },
        {
          name: '安全保护服务',
          value: 12309
        },
        {
          name: '电信、广播电视和卫星传输服务',
          value: 12223
        },
        {
          name: '影视节目制作',
          value: 12174
        },
        {
          name: '道路运输辅助活动',
          value: 12108
        },
        {
          name: '居民服务业',
          value: 11953
        },
        {
          name: '其他寄递服务',
          value: 10740
        },
        {
          name: '研究和试验发展',
          value: 9169
        },
        {
          name: '装卸搬运',
          value: 8641
        },
        {
          name: '其他未列明服务业',
          value: 8617
        },
        {
          name: '其他餐饮业',
          value: 8438
        },
        {
          name: '贸易经纪与代理',
          value: 8221
        },
        {
          name: '理发及美容服务',
          value: 8215
        },
        {
          name: '互联网接入及相关服务',
          value: 7994
        },
        {
          name: '纺织、服装及家庭用品批发',
          value: 7796
        },
        {
          name: '电力工程施工',
          value: 7647
        },
        {
          name: '技能培训、教育辅助及其他教育',
          value: 6770
        },
        {
          name: '其他未列明建筑业',
          value: 6711
        },
        {
          name: '食品制造业',
          value: 6565
        },
        {
          name: '保险中介服务',
          value: 6333
        },
        {
          name: '医药及医疗器材批发',
          value: 6172
        },
        {
          name: '运行维护服务',
          value: 5995
        },
        {
          name: '电子元件及电子专用材料制造',
          value: 5936
        },
        {
          name: '家用电器及电子产品专门零售',
          value: 5842
        },
        {
          name: '医院',
          value: 5834
        },
        {
          name: '农业科学研究和试验发展',
          value: 5809
        },
        {
          name: '家庭服务',
          value: 5795
        },
        {
          name: '互联网平台',
          value: 5676
        },
        {
          name: '五金、家具及室内装饰材料专门零售',
          value: 5439
        },
        {
          name: '饮料制造',
          value: 4962
        },
        {
          name: '文化、体育用品及器材批发',
          value: 4694
        },
        {
          name: '物业管理',
          value: 4619
        },
        {
          name: '货币银行服务',
          value: 4573
        },
        {
          name: '互联网和相关服务',
          value: 4376
        },
        {
          name: '会议、展览及相关服务',
          value: 4357
        },
        {
          name: '快递服务',
          value: 4222
        },
        {
          name: '其他未列明制造业',
          value: 4145
        },
        {
          name: '租赁业',
          value: 4084
        },
        {
          name: '石油、煤炭及其他燃料加工业',
          value: 4062
        },
        {
          name: '专业技术服务业',
          value: 3724
        },
        {
          name: '快餐服务',
          value: 3683
        },
        {
          name: '知识产权服务',
          value: 3639
        },
        {
          name: '电影和广播电视节目发行',
          value: 3622
        },
        {
          name: '工程技术与设计服务',
          value: 3610
        },
        {
          name: '录音制作',
          value: 3584
        },
        {
          name: '电信',
          value: 3543
        }
      ],
      // 真实数据
      hotWordsData: [
        {
          name: '航海技术',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '铁路物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '港口物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水路运输服务',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '外轮理货',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水运业务',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '市场营销',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '通信运营服务',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '市场营销',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '烟草栽培与加工技术',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食储运与质量安全',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '农产品营销与储运',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '烟草栽培与加工',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮油储运与检验技术',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '市场调查与统计分析',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '连锁经营与管理',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '药品营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '全媒体电商运营',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销与直播电商',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络直播与运营',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '直播电商服务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '港口机械操作与维护',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械操作与维护',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '智能网联汽车技术',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '交通运营服务',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '国际货运代理',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '智能网联汽车技术应用',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '行政管理',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '现代文秘',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '文秘',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '行政事务助理',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '通信工程',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络工程技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信工程',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '轨道交通通信信号设备制造与维护',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '铁道通信与信息化技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '民航通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代移动通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信软件技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信工程设计与监理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信系统运行管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络规划与优化技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '电信服务与管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业网络技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信运营服务',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络与信息安全',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '云计算技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '道路运输管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '铁路物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流技术与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '港口物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '工程物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '采购与供应管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '智能物流技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '供应链运营',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水路运输服务',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '国际货运代理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流设施运行与维护',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水运业务',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '劳动与社会保障',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '邮政快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递安全管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '邮政快递运营',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '邮政快递安全技术',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递安全管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '高速铁路运营管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道交通运营管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '餐饮智能管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路乘务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '商务英语',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '国际商务',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '商务管理',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '国际商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销与直播电商',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务数据分析与应用',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务英语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务日语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '应用外语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '计算机网络技术',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网站建设与管理',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务英语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务俄语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务助理',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        }
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 41486
        },
        {
          name: '中型企业',
          value: 4437
        },
        {
          name: '大型企业',
          value: 3031
        },
        {
          name: '其他',
          value: 7368
        }
      ],
      // 真实数据
      experienceData: [
        {
          name: '无经验',
          value: 28073
        },
        {
          name: '经验不限',
          value: 333340
        },
        {
          name: '1年以下',
          value: 15569
        }
      ],
      // 真实数据
      educationData: [
        {
          name: '学历不限',
          value: 229557
        },
        {
          name: '高中及以下',
          value: 45134
        },
        {
          name: '大专',
          value: 102291
        }
      ],
      // 真实数据
      threeIndustryData: [
        { name: '第一产业', value: 5728 },
        { name: '第二产业', value: 152447 },
        { name: '第三产业', value: 7799920 }
      ]
    }
  },
  month: {
    all: {
      year: '2025',
      month: '05',
      // 真实数据
      provinceMapData: [
        {
          name: '广东省',
          value: 666545,
          totalCompanies: 3715,
          group: 1
        },
        {
          name: '江苏省',
          value: 310288,
          totalCompanies: 6209,
          group: 2
        },
        {
          name: '四川省',
          value: 298695,
          totalCompanies: 5107,
          group: 3
        },
        {
          name: '浙江省',
          value: 296710,
          totalCompanies: 4560,
          group: 4
        },
        {
          name: '山东省',
          value: 258431,
          totalCompanies: 7836,
          group: 5
        },
        {
          name: '湖南省',
          value: 253013,
          totalCompanies: 2195,
          group: 6
        },
        {
          name: '河南省',
          value: 207555,
          totalCompanies: 4286,
          group: 7
        },
        {
          name: '湖北省',
          value: 198564,
          totalCompanies: 2419,
          group: 8
        },
        {
          name: '上海市',
          value: 156360,
          totalCompanies: 3899,
          group: 9
        },
        {
          name: '陕西省',
          value: 136556,
          totalCompanies: 3032,
          group: 10
        },
        {
          name: '北京市',
          value: 134925,
          totalCompanies: 2255,
          group: 11
        },
        {
          name: '天津市',
          value: 127144,
          totalCompanies: 2620,
          group: 12
        },
        {
          name: '河北省',
          value: 109996,
          totalCompanies: 2032,
          group: 13
        },
        {
          name: '辽宁省',
          value: 108908,
          totalCompanies: 3124,
          group: 14
        },
        {
          name: '安徽省',
          value: 107061,
          totalCompanies: 893,
          group: 15
        },
        {
          name: '山西省',
          value: 98416,
          totalCompanies: 1742,
          group: 16
        },
        {
          name: '云南省',
          value: 88155,
          totalCompanies: 1174,
          group: 17
        },
        {
          name: '江西省',
          value: 82900,
          totalCompanies: 1362,
          group: 18
        },
        {
          name: '福建省',
          value: 78266,
          totalCompanies: 1054,
          group: 19
        },
        {
          name: '重庆市',
          value: 69164,
          totalCompanies: 731,
          group: 20
        },
        {
          name: '吉林省',
          value: 59949,
          totalCompanies: 1508,
          group: 21
        },
        {
          name: '甘肃省',
          value: 59776,
          totalCompanies: 413,
          group: 22
        },
        {
          name: '贵州省',
          value: 55549,
          totalCompanies: 564,
          group: 23
        },
        {
          name: '黑龙江省',
          value: 40933,
          totalCompanies: 669,
          group: 24
        },
        {
          name: '内蒙古自治区',
          value: 39850,
          totalCompanies: 1309,
          group: 25
        },
        {
          name: '广西壮族自治区',
          value: 31661,
          totalCompanies: 539,
          group: 26
        },
        {
          name: '新疆维吾尔自治区',
          value: 26326,
          totalCompanies: 1194,
          group: 27
        },
        {
          name: '宁夏回族自治区',
          value: 20850,
          totalCompanies: 478,
          group: 28
        },
        {
          name: '青海省',
          value: 15280,
          totalCompanies: 351,
          group: 29
        },
        {
          name: '海南省',
          value: 14623,
          totalCompanies: 342,
          group: 30
        },
        {
          name: '西藏自治区',
          value: 4086,
          totalCompanies: 204,
          group: 31
        },
        {
          name: '香港特别行政区',
          value: 56,
          totalCompanies: 24,
          group: 32
        },
        {
          name: '澳门特别行政区',
          value: 2,
          totalCompanies: 2,
          group: 33
        },
        {
          name: '台湾省',
          value: 0,
          totalCompanies: 0,
          group: 34
        }
      ],
      // 真实数据
      professionRecruitmentData: [
        {
          name: '理货员',
          value: 698846,
          group: 1
        },
        {
          name: '仓储管理员',
          value: 606621,
          group: 2
        },
        {
          name: '网约配送员',
          value: 573268,
          group: 3
        },
        {
          name: '客运车辆驾驶员',
          value: 378756,
          group: 4
        },
        {
          name: '营销员',
          value: 361764,
          group: 5
        },
        {
          name: '客户服务管理员',
          value: 329426,
          group: 6
        },
        {
          name: '物流服务师',
          value: 104140,
          group: 7
        },
        {
          name: '装卸搬运工',
          value: 89564,
          group: 8
        },
        {
          name: '通信工程技术人员',
          value: 85708,
          group: 9
        },
        {
          name: '道路货运汽车驾驶员',
          value: 79066,
          group: 10
        },
        {
          name: '商务策划专业人员',
          value: 58140,
          group: 11
        },
        {
          name: '秘书',
          value: 46465,
          group: 12
        },
        {
          name: '市场营销专业人员',
          value: 44609,
          group: 13
        },
        {
          name: '铁路列车乘务员',
          value: 44394,
          group: 14
        },
        {
          name: '计算机软件工程技术人员',
          value: 43434,
          group: 15
        },
        {
          name: '人力资源管理专业人员',
          value: 41667,
          group: 16
        },
        {
          name: '互联网营销师',
          value: 38318,
          group: 17
        },
        {
          name: '信息系统运行维护工程技术人员',
          value: 34952,
          group: 18
        },
        {
          name: '会计专业人员',
          value: 32880,
          group: 19
        },
        {
          name: '招聘师',
          value: 27717,
          group: 20
        }
      ],
      // 真实数据
      industryRecruitmentData: [
        {
          name: '人力资源服务',
          value: 16043
        },
        {
          name: '技术推广服务',
          value: 9440
        },
        {
          name: '软件开发',
          value: 7295
        },
        {
          name: '组织管理服务',
          value: 7225
        },
        {
          name: '其他科技推广服务业',
          value: 7012
        },
        {
          name: '道路货物运输',
          value: 6967
        },
        {
          name: '其他商务服务业',
          value: 6936
        },
        {
          name: '其他信息技术服务业',
          value: 6932
        },
        {
          name: '咨询与调查',
          value: 6157
        },
        {
          name: '软件和信息技术服务业',
          value: 5309
        },
        {
          name: '机械设备经营租赁',
          value: 4959
        },
        {
          name: '信息技术咨询服务',
          value: 4943
        },
        {
          name: '综合管理服务',
          value: 3776
        },
        {
          name: '商务服务业',
          value: 3608
        },
        {
          name: '其他批发业',
          value: 3343
        },
        {
          name: '机械设备、五金产品及电子产品批发',
          value: 3084
        },
        {
          name: '工业与专业设计及其他专业技术服务',
          value: 2960
        },
        {
          name: '食品、饮料及烟草制品批发',
          value: 2732
        },
        {
          name: '综合零售',
          value: 2423
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 2309
        },
        {
          name: '运输代理业',
          value: 1897
        },
        {
          name: '餐饮配送及外卖送餐服务',
          value: 1703
        },
        {
          name: '财产保险',
          value: 1680
        },
        {
          name: '零售业',
          value: 1677
        },
        {
          name: '矿产品、建材及化工产品批发',
          value: 1586
        },
        {
          name: '汽车、摩托车、零配件和燃料及其他动力销售',
          value: 1505
        },
        {
          name: '批发业',
          value: 1467
        },
        {
          name: '货摊、无店铺及其他零售业',
          value: 1366
        },
        {
          name: '工程和技术研究和试验发展',
          value: 1338
        },
        {
          name: '纺织、服装及家庭用品批发',
          value: 1223
        },
        {
          name: '食品、饮料及烟草制品专门零售',
          value: 1214
        },
        {
          name: '其他未列明制造业',
          value: 1184
        },
        {
          name: '研究和试验发展',
          value: 1067
        },
        {
          name: '人身保险',
          value: 1014
        },
        {
          name: '其他居民服务业',
          value: 942
        },
        {
          name: '法律服务',
          value: 929
        },
        {
          name: '互联网信息服务',
          value: 840
        },
        {
          name: '其他文化艺术业',
          value: 805
        },
        {
          name: '房地产开发经营',
          value: 794
        },
        {
          name: '广告业',
          value: 768
        },
        {
          name: '工程技术与设计服务',
          value: 732
        },
        {
          name: '医药及医疗器材批发',
          value: 731
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 724
        },
        {
          name: '科技推广和应用服务业',
          value: 707
        },
        {
          name: '输配电及控制设备制造',
          value: 681
        },
        {
          name: '其他通用设备制造业',
          value: 679
        },
        {
          name: '汽车零部件及配件制造',
          value: 671
        },
        {
          name: '其他食品制造',
          value: 660
        },
        {
          name: '贸易经纪与代理',
          value: 633
        },
        {
          name: '城市公共交通运输',
          value: 627
        },
        {
          name: '医院',
          value: 620
        },
        {
          name: '纺织、服装及日用品专门零售',
          value: 612
        },
        {
          name: '物业管理',
          value: 601
        },
        {
          name: '其他未列明建筑业',
          value: 580
        },
        {
          name: '邮政业',
          value: 574
        },
        {
          name: '房地产中介服务',
          value: 572
        },
        {
          name: '塑料制品业',
          value: 571
        },
        {
          name: '建筑装饰和装修业',
          value: 559
        },
        {
          name: '土木工程建筑业',
          value: 542
        },
        {
          name: '保险业',
          value: 528
        },
        {
          name: '计算机、通信和其他电子设备制造业',
          value: 525
        },
        {
          name: '饮料制造',
          value: 507
        },
        {
          name: '电子器件制造',
          value: 488
        },
        {
          name: '专用设备制造业',
          value: 481
        },
        {
          name: '道路运输辅助活动',
          value: 477
        },
        {
          name: '专业技术服务业',
          value: 464
        },
        {
          name: '家用电器及电子产品专门零售',
          value: 462
        },
        {
          name: '通用仪器仪表制造',
          value: 462
        },
        {
          name: '其他仪器仪表制造业',
          value: 456
        },
        {
          name: '信息处理和存储支持服务',
          value: 448
        },
        {
          name: '道路运输业',
          value: 444
        },
        {
          name: '五金、家具及室内装饰材料专门零售',
          value: 443
        },
        {
          name: '公路旅客运输',
          value: 432
        },
        {
          name: '文化体育娱乐活动与经纪代理服务',
          value: 413
        },
        {
          name: '其他互联网服务',
          value: 398
        },
        {
          name: '其他房屋建筑业',
          value: 386
        },
        {
          name: '其他电子设备制造',
          value: 381
        },
        {
          name: '互联网接入及相关服务',
          value: 369
        },
        {
          name: '医学研究和试验发展',
          value: 368
        },
        {
          name: '互联网平台',
          value: 364
        },
        {
          name: '环保、邮政、社会公共服务及其他专用设备制造',
          value: 353
        },
        {
          name: '电子元件及电子专用材料制造',
          value: 333
        },
        {
          name: '电子和电工机械专用设备制造',
          value: 332
        },
        {
          name: '互联网和相关服务',
          value: 329
        },
        {
          name: '其他仓储业',
          value: 329
        },
        {
          name: '金属加工机械制造',
          value: 328
        },
        {
          name: '水上运输辅助活动',
          value: 328
        },
        {
          name: '医药及医疗器材专门零售',
          value: 312
        },
        {
          name: '通信设备制造',
          value: 309
        },
        {
          name: '质检技术服务',
          value: 304
        },
        {
          name: '通用设备制造业',
          value: 303
        },
        {
          name: '农副食品加工业',
          value: 302
        },
        {
          name: '电气机械和器材制造业',
          value: 301
        },
        {
          name: '仪器仪表制造业',
          value: 299
        },
        {
          name: '文艺创作与表演',
          value: 298
        },
        {
          name: '医疗仪器设备及器械制造',
          value: 295
        },
        {
          name: '方便食品制造',
          value: 291
        },
        {
          name: '调味品、发酵制品制造',
          value: 290
        },
        {
          name: '铁路、道路、隧道和桥梁工程建筑',
          value: 289
        },
        {
          name: '居民服务业',
          value: 287
        }
      ],
      // 真实数据
      hotWordsData: [
        {
          name: '航海技术',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流管理',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '铁路物流管理',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '港口物流管理',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水路运输服务',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '外轮理货',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水运业务',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 698846,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '烟草栽培与加工技术',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食储运与质量安全',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '农产品营销与储运',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '烟草栽培与加工',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮油储运与检验技术',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 606621,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '市场调查与统计分析',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '连锁经营与管理',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '药品营销',
          value: 361764,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 329426,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '通信运营服务',
          value: 329426,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '市场营销',
          value: 329426,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '道路运输管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '铁路物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流技术与管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '港口物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '工程物流管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '采购与供应管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '智能物流技术',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '供应链运营',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水路运输服务',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流服务与管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流服务与管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '国际货运代理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流设施运行与维护',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水运业务',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 104140,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '港口机械操作与维护',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械操作与维护',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 89564,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '通信工程',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络工程技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信工程',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '轨道交通通信信号设备制造与维护',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '铁道通信与信息化技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '民航通信技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代移动通信技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信软件技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信工程设计与监理',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信系统运行管理',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络规划与优化技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '电信服务与管理',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业网络技术',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信运营服务',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络与信息安全',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '云计算技术应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 85708,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '智能网联汽车技术',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '交通运营服务',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '国际货运代理',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '智能网联汽车技术应用',
          value: 79066,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '商务英语',
          value: 58140,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '国际商务',
          value: 58140,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '商务管理',
          value: 58140,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '行政管理',
          value: 46465,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '现代文秘',
          value: 46465,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '文秘',
          value: 46465,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '行政事务助理',
          value: 46465,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '高速铁路运营管理',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道交通运营管理',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路客运服务',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '餐饮智能管理',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输服务',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路乘务',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 44394,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '软件工程',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机应用工程',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '软件工程技术',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机程序设计',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '软件技术',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '计算机程序设计',
          value: 43434,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '计算机软件工程技术人员']
        },
        {
          name: '人力资源管理',
          value: 41667,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 41667,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '劳动与社会保障',
          value: 41667,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 41667,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '全媒体电商运营',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销与直播电商',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络直播与运营',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '直播电商服务',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 38318,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电气工程及其自动化',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '电子信息工程',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '信息管理与信息系统',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '软件工程技术',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '信息安全与管理',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '智能物流技术',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '司法信息技术',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 34952,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '信息系统运行维护工程技术人员']
        },
        {
          name: '大数据与财务管理',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与会计',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与财务管理',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '大数据与会计',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '会计信息管理',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '统计与会计核算',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '会计',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '财务管理',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '农村经济综合管理',
          value: 32880,
          professionName: ['专业技术人员', '经济和金融专业人员', '会计专业人员', '会计专业人员']
        },
        {
          name: '人力资源管理',
          value: 27717,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 27717,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 27717,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 27717,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        }
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 32341
        },
        {
          name: '中型企业',
          value: 5551
        },
        {
          name: '大型企业',
          value: 4006
        },
        {
          name: '其他',
          value: 5970
        }
      ],
      // 真实数据
      experienceData: [
        {
          name: '一年以下',
          value: 118941
        },
        {
          name: '1-3年',
          value: 51350
        },
        {
          name: '3-5年',
          value: 32565
        },
        {
          name: '5-10年',
          value: 13393
        },
        {
          name: '10年以上',
          value: 1636
        }
      ],
      // 真实数据
      educationData: [
        {
          name: '大专',
          value: 62763
        },
        {
          name: '学历不限',
          value: 90222
        },
        {
          name: '本科',
          value: 44864
        },
        {
          name: '高中及以下',
          value: 18115
        },
        {
          name: '研究生及以上',
          value: 1920
        }
      ],
      // 真实数据
      threeIndustryData: [
        { name: '第一产业', value: 4086 },
        { name: '第二产业', value: 142391 },
        { name: '第三产业', value: 3486366 }
      ]
    },
    college: {
      year: '2025',
      month: '05',
      // 真实数据
      provinceMapData: [
        {
          name: '广东省',
          value: 602442,
          totalCompanies: 1350,
          group: 1
        },
        {
          name: '江苏省',
          value: 270124,
          totalCompanies: 1821,
          group: 2
        },
        {
          name: '四川省',
          value: 246100,
          totalCompanies: 1709,
          group: 3
        },
        {
          name: '湖南省',
          value: 239064,
          totalCompanies: 817,
          group: 4
        },
        {
          name: '浙江省',
          value: 235445,
          totalCompanies: 1454,
          group: 5
        },
        {
          name: '山东省',
          value: 203508,
          totalCompanies: 2604,
          group: 6
        },
        {
          name: '河南省',
          value: 178751,
          totalCompanies: 1615,
          group: 7
        },
        {
          name: '湖北省',
          value: 175761,
          totalCompanies: 954,
          group: 8
        },
        {
          name: '天津市',
          value: 105057,
          totalCompanies: 822,
          group: 9
        },
        {
          name: '安徽省',
          value: 102277,
          totalCompanies: 433,
          group: 10
        },
        {
          name: '北京市',
          value: 101392,
          totalCompanies: 549,
          group: 11
        },
        {
          name: '陕西省',
          value: 101170,
          totalCompanies: 986,
          group: 12
        },
        {
          name: '河北省',
          value: 100221,
          totalCompanies: 764,
          group: 13
        },
        {
          name: '上海市',
          value: 95139,
          totalCompanies: 984,
          group: 14
        },
        {
          name: '山西省',
          value: 90829,
          totalCompanies: 677,
          group: 15
        },
        {
          name: '辽宁省',
          value: 83956,
          totalCompanies: 1067,
          group: 16
        },
        {
          name: '云南省',
          value: 79209,
          totalCompanies: 468,
          group: 17
        },
        {
          name: '江西省',
          value: 76878,
          totalCompanies: 516,
          group: 18
        },
        {
          name: '福建省',
          value: 69611,
          totalCompanies: 400,
          group: 19
        },
        {
          name: '重庆市',
          value: 62933,
          totalCompanies: 370,
          group: 20
        },
        {
          name: '甘肃省',
          value: 57331,
          totalCompanies: 182,
          group: 21
        },
        {
          name: '贵州省',
          value: 53338,
          totalCompanies: 277,
          group: 22
        },
        {
          name: '吉林省',
          value: 46664,
          totalCompanies: 619,
          group: 23
        },
        {
          name: '内蒙古自治区',
          value: 35352,
          totalCompanies: 458,
          group: 24
        },
        {
          name: '黑龙江省',
          value: 34638,
          totalCompanies: 292,
          group: 25
        },
        {
          name: '广西壮族自治区',
          value: 29548,
          totalCompanies: 249,
          group: 26
        },
        {
          name: '宁夏回族自治区',
          value: 19410,
          totalCompanies: 176,
          group: 27
        },
        {
          name: '新疆维吾尔自治区',
          value: 18611,
          totalCompanies: 271,
          group: 28
        },
        {
          name: '青海省',
          value: 14141,
          totalCompanies: 140,
          group: 29
        },
        {
          name: '海南省',
          value: 13254,
          totalCompanies: 108,
          group: 30
        },
        {
          name: '西藏自治区',
          value: 3471,
          totalCompanies: 73,
          group: 31
        },
        {
          name: '香港特别行政区',
          value: 7,
          totalCompanies: 3,
          group: 32
        },
        {
          name: '澳门特别行政区',
          value: 0,
          totalCompanies: 0,
          group: 33
        },
        {
          name: '台湾省',
          value: 0,
          totalCompanies: 0,
          group: 34
        }
      ],
      // 真实数据
      professionRecruitmentData: [
        {
          name: '理货员',
          value: 692364,
          group: 1
        },
        {
          name: '仓储管理员',
          value: 603729,
          group: 2
        },
        {
          name: '网约配送员',
          value: 571973,
          group: 3
        },
        {
          name: '客户服务管理员',
          value: 313313,
          group: 4
        },
        {
          name: '客运车辆驾驶员',
          value: 311210,
          group: 5
        },
        {
          name: '营销员',
          value: 247052,
          group: 6
        },
        {
          name: '物流服务师',
          value: 103181,
          group: 7
        },
        {
          name: '装卸搬运工',
          value: 89164,
          group: 8
        },
        {
          name: '通信工程技术人员',
          value: 84970,
          group: 9
        },
        {
          name: '道路货运汽车驾驶员',
          value: 66939,
          group: 10
        },
        {
          name: '商务策划专业人员',
          value: 44209,
          group: 11
        },
        {
          name: '铁路列车乘务员',
          value: 44206,
          group: 12
        },
        {
          name: '互联网营销师',
          value: 35212,
          group: 13
        },
        {
          name: '秘书',
          value: 35082,
          group: 14
        },
        {
          name: '人力资源管理专业人员',
          value: 33020,
          group: 15
        },
        {
          name: '打字员',
          value: 24690,
          group: 16
        },
        {
          name: '快递员',
          value: 24407,
          group: 17
        },
        {
          name: '招聘师',
          value: 22521,
          group: 18
        },
        {
          name: '市场营销专业人员',
          value: 20554,
          group: 19
        },
        {
          name: '信息系统运行维护工程技术人员',
          value: 20354,
          group: 20
        }
      ],
      // 真实数据
      industryRecruitmentData: [
        {
          name: '人力资源服务',
          value: 921212
        },
        {
          name: '其他信息技术服务业',
          value: 318780
        },
        {
          name: '组织管理服务',
          value: 208214
        },
        {
          name: '其他商务服务业',
          value: 173370
        },
        {
          name: '咨询与调查',
          value: 130446
        },
        {
          name: '道路货物运输',
          value: 129065
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 114835
        },
        {
          name: '技术推广服务',
          value: 99808
        },
        {
          name: '商务服务业',
          value: 91597
        },
        {
          name: '信息技术咨询服务',
          value: 82289
        },
        {
          name: '综合管理服务',
          value: 76503
        },
        {
          name: '其他科技推广服务业',
          value: 72566
        },
        {
          name: '软件开发',
          value: 67989
        },
        {
          name: '机械设备经营租赁',
          value: 46873
        },
        {
          name: '餐饮配送及外卖送餐服务',
          value: 43676
        },
        {
          name: '其他文化艺术业',
          value: 37650
        },
        {
          name: '水上运输辅助活动',
          value: 37641
        },
        {
          name: '广告业',
          value: 34043
        },
        {
          name: '公路旅客运输',
          value: 28420
        },
        {
          name: '综合零售',
          value: 25169
        },
        {
          name: '软件和信息技术服务业',
          value: 24348
        },
        {
          name: '工业与专业设计及其他专业技术服务',
          value: 22983
        },
        {
          name: '其他批发业',
          value: 20722
        },
        {
          name: '其他互联网服务',
          value: 16229
        },
        {
          name: '财产保险',
          value: 14882
        },
        {
          name: '邮政业',
          value: 14856
        },
        {
          name: '互联网信息服务',
          value: 14431
        },
        {
          name: '其他居民服务业',
          value: 14425
        },
        {
          name: '保险业',
          value: 12956
        },
        {
          name: '餐饮业',
          value: 12459
        },
        {
          name: '食品、饮料及烟草制品批发',
          value: 10169
        },
        {
          name: '运输代理业',
          value: 9497
        },
        {
          name: '货摊、无店铺及其他零售业',
          value: 9388
        },
        {
          name: '居民服务业',
          value: 9199
        },
        {
          name: '文化体育娱乐活动与经纪代理服务',
          value: 8727
        },
        {
          name: '道路运输业',
          value: 8434
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 8352
        },
        {
          name: '批发业',
          value: 7100
        },
        {
          name: '其他房屋建筑业',
          value: 6800
        },
        {
          name: '汽车、摩托车、零配件和燃料及其他动力销售',
          value: 6636
        },
        {
          name: '食品、饮料及烟草制品专门零售',
          value: 6585
        },
        {
          name: '工程和技术研究和试验发展',
          value: 6563
        },
        {
          name: '房地产中介服务',
          value: 6281
        },
        {
          name: '其他寄递服务',
          value: 5834
        },
        {
          name: '道路运输辅助活动',
          value: 4819
        },
        {
          name: '其他仓储业',
          value: 4498
        },
        {
          name: '城市公共交通运输',
          value: 4398
        },
        {
          name: '机械设备、五金产品及电子产品批发',
          value: 4336
        },
        {
          name: '影视节目制作',
          value: 4095
        },
        {
          name: '电子元件及电子专用材料制造',
          value: 4046
        },
        {
          name: '科技推广和应用服务业',
          value: 3914
        },
        {
          name: '医院',
          value: 3903
        },
        {
          name: '技能培训、教育辅助及其他教育',
          value: 3857
        },
        {
          name: '零售业',
          value: 3849
        },
        {
          name: '创业空间服务',
          value: 3648
        },
        {
          name: '人身保险',
          value: 3481
        },
        {
          name: '互联网平台',
          value: 3361
        },
        {
          name: '矿产品、建材及化工产品批发',
          value: 3207
        },
        {
          name: '信息处理和存储支持服务',
          value: 3205
        },
        {
          name: '研究和试验发展',
          value: 3167
        },
        {
          name: '文化艺术业',
          value: 3157
        },
        {
          name: '纺织、服装及日用品专门零售',
          value: 3115
        },
        {
          name: '互联网接入及相关服务',
          value: 3019
        },
        {
          name: '电力工程施工',
          value: 2940
        },
        {
          name: '电影和广播电视节目发行',
          value: 2590
        },
        {
          name: '电信、广播电视和卫星传输服务',
          value: 2457
        },
        {
          name: '农业科学研究和试验发展',
          value: 2388
        },
        {
          name: '文艺创作与表演',
          value: 2313
        },
        {
          name: '其他未列明服务业',
          value: 2261
        },
        {
          name: '法律服务',
          value: 2214
        },
        {
          name: '木质家具制造',
          value: 2032
        },
        {
          name: '纺织、服装及家庭用品批发',
          value: 1954
        },
        {
          name: '安全保护服务',
          value: 1925
        },
        {
          name: '运行维护服务',
          value: 1817
        },
        {
          name: '租赁业',
          value: 1750
        },
        {
          name: '家用电器及电子产品专门零售',
          value: 1712
        },
        {
          name: '装卸搬运',
          value: 1630
        },
        {
          name: '快递服务',
          value: 1406
        },
        {
          name: '提供住宿社会工作',
          value: 1241
        },
        {
          name: '输配电及控制设备制造',
          value: 1212
        },
        {
          name: '质检技术服务',
          value: 1166
        },
        {
          name: '互联网和相关服务',
          value: 1105
        },
        {
          name: '互联网数据服务',
          value: 1071
        },
        {
          name: '家用电力器具制造',
          value: 1071
        },
        {
          name: '家庭服务',
          value: 1029
        },
        {
          name: '广播、电视、电影和录音制作业',
          value: 1021
        },
        {
          name: '一般旅馆',
          value: 1015
        },
        {
          name: '理发及美容服务',
          value: 1013
        },
        {
          name: '工程技术与设计服务',
          value: 976
        },
        {
          name: '机动车、电子产品和日用产品修理业',
          value: 968
        },
        {
          name: '贸易经纪与代理',
          value: 954
        },
        {
          name: '通用仓储',
          value: 784
        },
        {
          name: '航空运输辅助活动',
          value: 779
        },
        {
          name: '保险中介服务',
          value: 767
        },
        {
          name: '电信',
          value: 724
        },
        {
          name: '科技中介服务',
          value: 676
        },
        {
          name: '铁路、道路、隧道和桥梁工程建筑',
          value: 667
        },
        {
          name: '建筑装饰和装修业',
          value: 662
        },
        {
          name: '互联网安全服务',
          value: 611
        },
        {
          name: '其他日用产品修理业',
          value: 611
        }
      ],
      // 真实数据
      hotWordsData: [
        {
          name: '航海技术',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '铁路物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '港口物流管理',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水路运输服务',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '外轮理货',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '水运业务',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '航空物流',
          value: 1480033,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '理货员']
        },
        {
          name: '市场营销',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '通信运营服务',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '市场营销',
          value: 1268926,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '商务咨询服务人员', '客户服务管理员']
        },
        {
          name: '烟草栽培与加工技术',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食储运与质量安全',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '农产品营销与储运',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '烟草栽培与加工',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮油储运与检验技术',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '粮食工程',
          value: 820571,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '仓储管理员']
        },
        {
          name: '市场调查与统计分析',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '连锁经营与管理',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '市场营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '药品营销',
          value: 782098,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员']
        },
        {
          name: '全媒体电商运营',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销与直播电商',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络直播与运营',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '市场营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '电子商务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '直播电商服务',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '网络营销',
          value: 191311,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '互联网营销师']
        },
        {
          name: '港口机械操作与维护',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械操作与维护',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '起重装卸机械操作与维修',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '港口机械智能控制',
          value: 157692,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '装卸搬运和运输代理服务人员',
            '装卸搬运工'
          ]
        },
        {
          name: '智能网联汽车技术',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '交通运营服务',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '国际货运代理',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '汽车保险理赔与评估',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '智能网联汽车技术应用',
          value: 151527,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员'
          ]
        },
        {
          name: '行政管理',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '现代文秘',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '文秘',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '行政事务助理',
          value: 149659,
          professionName: ['办事人员和有关人员', '行政办事及辅助人员', '行政事务处理人员', '秘书']
        },
        {
          name: '通信工程',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络工程技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信工程',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '轨道交通通信信号设备制造与维护',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '铁道通信与信息化技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '民航通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机网络技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '现代移动通信技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信软件技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信工程设计与监理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信系统运行管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络规划与优化技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '电信服务与管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信终端设备制造与维修',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业网络技术',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '计算机信息管理',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信网络应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '通信运营服务',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '网络与信息安全',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '云计算技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '工业互联网技术应用',
          value: 128490,
          professionName: ['专业技术人员', '工程技术人员', '信息和通信工程技术人员', '通信工程技术人员']
        },
        {
          name: '物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '道路运输管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流工程技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '铁路物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流技术与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '港口物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '工程物流管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '采购与供应管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '智能物流技术',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '供应链运营',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水路运输服务',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '冷链物流服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '国际货运代理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '物流设施运行与维护',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '现代物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '水运业务',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '航空物流',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '农产品营销与储运',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品营销',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '药品服务与管理',
          value: 118142,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '仓储物流服务人员', '物流服务师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 114357,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '人力资源服务人员', '招聘师']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '劳动与社会保障',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '人力资源管理',
          value: 103972,
          professionName: ['专业技术人员', '经济和金融专业人员', '人力资源专业人员', '人力资源管理专业人员']
        },
        {
          name: '邮政快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递安全管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '邮政快递运营',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '邮政快递安全技术',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递运营管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '快递安全管理',
          value: 77317,
          professionName: ['商业、服务业人员', '交通运输、仓储物流和邮政业服务人员', '邮政和快递服务人员', '快递员']
        },
        {
          name: '高速铁路运营管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道交通运营管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '餐饮智能管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '高速铁路乘务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁道运输管理',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '铁路客运服务',
          value: 70178,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '铁路列车乘务员'
          ]
        },
        {
          name: '商务英语',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '国际商务',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '商务管理',
          value: 60613,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '商务策划专业人员']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '国际商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销与直播电商',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务数据分析与应用',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务英语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务日语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '应用外语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '计算机网络技术',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网站建设与管理',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '跨境电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务英语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务俄语',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '商务助理',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '电子商务',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        },
        {
          name: '网络营销',
          value: 57843,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '电子商务服务人员', '电子商务师']
        }
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 11354
        },
        {
          name: '大型企业',
          value: 998
        },
        {
          name: '中型企业',
          value: 1168
        },
        {
          name: '其他',
          value: 2035
        }
      ],
      // 真实数据
      experienceData: [
        {
          name: '经验不限',
          value: 97621
        },
        {
          name: '1年以下',
          value: 3237
        },
        {
          name: '无经验',
          value: 7722
        }
      ],
      // 真实数据
      educationData: [
        {
          name: '大专',
          value: 20494
        },
        {
          name: '高中及以下',
          value: 11485
        },
        {
          name: '学历不限',
          value: 76603
        }
      ],
      // 真实数据
      threeIndustryData: [
        { name: '第一产业', value: 665 },
        { name: '第二产业', value: 31402 },
        { name: '第三产业', value: 3132982 }
      ]
    }
  }
}

export default positionData
