<script setup lang="ts">
import { computed } from 'vue'
import Icon from './Icon.vue'

// 定义接口
interface RankItem {
  name: string
  value: string | number
  rate: number
}

// 定义props
interface Props {
  data: RankItem[]
  rateTitle?: string
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  rateTitle: '',
})

// 计算最大值
const maxValue = computed(() => {
  if (props.data.length === 0) return 0
  return Math.max(...props.data.map(item => Number(item.value)))
})

// 按数值排序的数据
const sortedData = computed(() => {
  return [...props.data].sort((a, b) => Number(b.value) - Number(a.value))
})

// 获取百分比
const getPercentage = (value: string | number): number => {
  if (maxValue.value === 0) return 0
  return (Number(value) / maxValue.value) * 100
}

// 获取进度条颜色
const getBarColor = (index: number): string => {
  const colors = [
    'bg-gradient-to-r from-red-400 to-red-500',
    'bg-gradient-to-r from-green-400 to-green-500',
    'bg-gradient-to-r from-pink-400 to-pink-500',
    'bg-gradient-to-r from-blue-400 to-blue-500',
    'bg-gradient-to-r from-orange-400 to-orange-500',
    'bg-gradient-to-r from-purple-400 to-purple-500',
    'bg-gradient-to-r from-yellow-400 to-yellow-500',
    'bg-gradient-to-r from-indigo-400 to-indigo-500',
  ]
  return colors[index % colors.length]
}

// 获取进度条颜色
const getTextColor = (index: number): string => {
  const colors = [
    'text-red-400',
    'text-green-400',
    'text-pink-400',
    'text-blue-400',
    'text-orange-400',
    'text-purple-400',
    'text-yellow-400',
    'text-indigo-400',
  ]
  return colors[index % colors.length]
}

// 获取变化率图标
const getRateIcon = (rate: number): string => {
  if (rate > 0) {
    return 'icon-shang' // 上升图标
  } else if (rate < 0) {
    return 'icon-xia' // 下降图标
  } else {
    return ''
  }
}

// 获取变化率颜色
const getRateColor = (rate: number): string => {
  if (rate > 0) {
    return 'text-green-400'
  } else if (rate < 0) {
    return 'text-red-400'
  } else {
    return 'text-gray-400'
  }
}

// 获取变化率显示文本
const getRateText = (rate: number): string => {
  if (rate > 0) {
    return '+' + rate + '%'
  } else if (rate < 0) {
    return rate + '%'
  } else {
    return '0%'
  }
}
</script>

<template>
  <div class="w-full space-y-3">
    <div
      v-for="(item, index) in sortedData"
      :key="index"
      class="flex items-center justify-between w-full h-8"
    >
      <!-- 左侧名称 -->
      <div class="flex-shrink-0 w-14 mr-3">
        <span class="text-xs text-white truncate block">{{ item.name }}</span>
      </div>

      <!-- 中间进度条区域 -->
      <div class="flex-1 flex items-center mr-3">
        <!-- 进度条背景 -->
        <div class="w-full h-2 bg-gray-400/20 rounded-full overflow-hidden">
          <!-- 进度条 -->
          <div
            class="h-full rounded-full transition-all duration-500 ease-out"
            :class="getBarColor(index)"
            :style="{ width: getPercentage(item.value) + '%' }"
          ></div>
        </div>
      </div>

      <!-- 右侧数值 -->
      <div class="flex-shrink-0 mr-2">
        <span class="text-sm font-DIN-Medium" :class="getTextColor(index)">
          {{ item.value }}个
        </span>
      </div>

      <!-- 变化率 -->
      <div class="flex-shrink-0 w-[85px] flex items-center justify-start overflow-hidden">
        <span class="text-xs text-gray-400 whitespace-nowrap mr-1">{{ rateTitle }}</span>
        <div class="flex items-center gap-1">
          <!-- 变化率图标或横线 -->
          <span
            v-if="item.rate === 0"
            class="inline-block w-2 h-1 bg-gray-400 ml-[1px] mr-[2px]"
          ></span>
          <Icon v-else :name="getRateIcon(item.rate)" :color="getRateColor(item.rate)" :size="12" />
          <!-- 变化率文本 -->
          <span class="text-xs font-DIN-Medium" :class="getRateColor(item.rate)">
            {{ getRateText(item.rate) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
