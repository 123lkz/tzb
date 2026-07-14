<script setup lang="ts">
import TrendCard from '../common/TrendCard.vue'

const props = withDefaults(
  defineProps<{
    province: string
    time: string
    scope: string
    industryLabel: string
    industryLevel: string
  }>(),
  {
    province: '全国',
    time: 'month',
    scope: 'all',
    industryLabel: '',
    industryLevel: '1',
  }
)

const chartData = ref([
  { name: '2025-01', value: 120000 },
  { name: '2025-02', value: 300000 },
  { name: '2025-03', value: 160000 },
  { name: '2025-04', value: 180000 },
  { name: '2025-05', value: 200000 },
  { name: '2025-06', value: 220000 },
  { name: '2025-07', value: 240000 },
])
</script>

<template>
  <div class="mt-4 grid grid-cols-4 gap-4">
    <TrendCard
      title="招聘需求总人数"
      :value="120000"
      :indicator-desc="
        props.industryLabel ? props.industryLabel + '行业招聘需求总人数' : '标准行业招聘需求总人数'
      "
      quantifier="人"
      :chart-data="chartData"
      :colors="['#37A2FF', '#7bbcf5']"
      change-label="较上月"
      :change-rate="12.5"
      is-smooth-line
      height="230px"
      is-stat-all
      is-stat-year
    />
    <TrendCard
      title="招聘职位总个数"
      :value="457844"
      indicator-desc="招聘职位总个数"
      quantifier="个"
      :chart-data="chartData"
      :colors="['#80FFA5']"
      change-label="较上月"
      :change-rate="-12.5"
      is-smooth-line
      height="230px"
    />
    <TrendCard
      title="薪资中位数"
      :value="8500"
      indicator-desc="薪资中位数"
      quantifier="元"
      :chart-data="chartData"
      :colors="['#FFA940']"
      change-label="较上月"
      :change-rate="0"
      is-smooth-line
      height="230px"
    />
    <TrendCard
      title="招聘单位总个数"
      :value="120000"
      indicator-desc="招聘单位总个数"
      quantifier="个"
      :chart-data="chartData"
      :colors="['#8e44ad', '#d2b4de']"
      change-label="较上月"
      :change-rate="1.5"
      is-smooth-line
      height="230px"
    />
  </div>
</template>
