// 薪酬信息数据 - 包含年度和月度的全口径和应届大专生数据
export interface SalaryData {
  year: {
    all: YearlySalaryAllData
    college: YearlySalaryFreshGraduateData
  }
  month: {
    all: MonthlySalaryAllData
    college: MonthlySalaryFreshGraduateData
  }
}

// 年度全口径薪酬数据
export interface YearlySalaryAllData {
  year: string
  nationalMedianSalary: number // 全国薪资中位数
  provinceMapData: SalaryProvinceMapData[] // 薪酬省份地图数据
  professionSalaryData: ProfessionSalaryData[] // 薪资中位数职业排行
  industrySalaryData: IndustrySalaryData[] // 薪资中位数行业排行
  highSalaryWordsData: HighSalaryWordsData[] // 高薪职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustrySalaryData: ThreeIndustrySalaryData[] // 三大产业薪资中位数
}

// 年度应届大专生薪酬数据
export interface YearlySalaryFreshGraduateData {
  year: string
  nationalMedianSalary: number // 全国薪资中位数
  provinceMapData: SalaryProvinceMapData[] // 薪酬省份地图数据
  professionSalaryData: ProfessionSalaryData[] // 薪资中位数职业排行
  industrySalaryData: IndustrySalaryData[] // 薪资中位数行业排行
  highSalaryWordsData: HighSalaryWordsData[] // 高薪职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustrySalaryData: ThreeIndustrySalaryData[] // 三大产业薪资中位数
}

// 月度全口径薪酬数据
export interface MonthlySalaryAllData {
  year: string
  month: string
  nationalMedianSalary: number // 全国薪资中位数
  provinceMapData: SalaryProvinceMapData[] // 薪酬省份地图数据
  professionSalaryData: ProfessionSalaryData[] // 薪资中位数职业排行
  industrySalaryData: IndustrySalaryData[] // 薪资中位数行业排行
  highSalaryWordsData: HighSalaryWordsData[] // 高薪职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustrySalaryData: ThreeIndustrySalaryData[] // 三大产业薪资中位数
}

// 月度应届大专生薪酬数据
export interface MonthlySalaryFreshGraduateData {
  year: string
  month: string
  nationalMedianSalary: number // 全国薪资中位数
  provinceMapData: SalaryProvinceMapData[] // 薪酬省份地图数据
  professionSalaryData: ProfessionSalaryData[] // 薪资中位数职业排行
  industrySalaryData: IndustrySalaryData[] // 薪资中位数行业排行
  highSalaryWordsData: HighSalaryWordsData[] // 高薪职业对应专业词云图
  companyData: CompanyData[] // 招聘单位/公司规模
  experienceData: ExperienceData[] // 工作岗位经验要求
  educationData: EducationData[] // 工作岗位学历要求
  threeIndustrySalaryData: ThreeIndustrySalaryData[] // 三大产业薪资中位数
}

// 薪酬省份地图数据
export interface SalaryProvinceMapData {
  name: string
  value: number // 薪资中位数
  group: number
}

// 薪资中位数职业排行
export interface ProfessionSalaryData {
  name: string
  value: number // 薪资中位数
  group: number
}

// 薪资中位数行业排行
export interface IndustrySalaryData {
  name: string
  value: number // 薪资中位数
}

// 高薪职业对应专业词云图
export interface HighSalaryWordsData {
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

// 三大产业薪资中位数
export interface ThreeIndustrySalaryData {
  name: string
  value: number
}

export const salaryData: SalaryData = {
  year: {
    all: {
      year: '2025',
      // 真实数据
      nationalMedianSalary: 9000,
      // 真实数据
      provinceMapData: [
        {
          name: '香港特别行政区',
          value: 22500.0,
        },
        {
          name: '澳门特别行政区',
          value: 12500.0,
        },
        {
          name: '北京市',
          value: 11500.0,
        },
        {
          name: '上海市',
          value: 11500.0,
        },
        {
          name: '台湾省',
          value: 10249.75,
        },
        {
          name: '广东省',
          value: 9500.0,
        },
        {
          name: '浙江省',
          value: 9500.0,
        },
        {
          name: '安徽省',
          value: 9000.0,
        },
        {
          name: '重庆市',
          value: 9000.0,
        },
        {
          name: '福建省',
          value: 9000.0,
        },
        {
          name: '湖北省',
          value: 9000.0,
        },
        {
          name: '湖南省',
          value: 9000.0,
        },
        {
          name: '江苏省',
          value: 9000.0,
        },
        {
          name: '四川省',
          value: 8500.0,
        },
        {
          name: '西藏自治区',
          value: 8500.0,
        },
        {
          name: '江西省',
          value: 8000.0,
        },
        {
          name: '河南省',
          value: 8000.0,
        },
        {
          name: '山东省',
          value: 8000.0,
        },
        {
          name: '陕西省',
          value: 8000.0,
        },
        {
          name: '天津市',
          value: 8000.0,
        },
        {
          name: '新疆维吾尔自治区',
          value: 8000.0,
        },
        {
          name: '甘肃省',
          value: 7500.0,
        },
        {
          name: '广西壮族自治区',
          value: 7500.0,
        },
        {
          name: '贵州省',
          value: 7500.0,
        },
        {
          name: '海南省',
          value: 7500.0,
        },
        {
          name: '河北省',
          value: 7500.0,
        },
        {
          name: '内蒙古自治区',
          value: 7500.0,
        },
        {
          name: '宁夏回族自治区',
          value: 7500.0,
        },
        {
          name: '云南省',
          value: 7500.0,
        },
        {
          name: '青海省',
          value: 7479.5,
        },
        {
          name: '黑龙江省',
          value: 7000.0,
        },
        {
          name: '吉林省',
          value: 7000.0,
        },
        {
          name: '辽宁省',
          value: 7000.0,
        },
        {
          name: '山西省',
          value: 7000.0,
        },
      ],
      // 真实数据
      professionSalaryData: [
        {
          name: '化工设计工程技术人员',
          value: 28750,
          group: 1,
        },
        {
          name: '战略规划与管理工程技术人员',
          value: 23750,
          group: 2,
        },
        {
          name: '皮肤科医师',
          value: 22500,
          group: 3,
        },
        {
          name: '民航机场工程技术人员',
          value: 22000,
          group: 4,
        },
        {
          name: '管理学研究人员',
          value: 21500,
          group: 5,
        },
        {
          name: '机器人工程技术人员',
          value: 20500,
          group: 6,
        },
        {
          name: '人工智能工程技术人员',
          value: 18000,
          group: 7,
        },
        {
          name: '外科医师',
          value: 17750,
          group: 8,
        },
        {
          name: '事业单位负责人',
          value: 17500,
          group: 9,
        },
        {
          name: '重症医学科医师',
          value: 17500,
          group: 10,
        },
        {
          name: '口腔科医师',
          value: 17500,
          group: 11,
        },
        {
          name: '空调器制造工',
          value: 17250,
          group: 12,
        },
        {
          name: '雷达导航工程技术人员',
          value: 17000,
          group: 13,
        },
        {
          name: '城市管理网格员',
          value: 16250,
          group: 14,
        },
        {
          name: '安全评价工程技术人员',
          value: 16000,
          group: 15,
        },
        {
          name: '精算专业人员',
          value: 15500,
          group: 16,
        },
        {
          name: '证券保荐承销专业人员',
          value: 15500,
          group: 17,
        },
        {
          name: '数学研究人员',
          value: 15500,
          group: 18,
        },
        {
          name: '嵌入式系统设计工程技术人员',
          value: 15000,
          group: 19,
        },
        {
          name: '计算机硬件工程技术人员',
          value: 15000,
          group: 20,
        },
      ],
      // 真实数据
      industrySalaryData: [
        {
          name: '公开募集证券投资基金',
          value: 22500,
        },
        {
          name: '广播电视集成播控',
          value: 17750,
        },
        {
          name: '保险资产管理',
          value: 15500,
        },
        {
          name: '非公开募集证券投资基金',
          value: 15000,
        },
        {
          name: '汽车用发动机制造',
          value: 15000,
        },
        {
          name: '其他烟草制品制造',
          value: 15000,
        },
        {
          name: '狩猎和捕捉动物',
          value: 14500,
        },
        {
          name: '草种植及割草',
          value: 13500,
        },
        {
          name: '集成电路设计',
          value: 13000,
        },
        {
          name: '资本市场服务',
          value: 12500,
        },
        {
          name: '雷达及配套设备制造',
          value: 12500,
        },
        {
          name: '建筑业',
          value: 12500,
        },
        {
          name: '汽车整车制造',
          value: 12000,
        },
        {
          name: '电子和电工机械专用设备制造',
          value: 12000,
        },
        {
          name: '木材加工和木、竹、藤、棕、草制品业',
          value: 12000,
        },
        {
          name: '电池制造',
          value: 12000,
        },
        {
          name: '渔业专业及辅助性活动',
          value: 12000,
        },
        {
          name: '其他采矿业',
          value: 12000,
        },
        {
          name: '水的生产和供应业',
          value: 12000,
        },
        {
          name: '石油开采',
          value: 12000,
        },
        {
          name: '土地登记代理服务',
          value: 12000,
        },
        {
          name: '其他电子设备制造',
          value: 11500,
        },
        {
          name: '计算机、通信和其他电子设备制造业',
          value: 11500,
        },
        {
          name: '生物药品制品制造',
          value: 11500,
        },
        {
          name: '竹、藤家具制造',
          value: 11500,
        },
        {
          name: '防洪除涝设施管理',
          value: 11500,
        },
        {
          name: '其他煤炭采选',
          value: 11500,
        },
        {
          name: '纸浆制造',
          value: 11500,
        },
        {
          name: '土地调查评估服务',
          value: 11500,
        },
        {
          name: '气象服务',
          value: 11250,
        },
        {
          name: '电视',
          value: 11250,
        },
        {
          name: '海底管道运输',
          value: 11250,
        },
        {
          name: '电子器件制造',
          value: 11000,
        },
        {
          name: '其他保险活动',
          value: 11000,
        },
        {
          name: '化学药品制剂制造',
          value: 11000,
        },
        {
          name: '电力、热力生产和供应业',
          value: 11000,
        },
        {
          name: '助动车制造',
          value: 11000,
        },
        {
          name: '其他仪器仪表制造业',
          value: 10500,
        },
        {
          name: '仪器仪表制造业',
          value: 10500,
        },
        {
          name: '污水处理及其再生利用',
          value: 10500,
        },
        {
          name: '证券市场服务',
          value: 10500,
        },
        {
          name: '机械设备经营租赁',
          value: 10500,
        },
        {
          name: '货币金融服务',
          value: 10500,
        },
        {
          name: '货币银行服务',
          value: 10500,
        },
        {
          name: '金融业',
          value: 10500,
        },
        {
          name: '其他金融业',
          value: 10500,
        },
        {
          name: '光学仪器制造',
          value: 10500,
        },
        {
          name: '计算机制造',
          value: 10500,
        },
        {
          name: '专用设备制造业',
          value: 10500,
        },
        {
          name: '铁路、船舶、航空航天和其他运输设备制造业',
          value: 10500,
        },
        {
          name: '皮革制品制造',
          value: 10500,
        },
        {
          name: '钟表与计时仪器制造',
          value: 10500,
        },
        {
          name: '电车制造',
          value: 10500,
        },
        {
          name: '乐器制造',
          value: 10500,
        },
        {
          name: '常用有色金属矿采选',
          value: 10250,
        },
        {
          name: '文体设备和用品出租',
          value: 10250,
        },
        {
          name: '酒的制造',
          value: 10250,
        },
        {
          name: '搪瓷制品制造',
          value: 10250,
        },
        {
          name: '数字内容服务',
          value: 10000,
        },
        {
          name: '汽车零部件及配件制造',
          value: 10000,
        },
        {
          name: '其他未列明制造业',
          value: 10000,
        },
        {
          name: '保险业',
          value: 10000,
        },
        {
          name: '人身保险',
          value: 10000,
        },
        {
          name: '其他住宿业',
          value: 10000,
        },
        {
          name: '通用仪器仪表制造',
          value: 10000,
        },
        {
          name: '房地产中介服务',
          value: 10000,
        },
        {
          name: '家具制造业',
          value: 10000,
        },
        {
          name: '铁路运输设备制造',
          value: 10000,
        },
        {
          name: '非货币银行服务',
          value: 10000,
        },
        {
          name: '其他水利管理业',
          value: 10000,
        },
        {
          name: '餐饮业',
          value: 10000,
        },
        {
          name: '航空、航天器及设备制造',
          value: 10000,
        },
        {
          name: '智能消费设备制造',
          value: 10000,
        },
        {
          name: '生态保护',
          value: 10000,
        },
        {
          name: '纤维素纤维原料及纤维制造',
          value: 10000,
        },
        {
          name: '潜水救捞及其他未列明运输设备制造',
          value: 10000,
        },
        {
          name: '炼铁',
          value: 10000,
        },
        {
          name: '铁矿采选',
          value: 10000,
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 10000,
        },
        {
          name: '婚姻服务',
          value: 10000,
        },
        {
          name: '船舶及相关装置制造',
          value: 10000,
        },
        {
          name: '常用有色金属冶炼',
          value: 10000,
        },
        {
          name: '节能环保工程施工',
          value: 10000,
        },
        {
          name: '水上运输业',
          value: 10000,
        },
        {
          name: '黑色金属矿采选业',
          value: 10000,
        },
        {
          name: '贵金属矿采选',
          value: 10000,
        },
        {
          name: '其他科技推广服务业',
          value: 9500,
        },
        {
          name: '其他信息技术服务业',
          value: 9500,
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 9500,
        },
        {
          name: '输配电及控制设备制造',
          value: 9500,
        },
        {
          name: '互联网和相关服务',
          value: 9500,
        },
        {
          name: '医疗仪器设备及器械制造',
          value: 9500,
        },
        {
          name: '汽车制造业',
          value: 9500,
        },
        {
          name: '专用仪器仪表制造',
          value: 9500,
        },
        {
          name: '医学研究和试验发展',
          value: 9500,
        },
        {
          name: '生态保护和环境治理业',
          value: 9500,
        },
        {
          name: '电气机械和器材制造业',
          value: 9500,
        },
        {
          name: '通用设备制造业',
          value: 9500,
        },
        {
          name: '电力生产',
          value: 9500,
        },
      ],
      // 真实数据
      highSalaryWordsData: [
        {
          name: '应用化学',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化学工程与工艺',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '应用化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工智能制造工程技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工安全技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '应用化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '石油炼制技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '精细化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '石油化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '煤化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '高分子合成技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '海洋化工技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工智能制造技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工装备技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工自动化技术',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工机械维修',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工工艺',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '精细化工',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '生物化工',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '高分子材料加工',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '磷化工',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '化工安全管理',
          value: 28750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '化工工程技术人员',
            '化工设计工程技术人员',
          ],
        },
        {
          name: '城乡规划',
          value: 23750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '管理(工业)工程技术人员',
            '战略规划与管理工程技术人员',
          ],
        },
        {
          name: '城乡规划',
          value: 23750,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '管理(工业)工程技术人员',
            '战略规划与管理工程技术人员',
          ],
        },
        {
          name: '智慧机场运行与管理',
          value: 22000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '民航机场工程技术人员',
          ],
        },
        {
          name: '机场电工技术',
          value: 22000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '民航机场工程技术人员',
          ],
        },
        {
          name: '机场运行服务与管理',
          value: 22000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '民航机场工程技术人员',
          ],
        },
        {
          name: '机场场务技术与管理',
          value: 22000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '民航机场工程技术人员',
          ],
        },
        {
          name: '经济统计学',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '地质学',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '信息管理与信息系统',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '工程管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '财务管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '人力资源管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '公共事业管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '劳动与社会保障',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '土地资源管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '工业工程',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '企业数字化管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '人力资源管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '工商企业管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '工商企业管理',
          value: 21500,
          professionName: ['专业技术人员', '科学研究人员', '管理学研究人员', '管理学研究人员'],
        },
        {
          name: '机械电子工程技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能控制技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机器人技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '市场营销',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能制造技术应用',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人应用与维护',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '服务机器人应用与维护',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机械设计与制造',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机械制造及自动化',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机电设备技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能机电技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能控制技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能机器人技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '船舶智能焊接技术',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能制造技术应用',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能装备安装与调试',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能装备运行与维护',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人应用与维护',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '服务机器人应用与维护',
          value: 20500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '电子信息工程技术',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能工程技术',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '智能产品开发与应用',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 18000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '口腔医学',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '口腔医学技术',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '口腔医学技术',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '口腔医学',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '口腔医学技术',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '口腔义齿制造',
          value: 17500,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '口腔科医师'],
        },
        {
          name: '导航工程技术',
          value: 17000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '导航与位置服务',
          value: 17000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '民航通信技术',
          value: 17000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '安全工程技术',
          value: 16000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '安全工程技术人员',
            '安全评价工程技术人员',
          ],
        },
        {
          name: '安全技术与管理',
          value: 16000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '安全工程技术人员',
            '安全评价工程技术人员',
          ],
        },
        {
          name: '工程安全评价与监理',
          value: 16000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '安全工程技术人员',
            '安全评价工程技术人员',
          ],
        },
        {
          name: '工程安全评价与管理',
          value: 16000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '安全工程技术人员',
            '安全评价工程技术人员',
          ],
        },
        {
          name: '金融管理',
          value: 15500,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券保荐承销专业人员',
          ],
        },
        {
          name: '证券实务',
          value: 15500,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券保荐承销专业人员',
          ],
        },
        {
          name: '数学与应用数学',
          value: 15500,
          professionName: [
            '专业技术人员',
            '科学研究人员',
            '自然科学和地球科学研究人员',
            '数学研究人员',
          ],
        },
        {
          name: '信息与计算科学',
          value: 15500,
          professionName: [
            '专业技术人员',
            '科学研究人员',
            '自然科学和地球科学研究人员',
            '数学研究人员',
          ],
        },
        {
          name: '小学数学教育',
          value: 15500,
          professionName: [
            '专业技术人员',
            '科学研究人员',
            '自然科学和地球科学研究人员',
            '数学研究人员',
          ],
        },
        {
          name: '自动化',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '机械电子工程技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '电气工程及自动化',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '自动化技术与应用',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '嵌入式技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '电气自动化技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '工业过程自动化技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '化工自动化技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '智能产品开发与应用',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '嵌入式技术应用',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '微电子科学与工程',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '柔性电子技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路工程技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术应用',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '微电子技术',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术应用',
          value: 15000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '电信服务与管理',
          value: 15000,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '信息通信网络运行管理人员',
            '数字化解决方案设计师',
          ],
        },
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 109632,
        },
        {
          name: '中型企业',
          value: 14352,
        },
        {
          name: '大型企业',
          value: 8707,
        },
      ],
      // 真实数据
      experienceData: [
        {
          name: '经验不限',
          value: 376414,
        },
        {
          name: '1年及无经验',
          value: 58867,
        },
        {
          name: '1-3年',
          value: 283283,
        },
        {
          name: '3-5年',
          value: 193399,
        },
        {
          name: '5-10年',
          value: 83747,
        },
        {
          name: '10年以上',
          value: 10284,
        },
      ],
      // 真实数据
      educationData: [
        {
          name: '学历不限',
          value: 285364,
        },
        {
          name: '高中及以下',
          value: 80590,
        },
        {
          name: '大专',
          value: 354479,
        },
        {
          name: '本科',
          value: 272424,
        },
        {
          name: '研究生及以上',
          value: 13137,
        },
      ],
      // 真实数据
      threeIndustrySalaryData: [
        { name: '第一产业', value: 7500 },
        { name: '第二产业', value: 9000 },
        { name: '第三产业', value: 8500 },
      ],
    },
    college: {
      year: '2025',
      nationalMedianSalary: 9000,
      // 真实数据
      provinceMapData: [
        {
          name: '香港特别行政区',
          value: 14000,
        },
        {
          name: '上海市',
          value: 10500,
        },
        {
          name: '北京市',
          value: 10000,
        },
        {
          name: '浙江省',
          value: 9000,
        },
        {
          name: '广东省',
          value: 8500,
        },
        {
          name: '重庆市',
          value: 8000,
        },
        {
          name: '福建省',
          value: 8000,
        },
        {
          name: '湖北省',
          value: 8000,
        },
        {
          name: '湖南省',
          value: 8000,
        },
        {
          name: '江苏省',
          value: 8000,
        },
        {
          name: '天津市',
          value: 8000,
        },
        {
          name: '安徽省',
          value: 7500,
        },
        {
          name: '江西省',
          value: 7500,
        },
        {
          name: '贵州省',
          value: 7500,
        },
        {
          name: '河南省',
          value: 7500,
        },
        {
          name: '山东省',
          value: 7500,
        },
        {
          name: '陕西省',
          value: 7500,
        },
        {
          name: '四川省',
          value: 7500,
        },
        {
          name: '云南省',
          value: 7500,
        },
        {
          name: '甘肃省',
          value: 7000,
        },
        {
          name: '海南省',
          value: 7000,
        },
        {
          name: '宁夏回族自治区',
          value: 7000,
        },
        {
          name: '山西省',
          value: 7000,
        },
        {
          name: '新疆维吾尔自治区',
          value: 7000,
        },
        {
          name: '吉林省',
          value: 6863,
        },
        {
          name: '广西壮族自治区',
          value: 6500,
        },
        {
          name: '河北省',
          value: 6500,
        },
        {
          name: '黑龙江省',
          value: 6500,
        },
        {
          name: '辽宁省',
          value: 6500,
        },
        {
          name: '内蒙古自治区',
          value: 6500,
        },
        {
          name: '青海省',
          value: 6500,
        },
        {
          name: '西藏自治区',
          value: 6500,
        },
        {
          name: '台湾省',
          value: 5999,
        },
      ],
      // 真实数据
      professionSalaryData: [
        {
          name: '铁道运输工程技术人员',
          value: 35000,
          group: 1,
        },
        {
          name: '皮肤科医师',
          value: 31750,
          group: 2,
        },
        {
          name: '外科医师',
          value: 25000,
          group: 3,
        },
        {
          name: '银行国际业务专业人员',
          value: 21750,
          group: 4,
        },
        {
          name: '标准化工程技术人员',
          value: 16500,
          group: 5,
        },
        {
          name: '中医内科医师',
          value: 15000,
          group: 6,
        },
        {
          name: '全科医师',
          value: 15000,
          group: 7,
        },
        {
          name: '保健按摩师',
          value: 15000,
          group: 8,
        },
        {
          name: '船舶修理工',
          value: 13750,
          group: 9,
        },
        {
          name: '企业经理',
          value: 13500,
          group: 10,
        },
        {
          name: '水利水电建筑工程技术人员',
          value: 13000,
          group: 11,
        },
        {
          name: '证券交易专业人员',
          value: 12000,
          group: 12,
        },
        {
          name: '金融产品销售专业人员',
          value: 12000,
          group: 13,
        },
        {
          name: '二手车经纪人',
          value: 12000,
          group: 14,
        },
        {
          name: '其他住宿和餐饮服务人员',
          value: 12000,
          group: 15,
        },
        {
          name: '甲板部技术人员',
          value: 11500,
          group: 16,
        },
        {
          name: '信贷审核专业人员',
          value: 11500,
          group: 17,
        },
        {
          name: '焊工',
          value: 11500,
          group: 18,
        },
        {
          name: '模特',
          value: 11500,
          group: 19,
        },
        {
          name: '轨道交通列车司机',
          value: 11500,
          group: 20,
        },
      ],
      // 真实数据
      industrySalaryData: [
        {
          name: '保险资产管理',
          value: 18000,
        },
        {
          name: '雷达及配套设备制造',
          value: 16500,
        },
        {
          name: '电车制造',
          value: 15000,
        },
        {
          name: '租赁和商务服务业',
          value: 14250,
        },
        {
          name: '污水处理及其再生利用',
          value: 13500,
        },
        {
          name: '海底管道运输',
          value: 13500,
        },
        {
          name: '文体设备和用品出租',
          value: 12000,
        },
        {
          name: '其他土地管理服务',
          value: 12000,
        },
        {
          name: '其他采矿业',
          value: 12000,
        },
        {
          name: '水上旅客运输',
          value: 12000,
        },
        {
          name: '狩猎和捕捉动物',
          value: 11750,
        },
        {
          name: '货币金融服务',
          value: 11500,
        },
        {
          name: '电视',
          value: 11500,
        },
        {
          name: '其他畜牧业',
          value: 11500,
        },
        {
          name: '电影放映',
          value: 11500,
        },
        {
          name: '房地产中介服务',
          value: 10500,
        },
        {
          name: '其他保险活动',
          value: 10500,
        },
        {
          name: '酒的制造',
          value: 10500,
        },
        {
          name: '机械设备经营租赁',
          value: 10500,
        },
        {
          name: '铁路、船舶、航空航天和其他运输设备制造业',
          value: 10500,
        },
        {
          name: '货币银行服务',
          value: 10500,
        },
        {
          name: '核辐射加工',
          value: 10500,
        },
        {
          name: '水上运输辅助活动',
          value: 10500,
        },
        {
          name: '土地登记代理服务',
          value: 10500,
        },
        {
          name: '城市公园管理',
          value: 10500,
        },
        {
          name: '水的生产和供应业',
          value: 10500,
        },
        {
          name: '广播电视集成播控',
          value: 10500,
        },
        {
          name: '炼铁',
          value: 10000,
        },
        {
          name: '兽用药品制造',
          value: 10000,
        },
        {
          name: '电力工程施工',
          value: 10000,
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 10000,
        },
        {
          name: '水上运输业',
          value: 10000,
        },
        {
          name: '皮革制品制造',
          value: 10000,
        },
        {
          name: '餐饮业',
          value: 10000,
        },
        {
          name: '道路运输辅助活动',
          value: 9500,
        },
        {
          name: '快递服务',
          value: 9500,
        },
        {
          name: '其他仓储业',
          value: 9500,
        },
        {
          name: '居民服务业',
          value: 9500,
        },
        {
          name: '道路运输业',
          value: 9500,
        },
        {
          name: '租赁业',
          value: 9500,
        },
        {
          name: '金属制品修理',
          value: 9500,
        },
        {
          name: '中药材种植',
          value: 9500,
        },
        {
          name: '一般旅馆',
          value: 9250,
        },
        {
          name: '铁路货物运输',
          value: 9250,
        },
        {
          name: '信息系统集成和物联网技术服务',
          value: 9000,
        },
        {
          name: '泵、阀门、压缩机及类似机械制造',
          value: 9000,
        },
        {
          name: '保险业',
          value: 9000,
        },
        {
          name: '人身保险',
          value: 9000,
        },
        {
          name: '住宅房屋建筑',
          value: 9000,
        },
        {
          name: '木材加工和木、竹、藤、棕、草制品业',
          value: 9000,
        },
        {
          name: '其他房地产业',
          value: 9000,
        },
        {
          name: '五金、家具及室内装饰材料专门零售',
          value: 9000,
        },
        {
          name: '运输代理业',
          value: 9000,
        },
        {
          name: '铸造及其他金属制品制造',
          value: 9000,
        },
        {
          name: '饲料加工',
          value: 9000,
        },
        {
          name: '机动车、电子产品和日用产品修理业',
          value: 9000,
        },
        {
          name: '道路货物运输',
          value: 9000,
        },
        {
          name: '其他未列明金融业',
          value: 9000,
        },
        {
          name: '农业科学研究和试验发展',
          value: 9000,
        },
        {
          name: '其他金融业',
          value: 9000,
        },
        {
          name: '城市公共交通运输',
          value: 9000,
        },
        {
          name: '电线、电缆、光缆及电工器材制造',
          value: 9000,
        },
        {
          name: '文化艺术业',
          value: 9000,
        },
        {
          name: '互联网接入及相关服务',
          value: 9000,
        },
        {
          name: '婚姻服务',
          value: 9000,
        },
        {
          name: '铁合金冶炼',
          value: 9000,
        },
        {
          name: '殡葬服务',
          value: 9000,
        },
        {
          name: '通用仓储',
          value: 9000,
        },
        {
          name: '植物油加工',
          value: 9000,
        },
        {
          name: '其他日用产品修理业',
          value: 9000,
        },
        {
          name: '多式联运和运输代理业',
          value: 9000,
        },
        {
          name: '其他餐饮业',
          value: 9000,
        },
        {
          name: '金融信托与管理服务',
          value: 9000,
        },
        {
          name: '金融信息服务',
          value: 9000,
        },
        {
          name: '多式联运',
          value: 9000,
        },
        {
          name: '石油、煤炭及其他燃料加工业',
          value: 9000,
        },
        {
          name: '非公开募集证券投资基金',
          value: 9000,
        },
        {
          name: '通用航空服务',
          value: 9000,
        },
        {
          name: '市政设施管理',
          value: 9000,
        },
        {
          name: '家用电器修理',
          value: 9000,
        },
        {
          name: '金融资产管理公司',
          value: 9000,
        },
        {
          name: '谷物、棉花等农产品仓储',
          value: 9000,
        },
        {
          name: '其他烟草制品制造',
          value: 9000,
        },
        {
          name: '家庭服务',
          value: 8999,
        },
        {
          name: '商务服务业',
          value: 8999,
        },
        {
          name: '其他批发业',
          value: 8999,
        },
        {
          name: '互联网安全服务',
          value: 8750,
        },
        {
          name: '其他信息技术服务业',
          value: 8500,
        },
        {
          name: '组织管理服务',
          value: 8500,
        },
        {
          name: '食品、饮料及烟草制品批发',
          value: 8500,
        },
        {
          name: '技术推广服务',
          value: 8500,
        },
        {
          name: '咨询与调查',
          value: 8500,
        },
        {
          name: '信息技术咨询服务',
          value: 8500,
        },
        {
          name: '知识产权服务',
          value: 8500,
        },
        {
          name: '互联网信息服务',
          value: 8500,
        },
        {
          name: '综合管理服务',
          value: 8500,
        },
        {
          name: '批发业',
          value: 8500,
        },
        {
          name: '零售业',
          value: 8500,
        },
        {
          name: '餐饮配送及外卖送餐服务',
          value: 8500,
        },
        {
          name: '提供住宿社会工作',
          value: 8500,
        },
      ],
      // 真实数据
      highSalaryWordsData: [
        {
          name: '高速铁路运营管理',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '城市轨道交通智能运营',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁道工程技术',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁道通信与信息化技术',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁道交通运营管理',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '高速铁路客运服务',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '城市轨道交通运营管理',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁路物流管理',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁道运输管理',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '铁路客运服务',
          value: 35000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '铁道工程技术人员',
            '铁道运输工程技术人员',
          ],
        },
        {
          name: '国际金融',
          value: 21750,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '银行专业人员',
            '银行国际业务专业人员',
          ],
        },
        {
          name: '工业工程',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '标准化、计量、质量和认证认可工程技术人员',
            '标准化工程技术人员',
          ],
        },
        {
          name: '绿色食品生产技术',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '标准化、计量、质量和认证认可工程技术人员',
            '标准化工程技术人员',
          ],
        },
        {
          name: '标准化技术',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '标准化、计量、质量和认证认可工程技术人员',
            '标准化工程技术人员',
          ],
        },
        {
          name: '中医学',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '中医医师', '中医内科医师'],
        },
        {
          name: '预防医学',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '全科医师'],
        },
        {
          name: '健康管理',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '全科医师'],
        },
        {
          name: '临床医学',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '全科医师'],
        },
        {
          name: '预防医学',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '全科医师'],
        },
        {
          name: '健康管理',
          value: 15000,
          professionName: ['专业技术人员', '卫生专业技术人员', '临床和口腔医师', '全科医师'],
        },
        {
          name: '中医康复技术',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '中医养生保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '老年保健与管理',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '社区康复',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '保健按摩',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '美容保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '康复保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '中医养生保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '保健按摩',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '美容保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '康复保健',
          value: 15000,
          professionName: ['商业、服务业人员', '居民服务人员', '保健服务人员', '保健按摩师'],
        },
        {
          name: '航海技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '轮机工程',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶与海洋工程',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶智能制造技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '航海技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '轮机工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '水路运输与海事管理',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶智能焊接技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶舾装工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶涂装工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶通信装备技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '航海技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '轮机工程技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '水路运输安全管理',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶电子电气技术',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶检验',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶轮机',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶建造与维修',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶机械装置安装与维修',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶电气装置安装与调试',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶内装',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '轮机维护与管理',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶轮机',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '船舶建造与维修',
          value: 13750,
          professionName: [
            '生产制造及有关人员',
            '生产辅助人员',
            '船舶、航空器修理人员',
            '船舶修理工',
          ],
        },
        {
          name: '水利水电工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水文与水资源工程技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '智慧水利工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水利水电工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '生态水利工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水环境工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '建设工程管理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '建设工程监理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水政水资源管理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '智慧水利技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水利水电工程技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水利水电工程智能管理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水利水电建筑工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '智能水务管理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水环境智能监测与治理',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水生态修复技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '水利水电工程施工',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '水利水电建筑工程技术人员',
          ],
        },
        {
          name: '投资学',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券交易专业人员',
          ],
        },
        {
          name: '金融管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券交易专业人员',
          ],
        },
        {
          name: '金融服务与管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券交易专业人员',
          ],
        },
        {
          name: '财富管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券交易专业人员',
          ],
        },
        {
          name: '证券实务',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '证券交易专业人员',
          ],
        },
        {
          name: '金融学',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '金融工程',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '金融管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '金融科技应用',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '金融服务与管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '金融科技应用',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '信用管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '财富管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '证券实务',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '国际金融',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '农村金融',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '财务管理',
          value: 12000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '证券期货基金专业人员',
            '金融产品销售专业人员',
          ],
        },
        {
          name: '保险实务',
          value: 12000,
          professionName: [
            '商业、服务业人员',
            '批发与零售服务人员',
            '贸易经纪代理人员',
            '二手车经纪人',
          ],
        },
        {
          name: '汽车保险理赔与评估',
          value: 12000,
          professionName: [
            '商业、服务业人员',
            '批发与零售服务人员',
            '贸易经纪代理人员',
            '二手车经纪人',
          ],
        },
        {
          name: '汽车保险理赔与评估',
          value: 12000,
          professionName: [
            '商业、服务业人员',
            '批发与零售服务人员',
            '贸易经纪代理人员',
            '二手车经纪人',
          ],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶与海洋工程',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶智能制造技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '轮机工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶智能焊接技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶舾装工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶涂装工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶通信装备技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '轮机工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电子电气技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶检验',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶驾驶',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶轮机',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶建造与维修',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海捕捞',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '焊接加工',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '智能焊接技术',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '船舶智能焊接技术',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '焊接加工',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '焊接技术应用',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '金属表面处理技术应用',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '焊接加工',
          value: 11500,
          professionName: ['生产制造及有关人员', '机械制造基础加工人员', '机械热加工人员', '焊工'],
        },
        {
          name: '人物形象设计',
          value: 11500,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '会议及展览服务人员', '模特'],
        },
        {
          name: '服装模特',
          value: 11500,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '会议及展览服务人员', '模特'],
        },
        {
          name: '服装表演',
          value: 11500,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '会议及展览服务人员', '模特'],
        },
        {
          name: '服装模特',
          value: 11500,
          professionName: ['商业、服务业人员', '租赁和商务服务人员', '会议及展览服务人员', '模特'],
        },
        {
          name: '轨道交通车辆工程技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '高速铁路动车组技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道机车智能运用技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '高速铁路运营管理',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通信号与控制技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通设备与控制技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通智能运营',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '高速铁路动车组制造与维护',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通车辆制造与维护',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道机车运用与维护',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '动车组检修技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道交通运营管理',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通工程技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道车辆应用技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通机电技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通供配电技术',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通运营管理',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '电力机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '内燃机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通运输与管理',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通车辆运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道车辆运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '电力机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '内燃机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道运输服务',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通车辆运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通信号维护',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通供电',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通运营服务',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '电力机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '内燃机车运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通运输与管理',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '城市轨道交通车辆运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
        {
          name: '铁道车辆运用与检修',
          value: 11500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '轨道交通运输服务人员',
            '轨道交通列车司机',
          ],
        },
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 41486,
        },
        {
          name: '中型企业',
          value: 4437,
        },
        {
          name: '大型企业',
          value: 3031,
        },
        {
          name: '其他',
          value: 7368,
        },
      ],
      // 真实数据
      experienceData: [
        {
          name: '无经验',
          value: 28073,
        },
        {
          name: '经验不限',
          value: 333340,
        },
        {
          name: '1年以下',
          value: 15569,
        },
      ],
      // 真实数据
      educationData: [
        {
          name: '学历不限',
          value: 229557,
        },
        {
          name: '高中及以下',
          value: 45134,
        },
        {
          name: '大专',
          value: 102291,
        },
      ],
      // 真实数据
      threeIndustrySalaryData: [
        { name: '第一产业', value: 7500 },
        { name: '第二产业', value: 9000 },
        { name: '第三产业', value: 8500 },
      ],
    },
  },
  month: {
    all: {
      year: '2025',
      month: '05',
      nationalMedianSalary: 10200,
      // 真实数据
      provinceMapData: [
        {
          name: '香港特别行政区',
          value: 25000,
          group: 1,
        },
        {
          name: '上海市',
          value: 11500,
          group: 2,
        },
        {
          name: '北京市',
          value: 10499,
          group: 3,
        },
        {
          name: '浙江省',
          value: 9500,
          group: 4,
        },
        {
          name: '广东省',
          value: 9000,
          group: 5,
        },
        {
          name: '江苏省',
          value: 9000,
          group: 6,
        },
        {
          name: '重庆市',
          value: 8500,
          group: 7,
        },
        {
          name: '福建省',
          value: 8500,
          group: 8,
        },
        {
          name: '湖南省',
          value: 8499,
          group: 9,
        },
        {
          name: '湖北省',
          value: 8000,
          group: 10,
        },
        {
          name: '山东省',
          value: 8000,
          group: 11,
        },
        {
          name: '陕西省',
          value: 8000,
          group: 12,
        },
        {
          name: '四川省',
          value: 8000,
          group: 13,
        },
        {
          name: '天津市',
          value: 8000,
          group: 14,
        },
        {
          name: '西藏自治区',
          value: 8000,
          group: 15,
        },
        {
          name: '江西省',
          value: 7500,
          group: 16,
        },
        {
          name: '安徽省',
          value: 7500,
          group: 17,
        },
        {
          name: '甘肃省',
          value: 7500,
          group: 18,
        },
        {
          name: '贵州省',
          value: 7500,
          group: 19,
        },
        {
          name: '河南省',
          value: 7500,
          group: 20,
        },
        {
          name: '宁夏回族自治区',
          value: 7500,
          group: 21,
        },
        {
          name: '山西省',
          value: 7500,
          group: 22,
        },
        {
          name: '新疆维吾尔自治区',
          value: 7500,
          group: 23,
        },
        {
          name: '云南省',
          value: 7500,
          group: 24,
        },
        {
          name: '广西壮族自治区',
          value: 7000,
          group: 25,
        },
        {
          name: '海南省',
          value: 7000,
          group: 26,
        },
        {
          name: '河北省',
          value: 7000,
          group: 27,
        },
        {
          name: '黑龙江省',
          value: 7000,
          group: 28,
        },
        {
          name: '吉林省',
          value: 7000,
          group: 29,
        },
        {
          name: '辽宁省',
          value: 7000,
          group: 30,
        },
        {
          name: '内蒙古自治区',
          value: 7000,
          group: 31,
        },
        {
          name: '青海省',
          value: 7000,
          group: 32,
        },
        {
          name: '澳门特别行政区',
          value: 0,
          group: 33,
        },
        {
          name: '台湾省',
          value: 0,
          group: 34,
        },
      ],
      // 真实数据
      professionSalaryData: [
        {
          name: '事业单位负责人',
          value: 24000,
          group: 1,
        },
        {
          name: '皮肤科医师',
          value: 23000,
          group: 2,
        },
        {
          name: '机器人工程技术人员',
          value: 22500,
          group: 3,
        },
        {
          name: '人工智能工程技术人员',
          value: 17500,
          group: 4,
        },
        {
          name: '雷达导航工程技术人员',
          value: 16500,
          group: 5,
        },
        {
          name: '变压器互感器制造工',
          value: 16000,
          group: 6,
        },
        {
          name: '道路与桥隧工程技术人员',
          value: 15250,
          group: 7,
        },
        {
          name: '企业经理',
          value: 15000,
          group: 8,
        },
        {
          name: '计算机硬件工程技术人员',
          value: 15000,
          group: 9,
        },
        {
          name: '数字化解决方案设计师',
          value: 15000,
          group: 10,
        },
        {
          name: '数据库运行管理员',
          value: 14500,
          group: 11,
        },
        {
          name: '电影电视片发行人',
          value: 14500,
          group: 12,
        },
        {
          name: '嵌入式系统设计工程技术人员',
          value: 14250,
          group: 13,
        },
        {
          name: '中医内科医师',
          value: 13500,
          group: 14,
        },
        {
          name: '计算机软件工程技术人员',
          value: 13000,
          group: 15,
        },
        {
          name: '电气工程技术人员',
          value: 13000,
          group: 16,
        },
        {
          name: '社团会员管理员',
          value: 13000,
          group: 17,
        },
        {
          name: '专利代理专业人员',
          value: 12500,
          group: 18,
        },
        {
          name: '计算机程序设计员',
          value: 12500,
          group: 19,
        },
        {
          name: '集成电路工程技术人员',
          value: 12500,
          group: 20,
        },
      ],
      // 真实数据
      industrySalaryData: [
        {
          name: '信息传输、软件和信息技术服务业',
          value: 25000,
        },
        {
          name: '公开募集证券投资基金',
          value: 22500,
        },
        {
          name: '核辐射加工',
          value: 15000,
        },
        {
          name: '体育',
          value: 14750,
        },
        {
          name: '自行车和残疾人座车制造',
          value: 14000,
        },
        {
          name: '土地登记代理服务',
          value: 13500,
        },
        {
          name: '木材加工和木、竹、藤、棕、草制品业',
          value: 13500,
        },
        {
          name: '海洋工程建筑',
          value: 13000,
        },
        {
          name: '货币金融服务',
          value: 12500,
        },
        {
          name: '电视',
          value: 12500,
        },
        {
          name: '非公开募集证券投资基金',
          value: 12500,
        },
        {
          name: '保险资产管理',
          value: 12500,
        },
        {
          name: '废弃资源综合利用业',
          value: 12250,
        },
        {
          name: '其他未列明金融业',
          value: 12000,
        },
        {
          name: '医院',
          value: 12000,
        },
        {
          name: '污水处理及其再生利用',
          value: 12000,
        },
        {
          name: '船舶及相关装置制造',
          value: 12000,
        },
        {
          name: '其他采矿业',
          value: 12000,
        },
        {
          name: '雷达及配套设备制造',
          value: 12000,
        },
        {
          name: '电车制造',
          value: 11750,
        },
        {
          name: '狩猎和捕捉动物',
          value: 11750,
        },
        {
          name: '电池制造',
          value: 11500,
        },
        {
          name: '生物药品制品制造',
          value: 11500,
        },
        {
          name: '其他煤炭采选',
          value: 11500,
        },
        {
          name: '电影放映',
          value: 11500,
        },
        {
          name: '非金融机构支付服务',
          value: 11500,
        },
        {
          name: '天然气开采',
          value: 11500,
        },
        {
          name: '开采专业及辅助性活动',
          value: 11500,
        },
        {
          name: '邮政基本服务',
          value: 11500,
        },
        {
          name: '其他金融业',
          value: 11250,
        },
        {
          name: '汽车整车制造',
          value: 11250,
        },
        {
          name: '皮革、毛皮、羽毛及其制品和制鞋业',
          value: 11250,
        },
        {
          name: '其他仪器仪表制造业',
          value: 11000,
        },
        {
          name: '集成电路设计',
          value: 11000,
        },
        {
          name: '建筑业',
          value: 11000,
        },
        {
          name: '黑色金属矿采选业',
          value: 11000,
        },
        {
          name: '水上运输辅助活动',
          value: 11000,
        },
        {
          name: '中央银行服务',
          value: 11000,
        },
        {
          name: '搪瓷制品制造',
          value: 11000,
        },
        {
          name: '海底管道运输',
          value: 11000,
        },
        {
          name: '其他开采专业及辅助性活动',
          value: 10750,
        },
        {
          name: '计算机、通信和其他电子设备制造业',
          value: 10500,
        },
        {
          name: '电子器件制造',
          value: 10500,
        },
        {
          name: '光学仪器制造',
          value: 10500,
        },
        {
          name: '金融信托与管理服务',
          value: 10500,
        },
        {
          name: '专用设备制造业',
          value: 10500,
        },
        {
          name: '照明器具制造',
          value: 10500,
        },
        {
          name: '铁路、船舶、航空航天和其他运输设备制造业',
          value: 10500,
        },
        {
          name: '其他家具制造',
          value: 10500,
        },
        {
          name: '水利管理业',
          value: 10500,
        },
        {
          name: '餐饮业',
          value: 10500,
        },
        {
          name: '常用有色金属矿采选',
          value: 10500,
        },
        {
          name: '纤维素纤维原料及纤维制造',
          value: 10500,
        },
        {
          name: '助动车制造',
          value: 10500,
        },
        {
          name: '肥料制造',
          value: 10250,
        },
        {
          name: '电子和电工机械专用设备制造',
          value: 10000,
        },
        {
          name: '炼铁',
          value: 10000,
        },
        {
          name: '其他水利管理业',
          value: 10000,
        },
        {
          name: '其他信息技术服务业',
          value: 10000,
        },
        {
          name: '居民服务业',
          value: 10000,
        },
        {
          name: '汽车零部件及配件制造',
          value: 10000,
        },
        {
          name: '数字内容服务',
          value: 10000,
        },
        {
          name: '化学药品制剂制造',
          value: 10000,
        },
        {
          name: '木质家具制造',
          value: 10000,
        },
        {
          name: '机械设备经营租赁',
          value: 10000,
        },
        {
          name: '租赁业',
          value: 10000,
        },
        {
          name: '证券市场服务',
          value: 10000,
        },
        {
          name: '其他住宿业',
          value: 10000,
        },
        {
          name: '广播电视集成播控',
          value: 10000,
        },
        {
          name: '汽车制造业',
          value: 10000,
        },
        {
          name: '互联网平台',
          value: 10000,
        },
        {
          name: '基层医疗卫生服务',
          value: 10000,
        },
        {
          name: '其他仓储业',
          value: 10000,
        },
        {
          name: '家具制造业',
          value: 10000,
        },
        {
          name: '酒、饮料和精制茶制造业',
          value: 10000,
        },
        {
          name: '商业养老金',
          value: 10000,
        },
        {
          name: '铁矿采选',
          value: 10000,
        },
        {
          name: '生态保护',
          value: 10000,
        },
        {
          name: '皮革制品制造',
          value: 10000,
        },
        {
          name: '水上运输业',
          value: 10000,
        },
        {
          name: '多式联运和运输代理业',
          value: 10000,
        },
        {
          name: '草种植及割草',
          value: 10000,
        },
        {
          name: '节能环保工程施工',
          value: 10000,
        },
        {
          name: '摩托车制造',
          value: 10000,
        },
        {
          name: '皮革鞣制加工',
          value: 10000,
        },
        {
          name: '货币银行服务',
          value: 9750,
        },
        {
          name: '衡器制造',
          value: 9750,
        },
        {
          name: '其他水的处理、利用与分配',
          value: 9750,
        },
        {
          name: '其他未列明制造业',
          value: 9500,
        },
        {
          name: '通用设备制造业',
          value: 9500,
        },
        {
          name: '人身保险',
          value: 9500,
        },
        {
          name: '计算机制造',
          value: 9500,
        },
        {
          name: '环保、邮政、社会公共服务及其他专用设备制造',
          value: 9500,
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 9500,
        },
        {
          name: '保险业',
          value: 9500,
        },
        {
          name: '仪器仪表制造业',
          value: 9500,
        },
        {
          name: '航空运输业',
          value: 9500,
        },
        {
          name: '通用仪器仪表制造',
          value: 9500,
        },
        {
          name: '其他房地产业',
          value: 9500,
        },
        {
          name: '提供施工设备服务',
          value: 9500,
        },
      ],
      // 真实数据
      highSalaryWordsData: [
        {
          name: '机械电子工程技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能控制技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机器人技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '市场营销',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能制造技术应用',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人应用与维护',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '服务机器人应用与维护',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机械设计与制造',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机械制造及自动化',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '机电设备技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能机电技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能控制技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能机器人技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '船舶智能焊接技术',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能制造技术应用',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能装备安装与调试',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '智能装备运行与维护',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '工业机器人应用与维护',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '服务机器人应用与维护',
          value: 22500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '机器人工程技术人员',
          ],
        },
        {
          name: '电子信息工程技术',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能工程技术',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '智能产品开发与应用',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '人工智能技术应用',
          value: 17500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '人工智能工程技术人员',
          ],
        },
        {
          name: '导航工程技术',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '导航与位置服务',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '民航通信技术',
          value: 16500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '工业自动化仪器仪表装配与维护',
          value: 16000,
          professionName: [
            '生产制造及有关人员',
            '电气机械和器材制造人员',
            '输配电及控制设备制造人员',
            '变压器互感器制造工',
          ],
        },
        {
          name: '变配电设备运行与维护',
          value: 16000,
          professionName: [
            '生产制造及有关人员',
            '电气机械和器材制造人员',
            '输配电及控制设备制造人员',
            '变压器互感器制造工',
          ],
        },
        {
          name: '电机电器装配与维修',
          value: 16000,
          professionName: [
            '生产制造及有关人员',
            '电气机械和器材制造人员',
            '输配电及控制设备制造人员',
            '变压器互感器制造工',
          ],
        },
        {
          name: '电气自动化设备安装与维修',
          value: 16000,
          professionName: [
            '生产制造及有关人员',
            '电气机械和器材制造人员',
            '输配电及控制设备制造人员',
            '变压器互感器制造工',
          ],
        },
        {
          name: '道路与桥梁工程',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '地下与隧道工程技术',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '铁道桥梁隧道工程技术',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '道路与桥梁工程技术',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '道路机械化施工技术',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '道路工程检测技术',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '道路养护与管理',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '桥梁施工与养护',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '铁路施工与养护',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '市政工程施工',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '土建工程检测',
          value: 15250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '建筑工程技术人员',
            '道路与桥隧工程技术人员',
          ],
        },
        {
          name: '电信服务与管理',
          value: 15000,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '信息通信网络运行管理人员',
            '数字化解决方案设计师',
          ],
        },
        {
          name: '网络与信息安全',
          value: 14500,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '软件和信息技术服务人员',
            '数据库运行管理员',
          ],
        },
        {
          name: '影视制片管理',
          value: 14500,
          professionName: [
            '专业技术人员',
            '文学艺术、体育专业人员',
            '电影电视制作专业人员',
            '电影电视片发行人',
          ],
        },
        {
          name: '自动化',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '机械电子工程技术',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '电气工程及自动化',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '自动化技术与应用',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '嵌入式技术',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '电气自动化技术',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '工业过程自动化技术',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '化工自动化技术',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '智能产品开发与应用',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '嵌入式技术应用',
          value: 14250,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '嵌入式系统设计工程技术人员',
          ],
        },
        {
          name: '中医学',
          value: 13500,
          professionName: ['专业技术人员', '卫生专业技术人员', '中医医师', '中医内科医师'],
        },
        {
          name: '软件工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '计算机应用工程',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '软件工程技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '计算机程序设计',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '软件技术',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '计算机程序设计',
          value: 13000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '计算机软件工程技术人员',
          ],
        },
        {
          name: '计算机程序设计',
          value: 12500,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '软件和信息技术服务人员',
            '计算机程序设计员',
          ],
        },
        {
          name: '计算机程序设计',
          value: 12500,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '软件和信息技术服务人员',
            '计算机程序设计员',
          ],
        },
        {
          name: '计算机程序设计',
          value: 12500,
          professionName: [
            '商业、服务业人员',
            '信息传输、软件和信息技术服务人员',
            '软件和信息技术服务人员',
            '计算机程序设计员',
          ],
        },
        {
          name: '微电子科学与工程',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '柔性电子技术',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路工程技术',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术应用',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '微电子技术',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
        {
          name: '集成电路技术应用',
          value: 12500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '数字技术工程技术人员',
            '集成电路工程技术人员',
          ],
        },
      ],
      // 真实数据
      companyData: [
        { name: '小微企业', value: 32341 },
        { name: '中型企业', value: 5551 },
        { name: '大型企业', value: 4006 },
        { name: '其他', value: 5970 },
      ],
      // 真实数据
      experienceData: [
        {
          name: '一年以下',
          value: 118941,
        },
        {
          name: '1-3年',
          value: 51350,
        },
        {
          name: '3-5年',
          value: 32565,
        },
        {
          name: '5-10年',
          value: 13393,
        },
        {
          name: '10年以上',
          value: 1636,
        },
      ],
      // 真实数据
      educationData: [
        {
          name: '大专',
          value: 62763,
        },
        {
          name: '学历不限',
          value: 90222,
        },
        {
          name: '本科',
          value: 44864,
        },
        {
          name: '高中及以下',
          value: 18115,
        },
        {
          name: '研究生及以上',
          value: 1920,
        },
      ],
      // 真实数据
      threeIndustrySalaryData: [
        { name: '第一产业', value: 7000 },
        { name: '第二产业', value: 8500 },
        { name: '第三产业', value: 8000 },
      ],
    },
    college: {
      year: '2025',
      month: '05',
      nationalMedianSalary: 9200,
      // 真实数据
      provinceMapData: [
        {
          name: '香港特别行政区',
          value: 18000,
          group: 1,
        },
        {
          name: '上海市',
          value: 10500,
          group: 2,
        },
        {
          name: '北京市',
          value: 10000,
          group: 3,
        },
        {
          name: '浙江省',
          value: 9000,
          group: 4,
        },
        {
          name: '重庆市',
          value: 8500,
          group: 5,
        },
        {
          name: '广东省',
          value: 8500,
          group: 6,
        },
        {
          name: '福建省',
          value: 8000,
          group: 7,
        },
        {
          name: '湖南省',
          value: 8000,
          group: 8,
        },
        {
          name: '江苏省',
          value: 8000,
          group: 9,
        },
        {
          name: '江西省',
          value: 7500,
          group: 10,
        },
        {
          name: '安徽省',
          value: 7500,
          group: 11,
        },
        {
          name: '甘肃省',
          value: 7500,
          group: 12,
        },
        {
          name: '贵州省',
          value: 7500,
          group: 13,
        },
        {
          name: '河南省',
          value: 7500,
          group: 14,
        },
        {
          name: '湖北省',
          value: 7500,
          group: 15,
        },
        {
          name: '山东省',
          value: 7500,
          group: 16,
        },
        {
          name: '陕西省',
          value: 7500,
          group: 17,
        },
        {
          name: '山西省',
          value: 7500,
          group: 18,
        },
        {
          name: '四川省',
          value: 7500,
          group: 19,
        },
        {
          name: '天津市',
          value: 7500,
          group: 20,
        },
        {
          name: '云南省',
          value: 7500,
          group: 21,
        },
        {
          name: '广西壮族自治区',
          value: 7000,
          group: 22,
        },
        {
          name: '海南省',
          value: 7000,
          group: 23,
        },
        {
          name: '吉林省',
          value: 7000,
          group: 24,
        },
        {
          name: '宁夏回族自治区',
          value: 7000,
          group: 25,
        },
        {
          name: '新疆维吾尔自治区',
          value: 7000,
          group: 26,
        },
        {
          name: '河北省',
          value: 6500,
          group: 27,
        },
        {
          name: '黑龙江省',
          value: 6500,
          group: 28,
        },
        {
          name: '辽宁省',
          value: 6500,
          group: 29,
        },
        {
          name: '内蒙古自治区',
          value: 6500,
          group: 30,
        },
        {
          name: '青海省',
          value: 6500,
          group: 31,
        },
        {
          name: '西藏自治区',
          value: 6500,
          group: 32,
        },
        {
          name: '澳门特别行政区',
          value: 0,
          group: 33,
        },
        {
          name: '台湾省',
          value: 0,
          group: 34,
        },
      ],
      // 真实数据
      professionSalaryData: [
        {
          name: '皮肤科医师',
          value: 60000,
          group: 1,
        },
        {
          name: '中医内科医师',
          value: 18000,
          group: 2,
        },
        {
          name: '企业经理',
          value: 15000,
          group: 3,
        },
        {
          name: '品牌专业人员',
          value: 12750,
          group: 4,
        },
        {
          name: '汽车代驾员',
          value: 12000,
          group: 5,
        },
        {
          name: '甲板部技术人员',
          value: 11500,
          group: 6,
        },
        {
          name: '通信工程技术人员',
          value: 10500,
          group: 7,
        },
        {
          name: '地理信息系统工程技术人员',
          value: 10500,
          group: 8,
        },
        {
          name: '快递站点管理师',
          value: 10500,
          group: 9,
        },
        {
          name: '会展策划专业人员',
          value: 10000,
          group: 10,
        },
        {
          name: '道路货运汽车驾驶员',
          value: 10000,
          group: 11,
        },
        {
          name: '客运船舶驾驶员',
          value: 10000,
          group: 12,
        },
        {
          name: '家具设计师',
          value: 9750,
          group: 13,
        },
        {
          name: '雷达导航工程技术人员',
          value: 9500,
          group: 14,
        },
        {
          name: '客运车辆驾驶员',
          value: 9500,
          group: 15,
        },
        {
          name: '营销员',
          value: 9000,
          group: 16,
        },
        {
          name: '社会工作者',
          value: 9000,
          group: 17,
        },
        {
          name: '信息安全工程技术人员',
          value: 9000,
          group: 18,
        },
        {
          name: '快递员',
          value: 9000,
          group: 19,
        },
        {
          name: '网约配送员',
          value: 8999,
          group: 20,
        },
      ],
      // 真实数据
      industrySalaryData: [
        {
          name: '自行车和残疾人座车制造',
          value: 15000,
        },
        {
          name: '其他煤炭采选',
          value: 14250,
        },
        {
          name: '公开募集证券投资基金',
          value: 14000,
        },
        {
          name: '土地登记代理服务',
          value: 13500,
        },
        {
          name: '木材加工和木、竹、藤、棕、草制品业',
          value: 13500,
        },
        {
          name: '电视',
          value: 12500,
        },
        {
          name: '搪瓷制品制造',
          value: 12500,
        },
        {
          name: '其他采矿业',
          value: 12000,
        },
        {
          name: '雷达及配套设备制造',
          value: 12000,
        },
        {
          name: '废弃资源综合利用业',
          value: 12000,
        },
        {
          name: '狩猎和捕捉动物',
          value: 11750,
        },
        {
          name: '其他金融业',
          value: 11500,
        },
        {
          name: '医院',
          value: 11500,
        },
        {
          name: '邮政基本服务',
          value: 11500,
        },
        {
          name: '非公开募集证券投资基金',
          value: 11000,
        },
        {
          name: '电影放映',
          value: 11000,
        },
        {
          name: '水上运输辅助活动',
          value: 11000,
        },
        {
          name: '中央银行服务',
          value: 11000,
        },
        {
          name: '海底管道运输',
          value: 11000,
        },
        {
          name: '钟表与计时仪器制造',
          value: 10750,
        },
        {
          name: '照明器具制造',
          value: 10500,
        },
        {
          name: '铁路、船舶、航空航天和其他运输设备制造业',
          value: 10500,
        },
        {
          name: '肥料制造',
          value: 10500,
        },
        {
          name: '货币银行服务',
          value: 10500,
        },
        {
          name: '餐饮业',
          value: 10500,
        },
        {
          name: '生态保护',
          value: 10250,
        },
        {
          name: '货币金融服务',
          value: 10250,
        },
        {
          name: '炼铁',
          value: 10000,
        },
        {
          name: '其他信息技术服务业',
          value: 10000,
        },
        {
          name: '居民服务业',
          value: 10000,
        },
        {
          name: '机械设备经营租赁',
          value: 10000,
        },
        {
          name: '租赁业',
          value: 10000,
        },
        {
          name: '污水处理及其再生利用',
          value: 10000,
        },
        {
          name: '互联网平台',
          value: 10000,
        },
        {
          name: '其他仓储业',
          value: 10000,
        },
        {
          name: '酒的制造',
          value: 10000,
        },
        {
          name: '铁矿采选',
          value: 10000,
        },
        {
          name: '皮革制品制造',
          value: 10000,
        },
        {
          name: '多式联运和运输代理业',
          value: 10000,
        },
        {
          name: '水上运输业',
          value: 10000,
        },
        {
          name: '草种植及割草',
          value: 10000,
        },
        {
          name: '皮革鞣制加工',
          value: 10000,
        },
        {
          name: '衡器制造',
          value: 9750,
        },
        {
          name: '汽车、摩托车等修理与维护',
          value: 9500,
        },
        {
          name: '保险业',
          value: 9500,
        },
        {
          name: '集成电路设计',
          value: 9500,
        },
        {
          name: '电力工程施工',
          value: 9500,
        },
        {
          name: '其他房地产业',
          value: 9500,
        },
        {
          name: '城市公共交通运输',
          value: 9500,
        },
        {
          name: '其他日用产品修理业',
          value: 9500,
        },
        {
          name: '道路运输辅助活动',
          value: 9500,
        },
        {
          name: '互联网接入及相关服务',
          value: 9500,
        },
        {
          name: '快递服务',
          value: 9500,
        },
        {
          name: '玻璃纤维和玻璃纤维增强塑料制品制造',
          value: 9500,
        },
        {
          name: '提供施工设备服务',
          value: 9250,
        },
        {
          name: '商业养老金',
          value: 9250,
        },
        {
          name: '其他仪器仪表制造业',
          value: 9000,
        },
        {
          name: '计算机、通信和其他电子设备制造业',
          value: 9000,
        },
        {
          name: '其他批发业',
          value: 9000,
        },
        {
          name: '文艺创作与表演',
          value: 9000,
        },
        {
          name: '房地产中介服务',
          value: 9000,
        },
        {
          name: '人身保险',
          value: 9000,
        },
        {
          name: '建筑、安全用金属制品制造',
          value: 9000,
        },
        {
          name: '非金属矿物制品业',
          value: 9000,
        },
        {
          name: '专用设备制造业',
          value: 9000,
        },
        {
          name: '涂料、油墨、颜料及类似产品制造',
          value: 9000,
        },
        {
          name: '木质家具制造',
          value: 9000,
        },
        {
          name: '保险中介服务',
          value: 9000,
        },
        {
          name: '数字内容服务',
          value: 9000,
        },
        {
          name: '橡胶和塑料制品业',
          value: 9000,
        },
        {
          name: '其他农业',
          value: 9000,
        },
        {
          name: '谷物磨制',
          value: 9000,
        },
        {
          name: '基层医疗卫生服务',
          value: 9000,
        },
        {
          name: '电力供应',
          value: 9000,
        },
        {
          name: '运输代理业',
          value: 9000,
        },
        {
          name: '非专业视听设备制造',
          value: 9000,
        },
        {
          name: '家庭服务',
          value: 9000,
        },
        {
          name: '金融信托与管理服务',
          value: 9000,
        },
        {
          name: '光学仪器制造',
          value: 9000,
        },
        {
          name: '饲料加工',
          value: 9000,
        },
        {
          name: '家具制造业',
          value: 9000,
        },
        {
          name: '林业专业及辅助性活动',
          value: 9000,
        },
        {
          name: '电车制造',
          value: 9000,
        },
        {
          name: '文化、办公用机械制造',
          value: 9000,
        },
        {
          name: '金融资产管理公司',
          value: 9000,
        },
        {
          name: '其他土地管理服务',
          value: 9000,
        },
        {
          name: '其他开采专业及辅助性活动',
          value: 9000,
        },
        {
          name: '初等教育',
          value: 9000,
        },
        {
          name: '管道运输业',
          value: 9000,
        },
        {
          name: '知识产权服务',
          value: 8750,
        },
        {
          name: '蔬菜、菌类、水果和坚果加工',
          value: 8750,
        },
        {
          name: '黑色金属矿采选业',
          value: 8750,
        },
        {
          name: '麻纺织及染整精加工',
          value: 8749,
        },
        {
          name: '组织管理服务',
          value: 8500,
        },
        {
          name: '信息技术咨询服务',
          value: 8500,
        },
        {
          name: '技术推广服务',
          value: 8500,
        },
        {
          name: '电子器件制造',
          value: 8500,
        },
        {
          name: '零售业',
          value: 8500,
        },
        {
          name: '互联网和相关服务',
          value: 8500,
        },
        {
          name: '综合管理服务',
          value: 8500,
        },
      ],
      // 真实数据
      highSalaryWordsData: [
        {
          name: '中医学',
          value: 18000,
          professionName: ['专业技术人员', '卫生专业技术人员', '中医医师', '中医内科医师'],
        },
        {
          name: '市场营销',
          value: 12750,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '品牌专业人员'],
        },
        {
          name: '电子商务',
          value: 12750,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '品牌专业人员'],
        },
        {
          name: '全媒体电商运营',
          value: 12750,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '品牌专业人员'],
        },
        {
          name: '市场营销',
          value: 12750,
          professionName: ['专业技术人员', '经济和金融专业人员', '商务专业人员', '品牌专业人员'],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶与海洋工程',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶智能制造技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '轮机工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶动力工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电气工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶智能焊接技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶舾装工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶涂装工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶通信装备技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '轮机工程技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶电子电气技术',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶检验',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶驾驶',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶轮机',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '船舶建造与维修',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '航海捕捞',
          value: 11500,
          professionName: [
            '专业技术人员',
            '飞机和船舶技术人员',
            '船舶指挥和引航人员',
            '甲板部技术人员',
          ],
        },
        {
          name: '通信工程',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '网络工程技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '现代通信工程',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信终端设备制造与维修',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '计算机网络应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信网络应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '工业互联网技术应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '轨道交通通信信号设备制造与维护',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '铁道通信与信息化技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '民航通信技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '城市轨道交通通信信号技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '计算机网络技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '现代通信技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '现代移动通信技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信软件技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信工程设计与监理',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信系统运行管理',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '网络规划与优化技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '电信服务与管理',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信终端设备制造与维修',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '工业网络技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '计算机信息管理',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信网络应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '通信运营服务',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '网络与信息安全',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '云计算技术应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '工业互联网技术应用',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '通信工程技术人员',
          ],
        },
        {
          name: '地理信息科学',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '测绘工程技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '地理信息技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '测绘地理信息技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '空间数字建模与应用技术',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '地图制图与地理信息系统',
          value: 10500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '测绘和地理信息工程技术人员',
            '地理信息系统工程技术人员',
          ],
        },
        {
          name: '邮政快递管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政快递运营管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政快递智能技术',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政业务',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '快递运营管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '快递安全管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政快递运营',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政快递安全技术',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政通信服务',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '邮政业务',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '快递运营管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '快递安全管理',
          value: 10500,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递站点管理师',
          ],
        },
        {
          name: '会展经济与管理',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '展示艺术设计',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '会展策划与管理',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '展示艺术设计',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '会展服务与管理',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '文化产业经营与管理',
          value: 10000,
          professionName: [
            '专业技术人员',
            '经济和金融专业人员',
            '商务专业人员',
            '会展策划专业人员',
          ],
        },
        {
          name: '智能网联汽车技术',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '汽车保险理赔与评估',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '交通运营服务',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '国际货运代理',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '汽车保险理赔与评估',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '智能网联汽车技术应用',
          value: 10000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '道路运输服务人员',
            '道路货运汽车驾驶员',
          ],
        },
        {
          name: '木业产品智能制造',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '木业智能装备应用技术',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '家具设计与制造',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '产品艺术设计',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '家具艺术设计',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '家具设计与制作',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '工业设计',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '家具设计与制作',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '家具设计与制作',
          value: 9750,
          professionName: [
            '商业、服务业人员',
            '技术辅助服务人员',
            '专业化设计服务人员',
            '家具设计师',
          ],
        },
        {
          name: '导航工程技术',
          value: 9500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '导航与位置服务',
          value: 9500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '民航通信技术',
          value: 9500,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '电子工程技术人员',
            '雷达导航工程技术人员',
          ],
        },
        {
          name: '市场调查与统计分析',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '市场营销',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '连锁经营与管理',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '市场营销',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '市场营销',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '药品营销',
          value: 9000,
          professionName: ['商业、服务业人员', '批发与零售服务人员', '销售人员', '营销员'],
        },
        {
          name: '社会工作',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '社会工作',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '智慧社区管理',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '社区矫正',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '社会工作',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '社区管理与服务',
          value: 9000,
          professionName: [
            '专业技术人员',
            '监察、法律、社会和宗教专业人员',
            '宗教教职人员',
            '社会工作者',
          ],
        },
        {
          name: '信息安全',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '信息管理与信息系统',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '软件工程技术',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '信息安全与管理',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '计算机信息管理',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '信息安全技术应用',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '计算机信息管理',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '网络与信息安全',
          value: 9000,
          professionName: [
            '专业技术人员',
            '工程技术人员',
            '信息和通信工程技术人员',
            '信息安全工程技术人员',
          ],
        },
        {
          name: '邮政快递运营管理',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '快递运营管理',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '快递安全管理',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '邮政快递运营',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '邮政快递安全技术',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '快递运营管理',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
        {
          name: '快递安全管理',
          value: 9000,
          professionName: [
            '商业、服务业人员',
            '交通运输、仓储物流和邮政业服务人员',
            '邮政和快递服务人员',
            '快递员',
          ],
        },
      ],
      // 真实数据
      companyData: [
        {
          name: '小微企业',
          value: 11354,
        },
        {
          name: '大型企业',
          value: 998,
        },
        {
          name: '中型企业',
          value: 1168,
        },
        {
          name: '其他',
          value: 2035,
        },
      ],
      // 真实数据
      experienceData: [
        {
          name: '经验不限',
          value: 97621,
        },
        {
          name: '1年以下',
          value: 3237,
        },
        {
          name: '无经验',
          value: 7722,
        },
      ],
      // 真实数据
      educationData: [
        {
          name: '大专',
          value: 20494,
        },
        {
          name: '高中及以下',
          value: 11485,
        },
        {
          name: '学历不限',
          value: 76603,
        },
      ],
      // 真实数据
      threeIndustrySalaryData: [
        {
          name: '第一产业',
          value: 6000,
        },
        {
          name: '第二产业',
          value: 6500,
        },
        {
          name: '第三产业',
          value: 8000,
        },
      ],
    },
  },
}

export default salaryData
