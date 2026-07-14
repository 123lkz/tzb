<script lang="ts" setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { safeEchartsInit, addNoWheelZoomOption } from '~/utils/echartsUtils'

// 定义组件属性
interface Props {
  data: {
    xAxisValue: string[]
    yAxisValue: number[]
    changeRate: number[]
  }
  unit?: string
  title?: string
  barColor?: string
  lineColor?: string
  isSmoothLine?: boolean
  tooltipTitle?: string
  height?: string
  isStatAll?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  unit: '个',
  title: '数据趋势',
  barColor: '#00ffff',
  lineColor: '#AAD8E8',
  isSmoothLine: true,
  height: '220px',
  tooltipTitle: '',
  isStatAll: true,
})

// 图表引用
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null
let animationTimer: NodeJS.Timeout | null = null

// 格式化月份显示
const formatMonthLabels = (months: string[]): string[] => {
  return months.map((month, index) => {
    const [year, monthNum] = month.split('-')
    const currentYear = new Date().getFullYear()
    const previousYear = currentYear - 1

    // 如果是1月份且跨年，显示年份
    if (
      monthNum === '01' &&
      (year === currentYear.toString() || year === previousYear.toString())
    ) {
      return `${monthNum}\n\n${year}`
    }
    return monthNum
  })
}

// 格式化年月标题
const formatYearMonthTitle = (month: string): string => {
  const [year, monthNum] = month.split('-')
  return monthNum ? `${year}年${monthNum}月` : `${year}年`
}

// 计算Y轴左侧刻度（总数量）
const calculateLeftYAxis = (data: number[]): { min: number; max: number; interval: number } => {
  const maxValue = Math.max(...data)
  const maxWan = Math.ceil(maxValue / 10000) // 除以10000后向上取整

  // 确保最小值为0，分成6段
  const min = 0
  const max = maxWan
  const interval = Math.ceil(max / 6) // 向上取整确保覆盖最大值

  return { min, max, interval }
}

// 计算Y轴右侧刻度（变化率）
const calculateRightYAxis = (data: number[]): { min: number; max: number; interval: number } => {
  const maxValue = Math.max(...data)
  const minValue = Math.min(...data)

  // 向下取整最小值和向上取整最大值
  const min = Math.floor(minValue / 10) * 10
  const max = Math.ceil(maxValue / 10) * 10

  // 计算间隔，确保分成6段
  const range = max - min
  const interval = Math.ceil(range / 6)

  return { min, max, interval }
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 使用安全的初始化方法
  chartInstance = safeEchartsInit(chartRef.value)

  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return

  const { data, unit } = props

  // 计算除以10000后的数据
  const totalCountWan = data.yAxisValue.map((v: number) => Math.round((v / 10000) * 100) / 100)

  // 计算Y轴刻度
  const leftYAxis = calculateLeftYAxis(data.yAxisValue)
  const rightYAxis = calculateRightYAxis(data.changeRate)

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    // 禁用滚轮缩放，避免 passive 警告
    dataZoom: [],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999',
        },
      },
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#333333',
        fontSize: 12,
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        // 获取当前年份/月份数据
        const axisValue = params[0].axisValue
        const year = axisValue.split('-')[0]
        const month = axisValue.split('-')[1] || ''
        const yearMonthTitle = month ? `${year}年${month}月` : `${year}年`

        let result = `<div style="font-weight: bold; color: #333; margin-bottom: 8px;">${yearMonthTitle}${
          props.tooltipTitle
        }${props.isStatAll ? '（全口径）' : '（应届大专生）'}</div>`

        params.forEach((param: any) => {
          const color = param.color
          const name = param.seriesName
          const value = param.value

          if (param.seriesName === '总数量') {
            result += `<div style="display: flex; align-items: center; margin: 8px 0;">`
            result += `<span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${props.barColor};"></span>`
            result += `<span style="color: #666;">${name}: </span>`
            result += `<span style="color: #333; font-weight: bold;">${
              value.toFixed(2) + props.unit
            }</span>`
            result += `</div>`
          } else if (param.seriesName === '变化率') {
            const changeRate = value
            const changeColor = changeRate > 0 ? '#52c41a' : changeRate < 0 ? '#ff4d4f' : '#666'
            const changeSymbol = changeRate > 0 ? '+' : ''

            result += `<div style="display: flex; align-items: center; margin: 8px 0;">`
            result += `<span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${color};"></span>`
            result += `<span style="color: #666;">相比${
              month ? '上个月' : '去年同期'
            }的变化率: </span>`
            result += `<span style="color: ${changeColor}; font-weight: bold;">${changeSymbol}${changeRate}%</span>`
            result += `</div>`
          }
        })
        return result
      },
    },
    legend: {
      data: ['总数量', '变化率'],
      textStyle: {
        color: '#fff',
      },
      top: '10%',
      right: 0,
    },
    grid: {
      left: '1%',
      right: '2%',
      bottom: 0,
      top: '30%',
      containLabel: true,
    },
    xAxis: [
      {
        type: 'category',
        data: data.xAxisValue,
        axisPointer: {
          type: 'shadow',
        },
        axisLabel: {
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: 10,
          rotate: 45,
          interval: 0, // 强制全部显示
        },
        axisLine: {
          lineStyle: {
            color: '#333',
          },
        },
        axisTick: {
          alignWithLabel: true,
          lineStyle: {
            color: '#333',
          },
        },
      },
    ],
    yAxis: [
      {
        type: 'value',
        min: leftYAxis.min,
        max: leftYAxis.max,
        interval: leftYAxis.interval,
        axisLabel: {
          formatter: `{value}${unit}`,
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 9,
        },
        axisLine: {
          lineStyle: {
            color: '#333',
          },
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.2)',
            type: 'dashed',
            width: 1,
          },
        },
      },
      {
        type: 'value',
        min: rightYAxis.min,
        max: rightYAxis.max,
        interval: rightYAxis.interval,
        axisLabel: {
          formatter: '{value}%',
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 9,
        },
        axisLine: {
          lineStyle: {
            color: '#333',
          },
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.1)',
            type: 'dashed',
            width: 1,
          },
        },
      },
    ],
    series: [
      {
        name: '总数量',
        type: 'bar',
        data: totalCountWan, // 使用除以10000后的数据
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: props.barColor + '66' },
            { offset: 1, color: props.barColor },
          ]),
          borderRadius: [2, 2, 0, 0],
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: props.barColor + '44' },
              { offset: 1, color: props.barColor },
            ]),
          },
        },
      },
      {
        name: '变化率',
        type: 'line',
        yAxisIndex: 1,
        data: data.changeRate,
        smooth: props.isSmoothLine,
        lineStyle: {
          color: props.lineColor,
          width: 1,
        },
        itemStyle: {
          color: props.lineColor,
          borderWidth: 1,
          borderColor: '#fff',
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 1, color: props.lineColor + '4d' },
            { offset: 0, color: props.lineColor + '1a' },
          ]),
        },
        animation: true,
        animationDuration: 2000,
        animationEasing: 'cubicOut',
      },
    ],
  }

  chartInstance.setOption(option)

  // 启动点依次高亮动画
  startPointHighlightAnimation()
}

// 点依次高亮动画
const startPointHighlightAnimation = () => {
  if (!chartInstance || !props.data.changeRate.length) return

  // 清除之前的定时器
  if (animationTimer) {
    clearInterval(animationTimer)
  }

  let currentIndex = 0
  const totalPoints = props.data.changeRate.length

  // 设置定时器，每隔1秒高亮一个点
  animationTimer = setInterval(() => {
    // 高亮当前点
    chartInstance?.dispatchAction({
      type: 'highlight',
      seriesIndex: 1, // 折线图系列索引
      dataIndex: currentIndex,
    })

    // 取消之前高亮的点
    if (currentIndex > 0) {
      chartInstance?.dispatchAction({
        type: 'downplay',
        seriesIndex: 1,
        dataIndex: currentIndex - 1,
      })
    }

    currentIndex++

    // 循环播放
    if (currentIndex >= totalPoints) {
      currentIndex = 0
    }
  }, 1000)
}

// 监听数据变化
watch(
  () => props.data,
  () => {
    updateChart()
  },
  { deep: true }
)

// 监听窗口大小变化
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 组件挂载时初始化图表
onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (animationTimer) {
    clearInterval(animationTimer)
    animationTimer = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full" :style="{ height: props.height }"></div>
</template>

<style scoped>
/* 可以添加自定义样式 */
</style>
