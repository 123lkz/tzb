<script setup lang="ts">
import Icon from './Icon.vue'

interface Props {
  text?: string
  icon?: string
  iconSize?: number
}

const emit = defineEmits<{
  click: []
}>()

withDefaults(defineProps<Props>(), {
  text: '数据大屏',
  icon: 'icon-arrow-right',
  iconSize: 16,
})

const openDashboard = () => {
  emit('click')
}
</script>

<template>
  <button
    class="flex items-center gap-1.5 py-1.5 px-3 border-none bg-gradient-to-r from-[#00eaff] to-[#00ffff] text-[#1a2980] font-semibold text-xs rounded-md cursor-pointer transition-all duration-300 ease-in-out shadow-[0_2px_8px_rgba(0,234,255,0.3)] hover:-translate-y-0.5 hover:shadow-[0_6px_20px_rgba(0,234,255,0.4)]"
    :title="text"
    @click="openDashboard"
  >
    <span class="whitespace-nowrap text-xs">{{ text }}</span>
    <Icon :name="icon" :size="iconSize" color="#1a2980" />
  </button>
</template>
