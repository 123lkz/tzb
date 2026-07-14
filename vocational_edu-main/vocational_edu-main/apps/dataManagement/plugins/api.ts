import { initApi } from '@base/api/Api'

export default defineNuxtPlugin(() => {
  // 初始化 API
  initApi({
    baseUrl: () => {
      // 在开发环境中使用代理路径，生产环境使用完整 URL
      if (import.meta.dev) {
        return '/zjapi'
      }
      const config = useRuntimeConfig()
      return config.public.api || 'https://tte-api.smartedu.work/zjapi'
    },
    responseHandler: (response) => {
      // 对于文件下载，返回完整的响应对象
      if (
        response.config?.responseType === 'blob' ||
        response.headers?.['content-type']?.includes('application/vnd.openxmlformats-officedocument') ||
        response.headers?.['content-type']?.includes('application/octet-stream')
      ) {
        return response
      }
      return response.data
    },
    extractItems: (data) => {
      // 根据实际的数据结构来提取 items
      if (data && typeof data === 'object' && '_items' in data) {
        return data._items.map((item: Record<string, any>) => ({
          id: item._id || item.id,
          data: item
        }))
      }
      return null
    },
    errorHandler: (error) => {
      console.error('API Error:', error)
      return error
    }
  })
})
