export default defineNuxtPlugin(() => {
  // 只在客户端执行
  if (process.client) {
    // 获取 Nuxt 应用的 baseURL
    const config = useRuntimeConfig()
    const baseURL = config.app.baseURL || ''
    const iconfontPath = `${baseURL}/icons/iconfont.js`
    // 检查是否已经加载过
    if (document.querySelector(`script[src="${iconfontPath}"]`)) {
      return
    }

    // 动态加载 iconfont 脚本
    const script = document.createElement('script')
    script.src = iconfontPath
    script.async = true

    // 添加加载成功和失败的处理
    script.onload = () => {
      console.log('IconFont loaded successfully')
    }

    script.onerror = () => {
      console.error('Failed to load IconFont script from:', iconfontPath)
    }

    document.head.appendChild(script)
  }
})
