<script lang="ts" setup>
import * as echarts from 'echarts'
import type { EChartsOption, ECharts } from 'echarts'
import { formatLargeNumber } from '~/utils/num'

interface PieDataItem {
  value: number
  name: string
}

interface Props {
  data: PieDataItem[]
  colors?: string[]
  radius?: [string, string]
  center?: [string, string]
  title?: string
  height?: string
  quantifier?: string
  tooltipTitle?: string
  valueName?: string
  legend?: {
    left?: string
    right?: string
    top?: string
    bottom?: string
    textStyle?: {
      color?: string
      fontSize?: number
    }
  }
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  colors: () => ['#5470C6', '#FB8351', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#9B60B4'],
  radius: () => ['50%', '80%'],
  center: () => ['28%', '50%'],
  title: '总数',
  height: '100%',
  quantifier: '个',
  tooltipTitle: '',
  valueName: '',
  legend: () => ({
    right: '2%',
    top: 'center',
    bottom: 'auto',
  }),
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return

  // 计算总数量
  const total = props.data.reduce((sum: number, item: PieDataItem) => sum + item.value, 0)

  const option: EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: '#ffffff',
      borderColor: '#e0e0e0',
      borderWidth: 1,
      textStyle: {
        color: '#666666',
        fontSize: 12,
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 6px;',
      formatter: (params: any) => {
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px;display: flex;align-items: center;gap: 1px;justify-content: center;">
          <span>${params.name}</span>
          <span style="color: #666; font-weight: normal;">${props.tooltipTitle}</span>
          </div>
          <div style="display: flex; align-items: center; margin: 4px 0;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
              params.color
            };"></span>
            <span style="color: #666;">${props.valueName || '数值'}: </span>
            <span style="color: #333; font-weight: bold;padding-left: 4px;">${params.value}${
          props.quantifier ? ' ' + props.quantifier : ''
        }</span>
          </div>
          <div style="color: #666; font-size: 11px;">
          <span style="display:inline-block;margin-right:4px;border-radius:50%;width:8px;height:8px;background-color:${
            params.color
          };"></span>
            <span style="color: #666;">占比: </span>
            <span style="color: #333; font-weight: bold;padding-left: 4px;">${
              params.percent
            }%</span>
          </div>
        `
      },
    },
    legend: {
      orient: 'vertical',
      textStyle: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 11,
        ...props.legend.textStyle,
      },
      ...props.legend,
    },
    color: props.colors,
    series: [
      {
        type: 'pie',
        radius: props.radius,
        center: props.center,
        avoidLabelOverlap: false,
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: (idx: number) => idx * 100,
        animationDuration: 1500,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(0,0,0,0.5)',
          borderWidth: 2,
        },
        label: {
          show: true,
          position: 'center',
          formatter: () => {
            return `{title|${props.title}}\n\n{value|${formatLargeNumber(total)}} {quantifier|${
              props.quantifier
            }}`
          },
          rich: {
            title: {
              fontSize: 12,
              color: 'rgba(255, 255, 255, 0.6)',
              fontWeight: 'normal',
            },
            value: {
              fontSize: 14,
              color: 'rgba(255, 255, 255, 0.8)',
              fontWeight: 'bold',
            },
            quantifier: {
              fontSize: 11,
              color: 'rgba(255, 255, 255, 0.6)',
              fontWeight: 'normal',
            },
          },
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
        labelLine: {
          show: false,
        },
        data: props.data,
      },
    ],
  }

  chartInstance.setOption(option)
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize, { passive: true })
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})

watch(
  () => props.data,
  () => {
    updateChart()
  },
  { deep: true }
)
</script>

<template>
  <div ref="chartRef" class="w-full h-full relative z-10" :style="{ height: props.height }"></div>
</template>
