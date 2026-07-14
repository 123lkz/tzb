<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import Icon from './Icon.vue'
import Search from './Search/Search.vue'

// 过滤项接口定义
interface FilterOption {
  label: string
  value: string | number
}

// 列定义接口
interface Column {
  key: string
  title: string
  width?: string | number
  minWidth?: string | number
  maxWidth?: string | number
  fixed?: 'left' | 'right' | boolean
  sortable?: boolean
  formatter?: (value: any) => string
  align?: 'left' | 'center' | 'right'
  ellipsis?: boolean // 是否显示省略号
  tooltip?: boolean // 是否显示tooltip
  hidden?: boolean
  search?:
    | boolean
    | {
        key?: string
        label?: string
        placeholder?: string
        type?: 'input' | 'select'
        options?: FilterOption[]
      }
}

interface FilterItem {
  key: string
  label: string
  placeholder?: string
  type: 'input' | 'select'
  options?: FilterOption[]
}

// 组件属性
interface Props {
  title?: string
  titleIcon?: string
  columns: Column[]
  data: any[]
  pageSize?: number
  searchable?: boolean
  sortable?: boolean
  loading?: boolean
  error?: boolean
  onReload?: () => void
  // 分页信息
  total?: number
  totalPages?: number
  currentPage?: number
  hasNext?: boolean
  hasPrev?: boolean
  // 导出功能
  exportable?: boolean
  exportLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  titleIcon: '',
  pageSize: 20,
  searchable: true,
  sortable: true,
  loading: false,
  error: false,
  onReload: undefined,
  total: 0,
  totalPages: 0,
  currentPage: 1,
  hasNext: false,
  hasPrev: false,
  exportable: true,
  exportLoading: false
})

// 定义事件
const emit = defineEmits<{
  search: [data: Record<string, any>]
  reset: []
  add: []
  export: []
  'name-click': [row: any]
  sort: [field: string, order: 'asc' | 'desc']
  'page-change': [page: number]
}>()

// 响应式数据
const localCurrentPage = ref(1)
const pageSize = ref(props.pageSize)
const sortField = ref('')
const sortOrder = ref<'asc' | 'desc'>('asc')
const tableContainer = ref<HTMLElement>()
const tableHeader = ref<HTMLElement>()
const tableBody = ref<HTMLElement>()

// 动态宽度计算
const containerRef = ref<HTMLElement>()
const tableContainerWidth = ref('100%')
const windowWidth = ref(0)
let resizeTimer: NodeJS.Timeout | null = null

const filterLength = computed(() => {
  if (props.columns?.length) {
    return props.columns.filter((column) => column.search).length
  }
  return 0
})

// 计算属性 - 现在直接使用传入的数据，搜索和排序由父组件处理
const filteredData = computed(() => {
  return props.data || []
})

// 使用服务端返回的分页信息
const totalPages = computed(() => props.totalPages || Math.ceil(filteredData.value.length / pageSize.value))
const total = computed(() => props.total || filteredData.value.length)
const currentPageValue = computed(() => props.currentPage || localCurrentPage.value)

const startIndex = computed(() => (currentPageValue.value - 1) * pageSize.value)
const endIndex = computed(() => Math.min(startIndex.value + pageSize.value, total.value))

// 如果有服务端分页，直接使用传入的数据；否则使用本地分页
const paginatedData = computed(() => {
  if (props.total && props.totalPages) {
    // 服务端分页，直接使用传入的数据
    return filteredData.value
  }
  // 本地分页
  return filteredData.value.slice(startIndex.value, endIndex.value)
})

const visiblePages = computed(() => {
  const pages: number[] = []
  const maxVisible = 5
  const halfVisible = Math.floor(maxVisible / 2)

  let start = Math.max(1, currentPageValue.value - halfVisible)
  const end = Math.min(totalPages.value, start + maxVisible - 1)

  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

const visibleColumns = computed(() => {
  return props.columns.filter((column) => column.key)
})

// 计算表格容器宽度
const calculateTableWidth = () => {
  // 使用窗口宽度而不是容器宽度
  const windowWidthValue = window.innerWidth
  const leftMenuWidth = 240 // 左侧菜单宽度
  const padding = 32 // 页面内边距
  const availableWidth = windowWidthValue - leftMenuWidth - padding

  // 根据屏幕宽度动态调整
  if (windowWidthValue < 768) {
    // 小屏幕：使用100%宽度
    tableContainerWidth.value = '100%'
  } else if (windowWidthValue < 1200) {
    // 中等屏幕：使用计算出的宽度，但确保最小宽度
    tableContainerWidth.value = `${Math.max(availableWidth, 800)}px`
  } else {
    // 大屏幕：使用计算出的宽度，但确保最小宽度
    tableContainerWidth.value = `${Math.max(availableWidth, 1000)}px`
  }
}

// 防抖的 resize 处理函数
const debouncedResize = () => {
  if (resizeTimer) {
    clearTimeout(resizeTimer)
  }
  resizeTimer = setTimeout(() => {
    handleResize()
  }, 150)
}

// 处理窗口大小变化
const handleResize = () => {
  windowWidth.value = window.innerWidth
  calculateTableWidth()
}

// 方法

const handleSort = (column: Column) => {
  if (!column.sortable) return

  let newOrder: 'asc' | 'desc' = 'asc'
  if (sortField.value === column.key) {
    newOrder = sortOrder.value === 'asc' ? 'desc' : 'asc'
  }

  sortField.value = column.key
  sortOrder.value = newOrder

  // 触发排序事件给父组件
  emit('sort', column.key, newOrder)
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    if (props.total && props.totalPages) {
      // 服务端分页，触发事件给父组件
      emit('page-change', page)
    } else {
      // 本地分页，直接更新当前页
      localCurrentPage.value = page
    }
  }
}

// const handlePageSizeChange = () => {
//   currentPage.value = 1
// }

// 滚动同步功能已移除，现在使用统一的滚动容器

const getColumnStyle = (column: Column) => {
  const style: any = {}

  if (column.width) {
    // 如果设置了固定宽度，使用固定宽度
    style.width = typeof column.width === 'number' ? `${column.width}px` : column.width
    style.minWidth = style.width
    style.maxWidth = style.width
    style.flexShrink = 0
  } else {
    // 如果没有设置宽度，使用默认最小宽度
    style.minWidth = column.minWidth
      ? typeof column.minWidth === 'number'
        ? `${column.minWidth}px`
        : column.minWidth
      : '120px'
    style.maxWidth = column.maxWidth
      ? typeof column.maxWidth === 'number'
        ? `${column.maxWidth}px`
        : column.maxWidth
      : 'none'
    style.flex = '1'
  }

  if (column.align) {
    style.textAlign = column.align
  }

  // 如果设置了ellipsis，添加文本溢出样式
  if (column.ellipsis !== false) {
    style.overflow = 'hidden'
    style.textOverflow = 'ellipsis'
    style.whiteSpace = 'nowrap'
  }

  return style
}

const formatCellValue = (value: any, column: Column) => {
  if (column.formatter) {
    return column.formatter(value)
  }

  if (value === null || value === undefined) {
    return '-'
  }

  return String(value)
}

// 检测值是否为链接
const isLink = (value: any): boolean => {
  if (!value || typeof value !== 'string') return false
  const urlPattern = /^(https?:\/\/|www\.)[\w-]+(\.[\w-]+)+([\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?$/i
  return urlPattern.test(value.trim())
}

// 处理链接点击事件
const handleLinkClick = (url: string) => {
  let finalUrl = url.trim()
  // 如果链接没有协议，添加 https://
  if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
    finalUrl = 'https://' + finalUrl
  }
  // 在新标签页中打开链接
  window.open(finalUrl, '_blank', 'noopener,noreferrer')
}

// 监听数据变化，重置分页
watch(
  () => props.data,
  () => {
    localCurrentPage.value = 1
  },
  { deep: true }
)

// 搜索关键词监听已移除，现在由父组件处理搜索逻辑

// 数据变化监听已简化，现在使用统一的滚动容器

// 组件挂载
onMounted(() => {
  windowWidth.value = window.innerWidth
  calculateTableWidth()

  // 监听窗口大小变化
  window.addEventListener('resize', debouncedResize, { passive: true })
})

// 组件卸载时清理
onBeforeUnmount(() => {
  window.removeEventListener('resize', debouncedResize)
  if (resizeTimer) {
    clearTimeout(resizeTimer)
  }
})

// 从 columns 动态生成 filterConfig
const filterConfig = computed<FilterItem[]>(() => {
  return props.columns
    .filter((column) => column.search)
    .map((column) => {
      if (typeof column.search === 'boolean') {
        // 如果 search 是 true，使用默认配置
        return {
          key: column.key,
          label: column.title,
          placeholder: `请输入${column.title}`,
          type: 'input' as const
        }
      } else if (column.search) {
        // 如果 search 是对象，使用自定义配置
        const searchType = column.search.type || 'input'
        const defaultPlaceholder = searchType === 'select' ? `请选择${column.title}` : `请输入${column.title}`
        return {
          key: column.search.key || column.key,
          label: column.search.label || column.title,
          placeholder: column.search.placeholder || defaultPlaceholder,
          type: searchType,
          options: column.search.options
        }
      }
      // 这里不应该到达，但为了类型安全
      return {
        key: column.key,
        label: column.title,
        placeholder: `请输入${column.title}`,
        type: 'input' as const
      }
    })
})

const searchForm = ref({})

const handleSearch = (formData: Record<string, any>) => {
  // 将搜索数据传递给父组件
  emit('search', formData)
}

const handleReset = () => {
  // 重置搜索表单
  searchForm.value = {}
  // 触发重置事件给父组件
  emit('reset')
}

// 新增按钮处理
const handleAdd = () => {
  emit('add')
}

// 导出按钮处理
const handleExport = () => {
  emit('export')
}

// 处理名称点击事件
const handleNameClick = (row: any) => {
  // 发射事件给父组件处理
  window.open(`/position-detail/${row.id}`, '_blank')
  emit('name-click', row)
}
</script>

<template>
  <div ref="containerRef" class="w-full h-full flex flex-col">
    <Search v-model="searchForm" :filters="filterConfig" @search="handleSearch" @reset="handleReset" />
    <div class="flex items-center justify-between mb-4">
      <div class="font-bold text-[#00ffff]/80">{{ title }}</div>
      <div class="flex items-center gap-3">
        <!-- <button
          class="px-3 py-1 text-sm bg-[#00ffff]/20 border border-[#00ffff]/40 rounded-md text-[#00ffff] hover:bg-[#00ffff]/30 hover:border-[#00ffff]/60 focus:outline-none focus:ring-2 focus:ring-[#00ffff]/50 transition-all duration-200 flex items-center gap-2"
          @click="handleAdd"
        >
          <Icon name="icon-a-fangda2" size="16" />
          新增
        </button> -->
        <button
          v-if="exportable"
          :disabled="exportLoading || loading"
          class="px-3 py-1 text-sm bg-green-500/20 border border-green-500/40 rounded-md text-green-400 hover:bg-green-500/30 hover:border-green-500/60 focus:outline-none focus:ring-2 focus:ring-green-500/50 transition-all duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="handleExport"
        >
          <div v-if="exportLoading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-green-400"></div>
          <Icon v-else name="icon-file-excel-fill" size="16" />
          {{ exportLoading ? '导出中...' : '导出' }}
        </button>
      </div>
    </div>
    <div
      class="w-full relative overflow-hidden rounded-lg border border-[#00ffff]/10 bg-[#00ffff]/5"
      :style="{
        height: `calc(100% - 4rem - ${filterLength > 4 ? '176px' : '126px'})`
      }"
    >
      <div
        ref="tableContainer"
        class="overflow-auto h-full custom-scrollbar"
        style="scrollbar-width: thin; scrollbar-color: rgba(0, 255, 255, 0.6) rgba(0, 255, 255, 0.1)"
      >
        <!-- 表头区域 - 固定位置 -->
        <div
          ref="tableHeader"
          class="sticky top-0 z-20 bg-[#1f2842] border-b border-[#00ffff]/10"
          :style="{
            minWidth: `${
              50 +
              visibleColumns.reduce(
                (total, col) =>
                  total + (col.width ? (typeof col.width === 'number' ? col.width : parseInt(col.width)) : 120),
                0
              )
            }px`
          }"
        >
          <div class="flex">
            <div
              :class="[
                'text-[#00ffff]/80 font-medium text-xs sm:text-sm px-2 sm:px-4 py-2 sm:py-3 text-left whitespace-nowrap flex-shrink-0'
              ]"
              :style="{ width: '50px', minWidth: '50px' }"
            >
              #
            </div>
            <template v-for="column in visibleColumns" :key="column.key">
              <div
                v-if="!column.hidden"
                :class="[
                  'text-[#00ffff]/80 font-medium text-xs sm:text-sm px-2 sm:px-4 py-2 sm:py-3 text-left',
                  column.fixed === 'left' ? 'sticky left-[50px] z-[5]' : '',
                  column.fixed === 'right' ? 'sticky right-0 z-[5]' : '',
                  column.sortable ? 'cursor-pointer hover:bg-[#00ffff]/15 transition-colors' : '',
                  column.ellipsis !== false ? 'whitespace-nowrap' : ''
                ]"
                :style="getColumnStyle(column)"
                @click="handleSort(column)"
              >
                <div class="flex items-center justify-between min-w-0">
                  <span class="truncate flex-1">{{ column.title }}</span>
                  <div v-if="column.sortable" class="flex flex-col ml-2 flex-shrink-0">
                    <Icon
                      name="icon-arrow-up"
                      size="12"
                      :color="sortField === column.key && sortOrder === 'asc' ? '#00ffff' : 'rgba(255, 255, 255, 0.4)'"
                      class="transition-colors"
                    />
                    <Icon
                      name="icon-arrow-down"
                      size="12"
                      :color="sortField === column.key && sortOrder === 'desc' ? '#00ffff' : 'rgba(255, 255, 255, 0.4)'"
                      class="transition-colors"
                    />
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- 表格内容区域 -->
        <!-- Loading 状态 -->
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-[#00ffff]/5">
          <div class="text-center">
            <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-cyan-400 mx-auto mb-6"></div>
            <p class="text-cyan-400 text-xl font-medium mb-2">正在加载数据...</p>
            <p class="text-white/60 text-sm">请稍候，正在从服务器获取最新数据</p>
          </div>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="absolute inset-0 flex items-center justify-center bg-[#00ffff]/5">
          <div class="text-center">
            <div class="text-red-400 text-4xl mb-6">⚠️</div>
            <p class="text-red-400 text-xl font-medium mb-3">加载数据时出现错误</p>
            <p class="text-white/60 text-sm mb-8">请检查网络连接或稍后重试</p>
            <button
              v-if="onReload"
              class="px-8 py-4 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors border border-cyan-500/40 font-medium"
              @click="onReload"
            >
              🔄 重新加载
            </button>
          </div>
        </div>

        <!-- 正常数据状态 -->
        <template v-else-if="paginatedData.length > 0">
          <div
            ref="tableBody"
            :style="{
              minWidth: `${
                50 +
                visibleColumns.reduce(
                  (total, col) =>
                    total + (col.width ? (typeof col.width === 'number' ? col.width : parseInt(col.width)) : 120),
                  0
                )
              }px`
            }"
          >
            <div
              v-for="(row, index) in paginatedData"
              :key="row.id || index"
              :class="['flex', index % 2 !== 0 ? 'bg-[#00ffff]/5' : 'hover:bg-white/5 transition-colors']"
            >
              <div
                :class="[
                  'px-2 sm:px-4 py-2 sm:py-3 text-white/80 text-xs sm:text-sm border-b border-[#00ffff]/5 whitespace-nowrap cursor-default flex-shrink-0'
                ]"
                :style="{ width: '50px', minWidth: '50px' }"
              >
                {{ index + 1 }}
              </div>
              <template v-for="column in visibleColumns" :key="column.key">
                <div
                  v-if="!column.hidden"
                  :class="[
                    'px-2 sm:px-4 py-2 sm:py-3 text-white/80 text-xs sm:text-sm border-b border-[#00ffff]/5 cursor-default',
                    column.fixed ? 'bg-white/5' : '',
                    column.fixed === 'left' ? 'sticky left-[50px] z-[5]' : '',
                    column.fixed === 'right' ? 'sticky right-0 z-[5]' : '',
                    column.ellipsis !== false ? 'whitespace-nowrap' : ''
                  ]"
                  :style="getColumnStyle(column)"
                  :title="
                    column.tooltip !== false && column.ellipsis !== false
                      ? formatCellValue(row[column.key], column)
                      : undefined
                  "
                >
                  <slot :name="`cell-${column.key}`" :row="row" :column="column" :value="row[column.key]">
                    <!-- 如果值是链接，渲染为可点击的链接 -->
                    <a
                      v-if="isLink(row[column.key])"
                      class="text-blue-400 hover:text-blue-300 hover:underline transition-colors cursor-pointer"
                      @click.prevent="handleLinkClick(row[column.key])"
                    >
                      查看链接
                    </a>
                    <!-- 如果是 name 列，渲染为可点击的链接 -->
                    <a
                      v-else-if="column.key === 'name' && row['link']"
                      class="text-blue-400 hover:text-blue-300 hover:underline transition-colors cursor-pointer"
                      @click.prevent="handleNameClick(row)"
                    >
                      {{ formatCellValue(row[column.key], column) }}
                    </a>
                    <!-- 其他列正常渲染 -->
                    <span v-else>
                      {{ formatCellValue(row[column.key], column) }}
                    </span>
                  </slot>
                </div>
              </template>
            </div>
          </div>
        </template>
        <!-- 暂无数据状态 -->
        <div v-else class="absolute inset-0 flex items-center justify-center bg-[#00ffff]/5">
          <div class="text-center">
            <Icon name="icon-empty" size="120" color="text-white/20" class="opacity-50 mx-auto mb-6" />
            <p class="text-white/60 text-lg font-medium">暂无数据</p>
            <p class="text-white/40 text-sm mt-2">当前没有可显示的数据</p>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mt-4 px-4">
      <!-- 分页信息 -->
      <div class="text-white/70 text-sm">显示 {{ startIndex + 1 }}-{{ endIndex }} 条，共 {{ total }} 条</div>

      <!-- 分页控件和每页条数选择 -->
      <div class="flex flex-col sm:flex-row items-center gap-4">
        <!-- 分页控件 -->
        <div class="flex items-center gap-2">
          <button
            :disabled="props.hasPrev === false || currentPageValue <= 1"
            class="px-1.5 py-0.5 bg-white/10 border border-white/20 rounded text-white/80 hover:bg-white/15 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            @click="goToPage(currentPageValue - 1)"
          >
            <Icon name="icon-arrow-left" color="text-white/80" size="16" />
          </button>

          <div class="flex items-center gap-1">
            <button
              v-for="page in visiblePages"
              :key="page"
              :class="[
                'px-3 py-0.5 border border-white/10 rounded transition-colors',
                page === currentPageValue
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'bg-white/10 text-white/80 hover:bg-white/15 hover:text-white'
              ]"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
          </div>

          <button
            :disabled="props.hasNext === false || currentPageValue >= totalPages"
            class="px-1.5 py-0.5 bg-white/10 border border-white/20 rounded text-white/80 hover:bg-white/15 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            @click="goToPage(currentPageValue + 1)"
          >
            <Icon name="icon-arrow-right" color="text-white/80" size="16" />
          </button>
        </div>

        <!-- 每页条数选择 -->
        <div class="flex items-center gap-2 text-white/70 text-sm">
          <span>每页 20 条</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(0, 255, 255, 0.1);
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(0, 255, 255, 0.6) 0%, rgba(0, 255, 255, 0.4) 100%);
  border-radius: 4px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(0, 255, 255, 0.8) 0%, rgba(0, 255, 255, 0.6) 100%);
  border-color: rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
}

.custom-scrollbar::-webkit-scrollbar-thumb:active {
  background: linear-gradient(180deg, rgba(0, 255, 255, 0.9) 0%, rgba(0, 255, 255, 0.7) 100%);
  box-shadow: 0 0 12px rgba(0, 255, 255, 0.5);
}

.custom-scrollbar::-webkit-scrollbar-corner {
  background: rgba(0, 255, 255, 0.1);
}

/* 滚动条轨道渐变效果 */
.custom-scrollbar::-webkit-scrollbar-track:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    180deg,
    rgba(0, 255, 255, 0.05) 0%,
    rgba(0, 255, 255, 0.1) 50%,
    rgba(0, 255, 255, 0.05) 100%
  );
  border-radius: 4px;
}

/* 滚动条按钮样式（如果浏览器支持） */
.custom-scrollbar::-webkit-scrollbar-button {
  display: none;
}

/* 滚动条轨道阴影效果 */
.custom-scrollbar::-webkit-scrollbar-track {
  box-shadow: inset 0 0 4px rgba(0, 255, 255, 0.1);
}

/* 滚动条thumb发光效果 */
.custom-scrollbar::-webkit-scrollbar-thumb {
  position: relative;
}

.custom-scrollbar::-webkit-scrollbar-thumb::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.2) 0%,
    rgba(0, 255, 255, 0.1) 50%,
    rgba(0, 255, 255, 0.2) 100%
  );
  border-radius: 6px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover::before {
  opacity: 1;
}
</style>
