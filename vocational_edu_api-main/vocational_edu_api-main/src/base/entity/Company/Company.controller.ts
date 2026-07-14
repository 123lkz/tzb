import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import { Description, CloverController, Etag, User, IUser, CheckRoles, RestFilter, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { CompanyEntity } from '../../../entity/Company/Company'
import { CompanyCombinedId, ReplaceCompany, CreateCompany, UpdateCompany, GetCompanyResult, ListCompanyResult, CompanyListQueryValidator } from './Company.dto'
import { CheckOwner } from '../../../plugins/CheckOwner'

@CloverController(CompanyEntity)
export class CompanyControllerBase {
  protected readonly company = CompanyEntity

  @Get('/Company')
  @ApiResponse({ type: ListCompanyResult })
  @ApiExtension('x-lookup-property', ['_id', 'company_name', 'create_time'])
  @Description('获取公司列表')
  list(@User() user: IUser, @Query() listQuery: ListQuery): Promise<ListCompanyResult> {
    return this.company.query(user, listQuery, { queryValidator: CompanyListQueryValidator })
  }
}
