<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { formatLargeNumber } from '~/utils/num'

type BarDataItem = {
  year: string
  doubleHigh: number // 双高数量
  nonDoubleHigh: number // 非双高数量
}

const props = defineProps<{
  data: BarDataItem[]
  title?: string
  theme?: object
  colors?: {
    doubleHigh?: string
    nonDoubleHigh?: string
  }
  height?: string
  unit?: string
  quantifier?: string
  tooltipTitle?: string
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const defaultColors = {
  doubleHigh: '#91CC75',
  nonDoubleHigh: '#5370C6',
}

const getColors = () => ({
  ...defaultColors,
  ...props.colors,
})

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart || !props.data.length) return

  const colors = getColors()
  const years = props.data.map((item: BarDataItem) => item.year)
  const doubleHighData = props.data.map((item: BarDataItem) => item.doubleHigh)
  const nonDoubleHighData = props.data.map((item: BarDataItem) => item.nonDoubleHigh)
  const totalData = props.data.map((item: BarDataItem) => item.doubleHigh + item.nonDoubleHigh)

  // 计算最大值，向上取整到最近的10的倍数
  const maxTotal = Math.max(...totalData)
  const yMax = Math.ceil(maxTotal / 10) * 10

  const option: echarts.EChartsOption = {
    // title: 移除标题
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: (params: any) => {
        const dataIndex = params[0].dataIndex
        const dataItem = props.data[dataIndex]
        return `
          <div style="font-weight:bold;margin-bottom:5px;font-size:13px">${dataItem.year}${
          props.tooltipTitle
        }</div>
          <div style="display:flex;align-items:center;margin:3px 0;font-size:12px">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.doubleHigh
            };margin-right:5px"></span>
            双高: <span style="color: #666;font-weight:bold;margin-left:5px">${formatLargeNumber(
              dataItem.doubleHigh
            )}</span> 人
          </div>
          <div style="display:flex;align-items:center;margin:3px 0;font-size:12px">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.nonDoubleHigh
            };margin-right:5px"></span>
            非双高: <span style="color: #666;font-weight:bold;margin-left:5px">${formatLargeNumber(
              dataItem.nonDoubleHigh
            )}</span> 人
          </div>
          <div style="margin-top:5px;border-top:1px solid #eee;padding-top:5px;font-size:12px">
            总计: <span style="color: #666;font-weight:bold;margin-left:5px">${formatLargeNumber(
              dataItem.doubleHigh + dataItem.nonDoubleHigh
            )}</span> 人
          </div>
        `
      },
    },
    legend: {
      data: ['双高', '非双高'],
      right: 20,
      top: 10,
      textStyle: {
        color: 'rgba(255,255,255,0.9)',
        fontSize: 10,
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontWeight: 'normal',
        fontSize: 10,
        interval: 0,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255,255,255,0.6)',
        },
      },
      axisTick: {
        alignWithLabel: true,
      },
    },
    yAxis: {
      type: 'value',
      name: '单位:' + props.quantifier,
      min: 0,
      max: yMax,
      nameTextStyle: {
        color: 'rgba(255,255,255,0.6)',
        fontWeight: 'normal',
        padding: [0, 0, 0, 20],
        fontSize: 10,
      },
      axisLabel: {
        color: 'rgba(255,255,255,0.6)',
        fontWeight: 'normal',
        fontSize: 10,
        formatter: (value: number) => {
          return formatLargeNumber(value, 2)
        },
      },
      axisLine: {
        show: false,
        lineStyle: {
          color: 'rgba(255,255,255,0.6)',
        },
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: 'rgba(255,255,255,0.3)',
        },
      },
    },
    series: [
      {
        name: '双高',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: {
          color: colors.doubleHigh,
        },
        emphasis: {
          itemStyle: {
            color: echarts.color.lift(colors.doubleHigh as string, 0.2),
          },
        },
        data: doubleHighData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 8,
          textShadowColor: 'transparent',
          formatter: (params: any) => {
            return formatLargeNumber(params.value, 2)
          },
        },
      },
      {
        name: '非双高',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: {
          color: colors.nonDoubleHigh,
        },
        emphasis: {
          itemStyle: {
            color: echarts.color.lift(colors.nonDoubleHigh as string, 0.2),
          },
        },
        data: nonDoubleHighData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 9,
          textShadowColor: 'transparent',
          formatter: (params: any) => {
            return formatLargeNumber(params.value, 2)
          },
        },
      },
    ],
  }

  chart.setOption(option)
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

const handleResize = () => {
  chart?.resize()
}

watch(() => props.data, updateChart, { deep: true })
</script>

<template>
  <div ref="chartRef" class="w-full h-full" :style="{ height: props.height }" />
</template>
