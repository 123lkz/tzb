<script setup lang="ts">
import ThirdTitleHeader from '~/components/ThirdTitleHeader.vue'
import DoughnutChart from '~/components/Echart/DoughnutChart.vue'
import DoubleBarChart from '~/components/Echart/DoubleBarChart.vue'

const props = defineProps<{
  schoolData: { value: number; name: string }[]
  schoolStudentData: { value: number; name: string }[]
  totalGraduateData: { year: string; doubleHigh: number; nonDoubleHigh: number }[]
  height: number
}>()

// 定义tab类型
type TabType = 'students' | 'schools' | 'graduates'

// 当前选中的tab
const activeTab = ref<TabType>('students')
let timer: number | null = null

// tab配置
const tabs = [
  { key: 'students', label: '在校学生数' },
  { key: 'graduates', label: '毕业生数' },
  { key: 'schools', label: '学校数' },
]

const resetTimer = () => {
  if (timer) clearInterval(timer)
  timer = window.setInterval(() => {
    autoSwitchTab()
  }, 5000)
}

const pauseTimer = () => {
  if (timer) clearInterval(timer)
}

const autoSwitchTab = () => {
  const idx = tabs.findIndex(tab => tab.key === activeTab.value)
  const nextIdx = (idx + 1) % tabs.length
  activeTab.value = tabs[nextIdx].key as TabType
  resetTimer()
}

const switchTab = (tab: TabType) => {
  activeTab.value = tab
  resetTimer()
}

onMounted(() => {
  resetTimer()
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div
    class="relative w-full h-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 shadow-md flex flex-col justify-center items-center"
    :style="{ height: props.height }"
    @mouseenter="pauseTimer"
    @mouseleave="resetTimer"
  >
    <!-- 标题和Tab区域 -->
    <div class="flex items-center justify-between w-full">
      <ThirdTitleHeader title="大专院校统计(2022年)" size="xs" />
      <!-- Tab按钮 -->
      <div class="flex items-center gap-2 absolute right-5 top-4.5 z-10">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="px-1.5 py-1 text-xs"
          :class="[
            activeTab === tab.key
              ? 'text-blue-50 font-medium'
              : 'text-gray-400  hover:text-blue-100',
          ]"
          @click="switchTab(tab.key as TabType)"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>
    <!-- 图表展示区域 -->
    <div
      class="w-full h-full relative z-10 flex items-center justify-center"
      @mouseenter="pauseTimer"
      @mouseleave="resetTimer"
    >
      <DoughnutChart
        v-if="activeTab === 'students'"
        :data="schoolStudentData"
        title="在校学生数"
        height="170px"
        quantifier="人"
        :colors="['#FAC858', '#EE6666']"
      />
      <DoubleBarChart
        v-if="activeTab === 'graduates'"
        :data="totalGraduateData"
        height="170px"
        unit="万"
        quantifier="人"
        tooltip-title="年双高/非双高院校毕业生数"
      />
      <DoughnutChart
        v-if="activeTab === 'schools'"
        :data="schoolData"
        title="学校总数"
        height="170px"
        quantifier="所"
        :colors="['#5470C6', '#91CC75']"
      />
    </div>
  </div>
</template>

<style scoped>
/* Tab按钮悬停效果 */
button:hover {
  transform: translateY(-1px);
}

/* 活跃tab的发光效果 */
button:has(.active) {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}
</style>
