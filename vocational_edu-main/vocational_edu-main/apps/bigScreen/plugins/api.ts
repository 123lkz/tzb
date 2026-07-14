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
      return response.data
    },
    extractItems: (data, url) => {
      // 根据实际的数据结构来提取 items
      if (data && typeof data === 'object' && '_items' in data) {
        return data._items.map((item: any) => ({
          id: item._id || item.id,
          data: item
        }))
      }
      return null
    },
    errorHandler: (error, api) => {
      console.error('API Error:', error)
      return error
    }
  })
})
