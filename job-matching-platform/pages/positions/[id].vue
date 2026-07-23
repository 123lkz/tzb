<script setup lang="ts">
import { computed } from "vue"
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import Loading from "~/components/Common/Loading.vue"
import { fetchPositionById } from "~/utils/api"
const route=useRoute()
const {data:pos,pending}=await useAsyncData(()=>fetchPositionById(route.params.id as string))
const crumbs=computed(()=>[{label:"首页",path:"/"},{label:"岗位信息",path:"/positions"},{label:pos.value?.name||"详情",path:""}])
</script>
<template>
<div class="fade-in">
<Header :breadcrumbs="crumbs" />
<Loading v-if="pending" />
<template v-else-if="pos">
<div class="grid grid-cols-3 gap-4">
<div class="col-span-2 space-y-4">
<Card><div class="flex items-start justify-between mb-4"><div><h1 class="text-xl font-bold text-[#00ffff]">{{pos.name}}</h1><p class="text-sm text-[rgba(176,196,222,0.5)] mt-1">{{pos.company}} · {{pos.province}} {{pos.city}}</p></div><div class="text-right"><div class="text-2xl font-bold text-[#ffd93d]">{{pos.salaryMin}}-{{pos.salaryMax}}<span class="text-sm">K</span></div><p class="text-xs text-[rgba(176,196,222,0.3)]">月薪</p></div></div>
<div class="flex flex-wrap gap-2 mb-4"><span class="px-2.5 py-1 text-xs rounded bg-[rgba(0,255,255,0.1)] text-[#00ffff]">{{pos.education}}</span><span class="px-2.5 py-1 text-xs rounded bg-[rgba(255,107,107,0.1)] text-[#ff6b6b]">{{pos.experience}}</span><span v-for="tag in pos.tags" :key="tag" class="px-2.5 py-1 text-xs rounded bg-[rgba(255,217,61,0.08)] text-[#ffd93d]">{{tag}}</span><span class="px-2.5 py-1 text-xs rounded bg-[rgba(107,203,119,0.1)] text-[#6bcb77]">{{pos.industry}}</span></div>
</Card>
<Card><h3 class="text-sm text-[#00ffff] font-semibold mb-3">职位描述</h3><p class="text-xs text-[rgba(176,196,222,0.7)] leading-relaxed">{{pos.description}}</p></Card>
<Card><h3 class="text-sm text-[#00ffff] font-semibold mb-3">工作职责</h3><ul class="space-y-1.5"><li v-for="(r,i) in pos.responsibilities" :key="i" class="flex items-start gap-2 text-xs text-[rgba(176,196,222,0.7)]"><span class="text-[#00ffff]">·</span><span>{{r}}</span></li></ul></Card>
</div>
<div class="space-y-4">
<Card><h3 class="text-sm text-[#ff6b6b] font-semibold mb-3">必需技能</h3><div class="flex flex-wrap gap-1.5"><span v-for="s in pos.requiredSkills" :key="s" class="px-2 py-1 text-xs rounded bg-[rgba(255,107,107,0.1)] text-[#ff6b6b]">{{s}}</span></div></Card>
<Card><h3 class="text-sm text-[#ffd93d] font-semibold mb-3">加分技能</h3><div class="flex flex-wrap gap-1.5"><span v-for="s in pos.optionalSkills" :key="s" class="px-2 py-1 text-xs rounded bg-[rgba(255,217,61,0.08)] text-[#ffd93d]">{{s}}</span></div></Card>
<NuxtLink :to="'/matching?position='" class="block"><button class="w-full py-2.5 text-sm rounded bg-[rgba(0,255,255,0.15)] text-[#00ffff] border border-[rgba(0,255,255,0.3)] hover:bg-[rgba(0,255,255,0.25)] cursor-pointer">匹配此岗位</button></NuxtLink>
</div></div></template>
<div v-else class="flex-center py-20"><p class="text-sm text-[rgba(176,196,222,0.3)]">岗位不存在</p></div>
</div></template>
