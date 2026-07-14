import { Get, Post, Patch, Put, Delete, Body, Query, Headers, UseGuards } from '@nestjs/common'
import { ApiResponse, ApiTags, ApiExcludeController } from '@nestjs/swagger'
import { Description, CloverAPIAccountGuard, CloverController, CombinedId, RemoveResult, MutateResult, ListQuery } from '@havenzhang/clover'
import { UserCombinedId, AdminGetUserResult, AdminListUserResult, AdminUpdateUser, AdminCreateUser, AdminUserListQueryValidator } from './User.dto'
import { UserEntity } from '../../../entity/User/User'

@CloverController(UserEntity)
@ApiTags('用户账户')
@UseGuards(CloverAPIAccountGuard)
export class UserControllerAdmin {
  private readonly user = UserEntity

  @Get('/User')
  @ApiResponse({ type: () => AdminListUserResult })
  @Description('获取用户账户列表')
  list(@Query() listQuery: ListQuery) {
    return this.user.query({}, listQuery, { queryValidator: AdminUserListQueryValidator }, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Post('/User')
  @ApiResponse({ type: MutateResult })
  @Description('创建用户账户')
  create(@Body() input: AdminCreateUser): Promise<MutateResult> {
    return this.user.create({}, input)
  }

  @Patch('/User/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('更新用户账户')
  update(@CombinedId() combinedId: UserCombinedId, @Body() input: AdminUpdateUser, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.user.update({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Put('/User/:combinedId')
  @ApiResponse({ type: MutateResult })
  @Description('替换用户账户')
  replace(@CombinedId() combinedId: UserCombinedId, @Body() input: AdminCreateUser, @Headers('If-Match') etag: string): Promise<MutateResult> {
    return this.user.replace({}, combinedId, etag, input, { skipSoftDelete: true, skipEtagCheck: true })
  }

  @Get('/User/:combinedId')
  @ApiResponse({ type: () => AdminGetUserResult })
  @Description('获取用户账户')
  getOne(@CombinedId() combinedId: UserCombinedId) {
    return this.user.model.restGetOne(combinedId, { skipSoftDelete: true, skipProjectionCheck: true })
  }

  @Delete('/User/:combinedId')
  @ApiResponse({ type: RemoveResult })
  @Description('删除用户账户')
  remove(@CombinedId() combinedId: UserCombinedId, @Headers('If-Match') etag: string, @Query('force') force?: boolean): Promise<RemoveResult> {
    return this.user.remove({}, combinedId, etag, force ? { skipSoftDelete: true, skipEtagCheck: true } : {})
  }

  @Get('/User/_collection_stat')
  @Description('Stat用户账户')
  async statCollection() {
    const ret = (await this.user.model.aggregate([{ $collStats: { storageStats: {} } }], { skipSoftDelete: true }))[0]
    return {
      size: ret.storageStats.size,
      count: ret.storageStats.count,
      avgObjSize: ret.storageStats.avgObjSize,
      storageSize: ret.storageStats.storageSize,
      totalSize: ret.storageStats.totalSize,
      totalIndexSize: ret.storageStats.totalIndexSize,
      indexSizes: ret.storageStats.indexSizes,
    }
  }
}

