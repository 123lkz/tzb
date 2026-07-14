import { createEntityService } from '@havenzhang/clover'
import { OccupationCategoriesDtoType } from '../../base/entity/OccupationCategories/OccupationCategories.dto'
import {
  createOccupationCategoriesModel,
  OccupationCategoriesModel,
  OccupationCategoriesSchema
} from '../../base/entity/OccupationCategories/OccupationCategories.model'
import endpoint from '../../endpoints/OccupationCategories'
const occupationCategoriesModel = createOccupationCategoriesModel(OccupationCategoriesSchema)
export const OccupationCategoriesEntity = createEntityService<OccupationCategoriesModel, OccupationCategoriesDtoType>(
  endpoint,
  occupationCategoriesModel
)
