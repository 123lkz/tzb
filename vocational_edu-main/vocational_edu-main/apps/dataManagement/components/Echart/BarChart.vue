<template>
  <div class="h-full w-full rounded-lg p-4 shadow-md">
    <div ref="chartRef" class="w-full" :style="{ height: props.height }"></div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = withDefaults(
  defineProps<{
    data: Array<{ name: string; value: number }>
    height?: string
    unit?: string
  }>(),
  {
    height: '200px',
    unit: '',
  }
)

const chartRef = ref()
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

onMounted(() => {
  chart = echarts.init(chartRef.value)
  setOption()
  resizeObserver = new ResizeObserver(() => {
    chart && chart.resize()
  })
  if (chartRef.value) resizeObserver.observe(chartRef.value)
})
onBeforeUnmount(() => {
  if (resizeObserver && chartRef.value) resizeObserver.unobserve(chartRef.value)
  if (chart) chart.dispose()
})
watch(() => props.data, setOption, { deep: true })

function setOption() {
  if (!chart) return
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 0, right: 0, top: 6, bottom: 0, containLabel: true },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d.name),
      axisLabel: { color: '#fff' },
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
        type: 'bar',
        data: props.data.map(d => d.value),
        itemStyle: { color: '#00eaff' },
        barWidth: '40%',
      },
    ],
  })
}
</script>
