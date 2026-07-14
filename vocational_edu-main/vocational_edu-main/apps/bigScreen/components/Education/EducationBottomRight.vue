<script setup lang="ts">
import GradientBarChart from '../Echart/GradientBarChart.vue'

const data = [
  { name: '第一产业', value: 162980000 },
  { name: '第二产业', value: 212750000 },
  { name: '第三产业', value: 358660000 },
]
</script>

<template>
  <div
    class="relative w-full h-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 shadow-md flex"
  >
    <ThirdTitleHeader title="三大产业就业人员数统计局数据（2024年）" />
    <div class="absolute left-0 top-0 w-full h-full z-10 flex items-center justify-center">
      <GradientBarChart
        :data="data"
        unit="人"
        height="190px"
        :bar-gradient="{
          startColor: 'rgba(209, 196, 233, 0.3)',
          endColor: 'rgba(209, 196, 233, 1)',
        }"
        tooltip-title="2024年就业人员数"
        quantifier="元"
        :show-legend="false"
        :grid="{
          top: '27%',
          bottom: '8%',
          left: '12%',
          right: '7%',
        }"
        :x-axis-rotate="0"
        show-label
        bar-width="40%"
        :label-style="{
          fontSize: 12,
          color: 'rgba(209, 196, 233)',
        }"
      />
    </div>
  </div>
</template>
