import { createEntityService } from '@havenzhang/clover'
import endpoint from '../../endpoints/User'
import { createUserModel, UserModel, UserSchema } from '../../base/entity/User/User.model'
import { UserDtoType } from '../../base/entity/User/User.dto'
const userModel = createUserModel(UserSchema)
export const UserEntity = createEntityService<UserModel, UserDtoType>(endpoint, userModel)
