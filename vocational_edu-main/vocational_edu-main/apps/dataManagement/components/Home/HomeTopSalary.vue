<script setup lang="ts">
import Icon from '../common/Icon.vue'
import Tooltip from '../common/Tooltip.vue'
import StackedLineChart from '../Echart/StackedLineChart.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

// 薪资数据
const salaryData = [
  { title: '薪资25%分位数', value: 8500, color: 'from-blue-400/30 to-cyan-400/10' },
  { title: '薪资中位数', value: 12000, color: 'from-orange-400/30 to-yellow-400/10' },
  { title: '薪资75%分位数', value: 18000, color: 'from-green-400/30 to-emerald-400/10' },
]

// 创建动画实例
const animations = salaryData.map(() => {
  const { formattedValue, animateNumber, resetToZero } = useNumberAnimation()
  return { formattedValue, animateNumber, resetToZero }
})

// 组件挂载后启动动画
onMounted(() => {
  // 延迟启动动画，确保组件完全渲染
  setTimeout(() => {
    salaryData.forEach((item, index) => {
      animations[index].resetToZero()
      setTimeout(() => {
        animations[index].animateNumber(item.value, 1500, true)
      }, index * 200) // 每个卡片延迟200ms启动动画
    })
  }, 300)
})

const title = ref('薪资分布')
const indicatorDesc = ref('薪资分布')
const data = ref([
  {
    name: '2025-01',
    values: [
      { name: '10%分位数', value: 3060 },
      { name: '25%分位数', value: 4060 },
      { name: '薪资中位数', value: 5060 },
      { name: '75%分位数', value: 6060 },
      { name: '90%分位数', value: 7060 },
    ],
  },
  {
    name: '2025-02',
    values: [
      { name: '10%分位数', value: 3160 },
      { name: '25%分位数', value: 4160 },
      { name: '薪资中位数', value: 5160 },
      { name: '75%分位数', value: 6160 },
      { name: '90%分位数', value: 7160 },
    ],
  },
  {
    name: '2025-03',
    values: [
      { name: '10%分位数', value: 3360 },
      { name: '25%分位数', value: 4360 },
      { name: '薪资中位数', value: 5360 },
      { name: '75%分位数', value: 6360 },
      { name: '90%分位数', value: 7360 },
    ],
  },
  {
    name: '2025-04',
    values: [
      { name: '10%分位数', value: 3560 },
      { name: '25%分位数', value: 4560 },
      { name: '薪资中位数', value: 5560 },
      { name: '75%分位数', value: 6560 },
      { name: '90%分位数', value: 7560 },
    ],
  },
  {
    name: '2025-05',
    values: [
      { name: '10%分位数', value: 3760 },
      { name: '25%分位数', value: 4760 },
      { name: '薪资中位数', value: 5760 },
      { name: '75%分位数', value: 6760 },
      { name: '90%分位数', value: 7760 },
    ],
  },
  {
    name: '2025-06',
    values: [
      { name: '10%分位数', value: 3960 },
      { name: '25%分位数', value: 4960 },
      { name: '薪资中位数', value: 5960 },
      { name: '75%分位数', value: 6960 },
      { name: '90%分位数', value: 7960 },
    ],
  },
])
</script>

<template>
  <div
    class="w-full h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 mb-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 flex flex-col"
  >
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="w-6 h-6 rounded-full bg-[#00ffff]/20 flex items-center justify-center">
          <Icon name="icon-qiandai" :color="'#00ffff'" :size="16" />
        </div>
        <span class="text-[#00ffff] text-sm">{{ title }}</span>
      </div>
      <Tooltip :content="indicatorDesc" placement="bottom">
        <template #trigger>
          <div
            class="flex w-4 h-4 items-center justify-center border border-white/50 rounded-full cursor-help text-white/50"
          >
            <span class="text-xs scale-75">i</span>
          </div>
        </template>
        <div class="min-w-32">
          <div class="font-bold mb-1 text-sm text-gray-600">指标描述：</div>
          <div class="text-xs text-gray-400 whitespace-nowrap break-all">{{ indicatorDesc }}</div>
        </div>
      </Tooltip>
    </div>
    <div class="grid grid-cols-3 gap-2 my-4">
      <div
        v-for="(item, index) in salaryData"
        :key="index"
        class="bg-gradient-to-br p-2 rounded-lg border border-white/10 shadow-sm hover:shadow-md transition-all duration-300"
        :class="item.color"
      >
        <!-- 标题 -->
        <div class="text-xs text-white/80 mb-1">
          {{ item.title }}
        </div>

        <!-- 数值和单位 -->
        <div class="flex items-baseline gap-1">
          <span class="text-sm font-bold text-white font-DIN-Medium">
            {{ animations[index].formattedValue }}
          </span>
          <span class="text-xs text-white/70">元</span>
        </div>
      </div>
    </div>
    <div class="flex-1 min-h-0">
      <StackedLineChart
        width="100%"
        height="100%"
        :show-legend="false"
        :show-y-axis="false"
        :show-all-x-axis-labels="true"
        :use-smooth-line="true"
        :data="data"
        highlight-x-value="2025-03"
        :colors="['#a855f7', '#3b82f6', '#ef4444', '#10b981', '#f97316']"
      />
    </div>
  </div>
</template>

<style scoped>
/* 确保渐变效果平滑 */
.bg-gradient-to-br {
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
