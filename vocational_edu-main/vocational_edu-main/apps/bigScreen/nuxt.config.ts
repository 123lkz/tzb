export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],
  typescript: {
    strict: true,
  },
  vite: {
    resolve: {
      alias: {
        '@base': new URL('../../apps/base', import.meta.url).pathname,
      },
    },
    server: {
      proxy: {
        '/zjapi': {
          target: 'https://tte-api.smartedu.work',
          changeOrigin: true,
          secure: true,
        },
      },
    },
    assetsInclude: ['**/*.svg'],
  },
  app: {
    baseURL: '/zjscreen',
    head: {
      title: '国家职业教育人才供需动态匹配平台',
      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico',
        },
      ],
      htmlAttrs: {
        lang: 'zh-CN',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    },
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' },
  },
  compatibilityDate: '2025-06-13',
  devServer: {
    host: '0.0.0.0',
    port: '8567',
  },
  devtools: { enabled: true },
  nitro: {
    output: {
      dir: '../../dist/bigScreen',
    },
    devProxy: {
      '/zjapi': {
        target: 'https://tte-api.smartedu.work',
        changeOrigin: true,
      },
    },
  },
  runtimeConfig: {
    public: {
      version: require('./package.json').version,
      deployEnv: process.env.DEPLOY_ENV,
      api: 'https://tte-api.smartedu.work/zjapi',
    },
  },
})
