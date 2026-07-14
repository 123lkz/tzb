import { Injectable, Logger } from '@nestjs/common'
import { Cron } from '@nestjs/schedule'
import { BaseService } from '../entity/Base/Base.service'
import { CacheService } from '../services/CacheService'

/**
 * 基础数据缓存任务
 * 管理4种组合的基础数据缓存：month:all, month:college, year:all, year:college
 */
@Injectable()
export class BaseCacheTask {
  private readonly logger = new Logger(BaseCacheTask.name)
  private readonly cacheService = new CacheService()

  /**
   * 获取当前环境
   */
  private getEnvironment(): 'development' | 'production' {
    return process.env.NODE_ENV === 'production' ? 'production' : 'development'
  }

  /**
   * 每日凌晨03:00:00执行基础数据缓存任务
   * 生成今天的4种组合缓存数据
   */
  @Cron('0 0 3 * * *')
  async handleBaseCache() {
    this.logger.log('🚀 开始执行每日基础数据缓存任务 (03:00:00)...')

    const maxRetries = 2
    let attempt = 0
    let success = false

    while (attempt < maxRetries && !success) {
      attempt++
      this.logger.log(`📊 第 ${attempt} 次尝试缓存基础数据...`)

      try {
        const result = await BaseService.cacheAllCombinations()

        if (result.success) {
          this.logger.log('✅ 每日基础数据缓存任务执行成功')
          this.logger.log(`📊 成功缓存 ${result.results.length} 种组合的基础数据`)
          success = true
        } else {
          this.logger.warn(`⚠️ 第 ${attempt} 次尝试部分失败`)
          const failedResults = result.results.filter((r) => !r.success)
          failedResults.forEach((failed) => {
            this.logger.error(`❌ 缓存失败: ${JSON.stringify(failed.params)}, 错误: ${failed.error}`)
          })

          if (attempt < maxRetries) {
            this.logger.log(`🔄 将在 ${attempt * 5} 秒后进行第 ${attempt + 1} 次重试...`)
            await new Promise((resolve) => setTimeout(resolve, attempt * 5000)) // 递增延迟
          }
        }
      } catch (error) {
        this.logger.error(`💥 第 ${attempt} 次尝试执行失败: ${error.message}`)

        if (attempt < maxRetries) {
          this.logger.log(`🔄 将在 ${attempt * 5} 秒后进行第 ${attempt + 1} 次重试...`)
          await new Promise((resolve) => setTimeout(resolve, attempt * 5000)) // 递增延迟
        }
      }
    }

    if (!success) {
      this.logger.error(`💥 每日基础数据缓存任务最终失败，已重试 ${maxRetries} 次`)
    }
  }

  /**
   * 每日凌晨05:00:00执行缓存清理任务
   * 清理昨天的缓存数据，保留今天的缓存
   */
  @Cron('0 0 5 * * *')
  async handleCacheCleanup() {
    this.logger.log('🧹 开始执行每日缓存清理任务 (05:00:00)...')

    try {
      // 清理昨天的缓存
      const clearResult = await BaseService.clearYesterdayCache()

      if (clearResult.success) {
        this.logger.log('✅ 昨天缓存清理成功')
        this.logger.log(`📊 清理了 ${clearResult.clearedKeys.length} 个昨天的缓存`)
      } else {
        this.logger.warn('⚠️ 昨天缓存清理部分失败')
        clearResult.errors.forEach((error) => {
          this.logger.error(`❌ ${error}`)
        })
      }

      // 获取当前缓存状态
      const status = await BaseService.getCacheStatus()
      this.logger.log(
        `📊 当前缓存状态: 总计 ${status.summary.total} 个, 已缓存 ${status.summary.cached} 个, 缺失 ${status.summary.missing} 个`
      )
      this.logger.log(`📅 当前日期: ${status.summary.currentDate}`)

      this.logger.log('✅ 每日缓存清理任务执行完成')
    } catch (error) {
      this.logger.error(`💥 每日缓存清理任务执行失败: ${error.message}`)
      this.logger.error(error.stack)
    }
  }

  /**
   * Redis存储信息监控任务
   * 每天7点执行一次，监控缓存键和大小
   */
  @Cron('0 0 7 * * *') // 每天7点执行一次
  async handleRedisMonitoring() {
    this.logger.log('🔍 开始执行Redis存储信息监控任务 (每天7点)...')

    try {
      await this.monitorBaseCacheKeys()
      this.logger.log('✅ Redis存储信息监控任务执行完成')
    } catch (error) {
      this.logger.error(`💥 Redis存储信息监控任务执行失败: ${error.message}`)
    }
  }

  /**
   * 监控4种base缓存键的详细状态
   */
  private async monitorBaseCacheKeys() {
    try {
      // 使用本地时间获取当前日期
      const now = new Date()
      const currentDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

      const yesterday = new Date()
      yesterday.setDate(yesterday.getDate() - 1)
      const yesterdayStr = `${yesterday.getFullYear()}-${String(yesterday.getMonth() + 1).padStart(2, '0')}-${String(yesterday.getDate()).padStart(2, '0')}`

      const combinations = [
        { dateType: 'month', caliberType: 'all' },
        { dateType: 'month', caliberType: 'college' },
        { dateType: 'year', caliberType: 'all' },
        { dateType: 'year', caliberType: 'college' }
      ]

      this.logger.log('🔍 Base缓存键详细监控:')

      for (const combo of combinations) {
        const todayKey = `base:${currentDate}:${combo.dateType}:${combo.caliberType}`
        const yesterdayKey = `base:${yesterdayStr}:${combo.dateType}:${combo.caliberType}`

        // 检查今天的缓存
        const todayData = await this.cacheService.get(todayKey)
        const todaySize = todayData ? JSON.stringify(todayData).length : 0
        const todayExists = !!todayData

        // 检查昨天的缓存
        const yesterdayData = await this.cacheService.get(yesterdayKey)
        const yesterdaySize = yesterdayData ? JSON.stringify(yesterdayData).length : 0
        const yesterdayExists = !!yesterdayData

        this.logger.log(`  📋 ${combo.dateType}:${combo.caliberType}:`)
        this.logger.log(
          `    - 今天 (${todayKey}): ${todayExists ? '✅存在' : '❌不存在'} (${this.formatBytes(todaySize)})`
        )
        this.logger.log(
          `    - 昨天 (${yesterdayKey}): ${yesterdayExists ? '✅存在' : '❌不存在'} (${this.formatBytes(yesterdaySize)})`
        )

        // 如果存在缓存，显示部分内容信息
        if (todayData) {
          try {
            // todayData已经是解析后的对象，不需要再次JSON.parse
            const cacheInfo = todayData as any
            this.logger.log(
              `    - 今天缓存信息: 日期=${cacheInfo.cacheDate || 'N/A'}, 时间=${cacheInfo.cacheTime || 'N/A'}, 方法=${cacheInfo.method || 'N/A'}`
            )
          } catch (e) {
            this.logger.log('    - 今天缓存信息: 数据解析失败')
          }
        }
      }
    } catch (error) {
      this.logger.error(`💥 Base缓存键监控失败: ${error.message}`)
    }
  }

  /**
   * 格式化字节数为可读格式
   */
  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  /**
   * 手动触发缓存任务（用于测试或紧急情况）
   */
  async manualCacheAll() {
    this.logger.log('🔧 手动触发基础数据缓存任务...')

    try {
      const result = await BaseService.cacheAllCombinations()

      if (result.success) {
        this.logger.log('✅ 手动缓存任务执行成功')
        return {
          success: true,
          message: '手动缓存任务执行成功',
          results: result.results
        }
      }
      this.logger.warn('⚠️ 手动缓存任务部分失败')
      return {
        success: false,
        message: '手动缓存任务部分失败',
        results: result.results
      }
    } catch (error) {
      this.logger.error(`💥 手动缓存任务执行失败: ${error.message}`)
      return {
        success: false,
        message: `手动缓存任务执行失败: ${error.message}`,
        error: error.message
      }
    }
  }
}
