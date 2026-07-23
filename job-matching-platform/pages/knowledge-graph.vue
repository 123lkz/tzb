<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue"
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import Loading from "~/components/Common/Loading.vue"
import { fetchGraphData } from "~/utils/api"
import type { GraphNode } from "~/types"
const breadcrumbs=[{label:"首页",path:"/"},{label:"知识图谱",path:"/knowledge-graph"}]

const { data: graphData, pending } = await useAsyncData(() => fetchGraphData())
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: any = null
const selectedNode = ref<GraphNode | null>(null)

function renderGraph() {
  if (!chartRef.value || !graphData.value) return
  import("echarts").then((echarts: any) => {
    if (chartInstance) chartInstance.dispose()
    chartInstance = echarts.init(chartRef.value!)
    const categories = graphData.value!.categories
    const nodes = graphData.value!.nodes.map((n: any) => ({
      id: n.id, name: n.name, symbolSize: n.symbolSize, category: n.category,
      itemStyle: { borderColor: categories[n.category]?.itemStyle?.color || "#00ffff", borderWidth: 2, shadowBlur: 10, shadowColor: "rgba(0,255,255,0.3)" }
    }))
    const edges = graphData.value!.edges.map((e: any) => ({
      id: e.id, source: e.source, target: e.target,
      label: { show: true, formatter: e.label, fontSize: 10, color: "rgba(176,196,222,0.5)" },
      lineStyle: { color: "rgba(0,255,255,0.15)", width: Math.max(1, (e.weight||0.5)*3), curveness: 0.2 }
    }))
    chartInstance.setOption({
      backgroundColor: "transparent",
      legend: { data: categories.map((c: any) => c.name), textStyle: { color: "rgba(176,196,222,0.6)", fontSize: 12 }, bottom: 0 },
      series: [{
        type: "graph", layout: "force", roam: true, draggable: true, focusNodeAdjacency: true,
        force: { repulsion: 500, edgeLength: [100, 200] },
        data: nodes, edges, categories,
        label: { show: true, position: "bottom", color: "rgba(176,196,222,0.8)", fontSize: 11 },
        emphasis: { focus: "adjacency", lineStyle: { width: 2, color: "#00ffff" } }
      }]
    })
    chartInstance.on("click", (params: any) => {
      if (params.dataType === "node") {
        const node = graphData.value!.nodes.find((n: any) => n.id === params.data.id)
        if (node) selectedNode.value = node as GraphNode
      }
    })
  })
}

watch(graphData, (v) => { if (v) setTimeout(renderGraph, 100) })

let resizeObserver: ResizeObserver | null = null
onMounted(() => {
  if (chartRef.value) {
    resizeObserver = new ResizeObserver(() => chartInstance?.resize())
    resizeObserver.observe(chartRef.value)
  }
})
onUnmounted(() => { resizeObserver?.disconnect(); chartInstance?.dispose() })

const relatedNodes = computed(() => {
  if (!selectedNode.value || !graphData.value) return []
  const edges = graphData.value.edges.filter(e => e.source === selectedNode.value!.id || e.target === selectedNode.value!.id)
  const ids = new Set(edges.flatMap(e => [e.source, e.target]))
  return graphData.value.nodes.filter(n => ids.has(n.id) && n.id !== selectedNode.value!.id)
})
</script>
<template>
<div class="fade-in flex flex-col h-full">
<Header :breadcrumbs="breadcrumbs" />
<Loading v-if="pending" text="加载知识图谱..." />
<template v-else>
<div class="mb-3 px-4 py-2 rounded-lg bg-[rgba(255,217,61,0.05)] border border-[rgba(255,217,61,0.15)] flex items-center gap-2">
<span class="text-[#ffd93d] text-xs">&#9679;</span>
<span class="text-xs text-[rgba(176,196,222,0.6)]">
此页面为接口预留骨架。当前展示静态样例数据，后续需接入
<span class="text-[#00ffff]">Agent1</span> + <span class="text-[#00ffff]">Agent2</span>
产出到 Neo4j 的真实图谱数据。
</span></div>
<div class="flex gap-4 flex-1 overflow-hidden">
<div class="flex-1 relative"><div ref="chartRef" class="w-full h-full min-h-[68vh] rounded-lg border border-[rgba(0,255,255,0.08)]"></div></div>
<div class="w-72 flex-shrink-0 overflow-y-auto custom-scrollbar">
<Card v-if="selectedNode" class="!p-4 mb-3">
<div class="flex items-center justify-between mb-3"><h3 class="text-sm text-[#00ffff] font-semibold">{{selectedNode.name}}</h3>
<span class="text-[10px] px-1.5 py-0.5 rounded" :class="selectedNode.type==='position'?'bg-[rgba(0,255,255,0.15)] text-[#00ffff]':selectedNode.type==='skill'?'bg-[rgba(255,107,107,0.15)] text-[#ff6b6b]':'bg-[rgba(255,217,61,0.15)] text-[#ffd93d]'">{{selectedNode.type==='position'?'岗位':selectedNode.type==='skill'?'技能':'行业'}}</span></div>
<p v-if="selectedNode.description" class="text-xs text-[rgba(176,196,222,0.5)] mb-3">{{selectedNode.description}}</p>
<div v-if="relatedNodes.length" class="flex flex-wrap gap-1"><span v-for="rn in relatedNodes" :key="rn.id" class="px-1.5 py-0.5 text-[10px] rounded cursor-pointer bg-[rgba(0,255,255,0.08)] text-[rgba(0,255,255,0.6)] border border-[rgba(0,255,255,0.1)]" @click="selectedNode=rn">{{rn.name}}</span></div>
</Card>
<Card v-else class="!p-4 mb-3"><div class="text-center py-6"><svg class="w-10 h-10 mx-auto text-[rgba(0,255,255,0.15)] mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg><p class="text-xs text-[rgba(176,196,222,0.3)]">点击图谱中的节点查看详情</p></div></Card>
<Card class="!p-3"><h4 class="text-xs text-[rgba(176,196,222,0.5)] font-semibold mb-2">待接入接口</h4><div class="space-y-1.5 text-[10px]">
<div class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[rgba(255,217,61,0.5)]"></span><span class="text-[rgba(176,196,222,0.4)]">GET /api/graph/knowledge - 图谱数据</span></div>
<div class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[rgba(255,217,61,0.5)]"></span><span class="text-[rgba(176,196,222,0.4)]">GET /api/graph/node/:id - 节点详情</span></div>
<div class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[rgba(255,217,61,0.5)]"></span><span class="text-[rgba(176,196,222,0.4)]">GET /api/graph/evolution - 动态演化</span></div>
<div class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-[rgba(255,217,61,0.5)]"></span><span class="text-[rgba(176,196,222,0.4)]">数据来源: Agent1 + Agent2 i> Neo4j</span></div>
</div></Card>
</div></div></template></div></template>
