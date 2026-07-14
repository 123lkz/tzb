<script lang="ts" setup>
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { formatDate } from '~/utils/time'

interface DataItem {
  name: string // 如 "2025-04"
  values: Array<{
    name: string // 如 "25%分位数"
    value: number
  }>
}

interface ChartSeriesItem {
  name: string
  type: string
  data: number[]
}

interface ChartProps {
  width: string
  height?: string
  title?: string
  showLegend: boolean
  showYAxis: boolean
  showAllXAxisLabels: boolean
  useSmoothLine: boolean
  highlightXValue?: string
  data: DataItem[]
  colors: string[]
  legend?: any
  quantifier?: string
}

const props = withDefaults(defineProps<ChartProps>(), {
  width: '100%',
  height: 'auto',
  title: '',
  showLegend: true,
  showYAxis: true,
  showAllXAxisLabels: true,
  useSmoothLine: true,
  highlightXValue: '',
  colors: () => ['#00ffff', '#00ffff', '#00ffff', '#00ffff', '#00ffff'],
  data: () => [],
  legend: () => ({}),
  quantifier: '元',
})

const chartRef = ref<HTMLElement>()
const chartInstance = ref<ECharts>()
const resizeObserver = ref<ResizeObserver>()
let resizeTimer: NodeJS.Timeout | null = null

// 将服务端数据转换为 ECharts 需要的格式
const transformServerData = (serverData: DataItem[]) => {
  const xAxisData = serverData.map(item => item.name)
  const seriesMap: Record<string, ChartSeriesItem> = {}

  // 遍历服务端数据，构建系列
  serverData.forEach(item => {
    item.values.forEach(valueItem => {
      if (!seriesMap[valueItem.name]) {
        seriesMap[valueItem.name] = {
          name: valueItem.name,
          type: 'line',
          data: [],
        }
      }
      seriesMap[valueItem.name].data.push(valueItem.value)
    })
  })

  // 转换为数组形式
  const seriesData = Object.values(seriesMap)

  return {
    xAxisData,
    seriesData,
  }
}

// 处理后的图表数据
const chartData = computed(() => {
  return transformServerData(props.data)
})

// 初始化图表
const initChart = () => {
  if (!chartRef.value) {
    return
  }

  chartInstance.value = (echarts as any).init(chartRef.value)
  updateChart()
}

// 更新图表配置
const updateChart = () => {
  if (!chartInstance.value) {
    return
  }

  if (!chartData.value.xAxisData.length) {
    return
  }

  const { xAxisData, seriesData } = chartData.value

  const option: EChartsOption = {
    title: {
      text: props.title || '',
      show: !!props.title,
    },
    tooltip: {
      trigger: 'item',
      show: true,
      showContent: true,
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 0, 0, 0.1)',
      borderWidth: 1,
      textStyle: {
        color: '#333',
        fontSize: 12,
      },
      formatter: (params: any) => {
        // 获取同一 X 轴位置的所有数据
        const xAxisIndex = params.dataIndex
        const allSeriesData = seriesData.map((series, index) => ({
          name: series.name === '薪资中位数' ? series.name : '薪资' + series.name,
          value: series.data[xAxisIndex],
          color: props.colors[index],
          isMedian: series.name === '薪资中位数',
        }))

        const result = `
         <div style="font-weight: bold; color: #333; margin-bottom: 8px;">
           ${formatDate(params.name)}
         </div>
         ${allSeriesData
           .map(item => {
             const nameStyle = item.isMedian ? 'color: red; font-size: 13px;' : 'font-size: 12px;'
             const valueStyle = item.isMedian
               ? 'color: red; font-weight: bold; font-size: 13px;'
               : 'color: #333; font-weight: bold;'

             return `
             <div style="display: flex; align-items: center; gap: 4px; ${nameStyle}">
                 <span style="display: inline-block; width: 8px; height: 8px; background-color: ${item.color}; border-radius: 50%;"></span>
                 <span>${item.name}：</span>
                 <span style="${valueStyle}">${item.value}元</span>
             </div>
             `
           })
           .join('')}
         `
        return result
      },
    },
    legend: {
      data: seriesData.map(item => item.name),
      top: '2%',
      left: 'center',
      textStyle: {
        color: 'rgba(255,255,255,0.7)',
        fontSize: 9,
      },
      itemWidth: 8, // 缩小 legend 圆圈大小
      itemHeight: 8,
      ...props.legend,
    },
    grid: {
      top: '35%',
      left: '2%',
      right: '2%',
      bottom: '5%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xAxisData,
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontSize: 10,
      },
    },
    yAxis: {
      type: 'value',
      name: `（单位：${props.quantifier}）`, // 添加Y轴单位
      nameLocation: 'end', // 单位显示在Y轴末端
      nameTextStyle: {
        color: 'rgba(255,255,255,0.5)',
        fontSize: 10,
        padding: [0, 0, 0, 0],
      },
      min: (value: any) => {
        const min = Math.floor(value.min / 1000) * 1000
        return min > 0 ? min : 0
      },
      max: (value: any) => {
        const max = Math.ceil(value.max / 1000) * 1000
        return max + 1000
      },
      axisTick: {
        show: true, // Y轴刻度跟随showYAxis设置
        lineStyle: {
          color: 'rgba(255,255,255,0.2)',
          type: 'dashed',
          width: 1,
        },
      },
      axisLabel: {
        show: true, // Y轴标签跟随showYAxis设置
        color: 'rgba(255,255,255,0.5)',
        fontSize: 8,
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: 'rgba(255,255,255,0.2)',
          type: 'dashed',
          width: 1,
        },
      },
    },
    series: seriesData.map((item, index) => ({
      name: item.name,
      type: 'line' as const,
      data: item.data,
      smooth: props.useSmoothLine,
      symbol: 'emptyCircle', // 默认使用空心圆圈
      symbolSize: (_value: any, params: any) => {
        // 检查是否是高亮的月份
        if (props.highlightXValue && params.name === props.highlightXValue) {
          return 9 // 高亮月份使用更大的圆圈
        }
        return 5 // 其他月份使用正常大小
      },
      lineStyle: {
        width: 1,
        color: props.colors[index] || '#00ffff', // 使用动态颜色
      },
      itemStyle: {
        color: props.colors[index] || '#00ffff', // 设置数据点颜色
      },
      // 为第一个系列添加垂直标记线
      ...(index === 0 && props.highlightXValue
        ? {
            markLine: {
              silent: true,
              symbol: ['none', 'none'],
              lineStyle: {
                color: 'rgba(255,255,255,0.4)',
                type: 'dashed',
                width: 1,
              },
              data: [
                {
                  xAxis: props.highlightXValue,
                  label: {
                    show: true,
                    position: 'end',
                    formatter: '2025-03',
                    color: 'rgba(0,255,255,1)',
                    fontSize: 10,
                  },
                },
              ],
            },
          }
        : {}),
    })),
  }

  chartInstance.value.setOption(option)
}

// 监听数据变化
watch(
  () => props.data,
  () => {
    updateChart()
  },
  { deep: true }
)

// 监听高亮值变化
watch(
  () => props.highlightXValue,
  () => {
    updateChart()
  }
)

// 组件挂载时初始化图表
onMounted(() => {
  initChart()
  window.addEventListener('resize', debouncedResize)

  // 使用 ResizeObserver 监听容器大小变化
  if (chartRef.value) {
    resizeObserver.value = new ResizeObserver(() => {
      debouncedResize()
    })
    resizeObserver.value.observe(chartRef.value)
  }
})

// 防抖的 resize 处理函数
const debouncedResize = () => {
  if (resizeTimer) {
    clearTimeout(resizeTimer)
  }
  resizeTimer = setTimeout(() => {
    handleResize()
  }, 150)
}

// 处理窗口大小变化
const handleResize = () => {
  if (chartInstance.value) {
    // 先调整图表尺寸
    chartInstance.value.resize()
    // 然后重新渲染图表以确保正确显示
    updateChart()
  }
}

// 组件卸载时清理
onBeforeUnmount(() => {
  window.removeEventListener('resize', debouncedResize)
  resizeObserver.value?.disconnect()
  if (resizeTimer) {
    clearTimeout(resizeTimer)
  }
  chartInstance.value?.dispose()
})
</script>

<template>
  <div
    ref="chartRef"
    :style="{
      width: props.width,
      height: props.height === '100%' ? '100%' : props.height,
      flex: props.height === '100%' ? 1 : 'none',
      minHeight: props.height === '100%' ? 0 : 'auto',
    }"
  ></div>
</template>
