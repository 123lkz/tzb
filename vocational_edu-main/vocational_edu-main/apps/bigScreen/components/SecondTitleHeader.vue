<script lang="ts" setup>
defineProps<{
  title: string
  subtext?: string
}>()
</script>
<template>
  <div class="flex items-center relative">
    <div class="relative flex items-center justify-center">
      <svg viewBox="0 0 1024 1024" width="40" height="40">
        <path
          d="M675.9 107.2H348.1c-42.9 0-82.5 22.9-104 60.1L80 452.1c-21.4 37.1-21.4 82.7 0 119.8l164.1 284.8c21.4 37.2 61.1 60.1 104 60.1h327.8c42.9 0 82.5-22.9 104-60.1L944 571.9c21.4-37.1 21.4-82.7 0-119.8L779.9 167.3c-21.4-37.1-61.1-60.1-104-60.1z"
          fill="rgb(160, 253, 254, 0.3)"
        ></path>
      </svg>
      <div class="absolute">
        <slot name="second-svg"></slot>
      </div>
    </div>
    <div class="ml-2 flex flex-col items-start gap-[1px]">
      <p class="text-sm text-[#00ffff]/90">{{ title }}</p>
      <p v-if="subtext" class="text-xs text-[#00ffff]/70">{{ subtext }}</p>
    </div>
  </div>
</template>
