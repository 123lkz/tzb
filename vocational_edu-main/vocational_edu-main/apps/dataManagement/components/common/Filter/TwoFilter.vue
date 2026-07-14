<script setup lang="ts">
interface FilterOption {
  value: string
  label: string
}

interface Props {
  options?: FilterOption[]
  showBorder?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  options: () => [],
  showBorder: true,
})

const emits = defineEmits<{
  'on-change': [type: string]
}>()

// 统计口径，默认值为第一个选项
const filterType = ref(props.options[0]?.value || '')

// 统计口径切换
const handleQuantityFilterChange = (type: string) => {
  if (filterType.value === type) {
    return
  }
  filterType.value = type
  emits('on-change', filterType.value)
}

defineExpose({
  handleQuantityFilterChange,
  filterType,
})
</script>

<template>
  <div class="flex justify-center items-center">
    <div
      class="flex gap-3 bg-cyan-500/5 shadow-lg shadow-cyan-500/10 backdrop-blur-md"
      :class="[props.showBorder ? 'border border-cyan-400/20 p-1 rounded-md' : '']"
    >
      <div
        v-for="option in options"
        :key="option.value"
        class="flex items-center justify-center px-2 py-1 cursor-pointer transition-all duration-300 ease-in-out rounded"
        :class="[
          filterType === option.value
            ? 'text-cyan-400 bg-cyan-500/15'
            : 'text-white/60 hover:text-cyan-600 hover:bg-cyan-500/10 hover:-translate-y-0.5',
        ]"
        @click="handleQuantityFilterChange(option.value)"
      >
        <span class="text-xs tracking-wide whitespace-nowrap">{{ option.label }}</span>
      </div>
    </div>
  </div>
</template>
