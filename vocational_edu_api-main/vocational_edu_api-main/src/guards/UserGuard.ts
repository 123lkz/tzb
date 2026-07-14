// @ts-ignore
import { IUser, ObjectId, UserGuardBase, View } from '@havenzhang/clover'
import { ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common'
import { Reflector } from '@nestjs/core'
import { verify } from 'jsonwebtoken'
import { Model } from 'mongoose'
import config from '../config/config'
import { UserEntity } from '../entity/User/User'

@Injectable()
export class UserGuard extends UserGuardBase {
  constructor(protected readonly reflector: Reflector) {
    super(reflector)
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = this.getRequest(context)

    // bypass /admin
    if (request.url.startsWith('/api/v2/admin')) {
      return true
    }
    // write your guard here
    return super.canActivate(context)
  }

  protected async getUser(context: ExecutionContext) {
    const request = this.getRequest(context)
    const token = request.headers['authorization'] || ''
    if (token) {
      const user = await decodeToken(token, request.url)
      if (user.iss === 'Authorization Server') {
        return {
          roles: ['public']
        }
      }
      if (!user.roles) {
        user.roles = ['user']
      } else if (!user.roles.includes('user')) {
        user.roles.push('user')
      }

      return {
        id: user.id,
        roles: user.roles
      }
    }
    return {
      roles: ['public']
    }
  }
}

// 新增类型定义
interface AuthUserResult {
  _id: string
  roles: string[]
  tokenExp?: Date
  state?: string
}

export async function decodeToken(t: string, url: string) {
  if (!t) {
    throw new UnauthorizedException('令牌无效')
  }
  if (t.startsWith('Bearer ')) {
    t = t.substring(7)
  }
  try {
    const decoded: any = verify(t, config.TOKEN_SECRET)
    let roles = decoded.roles || []
    if (decoded.id) {
      const model = await getModel(roles, url)
      const ret: AuthUserResult = await (model as Model<AuthUserResult>).findOne(
        { _id: decoded.id },
        { tokenExp: 1, state: 1, roles: 1 },
        { lean: true }
      )
      if (ret) {
        if ('tokenExp' in ret) {
          const tokenExp = Math.floor(ret.tokenExp.getTime() / 1000)
          if (tokenExp > decoded.iat && tokenExp < decoded.exp) {
            throw new UnauthorizedException('令牌无效')
          }
        }
        // if (ret.state === 'block' || ret.state === 'logoff') {
        //   throw new UnauthorizedException('令牌无效')
        // }
      }
      roles = ret?.roles || []
    }
    return {
      id: decoded.id || '',
      email: decoded.email || '',
      roles: roles,
      iss: decoded.iss,
      iat: decoded.iat,
      exp: decoded.exp
    }
  } catch (e) {
    throw new UnauthorizedException('令牌无效')
  }
}

export async function getModel(roles: string[], url: string): Promise<Model<any>> {
  return UserEntity.model as Model<any>
}
