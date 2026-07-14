<script lang="ts" setup>
import * as echarts from 'echarts'
import type { EChartsOption, ECharts } from 'echarts'

/**
 * 双轴柱状图+折线图组件
 *
 * 功能特性：
 * - 支持左右Y轴独立刻度计算（平均分成5段，显示整数）
 * - 支持X轴文字旋转（xAxisLabelRotate属性）
 * - 动态系列名称和图例（根据传入数据的values.name自动设置）
 * - 支持自动滚动和动画效果
 * - Y轴不显示轴线，保持简洁视觉效果
 *
 * 使用示例：
 * <LineBarDualAxisChart
 *   :data="chartData"
 *   :x-axis-label-rotate="45"
 *   left-unit="个"
 *   right-unit="人"
 *   left-color="#5470c6"
 *   right-color="#91cc75"
 * />
 */

// 定义数据结构
interface DataItem {
  name: string
  values: Array<{
    name: string
    value: number
  }>
}

// 定义组件属性
interface Props {
  data: DataItem[]
  leftUnit?: string
  leftQuantifier?: string
  rightUnit?: string
  rightQuantifier?: string
  title?: string
  leftColor?: string
  rightColor?: string
  isSmoothLine?: boolean
  tooltipTitle?: string
  height?: string
  isStatAll?: boolean
  grid?: any
  legend?: any
  xAxisLabelRotate?: number // X轴标签旋转角度，正值顺时针，负值逆时针
}

const props = withDefaults(defineProps<Props>(), {
  leftUnit: '',
  leftQuantifier: '',
  rightUnit: '',
  rightQuantifier: '',
  title: '数据趋势',
  leftColor: '#00ffff',
  rightColor: '#AAD8E8',
  isSmoothLine: true,
  height: '220px',
  tooltipTitle: '',
  isStatAll: true,
  grid: () => ({}),
  legend: () => ({}),
  xAxisLabelRotate: 0
})

// 图表引用
const chartRef = ref<HTMLElement>()
let chartInstance: ECharts | null = null
let animationTimer: NodeJS.Timeout | null = null
let scrollTimer: NodeJS.Timeout | null = null
let currentScrollIndex = 0

// 计算Y轴刻度
const calculateYAxis = (data: number[]): { min: number; max: number; interval: number } => {
  const maxValue = Math.max(...data)

  // 确保最小值为0，分成5段
  const min = 0
  const max = Math.ceil(maxValue * 1.1) // 向上取整并留出10%空间

  // 计算合适的间隔，确保显示整数且平均分成5段
  let interval = Math.ceil(max / 5)

  // 如果间隔太大，尝试找到更合适的整数间隔
  if (interval > max / 5) {
    // 尝试常见的整数间隔：1, 2, 5, 10, 20, 50, 100, 200, 500, 1000等
    const commonIntervals = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    for (const commonInterval of commonIntervals) {
      if (commonInterval >= max / 5 && commonInterval <= max / 3) {
        interval = commonInterval
        break
      }
    }
  }

  // 重新计算最大值，确保能被间隔整除且正好分成5段
  const adjustedMax = Math.ceil(max / interval) * interval
  // 确保最大值能被5整除
  const finalMax = Math.ceil(adjustedMax / 5) * 5

  return { min, max: finalMax, interval: finalMax / 5 }
}

// 获取当前显示的数据范围
const getCurrentDisplayData = () => {
  const { data } = props
  const totalItems = data.length

  if (totalItems <= 12) {
    // 如果总数不超过12个，显示全部
    return {
      startIndex: 0,
      endIndex: totalItems - 1,
      xAxisData: data.map((item) => item.name),
      leftData: data.map((item) => {
        const leftItem = item.values[0]
        return leftItem?.value || 0
      }),
      rightData: data.map((item) => {
        const rightItem = item.values[1]
        return rightItem?.value || 0
      })
    }
  }
  // 如果总数超过12个，显示当前滚动窗口的数据
  const endIndex = Math.min(currentScrollIndex + 14, totalItems - 1)
  const startIndex = Math.max(0, endIndex - 14)

  const displayData = data.slice(startIndex, endIndex + 1)

  return {
    startIndex,
    endIndex,
    xAxisData: displayData.map((item) => item.name),
    leftData: displayData.map((item) => {
      const leftItem = item.values[0]
      return leftItem?.value || 0
    }),
    rightData: displayData.map((item) => {
      const rightItem = item.values[1]
      return rightItem?.value || 0
    })
  }
}

// 获取动态的系列名称和图例数据
const getSeriesNames = () => {
  if (props.data.length === 0) return { leftName: '', rightName: '', legendData: [] }

  const firstItem = props.data[0]
  if (!firstItem || firstItem.values.length < 2) return { leftName: '', rightName: '', legendData: [] }

  const leftName = firstItem.values[0]?.name || ''
  const rightName = firstItem.values[1]?.name || ''

  return {
    leftName,
    rightName,
    legendData: [leftName, rightName]
  }
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 创建图表实例
  chartInstance = (echarts as any).init(chartRef.value)

  // 更新图表
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return

  const { leftUnit, rightUnit, leftQuantifier, rightQuantifier } = props
  const displayData = getCurrentDisplayData()

  // 创建处理后的显示文本数组
  const xAxisDisplayText = displayData.xAxisData.map((text) => {
    if (text.length <= 6) {
      return text
    }
    return text.substring(0, 6) + '...'
  })

  // 分别计算左右两侧Y轴刻度
  const leftYAxis = calculateYAxis(displayData.leftData)
  const rightYAxis = calculateYAxis(displayData.rightData)

  const option: EChartsOption = {
    backgroundColor: 'transparent',
    // 禁用滚轮缩放，避免 passive 警告
    dataZoom: [],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      },
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#333333',
        fontSize: 12
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        // 获取完整的X轴标签名称（不使用省略号）
        const axisValue = params[0].axisValue
        const fullAxisValue = displayData.xAxisData[params[0].dataIndex] || axisValue

        let result = `<div style="font-weight: bold; color: #333; margin-bottom: 8px;">${fullAxisValue}${
          props.tooltipTitle
        }${props.isStatAll ? '（全口径）' : '（应届大专生）'}</div>`

        params.forEach((param: any) => {
          const color = param.color
          const name = param.seriesName
          const value = param.value
          const seriesNames = getSeriesNames()

          if (param.seriesName === seriesNames.leftName) {
            result += `<div style="display: flex; align-items: center; margin: 8px 0;">`
            result += `<span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${props.leftColor};"></span>`
            result += `<span style="color: #666;">${name}: </span>`
            result += `<span style="color: #333; font-weight: bold;">${value}${leftUnit}</span>`
            result += `</div>`
          } else if (param.seriesName === seriesNames.rightName) {
            result += `<div style="display: flex; align-items: center; margin: 8px 0;">`
            result += `<span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${color};"></span>`
            result += `<span style="color: #666;">${name}: </span>`
            result += `<span style="color: #333; font-weight: bold;">${value}${rightUnit}</span>`
            result += `</div>`
          }
        })
        return result
      }
    },
    legend: {
      data: getSeriesNames().legendData,
      textStyle: {
        color: '#fff',
        fontSize: 12
      },
      top: '5%',
      left: 'center',
      itemWidth: 12,
      itemHeight: 12,
      ...props.legend
    },
    grid: {
      left: '5%%',
      right: '5%%',
      bottom: '5%',
      top: '20%',
      containLabel: true,
      ...props.grid
    },
    xAxis: [
      {
        type: 'category',
        data: xAxisDisplayText, // 使用处理后的显示文本
        axisPointer: {
          type: 'shadow'
        },
        axisLabel: {
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: 10,
          rotate: props.xAxisLabelRotate, // 支持文字旋转
          interval: 0, // 强制全部显示
          margin: 8,
          // 添加鼠标悬停提示
          rich: {
            // 可以在这里定义富文本样式
          }
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.3)',
            width: 1
          }
        },
        axisTick: {
          alignWithLabel: true,
          lineStyle: {
            color: '#333'
          }
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        min: leftYAxis.min,
        max: leftYAxis.max,
        interval: leftYAxis.interval,
        name: '单位:' + leftUnit + leftQuantifier,
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 11
        },
        axisLabel: {
          formatter: (value: number) => Math.round(value).toString(),
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 10,
          margin: 8
        },
        axisLine: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.2)',
            type: 'dashed',
            width: 1
          }
        }
      },
      {
        type: 'value',
        min: rightYAxis.min,
        max: rightYAxis.max,
        interval: rightYAxis.interval,
        name: '单位:' + rightUnit + rightQuantifier,
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 11
        },
        axisLabel: {
          formatter: (value: number) => Math.round(value).toString(),
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 10,
          margin: 8
        },
        axisLine: {
          show: false
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: getSeriesNames().leftName,
        type: 'bar',
        data: displayData.leftData,
        yAxisIndex: 0,
        barWidth: '40%', // 设置柱状图宽度
        itemStyle: {
          color: new (echarts as any).graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: props.leftColor + '66' },
            { offset: 1, color: props.leftColor }
          ]),
          borderRadius: [2, 2, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new (echarts as any).graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: props.leftColor + '44' },
              { offset: 1, color: props.leftColor }
            ])
          }
        },
        // 在柱状图上只显示数值
        label: {
          show: true,
          position: 'top',
          formatter: `{c}`,
          color: props.leftColor,
          fontSize: 10,
          distance: 5
        }
      },
      {
        name: getSeriesNames().rightName,
        type: 'line',
        data: displayData.rightData,
        yAxisIndex: 1,
        smooth: props.isSmoothLine,
        lineStyle: {
          color: props.rightColor,
          width: 2
        },
        itemStyle: {
          color: props.rightColor,
          borderWidth: 2,
          borderColor: '#fff'
        },
        symbol: 'circle',
        symbolSize: 6,
        // 在折线图上只显示数值
        label: {
          show: true,
          position: 'top',
          formatter: `{c}`,
          color: props.rightColor,
          fontSize: 10,
          distance: 5
        },
        animation: true,
        animationDuration: 2000,
        animationEasing: 'cubicOut'
      }
    ]
  }

  chartInstance.setOption(option)

  // 启动点依次高亮动画
  startPointHighlightAnimation()

  // 启动自动滚动
  startAutoScroll()
}

// 点依次高亮动画
const startPointHighlightAnimation = () => {
  const displayData = getCurrentDisplayData()
  if (!chartInstance || !displayData.rightData.length) return

  // 清除之前的定时器
  if (animationTimer) {
    clearInterval(animationTimer)
  }

  let currentIndex = 0
  const totalPoints = displayData.rightData.length

  // 设置定时器，每隔1秒高亮一个点
  animationTimer = setInterval(() => {
    // 高亮当前点
    chartInstance?.dispatchAction({
      type: 'highlight',
      seriesIndex: 1, // 折线图系列索引
      dataIndex: currentIndex
    })

    // 取消之前高亮的点
    if (currentIndex > 0) {
      chartInstance?.dispatchAction({
        type: 'downplay',
        seriesIndex: 1,
        dataIndex: currentIndex - 1
      })
    }

    currentIndex++

    // 循环播放
    if (currentIndex >= totalPoints) {
      currentIndex = 0
    }
  }, 1000)
}

// 自动滚动函数
const startAutoScroll = () => {
  const { data } = props
  const totalItems = data.length

  // 如果总数不超过12个，不需要滚动
  if (totalItems <= 12) return

  // 清除之前的滚动定时器
  if (scrollTimer) {
    clearInterval(scrollTimer)
  }

  // 设置滚动定时器，每隔2000毫秒滚动一次
  scrollTimer = setInterval(() => {
    currentScrollIndex++

    // 如果滚动到末尾，重新开始
    if (currentScrollIndex >= totalItems) {
      currentScrollIndex = 0
    }

    // 更新图表
    updateChart()
  }, 2000)
}

// 监听数据变化
watch(
  () => props.data,
  () => {
    if (chartInstance) {
      updateChart()
    }
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
  // 延迟初始化，确保容器尺寸稳定
  setTimeout(() => {
    initChart()
  }, 100)

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
  if (scrollTimer) {
    clearInterval(scrollTimer)
    scrollTimer = null
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
