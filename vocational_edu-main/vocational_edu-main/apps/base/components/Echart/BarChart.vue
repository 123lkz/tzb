<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption, BarSeriesOption } from 'echarts'
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
  showLabel?: boolean
  unit?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '渐变柱状图',
  subtext: '支持点击缩放',
  zoomSize: 6,
  height: '240px',
  barGradient: {
    startColor: '#83bff6',
    endColor: '#188df0',
  },
  tooltipTitle: '数据',
  showLabel: false,
  unit: '',
})

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  // 销毁现有实例
  if (chartInstance) {
    chartInstance.dispose()
  }

  chartInstance = echarts.init(chartRef.value)
  updateChart()
  bindEvents()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return

  // 提取数据和标签
  const dataAxis = props.data.map(item => item.name)
  const data = props.data.map(item => item.value)
  const maxValue = Math.max(...data)
  const yMax = maxValue * 1.2 // 留出20%空间

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
              formatLargeNumber(param.value, 2) + props.unit
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
        rotate: dataAxis.length > 5 ? 30 : 0, // 标签旋转角度，防止重叠
        fontSize: 8,
        formatter: (value: string) => {
          if (value.length > 4) {
            return value.substring(0, 3) + '...'
          }
          return value
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
      z: 10,
    },
    yAxis: {
      name: '单位：' + props.unit,
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
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)',
          type: 'dashed',
        },
      },
      max: (value: any) => {
        // 确保最大值是合理的，避免出现9999999这样的异常值
        const maxDataValue = Math.max(...data)
        if (maxDataValue > 0) {
          return Math.ceil(maxDataValue * 1.2)
        }
        return 100 // 默认值
      },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
    ],
    grid: {
      top: '15%',
      bottom: 25,
      left: 55,
      right: 10,
    },
    series: [
      {
        name: props.title,
        type: 'bar',
        showBackground: false,
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: props.barGradient.startColor },
            { offset: 1, color: props.barGradient.endColor },
          ]),
        },
        label: {
          show: props.showLabel,
          position: 'top',
          formatter: (params: any) => {
            return formatLargeNumber(params.value, 2)
          },
          color: 'rgba(255,255,255,0.6)',
          fontSize: 9,
          fontWeight: 'bold',
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: props.barGradient.endColor },
              { offset: 1, color: props.barGradient.startColor },
            ]),
          },
        },
        data: data,
      } as BarSeriesOption,
    ],
  }

  chartInstance.setOption(option)
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
}

// 监听窗口变化，重新调整图表大小
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

// 监听数据变化
watch(
  () => props.data,
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
  <div
    ref="chartRef"
    class="w-full max-h-[240px] min-h-[120px] transition-all duration-300 ease-in-out"
    :style="{ height: props.height }"
  ></div>
</template>
