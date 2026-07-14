<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import Card from '../common/Card.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import TrendCard from '../common/TrendCard.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'
import { comparedMap } from '@/utils/constants'

const props = withDefaults(
  defineProps<{
    isCleaned: boolean
    time: string
  }>(),
  {
    isCleaned: false,
    time: 'month',
  }
)

const comparedTitle = computed(() => {
  return comparedMap[props.time]
})

const title = computed(() => {
  return props.isCleaned ? '（已清洗）' : '（全部）'
})

const mockDetail = [
  { name: '第1周', value: 9500 },
  { name: '第2周', value: 10200 },
  { name: '第3周', value: 8700 },
  { name: '第4周', value: 11000 },
  { name: '第5周', value: 10800 },
  { name: '第6周', value: 12000 },
]

const mockYiqingxi = [
  { name: '第1周', value: 800 },
  { name: '第2周', value: 900 },
  { name: '第3周', value: 850 },
  { name: '第4周', value: 950 },
  { name: '第5周', value: 1000 },
  { name: '第6周', value: 1100 },
]

const chartData = ref([
  { name: '第1周', value: 800 },
  { name: '第2周', value: 900 },
  { name: '第3周', value: 850 },
  { name: '第4周', value: 950 },
  { name: '第5周', value: 1000 },
  { name: '第6周', value: 1100 },
])

const wentiData = ref([
  { name: '行业关联', value: 800 },
  { name: '公司合并', value: 1000 },
  { name: '其他', value: 1100 },
])
</script>

<template>
  <div class="mt-8">
    <FifthTitle title="已爬取的单位数据概览" icon="icon-gongsi" :icon-size="14" size="md" />
    <div class="grid gap-4 mt-4" :class="isCleaned ? 'grid-cols-3' : 'grid-cols-4'">
      <TrendCard
        :key="isCleaned ? 'isCleaned' : 'all'"
        :title="`单位列表${title}`"
        :value="457844"
        indicator-desc="单位列表"
        quantifier="家"
        :chart-data="chartData"
        :colors="['#80FFA5']"
        :change-label="comparedTitle"
        :change-rate="-12.5"
        is-smooth-line
        height="230px"
      />
      <TrendCard
        :key="isCleaned ? 'isCleaned' : 'all'"
        :title="`职位新增单位${title}`"
        :value="457844"
        indicator-desc="职位详情"
        quantifier="家"
        :chart-data="mockDetail"
        :colors="['#37A2FF', '#7bbcf5']"
        :change-label="comparedTitle"
        :change-rate="-12.5"
        is-smooth-line
        height="230px"
      />
      <TrendCard
        :key="isCleaned ? 'isCleaned' : 'all'"
        title="单位清洗"
        :value="457844"
        indicator-desc="已经清洗完整的数据，将职位列表和职位详情进行合并"
        quantifier="家"
        :chart-data="mockYiqingxi"
        :colors="['#8e44ad', '#d2b4de']"
        :change-label="comparedTitle"
        :change-rate="-12.5"
        is-smooth-line
        height="230px"
      />
      <Card v-if="!isCleaned">
        <FirstTitle title="有问题单位分布" class="mb-4" />
        <GradientBarChart
          height="230px"
          :data="wentiData"
          :x-axis-rotate="30"
          :bar-gradient="{
            startColor: '#6dd0ed',
            endColor: '#92e4d0',
          }"
          :grid="{
            top: '20%',
            bottom: '0%',
            left: '3%',
            right: '3%',
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed',
          }"
          tooltip-title="有问题的单位数量"
          quantifier="家"
        />
      </Card>
    </div>
  </div>
</template>
