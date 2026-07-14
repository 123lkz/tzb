<script setup lang="ts">
import Icon from '../common/Icon.vue'
import Tooltip from '../common/Tooltip.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

interface Props {
  icon: string // 自定义图标
  title: string // 标题
  value: number // 值
  indicatorDesc: string // 指标描述
  quantifier: string // 数量单位
  chartData: Array<{ name: string; value: number }> // 图表数据
  colors?: string[] // 图表颜色
  changeLabel?: string // 变化率标签
  changeRate: number // 变化率
}

const props = withDefaults(defineProps<Props>(), {
  icon: '',
  title: '',
  value: 0,
  indicatorDesc: '',
  quantifier: '',
  chartData: () => [],
  colors: () => ['#80FFA5', '#198CEF'],
  changeLabel: '较上月',
  changeRate: 0,
})

// 使用数字动画
const { formattedValue, animateNumber, resetToZero } = useNumberAnimation()

// 监听 value 变化，触发动画
watch(
  () => props.value,
  (newValue: number) => {
    animateNumber(newValue, 1000, true) // 确保从0开始
  },
  { immediate: true }
)

// pageKey 用于强制刷新子组件
const pageKey = ref(Date.now())

// 监听页面尺寸变化，更新 pageKey
const handleResize = () => {
  pageKey.value = Date.now()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

// 组件挂载后确保从0开始动画
onMounted(() => {
  resetToZero() // 先重置到0
  // 延迟一点时间确保组件完全渲染后再开始动画
  setTimeout(() => {
    animateNumber(props.value, 1000, true)
  }, 200)
})
</script>

<template>
  <div
    class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex flex-col flex-1"
  >
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center gap-2">
        <div class="w-6 h-6 rounded-full bg-[#00ffff]/20 flex items-center justify-center">
          <Icon :name="icon" :color="'#00ffff'" :size="16" />
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

    <div class="flex items-baseline gap-1 mb-2">
      <span class="text-xl font-DIN-Medium font-bold text-[#00ffff]">{{ formattedValue }}</span>
      <span class="text-xs text-white/70">{{ quantifier }}</span>
    </div>

    <div class="mb-2 flex-1 min-h-0">
      <GradientBarChart
        :key="pageKey"
        width="100%"
        height="100%"
        :data="chartData"
        :x-axis-rotate="0"
        :show-y-axis="false"
        :bar-gradient="{
          startColor: props.colors[1] || 'rgba(255,255,255,0.1',
          endColor: props.colors[0],
        }"
        :tooltip-title="title"
        :quantifier="quantifier"
        :show-legend="false"
        :show-label="false"
        :grid="{
          top: '0',
          bottom: '0%',
          left: '-10%',
          right: '5%',
        }"
      />
    </div>

    <div class="border-b border-[#00ffff]/20 mb-2"></div>

    <div class="flex items-center justify-between">
      <span class="text-xs text-gray-300">{{ changeLabel }}</span>
      <div class="flex items-center gap-1">
        <Icon v-if="changeRate > 0" name="icon-shangsheng" color="text-green-400" :size="12" />
        <Icon v-else-if="changeRate < 0" name="icon-xiajiang" color="text-red-400" :size="12" />
        <span
          class="text-xs font-medium"
          :class="
            changeRate > 0 ? 'text-green-400' : changeRate < 0 ? 'text-red-400' : 'text-gray-400'
          "
        >
          {{ changeRate > 0 ? '+' : '' }}{{ changeRate.toFixed(1) }}%
        </span>
      </div>
    </div>
  </div>
</template>
