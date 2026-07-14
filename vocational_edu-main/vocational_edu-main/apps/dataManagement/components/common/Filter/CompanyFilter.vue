<script setup lang="ts">
import BaseFilter from './BaseFilter.vue'
import { companyScaleMap, companyScaleOptions } from '~/utils/constants'

const emit = defineEmits<{
  'update:modelValue': [value: string, label: string]
}>()

const props = defineProps<{
  modelValue: string
}>()

const handleCompanyChange = (value: string) => {
  emit('update:modelValue', value, companyScaleMap[value])
}
</script>

<template>
  <BaseFilter
    :model-value="props.modelValue"
    label="单位"
    :options="companyScaleOptions"
    placeholder="选择单位规模"
    :show-all-option="true"
    all-option-value="全部"
    all-option-label="全部"
    @update:model-value="handleCompanyChange"
  />
</template>
