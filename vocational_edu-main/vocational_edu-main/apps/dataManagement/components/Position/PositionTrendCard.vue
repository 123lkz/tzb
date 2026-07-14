<script setup lang="ts">
import Icon from '../common/Icon.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import Tooltip from '../common/Tooltip.vue'
import LineMixedBarChart from '../Echart/LineMixedBarChart.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

interface Props {
  title: string // 标题
  value: number // 值
  indicatorDesc: string // 指标描述
  quantifier: string // 数量单位
  chartData: Array<{ name: string; value: number }> // 图表数据
  colors?: string[] // 图表颜色
  changeLabel?: string // 变化率标签
  changeRate: number // 变化率
  isSmoothLine?: boolean
  height?: string
  isStatAll?: boolean
  isStatYear?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  value: 0,
  indicatorDesc: '',
  quantifier: '',
  chartData: () => [],
  colors: () => ['#80FFA5', '#198CEF'],
  changeLabel: '较上月',
  changeRate: 0,
  isSmoothLine: true,
  height: '100%',
  isStatAll: true,
  isStatYear: false,
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
    <FirstTitle :title="title" />
    <div class="flex justify-between items-center">
      <div class="flex items-baseline gap-1 my-2">
        <span class="text-2xl font-DIN-Medium font-bold text-[#00ffff]">{{ formattedValue }}</span>
        <span class="text-xs text-white/70">{{ quantifier }}</span>
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

    <div class="flex-1 min-h-0 mb-2">
      <LineMixedBarChart
        :data="props.chartData"
        :quantifier="props.quantifier"
        :bar-color="props.colors[0]"
        :is-smooth-line="props.isSmoothLine"
        :tooltip-title="props.title"
        height="200px"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
      />
    </div>

    <div class="border-b border-[#00ffff]/20 mb-2"></div>

    <div class="flex items-center justify-between h-6">
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
