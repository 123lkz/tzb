<script setup lang="ts">
import Icon from '../common/Icon.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import HorizontalBarChart from '../Echart/HorizontalBarChart.vue'
import Tooltip from '../common/Tooltip.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

interface Props {
  title: string // 标题
  titleIcon: string // 标题图标
  titleIconSize?: string | number // 标题图标大小
  indicatorDesc?: string // 指标描述
  subtext: string // 副标题
  chartData: Array<{ name: string; value: number }> // 图表数据
  quantifier?: string // 数量单位
  barColors?: string[] // 图表颜色
  tooltipTitle?: string // 图表标题
  changeLabel?: string // 变化率标签
  changeRate?: number // 变化率
  isStatAll?: boolean
  isStatYear?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  titleIcon: '',
  titleIconSize: 16,
  indicatorDesc: '',
  subtext: '',
  quantifier: '',
  chartData: () => [],
  barColors: () => ['#80FFA5', '#adfdc5'],
  tooltipTitle: '',
  changeLabel: '较上月',
  changeRate: 0,
  isStatAll: true,
  isStatYear: false,
})

const firstData = ref(props.chartData[0])
const { formattedValue, animateNumber, resetToZero } = useNumberAnimation()

// 监听 firstData 变化，触发动画
watch(
  () => firstData.value,
  newData => {
    if (newData && newData.value) {
      resetToZero() // 先重置到0
      // 延迟一点时间确保组件完全渲染后再开始动画
      setTimeout(() => {
        animateNumber(newData.value, 1000, true)
      }, 200)
    }
  },
  { immediate: true }
)

// 监听 chartData 变化，更新 firstData
watch(
  () => props.chartData,
  newChartData => {
    if (newChartData && newChartData.length > 0) {
      firstData.value = newChartData[0]
    }
  },
  { immediate: true }
)
</script>

<template>
  <div
    class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1"
  >
    <div class="flex items-center justify-between">
      <SecondTitle :title="title" :icon="titleIcon" :subtext="subtext" :icon-size="titleIconSize" />
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
      <HorizontalBarChart
        :data="props.chartData"
        :quantifier="props.quantifier"
        :bar-colors="props.barColors"
        :is-smooth-line="true"
        :is-show-province-data="true"
        :tooltip-title="props.tooltipTitle"
        height="240px"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
        :scroll-step="10"
      />
    </div>
    <div class="border-b border-[#00ffff]/20 mb-2"></div>
    <div class="flex justify-between items-center h-6">
      <div class="flex items-center gap-1">
        <Icon name="icon-remen" color="#FFBF00" :size="16" />
        <span class="text-sm text-[#FFBF00]">{{ firstData.name }}</span>
      </div>
      <div class="flex items-baseline gap-1">
        <span class="text-lg font-DIN-Medium font-bold text-[#FFBF00]">{{ formattedValue }}</span>
        <span class="text-xs text-[#FFBF00]/70">{{ quantifier }}</span>
      </div>
    </div>
  </div>
</template>
