import { CloverController } from '@havenzhang/clover'
import { ApiTags } from '@nestjs/swagger'
import { UserControllerBase } from '../../base/entity/User/User.controller'

@CloverController()
@ApiTags('用户账户')
export class UserController extends UserControllerBase {}
