import { Get, Post, Patch, Put, Delete, Body, Param, Query, Headers } from '@nestjs/common'
import { ApiResponse, ApiBody, ApiHeader, ApiExtension } from '@nestjs/swagger'
import { Description, CloverController, Etag, User, IUser, CheckRoles, RestFilter, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { UserEntity } from '../../../entity/User/User'
import { UserCombinedId, ReplaceUser, CreateUser, UpdateUser, GetUserResult, ListUserResult, UserListQueryValidator } from './User.dto'
import { CheckOwner } from '../../../plugins/CheckOwner'

@CloverController(UserEntity)
export class UserControllerBase {
  protected readonly user = UserEntity

  @Get('/User')
  @ApiResponse({ type: ListUserResult })
  @ApiExtension('x-lookup-property', ['_id', 'phone', 'registerAt', 'roles'])
  @CheckRoles('supervisor')
  @Description('监管：获取用户列表')
  list(@User() user: IUser, @Query() listQuery: ListQuery): Promise<ListUserResult> {
    return this.user.query(user, listQuery, { queryValidator: UserListQueryValidator })
  }

  @Patch('/User/:combinedId')
  @ApiResponse({ type: MutateResult })
  @CheckOwner('_id')
  @CheckRoles('user')
  @Description('用户：更新信息')
  update(@User() user: IUser, @CombinedId() combinedId: UserCombinedId, @Body() input: UpdateUser, @Etag() etag: string): Promise<MutateResult> {
    return this.user.update(user, combinedId, etag, input)
  }
}
