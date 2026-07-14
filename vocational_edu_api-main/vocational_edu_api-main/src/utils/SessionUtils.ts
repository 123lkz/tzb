import { BaseQueryParams } from '../entity/Base/Base.dto'

/**
 * 会话ID生成工具类
 * 统一管理 sessionId 的生成逻辑
 */
export class SessionUtils {
  /**
   * 根据查询参数生成稳定的sessionId（按天生成，同一天内相同参数使用相同sessionId）
   * @param params 查询参数
   * @param prefix 前缀，默认为 'screen'
   * @returns 稳定的sessionId
   */
  static generateStableSessionId(params: BaseQueryParams, prefix: string = 'base'): string {
    // 标准化参数，确保相同内容的对象生成相同的hash
    const normalizedParams = {
      dateType: params.dateType,
      caliberType: params.caliberType
    }

    const paramsStr = JSON.stringify(normalizedParams)
    const hash = require('crypto').createHash('md5').update(paramsStr).digest('hex')

    // 获取当前日期（YYYY-MM-DD格式）
    const today = new Date().toISOString().split('T')[0]

    return `${prefix}_${today}_${hash.substring(0, 12)}`
  }
}
