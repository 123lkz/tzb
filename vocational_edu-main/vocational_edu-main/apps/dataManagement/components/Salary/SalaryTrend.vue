<script lang="ts" setup>
import LineChart from '~/components/Echart/LineChart.vue'

const props = withDefaults(
  defineProps<{
    currentRegion: string
    data: Array<{ name: string; p25: number; median: number; p75: number }>
  }>(),
  {
    currentRegion: '全国',
  }
)

const lineChartOptions = computed(() => {
  const monthData = props.data

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const d = monthData[params[0].dataIndex]
        return `<div><b>${d.name}薪酬</b></div>
          <div>25分位：<span style='color:#38bdf8'>${d.p25}</span> 元</div>
          <div>中位数：<span style='color:#00eaff'>${d.median}</span> 元</div>
          <div>75分位：<span style='color:#f59e42'>${d.p75}</span> 元</div>`
      },
    },
    legend: {
      data: ['25分位', '中位数', '75分位'],
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
      data: monthData.map(d => {
        const match = d.name.match(/^(\d{4})-(\d{2})$/)
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
        name: '25分位',
        type: 'line',
        data: monthData.map(d => d.p25),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#38bdf8', width: 3 },
        itemStyle: { color: '#38bdf8' },
        areaStyle: { color: 'rgba(56,189,248,0.08)' },
      },
      {
        name: '中位数',
        type: 'line',
        data: monthData.map(d => d.median),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#00eaff', width: 3 },
        itemStyle: { color: '#00eaff' },
        areaStyle: { color: 'rgba(0,234,255,0.08)' },
      },
      {
        name: '75分位',
        type: 'line',
        data: monthData.map(d => d.p75),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: { color: '#f59e42', width: 3 },
        itemStyle: { color: '#f59e42' },
        areaStyle: { color: 'rgba(245,158,66,0.08)' },
      },
    ],
  }
})
</script>

<template>
  <div>
    <LineChart :options="lineChartOptions" />
  </div>
</template>
