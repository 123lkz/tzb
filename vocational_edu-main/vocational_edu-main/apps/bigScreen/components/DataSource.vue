<script setup lang="ts">
const props = defineProps<{
  source?: string
  isFake?: boolean
}>()
</script>

<template>
  <div class="text-xs text-white/40 absolute bottom-2 right-4">
    数据来源：<span v-if="props.isFake" class="text-red-500">假数据</span>
    <span v-else>{{ props.source }}</span>
  </div>
</template>
