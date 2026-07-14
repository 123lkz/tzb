<script setup lang="ts">
import Icon from '../common/Icon.vue'
import Tooltip from '../common/Tooltip.vue'
import GradientAreaChart from '../Echart/GradientAreaChart.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

interface Props {
  icon: string // 自定义图标
  title: string // 标题
  value: number // 值
  indicatorDesc: string // 指标描述
  quantifier: string // 数量单位
  chartHeight?: string
  chartData: Array<{ name: string; values: number[] }> // 图表数据
  color?: string // 图表颜色
  changeLabel?: string // 变化率标签
  changeRate: number // 变化率
}

const props = withDefaults(defineProps<Props>(), {
  icon: '',
  title: '',
  value: 0,
  indicatorDesc: '',
  quantifier: '',
  chartHeight: '80px',
  chartData: () => [],
  color: () => '#80FFA5',
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
    class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1"
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
    <div class="flex justify-between items-center mb-2">
      <div class="flex items-baseline gap-1">
        <span class="text-lg font-DIN-Medium font-bold text-[#00ffff]">{{ formattedValue }}</span>
        <span class="text-xs text-white/70">{{ quantifier }}</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="text-xs text-white/70">{{ changeLabel }}</span>
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

    <GradientAreaChart
      :height="chartHeight"
      :data="chartData"
      :show-y-axis="false"
      :color="props.color"
      :tooltip-title="title"
      :quantifier="quantifier"
    />
  </div>
</template>
