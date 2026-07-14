<script setup lang="ts">
import TreeSelect from '../TreeSelect.vue'

const emit = defineEmits<{
  change: [value: string, label: string, level: string]
}>()

const props = defineProps<{
  modelValue: string
}>()

const careerMajorCategoryOptions = [
  {
    value: '1',
    label: '党的机关、国家机关、群众团体和社会组织、企事业单位负责人',
  },
  {
    value: '2',
    label: '专业技术人员',
  },
  {
    value: '3',
    label: '办事人员和有关人员',
  },
  {
    value: '4',
    label: '社会生产服务和生活服务人员',
  },
]

const careerMediumCategoryOptions = [
  {
    value: '1-01',
    label: '中国共产党机关负责人',
  },
  {
    value: '1-02',
    label: '国家机关负责人',
  },
]

const careerMinorCategoryOptions = [
  {
    value: '1-01-00',
    label: '中国共产党机关负责人',
  },
  {
    value: '1-02-01',
    label: '国家权力机关负责人',
  },
  {
    value: '1-02-03',
    label: '人民政协机关负责人',
  },
]

const handleCareerChange = (value: string, option?: any) => {
  emit('change', value, option ? option.label : '', value ? value.split('-').length.toString() : '')
}
</script>

<template>
  <div class="flex items-center flex-nowrap flex-shrink-0">
    <label class="text-sm text-[#00eaff] font-medium uppercase tracking-wider whitespace-nowrap">
      标准职业：
    </label>
    <TreeSelect
      :model-value="props.modelValue"
      placeholder="选择标准职业"
      :option-labels="{
        '1': '标准职业大类',
        '2': '标准职业中类',
        '3': '标准职业小类',
        '4': '标准职业细类',
      }"
      :options-level1="careerMajorCategoryOptions"
      :options-level2="careerMediumCategoryOptions"
      :options-level3="careerMinorCategoryOptions"
      @change="handleCareerChange"
    />
  </div>
</template>
