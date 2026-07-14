import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class IndustryUpQuery {
  @CloverApiProperty({ description: '级别(2/3/4/5)', validator: Joi.number().integer().min(2).max(5).required() })
  level!: 2 | 3 | 4 | 5

  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200).optional() })
  name?: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50).optional() })
  code?: string
}

export class IndustryDownQuery {
  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200).optional() })
  name?: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50).optional() })
  code?: string
}

export class SimpleItem {
  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200) })
  name!: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50) })
  code!: string
}

export class IndustryUpResult {
  @CloverApiProperty({ description: '大类(1级)列表', type: [SimpleItem] })
  dalei: SimpleItem[]

  @CloverApiProperty({ description: '中类(2级)列表', type: [SimpleItem] })
  zhonglei: SimpleItem[]

  @CloverApiProperty({ description: '小类(3级)列表', type: [SimpleItem] })
  xiaoli: SimpleItem[]

  @CloverApiProperty({ description: '细类(4级)列表', type: [SimpleItem] })
  xilei: SimpleItem[]

  @CloverApiProperty({ description: '子类(5级)列表', type: [SimpleItem] })
  zilei: SimpleItem[]
}

export class IndustryDownResult {
  @CloverApiProperty({ description: '大类(1级)列表', type: [SimpleItem] })
  dalei?: SimpleItem[]

  @CloverApiProperty({ description: '中类(2级)列表', type: [SimpleItem] })
  zhonglei?: SimpleItem[]

  @CloverApiProperty({ description: '小类(3级)列表', type: [SimpleItem] })
  xiaoli?: SimpleItem[]

  @CloverApiProperty({ description: '细类(4级)列表', type: [SimpleItem] })
  xilei?: SimpleItem[]

  @CloverApiProperty({ description: '子类(5级)列表', type: [SimpleItem] })
  zilei: SimpleItem[]
}

export class GradeTreeItem {
  @CloverApiProperty({ description: '级别(2/3/4/5)', validator: Joi.number().integer().min(2).max(5).required() })
  level!: 2 | 3 | 4 | 5

  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200) })
  name!: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50) })
  code!: string

  @CloverApiProperty({ description: '子级列表', required: false })
  children?: any
}
