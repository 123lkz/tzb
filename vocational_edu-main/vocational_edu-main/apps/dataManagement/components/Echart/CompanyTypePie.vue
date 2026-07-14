<template>
  <div class="bg-white/5 border border-white/10 rounded-lg p-4 shadow-md">
    <div class="text-cyan-400 font-bold mb-2 text-center">单位性质分布</div>
    <div ref="chartRef" class="w-full h-64"></div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
const props = defineProps<{ data: Array<{ name: string; value: number }> }>()
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
watch(() => props.data, setOption)
function setOption() {
  if (!chart) return
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, textStyle: { color: '#00eaff' } },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '50%'],
        data: props.data,
        itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 1 },
      },
    ],
  })
}
</script>
