<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  data: {
    type: Array as PropType<
      Array<{
        title: string
        value: number
        changeRate?: number
        children?: Array<{
          title: string
          value: number
          changeRate?: number
        }>
      }>
    >,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
  title: String,
  unit: String,
  dialogTitle: String,
  pageSize: {
    type: Number,
    default: 10,
  },
  autoRotate: {
    type: Boolean,
    default: true,
  },
  rotateInterval: {
    type: Number,
    default: 8000,
  },
  fetchJobTitles: {
    type: Function as PropType<(title: string) => Array<{ name: string; value: number }>>,
    default: null,
  },
})

const emit = defineEmits(['page-change'])

const currentPage = ref(1)
let rotateTimer: NodeJS.Timeout | null = null

const showDialog = ref(false)
const dialogTitle = ref('')
const dialogData = ref<Array<{ name: string; value: number }>>([])

const nextPage = () => {
  const newPage = currentPage.value >= props.total ? 1 : currentPage.value + 1
  currentPage.value = newPage
  emit('page-change', newPage)
}

const prevPage = () => {
  const newPage = currentPage.value <= 1 ? props.total : currentPage.value - 1
  currentPage.value = newPage
  emit('page-change', newPage)
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= props.total) {
    currentPage.value = page
    emit('page-change', page)
  }
}

const startAutoRotate = () => {
  if (props.autoRotate !== false && props.total > 1) {
    rotateTimer = setInterval(() => {
      nextPage()
    }, props.rotateInterval || 8000)
  }
}

const stopAutoRotate = () => {
  if (rotateTimer) {
    clearInterval(rotateTimer)
    rotateTimer = null
  }
}

const handleIndustryClick = (title: string) => {
  if (!props.fetchJobTitles) {
    return
  }
  stopAutoRotate()
  dialogTitle.value = `${title} - ${props.dialogTitle || ''}`
  dialogData.value = props.fetchJobTitles(title).sort((a, b) => b.value - a.value)
  showDialog.value = true
}

onMounted(() => {
  startAutoRotate()
})

onUnmounted(() => {
  stopAutoRotate()
})
</script>

<template>
  <div
    class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 h-full flex flex-col"
  >
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">{{ title }}</h2>
      <span v-if="unit" class="text-sm opacity-70">{{ unit }}</span>
    </div>

    <div class="space-y-3">
      <div
        v-for="(item, index) in data"
        :key="index"
        class="flex items-center p-3 bg-gradient-to-r from-[#00ffff]/10 to-[#00ffff]/0 hover:from-[#00ffff]/20 cursor-pointer rounded-lg transition-all"
        @click="handleIndustryClick(item.title)"
      >
        <span class="w-8 text-right mr-3 font-mono"
          >{{ (currentPage - 1) * pageSize + index + 1 }}.</span
        >
        <span class="flex-grow truncate" :title="item.title">{{ item.title }}</span>
        <span class="font-mono">{{ item.value.toLocaleString() }}</span>
        <span
          v-if="item.changeRate !== undefined"
          class="ml-3 text-xs px-2 py-1 rounded-full"
          :class="{
            'bg-green-900/30 text-green-400': item.changeRate > 0,
            'bg-red-900/30 text-red-400': item.changeRate < 0,
          }"
        >
          {{ item.changeRate > 0 ? `↑${item.changeRate}%` : `↓${Math.abs(item.changeRate)}%` }}
        </span>
      </div>
    </div>

    <div v-if="total > 1" class="flex justify-center mt-3 space-x-1">
      <button
        v-for="page in Math.min(5, total)"
        :key="page"
        class="w-6 h-6 rounded text-sm transition-colors"
        :class="{
          'bg-blue-500 text-white': page === currentPage,
          'hover:bg-white/20 text-white': page !== currentPage,
        }"
        @click="goToPage(page)"
        @mouseenter="stopAutoRotate"
        @mouseleave="startAutoRotate"
      >
        {{ page }}
      </button>
      <span v-if="total > 5" class="px-1 text-white/50">...</span>
    </div>

    <!-- 对话框 -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="showDialog"
          class="fixed inset-0 flex items-center justify-center z-50 bg-black/30 backdrop-blur py-20"
          @click.self="
            () => {
              showDialog = false
              startAutoRotate()
            }
          "
        >
          <div
            class="px-10 bg-[#140222]/70 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.7)] border border-[#00ffff]/80 h-full flex flex-col"
          >
            <div
              class="flex justify-between items-center mb-4 sticky top-0 bg-blue-900/50 p-2 rounded-lg backdrop-blur-sm"
            >
              <h3 class="text-lg font-bold">{{ dialogTitle }}</h3>
              <button
                class="text-white/70 hover:text-white"
                @click="
                  () => {
                    showDialog = false
                    startAutoRotate()
                  }
                "
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <div class="space-y-4">
              <div
                v-for="(job, index) in dialogData"
                :key="index"
                class="flex items-center justify-between p-3 bg-gradient-to-r from-[#00ffff]/20 to-[#00ffff]/0 hover:from-[#00ffff]/20 rounded-lg transition-all"
              >
                <div class="flex items-center">
                  <span class="w-6 text-right mr-3 font-mono">{{ index + 1 }}.</span>
                  <span>{{ job.name }}</span>
                </div>
                <span class="font-mono text-[#00ffff] ml-20">{{ job.value.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
