<script setup lang="ts">
import Select from '../Select.vue'

interface FilterOption {
  value: string
  label: string
}

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const props = defineProps<{
  modelValue: string
  label: string
  options: FilterOption[]
  placeholder?: string
  showAllOption?: boolean
  allOptionValue?: string
  allOptionLabel?: string
}>()

const computedOptions = computed(() => {
  const optionsCopy = [...props.options]

  if (props.showAllOption) {
    optionsCopy.unshift({
      value: props.allOptionValue || '全部',
      label: props.allOptionLabel || '全部',
    })
  }

  return optionsCopy
})

const handleChange = (value: string) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="flex items-center flex-shrink-0">
    <label class="text-sm text-[#00eaff] font-medium uppercase tracking-wider whitespace-nowrap"
      >{{ label }}：</label
    >
    <Select
      :model-value="props.modelValue"
      :options="computedOptions"
      size="sm"
      :placeholder="props.placeholder || '请选择...'"
      @change="handleChange"
    />
  </div>
</template>
