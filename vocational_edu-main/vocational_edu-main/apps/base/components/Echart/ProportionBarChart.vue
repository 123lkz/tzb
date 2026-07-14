<script lang="ts" setup>
import * as echarts from 'echarts'

// 定义组件属性
interface Props {
  originalData?: {
    years: string[]
    primary: number[]
    secondary: number[]
    tertiary: number[]
  }
  data?: {
    years: string[]
    industries: {
      name: string
      data: number[]
    }[]
  }
  title?: string
  height?: string
  tooltipTitle?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '三大产业占比',
  height: '170px',
  tooltipTitle: '产值和比重',
})

// 图表引用
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

// 计算占比数据
const calculateProportionData = (data: {
  years: string[]
  industries: { name: string; data: number[] }[]
}) => {
  const { years, industries } = data
  const totalData: number[] = []

  // 计算每年的总和
  for (let i = 0; i < years.length; i++) {
    let sum = 0
    for (let j = 0; j < industries.length; j++) {
      sum += industries[j].data[i]
    }
    totalData.push(sum)
  }

  // 计算占比
  const proportionData = industries.map(industry => ({
    name: industry.name,
    data: industry.data.map((value, index) =>
      totalData[index] <= 0 ? 0 : (value / totalData[index]) * 100
    ),
  }))

  return proportionData
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return

  const chartData = props.data
  const proportionData = calculateProportionData(chartData)

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
        let result = `<div style="font-weight: bold; color: #333; margin-bottom: 8px;">${
          params[0].axisValue + props.tooltipTitle
        }</div>`

        // 使用真实的三大产业增加值数据（单位：亿元）
        const outputValues = {
          第一产业: props.originalData?.primary || [0, 0, 0, 0, 0],
          第二产业: props.originalData?.secondary || [0, 0, 0, 0, 0],
          第三产业: props.originalData?.tertiary || [0, 0, 0, 0, 0],
        }

        params.forEach((param: any) => {
          const color = param.color
          const name = param.seriesName
          const proportion = param.value.toFixed(1)
          const yearIndex = params[0].dataIndex
          const outputValue = outputValues[name] ? outputValues[name][yearIndex] : 0

          result += `<div style="display: flex; align-items: center; margin: 4px 0;">`
          result += `<span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${color};"></span>`
          result += `<span style="color: #666;">${name}: </span>`
          result += `<span style="color: #333; font-weight: bold;">${proportion}%</span>`
          result += `</div>`
          result += `<div style="color: #999; font-size: 11px; margin-left: 16px; margin-bottom: 4px;">产值: ${outputValue.toLocaleString()} 亿元</div>`
        })
        return result
      },
    },
    legend: {
      data: proportionData.map(item => item.name),
      textStyle: {
        color: '#fff',
        fontSize: 10,
      },
      top: '5%',
      right: '4%',
    },
    grid: {
      left: '4%',
      right: '4%',
      bottom: 0,
      top: '25%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: chartData.years,
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 10,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.5)',
        },
      },
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      interval: 20,
      axisLabel: {
        formatter: '{value}%',
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 10,
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)',
          type: 'dashed',
        },
      },
    },
    series: proportionData.map((item, index) => {
      const colors = ['#FAC857', '#5370C6', '#91CC75']

      return {
        name: item.name,
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: {
          color: colors[index],
          borderRadius: [2, 2, 0, 0],
        },
        label: {
          show: true,
          position: 'inside',
          formatter: (params: any) => params.value.toFixed(1) + '%',
          color: '#fff',
          fontSize: 9,
        },
        emphasis: {
          itemStyle: {
            color: colors[index],
          },
        },
        data: item.data,
      }
    }),
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
