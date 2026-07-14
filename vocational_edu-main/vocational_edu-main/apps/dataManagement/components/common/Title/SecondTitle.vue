<script lang="ts" setup>
import Icon from '../Icon.vue'

const emit = defineEmits<{
  click: []
}>()

withDefaults(
  defineProps<{
    type?: 'circle' | 'pentagon'
    title: string
    subtext?: string
    icon: string
    iconSize?: string | number
    showTextButton?: boolean
    buttonText?: string
    titleSize?: string
  }>(),
  {
    type: 'pentagon',
    subtext: '',
    iconSize: 28,
    showTextButton: false,
    buttonText: '更多',
    titleSize: 'sm',
  }
)

const handleClick = () => {
  emit('click')
}
</script>
<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <div class="relative flex items-center justify-center">
        <div
          v-if="type === 'circle'"
          class="w-8 h-8 rounded-full bg-[#00ffff]/10 border border-[#00ffff]/10"
        ></div>
        <svg v-else viewBox="0 0 1024 1024" width="40" height="40">
          <path
            d="M675.9 107.2H348.1c-42.9 0-82.5 22.9-104 60.1L80 452.1c-21.4 37.1-21.4 82.7 0 119.8l164.1 284.8c21.4 37.2 61.1 60.1 104 60.1h327.8c42.9 0 82.5-22.9 104-60.1L944 571.9c21.4-37.1 21.4-82.7 0-119.8L779.9 167.3c-21.4-37.1-61.1-60.1-104-60.1z"
            fill="rgb(0, 255, 255, 0.15)"
          ></path>
        </svg>
        <div class="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center">
          <Icon :name="icon" color="#00ffff" :size="iconSize" />
        </div>
      </div>
      <div class="flex flex-col items-start gap-[1px]">
        <p :class="`text-${titleSize} text-[#00ffff]/90`">{{ title }}</p>
        <p v-if="subtext" class="text-xs text-[#00ffff]/70">{{ subtext }}</p>
      </div>
    </div>
    <div v-if="showTextButton" class="flex items-center gap-1 cursor-pointer hover:scale-105">
      <span class="text-xs text-blue-200 hover:text-blue-100" @click="handleClick">
        {{ buttonText }}
      </span>
      <Icon name="icon-arrow-right" color="text-blue-200" :size="14" />
    </div>
  </div>
</template>
