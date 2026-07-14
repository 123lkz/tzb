<script setup lang="ts">
import LineChart from '~/components/Echart/LineChart.vue'
const props = defineProps<{
  data: Array<{ name: string; jobCount: number; recruitCount: number }>
}>()
const options = computed(() => {
  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const d = props.data[params[0].dataIndex]
        return `<div><b>${d.name}</b></div>
          <div>岗位数量：<span style='color:#38bdf8'>${d.jobCount}</span></div>
          <div>招聘总人数：<span style='color:#00eaff'>${d.recruitCount}</span></div>`
      },
    },
    legend: {
      data: ['岗位数量', '招聘总人数'],
      top: 5,
      right: 10,
      textStyle: { color: '#fff' },
    },
    grid: {
      left: '3%',
      right: '3%',
      top: '17%',
      bottom: '0',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => {
        const match = d.name.match(/^([0-9]{4})-([0-9]{2})$/)
        return match ? match[2] : d.name
      }),
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
    series: [
      {
        name: '岗位数量',
        type: 'line',
        data: props.data.map(d => d.jobCount),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#38bdf8', width: 3 },
        itemStyle: { color: '#38bdf8' },
        areaStyle: { color: 'rgba(56,189,248,0.08)' },
      },
      {
        name: '招聘总人数',
        type: 'line',
        data: props.data.map(d => d.recruitCount),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#00eaff', width: 3 },
        itemStyle: { color: '#00eaff' },
        areaStyle: { color: 'rgba(0,234,255,0.08)' },
      },
    ],
  }
})
</script>
<template>
  <LineChart :options="options" />
</template>
