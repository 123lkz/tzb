<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import type { ECharts, EChartsOption, BarSeriesOption } from 'echarts'
import { safeEchartsInit } from '~/utils/echartsUtils'
import { formatLargeNumber } from '~/utils/num'

// 定义props类型
interface BarDataItem {
  name: string
  value: number
}

interface Props {
  data: BarDataItem[]
  title?: string
  subtext?: string
  zoomSize?: number
  height?: string
  barGradient?: {
    startColor: string
    endColor: string
  }
  tooltipTitle?: string
  showYAxis?: boolean
  showLabel?: boolean
  unit?: string
  quantifier?: string
  grid?: {
    top?: string
    bottom?: string
    left?: string
    right?: string
  }
  xAxisRotate?: number
  barWidth?: number | string
  labelStyle?: {
    fontSize?: number
    color?: string
    fontWeight?: string
    fontFamily?: string
  }
  // 新增属性
  textTruncation?: boolean
  showAllLabels?: boolean
  autoScroll?: boolean
  visibleBars?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '渐变柱状图',
  subtext: '支持点击缩放',
  zoomSize: 6,
  width: '100%',
  height: 'auto',
  barGradient: () => ({
    startColor: '#83bff6',
    endColor: '#188df0',
  }),
  tooltipTitle: '数据',
  showYAxis: true,
  showLabel: true,
  unit: '',
  quantifier: '',
  grid: () => ({
    top: '25%',
    bottom: '18%',
    left: '15%',
    right: '5%',
  }),
  xAxisRotate: 30,
  barWidth: '60%',
  labelStyle: () => ({
    fontSize: 9,
    color: 'rgba(255,255,255,0.6)',
    fontWeight: 'bold',
    fontFamily: 'inherit',
  }),
  // 新增默认值
  textTruncation: true,
  showAllLabels: false,
  autoScroll: false,
  visibleBars: 8,
})

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: ECharts | null = null
let scrollTimer: NodeJS.Timeout | null = null
const isHovered = ref(false)

// 文字截断函数
const truncateText = (text: string, maxLength: number = 5) => {
  if (!props.textTruncation || text.length <= maxLength) {
    return text
  }
  return text.substring(0, maxLength) + '...'
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 销毁现有实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  // 检查数据是否有效
  if (!props.data || props.data.length === 0) {
    console.warn('GradientBarChart: No data provided')
    return
  }

  try {
    chartInstance = safeEchartsInit(chartRef.value)
    updateChart()
    bindEvents()

    // 启动自动滚动
    if (props.autoScroll && !isHovered.value) {
      startAutoScroll()
    }
  } catch (error) {
    console.error('GradientBarChart: Failed to initialize chart', error)
  }
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return
  // 提取数据和标签
  const dataAxis = props.data.map(item => item.name)
  const data = props.data.map(item => item.value)

  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#666666',
        fontSize: 12,
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        const param = params[0]
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px;">${
            param.name + props.tooltipTitle
          }</div>
          <div style="display: flex; align-items: center; margin: 4px 0;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
              props.barGradient.startColor
            };"></span>
            <span style="color: #666;">数值: </span>
            <span style="color: #333; font-weight: bold;">${
              formatLargeNumber(param.value, 2) + props.quantifier
            }</span>
          </div>
        `
      },
    },
    xAxis: {
      data: dataAxis,
      axisLabel: {
        inside: false,
        color: 'rgba(255,255,255,0.6)',
        rotate: props.xAxisRotate,
        fontSize: 9,
        interval: props.showAllLabels ? 0 : 'auto',
        formatter: (value: string) => {
          return truncateText(value, 5)
        },
      },
      axisTick: {
        show: false,
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: '#fff',
        },
      },
      splitLine: {
        show: false,
      },
      z: 10,
    },
    yAxis: {
      show: props.showYAxis,
      name: '单位：' + props.unit + props.quantifier,
      nameTextStyle: {
        color: 'rgba(255,255,255,0.6)',
        fontWeight: 'normal',
        fontSize: 10,
      },
      nameLocation: 'end', // 让单位显示在Y轴右侧
      nameGap: 10, // 与轴线的距离，可根据实际调整
      nameRotate: 0, // 不旋转
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 8,
        formatter: (value: number) => {
          return formatLargeNumber(value)
        },
      },
      // splitNumber: 5, // 限制分割线数量为5条
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.15)',
          type: 'dashed',
          width: 1,
        },
      },
      // max: (value: any) => {
      //   // 确保最大值是合理的，避免出现9999999这样的异常值
      //   const maxDataValue = Math.max(...data)
      //   if (maxDataValue > 0) {
      //     return Math.ceil(maxDataValue * 1.2)
      //   }
      //   return 100 // 默认值
      // },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
    ],
    grid: props.grid,
    series: [
      {
        name: props.title,
        type: 'bar',
        barWidth: props.barWidth,
        showBackground: false,
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: props.barGradient.startColor },
              { offset: 1, color: props.barGradient.endColor },
            ],
          },
        },
        label: {
          show: props.showLabel,
          position: 'top',
          formatter: (params: any) => {
            return formatLargeNumber(params.value, 2)
          },
          color: props.labelStyle.color,
          fontSize: props.labelStyle.fontSize,
          fontWeight: props.labelStyle.fontWeight,
          fontFamily: props.labelStyle.fontFamily,
        },
        emphasis: {
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: props.barGradient.endColor },
                { offset: 1, color: props.barGradient.startColor },
              ],
            },
          },
        },
        data,
      } as BarSeriesOption,
    ],
  }

  chartInstance.setOption(option)
}

// 自动滚动功能
const startAutoScroll = () => {
  if (!props.autoScroll || isHovered.value || !chartInstance) return

  let currentStart = 0
  const step = 1
  const maxStart = Math.max(0, props.data.length - props.visibleBars)

  scrollTimer = setInterval(() => {
    if (isHovered.value) return

    currentStart = (currentStart + step) % (maxStart + 1)
    const end = Math.min(currentStart + props.visibleBars, props.data.length)

    chartInstance?.dispatchAction({
      type: 'dataZoom',
      startValue: props.data[currentStart]?.name,
      endValue: props.data[end - 1]?.name,
    })
  }, 2000) // 每2秒滚动一次
}

const stopAutoScroll = () => {
  if (scrollTimer) {
    clearInterval(scrollTimer)
    scrollTimer = null
  }
}

// 绑定事件
const bindEvents = () => {
  if (!chartInstance) return

  // 点击柱子缩放
  chartInstance.on('click', (params: any) => {
    if (params.componentType !== 'series' || params.seriesType !== 'bar') {
      return
    }

    const dataAxis = props.data.map(item => item.name)
    const startIdx = Math.max(params.dataIndex - props.zoomSize / 2, 0)
    const endIdx = Math.min(params.dataIndex + props.zoomSize / 2, dataAxis.length - 1)

    chartInstance?.dispatchAction({
      type: 'dataZoom',
      startValue: dataAxis[startIdx],
      endValue: dataAxis[endIdx],
    })
  })

  // 鼠标移入停止滚动
  chartInstance.on('mouseover', () => {
    isHovered.value = true
    if (props.autoScroll) {
      stopAutoScroll()
    }
  })

  // 鼠标移出恢复滚动
  chartInstance.on('mouseout', () => {
    isHovered.value = false
    if (props.autoScroll) {
      startAutoScroll()
    }
  })
}

// 监听窗口变化，重新调整图表大小
const handleResize = () => {
  chartInstance?.resize()
}

// 强制重新渲染图表
const forceRerender = () => {
  if (chartRef.value && props.data && props.data.length > 0) {
    initChart()
  }
}

// 暴露方法给父组件
defineExpose({
  forceRerender,
  resize: handleResize,
  startAutoScroll,
  stopAutoScroll,
})

onMounted(() => {
  // 延迟初始化，确保 DOM 完全渲染
  setTimeout(() => {
    // 只有在没有数据监听器触发初始化时才手动初始化
    if (!chartInstance && props.data && props.data.length > 0) {
      initChart()
    }
  }, 200)
  window.addEventListener('resize', handleResize, { passive: true })
})

// 监听数据变化
watch(
  () => props.data,
  newData => {
    if (newData && newData.length > 0) {
      // 如果图表实例存在，直接更新
      if (chartInstance) {
        updateChart()
      } else {
        // 如果图表实例不存在，重新初始化
        initChart()
      }
    }
  },
  { deep: true, immediate: true }
)

// 监听标签样式变化
watch(
  () => props.labelStyle,
  () => {
    updateChart()
  },
  { deep: true }
)

// 监听自动滚动属性变化
watch(
  () => props.autoScroll,
  newValue => {
    if (newValue && !isHovered.value) {
      startAutoScroll()
    } else {
      stopAutoScroll()
    }
  }
)

// 监听可见柱子数量变化
watch(
  () => props.visibleBars,
  () => {
    if (chartInstance) {
      updateChart()
    }
  }
)

onBeforeUnmount(() => {
  stopAutoScroll()
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div
    ref="chartRef"
    class="transition-all duration-300 ease-in-out"
    :style="{
      width: props.width,
      height: props.height === '100%' ? '100%' : props.height,
      flex: props.height === '100%' ? 1 : 'none',
      minHeight: props.height === '100%' ? 0 : 'auto',
    }"
  ></div>
</template>
