<script setup lang="ts">
import Icon from './Icon.vue'

// 树形选项类型
export interface TreeNode {
  value: string
  label: string
  icon?: string
  description?: string
}

// 组件属性
interface Props {
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  showSearch?: boolean
  searchPlaceholder?: string
  size?: 'sm' | 'md'
  variant?: 'default' | 'outline' | 'filled'
  // 支持传入4个独立的options数组
  optionLabels?: Record<string, string>
  optionsLevel1?: TreeNode[]
  optionsLevel2?: TreeNode[]
  optionsLevel3?: TreeNode[]
  optionsLevel4?: TreeNode[]
  // 长文本处理
  maxLabelLines?: number
  showTooltip?: boolean
  // 滚动优化
  scrollThreshold?: number
  preloadDistance?: number
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '请选择...',
  disabled: false,
  showSearch: true,
  searchPlaceholder: '搜索...',
  size: 'sm',
  variant: 'default',
  optionsLevel1: () => [],
  optionsLevel2: () => [],
  optionsLevel3: () => [],
  optionsLevel4: () => [],
  optionLabels: () => ({}),
  maxLabelLines: 2,
  showTooltip: true,
  scrollThreshold: 100,
  preloadDistance: 200,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  change: [value: string, option: TreeNode]
  'level-change': [level: number, selectedNode: TreeNode | null]
}>()

const optionsLabelList = computed(() => {
  if (!props.optionLabels) {
    return []
  }

  return Object.keys(props.optionLabels).map(value => {
    return {
      label: props.optionLabels[value] as string,
      value,
    }
  })
})

// 响应式状态
const isOpen = ref(false)
const selectedOption = ref<TreeNode | null>(null)
const searchQuery = ref('')
const highlightedIndex = ref(-1)
const selectRef = ref<HTMLDivElement>()
const optionsRef = ref<HTMLDivElement>()

// 树形菜单状态
const currentLevel = ref(0) // 当前展开的层级
const expandedMenus = ref<TreeNode[][]>([]) // 每层展开的菜单
const selectedPath = ref<TreeNode[]>([]) // 选中的路径

// 滚动优化状态
const scrollPositions = ref(new Map<string, number>()) // 各层级的滚动位置

// 下拉菜单位置
const dropdownPosition = ref({ top: 0, left: 0, width: 0 as number | string })

// 计算属性 - 获取当前层级的选项
const getCurrentLevelOptions = (level: number): TreeNode[] => {
  switch (level) {
    case 0:
      return props.optionsLevel1
    case 1:
      return props.optionsLevel2
    case 2:
      return props.optionsLevel3
    case 3:
      return props.optionsLevel4
    default:
      return []
  }
}

// 计算属性 - 第一级选项（用于搜索和显示）
const firstLevelOptions = computed(() => {
  return getCurrentLevelOptions(0)
})

// 修改计算属性 - 过滤后的选项
const filteredOptions = computed(() => {
  if (!searchQuery.value) return firstLevelOptions.value

  // 搜索逻辑：搜索所有层级并构建层级路径
  const searchResults: Array<{
    option: TreeNode
    path: TreeNode[]
    pathLabels: string[]
  }> = []

  const searchKeyword = searchQuery.value.toLowerCase()

  // 逐级搜索，只返回匹配项及其父级路径
  for (let level = 0; level < 4; level++) {
    const levelOptions = getCurrentLevelOptions(level)

    for (const option of levelOptions) {
      if (option.label.toLowerCase().includes(searchKeyword)) {
        // 找到匹配项，构建完整路径
        const path: TreeNode[] = []
        const pathLabels: string[] = []

        // 构建父级路径
        if (level > 0) {
          // 根据当前选项的value构建父级路径
          const valueParts = option.value.split('-')

          for (let i = 0; i < level; i++) {
            const parentValue = valueParts.slice(0, i + 1).join('-')
            const parentLevelOptions = getCurrentLevelOptions(i)
            const parentOption = parentLevelOptions.find(opt => opt.value === parentValue)

            if (parentOption) {
              path.push(parentOption)
              pathLabels.push(parentOption.label)
            }
          }
        }

        // 添加当前匹配项
        path.push(option)
        pathLabels.push(option.label)

        searchResults.push({
          option,
          path,
          pathLabels,
        })
      }
    }
  }

  return searchResults
})

// 添加计算属性 - 是否显示搜索模式
const isSearchMode = computed(() => {
  return searchQuery.value.length > 0
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-4 py-2',
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

// 获取节点的子节点（从对应层级的options中获取数据）
const getNodeChildren = (level: number): TreeNode[] => {
  // 从对应层级的options中获取数据
  const nextLevelOptions = getCurrentLevelOptions(level + 1)
  if (nextLevelOptions.length > 0) {
    return nextLevelOptions
  }

  return []
}

// 获取层级标题
const getLevelTitle = (level: number): string => {
  return props.optionLabels[level] || ''
}

// 方法
const selectOption = (option: TreeNode, level: number) => {
  // 记录选择路径
  selectedPath.value[level] = option

  // 所有级别选择都更新 modelValue 并关闭弹框
  selectedOption.value = option
  emit('update:modelValue', option.value)
  emit('change', option.value, option)
  isOpen.value = false
  searchQuery.value = ''
  highlightedIndex.value = -1
  // 重置展开状态
  currentLevel.value = 0
  expandedMenus.value = []
  selectedPath.value = []
}

// 修改选择方法，支持搜索模式下的选择
const selectSearchResult = (searchResult: any) => {
  const { option, path } = searchResult

  // 设置选中路径
  selectedPath.value = path

  // 设置最终选中的选项
  selectedOption.value = option

  // 更新 modelValue
  emit('update:modelValue', option.value)
  emit('change', option.value, option)

  // 关闭弹框并重置搜索
  isOpen.value = false
  searchQuery.value = ''
  highlightedIndex.value = -1

  // 重置展开状态
  currentLevel.value = 0
  expandedMenus.value = []
}

const expandMenu = (option: TreeNode, level: number) => {
  const children = getNodeChildren(level)
  if (children.length === 0) return

  // 关闭其他层级的菜单
  if (level < currentLevel.value) {
    expandedMenus.value = expandedMenus.value.slice(0, level + 1)
  }

  // 展开当前菜单
  expandedMenus.value[level] = children
  currentLevel.value = level + 1

  // 记录选择路径 - 将当前选项设置为选中状态（但不更新 modelValue）
  selectedPath.value[level] = option

  // 触发 level-change 事件，让父组件更新子节点内容
  emit('level-change', level, option)
}

const handleMenuAction = (option: TreeNode, level: number) => {
  // 检查是否有下一级数据
  const hasNextLevel = getCurrentLevelOptions(level + 1).length > 0

  if (hasNextLevel) {
    // 有下一级数据，展开
    expandMenu(option, level)
  } else {
    // 没有下一级数据，选择
    selectOption(option, level)
  }
}

// 滚动优化处理
const handleScroll = (event: Event, level: number) => {
  const target = event.target as HTMLElement
  const scrollTop = target.scrollTop

  // 记录滚动位置
  const nodeKey = `${selectedPath.value[level]?.value}-${level}`
  scrollPositions.value.set(nodeKey, scrollTop)
}

// 防抖滚动处理
const debouncedScroll = (() => {
  let timeoutId: NodeJS.Timeout | null = null
  return (event: Event, level: number) => {
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      handleScroll(event, level)
    }, 100)
  }
})()

const calculateDropdownPosition = () => {
  if (!selectRef.value) return

  const rect = selectRef.value.getBoundingClientRect()
  dropdownPosition.value = {
    top: rect.bottom + window.scrollY + 8,
    left: rect.left + window.scrollX,
    width: 'auto',
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

  const currentOptions =
    currentLevel.value === 0
      ? filteredOptions.value
      : expandedMenus.value[currentLevel.value - 1] || []

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, currentOptions.length - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedIndex.value >= 0) {
        const option = currentOptions[highlightedIndex.value]
        handleMenuAction(option, currentLevel.value === 0 ? 0 : currentLevel.value - 1)
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

// 添加清除方法
const clearSelection = () => {
  selectedOption.value = null
  selectedPath.value = []
  expandedMenus.value = []
  currentLevel.value = 0
  emit('update:modelValue', '', { label: '', value: '' })
  emit('change', '', null)
}

// 监听器
watch(
  () => props.modelValue,
  newValue => {
    if (newValue) {
      // 检查是否包含分隔符，判断是否为多级路径
      if (newValue.includes('-')) {
        // 多级路径解析
        const pathParts = newValue.split('-')
        const selectedPathArray: TreeNode[] = []

        // 重置状态
        currentLevel.value = 0
        expandedMenus.value = []
        selectedPath.value = []

        // 逐级查找并设置选中状态
        for (let level = 0; level < pathParts.length && level < 4; level++) {
          const currentPath = pathParts.slice(0, level + 1).join('-')
          const levelOptions = getCurrentLevelOptions(level)

          // 在当前层级中查找匹配的选项
          const found = levelOptions.find(option => option.value === currentPath)
          if (found) {
            selectedPathArray[level] = found

            // 如果不是最后一级，展开下一级菜单
            if (level < pathParts.length - 1) {
              const children = getNodeChildren(level)
              if (children.length > 0) {
                expandedMenus.value[level] = children
                currentLevel.value = level + 1
              }
            }
          } else {
            // 如果某一级找不到，停止解析
            break
          }
        }

        // 更新选中路径
        selectedPath.value = selectedPathArray

        // 设置最终选中的选项为最后一级
        if (selectedPathArray.length > 0) {
          const lastSelected = selectedPathArray[selectedPathArray.length - 1]
          if (lastSelected) {
            selectedOption.value = lastSelected
          }
        }
      } else {
        // 单级值查找（保持原有逻辑）
        const findOption = (nodes: TreeNode[], value: string): TreeNode | null => {
          for (const node of nodes) {
            if (node.value === value) return node
          }
          return null
        }

        // 重置状态
        currentLevel.value = 0
        expandedMenus.value = []
        selectedPath.value = []

        // 在所有层级中查找
        for (let level = 0; level < 4; level++) {
          const levelOptions = getCurrentLevelOptions(level)
          const found = findOption(levelOptions, newValue)
          if (found) {
            selectedOption.value = found
            // 修复：为单级值设置 selectedPath
            selectedPath.value[level] = found
            break
          }
        }
      }
    } else {
      selectedOption.value = null
      selectedPath.value = []
      expandedMenus.value = []
      currentLevel.value = 0
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
      <div class="flex items-center space-x-2">
        <span
          v-if="selectedOption"
          class="font-medium truncate flex-1 max-w-32"
          :title="selectedOption.label"
        >
          {{ selectedOption.label }}
        </span>
        <span v-else class="text-gray-400 truncate flex-1">{{ placeholder }}</span>
      </div>

      <div class="flex items-center gap-1">
        <!-- 清除按钮 -->
        <div
          v-if="selectedOption"
          class="flex items-center p-1 cursor-pointer transition-all duration-200 hover:bg-[#00ffff]/20 rounded"
          title="清除选择"
          @click.stop="clearSelection"
        >
          <Icon name="icon-guanbi" :size="14" color="text-[#00ffff]/30" />
        </div>

        <!-- 下拉箭头 -->
        <div
          class="flex items-center transition-transform duration-300 flex-shrink-0"
          :class="{ 'rotate-180': isOpen }"
        >
          <Icon name="icon-xia" :size="16" />
        </div>
      </div>
    </div>

    <!-- 树形下拉菜单 -->
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
          class="fixed z-[999999] bg-white/90 backdrop-blur-sm rounded-xl py-1 shadow-2xl border border-gray-200 overflow-hidden"
          :style="{
            top: dropdownPosition.top + 'px',
            left: dropdownPosition.left + 'px',
            width: 'auto',
            maxHeight: '500px',
          }"
        >
          <!-- 搜索框 -->
          <div v-if="showSearch" class="px-3 py-1.5 border-b border-gray-50 min-w-[200px]">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="searchPlaceholder"
                class="w-full px-2 py-2 pl-8 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-300 focus:border-transparent"
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

          <!-- 搜索模式显示 -->
          <div v-if="isSearchMode" class="min-w-[600px] px-4 my-2">
            <!-- 搜索标题行 -->
            <div
              class="flex items-center gap-1 px-3 py-2 border-b border-gray-50 bg-gray-50 rounded"
            >
              <div
                v-for="item in optionsLabelList"
                :key="item.value"
                class="flex-1 text-xs font-bold text-gray-700 cursor-pointer"
                @click.stop="selectOption(item, 0)"
              >
                {{ item.label }}
              </div>
            </div>

            <!-- 搜索结果列表 -->
            <div class="max-h-96 overflow-y-auto py-1">
              <template v-if="filteredOptions.length > 0">
                <div
                  v-for="(searchResult, index) in filteredOptions"
                  :key="`${searchResult.option.value}-${index}`"
                  class="flex items-center gap-1 px-2 py-2 text-gray-500 hover:bg-[#00ffff]/20 hover:text-gray-700 rounded-md cursor-pointer transition-colors"
                  @click="selectSearchResult(searchResult)"
                >
                  <div class="flex-1 text-xs truncate">
                    {{ searchResult.pathLabels[0] || '-' }}
                  </div>
                  <div class="flex-1 text-xs truncate">
                    {{ searchResult.pathLabels[1] || '-' }}
                  </div>
                  <div class="flex-1 text-xs truncate">
                    {{ searchResult.pathLabels[2] || '-' }}
                  </div>
                  <div class="flex-1 text-xs truncate">
                    {{ searchResult.pathLabels[3] || '-' }}
                  </div>
                </div>
              </template>

              <!-- 无搜索结果 -->
              <div v-else class="p-8 text-center text-gray-500">
                <Icon name="icon-empty" :size="48" class="mx-auto mb-2" />
                <div class="text-sm text-gray-400">未找到匹配的选项</div>
              </div>
            </div>
          </div>

          <!-- 正常树形菜单显示 -->
          <div v-else class="flex">
            <!-- 第一级菜单 -->
            <div class="w-[200px] max-h-96 overflow-y-auto px-2">
              <div class="flex items-center gap-1 p-2">
                <span class="text-gray-700 text-xs font-bold">{{ getLevelTitle(1) }}</span>
                <Icon name="icon-xia" :size="14" class="flex items-center justify-center" />
              </div>

              <!-- 第一级有数据时显示 -->
              <template v-if="firstLevelOptions.length > 0">
                <div
                  v-for="(option, index) in filteredOptions"
                  :key="option.value"
                  class="flex items-center justify-between gap-1 my-0.5 transition-all duration-200"
                >
                  <div
                    class="line-clamp-1 leading-relaxed text-xs min-w-0 flex-1 px-2 rounded cursor-pointer"
                    :class="[
                      selectedPath[0]?.value === option.value
                        ? 'bg-gradient-to-r from-[#00eaff]/50 to-[#00ffff]/20 text-gray-700'
                        : 'hover:bg-gradient-to-r hover:from-[#00eaff]/30 hover:to-[#00ffff]/10 text-gray-500',
                    ]"
                    :title="option.label"
                    @click="selectOption(option, 0)"
                    @mouseenter="highlightedIndex = index"
                  >
                    {{ option.label }}
                  </div>
                  <div
                    v-if="getCurrentLevelOptions(1).length > 0"
                    class="flex items-center p-2 flex-shrink-0 cursor-pointer transition-all duration-200 hover:bg-[#00ffff]/20 rounded"
                    :title="
                      selectedPath[0]?.value === option.value ? `展开 ${option.label} 的子选项` : ''
                    "
                    @click.stop="expandMenu(option, 0)"
                  >
                    <Icon
                      name="icon-arrow-right"
                      :size="14"
                      :color="
                        selectedPath[0]?.value === option.value ? 'text-gray-700' : 'text-gray-400'
                      "
                    />
                  </div>
                </div>
              </template>

              <!-- 第一级无数据时显示 Empty -->
              <div v-else class="p-8 text-center text-gray-500">
                <Icon name="icon-empty" :size="48" class="mx-auto mb-2" />
                <div class="text-sm text-gray-400">暂无数据</div>
              </div>
            </div>

            <!-- 右侧展开的菜单 -->
            <template v-if="expandedMenus?.length > 0">
              <div
                v-for="(menu, level) in expandedMenus"
                :key="level"
                class="max-w-[200px] max-h-96 overflow-y-auto border-l px-2 border-[#6bb1c8] last:border-r-0 relative"
                @scroll="e => debouncedScroll(e, level + 1)"
              >
                <!-- 层级标题 -->
                <div class="flex items-center gap-1 p-2">
                  <span class="text-gray-700 text-xs font-bold">
                    {{ getLevelTitle(level + 2) }}
                  </span>
                  <Icon name="icon-xia" :size="14" class="flex items-center justify-center" />
                </div>

                <!-- 当前层级有数据时显示 -->
                <template v-if="menu.length > 0">
                  <div
                    v-for="option in menu"
                    :key="option.value"
                    class="flex items-center justify-between gap-1 my-0.5 transition-all duration-200"
                    @click="selectOption(option, level + 1)"
                  >
                    <div
                      class="line-clamp-1 leading-relaxed text-xs px-2 min-w-0 flex-1 rounded cursor-pointer"
                      :class="[
                        selectedPath[level + 1]?.value === option.value
                          ? 'bg-gradient-to-r from-[#00eaff]/50 to-[#00ffff]/20 text-gray-700'
                          : 'hover:bg-gradient-to-r hover:from-[#00eaff]/30 hover:to-[#00ffff]/10 text-gray-500',
                      ]"
                      :title="option.label"
                    >
                      {{ option.label }}
                    </div>
                    <div
                      v-if="getCurrentLevelOptions(level + 2).length > 0"
                      class="flex items-center p-2 flex-shrink-0 cursor-pointer transition-all duration-200 hover:bg-[#00ffff]/20 rounded"
                      :title="`展开 ${option.label} 的子选项`"
                      @click.stop="expandMenu(option, level + 1)"
                    >
                      <Icon
                        name="icon-arrow-right"
                        :size="14"
                        :color="
                          selectedPath[level + 1]?.value === option.value
                            ? 'text-gray-700'
                            : 'text-gray-400'
                        "
                      />
                    </div>
                  </div>
                </template>

                <!-- 当前层级无数据时显示 Empty -->
                <div v-else class="p-8 text-center text-gray-500">
                  <Icon name="icon-empty" :size="48" class="mx-auto mb-2" />
                  <div class="text-sm text-gray-400">暂无数据</div>
                </div>
              </div>
            </template>
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

/* 多行文本截断 */
.line-clamp-1 {
  height: 28px;
  line-height: 28px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 文本省略号 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
