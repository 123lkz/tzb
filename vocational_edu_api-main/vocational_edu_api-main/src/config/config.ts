import * as process from 'process'

require('dotenv').config()

export default {
  ENV: process.env.NODE_ENV,

  DEPLOY_ENV: process.env.DEPLOY_ENV,

  OPENAPI: process.env.OPENAPI === '1',

  DATABASE: {
    main: {
      // 主要数据库 URI
      uri: process.env.MONGO_URI
    },
    da: {
      // 数据分析库 URI
      uri: process.env.DA_MONGO_URI
    }
  },

  // Jwt secret
  TOKEN_SECRET: process.env.TOKEN_SECRET,

  // 服务端口
  PORT: process.env.PORT,

  // REDIS
  REDIS_URL: process.env.REDIS_URL,
  REDIS_HOST: process.env.REDIS_HOST,
  REDIS_PORT: parseInt(process.env.REDIS_PORT) || 6379,
  REDIS_PASSWORD: process.env.REDIS_PASSWORD,
  REDIS_DB: parseInt(process.env.REDIS_DB) || 0,
  REDIS_DB_ES: parseInt(process.env.REDIS_DB_ES) || 0,

  SMTP: {
    account: {
      user: process.env.SMTP_ACCOUNT_USER,
      pass: process.env.SMTP_ACCOUNT_PASS
    }
  },

  // 超时配置（毫秒）
  TIMEOUT: {
    // HTTP请求超时：1小时
    HTTP_REQUEST: parseInt(process.env.HTTP_REQUEST_TIMEOUT) || 3600000, // 1小时
    // 数据库查询超时：1小时
    DATABASE_QUERY: parseInt(process.env.DATABASE_QUERY_TIMEOUT) || 3600000, // 1小时
    // Redis操作超时：1小时
    REDIS_OPERATION: parseInt(process.env.REDIS_OPERATION_TIMEOUT) || 3600000, // 1小时
    // 应用程序启动超时：1小时
    APP_STARTUP: parseInt(process.env.APP_STARTUP_TIMEOUT) || 3600000 // 1小时
  }
} as const
