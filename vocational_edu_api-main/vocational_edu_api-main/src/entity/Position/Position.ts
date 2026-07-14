import { createEntityService } from '@havenzhang/clover'
import { PositionDtoType } from '../../base/entity/Position/Position.dto'
import { PositionModel, PositionSchema1, createPositionModel1 } from '../../base/entity/Position/Position.model'
import endpoint from '../../endpoints/Position'
const positionModel = createPositionModel1(PositionSchema1)
export const PositionEntity = createEntityService<PositionModel, PositionDtoType>(endpoint, positionModel)
