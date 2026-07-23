<template>
  <div :ref="setRef" style="width:100%;height:100%;min-height:220px"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue"

const props = withDefaults(defineProps<{
  data: {name:string;value:number}[]
  title?: string
}>(), { title: "" })

const chartRef = ref<HTMLElement | null>(null)
let chart: any = null
function setRef(el: any) { chartRef.value = el }

const colors = ["#00ffff","#ff6b6b","#ffd93d","#6bcb77","#845ef7","#ff922b","#339af0","#f06595","#20c997","#ffe066"]

function render() {
  if (!chartRef.value) return
  import("echarts").then((echarts: any) => {
    if (chart) chart.dispose()
    chart = echarts.init(chartRef.value!)
    chart.setOption({
      tooltip: { trigger: "item", formatter: "{b}: {c} ({d}%)" },
      series: [{
        type: "pie", radius: ["45%","70%"], avoidLabelOverlap: true,
        label: { show: true, formatter: "{b}", fontSize: 11, color: "rgba(176,196,222,0.7)" },
        emphasis: { label: { show: true, fontSize: 14, fontWeight: "bold" } },
        labelLine: { lineStyle: { color: "rgba(0,255,255,0.2)" } },
        data: props.data.map((d,i) => ({ ...d, itemStyle: { color: colors[i % colors.length] } }))
      }]
    })
  })
}

watch(() => props.data, render, { deep: true })
onMounted(() => { render(); window.addEventListener("resize", () => chart?.resize()) })
onUnmounted(() => { chart?.dispose() })
</script>