import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class SchoolParams {
  @CloverApiProperty({ description: '办学层次', validator: Joi.string().format('text').max(50) })
  level?: string
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

export class SchoolNumResult {
  @CloverApiProperty({ description: '全部院校数量', validator: Joi.number().min(0) })
  allSchoolNum: number
  @CloverApiProperty({ description: '双高院校数量', validator: Joi.number().min(0) })
  doubleHighNum: number
  @CloverApiProperty({ description: '本科院校数量', validator: Joi.number().min(0) })
  undergraduateNum: number
  @CloverApiProperty({ description: '专科院校数量', validator: Joi.number().min(0) })
  specialtyNum: number
}
