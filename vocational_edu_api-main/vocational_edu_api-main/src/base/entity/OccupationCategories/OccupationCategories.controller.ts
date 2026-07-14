import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import { Description, CloverController, Etag, User, IUser, CheckRoles, RestFilter, CombinedId, RemoveResult, MutateResult, ListQueryWithPaging } from '@havenzhang/clover'
import { OccupationCategoriesEntity } from '../../../entity/OccupationCategories/OccupationCategories'
import { OccupationCategoriesCombinedId, ReplaceOccupationCategories, CreateOccupationCategories, UpdateOccupationCategories, GetOccupationCategoriesResult, ListOccupationCategoriesResult, OccupationCategoriesListQueryValidator } from './OccupationCategories.dto'

@CloverController(OccupationCategoriesEntity)
export class OccupationCategoriesControllerBase {
  protected readonly occupationCategories = OccupationCategoriesEntity

  @Get('/OccupationCategories')
  @ApiResponse({ type: ListOccupationCategoriesResult })
  @ApiExtension('x-lookup-property', ['_id', 'code', 'level', 'name'])
  @Description('获取职业分类列表')
  list(@User() user: IUser, @Query() listQuery: ListQueryWithPaging): Promise<ListOccupationCategoriesResult> {
    return this.occupationCategories.query(user, listQuery, { queryValidator: OccupationCategoriesListQueryValidator })
  }
}
