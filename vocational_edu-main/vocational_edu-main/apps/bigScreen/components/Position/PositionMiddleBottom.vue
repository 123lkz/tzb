<script setup lang="ts">
import GradientBarChart from '../Echart/GradientBarChart.vue'
import PositionMiddleBottomCenter from './PositionMiddleBottomCenter.vue'
import DoughnutChart from '~/components/Echart/DoughnutChart.vue'
import ThirdTitleHeader from '~/components/ThirdTitleHeader.vue'

interface Props {
  isStatAll: boolean
  isStatYear: boolean
  year: number
  month: number
  companyData: Array<{ name: string; value: number }>
  experienceData: Array<{ name: string; value: number }>
  educationData: Array<{ name: string; value: number }>
  threeIndustryData: Array<{ name: string; value: number }>
}

const props = defineProps<Props>()
</script>

<template>
  <div class="grid grid-cols-3 gap-4 h-full">
    <div
      class="relative flex flex-col items-center h-full flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/5 flex-1 min-h-0"
      style="height: 100%"
    >
      <ThirdTitleHeader
        :title="
          props.isStatAll
            ? props.isStatYear
              ? `${props.year}年招聘单位规模`
              : `${props.year}年${props.month}月招聘单位规模`
            : props.isStatYear
            ? `${props.year}年招聘单位规模(应届大专生)`
            : `${props.year}年${props.month}月招聘单位规模(应届大专生)`
        "
      />
      <DoughnutChart
        :data="props.companyData"
        tooltip-title="招聘单位"
        height="170px"
        quantifier="家"
      />
    </div>

    <PositionMiddleBottomCenter
      :is-stat-all="props.isStatAll"
      :is-stat-year="props.isStatYear"
      :year="props.year"
      :month="props.month"
      :experience-data="props.experienceData"
      :education-data="props.educationData"
    />

    <div
      class="relative flex flex-col items-center h-full flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/5 flex-1 min-h-0"
      style="height: 100%"
    >
      <ThirdTitleHeader
        :title="
          props.isStatAll
            ? props.isStatYear
              ? `${props.year}年三大产业招聘总人数`
              : `${props.year}年${props.month}月三大产业招聘总人数`
            : props.isStatYear
            ? `${props.year}年三大产业招聘总人数(应届大专生)`
            : `${props.year}年${props.month}月三大产业招聘总人数(应届大专生)`
        "
      />
      <GradientBarChart
        :data="props.threeIndustryData"
        unit="万"
        height="170px"
        :bar-gradient="{
          startColor: 'rgba(255, 209, 128, 0.3)',
          endColor: 'rgba(255, 209, 128, 1)',
        }"
        tooltip-title="招聘需求总人数"
        quantifier="人"
        :show-legend="false"
        :grid="{
          top: '20%',
          bottom: '10%',
          left: '10%',
          right: '5%',
        }"
        :x-axis-rotate="0"
        show-label
        bar-width="40%"
        :label-style="{
          fontSize: 12,
          color: 'rgba(255, 209, 128)',
        }"
      />
    </div>
  </div>
</template>

<style scoped lang="scss"></style>
