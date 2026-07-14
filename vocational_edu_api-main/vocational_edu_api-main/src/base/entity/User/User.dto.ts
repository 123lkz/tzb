import { ObjectIdString, Joi, ListResultPageInfo, ArraySchemaProperty, CloverApiProperty, ObjectSchemaProperty } from '@havenzhang/clover'
import endpoint from '../../../endpoints/User'
export const User_idValidator = Joi.objectId()
export const User_idValidatorOptional = Joi.objectId().optional()
export const UserPhoneValidator = endpoint['schema']['phone'].validator
export const UserPhoneValidatorOptional = endpoint['schema']['phone'].validator.optional()
export const UserTelephoneValidator = endpoint['schema']['telephone'].validator
export const UserTelephoneValidatorOptional = endpoint['schema']['telephone'].validator.optional()
export const UserEmailValidator = endpoint['schema']['email'].validator
export const UserEmailValidatorOptional = endpoint['schema']['email'].validator.optional()
export const UserNameValidator = endpoint['schema']['name'].validator
export const UserNameValidatorOptional = endpoint['schema']['name'].validator.optional()
export const UserHeadImageValidator = endpoint['schema']['headImage'].validator
export const UserHeadImageValidatorOptional = endpoint['schema']['headImage'].validator.optional()
export const UserUsernameValidator = endpoint['schema']['username'].validator
export const UserUsernameValidatorOptional = endpoint['schema']['username'].validator.optional()
export const UserPasswordValidator = endpoint['schema']['password'].validator
export const UserPasswordValidatorOptional = endpoint['schema']['password'].validator.optional()
export const UserRolesValidator = Joi.array().items(Joi.string())
export const UserRolesValidatorOptional = Joi.array().items(Joi.string()).optional()
export const UserLastLoginValidator = Joi.date()
export const UserLastLoginValidatorOptional = Joi.date().optional()
export const UserLoginLogsIpValidator = endpoint['schema']['loginLogs']['item']['schema']['ip'].validator
export const UserLoginLogsIpValidatorOptional = endpoint['schema']['loginLogs']['item']['schema']['ip'].validator.optional()
export const UserLoginLogsTimeValidator = Joi.date()
export const UserLoginLogsTimeValidatorOptional = Joi.date().optional()
export const UserLoginLogsValidator = Joi.array().items(Joi.object().keys({
  ip: UserLoginLogsIpValidator,
  time: UserLoginLogsTimeValidator
}))
export const UserLoginLogsValidatorOptional = Joi.array().items(Joi.object().keys({
  ip: UserLoginLogsIpValidator,
  time: UserLoginLogsTimeValidator
})).optional()
export const UserLastTokenValidator = endpoint['schema']['lastToken'].validator
export const UserLastTokenValidatorOptional = endpoint['schema']['lastToken'].validator.optional()
export const UserTokenExpValidator = Joi.date()
export const UserTokenExpValidatorOptional = Joi.date().optional()
export const UserRegisterAtValidator = Joi.date()
export const UserRegisterAtValidatorOptional = Joi.date().optional()
export const UserRegisterIpValidator = endpoint['schema']['registerIp'].validator
export const UserRegisterIpValidatorOptional = endpoint['schema']['registerIp'].validator.optional()
export const UserLogoffAtValidator = Joi.date()
export const UserLogoffAtValidatorOptional = Joi.date().optional()
export const UserPasswordLogsIpValidator = endpoint['schema']['passwordLogs']['item']['schema']['ip'].validator
export const UserPasswordLogsIpValidatorOptional = endpoint['schema']['passwordLogs']['item']['schema']['ip'].validator.optional()
export const UserPasswordLogsTimeValidator = Joi.date()
export const UserPasswordLogsTimeValidatorOptional = Joi.date().optional()
export const UserPasswordLogsValidator = Joi.array().items(Joi.object().keys({
  ip: UserPasswordLogsIpValidator,
  time: UserPasswordLogsTimeValidator
}))
export const UserPasswordLogsValidatorOptional = Joi.array().items(Joi.object().keys({
  ip: UserPasswordLogsIpValidator,
  time: UserPasswordLogsTimeValidator
})).optional()
export const UserPhoneLogsIpValidator = endpoint['schema']['phoneLogs']['item']['schema']['ip'].validator
export const UserPhoneLogsIpValidatorOptional = endpoint['schema']['phoneLogs']['item']['schema']['ip'].validator.optional()
export const UserPhoneLogsTimeValidator = Joi.date()
export const UserPhoneLogsTimeValidatorOptional = Joi.date().optional()
export const UserPhoneLogsValidator = Joi.array().items(Joi.object().keys({
  ip: UserPhoneLogsIpValidator,
  time: UserPhoneLogsTimeValidator
}))
export const UserPhoneLogsValidatorOptional = Joi.array().items(Joi.object().keys({
  ip: UserPhoneLogsIpValidator,
  time: UserPhoneLogsTimeValidator
})).optional()
export const UserUsernameLogsIpValidator = endpoint['schema']['usernameLogs']['item']['schema']['ip'].validator
export const UserUsernameLogsIpValidatorOptional = endpoint['schema']['usernameLogs']['item']['schema']['ip'].validator.optional()
export const UserUsernameLogsTimeValidator = Joi.date()
export const UserUsernameLogsTimeValidatorOptional = Joi.date().optional()
export const UserUsernameLogsNameValidator = endpoint['schema']['usernameLogs']['item']['schema']['name'].validator
export const UserUsernameLogsNameValidatorOptional = endpoint['schema']['usernameLogs']['item']['schema']['name'].validator.optional()
export const UserUsernameLogsValidator = Joi.array().items(Joi.object().keys({
  ip: UserUsernameLogsIpValidator,
  time: UserUsernameLogsTimeValidator,
  name: UserUsernameLogsNameValidator
}))
export const UserUsernameLogsValidatorOptional = Joi.array().items(Joi.object().keys({
  ip: UserUsernameLogsIpValidator,
  time: UserUsernameLogsTimeValidator,
  name: UserUsernameLogsNameValidator
})).optional()
export const User_etagValidator = endpoint['schema']['_etag'].validator
export const User_etagValidatorOptional = endpoint['schema']['_etag'].validator.optional()
export const User_updatedValidator = endpoint['schema']['_updated'].validator
export const User_updatedValidatorOptional = endpoint['schema']['_updated'].validator.optional()
export const User_createdValidator = endpoint['schema']['_created'].validator
export const User_createdValidatorOptional = endpoint['schema']['_created'].validator.optional()
export const UserListQueryValidator = Joi.object().keys({
  _id: User_idValidator.optional(),
  phone: UserPhoneValidator.optional(),
  roles: UserRolesValidator.optional(),
  registerAt: UserRegisterAtValidator.optional()
})
export const AdminUserListQueryValidator = Joi.object().keys({
  _id: User_idValidator.optional(),
  phone: UserPhoneValidator.optional(),
  telephone: UserTelephoneValidator.optional(),
  email: UserEmailValidator.optional(),
  name: UserNameValidator.optional(),
  headImage: UserHeadImageValidator.optional(),
  username: UserUsernameValidator.optional(),
  password: UserPasswordValidator.optional(),
  roles: UserRolesValidator.optional(),
  lastLogin: UserLastLoginValidator.optional(),
  loginLogs: UserLoginLogsValidator.optional(),
  lastToken: UserLastTokenValidator.optional(),
  tokenExp: UserTokenExpValidator.optional(),
  registerAt: UserRegisterAtValidator.optional(),
  registerIp: UserRegisterIpValidator.optional(),
  logoffAt: UserLogoffAtValidator.optional(),
  passwordLogs: UserPasswordLogsValidator.optional(),
  phoneLogs: UserPhoneLogsValidator.optional(),
  usernameLogs: UserUsernameLogsValidator.optional(),
  _etag: User_etagValidator.optional(),
  _updated: User_updatedValidator.optional(),
  _created: User_createdValidator.optional()
})

export class UserUsernameLogsAdminLookupFields {
  ip?: string
  name?: string
  time?: Date
}

export class UpdateUserUsernameLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserUsernameLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false, validator: UserUsernameLogsNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserUsernameLogsTimeValidatorOptional })
  time?: Date
}

export class AdminCreateUserUsernameLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserUsernameLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false, validator: UserUsernameLogsNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserUsernameLogsTimeValidatorOptional })
  time?: Date
}

export class AdminUpdateUserUsernameLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserUsernameLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false, validator: UserUsernameLogsNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserUsernameLogsTimeValidatorOptional })
  time?: Date
}

export class AdminListUserUsernameLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false })
  name?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class AdminGetUserUsernameLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false })
  name?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class ReplaceUserUsernameLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserUsernameLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false, validator: UserUsernameLogsNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserUsernameLogsTimeValidatorOptional })
  time?: Date
}

export class CreateUserUsernameLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserUsernameLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false, validator: UserUsernameLogsNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserUsernameLogsTimeValidatorOptional })
  time?: Date
}

export class ListUserUsernameLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false })
  name?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class GetUserUsernameLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '曾用名', required: false })
  name?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class UserPhoneLogsAdminLookupFields {
  ip?: string
  time?: Date
}

export class UpdateUserPhoneLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPhoneLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPhoneLogsTimeValidatorOptional })
  time?: Date
}

export class AdminCreateUserPhoneLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPhoneLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPhoneLogsTimeValidatorOptional })
  time?: Date
}

export class AdminUpdateUserPhoneLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPhoneLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPhoneLogsTimeValidatorOptional })
  time?: Date
}

export class AdminListUserPhoneLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class AdminGetUserPhoneLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class ReplaceUserPhoneLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPhoneLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPhoneLogsTimeValidatorOptional })
  time?: Date
}

export class CreateUserPhoneLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPhoneLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPhoneLogsTimeValidatorOptional })
  time?: Date
}

export class ListUserPhoneLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class GetUserPhoneLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class UserPasswordLogsAdminLookupFields {
  ip?: string
  time?: Date
}

export class UpdateUserPasswordLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPasswordLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPasswordLogsTimeValidatorOptional })
  time?: Date
}

export class AdminCreateUserPasswordLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPasswordLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPasswordLogsTimeValidatorOptional })
  time?: Date
}

export class AdminUpdateUserPasswordLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPasswordLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPasswordLogsTimeValidatorOptional })
  time?: Date
}

export class AdminListUserPasswordLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class AdminGetUserPasswordLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class ReplaceUserPasswordLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPasswordLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPasswordLogsTimeValidatorOptional })
  time?: Date
}

export class CreateUserPasswordLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserPasswordLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserPasswordLogsTimeValidatorOptional })
  time?: Date
}

export class ListUserPasswordLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class GetUserPasswordLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class UserLoginLogsAdminLookupFields {
  ip?: string
  time?: Date
}

export class UpdateUserLoginLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserLoginLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserLoginLogsTimeValidatorOptional })
  time?: Date
}

export class AdminCreateUserLoginLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserLoginLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserLoginLogsTimeValidatorOptional })
  time?: Date
}

export class AdminUpdateUserLoginLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserLoginLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserLoginLogsTimeValidatorOptional })
  time?: Date
}

export class AdminListUserLoginLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class AdminGetUserLoginLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class ReplaceUserLoginLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserLoginLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserLoginLogsTimeValidatorOptional })
  time?: Date
}

export class CreateUserLoginLogs {
  @CloverApiProperty({ description: 'IP', required: false, validator: UserLoginLogsIpValidatorOptional })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false, validator: UserLoginLogsTimeValidatorOptional })
  time?: Date
}

export class ListUserLoginLogsItem {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class GetUserLoginLogsResult {
  @CloverApiProperty({ description: 'IP', required: false })
  ip?: string
  @CloverApiProperty({ description: '时间', required: false })
  time?: Date
}

export class UpdateUser {
  @CloverApiProperty({ description: '邮箱', required: false, validator: UserEmailValidatorOptional })
  email?: string
  @CloverApiProperty({ description: '联系电话', required: false, validator: UserTelephoneValidatorOptional })
  telephone?: string
}

export class UserLookupFields {
  _id?: string
  phone?: string
  registerAt?: Date
  roles?: string[]
}

export class UserAdminLookupFields {
  _created?: Date
  _etag?: string
  _id?: string
  _updated?: Date
  email?: string
  headImage?: string
  lastLogin?: Date
  lastToken?: string
  logoffAt?: Date
  name?: string
  password?: string
  phone?: string
  registerAt?: Date
  registerIp?: string
  roles?: string[]
  telephone?: string
  tokenExp?: Date
  username?: string
}

export class AdminCreateUser {
  @CloverApiProperty({ required: false, validator: User_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: User_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: User_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: User_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '邮箱', required: false, validator: UserEmailValidatorOptional })
  email?: string
  @CloverApiProperty({ description: '头像', required: false, validator: UserHeadImageValidatorOptional })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false, validator: UserLastLoginValidatorOptional })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false, validator: UserLastTokenValidatorOptional })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [AdminCreateUserLoginLogs], required: false, validator: UserLoginLogsValidatorOptional })
  loginLogs?: AdminCreateUserLoginLogs[]
  @CloverApiProperty({ description: '注销时间', required: false, validator: UserLogoffAtValidatorOptional })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false, validator: UserNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '密码', validator: UserPasswordValidator })
  password: string
  @CloverApiProperty({ description: '密码修改日志', type: [AdminCreateUserPasswordLogs], required: false, validator: UserPasswordLogsValidatorOptional })
  passwordLogs?: AdminCreateUserPasswordLogs[]
  @CloverApiProperty({ description: '手机号', validator: UserPhoneValidator })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [AdminCreateUserPhoneLogs], required: false, validator: UserPhoneLogsValidatorOptional })
  phoneLogs?: AdminCreateUserPhoneLogs[]
  @CloverApiProperty({ description: '注册时间', required: false, validator: UserRegisterAtValidatorOptional })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false, validator: UserRegisterIpValidatorOptional })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false, validator: UserRolesValidatorOptional })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false, validator: UserTelephoneValidatorOptional })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false, validator: UserTokenExpValidatorOptional })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false, validator: UserUsernameValidatorOptional })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [AdminCreateUserUsernameLogs], required: false, validator: UserUsernameLogsValidatorOptional })
  usernameLogs?: AdminCreateUserUsernameLogs[]
}

export class AdminUpdateUser {
  @CloverApiProperty({ required: false, validator: User_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ required: false, validator: User_etagValidatorOptional })
  _etag?: string
  @CloverApiProperty({ description: 'ID', required: false, validator: User_idValidatorOptional, format: 'objectId' })
  _id?: string
  @CloverApiProperty({ required: false, validator: User_updatedValidatorOptional })
  _updated?: Date
  @CloverApiProperty({ description: '邮箱', required: false, validator: UserEmailValidatorOptional })
  email?: string
  @CloverApiProperty({ description: '头像', required: false, validator: UserHeadImageValidatorOptional })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false, validator: UserLastLoginValidatorOptional })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false, validator: UserLastTokenValidatorOptional })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [AdminUpdateUserLoginLogs], required: false, validator: UserLoginLogsValidatorOptional })
  loginLogs?: AdminUpdateUserLoginLogs[]
  @CloverApiProperty({ description: '注销时间', required: false, validator: UserLogoffAtValidatorOptional })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false, validator: UserNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '密码', required: false, validator: UserPasswordValidatorOptional })
  password?: string
  @CloverApiProperty({ description: '密码修改日志', type: [AdminUpdateUserPasswordLogs], required: false, validator: UserPasswordLogsValidatorOptional })
  passwordLogs?: AdminUpdateUserPasswordLogs[]
  @CloverApiProperty({ description: '手机号', required: false, validator: UserPhoneValidatorOptional })
  phone?: string
  @CloverApiProperty({ description: '手机号修改日志', type: [AdminUpdateUserPhoneLogs], required: false, validator: UserPhoneLogsValidatorOptional })
  phoneLogs?: AdminUpdateUserPhoneLogs[]
  @CloverApiProperty({ description: '注册时间', required: false, validator: UserRegisterAtValidatorOptional })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false, validator: UserRegisterIpValidatorOptional })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false, validator: UserRolesValidatorOptional })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false, validator: UserTelephoneValidatorOptional })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false, validator: UserTokenExpValidatorOptional })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false, validator: UserUsernameValidatorOptional })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [AdminUpdateUserUsernameLogs], required: false, validator: UserUsernameLogsValidatorOptional })
  usernameLogs?: AdminUpdateUserUsernameLogs[]
}

export class AdminListUserItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '邮箱', required: false })
  email?: string
  @CloverApiProperty({ description: '头像', required: false })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [AdminListUserLoginLogsItem], required: false })
  loginLogs?: AdminListUserLoginLogsItem[]
  @CloverApiProperty({ description: '注销时间', required: false })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false })
  name?: string
  @CloverApiProperty({ description: '密码' })
  password: string
  @CloverApiProperty({ description: '密码修改日志', type: [AdminListUserPasswordLogsItem], required: false })
  passwordLogs?: AdminListUserPasswordLogsItem[]
  @CloverApiProperty({ description: '手机号' })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [AdminListUserPhoneLogsItem], required: false })
  phoneLogs?: AdminListUserPhoneLogsItem[]
  @CloverApiProperty({ description: '注册时间', required: false })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [AdminListUserUsernameLogsItem], required: false })
  usernameLogs?: AdminListUserUsernameLogsItem[]
}

export class AdminGetUserResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '邮箱', required: false })
  email?: string
  @CloverApiProperty({ description: '头像', required: false })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [AdminGetUserLoginLogsResult], required: false })
  loginLogs?: AdminGetUserLoginLogsResult[]
  @CloverApiProperty({ description: '注销时间', required: false })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false })
  name?: string
  @CloverApiProperty({ description: '密码' })
  password: string
  @CloverApiProperty({ description: '密码修改日志', type: [AdminGetUserPasswordLogsResult], required: false })
  passwordLogs?: AdminGetUserPasswordLogsResult[]
  @CloverApiProperty({ description: '手机号' })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [AdminGetUserPhoneLogsResult], required: false })
  phoneLogs?: AdminGetUserPhoneLogsResult[]
  @CloverApiProperty({ description: '注册时间', required: false })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [AdminGetUserUsernameLogsResult], required: false })
  usernameLogs?: AdminGetUserUsernameLogsResult[]
}

export class ReplaceUser {
  @CloverApiProperty({ required: false, validator: User_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '邮箱', required: false, validator: UserEmailValidatorOptional })
  email?: string
  @CloverApiProperty({ description: '头像', required: false, validator: UserHeadImageValidatorOptional })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false, validator: UserLastLoginValidatorOptional })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false, validator: UserLastTokenValidatorOptional })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [ReplaceUserLoginLogs], required: false, validator: UserLoginLogsValidatorOptional })
  loginLogs?: ReplaceUserLoginLogs[]
  @CloverApiProperty({ description: '注销时间', required: false, validator: UserLogoffAtValidatorOptional })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false, validator: UserNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '密码', validator: UserPasswordValidator })
  password: string
  @CloverApiProperty({ description: '密码修改日志', type: [ReplaceUserPasswordLogs], required: false, validator: UserPasswordLogsValidatorOptional })
  passwordLogs?: ReplaceUserPasswordLogs[]
  @CloverApiProperty({ description: '手机号', validator: UserPhoneValidator })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [ReplaceUserPhoneLogs], required: false, validator: UserPhoneLogsValidatorOptional })
  phoneLogs?: ReplaceUserPhoneLogs[]
  @CloverApiProperty({ description: '注册时间', required: false, validator: UserRegisterAtValidatorOptional })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false, validator: UserRegisterIpValidatorOptional })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false, validator: UserRolesValidatorOptional })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false, validator: UserTelephoneValidatorOptional })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false, validator: UserTokenExpValidatorOptional })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false, validator: UserUsernameValidatorOptional })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [ReplaceUserUsernameLogs], required: false, validator: UserUsernameLogsValidatorOptional })
  usernameLogs?: ReplaceUserUsernameLogs[]
}

export class CreateUser {
  @CloverApiProperty({ required: false, validator: User_createdValidatorOptional })
  _created?: Date
  @CloverApiProperty({ description: '邮箱', required: false, validator: UserEmailValidatorOptional })
  email?: string
  @CloverApiProperty({ description: '头像', required: false, validator: UserHeadImageValidatorOptional })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false, validator: UserLastLoginValidatorOptional })
  lastLogin?: Date
  @CloverApiProperty({ description: '最后登录 Token', required: false, validator: UserLastTokenValidatorOptional })
  lastToken?: string
  @CloverApiProperty({ description: '登录日志', type: [CreateUserLoginLogs], required: false, validator: UserLoginLogsValidatorOptional })
  loginLogs?: CreateUserLoginLogs[]
  @CloverApiProperty({ description: '注销时间', required: false, validator: UserLogoffAtValidatorOptional })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false, validator: UserNameValidatorOptional })
  name?: string
  @CloverApiProperty({ description: '密码', validator: UserPasswordValidator })
  password: string
  @CloverApiProperty({ description: '密码修改日志', type: [CreateUserPasswordLogs], required: false, validator: UserPasswordLogsValidatorOptional })
  passwordLogs?: CreateUserPasswordLogs[]
  @CloverApiProperty({ description: '手机号', validator: UserPhoneValidator })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [CreateUserPhoneLogs], required: false, validator: UserPhoneLogsValidatorOptional })
  phoneLogs?: CreateUserPhoneLogs[]
  @CloverApiProperty({ description: '注册时间', required: false, validator: UserRegisterAtValidatorOptional })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false, validator: UserRegisterIpValidatorOptional })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false, validator: UserRolesValidatorOptional })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false, validator: UserTelephoneValidatorOptional })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false, validator: UserTokenExpValidatorOptional })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false, validator: UserUsernameValidatorOptional })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [CreateUserUsernameLogs], required: false, validator: UserUsernameLogsValidatorOptional })
  usernameLogs?: CreateUserUsernameLogs[]
}

export class ListUserItem {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '邮箱', required: false })
  email?: string
  @CloverApiProperty({ description: '头像', required: false })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false })
  lastLogin?: Date
  @CloverApiProperty({ description: '登录日志', type: [ListUserLoginLogsItem], required: false })
  loginLogs?: ListUserLoginLogsItem[]
  @CloverApiProperty({ description: '注销时间', required: false })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false })
  name?: string
  @CloverApiProperty({ description: '密码修改日志', type: [ListUserPasswordLogsItem], required: false })
  passwordLogs?: ListUserPasswordLogsItem[]
  @CloverApiProperty({ description: '手机号' })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [ListUserPhoneLogsItem], required: false })
  phoneLogs?: ListUserPhoneLogsItem[]
  @CloverApiProperty({ description: '注册时间', required: false })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [ListUserUsernameLogsItem], required: false })
  usernameLogs?: ListUserUsernameLogsItem[]
}

export class GetUserResult {
  @CloverApiProperty({ required: false })
  _created?: Date
  @CloverApiProperty()
  _etag: string
  @CloverApiProperty({ description: 'ID', format: 'objectId' })
  _id: string
  @CloverApiProperty()
  _updated: Date
  @CloverApiProperty({ description: '邮箱', required: false })
  email?: string
  @CloverApiProperty({ description: '头像', required: false })
  headImage?: string
  @CloverApiProperty({ description: '上次登录时间', required: false })
  lastLogin?: Date
  @CloverApiProperty({ description: '登录日志', type: [GetUserLoginLogsResult], required: false })
  loginLogs?: GetUserLoginLogsResult[]
  @CloverApiProperty({ description: '注销时间', required: false })
  logoffAt?: Date
  @CloverApiProperty({ description: '姓名', required: false })
  name?: string
  @CloverApiProperty({ description: '密码修改日志', type: [GetUserPasswordLogsResult], required: false })
  passwordLogs?: GetUserPasswordLogsResult[]
  @CloverApiProperty({ description: '手机号' })
  phone: string
  @CloverApiProperty({ description: '手机号修改日志', type: [GetUserPhoneLogsResult], required: false })
  phoneLogs?: GetUserPhoneLogsResult[]
  @CloverApiProperty({ description: '注册时间', required: false })
  registerAt?: Date
  @CloverApiProperty({ description: '注册 IP', required: false })
  registerIp?: string
  @CloverApiProperty({ description: '角色', required: false })
  roles?: string[]
  @CloverApiProperty({ description: '联系电话', required: false })
  telephone?: string
  @CloverApiProperty({ description: 'Token 失效时间', required: false })
  tokenExp?: Date
  @CloverApiProperty({ description: '用户名（昵称）', required: false })
  username?: string
  @CloverApiProperty({ description: '用户名修改日志', type: [GetUserUsernameLogsResult], required: false })
  usernameLogs?: GetUserUsernameLogsResult[]
}

export interface UserCombinedId {
  _id?: string
}

export class ListUserResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [ListUserItem] })
  _items: ListUserItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class AdminListUserResult {
  @CloverApiProperty()
  _status: string
  @CloverApiProperty({ type: [AdminListUserItem] })
  _items: AdminListUserItem[]
  @CloverApiProperty({ type: ListResultPageInfo })
  _pageInfo: ListResultPageInfo
}

export class UpsertUser {
}

export class RemoveUser {
}

export class UserCombinedId {
}

export interface UserDtoType {
  item: GetUserResult
  create: CreateUser
  replace: ReplaceUser
  update: UpdateUser
}
