<script setup lang="ts">
import * as echarts from 'echarts'
import { safeEchartsInit } from '~/utils/echartsUtils'

export interface DataItem {
  name: string
  value: number
}

interface Props {
  data?: DataItem[]
  xAxisData?: string[]
  seriesData?: number[]
  height?: string
  smooth?: boolean
  showSymbol?: boolean
  lineColor?: string
  areaColor?: string
  showArea?: boolean
  unit?: string
  grid?: any
  xAxis?: any
  yAxis?: any
  tooltip?: any
  customOptions?: echarts.EChartsCoreOption
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  xAxisData: () => [],
  seriesData: () => [],
  height: '200px',
  smooth: true,
  showSymbol: false,
  lineColor: '#73C0DE',
  areaColor: 'rgba(115, 192, 222, 0.1)',
  showArea: false,
  unit: '',
  grid: () => ({
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '5%',
    containLabel: true,
  }),
  xAxis: () => ({
    type: 'category',
    boundaryGap: false,
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.6)',
      fontSize: 10,
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(255, 255, 255, 0.3)',
      },
    },
    axisTick: {
      show: false,
    },
  }),
  yAxis: () => ({
    type: 'value',
    name: '单位',
    nameLocation: 'end',
    nameGap: 15,
    nameTextStyle: {
      color: 'rgba(255, 255, 255, 0.6)',
      fontSize: 10,
      align: 'right',
    },
    axisLabel: {
      color: 'rgba(255, 255, 255, 0.6)',
      fontSize: 10,
      formatter: '{value}',
      show: true,
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(255, 255, 255, 0.2)',
        type: 'dashed',
      },
    },
    axisLine: {
      show: true,
      lineStyle: {
        color: 'rgba(255, 255, 255, 0.3)',
      },
    },
    axisTick: {
      show: true,
      lineStyle: {
        color: 'rgba(255, 255, 255, 0.3)',
      },
    },
  }),
  tooltip: () => ({
    trigger: 'axis',
    backgroundColor: '#ffffff',
    borderColor: '#e0e0e0',
    borderWidth: 1,
    textStyle: {
      color: '#666666',
      fontSize: 12,
    },
    extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
  }),
  customOptions: () => ({}),
})

const chartRef = ref()
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

// 计算最终的options
const finalOptions = computed(() => {
  // 处理数据
  let xData: string[] = []
  let yData: number[] = []

  if (props.data && props.data.length > 0) {
    xData = props.data.map(item => item.name)
    yData = props.data.map(item => item.value)
  } else if (props.xAxisData && props.seriesData) {
    xData = props.xAxisData
    yData = props.seriesData
  }

  // 计算Y轴范围和区间
  const calculateYAxisRange = (data: number[]) => {
    if (data.length === 0) return { min: 0, max: 100, interval: 20 }

    const min = Math.min(...data)
    const max = Math.max(...data)

    // 计算合适的下限（向下取整到最近的整百/整千）
    const getLowerBound = (value: number) => {
      if (value <= 0) return 0
      const magnitude = Math.pow(10, Math.floor(Math.log10(value)))
      return Math.floor(value / magnitude) * magnitude
    }

    // 计算合适的上限（向上取整到最近的整百/整千）
    const getUpperBound = (value: number) => {
      const magnitude = Math.pow(10, Math.floor(Math.log10(value)))
      return Math.ceil(value / magnitude) * magnitude
    }

    const lowerBound = getLowerBound(min)
    const upperBound = getUpperBound(max)
    const range = upperBound - lowerBound

    // 动态计算区间
    const calculateInterval = (range: number) => {
      if (range <= 0) return 1

      // 根据范围大小选择合适的区间
      const magnitude = Math.pow(10, Math.floor(Math.log10(range)))
      const normalizedRange = range / magnitude

      if (normalizedRange <= 2) return magnitude / 5
      if (normalizedRange <= 5) return magnitude / 4
      if (normalizedRange <= 10) return magnitude / 2
      return magnitude
    }

    const interval = calculateInterval(range)

    return { min: lowerBound, max: upperBound, interval }
  }

  const yAxisRange = calculateYAxisRange(yData)

  const baseOptions: echarts.EChartsCoreOption = {
    backgroundColor: 'transparent',
    grid: props.grid,
    tooltip: props.tooltip,
    xAxis: {
      ...props.xAxis,
      data: xData,
    },
    yAxis: {
      ...props.yAxis,
      name: props.unit || '单位',
      min: yAxisRange.min,
      max: yAxisRange.max,
      interval: yAxisRange.interval,
    },
    series: [
      {
        data: yData,
        type: 'line',
        smooth: props.smooth,
        symbol: props.showSymbol ? 'circle' : 'none',
        symbolSize: 6,
        lineStyle: {
          color: props.lineColor,
          width: 2,
        },
        itemStyle: {
          color: props.lineColor,
        },
        areaStyle: props.showArea
          ? {
              color: props.areaColor,
            }
          : undefined,
      },
    ],
  }

  // 合并自定义options
  return {
    ...baseOptions,
    ...props.customOptions,
  }
})

onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  destroyChart()
})

watch(
  () => finalOptions.value,
  () => {
    setOption()
  },
  { deep: true }
)

function initChart() {
  if (!chartRef.value) return
  chart = safeEchartsInit(chartRef.value)
  setOption()

  resizeObserver = new ResizeObserver(() => {
    chart && chart.resize()
  })
  resizeObserver.observe(chartRef.value)
}

function setOption() {
  if (!chart) return
  chart.setOption(finalOptions.value)
}

function destroyChart() {
  if (resizeObserver && chartRef.value) {
    resizeObserver.unobserve(chartRef.value)
  }
  if (chart) {
    chart.dispose()
    chart = null
  }
}
</script>

<template>
  <div ref="chartRef" class="w-full" :style="{ height: props.height }"></div>
</template>
