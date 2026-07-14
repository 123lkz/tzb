import { createEntityService } from '@havenzhang/clover'
import endpoint from '../../endpoints/Company'
import { createCompanyModel, CompanyModel, CompanySchema } from '../../base/entity/Company/Company.model'
import { CompanyDtoType } from '../../base/entity/Company/Company.dto'
const companyModel = createCompanyModel(CompanySchema)
export const CompanyEntity = createEntityService<CompanyModel, CompanyDtoType>(endpoint, companyModel)
