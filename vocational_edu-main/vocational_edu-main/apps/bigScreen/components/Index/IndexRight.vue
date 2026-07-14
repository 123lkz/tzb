<script setup lang="ts">
import ThreeIndustries from './ThreeIndustries.vue'
import TitleHeader from '~/components/TitleHeader.vue'
import ProportionBarChart from '~/components/Echart/ProportionBarChart.vue'
import GradientBarChart from '~/components/Echart/GradientBarChart.vue'

interface ThreeIndustriesValue {
  years: string[]
  primary: number[]
  secondary: number[]
  tertiary: number[]
}

interface IndustrySubItem {
  name: string
}

interface IndustryItem {
  name: string
  industries: IndustrySubItem[]
}

interface ThreeIndustriesIncludes {
  name: string
  color: string
  industries: IndustryItem[]
}

interface PrimaryIndustryValueData {
  name: string
  value: number
}

interface PrimaryIndustryPeopleData {
  name: string
  value: number
}

const props = defineProps({
  threeIndustriesValue: {
    type: Object as PropType<ThreeIndustriesValue>,
    required: true,
  },
  threeIndustriesIncludes: {
    type: Array as PropType<ThreeIndustriesIncludes[]>,
    required: true,
  },
  primaryIndustryValueData: {
    type: Array as PropType<PrimaryIndustryValueData[]>,
    required: true,
  },
  primaryIndustryPeopleData: {
    type: Array as PropType<PrimaryIndustryPeopleData[]>,
    required: true,
  },
})

const formatThreeIndustriesValue = computed(() => {
  const years = props.threeIndustriesValue.years
  const industries = [
    {
      name: '第一产业',
      data: props.threeIndustriesValue.primary,
    },
    {
      name: '第二产业',
      data: props.threeIndustriesValue.secondary,
    },
    {
      name: '第三产业',
      data: props.threeIndustriesValue.tertiary,
    },
  ]

  return { years, industries }
})
</script>

<template>
  <div class="w-full grid grid-rows-4 gap-3">
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-4 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      style="max-height: 222.5px"
    >
      <TitleHeader title="三大产业产值比重（近5年的数据）" />
      <ProportionBarChart
        :data="formatThreeIndustriesValue"
        :original-data="props.threeIndustriesValue"
        tooltip-title="年三大产业产值和比重"
      />
    </div>
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-4 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      style="max-height: 220.5px"
    >
      <TitleHeader title="三大产业和标准行业分类的对应关系" />
      <ThreeIndustries :data="props.threeIndustriesIncludes" />
    </div>
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-4 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      style="max-height: 223.5px"
    >
      <TitleHeader title="标准行业产值（一级标准行业分类）" />
      <GradientBarChart
        :data="props.primaryIndustryValueData"
        unit="亿元"
        height="174px"
        :bar-gradient="{
          startColor: '#00ffff',
          endColor: '#198CEF',
        }"
        tooltip-title="产值"
        quantifier="亿元"
      />
    </div>
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-4 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      style="max-height: 223.5px"
    >
      <TitleHeader title="标准行业从业人员数（一级标准行业分类）" />
      <GradientBarChart
        :data="props.primaryIndustryPeopleData"
        height="174px"
        tooltip-title="从业人员数"
        quantifier="人"
      />
    </div>
  </div>
</template>
