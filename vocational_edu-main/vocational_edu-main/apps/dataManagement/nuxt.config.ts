import { resolve } from 'path'
import { fileURLToPath } from 'url'
import Icons from 'unplugin-icons/vite'

const currentDir = fileURLToPath(new URL('.', import.meta.url))

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/icon'],
  typescript: {
    strict: true
  },
  app: {
    baseURL: '/zjdata',
    head: {
      title: '国家职业教育人才供需动态匹配数据中台',
      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico'
        }
      ],
      htmlAttrs: {
        lang: 'zh-CN'
      },
      meta: [{ charset: 'utf-8' }, { name: 'viewport', content: 'width=device-width, initial-scale=1' }]
    },
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' }
  },
  compatibilityDate: '2025-06-13',
  devServer: {
    host: '0.0.0.0',
    port: 8568
  },
  nitro: {
    output: {
      dir: '../../dist/dataManagement'
    },
    devProxy: {
      '/zjapi': {
        target: 'https://tte-api.smartedu.work',
        changeOrigin: true
      }
    }
  },
  alias: {
    '@base': resolve(currentDir, '../../apps/base')
  },
  vite: {
    resolve: {
      alias: {
        '@base': resolve(currentDir, '../../apps/base')
      }
    },
    server: {
      fs: {
        allow: [
          // 添加项目根目录
          resolve(currentDir, '../../'),
          resolve(currentDir, '../../apps/base')
        ]
      },
      proxy: {
        '/zjapi': {
          target: 'https://tte-api.smartedu.work',
          changeOrigin: true,
          secure: true
        }
      }
    },
    plugins: [
      Icons({
        autoInstall: true,
        compiler: 'vue3',
        customCollections: {
          // 可以在这里添加自定义图标集
        }
      })
    ]
  },
  runtimeConfig: {
    public: {
      version: require('./package.json').version,
      deployEnv: process.env.DEPLOY_ENV,
      api: 'https://tte-api.smartedu.work/zjapi'
    }
  },
  css: ['~/assets/css/fonts.css', '~/assets/css/common.css']
})
