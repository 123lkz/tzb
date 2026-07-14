<script setup lang="ts">
import WithTitleLineMixedBar from '../WithTitleLineMixedBar.vue'

const props = defineProps<{
  isStatAll: boolean
  isStatYear: boolean
  companyChartData: {
    months: string[]
    totalCount: number[]
    changeRate: number[]
  }
  peopleChartData: {
    months: string[]
    totalCount: number[]
    changeRate: number[]
  }
  professionChartData: {
    months: string[]
    totalCount: number[]
    changeRate: number[]
  }
}>()
</script>

<template>
  <div class="h-full flex flex-col gap-3">
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 flex-1 min-h-0"
    >
      <WithTitleLineMixedBar
        :data="props.companyChartData"
        :title="props.isStatAll ? '招聘单位总数量' : '招聘单位总数量（应届大专生）'"
        tooltip-title="招聘单位总数量和变化率"
        height="230px"
        unit="万家"
        :bar-color="'#0066FF'"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
      />
    </div>
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 flex-1 min-h-0"
    >
      <WithTitleLineMixedBar
        :data="props.peopleChartData"
        :title="props.isStatAll ? '招聘需求总人数' : '招聘需求总人数（应届大专生）'"
        tooltip-title="招聘总人数和变化率"
        height="230px"
        unit="万人"
        :bar-color="'#FAC857'"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
      />
    </div>
    <div
      class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 flex-1 min-h-0 relative"
    >
      <WithTitleLineMixedBar
        :data="props.professionChartData"
        :title="props.isStatAll ? '招聘职位总个数' : '招聘职位总个数（应届大专生）'"
        tooltip-title="招聘职位个数和变化率"
        height="230px"
        unit="万个"
        :bar-color="'#00ff80'"
        :is-stat-all="props.isStatAll"
        :is-stat-year="props.isStatYear"
      />
    </div>
  </div>
</template>
