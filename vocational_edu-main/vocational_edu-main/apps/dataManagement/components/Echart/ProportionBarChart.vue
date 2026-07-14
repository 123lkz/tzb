<script lang="ts" setup>
import * as echarts from 'echarts'
import { safeEchartsInit } from '~/utils/echartsUtils'

export interface DataItem {
  name: string
  values: {
    name: string
    value: number
  }[]
}

// 定义组件属性
interface Props {
  data: DataItem[]
  height?: string
  tooltipTitle?: string
  unit?: string
  quantifier?: string
  tooltipFormatter?: (params: any) => string
  legend?: any
  grid?: any
  colors?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  height: '150px',
  tooltipTitle: '数值和占比',
  unit: '',
  quantifier: '',
  colors: () => ['#FAC857', '#5370C6', '#91CC75', '#EE6666', '#73C0DE', '#3BA272', '#91CC75'],
  data: () => [],
  legend: () => ({
    textStyle: {
      color: 'rgba(255, 255, 255, 0.7)',
      fontSize: 10,
    },
    top: '0%',
    left: 'right',
  }),
  grid: () => ({
    left: '0%',
    right: '0%',
    bottom: 0,
    top: '25%',
    containLabel: true,
  }),
  tooltipFormatter: () => '',
})

// 图表引用
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const defaultTooltipFormatter = (params: any) => {
  // 计算除了透明总数值系列和百分比线之外的所有系列的value总和
  const totalValue = params
    .filter((param: any) => param.seriesName !== 'total' && param.seriesType !== 'line') // 排除透明总数值系列和百分比线
    .reduce((sum: number, param: any) => sum + (param.value || 0), 0)

  return `
    <div class="text-gray-700 text-xs font-bold mb-2">
    ${params[0].axisValue + props.tooltipTitle}
    </div>
    <div class="flex items-center text-gray-400 mb-2">
      <span class="w-2 h-2 bg-gray-500 rounded-full"></span>
      <span class="text-gray-600 text-xs ml-1 -mr-1">
      总数量：
      </span>
      <span class="text-gray-600 text-xs font-DIN-Medium">
        ${totalValue.toLocaleString()}${props.unit}
      </span>
      <span class="text-gray-600 text-xs">
        ${props.quantifier}
      </span>
    </div>
    ${params
      .filter((data: any) => data.seriesName !== 'total' && data.seriesType !== 'line')
      .map(
        (data: any) => `
        <div class="flex items-center text-gray-400 mb-2">
          <span class="w-2 h-2 bg-gray-500 rounded-full" style="background-color: ${
            data.color
          }"></span>
          <span class="text-gray-600 text-xs ml-1 -mr-1">
            ${data.seriesName}：
          </span>
          <span class="text-xs font-DIN-Medium" style="color: ${data.color}">
            ${data.value ?? 0}${props.unit}
          </span>
          <span class="text-gray-600 text-xs">
            ${props.quantifier}，占比
          </span>
          <span class="text-xs font-DIN-Medium ml-1" style="color: ${data.color}">
            ${((data.value ?? 0) / totalValue) * 100}%
          </span>
        </div>
      `
      )
      .join('')}
  `
}

// 计算数据
const calculateData = (dataArray: DataItem[]) => {
  const result = dataArray.map(dataItem => {
    const { name, values } = dataItem

    // 计算总和用于百分比
    const total = values.reduce((sum: number, item: { value: number }) => sum + item.value, 0)

    // 处理数据，包含原始值和百分比
    const processedData = values.map((item: { name: string; value: number }) => ({
      name: item.name,
      value: item.value,
      originalValue: item.value,
      percentage: total <= 0 ? 0 : (item.value / total) * 100,
    }))

    return {
      name,
      data: processedData,
      total,
    }
  })

  return result
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chartInstance = safeEchartsInit(chartRef.value as HTMLElement)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance || !props.data || props.data.length === 0) return

  const processedData = calculateData(props.data)

  // 获取所有唯一的类别名称
  const allCategories = new Set<string>()
  processedData.forEach(item => {
    item.data.forEach(cat => allCategories.add(cat.name))
  })
  const categories = Array.from(allCategories)

  // 获取所有年份/名称
  const years = processedData.map(item => item.name)

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
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
        if (props.tooltipFormatter(params)) {
          return props.tooltipFormatter(params)
        }
        return defaultTooltipFormatter(params)
      },
    },
    legend: {
      data: categories,
      ...props.legend,
    },
    grid: props.grid,
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 10,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)',
        },
      },
    },
    yAxis: [
      {
        type: 'value',
        position: 'left',
        name: '单位：' + props.unit + props.quantifier,
        nameLocation: 'end',
        nameGap: 15,
        nameTextStyle: {
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 10,
          align: 'left',
        },
        axisLabel: {
          color: 'rgba(255, 255, 255, 0.6)',
          fontSize: 10,
          formatter: '{value}',
        },
        splitLine: {
          show: processedData.some(item => item.total > 0), // 只有当有数据时才显示分割线
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.2)',
            type: 'dashed',
          },
        },
        axisTick: {
          show: false,
        },
        axisLine: {
          show: false,
        },
      },
      {
        type: 'value',
        min: 0,
        max: 100,
        position: 'right',
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
          formatter: '{value}%',
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLine: {
          show: false,
        },
      },
    ],
    series: [
      // 左侧Y轴的数据系列（柱状图）
      ...categories.map((category, index) => {
        return {
          name: category,
          type: 'bar' as const,
          yAxisIndex: 0, // 使用左侧Y轴
          stack: 'total',
          barWidth: '60%',
          itemStyle: {
            color: props.colors[index % props.colors.length],
            borderRadius: [2, 2, 0, 0],
          },
          label: {
            show: true,
            position: 'inside' as const,
            formatter: (params: any) => params.value.toLocaleString(),
            color: '#fff',
            fontSize: 9,
          },
          emphasis: {
            itemStyle: {
              color: props.colors[index % props.colors.length],
            },
          },
          data: processedData.map(yearData => {
            const categoryData = yearData.data.find(item => item.name === category)
            return categoryData
              ? {
                  value: categoryData.value,
                  originalValue: categoryData.originalValue,
                  percentage: categoryData.percentage,
                }
              : {
                  value: 0,
                  originalValue: 0,
                  percentage: 0,
                }
          }),
        }
      }),
      // 总数值标签系列
      {
        name: 'total',
        type: 'bar' as const,
        yAxisIndex: 0,
        stack: 'total',
        barWidth: '60%',
        itemStyle: {
          color: 'transparent',
        },
        label: {
          show: true,
          position: 'top' as const,
          formatter: (params: any) => {
            // 计算该位置的总和
            const yearIndex = params.dataIndex
            const yearData = processedData[yearIndex]
            const total = yearData ? yearData.total : 0
            return total > 0 ? total.toLocaleString() : ''
          },
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: 10,
        },
        data: processedData.map(yearData => ({
          value: 0, // 透明柱，只用于显示标签
          total: yearData.total,
        })),
      },
      // 右侧Y轴的数据系列（百分比线）
      {
        type: 'line' as const,
        yAxisIndex: 1, // 使用右侧Y轴
        symbol: 'none',
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)',
          width: 1,
        },
        data: processedData.map(yearData => {
          // 计算该年份所有类别的累计百分比
          let cumulativePercentage = 0
          yearData.data.forEach(item => {
            cumulativePercentage += item.percentage
          })
          return cumulativePercentage
        }),
      },
    ],
  }

  chartInstance.setOption(option)
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
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full" :style="{ height: props.height }"></div>
</template>
