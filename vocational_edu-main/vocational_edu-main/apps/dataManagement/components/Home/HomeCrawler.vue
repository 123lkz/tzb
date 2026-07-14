<script setup lang="ts">
import Icon from '../common/Icon.vue'
import HomeBottomLeftCard from './HomeBottomCard.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

const mockData1 = [
  {
    name: '2024-08',
    value: 12580,
  },
  {
    name: '2024-09',
    value: 14500,
  },
  {
    name: '2024-10',
    value: 8000,
  },
  {
    name: '2024-11',
    value: 11000,
  },
  {
    name: '2024-12',
    value: 12000,
  },
  {
    name: '2025-01',
    value: 15000,
  },
  {
    name: '2025-02',
    value: 6000,
  },
  {
    name: '2025-03',
    value: 10000,
  },
  {
    name: '2025-04',
    value: 7500,
  },
  {
    name: '2025-05',
    value: 9000,
  },
  {
    name: '2025-06',
    value: 17500,
  },
  {
    name: '2025-07',
    value: 18000,
  },
]

const mockData2 = [
  {
    name: '2024-08',
    value: 8500,
  },
  {
    name: '2024-09',
    value: 12000,
  },
  {
    name: '2024-10',
    value: 12500,
  },
  {
    name: '2024-11',
    value: 10000,
  },
  {
    name: '2024-12',
    value: 7000,
  },
  {
    name: '2025-01',
    value: 11000,
  },
  {
    name: '2025-02',
    value: 8000,
  },
  {
    name: '2025-03',
    value: 7000,
  },
  {
    name: '2025-04',
    value: 12500,
  },
  {
    name: '2025-05',
    value: 13000,
  },
  {
    name: '2025-06',
    value: 6000,
  },
  {
    name: '2025-07',
    value: 14000,
  },
]

const totalPlatforms = ref(6)
const { formattedValue, animateNumber, resetToZero } = useNumberAnimation()

// 监听 value 变化，触发动画
watch(
  () => totalPlatforms.value,
  (newValue: number) => {
    animateNumber(newValue, 1000, true) // 确保从0开始
  },
  { immediate: true }
)

// 组件挂载后确保从0开始动画
onMounted(() => {
  resetToZero() // 先重置到0
  // 延迟一点时间确保组件完全渲染后再开始动画
  setTimeout(() => {
    animateNumber(6, 1000, true)
  }, 200)
})
</script>

<template>
  <div
    class="w-full h-full text-white bg-white/5 border border-white/10 rounded-lg px-4 py-3 shadow-md"
  >
    <div class="grid grid-cols-11 gap-4 h-full">
      <!-- 左侧区域 -->
      <div class="col-span-3 flex flex-col items-center justify-center gap-1.5 relative h-full">
        <!-- 第一个图标 - 0度 -->
        <div class="transform rotate-180 absolute top-0 left-0 w-full opacity-50">
          <Icon name="icon-yuanhu-" width="100%" height="20px" color="#00ffff" />
        </div>
        <div class="text-[#00ffff]/80">爬虫数据概览</div>
        <!-- 副标题 -->
        <div class="flex items-center gap-1 text-sm">
          <span class="text-[#00ffff]">招聘平台总个数</span>
          <span
            class="text-[#00ffff] font-DIN-Medium w-6 h-6 inline-flex items-center justify-center rounded-md bg-[#00ffff]/20"
            >{{ formattedValue }}</span
          >
          <span class="text-xs text-[#00ffff]">个</span>
        </div>
        <!-- 第二个图标 - 180度 -->
        <div class="transform rotate-0 absolute bottom-0 left-0 w-full opacity-50">
          <Icon name="icon-yuanhu-" width="100%" height="20px" color="#00ffff" />
        </div>
      </div>

      <!-- 中间内容区域 -->
      <div class="col-span-4">
        <HomeBottomLeftCard
          icon="icon-liebiao"
          title="职位列表总个数"
          :value="8500"
          indicator-desc="职位列表总个数"
          quantifier="条"
          chart-height="50px"
          :chart-data="mockData1"
          :change-rate="-3.2"
          change-label="较上周"
          :color="'#00DDFF'"
        />
      </div>

      <!-- 右侧占位区域 -->
      <div class="col-span-4">
        <HomeBottomLeftCard
          icon="icon-xiangqing"
          title="职位详情总个数"
          :value="8500"
          indicator-desc="职位列表总个数"
          quantifier="条"
          chart-height="50px"
          :chart-data="mockData2"
          :change-rate="12.2"
          change-label="较上周"
          :color="'#FF0087'"
        />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
