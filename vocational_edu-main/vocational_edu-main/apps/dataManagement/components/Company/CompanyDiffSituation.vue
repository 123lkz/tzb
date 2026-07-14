<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import Card from '../common/Card.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import DoughnutChart from '../Echart/DoughnutChart.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'

const props = defineProps<{
  companyScaleName: string
}>()

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
const companyData = [
  { name: '大型', value: 285364 },
  { name: '中型', value: 80590 },
  { name: '小微型', value: 354479 },
]
</script>

<template>
  <div class="w-full h-full flex flex-col gap-4 bg-white/5 backdrop-blur-sm rounded-lg p-4 mt-6">
    <FifthTitle
      :title="`${props.companyScaleName || ''}招聘单位总个数分布`"
      type="circle"
      size="md"
      icon="icon-gongsi"
    />
    <div class="grid grid-cols-12 gap-4">
      <Card class="col-span-4">
        <SecondTitle
          :title="`${props.companyScaleName || ''}招聘单位经验要求分布`"
          type="circle"
          icon="icon-jingyan"
          :icon-size="16"
        />
        <DoughnutChart
          :data="experienceData"
          tooltip-title="工作经验要求的招聘单位总个数"
          value-name="单位总个数"
          height="180px"
          quantifier="个"
          :center="['28%', '50%']"
          :radius="['40%', '70%']"
          :legend="{
            right: '0%',
            top: '10%',
            bottom: 'auto',
            textStyle: {
              color: 'rgba(255, 255, 255, 0.7)',
              fontSize: 10,
            },
          }"
        />
      </Card>
      <Card class="col-span-4">
        <SecondTitle
          :title="`${props.companyScaleName || ''}招聘单位学历要求分布`"
          type="circle"
          icon="icon-xueli"
          :icon-size="18"
        />
        <DoughnutChart
          :data="educationData"
          tooltip-title="学历要求的招聘单位总个数"
          value-name="单位总个数"
          height="180px"
          quantifier="个"
          :center="['28%', '50%']"
          :radius="['40%', '70%']"
          :legend="{
            right: '0%',
            top: 'center',
            bottom: 'auto',
            textStyle: {
              color: 'rgba(255, 255, 255, 0.7)',
              fontSize: 10,
            },
          }"
        />
      </Card>
    </div>
  </div>
</template>
