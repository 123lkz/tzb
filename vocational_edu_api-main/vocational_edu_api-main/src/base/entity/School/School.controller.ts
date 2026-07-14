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
import { SchoolEntity } from '../../../entity/School/School'
import {
  SchoolCombinedId,
  ReplaceSchool,
  CreateSchool,
  UpdateSchool,
  GetSchoolResult,
  ListSchoolResult,
  SchoolListQueryValidator
} from './School.dto'

@CloverController(SchoolEntity)
export class SchoolControllerBase {
  protected readonly school = SchoolEntity

  @Get('/School')
  @ApiResponse({ type: ListSchoolResult })
  @ApiExtension('x-lookup-property', [
    '_id',
    'is211',
    'is985',
    'isCenter',
    'isDoubleHigh',
    'isDoubleTop',
    'isLocal',
    'level',
    'location',
    'manager',
    'note',
    'openState',
    'province',
    'school',
    'schoolCode'
  ])
  @Description('获取学校列表')
  list(@User() user: IUser, @Query() listQuery: ListQueryWithPaging): Promise<ListSchoolResult> {
    return this.school.query(user, listQuery, { queryValidator: SchoolListQueryValidator })
  }
}
