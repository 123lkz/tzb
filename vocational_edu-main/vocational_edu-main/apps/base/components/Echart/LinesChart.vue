<script setup lang="ts">
import LineChart from './LineChart.vue'

type LineSeries = {
  name: string
  dataKey: string
  color?: string
}

const props = defineProps<{
  data: Array<Record<string, any>>
  xKey?: string
  series: LineSeries[]
  legend?: boolean
}>()

const xKey = computed(() => props.xKey || 'name')

const options = computed(() => {
  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const d = props.data[params[0].dataIndex]
        let html = `<div><b>${d[xKey.value]}</b></div>`
        props.series.forEach((s, idx) => {
          const color = s.color || (params[idx] && params[idx].color) || '#38bdf8'
          html += `<div>${s.name}：<span style='color:${color}'>${d[s.dataKey]}</span></div>`
        })
        return html
      },
    },
    legend:
      props.legend !== false
        ? {
            data: props.series.map(s => s.name),
            top: 5,
            right: 10,
            textStyle: { color: '#fff' },
          }
        : undefined,
    grid: {
      left: '3%',
      right: '3%',
      top: '17%',
      bottom: '0',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d[xKey.value]),
      axisLabel: {
        color: '#fff',
        formatter: (v: string) => v,
      },
      axisLine: { lineStyle: { color: '#00eaff' } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#00eaff' },
      axisLine: { lineStyle: { color: '#00eaff' } },
      splitLine: { lineStyle: { color: 'rgba(0,234,255,0.1)' } },
    },
    series: props.series.map((s, idx) => ({
      name: s.name,
      type: 'line',
      data: props.data.map(d => d[s.dataKey]),
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: {
        color: s.color || ['#38bdf8', '#00eaff', '#facc15', '#ee6666'][idx % 4],
        width: 3,
      },
      itemStyle: { color: s.color || ['#38bdf8', '#00eaff', '#facc15', '#ee6666'][idx % 4] },
      areaStyle: {
        color: (s.color || ['#38bdf8', '#00eaff', '#facc15', '#ee6666'][idx % 4]) + '14',
      },
    })),
  }
})
</script>
<template>
  <LineChart :options="options" />
</template>
