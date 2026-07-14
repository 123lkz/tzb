<script setup lang="ts">
import ListScroll from './ListScroll.vue'
import ListChart from './ListChart.vue'
import { formatLargeNumber } from '~/utils/num'

const props = defineProps<{
  data: any[]
  height?: number
  unit: string
  tooltipTitle: string
  showCount?: number
}>()

const pageSize = ref(props.showCount || 10)
const currentPage = ref(0)
const isPaused = ref(false)
let timer: ReturnType<typeof setTimeout> | null = null

const totalPages = computed(() => {
  return Math.ceil(props.data.length / pageSize.value)
})

const pageData = computed(() => {
  const start = currentPage.value * pageSize.value
  return props.data.slice(start, start + pageSize.value)
})

function clearTimer() {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
}

function autoScroll() {
  clearTimer()
  if (isPaused.value || totalPages.value <= 1) return
  timer = setTimeout(() => {
    nextPage()
    autoScroll()
  }, 3000)
}

function nextPage() {
  if (totalPages.value <= 1) return
  currentPage.value = (currentPage.value + 1) % totalPages.value
}

function prevPage() {
  if (totalPages.value <= 1) return
  currentPage.value = (currentPage.value - 1 + totalPages.value) % totalPages.value
}

function setPageSize(size: number) {
  pageSize.value = size
  currentPage.value = 0
  autoScroll()
}

// 只监听 pageSize 和数据变化时重置 currentPage
watch([pageSize, () => props.data], () => {
  currentPage.value = 0
  autoScroll()
})

// 只监听 isPaused 控制自动滚动
watch(isPaused, () => {
  if (isPaused.value) {
    clearTimer()
  } else {
    autoScroll()
  }
})

onMounted(() => {
  autoScroll()
})
onBeforeUnmount(() => {
  clearTimer()
})

const handleMouseEnter = () => {
  isPaused.value = true
  clearTimer()
}
const handleMouseLeave = () => {
  isPaused.value = false
  autoScroll()
}
</script>

<template>
  <div
    class="mt-4 w-full h-full relative flex flex-col"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div class="flex-1 overflow-hidden">
      <Transition name="list" tag="div">
        <ListScroll
          :key="currentPage"
          :cdata="pageData"
          :limit="pageSize"
          :height="props.height || 1.65"
        >
          <template #default="{ row, index }">
            <div
              class="w-full flex items-center justify-between gap-3 px-2 cursor-help"
              :class="{
                'text-orange-400': currentPage * pageSize + index === 0,
                'text-blue-400': currentPage * pageSize + index === 1,
                'text-green-400': currentPage * pageSize + index === 2,
                'text-yellow-400': currentPage * pageSize + index === 3,
                'text-teal-400': currentPage * pageSize + index === 4,
              }"
            >
              <div class="flex items-center gap-3">
                <div class="w-4 text-xs text-center flex-grow-0 text-white/80">
                  {{ currentPage * pageSize + index + 1 }}
                </div>
                <div
                  class="w-36 overflow-hidden min-w-0 line-ellipse text-left tooltip-container whitespace-nowrap"
                  :title="`${row.name}${props.tooltipTitle}\n排名: ${
                    currentPage * pageSize + index + 1
                  }\n数值: ${formatLargeNumber(row.value, 1) + props.unit}`"
                >
                  {{ row.name }}
                </div>
              </div>
              <ListChart
                class="font-bignum whitespace-nowrap"
                :value="formatLargeNumber(row.value, 1) + props.unit"
              />
            </div>
          </template>
        </ListScroll>
      </Transition>
    </div>
    <!-- 底部分页与操作 -->
    <div class="w-full flex items-center justify-center gap-6 select-none" style="height: 2.2rem">
      <button
        :disabled="totalPages <= 1"
        class="w-8 h-6 inline-flex items-center justify-center bg-gray-700 bg-opacity-60 text-white rounded hover:bg-opacity-90 disabled:opacity-40"
        @click="prevPage"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
        >
          <polygon points="11,3 5,8 11,13" />
        </svg>
      </button>
      <span class="text-xs text-gray-400">
        {{ totalPages > 1 ? `${currentPage + 1}/${totalPages}` : '1/1' }}
      </span>
      <button
        :disabled="totalPages <= 1"
        class="w-8 h-6 inline-flex items-center justify-center bg-gray-700 bg-opacity-60 text-white rounded hover:bg-opacity-90 disabled:opacity-40"
        @click="nextPage"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
        >
          <polygon points="5,3 11,8 5,13" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(40px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-40px);
}
</style>
