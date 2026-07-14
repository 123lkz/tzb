<script setup lang="ts">
interface SalaryData {
  name: string
  value: number
  unit: string
}

interface Props {
  title?: string
  data?: SalaryData[]
}

const props = withDefaults(defineProps<Props>(), {
  title: '招聘平台职位个数',
  data: () => [
    { name: '智联招聘', value: 3500, unit: '条' },
    { name: 'Boss直聘', value: 4500, unit: '条' },
    { name: '58同城', value: 6500, unit: '条' },
    { name: '前程无忧', value: 8500, unit: '条' },
    { name: '拉勾网', value: 10500, unit: '条' },
    { name: '猎聘网', value: 12500, unit: '条' },
  ],
})

// 格式化数字
const formatNumber = (num: number): string => {
  return num.toLocaleString()
}

// 每行的颜色配置
const rowColors = [
  'text-red-200',
  'text-green-200',
  'text-orange-200',
  'text-sky-200',
  'text-amber-200',
  'text-lime-200',
]

// 平台图标映射
const platformIcons = {
  智联招聘: '🔗',
  Boss直聘: '💼',
  '58同城': '🏢',
  前程无忧: '📋',
  拉勾网: '🎯',
  猎聘网: '🎖️',
}
</script>

<template>
  <div
    class="w-full border border-[#00ffff]/40 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg relative mt-2 shadow-[inset_0_0_15px_rgba(0,255,255,0.1)]"
  >
    <!-- 顶部标题区域 -->
    <div
      class="flex items-center justify-center bg-[#18102d] absolute -top-3 left-1/2 -translate-x-1/2 w-3/4 z-10"
    >
      <!-- 左侧装饰圆点 -->
      <div class="absolute left-0 w-2 h-2 bg-[#00ffff]/60 rounded-full"></div>

      <!-- 标题文本 -->
      <div class="z-10 text-base font-bold text-[#00ffff]/90 text-sm">
        {{ title }}
      </div>

      <!-- 右侧装饰圆点 -->
      <div class="absolute right-0 w-2 h-2 bg-[#00ffff]/60 rounded-full"></div>
    </div>

    <!-- 内容区域 -->
    <div class="px-4 py-4 space-y-3">
      <div
        v-for="(item, index) in data"
        :key="index"
        :class="[
          'flex justify-between items-center rounded-md font-medium transition-all duration-300 hover:translate-x-1 hover:shadow-lg',
          rowColors[index],
        ]"
      >
        <!-- 左侧标签 -->
        <div class="text-sm" :class="rowColors[index]">
          {{ item.name }}
        </div>

        <!-- 右侧数值 -->
        <div class="flex items-center gap-1">
          <span class="text-base font-bold font-DIN-Medium" :class="rowColors[index]">
            {{ formatNumber(item.value) }}
          </span>
          <span class="text-xs" :class="rowColors[index]">
            {{ item.unit }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
