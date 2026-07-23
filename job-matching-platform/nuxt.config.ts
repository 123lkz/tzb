import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  typescript: { strict: true },
  app: {
    head: {
      title: '新一代信息技术岗位全景图谱 - 人岗匹配平台',
      htmlAttrs: { lang: 'zh-CN' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    },
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' }
  },
  compatibilityDate: '2025-06-13',
  devServer: {
    host: '0.0.0.0',
    port: 8570
  },
  css: ['~/assets/css/common.css'],
  vite: {
    assetsInclude: ['**/*.svg']
  }
})
