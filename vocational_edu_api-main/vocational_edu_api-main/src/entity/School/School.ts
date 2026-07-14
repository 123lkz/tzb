import { createEntityService, RestModel } from '@havenzhang/clover'
import { SchoolDtoType } from '../../base/entity/School/School.dto'
import { SchoolModel, SchoolSchema } from '../../base/entity/School/School.model'
import endpoint from '../../endpoints/Schools'
import { connections } from '../../utils/DatabaseUtils'

if (!connections.da) {
  require('../../database')
}

const schoolModel = connections.da.model<SchoolModel, RestModel<SchoolModel, SchoolDtoType>>('School', SchoolSchema)
export const SchoolEntity = createEntityService<SchoolModel, SchoolDtoType>(endpoint, schoolModel)
