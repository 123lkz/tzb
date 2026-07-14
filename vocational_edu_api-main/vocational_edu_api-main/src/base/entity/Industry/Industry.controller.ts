import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import {
  Description,
  CloverController,
  Etag,
  User,
  IUser,
  CheckRoles,
  RestFilter,
  CombinedId,
  RemoveResult,
  MutateResult,
  ListQueryWithPaging
} from '@havenzhang/clover'
import { IndustryEntity } from '../../../entity/Industry/Industry'
import {
  IndustryCombinedId,
  ReplaceIndustry,
  CreateIndustry,
  UpdateIndustry,
  GetIndustryResult,
  ListIndustryResult,
  IndustryListQueryValidator
} from './Industry.dto'

@CloverController(IndustryEntity)
export class IndustryControllerBase {
  protected readonly industry = IndustryEntity

  @Get('/Industry')
  @ApiResponse({ type: ListIndustryResult })
  @ApiExtension('x-lookup-property', ['_id', 'code', 'level', 'name'])
  @Description('获取职业分类列表')
  list(@User() user: IUser, @Query() listQuery: ListQueryWithPaging): Promise<ListIndustryResult> {
    return this.industry.query(user, listQuery, { queryValidator: IndustryListQueryValidator })
  }
}
