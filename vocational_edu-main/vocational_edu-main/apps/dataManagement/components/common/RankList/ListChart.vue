<script lang="ts" setup>
import { useAnimate } from '@/composables/useAnimate'

const props = withDefaults(
  defineProps<{
    value: string | number
    size?: string
    isCard?: boolean
    isFloat?: boolean
  }>(),
  {
    size: 'normal',
    isCard: false,
    isFloat: false,
  }
)

const { value: num, update } = useAnimate(0)

watch(() => props.value, update)
update(props.value)
</script>

<template>
  <span v-if="typeof value !== 'number'">{{ value }}</span>
  <span v-else-if="!isCard" class="whitespace-nowrap">{{
    formatNumber(isFloat ? num.toFixed(1) : num)
  }}</span>
  <div v-else class="flex">
    <div
      v-for="(d, index) in formatNumber(num as number)"
      :key="index"
      class="whitespace-nowrap bg-blue-400 bg-opacity-50 rounded font-number font-bold mx-1 flex justify-center flex-shrink-0 items-center text-white"
      :class="{
        'w-6 h-12': size === 'normal',
        'w-10 h-16': size === 'large',
      }"
    >
      {{ d }}
    </div>
  </div>
</template>
