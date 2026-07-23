<script setup lang="ts">defineProps<{text?:string}>()</script>
<template><div class="flex-center flex-col gap-3 py-20"><div class="w-10 h-10 rounded-full border-2 border-transparent border-t-[#00ffff] animate-spin"></div><p class="text-sm text-[rgba(176,196,222,0.5)]">{{text||"加载中..."}}</p></div></template>
