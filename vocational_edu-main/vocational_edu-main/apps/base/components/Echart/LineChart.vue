<template>
  <div class="h-full w-full rounded-lg shadow-md">
    <div ref="chartRef" class="w-full" :style="{ height: props.height }"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = withDefaults(
  defineProps<{
    options: echarts.EChartsCoreOption
    height?: string
  }>(),
  {
    height: '200px',
  }
)

const chartRef = ref()
let chart: echarts.ECharts | null = null
let resizeObserver: ResizeObserver | null = null

onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  destroyChart()
})

watch(
  () => props.options,
  () => {
    setOption()
  },
  { deep: true }
)

function initChart() {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  setOption()

  resizeObserver = new ResizeObserver(() => {
    chart && chart.resize()
  })
  resizeObserver.observe(chartRef.value)
}

function setOption() {
  if (!chart) return
  chart.setOption(props.options)
}

function destroyChart() {
  if (resizeObserver && chartRef.value) {
    resizeObserver.unobserve(chartRef.value)
  }
  if (chart) {
    chart.dispose()
    chart = null
  }
}
</script>
