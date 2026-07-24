<script setup lang="ts">
const route=useRoute()
const items=[{l:"首页总览",p:"/",i:"M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"},{l:"岗位信息",p:"/positions",i:"M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"},{l:"简历匹配",p:"/matching",i:"M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"},{l:"能力洞察",p:"/insights",i:"M13 10V3L4 14h7v7l9-11h-7z"},{l:"知识图谱",p:"/knowledge-graph",i:"M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"}]
function active(p:string){return p==="/"?route.path==="/":route.path.startsWith(p)}
</script>
<template>
<aside class="w-56 flex-shrink-0 h-full bg-[#0d0117] border-r border-[rgba(0,255,255,0.1)] flex flex-col">
<div class="h-16 flex items-center justify-center gap-2 border-b border-[rgba(0,255,255,0.1)]"><img src="/logo-icon.png" class="h-8 w-auto"/><img src="/logo-text.png" class="h-6 w-auto"/></div>
<nav class="flex-1 py-4 overflow-y-auto custom-scrollbar">
<NuxtLink v-for="it in items" :key="it.p" :to="it.p" class="flex items-center gap-3 px-6 py-3 mx-2 rounded-lg transition-all duration-300 text-sm" :class="active(it.p)?'bg-[rgba(0,255,255,0.15)] text-[#00ffff]':'text-[rgba(176,196,222,0.6)] hover:text-[#00ffff] hover:bg-[rgba(0,255,255,0.05)]'">
<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path :d="it.i" stroke-linecap="round" stroke-linejoin="round"/></svg>
<span>{{it.l}}</span></NuxtLink></nav>
<div class="py-3 text-center border-t border-[rgba(0,255,255,0.1)]"><p class="text-xs text-[rgba(176,196,222,0.3)]">岗好遇见</p></div>
</aside>
</template>
