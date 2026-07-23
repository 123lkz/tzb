<template>
  <div :ref="setRef" style="width:100%;height:100%;min-height:250px"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue"

const props = withDefaults(defineProps<{
  data: {name:string;value:number}[]
  title?: string
  color?: string
}>(), {
  title: "",
  color: "#00ffff"
})

const chartRef = ref<HTMLElement | null>(null)
let chart: any = null

function setRef(el: any) { chartRef.value = el }

function render() {
  if (!chartRef.value) return
  import("echarts").then((echarts: any) => {
    if (chart) chart.dispose()
    chart = echarts.init(chartRef.value!)
    chart.setOption({
      tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
      grid: { left: "3%", right: "4%", bottom: "8%", top: "10%", containLabel: true },
      xAxis: {
        type: "category",
        data: props.data.map(d => d.name),
        axisLabel: { color: "rgba(176,196,222,0.6)", fontSize: 11 },
        axisLine: { lineStyle: { color: "rgba(0,255,255,0.15)" } },
        axisTick: { alignWithLabel: true }
      },
      yAxis: {
        type: "value",
        axisLabel: { color: "rgba(176,196,222,0.6)", fontSize: 11 },
        splitLine: { lineStyle: { color: "rgba(0,255,255,0.08)" } }
      },
      series: [{
        data: props.data,
        type: "bar",
        barWidth: "50%",
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: props.color },
            { offset: 1, color: "rgba(0,255,255,0.15)" }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        emphasis: { itemStyle: { color: "rgba(0,255,255,0.8)" } }
      }]
    })
  })
}

watch(() => props.data, render, { deep: true })
onMounted(() => { render(); window.addEventListener("resize", () => chart?.resize()) })
onUnmounted(() => { chart?.dispose() })
</script>