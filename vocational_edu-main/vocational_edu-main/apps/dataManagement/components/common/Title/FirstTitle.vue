<script lang="ts" setup>
import Icon from '../Icon.vue'

const props = defineProps<{
  title: string
}>()
</script>

<template>
  <div class="flex w-full h-8 items-center relative overflow-hidden">
    <div
      class="absolute left-0 top-0 w-full h-full bg-gradient-to-l from-[#00ffff]/0 to-[#00ffff]/30 rounded-md"
    />
    <div class="flex items-center gap-2 px-2 py-1 pb-1.5">
      <span class="text-white text-sm">{{ props.title }}</span>
    </div>
    <div
      class="absolute bottom-0 w-full h-1 bg-gradient-to-l from-[#00ffff]/40 to-[#00ffff]/0 rounded-full"
    ></div>
    <div class="absolute right-0 top-0 w-full h-full flex items-center justify-end">
      <Icon name="icon-xiexian" color="#00ffff" size="28" class="opacity-20" />
    </div>
  </div>
</template>
