<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import type { ECharts, PieSeriesOption } from 'echarts'
import * as echarts from 'echarts'
import { safeEchartsInit } from '~/utils/echartsUtils'

interface PieDataItem {
  value: number
  name: string
}

interface Props {
  title?: string
  height?: string
  data: PieDataItem[]
  radius?: string | number
  legendPosition?: 'left' | 'right' | 'top' | 'bottom'
  quantifier?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  height: '100%',
  radius: '50%',
  legendPosition: 'top',
  quantifier: '',
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return

  // 销毁之前的实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  // 初始化图表
  chartInstance = safeEchartsInit(chartRef.value)

  // 检查数据是否有效
  if (!props.data || props.data.length === 0) {
    console.warn('PieChart: No data provided')
    return
  }

  const options: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    title: {
      show: !!props.title,
      text: props.title,
      left: 'center',
      bottom: 0,
      textStyle: {
        color: 'rgba(255, 255, 255, 0.8)',
        fontSize: 13,
      },
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#333',
        fontSize: 12,
      },
    },
    legend: {
      orient:
        props.legendPosition === 'left' || props.legendPosition === 'right'
          ? 'vertical'
          : 'horizontal',
      left: props.legendPosition,
      data: props.data.map(item => item.name),
      textStyle: {
        color: 'rgba(255, 255, 255, 0.8)',
        fontSize: 12,
      },
    },
    series: [
      {
        name: '占比',
        type: 'pie',
        radius: props.radius,
        data: props.data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 255, 255, 0.5)',
          },
        },
        label: {
          show: true,
          formatter: function (params: any) {
            return `${params.name}\n${formatLargeNumber(params.value)}${props.quantifier}`
          },
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: 11,
          lineHeight: 14,
        },
        labelLine: {
          length: 10,
          length2: 10,
          smooth: true,
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.5)',
            width: 1,
          },
        },
        itemStyle: {
          borderColor: 'rgba(255, 255, 255, 0.2)',
          borderWidth: 1,
        },
        color: [
          '#9a60b4', // 紫色
          '#73c0de', // 浅蓝色
          '#ea7ccc', // 粉色
          '#ee6666', // 红色
          '#3ba272', // 深绿色
          '#fac858', // 黄色
          '#5470c6', // 深蓝色
          '#fc8452', // 橙色
        ],
      } as PieSeriesOption,
    ],
  }

  chartInstance.setOption(options)
}

const resizeChart = () => {
  chartInstance?.resize()
}

// 监听数据变化
watch(
  () => props.data,
  () => {
    initChart()
  },
  { deep: true }
)

onMounted(() => {
  // 延迟初始化，确保 DOM 完全渲染
  setTimeout(() => {
    initChart()
  }, 100)
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', resizeChart)
})
</script>

<template>
  <div ref="chartRef" class="w-full" :style="{ height: props.height }"></div>
</template>
