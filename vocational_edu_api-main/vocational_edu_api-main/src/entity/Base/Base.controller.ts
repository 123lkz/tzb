import { CloverController, Description } from '@havenzhang/clover'
import { BadRequestException, Get, Post, Query } from '@nestjs/common'
import { ApiResponse, ApiTags } from '@nestjs/swagger'
import { BaseService } from './Base.service'

@CloverController()
@ApiTags('基础数据缓存管理')
export class BaseController {
  /**
   * 缓存所有4种组合的基础数据（聚合方案）
   */
  @Get('/base/cache/all')
  @Description('手动缓存所有4种组合的基础数据（异步执行）')
  @ApiResponse({
    description: '批量缓存任务启动结果',
    schema: {
      type: 'object',
      properties: {
        success: { type: 'boolean', description: '是否成功启动' },
        message: { type: 'string', description: '提示信息' },
        taskId: { type: 'string', description: '任务ID' },
        totalTasks: { type: 'number', description: '总任务数' }
      }
    }
  })
  async cacheAllCombinations() {
    try {
      // 生成任务ID
      const taskId = `cache_all_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

      // 异步执行批量缓存任务，不等待结果
      BaseService.cacheAllCombinationsAsync(taskId)
        .then((result) => {
          console.log(`✅ 批量缓存任务完成: ${taskId}, 成功: ${result.successCount}/${result.totalCount}`)
        })
        .catch((error) => {
          console.error(`❌ 批量缓存任务失败: ${taskId}, 错误: ${error.message}`)
        })

      return {
        success: true,
        message: '批量缓存任务已启动，正在后台处理中...',
        taskId,
        totalTasks: BaseService.CACHE_COMBINATIONS.length
      }
    } catch (error) {
      throw new BadRequestException(`启动批量缓存任务失败: ${error.message}`)
    }
  }

  /**
   * 触发单个查询条件的基础数据缓存
   */
  @Get('/base/cache/single')
  @Description('手动触发单个查询条件的基础数据缓存（异步执行）')
  @ApiResponse({
    description: '缓存任务启动结果',
    schema: {
      type: 'object',
      properties: {
        success: { type: 'boolean', description: '是否成功启动' },
        message: { type: 'string', description: '提示信息' },
        taskId: { type: 'string', description: '任务ID' },
        cacheKey: { type: 'string', description: '缓存键' }
      }
    }
  })
  async cacheSingleCombination(@Query() params: { dateType: 'month' | 'year'; caliberType: 'all' | 'college' }) {
    try {
      if (!params.dateType || !params.caliberType) {
        throw new BadRequestException('缺少必要参数: dateType 和 caliberType')
      }

      // 生成任务ID和缓存键
      const taskId = `cache_single_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      const cacheKey = BaseService.generateCacheKey(params)

      // 异步执行缓存任务，不等待结果
      BaseService.cacheSingleCombinationAsync(params, taskId)
        .then((result) => {
          console.log(`✅ 缓存任务完成: ${taskId}, 缓存键: ${cacheKey}`)
        })
        .catch((error) => {
          console.error(`❌ 缓存任务失败: ${taskId}, 错误: ${error.message}`)
        })

      return {
        success: true,
        message: '缓存任务已启动，正在后台处理中...',
        taskId,
        cacheKey
      }
    } catch (error) {
      throw new BadRequestException(`启动缓存任务失败: ${error.message}`)
    }
  }

  /**
   * 清理昨天的缓存
   */
  @Post('/base/cache/clear-yesterday')
  @Description('清理昨天的缓存（保留今天的缓存）')
  @ApiResponse({
    description: '清理操作结果',
    schema: {
      type: 'object',
      properties: {
        success: { type: 'boolean', description: '是否全部成功' },
        clearedKeys: { type: 'array', items: { type: 'string' } },
        errors: { type: 'array', items: { type: 'string' } }
      }
    }
  })
  async clearYesterdayCache() {
    try {
      return await BaseService.clearYesterdayCache()
    } catch (error) {
      throw new BadRequestException(`清理昨天缓存失败: ${error.message}`)
    }
  }

  /**
   * 清理今天的缓存
   */
  @Post('/base/cache/clear-today')
  @Description('清理今天的缓存（base四种组合）')
  @ApiResponse({
    description: '清理操作结果',
    schema: {
      type: 'object',
      properties: {
        success: { type: 'boolean', description: '是否全部成功' },
        clearedKeys: { type: 'array', items: { type: 'string' } },
        errors: { type: 'array', items: { type: 'string' } }
      }
    }
  })
  async clearTodayCache() {
    try {
      return await BaseService.clearTodayCache()
    } catch (error) {
      throw new BadRequestException(`清理今天缓存失败: ${error.message}`)
    }
  }

  /**
   * 获取缓存状态信息
   */
  @Get('/base/cache/status')
  @Description('获取缓存状态信息')
  @ApiResponse({
    description: '缓存状态信息',
    schema: {
      type: 'object',
      properties: {
        combinations: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              params: {
                type: 'object',
                properties: {
                  dateType: { type: 'string', enum: ['month', 'year'] },
                  caliberType: { type: 'string', enum: ['all', 'college'] }
                }
              },
              cacheKey: { type: 'string' },
              exists: { type: 'boolean' },
              ttl: { type: 'number' }
            }
          }
        },
        summary: {
          type: 'object',
          properties: {
            total: { type: 'number' },
            cached: { type: 'number' },
            missing: { type: 'number' }
          }
        }
      }
    }
  })
  async getCacheStatus() {
    try {
      return await BaseService.getCacheStatus()
    } catch (error) {
      throw new BadRequestException(`获取缓存状态失败: ${error.message}`)
    }
  }

  @Get('/base/cache/redis-memory')
  @Description('检查Redis内存使用情况')
  @ApiResponse({
    status: 200,
    description: 'Redis内存信息',
    schema: {
      type: 'object',
      properties: {
        usedMemory: { type: 'string' },
        maxMemory: { type: 'string' },
        usagePercent: { type: 'number' },
        evictionPolicy: { type: 'string' }
      }
    }
  })
  async checkRedisMemory() {
    try {
      const cacheService = BaseService.getCacheService()
      await cacheService.checkRedisMemoryNow()
      return { message: 'Redis内存检查完成，请查看日志' }
    } catch (error) {
      throw new BadRequestException(`检查Redis内存失败: ${error.message}`)
    }
  }
}
