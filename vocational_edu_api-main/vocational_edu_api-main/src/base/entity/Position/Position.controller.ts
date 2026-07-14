import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import { Description, CloverController, Etag, User, IUser, CheckRoles, RestFilter, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { PositionEntity } from '../../../entity/Position/Position'
import { PositionCombinedId, ReplacePosition, CreatePosition, UpdatePosition, GetPositionResult, ListPositionResult, PositionListQueryValidator } from './Position.dto'
import { CheckOwner } from '../../../plugins/CheckOwner'

@CloverController(PositionEntity)
export class PositionControllerBase {
  protected readonly position = PositionEntity

  @Get('/Position')
  @ApiResponse({ type: ListPositionResult })
  @ApiExtension('x-lookup-property', ['_id', 'bossCert', 'brandIndustry', 'brandName', 'brandScaleName', 'businessDistrict', 'cityName', 'create_time', 'jobDegree', 'jobExperience', 'jobName', 'salaryDesc', 'skills'])
  @Description('获取职位列表')
  list(@User() user: IUser, @Query() listQuery: ListQuery): Promise<ListPositionResult> {
    return this.position.query(user, listQuery, { queryValidator: PositionListQueryValidator })
  }
}
