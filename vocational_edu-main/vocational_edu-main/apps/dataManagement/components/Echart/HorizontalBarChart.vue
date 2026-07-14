<script setup lang="ts">
import * as echarts from 'echarts'
import { getShortProvinceName } from '~/utils/map'

interface Props {
  data: Array<{
    name: string
    value: number
    group?: number
    originalName?: string
    totalCompanies?: number
  }>
  itemStyle?: any
  emphasisStyle?: any
  height?: string | number
  unit?: string
  tooltipTitle?: string
  xAxisMin?: string | number
  xAxisMax?: string | number
  quantifier?: string
  isShowProvinceData?: boolean
  scrollStep?: number // 新增：每次滚动的条数
  scrollInterval?: number
  displayCount?: number
  barColors?: (() => string[]) | string[]
  grid?: Record<string, any>
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  height: '100%',
  unit: '',
  tooltipTitle: '',
  xAxisMin: undefined,
  xAxisMax: undefined,
  quantifier: '',
  isShowProvinceData: false,
  scrollStep: 1, // 默认每次滚动1条
  scrollInterval: 5000,
  displayCount: 10,
  grid: () => ({}),
  barColors: () => [],
  itemStyle: () => ({}),
  emphasisStyle: () => ({})
})

// 工具提示格式化函数
const formatterTooltip = (params: any) => {
  const data = params[0].data
  const fullName = data.originalName || data.name
  const tooltipTitle = props.tooltipTitle || '数据'

  return `
    <div style="font-size: 12px;">
      <div style="font-weight: bold; color: #333; margin-bottom: 8px; text-align: left;">${fullName}${tooltipTitle}</div>
      <div style="display: flex; align-items: center;">
        <span style="color: #666;">${props.tooltipTitle}排名: </span>
        <span style="color: #333; font-weight: bold; margin-left: 4px;">${data.group}</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span style="color: #666;">数值: </span>
        <span style="color: #333; font-weight: bold; margin-left: 4px;">${data.value.toLocaleString()}${props.unit}${
    props.quantifier
  }</span>
      </div>
    </div>
  `
}

const emit = defineEmits(['bar-hover', 'bar-mouseout', 'bar-scroll'])

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null
let timer: NodeJS.Timeout | null = null
let currentStartIndex = 0

// 处理柱状图 hover 事件
const handleBarHover = (params: any) => {
  if (params.componentType === 'series' && params.seriesType === 'bar') {
    const provinceName = params.data.originalName || params.data.name
    emit('bar-hover', provinceName)
    // 鼠标移入时暂停滚动
    pauseAutoScroll()
  }
}

// 暂停滚动
const pauseAutoScroll = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

// 恢复滚动
const resumeAutoScroll = (dataLength: number) => {
  if (props.data.length > props.displayCount) {
    startAutoScroll(dataLength)
  }
}

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    renderChart()
    window.addEventListener('resize', handleResize, { passive: true })

    // 监听鼠标点击和移动事件
    if (chart) {
      chart.on('mousemove', handleBarHover)
      chart.on('mouseout', () => {
        emit('bar-hover', '')
        emit('bar-mouseout')
        // 鼠标移开时恢复滚动
        if (props.data.length > props.displayCount) {
          resumeAutoScroll(props.data.length)
        }
      }) // 鼠标移开时取消高亮并恢复滚动
    }
  }
})

const handleResize = () => {
  chart?.resize()
}

const startAutoScroll = (dataLength: number) => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }

  // 设置滚动间隔，默认为2秒
  const interval = props.scrollInterval || 2000

  timer = setInterval(() => {
    // 确保滚动步数不超过数据长度
    const step = Math.min(props.scrollStep, dataLength)
    currentStartIndex = (currentStartIndex + step) % dataLength
    updateChartView(dataLength)
    emit('bar-scroll', currentStartIndex) // 滚动时emit当前起始index
  }, interval)
}

const updateChartView = (dataLength: number) => {
  if (!chart || dataLength <= props.displayCount) return

  // 计算当前显示的数据范围
  const actualDisplayCount = Math.min(props.displayCount, dataLength)
  const startPercent = (currentStartIndex / dataLength) * 100
  const endPercent = ((currentStartIndex + actualDisplayCount) / dataLength) * 450

  // 获取当前显示的数据
  const sortedData = [...props.data].sort((a, b) => b.value - a.value)
  const currentData = []

  for (let i = 0; i < actualDisplayCount; i++) {
    const index = (currentStartIndex + i) % dataLength
    const originalName = sortedData[index].name
    const displayName = originalName.length > 5 ? originalName.substring(0, 3) + '...' : originalName

    // 根据 unit 决定是否除以10000
    const value = props.unit === '万' ? sortedData[index].value / 10000 : sortedData[index].value

    currentData.push({
      ...sortedData[index],
      value,
      name: props.isShowProvinceData ? getShortProvinceName(originalName) : displayName,
      originalName
    })
  }

  chart.setOption({
    dataZoom: [
      {
        start: startPercent,
        end: endPercent
      }
    ],
    yAxis: {
      data: getCurrentYAxisData()
    },
    series: [
      {
        data: currentData
      }
    ]
  })
}

const getCurrentYAxisData = () => {
  const sortedData = [...props.data].sort((a, b) => b.value - a.value)
  const dataLength = sortedData.length
  const actualDisplayCount = Math.min(props.displayCount, dataLength)
  const displayData = []

  for (let i = 0; i < actualDisplayCount; i++) {
    const index = (currentStartIndex + i) % dataLength
    const originalName = sortedData[index].name

    if (props.isShowProvinceData) {
      displayData.push(getShortProvinceName(originalName))
    } else {
      displayData.push(originalName.length > 5 ? originalName.substring(0, 3) + '...' : originalName)
    }
  }

  return displayData
}

const renderChart = () => {
  if (!chart || !props.data.length) return

  const sortedData = [...props.data].sort((a, b) => b.value - a.value)
  const dataLength = sortedData.length

  // 准备扩展后的循环数据（原始数据 + 前10条数据）
  const extendedData = [...sortedData, ...sortedData.slice(0, props.displayCount)].map((item) => {
    const originalName = item.name
    const displayName = originalName.length > 5 ? originalName.substring(0, 3) + '...' : originalName
    return {
      ...item,
      name: props.isShowProvinceData ? getShortProvinceName(originalName) : displayName,
      originalName // 保存原始名称用于tooltip
    }
  })
  const totalLength = extendedData.length

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#666666',
        fontSize: 12
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: formatterTooltip
    },
    grid: {
      left: '3%',
      right: '15%',
      bottom: '0',
      top: '10%',
      containLabel: true,
      ...props.grid
    },
    xAxis: {
      type: 'value',
      name: `（单位：${props.unit}${props.quantifier}）`,
      nameLocation: 'end',
      min: props.xAxisMin,
      max: props.xAxisMax,
      nameTextStyle: {
        align: 'right',
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 8,
        padding: [0, 0, 0, 0] // 设置名称的边距
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 10,
        showMaxLabel: true,
        showMinLabel: true,
        rotate: 45, // 新增：x轴标签旋转45度
        formatter: function (value: number) {
          if (value < 0.01) {
            return value.toString()
          } else if (Number.isInteger(value)) {
            // 如果是整数（证书），不保留小数
            return value.toString()
          } else {
            // 如果是小数，保留两位小数
            return value.toFixed(2)
          }
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
          type: 'dashed'
        }
      }
    },
    yAxis: {
      type: 'category',
      data: getCurrentYAxisData(),
      inverse: true,
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 10
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    },
    series: [
      {
        type: 'bar',
        data: extendedData.map((item) => {
          // 根据 unit 决定是否除以10000
          const value = props.unit === '万' ? item.value / 10000 : item.value
          return {
            group: item.group,
            value,
            name: item.name,
            originalName: item.originalName // 保存原始名称用于tooltip
          }
        }),
        itemStyle: {
          color: new (echarts as any).graphic.LinearGradient(0, 0, 1, 0, [
            {
              offset: 0,
              // @ts-ignore
              color: Array.isArray(props.barColors)
                ? props.barColors[0]
                : typeof props.barColors === 'function'
                ? props.barColors()[0]
                : 'rgba(0, 255, 255, 0.8)'
            },
            {
              offset: 1,
              color: Array.isArray(props.barColors)
                ? props.barColors[1]
                : typeof props.barColors === 'function'
                ? props.barColors()[1]
                : 'rgba(0, 255, 255, 0.1)'
            }
          ]),
          borderRadius: [0, 4, 4, 0],
          shadowColor: 'rgba(58, 160, 255, 0.5)',
          shadowBlur: 8,
          ...props.itemStyle
        },
        label: {
          show: true,
          position: 'right',
          formatter: function (params: any) {
            const value = params.value

            if (value < 0.01) {
              return value.toString()
            } else if (Number.isInteger(value)) {
              // 如果是整数（证书），不保留小数
              return value.toString()
            } else {
              // 如果是小数，保留两位小数
              return value.toFixed(2)
            }
          },
          color: '#fff',
          fontSize: 10,
          distance: 5
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: 'rgba(0, 255, 255, 1)' },
              { offset: 1, color: 'rgba(0, 128, 255, 0.7)' }
            ]),
            borderRadius: [0, 4, 4, 0],
            shadowColor: 'rgba(0, 255, 255, 0.7)',
            shadowBlur: 12,
            ...props.emphasisStyle
          }
        }
      }
    ],
    // 添加dataZoom配置实现滚动效果
    dataZoom: [
      {
        type: 'inside',
        orient: 'vertical',
        yAxisIndex: 0,
        start: 0,
        end: (props.displayCount / totalLength) * 450,
        zoomLock: true, // 禁止缩放
        moveOnMouseMove: false, // 禁止鼠标拖动
        filterMode: 'filter'
      }
    ]
  }

  chart.setOption(option)

  // 当数据超过10条时启动自动滚动
  if (dataLength > props.displayCount) {
    startAutoScroll(dataLength)
  } else if (timer) {
    // 数据不足10条时清除定时器
    clearInterval(timer)
    timer = null
  }
}

watch(
  () => props.data,
  () => {
    currentStartIndex = 0 // 重置滚动位置
    renderChart()
    emit('bar-scroll', currentStartIndex) // 数据变化时emit一次
  },
  { deep: true }
)

watch(
  () => [props.scrollInterval, props.scrollStep],
  () => {
    if (props.data.length > props.displayCount) {
      startAutoScroll(props.data.length)
    }
  }
)

watch(
  () => [props.xAxisMin, props.xAxisMax],
  () => {
    renderChart()
  }
)

onBeforeUnmount(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  if (chart) {
    chart.off('mousemove', handleBarHover)
    chart.off('mouseout')
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full" :style="{ height: props.height }"></div>
</template>
