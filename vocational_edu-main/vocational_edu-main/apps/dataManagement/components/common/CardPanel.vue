<template>
  <div
    class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
  >
    <div v-if="$slots.title">
      <TitleHeader :title="getTitleSlotText()">
        <template #button>
          <slot name="button" />
        </template>
      </TitleHeader>
    </div>
    <div>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSlots, h } from 'vue'
import TitleHeader from './Title/FirstTitle.vue'

const slots = useSlots()
function getTitleSlotText() {
  const vnodes = slots.title?.() || []
  let text = ''
  vnodes.forEach(vnode => {
    if (typeof vnode.children === 'string') {
      text += vnode.children
    }
  })
  return text
}
</script>
