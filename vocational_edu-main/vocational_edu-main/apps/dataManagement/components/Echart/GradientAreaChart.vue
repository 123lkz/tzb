<script lang="ts" setup>
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { formatDate } from '~/utils/time'

interface Props {
  height?: string // 新增高度属性
  color?: string
  title?: string
  tooltipTitle?: string
  showXAxis?: boolean
  showYAxis?: boolean
  xAxisInterval?: number
  unit?: string
  quantifier?: string
  data: Array<{ name: string; value: number }>
  showLabel?: boolean
  showSymbol?: boolean
  showYAxisUnit?: boolean
  yAxisMin?: number
  yAxisMax?: number
  grid?: {
    top?: string
    bottom?: string
    left?: string
    right?: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  tooltipTitle: '',
  unit: '',
  quantifier: '',
  showYAxis: true,
  showXAxis: true,
  xAxisInterval: 2,
  data: () => [],
  height: '200px',
  color: () => '#80FFA5',
  showLabel: false,
  showSymbol: false,
  showYAxisUnit: false,
  yAxisMin: undefined,
  yAxisMax: undefined,
  grid: () => ({}),
})

const xAxisData = computed(() => {
  return props.data.map((item: { name: string }) => item.name)
})

const seriesData = computed(() => {
  return props.data.map((item: { value: number }) => item.value)
})

// 计算Y轴范围
const yAxisRange = computed(() => {
  if (seriesData.value.length === 0) return { min: 0, max: 100 }

  // 如果用户自定义了最小值和最大值，直接使用
  if (props.yAxisMin !== undefined && props.yAxisMax !== undefined) {
    return { min: props.yAxisMin, max: props.yAxisMax }
  }

  const min = Math.min(...seriesData.value)
  const max = Math.max(...seriesData.value)

  // 计算数据范围
  const range = max - min

  // 如果数据范围太小，设置最小范围
  const minRange = Math.max(range * 0.2, 1)

  // 向下取整最小值，向上取整最大值
  let yMin = Math.floor(min - minRange * 0.1)
  let yMax = Math.ceil(max + minRange * 0.1)

  // 如果用户只自定义了最小值
  if (props.yAxisMin !== undefined) {
    yMin = props.yAxisMin
  }

  // 如果用户只自定义了最大值
  if (props.yAxisMax !== undefined) {
    yMax = props.yAxisMax
  }

  return { min: yMin, max: yMax }
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return

  // Initialize chart
  chartInstance = echarts.init(chartRef.value)

  const options: EChartsOption = {
    color: props.color,
    grid: {
      top: 0,
      left: '8%',
      right: '8%',
      bottom: 0,
      containLabel: true,
      ...props.grid,
    },
    title: {
      text: props.title,
      show: !!props.title,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 1)',
      borderColor: 'rgba(0, 255, 255, 0.3)',
      borderWidth: 1,
      axisPointer: {
        type: 'line',
        lineStyle: {
          color: props.color,
          width: 1,
          type: 'dashed',
        },
      },
      formatter: function (params: any) {
        if (!Array.isArray(params)) return ''

        let result = `<div>
          <div class="text-xs font-semibold mb-1 text-gray-700">
            ${formatDate(params[0].axisValue)}${props.tooltipTitle}
          </div>`

        params.forEach(param => {
          const color = param.color || props.color || '#00ffff'
          result += `
            <div class="flex items-center mb-1 text-gray-400 text-xs text-gray-600">
              <span class="w-2 h-2 rounded-full" style="background-color: ${color}"></span>
              <span class="ml-1 -mr-1">
                总数量：
              </span>
              <span class="font-DIN-Medium" style="color: ${color}">
                ${param.value}${props.unit}
              </span>
              <span>
                ${props.quantifier}
              </span>
            </div>`
        })

        result += '</div>'
        return result
      },
    },
    legend: {
      show: false, // 单系列数据不需要显示图例
    },
    xAxis: {
      type: 'category',
      show: props.showXAxis,
      boundaryGap: false,
      data: xAxisData.value,
      axisTick: {
        show: false,
      },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 10,
        interval: props.xAxisInterval,
        rotate: 0,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255,255,255,0.3)',
        },
      },
    },
    yAxis: {
      type: 'value',
      show: props.showYAxis,
      min: yAxisRange.value.min,
      max: yAxisRange.value.max,
      name: props.showYAxisUnit ? '单位：' + props.unit + props.quantifier : '',
      nameTextStyle: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 10,
      },
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
      axisLabel: {
        show: props.showYAxis,
        color: 'rgba(255,255,255,0.6)',
        fontSize: 10,
      },
      splitLine: {
        show: props.showYAxis,
        lineStyle: {
          color: 'rgba(255,255,255,0.1)',
          type: 'dashed',
        },
      },
    },
    series: [
      {
        name: '',
        type: 'line',
        stack: 'Total',
        smooth: true,
        lineStyle: {
          width: 0,
        },
        showSymbol: props.showSymbol,
        symbol: 'circle',
        symbolSize: 6,
        itemStyle: {
          color: props.color,
          borderColor: '#fff',
          borderWidth: 2,
        },
        areaStyle: {
          opacity: 0.8,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: props.color,
            },
            {
              offset: 1,
              color: getDarkerColor(props.color),
            },
          ]),
        },
        emphasis: {
          focus: 'series',
        },
        label: {
          show: props.showLabel,
          position: 'top',
          color: props.color,
          fontSize: 10,
          formatter: function (params: any) {
            return params.value.toFixed(2)
          },
        },
        data: seriesData.value,
      },
    ],
  }

  chartInstance.setOption(options)
}

function getDarkerColor(hex: string): string {
  if (hex === '#FFBF00') return '#E03E4C'
  if (hex === '#80FFA5') return '#01BFEC'
  if (hex === '#00DDFF') return '#4D77FF'
  if (hex === '#37A2FF') return '#7415DB'
  if (hex === '#FF0087') return '#87009D'
  return hex
}

const resizeChart = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', resizeChart)
  }
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', resizeChart)
  }
  chartInstance?.dispose()
})

watch(
  () => [
    props.title,
    props.showYAxis,
    props.showXAxis,
    props.data,
    props.showYAxisUnit,
    props.yAxisMin,
    props.yAxisMax,
    yAxisRange.value,
  ],
  () => {
    initChart()
  },
  { deep: true }
)
</script>

<template>
  <div ref="chartRef" :style="{ height: height, width: '100%' }"></div>
</template>
