<script setup lang="ts">
import { h } from 'vue'
import Icon from '../common/Icon.vue'
import HomeTopLeftCard from './HomeTopLeftCard.vue'

interface StatisticsItem {
  title: string
  value: number
  unit: string
  trend: number // 变化百分比
  period: string // 对比周期
}

interface Props {
  title?: string
  data?: StatisticsItem[]
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [
    { title: '招聘职位总个数', value: 45600, unit: '个', trend: 8.7, period: '较上月' },
    { title: '招聘需求总人数', value: 125000, unit: '人', trend: 12.5, period: '较上月' },
    { title: '招聘单位总数量', value: 8500, unit: '家', trend: -2.3, period: '较上月' },
    { title: '招聘标准行业总个数', value: 156, unit: '个', trend: 1.2, period: '较上月' },
    { title: '招聘标准职业总个数', value: 2340, unit: '个', trend: 15.8, period: '较上月' },
  ],
})

// 格式化数字
const formatNumber = (num: number): string => {
  return num.toLocaleString()
}

// 获取趋势信息
const getTrendInfo = (trend: number) => {
  if (trend > 0) {
    return {
      icon: '↗',
      color: 'text-green-400',
      text: `+${trend.toFixed(1)}%`,
    }
  } else if (trend < 0) {
    return {
      icon: '↘',
      color: 'text-red-400',
      text: `${trend.toFixed(1)}%`,
    }
  } else {
    return {
      icon: '→',
      color: 'text-gray-400',
      text: '0.0%',
    }
  }
}

const JobIcon = h(Icon, {
  name: 'icon-gangwei',
  size: 16,
  color: 'text-cyan-500',
})

const PersonIcon = h(Icon, {
  name: 'icon-hrcollegepeopleCardingRange',
  size: 16,
  color: 'text-amber-500',
})

const CompanyIcon = h(Icon, {
  name: 'icon-gongsi',
  size: 16,
  color: 'text-blue-500',
})

// 图表数据
const barChartData = [
  { name: '1月', value: 1200 },
  { name: '2月', value: 1400 },
  { name: '3月', value: 1600 },
  { name: '4月', value: 1800 },
  { name: '5月', value: 2000 },
  { name: '6月', value: 2200 },
]

const lineChartData = [
  { name: '1月', value: 7500 },
  { name: '2月', value: 7800 },
  { name: '3月', value: 8000 },
  { name: '4月', value: 8200 },
  { name: '5月', value: 8500 },
  { name: '6月', value: 8300 },
]

const barChartData2 = [
  { name: '1月', value: 1800 },
  { name: '2月', value: 1900 },
  { name: '3月', value: 2100 },
  { name: '4月', value: 2200 },
  { name: '5月', value: 2300 },
  { name: '6月', value: 2340 },
]
</script>

<template>
  <div class="w-full h-full flex-1 grid grid-cols-1 gap-2">
    <div class="grid grid-rows-3 gap-4">
      <HomeTopLeftCard
        icon="icon-gangwei"
        title="招聘职位总个数"
        :value="12580"
        indicator-desc="职位数量"
        quantifier="个"
        :chart-data="barChartData"
        :change-rate="12.5"
        change-label="较上月"
        :colors="['#80FFA5', '#adfdc5']"
      />
      <HomeTopLeftCard
        title="招聘总人数"
        :value="8500"
        indicator-desc="招聘总人数"
        quantifier="人"
        icon="icon-hrcollegepeopleCardingRange"
        :chart-data="lineChartData"
        :change-rate="-3.2"
        change-label="较上月"
        :colors="['#FFBF00', '#c6b26c']"
      />
      <HomeTopLeftCard
        title="招聘单位总数量"
        :value="2340"
        indicator-desc="单位数量"
        quantifier="家"
        icon="icon-gongsi"
        :chart-data="barChartData2"
        :change-rate="0"
        change-label="较上月"
        :colors="['#37A2FF', '#7bbcf5']"
      />
    </div>
  </div>
</template>
