import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class SchoolParams {
  @CloverApiProperty({ description: '办学层次', validator: Joi.string().format('text').max(50) })
  category?: string
}

export class YearParams extends SchoolParams {
  @CloverApiProperty({
    description: '年份',
    required: false,
    validator: Joi.number().integer().optional()
  })
  year?: number
}

export class provinceParams {
  @CloverApiProperty({ description: '省份', validator: Joi.string().format('text').max(50) })
  name?: string
}

export class ResultItem {
  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(50) })
  name: string
  @CloverApiProperty({ description: '数量', validator: Joi.number().min(0) })
  value: number
  @CloverApiProperty({ description: '排名', validator: Joi.number().min(0) })
  rank?: number
}

export class ProvinceSchoolResult {
  @CloverApiProperty({ description: '省份分布数据', type: [ResultItem] })
  provinceData: ResultItem[]
}

export class ProvinceSchoolNumItem extends ResultItem {
  @CloverApiProperty({ description: '双高院校数量', validator: Joi.number().min(0) })
  doubleHighNum: number
}

export class GraduateYearItem {
  @CloverApiProperty({ description: '年份', validator: Joi.number().integer().min(2016).max(2022) })
  year: number
  @CloverApiProperty({ description: '招生人数', validator: Joi.number().min(0) })
  enrollmentNum: number
  @CloverApiProperty({ description: '毕业生人数', validator: Joi.number().min(0) })
  graduateNum: number
  @CloverApiProperty({ description: '在校学生数', validator: Joi.number().min(0) })
  inSchoolNum: number

  @CloverApiProperty({ description: '双高院校招生人数', validator: Joi.number().min(0) })
  dhEnrollmentNum: number
  @CloverApiProperty({ description: '非双高院校招生人数', validator: Joi.number().min(0) })
  ndhEnrollmentNum: number

  @CloverApiProperty({ description: '双高院校毕业生人数', validator: Joi.number().min(0) })
  dhGraduateNum: number
  @CloverApiProperty({ description: '非双高院校毕业生人数', validator: Joi.number().min(0) })
  ndhGraduateNum: number

  @CloverApiProperty({ description: '双高院校在校学生数', validator: Joi.number().min(0) })
  dhInSchoolNum: number
  @CloverApiProperty({ description: '非双高院校在校学生数', validator: Joi.number().min(0) })
  ndhInSchoolNum: number
}

export class GraduateNumResult {
  @CloverApiProperty({ description: '2016-2022年各年学生数量', type: [GraduateYearItem] })
  list: GraduateYearItem[]
}

export class MajorByPositionResult {
  @CloverApiProperty({ description: '专业名称列表', type: [String] })
  major_name: string[]

  @CloverApiProperty({ description: '专业代码列表', type: [String] })
  major_code: string[]

  @CloverApiProperty({ description: '学历层次列表', type: [String] })
  education_level: string[]

  @CloverApiProperty({
    description: '对应职业名称',
    validator: Joi.string().format('text').max(200)
  })
  job_name: string

  @CloverApiProperty({
    description: '对应职业编码',
    validator: Joi.string().format('text').max(100)
  })
  job_code: string

  @CloverApiProperty({ description: '匹配数量', validator: Joi.number().min(0) })
  count: number
}

export class SpecialtySchoolNumResult {
  @CloverApiProperty({ description: '专科学校数量', validator: Joi.number().min(0) })
  specialtySchoolNum: number
  @CloverApiProperty({ description: '双高院校数量', validator: Joi.number().min(0) })
  doubleHighSchoolNum: number
  @CloverApiProperty({ description: '非双高院校数量', validator: Joi.number().min(0) })
  nonDoubleHighSchoolNum: number
}

export class MajorByPositionResult1 {
  @CloverApiProperty({ description: '专业名', validator: Joi.string().format('text').max(100) })
  name: string
  @CloverApiProperty({ description: '数量', validator: Joi.number().min(0) })
  value: number
  @CloverApiProperty({ description: '对应的职业', type: [String] })
  professionName: string[]
}
