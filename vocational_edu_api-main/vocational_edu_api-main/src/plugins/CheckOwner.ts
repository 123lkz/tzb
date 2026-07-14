import { EntityService, IUser } from '@havenzhang/clover'
import {
  applyDecorators,
  BadRequestException,
  CanActivate,
  ExecutionContext,
  Injectable,
  SetMetadata,
  UseGuards
} from '@nestjs/common'
import { Reflector } from '@nestjs/core'

@Injectable()
class CheckOwnerGuard implements CanActivate {
  constructor(protected readonly reflector: Reflector) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = this.getRequest(context)
    const entity = this.reflector.get<EntityService<any, any>>('clover/entity', context.getClass())
    const ownerField: string = this.reflector.get<string>('ownerField', context.getHandler()) || 'owner'
    const user: IUser = request.user
    const combinedId = request.combinedId

    if (!entity) {
      throw new Error('CheckOwnerGuard must be used in entity service')
    }
    if (!user || combinedId === undefined) {
      throw new Error(
        'CheckOwnerGuard must be used in entity service, and request must have user and combinedId: ' + request.url
      )
    }

    if (Array.isArray(user.roles) && user.roles.includes('admin')) {
      return true
    }

    const doc = await entity.model.findOne(combinedId, { [ownerField]: 1 }, { lean: true })
    if (!doc) {
      if (combinedId[ownerField] === user.id) {
        return true
      }
      throw new BadRequestException('请求无效')
    }
    // @ts-ignore
    return doc && doc[ownerField] && doc[ownerField].toString() === user.id
  }

  getRequest<T = any>(context: ExecutionContext): T {
    return context.switchToHttp().getRequest()
  }
}

// 插件提供一个装饰器，自动加载到配置定义的 restful 方法中
// 添加插件需要执行 clover 指令
// 装饰器可以在自定义方法中使用
export const CheckOwner = function (field: string) {
  return applyDecorators(SetMetadata('ownerField', field), UseGuards(CheckOwnerGuard))
}

export function build(config: string = 'owner') {
  return {
    name: 'CheckOwner',
    arguments: `'${config}'`
  }
}
