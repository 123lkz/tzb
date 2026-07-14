<script setup lang="ts">
import Icon from './Icon.vue'

// 学历选项类型
export interface EducationOption {
  value: string
  label: string
}

// 组件属性
interface Props {
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  showSearch?: boolean
  searchPlaceholder?: string
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'outline' | 'filled'
  options?: EducationOption[]
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '请选择...',
  disabled: false,
  showSearch: true,
  searchPlaceholder: '搜索...',
  size: 'sm',
  variant: 'default',
  options: () => [],
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  change: [value: string, option: EducationOption]
}>()

// 响应式状态
const isOpen = ref(false)
const selectedOption = ref<EducationOption | null>(null)
const searchQuery = ref('')
const highlightedIndex = ref(-1)
const selectRef = ref<HTMLDivElement>()
const optionsRef = ref<HTMLDivElement>()

// 下拉菜单位置
const dropdownPosition = ref({ top: 0, left: 0, width: 0 as number | string })

// 计算属性
const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options
  return props.options.filter(option =>
    option.label.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-5 py-3',
  }
  return sizes[props.size]
})

const variantClasses = computed(() => {
  const variants = {
    default:
      'bg-gradient-to-r from-[#00eaff]/10 to-[#00ffff]/10 text-[#00ffff] border border-[#00ffff]/20 shadow-lg',
    outline:
      'bg-transparent border-2 border-blue-500 text-blue-600 hover:border-blue-600 hover:bg-blue-50',
    filled: 'bg-gray-100 border border-gray-300 text-gray-700 hover:bg-gray-200',
  }
  return variants[props.variant]
})

// 计算下拉菜单的最小宽度
const dropdownMinWidth = computed(() => {
  if (!selectRef.value) return '200px'
  const rect = selectRef.value.getBoundingClientRect()
  return Math.max(rect.width, 200) + 'px'
})

// 方法
const selectOption = (option: EducationOption) => {
  selectedOption.value = option
  emit('update:modelValue', option.value)
  emit('change', option.value, option)
  isOpen.value = false
  searchQuery.value = ''
  highlightedIndex.value = -1
}

const calculateDropdownPosition = () => {
  if (!selectRef.value) return

  const rect = selectRef.value.getBoundingClientRect()
  dropdownPosition.value = {
    top: rect.bottom + window.scrollY + 8,
    left: rect.left + window.scrollX,
    width: 'auto', // 改为自动宽度
  }
}

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => {
      searchQuery.value = ''
      highlightedIndex.value = -1
      calculateDropdownPosition()
    })
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  if (!isOpen.value) return

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedIndex.value = Math.min(
        highlightedIndex.value + 1,
        filteredOptions.value.length - 1
      )
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedIndex.value >= 0) {
        selectOption(filteredOptions.value[highlightedIndex.value])
      }
      break
    case 'Escape':
      isOpen.value = false
      break
  }
}

const handleClickOutside = (event: Event) => {
  if (selectRef.value && !selectRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
}

// 监听器
watch(
  () => props.modelValue,
  newValue => {
    if (newValue) {
      selectedOption.value = props.options.find(option => option.value === newValue) || null
    } else {
      selectedOption.value = null
    }
  },
  { immediate: true }
)

// 生命周期
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div ref="selectRef" class="relative w-full">
    <!-- 选择器触发器 -->
    <div
      :class="[
        'relative flex items-center justify-between gap-1 cursor-pointer rounded-lg transition-all duration-300 ease-out',
        sizeClasses,
        variantClasses,
        props.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
      ]"
      @click="toggleDropdown"
    >
      <!-- 选中内容 -->
      <div class="flex items-center space-x-2 flex-1">
        <span
          v-if="selectedOption"
          class="font-medium whitespace-nowrap overflow-hidden text-ellipsis max-w-40"
          >{{ selectedOption.label }}</span
        >
        <span v-else class="text-gray-400">{{ placeholder }}</span>
      </div>

      <!-- 箭头图标 -->
      <div
        class="flex items-center transition-transform duration-300"
        :class="{ 'rotate-180': isOpen }"
      >
        <Icon name="icon-xia" :size="18" />
      </div>
    </div>

    <!-- 下拉选项 -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 scale-95 -translate-y-2"
        enter-to-class="opacity-100 scale-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 scale-100 translate-y-0"
        leave-to-class="opacity-0 scale-95 -translate-y-2"
      >
        <div
          v-if="isOpen"
          ref="optionsRef"
          class="fixed z-[999999] bg-white/90 backdrop-blur-sm rounded-xl shadow-2xl border border-gray-200 overflow-hidden whitespace-nowrap"
          :style="{
            top: dropdownPosition.top + 'px',
            left: dropdownPosition.left + 'px',
            width:
              typeof dropdownPosition.width === 'number'
                ? dropdownPosition.width + 'px'
                : dropdownPosition.width,
            minWidth: dropdownMinWidth,
            maxHeight: '300px',
          }"
        >
          <!-- 搜索框 -->
          <div v-if="showSearch" class="px-4 py-2 border-b border-gray-50">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="searchPlaceholder"
                class="w-full px-3 py-2 pl-8 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-300 focus:border-transparent"
                @click.stop
              />
              <Icon
                name="icon-sousuo"
                :size="14"
                color="text-gray-400"
                class="absolute left-2 top-2.5"
              />
            </div>
          </div>

          <!-- 无结果提示 -->
          <div v-if="filteredOptions.length === 0" class="p-4 text-center text-gray-500">
            <Icon name="icon-empty" :size="48" />
            <div class="text-xs text-gray-400 whitespace-nowrap">未找到匹配的选项</div>
          </div>

          <!-- 选项列表 -->
          <div v-else class="max-h-60 overflow-y-auto px-4 py-3 px-4">
            <div
              v-for="(option, index) in filteredOptions"
              :key="option.value"
              :class="[
                'flex items-center px-3 py-1.5 my-1 text-sm rounded-lg cursor-pointer transition-all duration-200',
                selectedOption?.value === option.value
                  ? 'bg-gradient-to-r from-[#00ffff]/40 to-[#00ffff]/10'
                  : 'hover:bg-gradient-to-r hover:from-[#00ffff]/30 hover:to-[#00ffff]/10',
              ]"
              @click="selectOption(option)"
              @mouseenter="highlightedIndex = index"
            >
              <!-- 图标 -->
              <Icon v-if="option.icon" :name="option.icon" :size="14" class="mr-3" />
              <!-- 内容 -->
              <div class="flex-1">
                <div class="font-medium text-gray-900 whitespace-nowrap">{{ option.label }}</div>
                <div v-if="option.description" class="text-sm text-gray-500 mt-1 whitespace-nowrap">
                  {{ option.description }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 背景遮罩 -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="fixed inset-0 bg-black bg-opacity-25 z-[9998]"
          @click="isOpen = false"
        />
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
/* 自定义滚动条 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 平滑动画 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* 悬停效果增强 */
.hover\:scale-\[1\.02\]:hover {
  transform: scale(1.02);
}

.active\:scale-\[0\.98\]:active {
  transform: scale(0.98);
}
</style>
