import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {},
  },
  app: {
    baseURL: '/zj',
    head: {
      script: [{ src: '/zj/three.js' }]
    }
  },
  build: {
    transpile: [/echarts/]
  },
  nitro: {
    output: {
      dir: '../../dist/bigScreen/.output'
    },
    devProxy: {
      // '/api/v2': 'https://next.smartedu.work/api/v2',
      // '/api/stat': 'http://192.168.3.2:9846/api/stat'
    }
  },
  plugins: [],
} satisfies Config 