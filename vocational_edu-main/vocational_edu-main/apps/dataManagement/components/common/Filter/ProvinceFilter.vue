<script setup lang="ts">
import BaseFilter from './BaseFilter.vue'
import { provinceOptions } from '~/utils/constants'

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const props = defineProps<{
  modelValue: string
}>()

const handleProvinceChange = (value: string) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <BaseFilter
    :model-value="props.modelValue"
    label="省份"
    :options="provinceOptions"
    placeholder="选择省份"
    :show-all-option="true"
    all-option-value="全国"
    all-option-label="全国"
    @update:model-value="handleProvinceChange"
  />
</template>
