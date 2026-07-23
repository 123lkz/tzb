<script setup lang="ts">
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import { generateMockReport } from "~/utils/mockData"
const route = useRoute()
const report = generateMockReport("大模型算法工程师")
function getColor(s: number): string {
  return s >= 0.8 ? "#6bcb77" : s >= 0.6 ? "#ffd93d" : "#ff6b6b"
}
const dimensions = [
  {k:"技能匹配", v:report.dimensionScores.skill*100, w:"权重45%"},
  {k:"经验匹配", v:report.dimensionScores.experience*100, w:"权重30%"},
  {k:"职责匹配", v:report.dimensionScores.responsibility*100, w:"权重25%"}
]
</script>
<template>
<div class="fade-in">
<Header :breadcrumbs="[{label:'首页',path:'/'},{label:'简历-岗位匹配',path:'/matching'},{label:'匹配诊断报告',path:''}]" />
<div class="grid grid-cols-4 gap-4 mb-4">
<Card class="!p-4 col-span-1 flex-center flex-col">
<div class="relative w-28 h-28 flex-center">
<svg viewBox="0 0 120 120" class="w-full h-full"><circle cx="60" cy="60" r="50" fill="none" stroke="rgba(0,255,255,0.1)" stroke-width="8"/><circle cx="60" cy="60" r="50" fill="none" :stroke="getColor(report.overallMatchScore)" stroke-width="8" :stroke-dasharray="`${report.overallMatchScore*314} 314`" stroke-linecap="round" transform="rotate(-90 60 60)"/></svg>
<div class="absolute text-center"><span class="text-2xl font-bold" :style="{color:getColor(report.overallMatchScore)}">{{Math.round(report.overallMatchScore*100)}}%</span></div>
</div>
<span class="text-xs text-[rgba(176,196,222,0.4)] mt-2">综合匹配度</span>
</Card>
<div class="col-span-3 grid grid-cols-3 gap-4">
<Card v-for="(d,i) in dimensions" :key="i" class="!p-4 flex flex-col items-center gap-2">
<span class="text-xs text-[rgba(176,196,222,0.4)]">{{d.k}}</span>
<span class="text-xl font-bold" :style="{color:getColor(d.v/100)}">{{Math.round(d.v)}}%</span>
<div class="w-full bg-[rgba(0,255,255,0.1)] rounded h-1.5"><div class="h-full rounded" :style="{width:d.v+'%',background:getColor(d.v/100)}"></div></div>
<span class="text-[10px] text-[rgba(176,196,222,0.3)]">{{d.w}}</span>
</Card>
</div></div>
<div class="grid grid-cols-2 gap-4">
<Card><h3 class="text-sm text-[#00ffff] font-semibold mb-3">技能匹配详情</h3><div class="space-y-2">
<div v-for="s in report.skillMatches" :key="s.skill" class="bg-[rgba(0,255,255,0.04)] rounded p-2">
<div class="flex items-center justify-between"><div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full" :class="s.matched?'bg-[#6bcb77]':'bg-[#ff6b6b]'"></span><span class="text-xs">{{s.skill}}</span><span v-if="s.required" class="text-[10px] px-1 py-0.5 rounded bg-[rgba(255,107,107,0.1)] text-[#ff6b6b]">必需</span><span v-else class="text-[10px] px-1 py-0.5 rounded bg-[rgba(255,217,61,0.1)] text-[#ffd93d]">加分</span></div><span class="text-[10px]" :class="s.matched?'text-[#6bcb77]':'text-[#ff6b6b]'">{{s.matched?"已匹配":"未匹配"}}</span></div>
<p v-if="s.evidence" class="text-[10px] text-[rgba(176,196,222,0.4)] mt-1">{{s.evidence}}</p>
<p v-if="s.suggestion" class="text-[10px] text-[#ffd93d] mt-0.5">建议：{{s.suggestion}}</p>
</div></div></Card>
<div class="space-y-4">
<Card><h3 class="text-sm text-[#ff6b6b] font-semibold mb-3">差距分析</h3><div v-if="report.gaps.length===0" class="text-xs text-center py-6 text-[rgba(176,196,222,0.4)]">未发现明显差距</div>
<div v-else class="space-y-2"><div v-for="g in report.gaps" :key="g.skill" class="bg-[rgba(255,107,107,0.04)] rounded p-2 border border-[rgba(255,107,107,0.1)]">
<div class="flex items-center justify-between mb-1"><span class="text-xs">{{g.skill}}</span><span class="text-[10px] px-1 py-0.5 rounded" :class="g.importance==='high'?'bg-[rgba(255,107,107,0.15)] text-[#ff6b6b]':'bg-[rgba(255,217,61,0.15)] text-[#ffd93d]'">{{g.importance==="high"?"高优先级":"中"}}</span></div>
<p class="text-[10px] text-[rgba(176,196,222,0.4)]">{{g.reason}}</p>
<p class="text-[10px] text-[#ffd93d]">→ {{g.suggestion}}</p>
</div></div></Card>
<Card><h3 class="text-sm text-[#6bcb77] font-semibold mb-3">优势总结</h3><ul class="space-y-1.5"><li v-for="(s,i) in report.strengths" :key="i" class="flex items-start gap-2 text-xs"><span class="text-[#6bcb77]">·</span><span>{{s}}</span></li></ul></Card>
</div></div>
<div class="text-[10px] text-[rgba(176,196,222,0.25)] text-right mt-2">诊断模型：{{report.provenance.model}} · {{report.provenance.timestamp}}</div>
</div>
</template>
