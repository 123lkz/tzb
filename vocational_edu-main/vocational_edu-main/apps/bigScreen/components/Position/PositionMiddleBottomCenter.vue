<script setup lang="ts">
import DoughnutChart from '~/components/Echart/DoughnutChart.vue'
import ThirdTitleHeader from '~/components/ThirdTitleHeader.vue'

interface Props {
  isStatAll: boolean
  isStatYear: boolean
  year: number
  month: number
  experienceData: Array<{ name: string; value: number }>
  educationData: Array<{ name: string; value: number }>
}

const props = defineProps<Props>()

const title = ref('招聘要求')
const isEducation = ref(true)
let timer: number | null = null

const resetTimer = () => {
  if (timer) clearInterval(timer)
  timer = window.setInterval(() => {
    toggleCloud()
  }, 5000)
}

const toggleCloud = () => {
  isEducation.value = !isEducation.value
  resetTimer()
}

const pauseTimer = () => {
  if (timer) clearInterval(timer)
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
    class="relative flex flex-col items-center h-full flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/5 flex-1 min-h-0"
    style="height: 100%"
    @mouseenter="pauseTimer"
    @mouseleave="resetTimer"
  >
    <!-- 标题和Tab区域 -->
    <div class="flex items-center justify-between w-full">
      <ThirdTitleHeader
        :title="
          props.isStatAll
            ? props.isStatYear
              ? `${props.year}年${title}`
              : `${props.year}年${props.month}月${title}`
            : props.isStatYear
            ? `${props.year}年${title}(应届大专生)`
            : `${props.year}年${props.month}月${title}(应届大专生)`
        "
        :size="!props.isStatAll && !props.isStatYear ? 'xs' : 'sm'"
      />
      <!-- Tab按钮 -->
      <div class="flex items-center gap-1 absolute right-4 top-4.5 z-10">
        <!-- 学历要求 Tab -->
        <button
          class="flex items-center px-2 py-1.5 rounded text-xs font-medium transition"
          :class="
            isEducation
              ? 'bg-[#00ffff]/30 text-white shadow-sm'
              : 'text-gray-400 hover:bg-[#00ffff]/20 hover:text-gray-50'
          "
          @click="
            () => {
              if (!isEducation) {
                isEducation = true
                resetTimer()
              }
            }
          "
        >
          学历要求
        </button>
        <!-- 经验要求 Tab -->
        <button
          class="flex items-center px-2 py-1.5 rounded text-xs font-medium transition"
          :class="
            !isEducation
              ? 'bg-[#00ffff]/30 text-white shadow-sm'
              : 'text-gray-400 hover:bg-[#00ffff]/20 hover:text-gray-50'
          "
          @click="
            () => {
              if (isEducation) {
                isEducation = false
                resetTimer()
              }
            }
          "
        >
          经验要求
        </button>
      </div>
    </div>
    <!-- 扇形图展示区域 -->
    <div class="w-full h-full relative z-10 mt-4 flex items-center justify-center">
      <transition name="slide-fade" mode="out-in">
        <DoughnutChart
          v-if="isEducation"
          :data="props.educationData"
          tooltip-title="招聘职位学历要求"
          value-name="职位总个数"
          height="150px"
          quantifier="个"
        />
        <DoughnutChart
          v-else
          :data="props.experienceData"
          tooltip-title="招聘职位经验要求"
          value-name="职位总个数"
          height="150px"
          quantifier="个"
        />
      </transition>
    </div>
  </div>
</template>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.55, 0, 0.1, 1);
  position: absolute;
  width: 100%;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.slide-fade-enter-to {
  opacity: 1;
  transform: translateX(0);
}
.slide-fade-leave-from {
  opacity: 1;
  transform: translateX(0);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
</style>
