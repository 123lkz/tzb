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
    data: {
      education: Array<{ name: string; value: number }>
      experience: Array<{ name: string; value: number }>
    }
    title: string
    height?: string
  }>(),
  {
    height: '240px',
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
    legend: { data: ['学历', '年限'], textStyle: { color: '#00eaff' } },
    grid: {
      left: 0,
      right: 8,
      bottom: 0,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: props.data.experience.map(d => d.name),
      axisLabel: { color: '#fff' },
    },
    yAxis: [
      { type: 'value', name: '学历', position: 'left', axisLabel: { color: '#00eaff' } },
      { type: 'value', name: '年限', position: 'right', axisLabel: { color: '#f59e42' } },
    ],
    series: [
      {
        name: '学历',
        type: 'bar',
        data: props.data.education.map(d => d.value),
        yAxisIndex: 0,
        itemStyle: { color: '#00eaff' },
      },
      {
        name: '年限',
        type: 'line',
        data: props.data.experience.map(d => d.value),
        yAxisIndex: 1,
        itemStyle: { color: '#f59e42' },
      },
    ],
  })
}
</script>
