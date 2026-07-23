<script setup lang="ts">
defineProps<{breadcrumbs?:{label:string;path:string}[]}>()
const def=[{label:"首页",path:"/"}]
</script>
<template>
<div class="flex items-center justify-between py-3 px-4 h-14 rounded-lg bg-[rgba(0,255,255,0.05)] backdrop-blur-sm border-b border-[rgba(0,255,255,0.08)] mb-4">
<nav class="flex items-center gap-2">
<template v-for="(item,idx) in (breadcrumbs||def)" :key="idx">
<NuxtLink v-if="idx<(breadcrumbs||def).length-1" :to="item.path" class="text-[rgba(176,196,222,0.5)] no-underline text-xs hover:text-[#00eaff]">{{item.label}}</NuxtLink>
<svg v-if="idx<(breadcrumbs||def).length-1" class="w-3 h-3 text-[rgba(176,196,222,0.2)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>
<span v-else class="text-[#00eaff] text-xs font-semibold">{{item.label}}</span>
</template></nav><slot name="right"/></div></template>
