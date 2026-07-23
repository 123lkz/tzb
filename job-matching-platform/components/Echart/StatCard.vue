<template>
  <div class="bg-[rgba(0,255,255,0.06)] border border-[rgba(0,255,255,0.12)] rounded-lg p-3 card-hover">
    <div class="flex items-center justify-between mb-1">
      <span class="text-xs text-[rgba(176,196,222,0.5)]">{{ label }}</span>
      <span v-if="trend" class="text-[10px]" :class="trend > 0 ? 'text-[#6bcb77]' : 'text-[#ff6b6b]'">
        {{ trend > 0 ? '+' : '' }}{{ trend }}%
      </span>
    </div>
    <div class="flex items-baseline gap-1">
      <span class="text-xl font-bold" :style="{color: color || '#00ffff'}">{{ value }}</span>
      <span class="text-xs text-[rgba(176,196,222,0.35)]">{{ unit }}</span>
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{ label: string; value: string|number; unit?: string; color?: string; trend?: number }>()
</script>
<style scoped>
.card-hover { transition: all 0.3s ease; }
.card-hover:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,255,255,0.15); }
</style>
