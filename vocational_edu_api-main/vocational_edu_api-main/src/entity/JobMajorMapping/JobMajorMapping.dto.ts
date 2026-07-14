import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class JobMajorMappingDto {
  @CloverApiProperty({ description: 'ID', validator: Joi.string().format('text').max(50) })
  _id?: string

  @CloverApiProperty({ description: '职业编码', validator: Joi.string().format('text').max(100) })
  job_code: string

  @CloverApiProperty({ description: '职业名称', validator: Joi.string().format('text').max(200) })
  job_name: string

  @CloverApiProperty({ description: '专业代码', validator: Joi.string().format('text').max(100) })
  major_code: string

  @CloverApiProperty({ description: '专业名称', validator: Joi.string().format('text').max(200) })
  major_name: string

  @CloverApiProperty({ description: '学历层次', validator: Joi.string().format('text').max(50) })
  education_level: string
}

export class MajorByPositionResult {
  @CloverApiProperty({ description: '专业名称', validator: Joi.string().format('text').max(200) })
  major_name: string

  @CloverApiProperty({ description: '专业代码', validator: Joi.string().format('text').max(100) })
  major_code: string

  @CloverApiProperty({ description: '学历层次', validator: Joi.string().format('text').max(50) })
  education_level: string

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
