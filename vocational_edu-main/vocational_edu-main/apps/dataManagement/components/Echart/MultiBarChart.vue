<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import type { ECharts, EChartsOption, BarSeriesOption } from 'echarts'
import { safeEchartsInit } from '~/utils/echartsUtils'
import { formatLargeNumber } from '~/utils/num'

// 定义数据结构类型
interface GroupDataItem {
  name: string // 分组名称（如"薪资中位数"）
  value: number // 分组值
}

interface BarDataItem {
  name: string // 主类别名称（如"2023年"）
  values: GroupDataItem[] // 该类别下的多组数据
}

interface Props {
  data: BarDataItem[]
  title?: string
  subtext?: string
  zoomSize?: number
  height?: string
  // 多组柱状图的颜色配置（支持纯色或渐变，长度应与分组数量一致）
  colors?: (string | { startColor: string; endColor: string })[]
  tooltipTitle?: string
  showYAxis?: boolean
  showLabel?: boolean
  quantifier?: string
  grid?: {
    top?: string
    bottom?: string
    left?: string
    right?: string
  }
  xAxisInterval?: number
  xAxisRotate?: number
  xAxisMaxLength?: number // x轴标签最大字符数，超过显示省略号
  barWidth?: number | string // 单组内柱子宽度
  barGap?: string // 同组内柱子间距
  barCategoryGap?: string // 不同组柱子间距
  labelStyle?: {
    fontSize?: number
    color?: string
    fontWeight?: string
    fontFamily?: string
  }
  showLegend?: boolean // 是否显示图例
  legendStyle?: any
}

// 默认配置
const props = withDefaults(defineProps<Props>(), {
  title: '多组柱状图',
  subtext: '支持多维度数据对比',
  zoomSize: 6,
  height: '300px',
  colors: () => [
    { startColor: '#72edc8', endColor: '#51dacf' },
    { startColor: '#fccd57', endColor: '#ffb627' },
    { startColor: '#83bff6', endColor: '#188df0' },
    { startColor: '#ff9a9e', endColor: '#fad0c4' }
  ],
  tooltipTitle: '数据统计',
  showYAxis: true,
  showLabel: true,
  quantifier: '',
  grid: () => ({
    top: '10%',
    bottom: '18%',
    left: '0%',
    right: '0%'
  }),
  xAxisInterval: 0,
  xAxisRotate: 0,
  xAxisMaxLength: 0, // 0表示不限制长度
  barWidth: '15%',
  barGap: '30%', // 同组内柱子间距
  barCategoryGap: '20%', // 不同组间距
  labelStyle: () => ({
    fontSize: 12,
    color: '#333',
    fontWeight: 'normal',
    fontFamily: 'inherit'
  }),
  showLegend: false,
  legendStyle: () => ({})
})

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 销毁现有实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  // 检查数据有效性
  if (!props.data || props.data.length === 0) {
    console.warn('MultiBarChart: 未提供有效数据')
    return
  }
  const firstItemValues = props.data[0].values
  if (!firstItemValues || firstItemValues.length === 0) {
    console.warn('MultiBarChart: 数据格式错误，缺少values字段')
    return
  }

  try {
    chartInstance = safeEchartsInit(chartRef.value)
    updateChart()
    bindEvents()
  } catch (error) {
    console.error('MultiBarChart: 初始化图表失败', error)
  }
}

// 更新图表配置
const updateChart = () => {
  if (!chartInstance) return

  // 提取基础数据
  const xAxisData = props.data.map((item) => item.name) // x轴类别（如年份）
  const groupNames = props.data[0].values.map((item) => item.name) // 分组名称（如各分位数）

  // 生成系列数据（每个分组一个series）
  const series: BarSeriesOption[] = groupNames.map((groupName, groupIndex) => {
    // 提取当前分组的所有数据
    const data = props.data.map((mainItem) => {
      const groupItem = mainItem.values.find((item) => item.name === groupName)
      return groupItem?.value || 0
    })

    // 处理颜色（支持纯色或渐变）
    const colorConfig = props.colors![groupIndex % props.colors!.length]
    let itemColor: any = '#ccc' // 默认颜色
    if (typeof colorConfig === 'string') {
      itemColor = colorConfig
    } else {
      itemColor = {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: colorConfig.startColor },
          { offset: 1, color: colorConfig.endColor }
        ]
      }
    }

    return {
      name: groupName,
      type: 'bar',
      barWidth: props.barWidth,
      data,
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: itemColor
      },
      label: {
        show: props.showLabel,
        position: 'top',
        formatter: (params: any) => formatLargeNumber(params.value, 2),
        color: props.labelStyle.color,
        fontSize: props.labelStyle.fontSize,
        fontWeight: props.labelStyle.fontWeight,
        fontFamily: props.labelStyle.fontFamily
      },
      emphasis: {
        itemStyle: {
          // 高亮时反转渐变
          color:
            typeof colorConfig === 'string'
              ? colorConfig
              : {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: colorConfig.endColor },
                    { offset: 1, color: colorConfig.startColor }
                  ]
                }
        }
      }
    }
  })

  // 图表配置项
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: { color: '#666666', fontSize: 12 },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        // 格式化多组数据的tooltip
        const mainName = params[0].name // 主类别名称（如"2023年"）
        let content = `<div style="font-weight: bold; color: #333; margin-bottom: 8px;">${mainName} ${props.tooltipTitle}</div>`

        params.forEach((param: any) => {
          content += `
            <div style="display: flex; align-items: center; margin: 4px 0;">
              <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
                param.color?.colorStops[0].color || param.color
              };"></span>
              <span style="color: #666;">${param.seriesName}: </span>
              <span style="color: #333; font-weight: bold;">${formatLargeNumber(param.value, 2)}${
            props.quantifier
          }</span>
            </div>
          `
        })
        return content
      }
    },
    legend: {
      show: props.showLegend,
      data: groupNames,
      textStyle: { color: 'rgba(255,255,255,0.7)', fontSize: 10 },
      top: '3%',
      left: 'center',
      itemWidth: 10,
      itemHeight: 10,
      orient: 'horizontal',
      icon: 'roundRect',
      ...props.legendStyle
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        rotate: props.xAxisRotate,
        fontSize: 10,
        interval: props.xAxisInterval,
        formatter: (value: string) => {
          // 如果设置了最大长度限制，则截断文字并添加省略号
          if (props.xAxisMaxLength && props.xAxisMaxLength > 0 && value.length > props.xAxisMaxLength) {
            return value.substring(0, props.xAxisMaxLength) + '...'
          }
          return value
        }
      },
      axisTick: { show: false },
      axisLine: {
        show: true,
        lineStyle: { color: 'rgba(255,255,255,0.5)' }
      },
      splitLine: { show: false }
    },
    yAxis: {
      show: props.showYAxis,
      name: '（单位：' + props.quantifier + '）',
      nameTextStyle: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 10,
        fontWeight: 'normal'
      },
      nameLocation: 'end',
      nameGap: 10,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 11,
        formatter: (value: number) => formatLargeNumber(value)
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255,255,255,0.2)',
          type: 'dashed',
          width: 1
        }
      }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      }
    ],
    grid: props.grid,
    series,
    barGap: props.barGap, // 同组内柱子间距
    barCategoryGap: props.barCategoryGap // 不同组间距
  }

  chartInstance.setOption(option)
}

// 绑定交互事件
const bindEvents = () => {
  if (!chartInstance) return

  // 点击柱子时缩放聚焦
  chartInstance.on('click', (params: any) => {
    if (params.componentType !== 'series' || params.seriesType !== 'bar') return

    const startIdx = Math.max(params.dataIndex - props.zoomSize / 2, 0)
    const endIdx = Math.min(params.dataIndex + props.zoomSize / 2, props.data.length - 1)

    chartInstance?.dispatchAction({
      type: 'dataZoom',
      startValue: props.data[startIdx].name,
      endValue: props.data[endIdx].name
    })
  })
}

// 窗口resize处理
const handleResize = () => {
  chartInstance?.resize()
}

// 暴露给父组件的方法
const forceRerender = () => {
  if (chartRef.value && props.data && props.data.length > 0) {
    initChart()
  }
}

defineExpose({
  forceRerender,
  resize: handleResize
})

// 生命周期
onMounted(() => {
  setTimeout(() => {
    if (!chartInstance && props.data && props.data.length > 0) {
      initChart()
    }
  }, 200)
  window.addEventListener('resize', handleResize, { passive: true })
})

// 监听数据变化
watch(
  () => props.data,
  (newData) => {
    if (newData && newData.length > 0 && newData[0].values.length > 0) {
      chartInstance ? updateChart() : initChart()
    }
  },
  { deep: true, immediate: true }
)

// 监听样式相关配置变化
watch(
  [() => props.labelStyle, () => props.colors, () => props.grid],
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

<template>
  <div ref="chartRef" class="w-full transition-all duration-300 ease-in-out" :style="{ height: props.height }"></div>
</template>
