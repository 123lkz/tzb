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
import { SchoolEnrollmentEntity } from '../../../entity/SchoolEnrollment/SchoolEnrollment'
import {
  SchoolEnrollmentCombinedId,
  ReplaceSchoolEnrollment,
  CreateSchoolEnrollment,
  UpdateSchoolEnrollment,
  GetSchoolEnrollmentResult,
  ListSchoolEnrollmentResult,
  SchoolEnrollmentListQueryValidator
} from './SchoolEnrollment.dto'

@CloverController(SchoolEnrollmentEntity)
export class SchoolEnrollmentControllerBase {
  protected readonly schoolEnrollment = SchoolEnrollmentEntity
}
