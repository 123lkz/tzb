<script setup lang="ts">
import * as echarts from 'echarts'
import type { ECharts, EChartsOption, PieSeriesOption } from 'echarts'
import { formatLargeNumber } from '@/utils/num'

// 定义props类型
interface RoseDataItem {
  name: string
  value: number
  color?: string
  quantifier?: string
}

interface Props {
  data: RoseDataItem[]
  tooltipTitle?: string
  secondTooltipTitle?: string
  height?: string
  radius?: string | string[]
  center?: string | string[]
  quantifier?: string
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  tooltipTitle: '',
  secondTooltipTitle: '',
  height: '240px',
  radius: () => ['15%', '45%'],
  center: () => ['10%', '45%'],
  quantifier: '个',
})

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 销毁现有实例
  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return

  // 排序数据
  const sortedData = [...props.data].sort((a, b) => b.value - a.value)

  const option: EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#666666',
        fontSize: 12,
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: function (params: any) {
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px; font-size: 13px">${
            params.name
          }</div>
          <div style="margin-top: 8px; font-size: 12px;">
            <div style="color: #666; margin-bottom: 4px; font-weight: bold;">
              <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
                params.color
              };"></span>
              ${
                props.tooltipTitle
              }：<span style="color: #333;font-weight:bold;">${formatLargeNumber(
          params.value
        )}</span>${props.quantifier}
            </div>
          </div>
        `
      },
    },
    series: [
      {
        type: 'pie',
        radius: props.radius,
        center: props.center,
        roseType: 'area',
        itemStyle: {
          borderRadius: 8,
          borderWidth: 1,
          borderColor: '#fafafa',
        },
        label: {
          show: true,
          formatter: '{b}',
          color: '#fff',
          fontSize: 11,
          lineHeight: 14,
        },
        labelLine: {
          length: 10,
          length2: 15,
          smooth: true,
          lineStyle: {
            color: '#fff',
            width: 1.5,
          },
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
          label: {
            fontWeight: 'bold',
            fontSize: 14,
          },
        },
        data: sortedData,
      } as PieSeriesOption,
    ],
  }
  chartInstance.setOption(option)
}

// 监听窗口变化，重新调整图表大小
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

// 监听数据变化
watch(
  () => props.data,
  () => {
    updateChart()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.rose-chart-container {
  @apply w-full h-full;
  transition: all 0.3s ease;
}
</style>
<template>
  <div ref="chartRef" class="w-full h-full" :style="{ height: props.height }"></div>
</template>
