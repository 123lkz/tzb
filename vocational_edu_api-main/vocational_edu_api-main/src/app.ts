require('dotenv').config()
import { createCloverApp, setEnv } from '@havenzhang/clover'
import { ConsoleLogger } from '@nestjs/common'
import { AppModule } from './app.module'
import { AdminModule } from './base/admin.module'
import config from './config/config'
import './database' // 必须在 Module 之前导入，确保先完成连接创建
import { CacheService } from './services/CacheService'
import { connectDatabase } from './utils/DatabaseUtils'

setEnv(['CLOVER_API_DBNAME', 'clover_main.db'])
setEnv(['CLOVER_API_BASEURL', '/vocational_edu_api'])

async function bootstrap() {
  const logger = new ConsoleLogger()
  logger.log('start MongoDB connect...')
  await connectDatabase(['main', 'da'])
  logger.log('MongoDB connected...')

  // 预初始化Redis连接
  try {
    logger.log('start Redis connect...')
    await CacheService.preInitialize()
    logger.log('Redis connected...')
  } catch (error) {
    logger.error('Redis initialization failed:', error)
    // 不阻止应用启动，但会在后续操作中处理连接问题
  }

  const app = await createCloverApp({
    globalPrefix: '/zjapi',
    appModule: AppModule,
    adminModule: AdminModule,
    cloverApi: process.env.DEPLOY_ENV === 'test'
  })

  // 设置HTTP请求超时时间为1小时
  app.use((req: any, res: any, next: any) => {
    req.setTimeout(config.TIMEOUT.HTTP_REQUEST, () => {
      res.status(408).json({ error: 'Request timeout' })
    })
    res.setTimeout(config.TIMEOUT.HTTP_REQUEST, () => {
      res.status(408).json({ error: 'Response timeout' })
    })
    next()
  })

  app.enableCors({
    origin: [
      'http://localhost:8567',
      'http://localhost:8568',
      'https://tte.smartedu.work' // 正式环境
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Custom-Header', 'X-Requested-With', 'x-client-info', 'If-Match'],
    credentials: true,
    maxAge: 3600
  })

  // 添加健康检查端点
  app.use('/health', (req: any, res: any) => {
    res.status(200).json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      version: process.env.npm_package_version || '1.0.0'
    })
  })

  const port = config.PORT || 3008
  setTimeout(() => {
    logger.log('App start listen on http://localhost:' + port + '/vocational_edu_api/')
  }, 2000)

  await app.listen(port, '0.0.0.0')
}

bootstrap()
