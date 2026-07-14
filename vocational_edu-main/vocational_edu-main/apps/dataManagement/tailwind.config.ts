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
    extend: {
      fontFamily: {
        'DIN-Regular': ['DIN-Regular', 'sans-serif'],
        'DIN-Medium': ['DIN-Medium', 'sans-serif'],
        DIN: ['DIN-Regular', 'DIN-Medium', 'sans-serif'], // 保持向后兼容
      },
    },
  },
  plugins: [],
} satisfies Config
