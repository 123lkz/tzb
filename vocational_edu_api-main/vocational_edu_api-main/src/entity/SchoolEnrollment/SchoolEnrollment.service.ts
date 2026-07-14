import { Injectable } from '@nestjs/common'
import { DOUBLE_HIGH_SCHOOLS } from '../../constants/doubleHighSchools'
import { CacheService } from '../../services/CacheService'
import { JobMajorMappingEntity } from '../JobMajorMapping/JobMajorMapping'
import { SchoolEnrollmentEntity } from './SchoolEnrollment'
import {
  GraduateNumResult,
  GraduateYearItem,
  MajorByPositionResult,
  ResultItem,
  SchoolParams,
  YearParams
} from './SchoolEnrollment.dto'

@Injectable()
export class SchoolEnrollmentService {
  private static cacheService: CacheService

  constructor() {
    if (!SchoolEnrollmentService.cacheService) {
      SchoolEnrollmentService.cacheService = CacheService.getInstance()
    }
  }

  static async getSchoolNumByProvince(params?: YearParams): Promise<Array<ResultItem & { doubleHighNum: number }>> {
    console.log('📊 开始获取省份学校数量数据...')

    const match: any = {
      school_location: { $nin: [null, '', undefined] },
      school_name: { $nin: [null, '', undefined] }
    }
    if (params?.category) {
      match.category = params.category
    }

    if (params?.year) {
      match.year = Number(params.year)
    } else {
      match.year = { $gte: 2020, $lte: 2022 }
    }

    const pipeline: any[] = [
      { $match: match },
      {
        $group: {
          _id: '$school_location',
          schools: { $addToSet: '$school_name' }
        }
      },
      { $project: { _id: 1, value: { $size: '$schools' } } },
      { $sort: { value: -1 } }
    ]

    const list = await (SchoolEnrollmentEntity as any).model.aggregate(pipeline)

    // 统计各省双高院校数量（基于专科院校名单匹配）
    const dhPipeline: any[] = [
      { $match: { category: '专科', school_name: { $nin: [null, '', undefined] } } },
      { $group: { _id: { province: '$school_location', school: '$school_name' } } },
      { $group: { _id: '$_id.province', schools: { $addToSet: '$_id.school' } } },
      { $project: { _id: 1, schools: 1 } }
    ]
    const dhRaw = await (SchoolEnrollmentEntity as any).model.aggregate(dhPipeline)
    const doubleHighSet = DOUBLE_HIGH_SCHOOLS
    const provinceToDhNum = new Map<string, number>()
    dhRaw.forEach((doc: any) => {
      const dhNum = (doc.schools as string[]).filter((n) => doubleHighSet.has(n)).length
      provinceToDhNum.set(doc._id, dhNum)
    })

    const provinceData: Array<ResultItem & { doubleHighNum: number }> = list.map((item: any, index: number) => ({
      name: item._id,
      value: item.value || 0,
      rank: index + 1,
      doubleHighNum: provinceToDhNum.get(item._id) || 0
    }))

    return provinceData
  }

  static async getStudentNumByProvince(params?: SchoolParams): Promise<ResultItem[]> {
    console.log('📊 开始获取省份学生数量数据...')

    const match: any = {
      school_location: { $nin: [null, '', undefined] },
      school_name: { $nin: [null, '', undefined] },
      year: { $gte: 2020, $lte: 2022 }
    }
    if (params?.category) {
      match.category = params.category
    }

    const pipeline: any[] = [
      { $match: match },
      {
        $group: {
          _id: '$school_location',
          studentNum: { $sum: { $ifNull: ['$enrollment_count', 0] } }
        }
      },
      { $project: { _id: 1, studentNum: 1 } },
      { $sort: { studentNum: -1 } }
    ]

    const list = await (SchoolEnrollmentEntity as any).model.aggregate(pipeline)

    const provinceData: ResultItem[] = list.map((item: any, index: number) => ({
      name: item._id,
      value: item.studentNum || 0,
      rank: index + 1
    }))

    return provinceData
  }

  static async getStudentNumByMajor(params?: SchoolParams): Promise<ResultItem[]> {
    console.log('📊 开始获取专业学生数量数据...')

    const match: any = {
      year: { $gte: 2020, $lte: 2022 },
      major: { $nin: [null, '', undefined] },
      enrollment_count: { $nin: [null, undefined] }
    }
    if (params?.category) {
      match.category = params.category
    }

    const pipeline: any[] = [
      { $match: match },
      {
        $group: {
          _id: '$major',
          studentNum: { $sum: { $ifNull: ['$enrollment_count', 0] } }
        }
      },
      { $project: { _id: 1, studentNum: 1 } },
      { $sort: { studentNum: -1 } }
    ]

    const list = await (SchoolEnrollmentEntity as any).model.aggregate(pipeline)

    const majorData: ResultItem[] = list.map((item: any, index: number) => ({
      name: item._id,
      value: item.studentNum || 0,
      rank: index + 1
    }))

    return majorData
  }

  static async getStudentNumByYear(params?: SchoolParams): Promise<GraduateNumResult> {
    console.log('📊 开始获取年度学生数量数据...')

    // 双高院校名单
    const doubleHighSchool = new Set<string>([
      '北京电子科技职业学院',
      '天津市职业大学',
      '江苏农林职业技术学院',
      '无锡职业技术学院',
      '金华职业技术学院',
      '浙江机电职业技术学院',
      '山东商业职业技术学院',
      '黄河水利职业技术学院',
      '深圳职业技术学院',
      '陕西工业职业技术学院',
      '北京工业职业技术学院',
      '天津医学高等专科学校',
      '河北工业职业技术学院',
      '辽宁省交通高等专科学校',
      '常州信息职业技术学院',
      '江苏农牧科技职业学院',
      '南京信息职业技术学院',
      '杭州职业技术学院',
      '宁波职业技术学院',
      '浙江金融职业学院',
      '日照职业技术学院',
      '淄博职业学院',
      '长沙民政职业技术学院',
      '广东轻工职业技术学院',
      '广州番禺职业技术学院',
      '深圳信息职业技术学院',
      '顺德职业技术学院',
      '重庆电子工程职业学院',
      '重庆工业职业技术学院',
      '杨凌职业技术学院',
      '北京财贸职业学院',
      '天津轻工职业技术学院',
      '山西省财政税务专科学校',
      '内蒙古机电职业技术学院',
      '长春汽车工业高等专科学校',
      '哈尔滨职业技术学院',
      '上海工艺美术职业学院',
      '常州机电职业技术学院',
      '江苏经贸职业技术学院',
      '温州职业技术学院',
      '芜湖职业技术学院',
      '福建船政交通职业学院',
      '九江职业技术学院',
      '滨州职业学院',
      '武汉船舶职业技术学院',
      '湖南铁道职业技术学院',
      '南宁职业技术学院',
      '海南经贸职业技术学院',
      '四川工程职业技术学院',
      '贵州交通职业技术学院',
      '昆明冶金高等专科学校',
      '陕西铁路工程职业技术学院',
      '西安航空职业技术学院',
      '兰州资源环境职业技术学院',
      '宁夏职业技术学院',
      '新疆农业职业技术学院',
      '北京农业职业学院',
      '北京信息职业技术学院',
      '天津电子信息职业技术学院',
      '天津现代职业技术学院',
      '邢台职业技术学院',
      '山西工程职业学院',
      '辽宁农业职业技术学院',
      '长春职业技术学院',
      '黑龙江农业经济职业学院',
      '黑龙江建筑职业技术学院',
      '江苏建筑职业技术学院',
      '浙江建设职业技术学院',
      '安徽机电职业技术学院',
      '安徽商贸职业技术学院',
      '福建信息职业技术学院',
      '江西应用技术职业学院',
      '山东科技职业学院',
      '黄冈职业技术学院',
      '武汉职业技术学院',
      '湖南工业职业技术学院',
      '湖南工艺美术职业学院',
      '湖南汽车工程职业学院',
      '重庆城市管理职业学院',
      '成都航空职业技术学院',
      '四川交通职业技术学院',
      '兰州石化职业技术学院',
      '北京劳动保障职业学院',
      '天津交通职业学院',
      '石家庄铁路职业技术学院',
      '唐山工业职业技术学院',
      '山西机电职业技术学院',
      '山西职业技术学院',
      '内蒙古化工职业学院',
      '黑龙江职业学院',
      '黑龙江农业工程职业学院',
      '常州工程职业技术学院',
      '江苏工程职业技术学院',
      '江苏海事职业技术学院',
      '江苏食品药品职业技术学院',
      '南通航运职业技术学院',
      '苏州工艺美术职业技术学院',
      '苏州农业职业技术学院',
      '浙江交通职业技术学院',
      '浙江经济职业技术学院',
      '浙江经贸职业技术学院',
      '浙江旅游职业学院',
      '安徽水利水电职业技术学院',
      '福州职业技术学院',
      '黎明职业大学',
      '漳州职业技术学院',
      '江西财经职业学院',
      '江西环境工程职业学院',
      '江西交通职业技术学院',
      '济南职业学院',
      '青岛职业技术学院',
      '山东畜牧兽医职业学院',
      '山东交通职业学院',
      '威海职业学院',
      '潍坊职业学院',
      '烟台职业学院',
      '河南工业职业技术学院',
      '河南农业职业学院',
      '河南职业技术学院',
      '许昌职业技术学院',
      '郑州铁路职业技术学院',
      '武汉铁路职业技术学院',
      '襄阳职业技术学院',
      '长沙航空职业技术学院',
      '湖南化工职业技术学院',
      '广东科学技术职业学院',
      '广东水利电力职业技术学院',
      '广州铁路职业技术学院',
      '广西职业技术学院',
      '柳州职业技术学院',
      '重庆电力高等专科学校',
      '重庆工程职业技术学院',
      '重庆工商职业学院',
      '成都纺织高等专科学校',
      '成都职业技术学院',
      '四川建筑职业技术学院',
      '铜仁职业技术学院',
      '陕西国防工业职业技术学院',
      '陕西职业技术学院',
      '酒泉职业技术学院',
      '宁夏工商职业技术学院',
      '北京交通运输职业学院',
      '天津渤海职业技术学院',
      '沧州医学高等专科学校',
      '承德石油高等专科学校',
      '河北化工医药职业技术学院',
      '秦皇岛职业技术学院',
      '石家庄邮电职业技术学院',
      '石家庄职业技术学院',
      '内蒙古建筑职业技术学院',
      '渤海船舶职业学院',
      '辽宁机电职业技术学院',
      '辽宁经济职业技术学院',
      '沈阳职业技术学院',
      '吉林交通职业技术学院',
      '吉林铁道职业技术学院',
      '哈尔滨铁道职业技术学院',
      '南京铁道职业技术学院',
      '南通职业大学',
      '苏州工业职业技术学院',
      '无锡商业职业技术学院',
      '徐州工业职业技术学院',
      '浙江工贸职业技术学院',
      '浙江警官职业学院',
      '浙江商业职业技术学院',
      '浙江艺术职业学院',
      '安徽医学高等专科学校',
      '江西外语外贸职业学院',
      '东营职业学院',
      '青岛酒店管理职业技术学院',
      '山东职业学院',
      '湖北交通职业技术学院',
      '湖北职业技术学院',
      '武汉电力职业技术学院',
      '长沙商贸旅游职业技术学院',
      '湖南交通职业技术学院',
      '湖南生物机电职业技术学院',
      '岳阳职业技术学院',
      '东莞职业技术学院',
      '广东工贸职业技术学院',
      '广东机电职业技术学院',
      '广东食品药品职业学院',
      '广州民航职业技术学院',
      '中山火炬职业技术学院',
      '广西建设职业技术学院',
      '重庆航天职业技术学院',
      '重庆三峡医药高等专科学校',
      '重庆三峡职业学院',
      '重庆医药高等专科学校',
      '成都农业科技职业学院',
      '四川邮电职业技术学院',
      '贵州轻工职业技术学院',
      '昆明工业职业技术学院',
      '云南机电职业技术学院',
      '陕西能源职业技术学院',
      '咸阳职业技术学院',
      '新疆轻工职业技术学院'
    ])

    const baseMatch: any = { year: { $gte: 2014, $lte: 2022 } }
    if (params?.category) baseMatch.category = params.category

    // 按年+学校聚合，得到每年每校的招生数
    const perSchoolPerYear = (await (SchoolEnrollmentEntity as any).model.aggregate([
      { $match: baseMatch },
      {
        $group: {
          _id: { year: '$year', school: '$school_name' },
          enroll: { $sum: { $ifNull: ['$enrollment_count', 0] } }
        }
      },
      { $project: { _id: 0, year: '$_id.year', school: '$_id.school', enroll: 1 } },
      { $sort: { year: 1 } }
    ])) as Array<{ year: number; school: string; enroll: number }>

    // 构建映射：year -> { total, dhTotal, ndhTotal }
    const yearStats = new Map<number, { total: number; dhTotal: number; ndhTotal: number }>()
    for (const { year, school, enroll } of perSchoolPerYear) {
      if (!yearStats.has(year)) yearStats.set(year, { total: 0, dhTotal: 0, ndhTotal: 0 })
      const y = yearStats.get(year)!
      y.total += enroll || 0
      if (doubleHighSchool.has(school)) y.dhTotal += enroll || 0
      else y.ndhTotal += enroll || 0
    }

    const resultList: GraduateYearItem[] = []
    for (let year = 2017; year <= 2022; year++) {
      const y = yearStats.get(year) || { total: 0, dhTotal: 0, ndhTotal: 0 }
      const y1 = yearStats.get(year - 1) || { total: 0, dhTotal: 0, ndhTotal: 0 }
      const y2 = yearStats.get(year - 2) || { total: 0, dhTotal: 0, ndhTotal: 0 }
      const y3 = yearStats.get(year - 3) || { total: 0, dhTotal: 0, ndhTotal: 0 }

      const enrollmentNum = y.total
      const dhEnrollmentNum = y.dhTotal
      const ndhEnrollmentNum = y.ndhTotal

      const graduateNum = y3.total
      const dhGraduateNum = y3.dhTotal
      const ndhGraduateNum = y3.ndhTotal

      const inSchoolNum = y.total + y1.total + y2.total
      const dhInSchoolNum = y.dhTotal + y1.dhTotal + y2.dhTotal
      const ndhInSchoolNum = y.ndhTotal + y1.ndhTotal + y2.ndhTotal

      resultList.push({
        year,
        enrollmentNum,
        graduateNum,
        inSchoolNum,
        dhEnrollmentNum,
        ndhEnrollmentNum,
        dhGraduateNum,
        ndhGraduateNum,
        dhInSchoolNum,
        ndhInSchoolNum
      })
    }

    return { list: resultList }
  }

  static async getSchoolNum(): Promise<ResultItem[]> {
    console.log('📊 开始获取学校数量数据...')

    const pipeline: any[] = [
      { $match: { category: '专科', school_name: { $nin: [null, '', undefined] } } },
      { $group: { _id: '$school_name' } },
      { $project: { _id: 1 } }
    ]

    const uniqueSchools: Array<{ _id: string }> = await (SchoolEnrollmentEntity as any).model.aggregate(pipeline)
    const uniqueNames = new Set<string>(uniqueSchools.map((s) => s._id))

    const doubleHighSchool = new Set<string>([
      '北京电子科技职业学院',
      '天津市职业大学',
      '江苏农林职业技术学院',
      '无锡职业技术学院',
      '金华职业技术学院',
      '浙江机电职业技术学院',
      '山东商业职业技术学院',
      '黄河水利职业技术学院',
      '深圳职业技术学院',
      '陕西工业职业技术学院',
      '北京工业职业技术学院',
      '天津医学高等专科学校',
      '河北工业职业技术学院',
      '辽宁省交通高等专科学校',
      '常州信息职业技术学院',
      '江苏农牧科技职业学院',
      '南京信息职业技术学院',
      '杭州职业技术学院',
      '宁波职业技术学院',
      '浙江金融职业学院',
      '日照职业技术学院',
      '淄博职业学院',
      '长沙民政职业技术学院',
      '广东轻工职业技术学院',
      '广州番禺职业技术学院',
      '深圳信息职业技术学院',
      '顺德职业技术学院',
      '重庆电子工程职业学院',
      '重庆工业职业技术学院',
      '杨凌职业技术学院',
      '北京财贸职业学院',
      '天津轻工职业技术学院',
      '山西省财政税务专科学校',
      '内蒙古机电职业技术学院',
      '长春汽车工业高等专科学校',
      '哈尔滨职业技术学院',
      '上海工艺美术职业学院',
      '常州机电职业技术学院',
      '江苏经贸职业技术学院',
      '温州职业技术学院',
      '芜湖职业技术学院',
      '福建船政交通职业学院',
      '九江职业技术学院',
      '滨州职业学院',
      '武汉船舶职业技术学院',
      '湖南铁道职业技术学院',
      '南宁职业技术学院',
      '海南经贸职业技术学院',
      '四川工程职业技术学院',
      '贵州交通职业技术学院',
      '昆明冶金高等专科学校',
      '陕西铁路工程职业技术学院',
      '西安航空职业技术学院',
      '兰州资源环境职业技术学院',
      '宁夏职业技术学院',
      '新疆农业职业技术学院',
      '北京农业职业学院',
      '北京信息职业技术学院',
      '天津电子信息职业技术学院',
      '天津现代职业技术学院',
      '邢台职业技术学院',
      '山西工程职业学院',
      '辽宁农业职业技术学院',
      '长春职业技术学院',
      '黑龙江农业经济职业学院',
      '黑龙江建筑职业技术学院',
      '江苏建筑职业技术学院',
      '浙江建设职业技术学院',
      '安徽机电职业技术学院',
      '安徽商贸职业技术学院',
      '福建信息职业技术学院',
      '江西应用技术职业学院',
      '山东科技职业学院',
      '黄冈职业技术学院',
      '武汉职业技术学院',
      '湖南工业职业技术学院',
      '湖南工艺美术职业学院',
      '湖南汽车工程职业学院',
      '重庆城市管理职业学院',
      '成都航空职业技术学院',
      '四川交通职业技术学院',
      '兰州石化职业技术学院',
      '北京劳动保障职业学院',
      '天津交通职业学院',
      '石家庄铁路职业技术学院',
      '唐山工业职业技术学院',
      '山西机电职业技术学院',
      '山西职业技术学院',
      '内蒙古化工职业学院',
      '黑龙江职业学院',
      '黑龙江农业工程职业学院',
      '常州工程职业技术学院',
      '江苏工程职业技术学院',
      '江苏海事职业技术学院',
      '江苏食品药品职业技术学院',
      '南通航运职业技术学院',
      '苏州工艺美术职业技术学院',
      '苏州农业职业技术学院',
      '浙江交通职业技术学院',
      '浙江经济职业技术学院',
      '浙江经贸职业技术学院',
      '浙江旅游职业学院',
      '安徽水利水电职业技术学院',
      '福州职业技术学院',
      '黎明职业大学',
      '漳州职业技术学院',
      '江西财经职业学院',
      '江西环境工程职业学院',
      '江西交通职业技术学院',
      '济南职业学院',
      '青岛职业技术学院',
      '山东畜牧兽医职业学院',
      '山东交通职业学院',
      '威海职业学院',
      '潍坊职业学院',
      '烟台职业学院',
      '河南工业职业技术学院',
      '河南农业职业学院',
      '河南职业技术学院',
      '许昌职业技术学院',
      '郑州铁路职业技术学院',
      '武汉铁路职业技术学院',
      '襄阳职业技术学院',
      '长沙航空职业技术学院',
      '湖南化工职业技术学院',
      '广东科学技术职业学院',
      '广东水利电力职业技术学院',
      '广州铁路职业技术学院',
      '广西职业技术学院',
      '柳州职业技术学院',
      '重庆电力高等专科学校',
      '重庆工程职业技术学院',
      '重庆工商职业学院',
      '成都纺织高等专科学校',
      '成都职业技术学院',
      '四川建筑职业技术学院',
      '铜仁职业技术学院',
      '陕西国防工业职业技术学院',
      '陕西职业技术学院',
      '酒泉职业技术学院',
      '宁夏工商职业技术学院',
      '北京交通运输职业学院',
      '天津渤海职业技术学院',
      '沧州医学高等专科学校',
      '承德石油高等专科学校',
      '河北化工医药职业技术学院',
      '秦皇岛职业技术学院',
      '石家庄邮电职业技术学院',
      '石家庄职业技术学院',
      '内蒙古建筑职业技术学院',
      '渤海船舶职业学院',
      '辽宁机电职业技术学院',
      '辽宁经济职业技术学院',
      '沈阳职业技术学院',
      '吉林交通职业技术学院',
      '吉林铁道职业技术学院',
      '哈尔滨铁道职业技术学院',
      '南京铁道职业技术学院',
      '南通职业大学',
      '苏州工业职业技术学院',
      '无锡商业职业技术学院',
      '徐州工业职业技术学院',
      '浙江工贸职业技术学院',
      '浙江警官职业学院',
      '浙江商业职业技术学院',
      '浙江艺术职业学院',
      '安徽医学高等专科学校',
      '江西外语外贸职业学院',
      '东营职业学院',
      '青岛酒店管理职业技术学院',
      '山东职业学院',
      '湖北交通职业技术学院',
      '湖北职业技术学院',
      '武汉电力职业技术学院',
      '长沙商贸旅游职业技术学院',
      '湖南交通职业技术学院',
      '湖南生物机电职业技术学院',
      '岳阳职业技术学院',
      '东莞职业技术学院',
      '广东工贸职业技术学院',
      '广东机电职业技术学院',
      '广东食品药品职业学院',
      '广州民航职业技术学院',
      '中山火炬职业技术学院',
      '广西建设职业技术学院',
      '重庆航天职业技术学院',
      '重庆三峡医药高等专科学校',
      '重庆三峡职业学院',
      '重庆医药高等专科学校',
      '成都农业科技职业学院',
      '四川邮电职业技术学院',
      '贵州轻工职业技术学院',
      '昆明工业职业技术学院',
      '云南机电职业技术学院',
      '陕西能源职业技术学院',
      '咸阳职业技术学院',
      '新疆轻工职业技术学院'
    ])

    let doubleHighCount = 0
    for (const name of uniqueNames) {
      if (doubleHighSchool.has(name)) doubleHighCount++
    }
    const nonDoubleHigh = uniqueNames.size - doubleHighCount

    const result: ResultItem[] = [
      { name: '双高大专院校', value: doubleHighCount, rank: 1 },
      { name: '非双高大专院校', value: nonDoubleHigh, rank: 2 }
    ]

    return result
  }

  private static generateStableSessionId(params: any): string {
    // 标准化参数，确保相同内容的对象生成相同的hash
    const normalizedParams = {
      dateType: params.dateType,
      caliberType: params.caliberType
    }
    const paramsStr = JSON.stringify(normalizedParams)
    const hash = require('crypto').createHash('md5').update(paramsStr).digest('hex')
    // 获取当前日期（YYYY-MM-DD格式）
    const today = new Date().toISOString().split('T')[0]
    return `screen_${today}_${hash.substring(0, 12)}`
  }

  static async getMajorByPosition(): Promise<MajorByPositionResult[]> {
    console.log('📊 开始获取专业对应岗位数据...')

    try {
      // 1. 从Position服务获取热门岗位对应的职业数据
      const { PositionService } = await import('../Position/Position.service')
      const service = new PositionService()

      // 获取基础数据（包含热门职业排行）
      const params = { dateType: 'month', caliberType: 'college' }
      const sessionId = this.generateStableSessionId(params)
      const baseData = await (service as any).getBaseData(params, sessionId)

      if (!baseData.careerRanking || baseData.careerRanking.length === 0) {
        console.log('未找到热门职业排行数据')
        return []
      }

      console.log('获取到热门职业排行数据:', baseData.careerRanking.length, '个职业', baseData.careerRanking)

      // 2. 获取职业映射数据，建立第三级职业到第四级职业编码的映射
      const jobMappings = baseData.jobMappings || []
      const thirdToFourthLevelMap = new Map<string, { name: string; code: string }[]>()

      jobMappings.forEach((mapping: any) => {
        if (
          mapping.standard_classification?.xilei?.primary?.name &&
          mapping.standard_classification?.xilei?.primary?.code &&
          mapping.standard_classification?.xiaoli?.primary?.name
        ) {
          // 修正：xiaoli是第三级，xilei是第四级
          const thirdLevel = mapping.standard_classification.xiaoli.primary.name
          const fourthLevelName = mapping.standard_classification.xilei.primary.name
          const fourthLevelCode = mapping.standard_classification.xilei.primary.code

          if (!thirdToFourthLevelMap.has(thirdLevel)) {
            thirdToFourthLevelMap.set(thirdLevel, [])
          }
          thirdToFourthLevelMap.get(thirdLevel)!.push({
            name: fourthLevelName,
            code: fourthLevelCode
          })
        }
      })

      console.log('第三级到第四级职业映射数量:', thirdToFourthLevelMap.size)

      // 3. 收集前五条热门职业对应的第四级职业编码
      const fourthLevelCareerCodes = new Set<string>()
      const fourthLevelCareerNames = new Set<string>()

      // 只取前五条热门职业
      const topFiveCareers = baseData.careerRanking.slice(0, 5)
      console.log(
        '前五条热门职业:',
        topFiveCareers.map((c: any) => c.name)
      )

      topFiveCareers.forEach((career: any) => {
        const thirdLevelCareer = career.name
        const fourthLevelCareersForThird = thirdToFourthLevelMap.get(thirdLevelCareer) || []
        fourthLevelCareersForThird.forEach((fourthLevel) => {
          fourthLevelCareerCodes.add(fourthLevel.code)
          fourthLevelCareerNames.add(fourthLevel.name)
        })
      })

      console.log('需要查询的第四级职业编码数量:', fourthLevelCareerCodes.size, Array.from(fourthLevelCareerCodes))
      console.log('需要查询的第四级职业名称数量:', fourthLevelCareerNames.size, Array.from(fourthLevelCareerNames))

      // 4. 根据第四级职业编码查询JobMajorMapping表（仅匹配学历层次包含“专科”的记录）
      const majorMappings = await (JobMajorMappingEntity as any).model
        .find({
          job_code: { $in: Array.from(fourthLevelCareerCodes) },
          education_level: { $regex: '专科' }
        })
        .lean()

      console.log('查询到的专业映射数据数量:', majorMappings.length)

      // 5. 按职业分组，每个职业对应多个专业
      const jobToMajorsMap = new Map<
        string,
        {
          job_name: string
          job_code: string
          majors: Array<{
            major_name: string
            major_code: string
            education_level: string
          }>
        }
      >()

      majorMappings.forEach((mapping: any) => {
        const jobKey = `${mapping.job_code}_${mapping.job_name}`

        if (!jobToMajorsMap.has(jobKey)) {
          jobToMajorsMap.set(jobKey, {
            job_name: mapping.job_name,
            job_code: mapping.job_code,
            majors: []
          })
        }

        const jobData = jobToMajorsMap.get(jobKey)!

        // 检查是否已存在相同的专业（避免重复）
        const existingMajor = jobData.majors.find(
          (m) =>
            m.major_name === mapping.major_name &&
            m.major_code === mapping.major_code &&
            m.education_level === mapping.education_level
        )

        if (!existingMajor) {
          jobData.majors.push({
            major_name: mapping.major_name,
            major_code: mapping.major_code,
            education_level: mapping.education_level
          })
        }
      })

      // 6. 转换为结果格式，按专业数量排序
      const result: MajorByPositionResult[] = Array.from(jobToMajorsMap.values())
        .map((jobData) => ({
          job_name: jobData.job_name,
          job_code: jobData.job_code,
          major_name: jobData.majors.map((m) => m.major_name),
          major_code: jobData.majors.map((m) => m.major_code),
          education_level: jobData.majors.map((m) => m.education_level),
          count: jobData.majors.length
        }))
        .sort((a, b) => b.count - a.count)

      console.log('最终返回的专业数据数量:', result.length)

      return result
    } catch (error) {
      console.error('获取专业对应岗位数据失败:', error)
      throw error
    }
  }
}
