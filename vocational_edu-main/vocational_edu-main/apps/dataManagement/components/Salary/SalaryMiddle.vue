<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import DoughnutChart from '../Echart/DoughnutChart.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'
import MultiBarChart from '../Echart/MultiBarChart.vue'

const experienceData = [
  { name: '经验不限', value: 7000 },
  { name: '1年及无经验', value: 5000 },
  { name: '1-3年', value: 6000 },
  { name: '3-5年', value: 7000 },
  { name: '5-10年', value: 8000 },
  { name: '10年以上', value: 13000 },
]
const educationData = [
  { name: '学历不限', value: 8000 },
  { name: '高中及以下', value: 5000 },
  { name: '大专', value: 7000 },
  { name: '本科', value: 9000 },
  { name: '研究生及以上', value: 12000 },
]
const companyData = ref([
  { value: 1048, name: '微型企业' },
  { value: 735, name: '小型企业' },
  { value: 580, name: '中型企业' },
  { value: 580, name: '大型企业' },
])
const chartData = [
  {
    name: '第一产业',
    values: [
      { name: '薪资25%分位数', value: 6500 },
      { name: '薪资中位数', value: 8500 },
      { name: '薪资75%分位数', value: 12000 },
      { name: '薪资平均数', value: 9000 },
    ],
  },
  {
    name: '第二产业',
    values: [
      { name: '薪资25%分位数', value: 6500 },
      { name: '薪资中位数', value: 8500 },
      { name: '薪资75%分位数', value: 12000 },
      { name: '薪资平均数', value: 9000 },
    ],
  },
  {
    name: '第三产业',
    values: [
      { name: '薪资25%分位数', value: 6500 },
      { name: '薪资中位数', value: 8500 },
      { name: '薪资75%分位数', value: 12000 },
      { name: '薪资平均数', value: 9000 },
    ],
  },
]
</script>

<template>
  <div class="w-full h-[284px] shadow-md mt-5 grid grid-cols-4 gap-2 flex-shrink-0">
    <div
      class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
    >
      <FifthTitle title="不同学历的薪资中位数" />
      <GradientBarChart
        height="230px"
        :data="educationData"
        :x-axis-rotate="30"
        :bar-gradient="{
          startColor: '#6dd0ed',
          endColor: '#92e4d0',
        }"
        :grid="{
          top: '20%',
          bottom: '0%',
          left: '3%',
          right: '5%',
        }"
        :label-style="{
          fontSize: 11,
          color: '#6dd0ed',
        }"
        tooltip-title="学历的薪资中位数"
        quantifier="元"
      />
    </div>
    <div
      class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
    >
      <FifthTitle title="不同工作年限的薪资中位数" />
      <GradientBarChart
        height="230px"
        :data="experienceData"
        :x-axis-rotate="30"
        :bar-gradient="{
          startColor: '#f97316',
          endColor: '#fcc316',
        }"
        :grid="{
          top: '20%',
          bottom: '0%',
          left: '3%',
          right: '5%',
        }"
        :label-style="{
          fontSize: 11,
          color: '#f97316',
        }"
        tooltip-title="工作经验的薪资中位数"
        quantifier="元"
      />
    </div>
    <div
      class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
    >
      <FifthTitle title="不同单位规模的薪资中位数" />
      <GradientBarChart
        height="230px"
        :data="companyData"
        :x-axis-rotate="0"
        :bar-gradient="{
          startColor: '#b39ddb',
          endColor: '#e1bee7',
        }"
        :grid="{
          top: '20%',
          bottom: '0%',
          left: '3%',
          right: '5%',
        }"
        :label-style="{
          fontSize: 11,
          color: '#b39ddb',
        }"
        tooltip-title="工作经验的薪资中位数"
        quantifier="元"
      />
    </div>
    <div
      class="h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
    >
      <FifthTitle title="三大产业薪资分布" />
      <MultiBarChart
        :data="chartData"
        height="230px"
        quantifier="元"
        tooltip-title="薪资分布"
        :show-legend="true"
        :show-label="false"
        :grid="{ top: '35%', bottom: '0%', left: '0%', right: '0%' }"
      />
    </div>
  </div>
</template>
