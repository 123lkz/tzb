interface EnumOption {
  value: string
  label: string
}

// 年份
export const eduYearMap: Record<string, string> = {
  '2020': '2020年',
  '2021': '2021年',
  '2022': '2022年',
  '2023': '2023年',
  '2024': '2024年',
}

export const eduYearOptions: EnumOption[] = Object.entries(eduYearMap).map(([value, label]) => ({
  value: value as string,
  label: label as string,
}))

// 学校类型
export const schoolTypeMap: Record<string, string> = {
  all: '全部院校',
  undergraduate: '本科院校',
  college: '专科院校',
}

export const schoolTypeOptions: EnumOption[] = Object.entries(schoolTypeMap).map(
  ([value, label]) => ({
    value: value as string,
    label: label as string,
  })
)

// 省份：全称-简称
export const provinceMap: Record<string, string> = {
  北京市: '北京',
  天津市: '天津',
  河北省: '河北',
  山西省: '山西',
  内蒙古自治区: '内蒙古',
  辽宁省: '辽宁',
  吉林省: '吉林',
  黑龙江省: '黑龙江',
  上海市: '上海',
  江苏省: '江苏',
  浙江省: '浙江',
  安徽省: '安徽',
  福建省: '福建',
  江西省: '江西',
  山东省: '山东',
  河南省: '河南',
  湖北省: '湖北',
  湖南省: '湖南',
  广东省: '广东',
  广西壮族自治区: '广西',
  海南省: '海南',
  重庆市: '重庆',
  四川省: '四川',
  贵州省: '贵州',
  云南省: '云南',
  西藏自治区: '西藏',
  陕西省: '陕西',
  甘肃省: '甘肃',
  青海省: '青海',
  宁夏回族自治区: '宁夏',
  新疆维吾尔自治区: '新疆',
  台湾省: '台湾',
  香港特别行政区: '香港',
  澳门特别行政区: '澳门',
}

// 省份 - 列表
export const provinceOptions: EnumOption[] = Object.entries(provinceMap).map(([value, label]) => ({
  value: value as string,
  label: label as string,
}))

// 统计口径
export const caliberMap: Record<string, string> = {
  all: '全口径',
  college: '大专生',
  collegeFresh: '应届大专生',
  bachelor: '本科生',
  bachelorFresh: '应届本科生',
  masterPlus: '研究生及以上',
}

export const caliberOptions: EnumOption[] = Object.entries(caliberMap).map(([value, label]) => ({
  value: value as string,
  label: label as string,
}))

// 职业-分类-标准职业
export const careerCategoryMap: Record<string, string> = {
  '1': '标准职业大类',
  '2': '标准职业中类',
  '3': '标准职业小类',
  '4': '标准职业细类',
}

export const careerCategoryOptions: EnumOption[] = Object.entries(careerCategoryMap).map(
  ([value, label]) => ({
    value: value as string,
    label: label as string,
  })
)

export const careerMajorCategoryOptions: EnumOption[] = [
  { value: '1', label: '党的机关、国家机关、群众团体和社会组织、企事业单位负责人' },
  { value: '2', label: '专业技术人员' },
  { value: '3', label: '办事人员和有关人员' },
  { value: '4', label: '社会生产服务和生活服务人员' },
  { value: '5', label: '农、林、牧、渔业生产及辅助人员' },
  { value: '6', label: '生产制造及有关人员' },
  { value: '7', label: '军队人员' },
  { value: '8', label: '不便分类的其他从业人员' },
]

// 行业-分类-标准行业
export const industryCategoryMap: Record<string, string> = {
  '1': '国民经济行业门类',
  '2': '国民经济行业大类',
  '3': '国民经济行业中类',
  '4': '国民经济行业小类',
}

export const industryCategoryList: EnumOption[] = Object.entries(industryCategoryMap).map(
  ([value, label]) => ({
    value: value as string,
    label: label as string,
  })
)

export const industryCategoryOptions: EnumOption[] = [
  { value: '1', label: '第一产业' },
  { value: '2', label: '第二产业' },
  { value: '3', label: '第三产业' },
]

export const industryMajorCategoryOptions: EnumOption[] = [
  { value: 'A', label: '农、林、牧、渔业' },
  { value: 'B', label: '采矿业' },
  { value: 'C', label: '制造业' },
  { value: 'D', label: '电力、热力、燃气及水生产和供应业' },
  { value: 'E', label: '建筑业' },
  { value: 'F', label: '批发和零售业' },
  { value: 'G', label: '交通运输、仓储和邮政业' },
  { value: 'H', label: '住宿和餐饮业' },
  { value: 'I', label: '信息传输、软件和信息技术服务业' },
  { value: 'J', label: '金融业' },
  { value: 'K', label: '房地产业' },
  { value: 'L', label: '租赁和商务服务业' },
  { value: 'M', label: '科学研究和技术服务业' },
  { value: 'N', label: '水利、环境和公共设施管理业' },
  { value: 'O', label: '居民服务、修理和其他服务业' },
  { value: 'P', label: '教育' },
  { value: 'Q', label: '卫生和社会工作' },
  { value: 'R', label: '文化、体育和娱乐业' },
  { value: 'S', label: '公共管理、社会保障和社会组织' },
  { value: 'T', label: '国际组织' },
]

export const industryMediumCategoryOptions: EnumOption[] = [
  { value: 'A-01', label: '农业' },
  { value: 'A-02', label: '林业' },
  { value: 'A-03', label: '畜牧业' },
  { value: 'A-04', label: '渔业' },
  { value: 'A-05', label: '农、林、牧、渔专业及辅助性活动' },
  {
    value: 'B-06',
    label: '煤炭开采和洗选业',
  },
  {
    value: 'B-07',
    label: '石油和天然气开采业',
  },
  {
    value: 'B-08',
    label: '黑色金属矿采选业',
  },
  {
    value: 'B-09',
    label: '有色金属矿采选业',
  },
  {
    value: 'B-10',
    label: '非金属矿采选业',
  },
]

// 单位规模
export const companyScaleMap: Record<string, string> = {
  large: '大型',
  middle: '中型',
  smallAndMicro: '小微型',
  small: '小型',
  micro: '微型',
}

export const companyScaleOptions: EnumOption[] = Object.entries(companyScaleMap).map(
  ([value, label]) => ({
    value: value as string,
    label: label as string,
  })
)

export const comparedMap: Record<string, string> = {
  weekly: '较上周',
  month: '较上月',
  year: '较去年',
}
