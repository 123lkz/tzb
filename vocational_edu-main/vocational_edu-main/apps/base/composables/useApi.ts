import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
// import { useAuthStore } from '~/stores/auth'

// 类型定义
type ApiResponse<T = any> = {
  data: T
}

type RequestConfig = AxiosRequestConfig & {
  silent?: boolean // 是否静默请求（不显示错误提示）
  retry?: boolean // 是否自动重试
  _retry?: boolean // 内部使用，标记是否已经重试过
}

// TODO 在 nuxt.config.ts 中设置
const getBaseURL = () => {
  // SSR 阶段逻辑
  if (process.server) {
    return 'http://localhost:8569/zjapi'
  }

  // CSR 阶段逻辑
  return 'https://tte-api.smartedu.work/zjapi'
}

// 创建axios实例
const instance = axios.create({
  baseURL: getBaseURL(),
  timeout: 30000,
  withCredentials: true,
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// 请求队列处理（用于刷新Token时暂停请求）
const isRefreshing = false
const requests: ((token: string) => void)[] = []

/**
 * 请求拦截器
 * 2. 添加认证Token
 * 3. 添加客户端信息
 */
instance.interceptors.request.use(
  (config: RequestConfig) => {
    // 添加认证Token
    /*   const authStore = useAuthStore()
    config.headers.Authorization = authStore.token ? `Bearer ${authStore.token}` : '' */
    // 自动添加客户端信息
    config.headers['X-Client-Info'] = JSON.stringify({
      platform: process.client ? 'web' : 'server',
      version: process.env.APP_VERSION || '1.0.0'
    })
    if (config.body instanceof FormData) {
      config.headers['Content-Type'] = 'multipart/form-data'
    } else {
      config.headers['Content-Type'] = 'application/json;charset=UTF-8'
      // 如果是 JSON 数据，确保数据正确序列化
      if (config.body) {
        config.data = JSON.stringify(config.body)
      }
    }

    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 1. 处理业务逻辑错误
 * 2. 处理Token过期
 * 3. 处理其他HTTP错误
 */
instance.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // 业务逻辑错误处理
    if ([200, 201].includes(response.status)) {
      return response
    }
    return handleBusinessError(response.data, response.config)
  },
  async (error: AxiosError) => {
    const { config, response } = error

    // 处理网络错误
    if (!response) {
      return handleNetworkError(error)
    }

    const originalRequest = config as RequestConfig

    // Token过期处理
    /*     if (response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (!isRefreshing) {
        const authStore = useAuthStore()
        isRefreshing = true
        try {
          const res = await $user.RefreshToken()
          isRefreshing = false
          requests.forEach((cb) => cb(authStore.token))
          requests = []
          return instance(originalRequest)
        } catch (e) {
          authStore.logout()
          return Promise.reject(e)
        }
      }

      return new Promise((resolve) => {
        requests.push((token: string) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          resolve(instance(originalRequest))
        })
      })
    } */

    // 其他HTTP错误处理
    return Promise.reject(handleHttpError(response.status, response.data, originalRequest))
  }
)

// 错误处理函数
function handleBusinessError(data, config: RequestConfig) {
  return Promise.reject(data)
}

function handleNetworkError(error: AxiosError) {
  return Promise.reject({ code: -1, message: '网络错误' })
}

function handleHttpError(status: number, data: any, config: RequestConfig) {
  const errorMap: Record<number, string> = {
    400: '请求参数错误',
    403: '拒绝访问',
    404: '资源未找到',
    500: '服务器内部错误',
    503: '服务不可用'
  }

  const message = data?.message || errorMap[status] || '未知错误'

  if (!config.silent) {
    // useNuxtApp().$toast.error(message)
  }

  return Promise.reject({
    code: status,
    message,
    data
  })
}

export const API = {
  request: async <T = any>(config: AxiosRequestConfig): Promise<T> => {
    try {
      if (config.path) {
        config.url = config.path
        delete config.path
      }

      if (config.query) {
        config.params = config.query
        delete config.query
      }

      const response = await instance(config)
      return response.data
    } catch (error) {
      throw error
    }
  }
}
