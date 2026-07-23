<template>
  <div :ref="setRef" style="width:100%;height:100%;min-height:220px"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue"

const props = withDefaults(defineProps<{
  data: {range:string;count:number}[]
  title?: string
}>(), { title: "" })

const chartRef = ref<HTMLElement | null>(null)
let chart: any = null
function setRef(el: any) { chartRef.value = el }

function render() {
  if (!chartRef.value) return
  import("echarts").then((echarts: any) => {
    if (chart) chart.dispose()
    chart = echarts.init(chartRef.value!)
    chart.setOption({
      tooltip: { trigger: "axis" },
      grid: { left: "3%", right: "4%", bottom: "3%", top: "8%", containLabel: true },
      xAxis: {
        type: "category",
        data: props.data.map(d => d.range),
        axisLabel: { color: "rgba(176,196,222,0.6)", fontSize: 11 },
        axisLine: { lineStyle: { color: "rgba(0,255,255,0.15)" } }
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "rgba(176,196,222,0.5)", fontSize: 10 },
        splitLine: { lineStyle: { color: "rgba(0,255,255,0.08)" } }
      },
      series: [{
        data: props.data.map(d => d.count),
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 8,
        lineStyle: { width: 3, color: "#ffd93d" },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(255,217,61,0.3)" },
            { offset: 1, color: "rgba(255,217,61,0.02)" }
          ])
        },
        itemStyle: { color: "#ffd93d" }
      }]
    })
  })
}

watch(() => props.data, render, { deep: true })
onMounted(() => { render(); window.addEventListener("resize", () => chart?.resize()) })
onUnmounted(() => { chart?.dispose() })
</script>