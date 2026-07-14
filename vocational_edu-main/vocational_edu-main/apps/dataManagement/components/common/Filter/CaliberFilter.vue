<script setup lang="ts">
import BaseFilter from './BaseFilter.vue'
import { caliberOptions } from '~/utils/constants'

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const props = defineProps<{
  modelValue: string
}>()

const handleCaliberChange = (value: string) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <BaseFilter
    :model-value="props.modelValue"
    label="口径"
    :options="caliberOptions"
    placeholder="选择统计口径"
    @update:model-value="handleCaliberChange"
  />
</template>
