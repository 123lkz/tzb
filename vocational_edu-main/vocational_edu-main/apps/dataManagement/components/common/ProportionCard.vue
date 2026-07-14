<script setup lang="ts">
import ProportionBarChart, { type DataItem } from '../Echart/ProportionBarChart.vue'
import FirstTitle from './Title/FirstTitle.vue'
import Card from './Card.vue'
import Icon from './Icon.vue'

withDefaults(
  defineProps<{
    title: string
    total: number
    quantifier: string
    changeRate: number
    chartData: DataItem[]
    chartHeight?: string
    tooltipTitle?: string
    unit?: string
    legend?: any
    grid?: any
    colors?: string[]
  }>(),
  {
    title: '',
    total: 0,
    quantifier: '',
    changeRate: 0,
    chartData: () => [],
    chartHeight: '210px',
    tooltipTitle: '',
    unit: '万',
    legend: {
      bottom: '0%',
      left: 'center',
      textStyle: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 10,
      },
    },
    grid: {
      top: '18%',
      bottom: '15%',
      left: '0%',
      right: '0%',
    },
    colors: () => [],
  }
)
</script>

<template>
  <Card>
    <FirstTitle :title="title" />
    <div class="flex items-baseline justify-between gap-1 my-2">
      <div class="flex items-baseline gap-1">
        <span class="text-xl font-DIN-Medium font-bold text-[#00ffff]">{{
          total?.toLocaleString?.() ?? 0
        }}</span>
        <span class="text-xs text-white/70">{{ unit }}{{ quantifier }}</span>
      </div>
      <div class="flex items-center justify-between pt-3 gap-3">
        <span class="text-xs text-gray-300">较上一年</span>
        <div class="flex items-center gap-1">
          <Icon v-if="changeRate > 0" name="icon-shangsheng" color="text-green-400" :size="12" />
          <Icon v-else-if="changeRate < 0" name="icon-xiajiang" color="text-red-400" :size="12" />
          <span
            class="text-xs font-medium"
            :class="
              changeRate > 0 ? 'text-green-400' : changeRate < 0 ? 'text-red-400' : 'text-gray-400'
            "
          >
            {{
              changeRate === 0
                ? '无变化'
                : changeRate > 0
                ? `+${changeRate.toFixed(2)}%`
                : `${changeRate.toFixed(2)}%`
            }}
          </span>
        </div>
      </div>
    </div>
    <div class="mb-2">
      <ProportionBarChart
        :data="chartData"
        :height="chartHeight"
        :tooltip-title="tooltipTitle"
        :unit="unit"
        :quantifier="quantifier"
        :legend="legend"
        :grid="grid"
        :colors="colors"
      />
    </div>
  </Card>
</template>
