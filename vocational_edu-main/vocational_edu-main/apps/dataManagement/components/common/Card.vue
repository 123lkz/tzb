<script setup lang="ts">
import Icon from '@/components/common/Icon.vue'

withDefaults(
  defineProps<{
    isActive?: boolean
  }>(),
  {
    isActive: false,
  }
)
</script>
<template>
  <div
    class="h-full relative bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1 flex flex-col"
  >
    <Icon
      v-if="isActive"
      name="icon-you"
      class="absolute top-1/2 -translate-y-1/2 z-[9999] transition-all duration-300 -right-[22px] opacity-40"
      color="#00ffff"
      :size="30"
    />
    <slot />
  </div>
</template>
