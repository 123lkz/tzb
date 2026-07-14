<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { formatLargeNumber } from '~/utils/num'

type BarDataItem = {
  year: string
  doubleFirst: number // 双一流
  normalBachelor: number // 普通本科
  doubleHigh: number // 双高专科
  normalCollege: number // 普通专科
}

const props = defineProps<{
  data: BarDataItem[]
  title?: string
  theme?: object
  colors?: {
    doubleFirst?: string
    normalBachelor?: string
    doubleHigh?: string
    normalCollege?: string
  }
  height?: string
  unit?: string
  quantifier?: string
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const defaultColors = {
  doubleFirst: '#5470C6',
  normalBachelor: '#91CC75',
  doubleHigh: '#FAC858',
  normalCollege: '#EE6666',
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
  const doubleFirstData = props.data.map((item: BarDataItem) => item.doubleFirst)
  const normalBachelorData = props.data.map((item: BarDataItem) => item.normalBachelor)
  const doubleHighData = props.data.map((item: BarDataItem) => item.doubleHigh)
  const normalCollegeData = props.data.map((item: BarDataItem) => item.normalCollege)
  const totalData = props.data.map(
    (item: BarDataItem) =>
      item.doubleFirst + item.normalBachelor + item.doubleHigh + item.normalCollege
  )

  const yMax = Math.ceil(Math.max(...totalData) / 10) * 10

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const dataIndex = params[0].dataIndex
        const dataItem = props.data[dataIndex]
        return `
          <div style="font-weight:normal;margin-bottom:5px;color:rgba(255,255,255,0.9)">${
            dataItem.year
          }</div>
          <div style="display:flex;align-items:center;margin:3px 0">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.doubleFirst
            };margin-right:5px"></span>
            双一流: ${formatLargeNumber(dataItem.doubleFirst)} 人
          </div>
          <div style="display:flex;align-items:center;margin:3px 0">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.normalBachelor
            };margin-right:5px"></span>
            普通本科: ${formatLargeNumber(dataItem.normalBachelor)} 人
          </div>
          <div style="display:flex;align-items:center;margin:3px 0">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.doubleHigh
            };margin-right:5px"></span>
            双高专科: ${formatLargeNumber(dataItem.doubleHigh)} 人
          </div>
          <div style="display:flex;align-items:center;margin:3px 0">
            <span style="display:inline-block;width:10px;height:10px;background:${
              colors.normalCollege
            };margin-right:5px"></span>
            普通专科: ${formatLargeNumber(dataItem.normalCollege)} 人
          </div>
          <div style="margin-top:5px;border-top:1px solid #eee;padding-top:5px">
            总计: ${formatLargeNumber(
              dataItem.doubleFirst +
                dataItem.normalBachelor +
                dataItem.doubleHigh +
                dataItem.normalCollege
            )} 人
          </div>
        `
      },
    },
    legend: {
      data: ['双一流', '普通本科', '双高专科', '普通专科'],
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
      name: '单位:' + (props.quantifier || ''),
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
        name: '双一流',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: { color: colors.doubleFirst },
        emphasis: {
          itemStyle: { color: echarts.color.lift(colors.doubleFirst as string, 0.2) },
        },
        data: doubleFirstData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 8,
          textShadowColor: 'transparent',
          formatter: (params: any) => formatLargeNumber(params.value, 2),
        },
      },
      {
        name: '普通本科',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: { color: colors.normalBachelor },
        emphasis: {
          itemStyle: { color: echarts.color.lift(colors.normalBachelor as string, 0.2) },
        },
        data: normalBachelorData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 8,
          textShadowColor: 'transparent',
          formatter: (params: any) => formatLargeNumber(params.value, 2),
        },
      },
      {
        name: '双高专科',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: { color: colors.doubleHigh },
        emphasis: {
          itemStyle: { color: echarts.color.lift(colors.doubleHigh as string, 0.2) },
        },
        data: doubleHighData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 8,
          textShadowColor: 'transparent',
          formatter: (params: any) => formatLargeNumber(params.value, 2),
        },
      },
      {
        name: '普通专科',
        type: 'bar',
        stack: 'total',
        barWidth: '60%',
        itemStyle: { color: colors.normalCollege },
        emphasis: {
          itemStyle: { color: echarts.color.lift(colors.normalCollege as string, 0.2) },
        },
        data: normalCollegeData,
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.8)',
          fontWeight: 'normal',
          fontSize: 8,
          textShadowColor: 'transparent',
          formatter: (params: any) => formatLargeNumber(params.value, 2),
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
