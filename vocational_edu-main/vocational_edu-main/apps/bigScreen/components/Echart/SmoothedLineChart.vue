<template>
  <div ref="chartContainer" class="line-chart-container" :style="{ height: height }">
    <div ref="chartRef" class="w-full h-full"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption, LineSeriesOption } from 'echarts'

// 定义props类型
interface LineDataItem {
  name: string
  total: number
  rate: number
}

interface Props {
  data: LineDataItem[]
  xAxisData?: string[]
  height?: string
  color?: string
  yAxisUnit?: string
  smooth?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  height: '100%',
  color: '#91cc75',
  yAxisUnit: '',
  smooth: true,
  areaStyle: true,
})

const chartRef = ref<HTMLDivElement | null>(null)
const chartContainer = ref<HTMLDivElement | null>(null)
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

  // 提取数据和标签
  const xAxisData = props.xAxisData || props.data.map((item: LineDataItem) => item.name)
  const totalData = props.data.map((item: LineDataItem) => item.total)
  const rateData = props.data.map((item: LineDataItem) => item.rate)

  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#666666',
        fontSize: 12,
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        const totalParam = params[0]
        const rateParam = params[1]
        const title = '数据趋势'
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px;">${title} - ${totalParam.name}</div>
          <div style="display: flex; align-items: center; margin: 4px 0;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${totalParam.color};"></span>
            <span style="color: #666;">总量: </span>
            <span style="color: #333; font-weight: bold;">${totalParam.value}${props.yAxisUnit}</span>
          </div>
          <div style="display: flex; align-items: center; margin: 4px 0;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${rateParam.color};"></span>
            <span style="color: #666;">变化率: </span>
            <span style="color: #333; font-weight: bold;">${rateParam.value}%</span>
          </div>
        `
      },
    },
    grid: {
      top: 10,
      right: 60,
      bottom: 10,
      left: 60,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: {
        color: '#71717a',
      },
      axisLine: {
        lineStyle: {
          color: '#d4d4d8',
          shadowColor: 'rgba(0, 0, 0, 0.1)',
          shadowBlur: 4,
          shadowOffsetX: 0,
          shadowOffsetY: 2,
        },
      },
      axisTick: {
        alignWithLabel: true,
      },
    },
    yAxis: [
      {
        type: 'value',
        name: `总量${props.yAxisUnit}`,
        nameTextStyle: {
          color: '#71717a',
          fontSize: 12,
        },
        axisLabel: {
          color: '#71717a',
          formatter: (value: number) => `${value}${props.yAxisUnit}`,
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: '#d4d4d8',
          },
        },
        axisTick: {
          show: false,
        },
        splitLine: {
          lineStyle: {
            color: '#e2e8f0',
            type: 'dashed',
          },
        },
      },
      {
        type: 'value',
        name: '变化率(%)',
        nameTextStyle: {
          color: '#71717a',
          fontSize: 12,
        },
        axisLabel: {
          color: '#71717a',
          formatter: (value: number) => `${value}%`,
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: '#d4d4d8',
          },
        },
        axisTick: {
          show: false,
        },
        splitLine: {
          show: false,
        },
      },
    ],
    series: [
      {
        name: '总量',
        type: 'line',
        yAxisIndex: 0,
        data: totalData,
        smooth: props.smooth,
        showSymbol: true,
        symbol: 'emptyCircle',
        symbolSize: 6,
        itemStyle: {
          color: props.color,
          borderColor: props.color,
          borderWidth: 1,
        },
        lineStyle: {
          width: 1.5,
          color: props.color,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: `${props.color}80` },
            { offset: 1, color: `${props.color}10` },
          ]),
        },
      } as LineSeriesOption,
      {
        name: '变化率',
        type: 'line',
        yAxisIndex: 1,
        data: rateData,
        smooth: props.smooth,
        showSymbol: true,
        symbol: 'emptyCircle',
        symbolSize: 6,
        itemStyle: {
          color: '#ff9f43',
          borderColor: '#ff9f43',
          borderWidth: 1,
        },
        lineStyle: {
          width: 1.5,
          color: '#ff9f43',
        },
      } as LineSeriesOption,
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
  () => [props.data, props.height, props.xAxisData],
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
.line-chart-container {
  @apply w-full;
}
</style>
