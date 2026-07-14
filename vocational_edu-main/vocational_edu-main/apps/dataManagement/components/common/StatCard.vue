<template>
  <div
    :class="[
      'h-full py-4 px-6 flex justify-center items-baseline cursor-pointer transition-all rounded-xl transform hover:scale-105',
      highlight
        ? 'bg-gradient-to-b from-[#00eaff20] via-[#00eaff30] to-[#00eaff20] border-2 border-cyan-400 shadow-lg shadow-cyan-400/30'
        : 'bg-gradient-to-b from-[#182848cc] via-[#25395ecc] to-[#1a2980cc] hover:scale-105',
    ]"
    :style="
      highlight
        ? {
            boxShadow:
              '0 0 20px rgba(0, 234, 255, 0.5), 0 0 40px rgba(0, 234, 255, 0.3), 0 0 60px rgba(0, 234, 255, 0.1)',
            filter: 'drop-shadow(0 0 10px rgba(0, 234, 255, 0.4))',
          }
        : {}
    "
    @click="$emit('click')"
  >
    <div :class="['text-lg text-cyan-300 text-center']">
      {{ title }}
    </div>
    <div
      :class="[
        'text-2xl ml-4 font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-400',
      ]"
    >
      {{ value }}
      <span class="text-base">{{ unit }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; value: string | number; highlight?: boolean; unit: string }>()
</script>

<style scoped>
.text-shadow-glow {
  filter: drop-shadow(0 0 8px rgba(0, 234, 255, 0.6));
}
</style>
