<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import DoughnutChart from '../Echart/DoughnutChart.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'

const experienceData = [
  { name: '经验不限', value: 376414 },
  { name: '1年及无经验', value: 58867 },
  { name: '1-3年', value: 283283 },
  { name: '3-5年', value: 193399 },
  { name: '5-10年', value: 83747 },
  { name: '10年以上', value: 10284 },
]
const educationData = [
  { name: '学历不限', value: 285364 },
  { name: '高中及以下', value: 80590 },
  { name: '大专', value: 354479 },
  { name: '本科', value: 272424 },
  { name: '研究生及以上', value: 13137 },
]
const pieData = ref([
  { value: 1048, name: '第一产业' },
  { value: 735, name: '第二产业' },
  { value: 580, name: '第三产业' },
])
</script>

<template>
  <div class="w-full h-[284px] shadow-md mt-5 grid grid-cols-5 gap-2 overflow-hidden flex-shrink-0">
    <div class="col-span-3 bg-white/5 border border-white/10 rounded-lg px-2 py-3">
      <FifthTitle title="招聘职位要求分布" subtext="（按招聘人数统计）" />
      <div class="grid grid-cols-3 gap-4 mt-3">
        <div
          class="h-full bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex flex-col gap-4"
        >
          <SecondTitle
            title="招聘职位经验要求分布"
            type="circle"
            icon="icon-jingyan"
            :icon-size="16"
          />
          <DoughnutChart
            :data="experienceData"
            tooltip-title="招聘职位经验要求"
            value-name="职位总个数"
            height="150px"
            quantifier="个"
            :center="['23%', '45%']"
            :radius="['35%', '60%']"
            :legend="{
              right: '0%',
              top: '0%',
              bottom: 'auto',
              textStyle: {
                color: 'rgba(255, 255, 255, 0.7)',
                fontSize: 10,
              },
            }"
          />
        </div>
        <div
          class="h-full bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1"
        >
          <SecondTitle
            title="招聘职位学历要求分布"
            type="circle"
            icon="icon-xueli"
            :icon-size="18"
          />
          <DoughnutChart
            :data="educationData"
            tooltip-title="招聘职位学历要求"
            value-name="职位总个数"
            height="150px"
            quantifier="个"
            :center="['23%', '55%']"
            :radius="['35%', '60%']"
            :legend="{
              right: '0%',
              top: '13%',
              bottom: 'auto',
              textStyle: {
                color: 'rgba(255, 255, 255, 0.7)',
                fontSize: 10,
              },
            }"
          />
        </div>
        <div
          class="h-full bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1"
        >
          <SecondTitle title="招聘单位规模分布" type="circle" icon="icon-gongsi" :icon-size="18" />
          <DoughnutChart
            :data="educationData"
            tooltip-title="招聘职位学历要求"
            value-name="职位总个数"
            height="150px"
            quantifier="个"
            :center="['23%', '55%']"
            :radius="['35%', '60%']"
            :legend="{
              right: '0%',
              top: '15%',
              bottom: 'auto',
              textStyle: {
                color: 'rgba(255, 255, 255, 0.7)',
                fontSize: 10,
              },
            }"
          />
        </div>
      </div>
    </div>
    <div class="col-span-2 bg-white/5 border border-white/10 rounded-lg px-4 py-3">
      <FifthTitle title="三大产业与招聘职位总个数和招聘需求总人数" />
      <div class="grid grid-cols-2 gap-4 mt-3 flex-1 min-h-0">
        <div
          class="h-full bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <SecondTitle
            title="三大产业招聘职位总个数"
            type="circle"
            icon="icon-gangwei"
            :icon-size="20"
          />
          <GradientBarChart
            height="160px"
            :data="pieData"
            :x-axis-rotate="0"
            :bar-gradient="{
              startColor: '#6dd0ed',
              endColor: '#92e4d0',
            }"
            :grid="{
              top: '25%',
              bottom: '2%',
              left: '3%',
              right: '5%',
            }"
            :label-style="{
              fontSize: 12,
              color: '#6dd0ed',
            }"
            tooltip-title="三大产业招聘职位总个数"
            quantifier="个"
          />
        </div>
        <div
          class="h-full bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <SecondTitle
            title="三大产业招聘需求总人数"
            type="circle"
            icon="icon-hrcollegepeopleCardingRange"
            :icon-size="18"
          />
          <GradientBarChart
            height="160px"
            :data="pieData"
            :x-axis-rotate="0"
            :bar-gradient="{
              startColor: '#955fe9',
              endColor: '#8592eb',
            }"
            :grid="{
              top: '25%',
              bottom: '2%',
              left: '3%',
              right: '5%',
            }"
            tooltip-title="三大产业招聘需求总人数"
            quantifier="人"
            :label-style="{
              fontSize: 12,
              color: '#955fe9',
            }"
          />
        </div>
      </div>
    </div>
  </div>
</template>
