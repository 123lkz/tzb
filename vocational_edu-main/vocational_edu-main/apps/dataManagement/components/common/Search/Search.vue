<script setup lang="ts">
import Icon from '../Icon.vue'

// 过滤项接口定义
export interface FilterOption {
  label: string
  value: string | number
}

export interface FilterItem {
  key: string
  label: string
  placeholder?: string
  type: 'input' | 'select'
  options?: FilterOption[]
}

// Props 定义
interface Props {
  filters?: FilterItem[]
  modelValue?: Record<string, any>
  maxVisibleItems?: number
}

// Emits 定义
interface Emits {
  (e: 'update:modelValue', value: Record<string, any>): void
  (e: 'search', value: Record<string, any>): void
  (e: 'reset'): void
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => ({}),
  maxVisibleItems: 5,
  filters: () => [],
})

const emit = defineEmits<Emits>()

// 响应式数据
const formData = ref<Record<string, any>>({})

const handleSearch = () => {
  emit('search', { ...formData.value })
}

const handleReset = () => {
  // 重置表单数据
  const resetData: Record<string, any> = {}
  if (props.filters) {
    props.filters.forEach(filter => {
      resetData[filter.key] = ''
    })
  }
  formData.value = resetData
  emit('update:modelValue', resetData)
  emit('reset')
}

// 防止循环更新的标志
const isUpdatingFromParent = ref(false)

// 监听 props.modelValue 变化
watch(
  () => props.modelValue,
  newValue => {
    if (newValue && !isUpdatingFromParent.value) {
      isUpdatingFromParent.value = true
      formData.value = { ...newValue }
      nextTick(() => {
        isUpdatingFromParent.value = false
      })
    }
  },
  { immediate: true, deep: true }
)

// 监听 formData 变化，同步到父组件
watch(
  formData,
  newValue => {
    if (!isUpdatingFromParent.value) {
      emit('update:modelValue', { ...newValue })
    }
  },
  { deep: true }
)

// 初始化
onMounted(() => {
  // 初始化表单数据
  const initialData: Record<string, any> = {}
  if (props.filters) {
    props.filters.forEach(filter => {
      initialData[filter.key] = props.modelValue?.[filter.key] || ''
    })
  }
  formData.value = initialData
})
</script>

<template>
  <div class="rounded-lg p-4 shadow-sm bg-[#00ffff]/10 mb-4">
    <div class="flex-1 flex items-start justify-between gap-4">
      <div class="flex flex-wrap gap-3">
        <div
          v-for="item in props.filters"
          :key="item.key"
          class="flex items-center gap-2 min-w-0 flex-shrink-0"
        >
          <label class="text-sm font-medium text-gray-400 whitespace-nowrap">
            {{ item.label }}:
          </label>
          <!-- Input 类型 -->
          <input
            v-if="item.type === 'input'"
            v-model="formData[item.key]"
            :placeholder="item.placeholder"
            class="px-3 py-1.5 bg-[#00ffff]/0 border border-[#00ffff]/30 rounded-md focus:outline-none focus:ring-1 focus:ring-[#00ffff]/50 focus:border-transparent text-sm w-[160px] text-white/80"
            type="text"
          />
          <!-- Select 类型 -->
          <div v-else-if="item.type === 'select'" class="relative w-[160px]">
            <select
              v-model="formData[item.key]"
              class="appearance-none px-3 py-1.5 bg-[#1f2842] border border-[#00ffff]/30 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-[#00ffff]/50 focus:border-transparent text-white/80 cursor-pointer w-full pr-8"
            >
              <option value="" style="cursor: pointer">
                {{ item.placeholder || '请选择' }}
              </option>
              <option
                v-for="option in item.options || []"
                :key="option.value"
                :value="option.value"
                style="cursor: pointer"
              >
                {{ option.label }}
              </option>
            </select>
            <!-- 自定义下拉箭头 -->
            <span class="pointer-events-none absolute right-2 top-1.5 text-[#00ffff]/70">
              <Icon name="icon-xia" :size="18" color="text-[#00ffff]/50" />
            </span>
          </div>
        </div>
      </div>
      <div class="flex items-center justify-end flex-shrink-0 gap-2">
        <button
          class="px-4 py-1.5 flex-shrink-0 whitespace-nowrap text-sm font-medium text-white bg-gray-500 rounded-md hover:bg-gray-400 focus:outline-none transition-colors"
          @click="handleReset"
        >
          重置
        </button>
        <button
          class="px-4 py-1.5 flex-shrink-0 whitespace-nowrap text-sm font-medium text-white bg-[#00ffff]/50 rounded-md hover:bg-[#00ffff]/70 focus:outline-none transition-colors"
          @click="handleSearch"
        >
          查询
        </button>
      </div>
    </div>
  </div>
</template>
