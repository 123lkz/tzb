import { CloverApiProperty, Joi } from '@havenzhang/clover'

/**
 * 基础数据查询参数
 * 用于数据大屏相关的所有查询
 */
export class BaseQueryParams {
  @CloverApiProperty({ description: '年度/月度', validator: Joi.string().format('text').max(50) })
  dateType?: 'year' | 'month'

  @CloverApiProperty({
    description: '全口径/应届大专生',
    validator: Joi.string().format('text').max(50)
  })
  caliberType?: 'all' | 'college'
}
