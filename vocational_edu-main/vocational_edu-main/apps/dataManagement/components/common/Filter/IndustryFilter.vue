<script setup lang="ts">
import TreeSelect from '../TreeSelect.vue'
import { industryMajorCategoryOptions, industryMediumCategoryOptions } from '~/utils/constants'

const emit = defineEmits<{
  change: [value: string, label: string, level: string]
}>()

const props = defineProps<{
  modelValue: string
}>()

const industryMinorCategoryOptions = [
  {
    value: 'A-01-011',
    label: '谷物种植',
  },
  {
    value: 'A-01-012',
    label: '豆类、油料和薯类种植',
  },
  {
    value: 'A-01-013',
    label: '棉、麻、糖、烟草种植',
  },
]

const handleIndustryChange = (value: string, option?: any) => {
  emit('change', value, option ? option.label : '', value ? value.split('-').length.toString() : '')
}
</script>

<template>
  <div class="flex items-center flex-nowrap flex-shrink-0">
    <label class="text-sm text-[#00eaff] font-medium uppercase tracking-wider whitespace-nowrap">
      标准行业：
    </label>
    <TreeSelect
      :model-value="props.modelValue"
      placeholder="选择标准行业"
      :option-labels="{
        '1': '国民经济行业门类',
        '2': '国民经济行业大类',
        '3': '国民经济行业中类',
        '4': '国民经济行业小类',
      }"
      :options-level1="industryMajorCategoryOptions"
      :options-level2="industryMediumCategoryOptions"
      :options-level3="industryMinorCategoryOptions"
      @change="handleIndustryChange"
    />
  </div>
</template>
