import { CloverApiProperty, Joi } from '@havenzhang/clover'

export class OccupationUpQuery {
  @CloverApiProperty({
    description: '级别(1/2/3/4)',
    validator: Joi.number().integer().min(1).max(4).required()
  })
  level!: 1 | 2 | 3 | 4

  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200) })
  name?: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50) })
  code?: string
}

export class SimpleItem {
  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200) })
  name!: string
  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50) })
  code!: string
}

export class OccupationUpResult {
  @CloverApiProperty({ description: '大类(1级)', type: [SimpleItem] })
  dalei: SimpleItem[]
  @CloverApiProperty({ description: '中类(2级)', type: [SimpleItem] })
  zhonglei: SimpleItem[]
  @CloverApiProperty({ description: '小类(3级)', type: [SimpleItem] })
  xiaoli: SimpleItem[]
  @CloverApiProperty({ description: '细类(4级，若请求level=4则返回)', type: [SimpleItem] })
  xilei: SimpleItem[]
}

export class OccupationDownQuery {
  @CloverApiProperty({
    description: '父级小类编码(3级)',
    validator: Joi.string().format('text').max(50)
  })
  code?: string
  @CloverApiProperty({
    description: '父级小类名称(3级)',
    validator: Joi.string().format('text').max(200)
  })
  name?: string
}

export class OccupationDownResult {
  @CloverApiProperty({ description: '大类(1级)列表', type: [SimpleItem] })
  dalei?: SimpleItem[]
  @CloverApiProperty({ description: '中类(2级)列表', type: [SimpleItem] })
  zhonglei?: SimpleItem[]
  @CloverApiProperty({ description: '小类(3级)列表', type: [SimpleItem] })
  xiaoli?: SimpleItem[]
  @CloverApiProperty({ description: '细类(4级)列表', type: [SimpleItem] })
  xilei: SimpleItem[]
}

export class GradeTreeItem {
  @CloverApiProperty({
    description: '级别(1/2/3/4)',
    validator: Joi.number().integer().min(1).max(4).required()
  })
  level!: 1 | 2 | 3 | 4

  @CloverApiProperty({ description: '名称', validator: Joi.string().format('text').max(200) })
  name!: string

  @CloverApiProperty({ description: '编码', validator: Joi.string().format('text').max(50) })
  code!: string

  @CloverApiProperty({ description: '子级列表' })
  children?: any
}
