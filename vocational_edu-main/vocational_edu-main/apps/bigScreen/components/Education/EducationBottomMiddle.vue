<script setup lang="ts">
import HotWordCloud, { type DataItem } from '../Echart/HotWordCloud.vue'

const props = defineProps<{
  hotProfessionData: DataItem[]
  highSalaryMajorData: DataItem[]
}>()

const isHotProfessionCloud = ref(true)
let timer: number | null = null

const resetTimer = () => {
  if (timer) clearInterval(timer)
  timer = window.setInterval(() => {
    toggleCloud()
  }, 5000)
}

const toggleCloud = () => {
  isHotProfessionCloud.value = !isHotProfessionCloud.value
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
    class="relative w-full h-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 shadow-md flex flex-col items-center"
    @mouseenter="pauseTimer"
    @mouseleave="resetTimer"
  >
    <!-- 标题和Tab区域 -->
    <div class="flex items-center justify-between w-full relative z-10">
      <ThirdTitleHeader title="标准职业对应专业词云图" />
      <!-- Tab按钮 -->
      <div class="flex items-center gap-1 absolute right-0 top-4.5 z-10">
        <button
          class="flex items-center px-2 py-1.5 rounded text-xs font-medium transition"
          :class="
            isHotProfessionCloud
              ? 'bg-[#00ffff]/30 text-white shadow-sm'
              : 'text-gray-400 hover:bg-[#00ffff]/20 hover:text-gray-50'
          "
          @click="
            () => {
              if (!isHotProfessionCloud) {
                isHotProfessionCloud = true
                resetTimer()
              }
            }
          "
        >
          热门职业
        </button>
        <!-- 经验要求 Tab -->
        <button
          class="flex items-center px-2 py-1.5 rounded text-xs font-medium transition"
          :class="
            !isHotProfessionCloud
              ? 'bg-[#00ffff]/30 text-white shadow-sm'
              : 'text-gray-400 hover:bg-[#00ffff]/20 hover:text-gray-50'
          "
          @click="
            () => {
              if (isHotProfessionCloud) {
                isHotProfessionCloud = false
                resetTimer()
              }
            }
          "
        >
          高薪职业
        </button>
      </div>
    </div>
    <!-- 云图展示区域 -->
    <div
      class="w-full h-full absolute top-4 bottom-4 left-0 right-8 flex items-center justify-start pl-4"
    >
      <transition name="slide-fade" mode="out-in">
        <HotWordCloud
          v-if="isHotProfessionCloud"
          key="hotProfession"
          tooltip-title="热门标准职业"
          :data="props.hotProfessionData"
          :width="340"
          :height="160"
        />
        <HotWordCloud
          v-else
          key="highSalaryMajor"
          tooltip-title="高薪标准职业"
          :data="props.highSalaryMajorData"
          :width="340"
          :height="160"
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
