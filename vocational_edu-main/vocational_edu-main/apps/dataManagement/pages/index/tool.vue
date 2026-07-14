<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import Icon from '@/components/common/Icon.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '工具助手', path: '/tool' },
]

const cardList = [
  {
    title: '自定义图表',
    description:
      '支持上传Excel数据，通过直观的拖拽式界面快速创建多种类型的图表。无需编写代码，即可生成专业的可视化图表。',
    icon: 'icon-shanxingtu',
    funcPoints: [
      '自定义维度过滤',
      '自定义图表样式',
      '拖拽式配置',
      '实时预览',
      '导出 Excel',
      '生成图表图片',
    ],
    link: '/tool-chart',
  },
  {
    title: 'AI分析',
    description:
      '深度集成AI能力，通过自然语言与数据进行交互。AI自动理解问题意图，执行分析并生成图文并茂的结论报告。',
    icon: 'icon-AIzhinengti',
    funcPoints: ['自然语言交互', '数据联动', '智能数据洞察', '趋势分析', 'AI分析报告'],
    link: '/tool-ai',
  },
]

const handleOpenLink = (link: string) => {
  useRouter().push(link)
}
</script>

<template>
  <div class="flex flex-col pl-4 pt-4">
    <div class="flex-shrink-0 mr-4">
      <Header
        :breadcrumbs="breadcrumbs"
        :show-province="false"
        :show-scope="false"
        :show-time="false"
      ></Header>
    </div>
    <div class="flex flex-col overflow-x-hidden pt-6">
      <div class="flex-shrink-0 mr-4 mb-6">
        <h1 class="text-2xl font-bold text-[#00eaff] mb-2">工具助手</h1>
        <p class="text-[#00eaff]/70 text-sm">选择您需要的工具来提升数据分析效率</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl">
        <div
          v-for="card in cardList"
          :key="card.title"
          class="group relative cursor-pointer"
          @click="handleOpenLink(card.link)"
        >
          <!-- 主卡片容器 -->
          <div
            class="relative max-h-96 bg-gradient-to-br from-slate-900/80 to-slate-800/60 backdrop-blur-xl rounded-2xl p-6 border border-[#00ffff]/30 shadow-2xl hover:shadow-[0_0_40px_rgba(0,255,255,0.3)] transition-all duration-500 hover:border-[#00ffff]/60 hover:transform hover:-translate-y-2 overflow-hidden"
          >
            <!-- 背景装饰图案 -->
            <div class="absolute inset-0 opacity-10">
              <div
                class="absolute top-6 right-6 w-16 h-16 border-2 border-[#00ffff]/50 rounded-lg rotate-12"
              ></div>

              <!-- 渐变装饰 -->
              <div
                class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-[#00ffff]/20 to-transparent rounded-full blur-xl"
              ></div>
              <div
                class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-purple-500/20 to-transparent rounded-full blur-lg"
              ></div>
            </div>

            <!-- 内容区域 -->
            <div class="relative z-10 h-full flex flex-col">
              <!-- 图标和标题区域 -->
              <div class="flex items-start justify-between mb-6">
                <div class="flex items-center space-x-4">
                  <div class="relative">
                    <div
                      class="w-16 h-16 bg-gradient-to-br from-[#6dd0ed]/70 to-[#92e4d0]/70 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300"
                    >
                      <Icon :name="card.icon" color="#fff" :size="32" />
                    </div>
                  </div>

                  <div>
                    <h3
                      class="text-2xl font-bold text-white mb-2 group-hover:text-[#00ffff] transition-colors duration-300"
                    >
                      {{ card.title }}
                    </h3>
                    <div
                      class="w-12 h-1 bg-gradient-to-r from-[#00ffff] to-cyan-400 rounded-full"
                    ></div>
                  </div>
                </div>
                <!-- 底部操作区域 -->
                <div class="flex items-center justify-end">
                  <div class="flex items-center space-x-2 text-[#00ffff]/70 text-sm">
                    <Icon name="icon-qianwang" color="#00ffff" :size="14" />
                    <span>立即体验</span>
                  </div>
                </div>
              </div>

              <!-- 描述 -->
              <p class="text-gray-300 text-sm leading-relaxed mb-6 flex-1">
                {{ card.description }}
              </p>

              <!-- 功能特点 -->
              <div class="grid grid-cols-2 gap-2">
                <div
                  v-for="funcPoint in card.funcPoints"
                  :key="funcPoint"
                  class="flex items-center text-xs text-gray-400 bg-slate-800/50 rounded-lg px-3 py-2 backdrop-blur-sm border border-slate-700/50 hover:border-[#00ffff]/30 transition-colors duration-300"
                >
                  <div class="w-1.5 h-1.5 bg-[#00ffff] rounded-full mr-2 flex-shrink-0"></div>
                  <span class="truncate">{{ funcPoint }}</span>
                </div>
              </div>
            </div>

            <!-- 悬停时的光效 -->
            <div
              class="absolute inset-0 bg-gradient-to-r from-[#00ffff]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
