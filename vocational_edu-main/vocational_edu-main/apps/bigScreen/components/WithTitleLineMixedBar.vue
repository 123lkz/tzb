<script lang="ts" setup>
import LineMixedBarChart from './Echart/LineMixedBarChart.vue'
import TitleHeader from './TitleHeader.vue'

interface ChartData {
  months: string[]
  totalCount: number[]
  changeRate: number[]
}

interface Props {
  data: ChartData
  title: string
  unit: string
  barColor?: string
  isSmoothLine?: boolean
  tooltipTitle?: string
  height?: string
  isStatAll?: boolean
  isStatYear?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  barColor: '#0066FF',
  isSmoothLine: true,
  height: '100%',
  isStatAll: true,
  isStatYear: false,
  tooltipTitle: ''
})
</script>

<template>
  <div class="w-full h-full p-2 flex flex-col">
    <TitleHeader :title="props.title" />
    <div class="flex-1 min-h-0">
      <LineMixedBarChart
        :data="{
          xAxisValue: props.data.months,
          yAxisValue: props.data.totalCount,
          changeRate: props.data.changeRate
        }"
        :unit="props.unit"
        :bar-color="props.barColor"
        :is-smooth-line="props.isSmoothLine"
        :tooltip-title="props.tooltipTitle"
        :height="props.height"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
      />
    </div>
  </div>
</template>
