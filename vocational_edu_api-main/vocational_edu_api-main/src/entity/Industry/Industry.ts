import { createEntityService, RestModel } from '@havenzhang/clover'
import { IndustryDtoType } from '../../base/entity/Industry/Industry.dto'
import { IndustryModel, IndustrySchema } from '../../base/entity/Industry/Industry.model'
import endpoint from '../../endpoints/Industry'
import { connections } from '../../utils/DatabaseUtils'

// 确保在使用前触发数据库初始化
if (!connections.main) {
  require('../../database')
}

const industryModel = connections.main.model<IndustryModel, RestModel<IndustryModel, IndustryDtoType>>(
  'Industry',
  IndustrySchema
)
export const IndustryEntity = createEntityService<IndustryModel, IndustryDtoType>(endpoint, industryModel)
