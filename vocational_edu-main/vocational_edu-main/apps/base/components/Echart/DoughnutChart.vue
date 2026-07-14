<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
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
  title?: string
  height?: string
  unit?: string
  tooltipTitle?: string
}

const props = withDefaults(defineProps<Props>(), {
  colors: () => ['#5470C6', '#FB8351', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#9B60B4'],
  radius: () => ['50%', '80%'],
  title: '总数',
  height: '100%',
  tooltipTitle: '',
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null
let tooltipTimer: ReturnType<typeof setInterval> | null = null
let currentIndex = 0

function addChartMouseEvents() {
  if (!chartInstance) return
  chartInstance.off('mouseover')
  chartInstance.off('mouseout')
  chartInstance.on('mouseover', params => {
    if (params.componentType === 'series' && params.seriesType === 'pie') {
      stopTooltipLoop()
      // 高亮当前
      chartInstance?.dispatchAction({
        type: 'highlight',
        seriesIndex: params.seriesIndex,
        dataIndex: params.dataIndex,
      })
      // 显示tooltip
      chartInstance?.dispatchAction({
        type: 'showTip',
        seriesIndex: params.seriesIndex,
        dataIndex: params.dataIndex,
      })
    }
  })
  chartInstance.on('mouseout', params => {
    if (params.componentType === 'series' && params.seriesType === 'pie') {
      startTooltipLoop()
    }
  })
}

const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  updateChart()
  addChartMouseEvents()
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
      position: function (point, params, dom, rect, size) {
        // point: 鼠标位置 [x, y]
        // size: { contentSize, viewSize }
        const [x, y] = point
        const [contentWidth, contentHeight] = size.contentSize
        const [viewWidth, viewHeight] = size.viewSize
        let posX = x + 20
        let posY = y
        if (x + contentWidth + 30 > viewWidth) {
          posX = x - contentWidth - 20
        }
        if (posY + contentHeight > viewHeight) {
          posY = viewHeight - contentHeight - 10
        }
        if (posY < 0) posY = 10
        return [posX, posY]
      },
      formatter: (params: any) => {
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px;display: flex;align-items: center;gap: 2px;justify-content: center;">
          <span>${params.name}</span>
          <span style="color: #666; font-weight: normal;">${props.tooltipTitle}</span>
          </div>
          <div style="display: flex; align-items: center; margin: 4px 0;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
              params.color
            };"></span>
            <span style="color: #666;">数值: </span>
            <span style="color: #333; font-weight: bold;padding-left: 4px;">${params.value}${
          props.unit ? ' ' + props.unit : ''
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
      right: '5%',
      top: 'center',
      bottom: 'auto',
      orient: 'vertical',
      textStyle: {
        color: 'rgba(255, 255, 255, 0.6)',
        fontSize: 11,
      },
    },
    color: props.colors,
    series: [
      {
        type: 'pie',
        radius: props.radius,
        center: ['25%', '55%'],
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
            return `{title|${props.title}}\n\n{value|${formatLargeNumber(total)}} {unit|${
              props.unit
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
            unit: {
              fontSize: 11,
              color: 'rgba(255, 255, 255, 0.6)',
              fontWeight: 'normal',
            },
          },
          fontSize: 16,
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
  addChartMouseEvents()
}

function startTooltipLoop() {
  stopTooltipLoop()
  if (!chartInstance || !props.data.length) return
  currentIndex = 0
  tooltipTimer = setInterval(() => {
    if (!chartInstance) return
    // 取消之前的高亮
    chartInstance.dispatchAction({
      type: 'downplay',
      seriesIndex: 0,
      dataIndex: (currentIndex - 1 + props.data.length) % props.data.length,
    })
    // 高亮当前
    chartInstance.dispatchAction({
      type: 'highlight',
      seriesIndex: 0,
      dataIndex: currentIndex,
    })
    // 显示tooltip
    chartInstance.dispatchAction({
      type: 'showTip',
      seriesIndex: 0,
      dataIndex: currentIndex,
    })
    currentIndex = (currentIndex + 1) % props.data.length
  }, 2000) // 每2秒切换一次
}

function stopTooltipLoop() {
  if (tooltipTimer) {
    clearInterval(tooltipTimer)
    tooltipTimer = null
  }
  if (chartInstance) {
    chartInstance.dispatchAction({
      type: 'downplay',
      seriesIndex: 0,
    })
    chartInstance.dispatchAction({
      type: 'hideTip',
      seriesIndex: 0,
    })
  }
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  startTooltipLoop()
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
  stopTooltipLoop()
})

watch(
  () => props.data,
  () => {
    updateChart()
    startTooltipLoop()
  },
  { deep: true }
)
</script>

<template>
  <div ref="chartRef" class="w-full h-full relative z-10" :style="{ height: props.height }"></div>
</template>
