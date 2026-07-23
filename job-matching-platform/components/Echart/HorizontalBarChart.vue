<template>
  <div :ref="setRef" style="width:100%;height:100%;min-height:220px"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue"

const props = withDefaults(defineProps<{
  data: {name:string;value:number}[]
  title?: string
  color?: string
}>(), { title: "", color: "#6bcb77" })

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
      grid: { left: "3%", right: "4%", bottom: "3%", top: "8%", containLabel: true },
      xAxis: {
        type: "value",
        axisLabel: { color: "rgba(176,196,222,0.5)", fontSize: 10 },
        splitLine: { lineStyle: { color: "rgba(0,255,255,0.08)" } }
      },
      yAxis: {
        type: "category",
        data: props.data.map(d => d.name).reverse(),
        axisLabel: { color: "rgba(176,196,222,0.7)", fontSize: 11 },
        axisLine: { lineStyle: { color: "rgba(0,255,255,0.15)" } }
      },
      series: [{
        data: props.data.map(d => d.value).reverse(),
        type: "bar",
        barWidth: "55%",
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: "rgba(107,203,119,0.15)" },
            { offset: 1, color: props.color }
          ]),
          borderRadius: [0, 4, 4, 0]
        }
      }]
    })
  })
}

watch(() => props.data, render, { deep: true })
onMounted(() => { render(); window.addEventListener("resize", () => chart?.resize()) })
onUnmounted(() => { chart?.dispose() })
</script>