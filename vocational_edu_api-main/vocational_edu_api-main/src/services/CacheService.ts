import { Injectable, Logger } from '@nestjs/common'
import Redis from 'ioredis'
import config from '../config/config'

@Injectable()
export class CacheService {
  private readonly logger = new Logger(CacheService.name)
  private redis: Redis
  private static instance: CacheService

  constructor() {
    // 单例模式：如果已经存在实例，直接返回
    if (CacheService.instance) {
      return CacheService.instance
    }

    // 设置单例实例
    CacheService.instance = this

    // 初始化Redis连接
    this.initializeRedis()
  }

  /**
   * 初始化Redis连接
   */
  private initializeRedis(): void {
    const redisUrl = process.env.REDIS_URL

    if (redisUrl) {
      // 使用Redis URL连接
      this.redis = new Redis(redisUrl, {
        maxRetriesPerRequest: 5,
        connectTimeout: 10000, // 10秒连接超时
        commandTimeout: 30000, // 30秒命令超时
        lazyConnect: false, // 立即连接
        enableReadyCheck: true,
        enableOfflineQueue: false, // 禁用离线队列，避免内存泄漏
        keepAlive: 30000, // 保持连接活跃
        family: 4 // 强制使用IPv4
      })
    } else {
      // 使用单独配置连接
      this.redis = new Redis({
        host: config.REDIS_HOST || 'localhost',
        port: config.REDIS_PORT || 6379,
        password: config.REDIS_PASSWORD,
        db: config.REDIS_DB || 0,
        maxRetriesPerRequest: 5,
        connectTimeout: 10000, // 10秒连接超时
        commandTimeout: 30000, // 30秒命令超时
        lazyConnect: false, // 立即连接
        enableReadyCheck: true,
        enableOfflineQueue: false, // 禁用离线队列，避免内存泄漏
        keepAlive: 30000, // 保持连接活跃
        family: 4 // 强制使用IPv4
      })
    }

    this.setupRedisEventListeners()

    // 添加连接健康检查
    this.startHealthCheck()

    // 立即尝试连接
    this.ensureConnection()
  }

  /**
   * 设置Redis事件监听器
   */
  private setupRedisEventListeners(): void {
    this.redis.on('error', (err) => {
      this.logger.error('Redis连接错误:', err)
    })

    this.redis.on('connect', () => {
      this.logger.log('Redis连接成功')
    })

    this.redis.on('ready', () => {
      this.logger.log('Redis准备就绪')
    })

    this.redis.on('close', () => {
      this.logger.warn('Redis连接关闭')
    })

    this.redis.on('reconnecting', () => {
      this.logger.log('Redis重新连接中...')
    })
  }

  /**
   * 确保Redis连接已建立
   */
  private async ensureConnection(): Promise<void> {
    try {
      if (this.redis.status === 'connecting' || this.redis.status === 'wait') {
        this.logger.log('等待Redis连接建立...')
        // 等待连接建立
        await new Promise<void>((resolve, reject) => {
          const timeout = setTimeout(() => {
            reject(new Error('Redis连接超时'))
          }, 10000) // 10秒超时

          const onReady = () => {
            clearTimeout(timeout)
            this.redis.off('ready', onReady)
            this.redis.off('error', onError)
            resolve()
          }

          const onError = (err: Error) => {
            clearTimeout(timeout)
            this.redis.off('ready', onReady)
            this.redis.off('error', onError)
            reject(err)
          }

          if (this.redis.status === 'ready') {
            clearTimeout(timeout)
            resolve()
          } else {
            this.redis.once('ready', onReady)
            this.redis.once('error', onError)
          }
        })
      }

      // 测试连接
      await this.testConnection()
    } catch (error) {
      this.logger.error('Redis连接初始化失败:', error)
      // 不抛出错误，允许应用继续启动，但会在后续操作中处理连接问题
    }
  }

  /**
   * 生成数据大屏缓存键
   * @param params 查询参数
   * @param sessionId 会话标识（用于标识同一批请求）
   * @param dataType 数据类型（trend/province/industry/career/distribution）
   */
  generateScreenDataCacheKey(params: any, sessionId: string, dataType: string): string {
    const paramsStr = JSON.stringify(params)
    return `position_screen:${sessionId}:${dataType}:${Buffer.from(paramsStr).toString('base64')}`
  }

  /**
   * 获取缓存数据
   * @param key 缓存键
   * @param ttl 过期时间（秒）
   */
  async get<T>(key: string, ttl: number = 300): Promise<T | null> {
    try {
      // 检查Redis连接状态
      if (this.redis.status !== 'ready') {
        this.logger.warn(`Redis未就绪，状态: ${this.redis.status}，跳过缓存获取`)
        return null
      }

      // 记录开始读取缓存的时间
      const startTime = Date.now()
      this.logger.log(`🔍 开始读取缓存: ${key}`)

      const data = await this.redis.get(key)
      const readTime = Date.now() - startTime

      if (data) {
        // 获取剩余TTL
        const remainingTtl = await this.redis.ttl(key)

        // 计算数据大小
        const dataSize = Buffer.byteLength(data, 'utf8')

        // 判断缓存类型
        let cacheType = '临时缓存'
        if (remainingTtl === -1) {
          cacheType = '永久缓存'
        } else if (remainingTtl > 0) {
          cacheType = `临时缓存(剩余${remainingTtl}秒)`
        }

        // this.logger.log(`📖 缓存命中: ${key}`)
        // this.logger.log(`   📊 缓存类型: ${cacheType}`)
        // this.logger.log(`   📏 数据大小: ${dataSize} bytes`)
        // this.logger.log(`   ⏱️ 读取耗时: ${readTime}ms`)
        // this.logger.log(`   🔒 TTL状态: ${remainingTtl === -1 ? '永不过期' : `${remainingTtl}秒后过期`}`)

        // 不再自动刷新过期时间，保持原有的TTL
        const parsedData = JSON.parse(data)
        this.logger.log(`✅ 缓存数据解析成功: ${key}`)
        return parsedData
      }

      // this.logger.log(`📭 缓存未命中: ${key}`)
      // this.logger.log(`   ⏱️ 查询耗时: ${readTime}ms`)
      return null
    } catch (error) {
      this.logger.error(`❌ 获取缓存失败: ${key}`, error)
      this.logger.error(`   错误详情: ${error.message}`)
      return null
    }
  }

  /**
   * 设置缓存数据
   * @param key 缓存键
   * @param data 数据
   * @param ttl 过期时间（秒），0表示永久缓存
   */
  async set(key: string, data: any, ttl: number = 0): Promise<boolean> {
    try {
      // 检查Redis连接状态
      if (this.redis.status !== 'ready') {
        this.logger.warn(`Redis未就绪，状态: ${this.redis.status}，跳过缓存设置`)
        return false
      }

      const serializedData = JSON.stringify(data)
      const dataSize = Buffer.byteLength(serializedData, 'utf8')

      if (ttl === 0) {
        // 永久缓存
        this.logger.log(`💾 设置永久缓存: ${key}, 大小: ${dataSize} bytes`)
        await this.redis.set(key, serializedData)
      } else {
        // 有TTL的缓存
        this.logger.log(`💾 设置缓存: ${key}, 大小: ${dataSize} bytes, TTL: ${ttl}秒`)
        await this.redis.setex(key, ttl, serializedData)
      }

      // 验证缓存是否设置成功
      const verifyResult = await this.redis.exists(key)
      if (verifyResult === 1) {
        // 检查TTL是否正确设置
        const ttlResult = await this.redis.ttl(key)
        if (ttl === 0) {
          this.logger.log(`✅ 永久缓存设置成功并验证通过: ${key}, TTL: ${ttlResult}秒`)
        } else {
          this.logger.log(`✅ 缓存设置成功并验证通过: ${key}, TTL: ${ttlResult}秒`)
        }

        if (ttlResult === -1) {
          if (ttl === 0) {
            this.logger.log(`✅ 永久缓存设置成功: ${key} 将永不过期`)
          } else {
            this.logger.warn(`⚠️ 警告: 缓存 ${key} 没有设置TTL，将永不过期`)
          }
        } else if (ttlResult === -2) {
          this.logger.error(`❌ 错误: 缓存 ${key} 不存在`)
          return false
        }

        return true
      }
      this.logger.error(`❌ 缓存设置失败，验证不通过: ${key}`)
      return false
    } catch (error) {
      this.logger.error(`设置缓存失败: ${key}`, error)
      return false
    }
  }

  /**
   * 删除缓存
   * @param key 缓存键
   */
  async del(key: string): Promise<boolean> {
    try {
      await this.redis.del(key)
      return true
    } catch (error) {
      this.logger.error(`删除缓存失败: ${key}`, error)
      return false
    }
  }

  /**
   * 批量删除缓存（按模式）
   * @param pattern 模式匹配
   */
  async delPattern(pattern: string): Promise<number> {
    try {
      const keys = await this.redis.keys(pattern)
      if (keys.length > 0) {
        return await this.redis.del(...keys)
      }
      return 0
    } catch (error) {
      this.logger.error(`批量删除缓存失败: ${pattern}`, error)
      return 0
    }
  }

  /**
   * 检查键是否存在
   * @param key 缓存键
   */
  async exists(key: string): Promise<boolean> {
    try {
      const result = await this.redis.exists(key)
      return result === 1
    } catch (error) {
      this.logger.error(`检查缓存键失败: ${key}`, error)
      return false
    }
  }

  /**
   * 设置键的过期时间
   * @param key 缓存键
   * @param ttl 过期时间（秒）
   */
  async expire(key: string, ttl: number): Promise<boolean> {
    try {
      const result = await this.redis.expire(key, ttl)
      return result === 1
    } catch (error) {
      this.logger.error(`设置过期时间失败: ${key}`, error)
      return false
    }
  }

  /**
   * 获取键的剩余过期时间
   * @param key 缓存键
   * @returns 剩余秒数，-1表示永不过期，-2表示键不存在
   */
  async ttl(key: string): Promise<number> {
    try {
      if (this.redis.status !== 'ready') {
        return -2
      }
      return await this.redis.ttl(key)
    } catch (error) {
      this.logger.error(`获取TTL失败: ${key}`, error)
      return -2
    }
  }

  /**
   * 获取或设置缓存数据（带锁机制）
   * @param key 缓存键
   * @param fetchFn 获取数据的函数
   * @param ttl 过期时间（秒）
   * @param lockTimeout 锁超时时间（秒）
   */
  async getOrSet<T>(key: string, fetchFn: () => Promise<T>, ttl: number = 300, lockTimeout: number = 10): Promise<T> {
    // 检查Redis连接状态
    if (this.redis.status !== 'ready') {
      this.logger.warn(`Redis未就绪，状态: ${this.redis.status}，直接执行查询`)
      return await fetchFn()
    }

    try {
      // 先尝试获取缓存
      const cached = await this.get<T>(key, ttl)
      if (cached !== null) {
        return cached
      }

      // 使用分布式锁避免重复查询
      const lockKey = `${key}:lock`
      const lockValue = Date.now().toString()

      // 尝试获取锁
      const lockResult = await this.redis.set(lockKey, lockValue, 'EX', lockTimeout, 'NX')

      if (lockResult === 'OK') {
        // 获取锁成功，执行查询（带超时控制）
        try {
          const data = await Promise.race([
            fetchFn(),
            new Promise<never>((_, reject) =>
              setTimeout(() => reject(new Error('Data fetch timeout')), config.TIMEOUT.REDIS_OPERATION)
            )
          ])
          await this.set(key, data, ttl)
          return data
        } finally {
          // 释放锁
          try {
            await this.redis.del(lockKey)
          } catch (delError) {
            this.logger.warn(`释放锁失败: ${lockKey}`, delError)
          }
        }
      } else {
        // 获取锁失败，等待一段时间后重试
        await new Promise((resolve) => setTimeout(resolve, 100))
        return this.getOrSet(key, fetchFn, ttl, lockTimeout)
      }
    } catch (error) {
      this.logger.error(`获取或设置缓存失败: ${key}`, error)
      // 如果缓存失败，直接执行查询
      return await fetchFn()
    }
  }

  /**
   * 测试Redis连接
   */
  async testConnection(): Promise<boolean> {
    try {
      const result = await this.redis.ping()
      this.logger.log(`Redis连接测试: ${result}`)
      return result === 'PONG'
    } catch (error) {
      this.logger.error('Redis连接测试失败:', error)
      return false
    }
  }

  /**
   * 获取Redis连接状态
   */
  getConnectionStatus(): string {
    return this.redis.status
  }

  /**
   * 获取Redis连接信息（用于诊断）
   */
  getConnectionInfo(): {
    status: string
    host: string
    port: number
    db: number
    usingUrl: boolean
  } {
    const options = this.redis.options
    return {
      status: this.redis.status,
      host: options.host || 'unknown',
      port: options.port || 6379,
      db: options.db || 0,
      usingUrl: !!process.env.REDIS_URL
    }
  }

  /**
   * 启动连接健康检查
   */
  private startHealthCheck(): void {
    // 每10秒检查一次连接状态
    setInterval(async () => {
      try {
        const status = this.redis.status
        if (status === 'ready') {
          // 每2分钟检查一次内存使用情况
          if (Date.now() % 120000 < 10000) {
            // 每2分钟检查一次
            await this.checkRedisMemory()
          }
        } else if (status === 'connecting' || status === 'wait') {
          this.logger.warn(`⚠️ Redis连接状态异常: ${status}，尝试重新连接`)
          // 如果连接状态异常，尝试重新连接
          if (status === 'wait') {
            this.redis.disconnect()
            this.redis.connect()
          }
        } else {
          this.logger.error(`❌ Redis连接状态严重异常: ${status}`)
        }
      } catch (error) {
        this.logger.error('❌ Redis健康检查失败:', error)
        // 尝试重新连接
        try {
          this.redis.disconnect()
          this.redis.connect()
        } catch (reconnectError) {
          this.logger.error('❌ Redis重连失败:', reconnectError)
        }
      }
    }, 10000) // 改为每10秒检查一次
  }

  /**
   * 手动检查Redis内存使用情况（公开方法）
   */
  async checkRedisMemoryNow(): Promise<void> {
    await this.checkRedisMemory()
  }

  /**
   * 检查Redis内存使用情况
   */
  private async checkRedisMemory(): Promise<void> {
    try {
      const info = await this.redis.info('memory')
      const lines = info.split('\r\n')
      const memoryInfo: any = {}

      lines.forEach((line) => {
        if (line.includes(':')) {
          const [key, value] = line.split(':')
          memoryInfo[key] = value
        }
      })

      const usedMemory = parseInt(memoryInfo.used_memory || '0')
      const maxMemory = parseInt(memoryInfo.maxmemory || '0')
      const usedMemoryHuman = memoryInfo.used_memory_human || '0B'
      const maxMemoryHuman = memoryInfo.maxmemory_human || '0B'

      this.logger.log(`💾 Redis内存使用: ${usedMemoryHuman} / ${maxMemoryHuman}`)

      if (maxMemory > 0) {
        const usagePercent = (usedMemory / maxMemory) * 100
        this.logger.log(`📊 Redis内存使用率: ${usagePercent.toFixed(2)}%`)

        if (usagePercent > 80) {
          this.logger.warn(`⚠️ Redis内存使用率过高: ${usagePercent.toFixed(2)}%`)
        }
      }

      // 检查内存策略
      const evictionPolicy = memoryInfo.maxmemory_policy || 'noeviction'
      this.logger.log(`🔧 Redis内存策略: ${evictionPolicy}`)
    } catch (error) {
      this.logger.error('❌ Redis内存检查失败:', error)
    }
  }

  /**
   * 强制重新连接Redis
   */
  async forceReconnect(): Promise<void> {
    try {
      this.logger.log('强制重新连接Redis...')
      await this.redis.quit()
      // 等待一秒后重新连接
      setTimeout(() => {
        this.redis.connect()
      }, 1000)
    } catch (error) {
      this.logger.error('强制重连Redis失败:', error)
    }
  }

  /**
   * 预初始化Redis连接（在应用启动时调用）
   * 确保Redis连接在应用启动时就建立好
   */
  static async preInitialize(): Promise<CacheService> {
    if (!CacheService.instance) {
      const instance = new CacheService()
      // 等待连接建立
      await new Promise<void>((resolve) => {
        const checkConnection = () => {
          if (instance.redis.status === 'ready') {
            resolve()
          } else {
            setTimeout(checkConnection, 100)
          }
        }
        checkConnection()
      })
      return instance
    }
    return CacheService.instance
  }

  /**
   * 获取单例实例（如果不存在则创建）
   */
  static getInstance(): CacheService {
    if (!CacheService.instance) {
      CacheService.instance = new CacheService()
    }
    return CacheService.instance
  }

  /**
   * 关闭Redis连接
   */
  async close(): Promise<void> {
    await this.redis.quit()
  }
}
