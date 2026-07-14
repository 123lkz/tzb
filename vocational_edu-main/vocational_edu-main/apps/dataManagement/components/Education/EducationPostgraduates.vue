<script setup lang="ts">
import FirstTitle from '../common/Title/FirstTitle.vue'
import { type DataItem } from '~/components/Echart/LineChart.vue'
import GradientAreaChart from '~/components/Echart/GradientAreaChart.vue'

// 真实数据
const zhaoshengData = ref<DataItem[]>([
  {
    name: '2020',
    value: 110.6551,
  },
  {
    name: '2021',
    value: 117.6526,
  },
  {
    name: '2022',
    value: 124.2479,
  },
  {
    name: '2023',
    value: 130.1679,
  },
  {
    name: '2024',
    value: 135.6778,
  },
])

// 真实数据
const zaixiaoshengData = ref<DataItem[]>([
  {
    name: '2020',
    value: 313.9598,
  },
  {
    name: '2021',
    value: 333.2373,
  },
  {
    name: '2022',
    value: 365.3613,
  },
  {
    name: '2023',
    value: 388.294,
  },
  {
    name: '2024',
    value: 409.5436,
  },
])

// 真实数据
const biyeshengData = ref<DataItem[]>([
  {
    name: '2020',
    value: 72.8627,
  },
  {
    name: '2021',
    value: 77.2761,
  },
  {
    name: '2022',
    value: 86.2165,
  },
  {
    name: '2023',
    value: 101.4755,
  },
  {
    name: '2024',
    value: 108.3595,
  },
])
</script>

<template>
  <div class="flex items-center gap-4 border-t border-dotted border-[#00ffff]/30 pt-6">
    <div class="flex items-center relative px-6">
      <span
        class="w-6 h-24 bg-[#00ffff]/20 rounded-full rounded-br-none absolute left-0 -top-8"
      ></span>
      <span
        class="bg-[#00ffff]/90 py-4 px-1.5 -ml-3 rounded-full inline-block text-black text-sm font-semibold flex flex-col leading-tight"
      >
        <span>研</span>
        <span>究</span>
        <span>生</span>
        <span>数</span>
        <span>据</span>
      </span>
      <span class="w-6 h-24 bg-[#00ffff]/20 rounded-full absolute right-3 -bottom-8"></span>
    </div>
    <div class="grid grid-cols-3 gap-8 w-full">
      <div
        class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      >
        <FirstTitle title="研究生招生数" />
        <div class="flex items-center gap-2 mt-2">
          <GradientAreaChart
            :height="'180px'"
            :data="zhaoshengData"
            :show-y-axis="true"
            tooltip-title="研究生招生数"
            unit="万"
            quantifier="人"
            color="#37A2FF"
            :x-axis-interval="0"
            :show-label="true"
            :show-symbol="true"
            :show-y-axis-unit="true"
            :grid="{
              top: '15%',
              left: '0%',
              bottom: '0%',
            }"
            :y-axis-min="0"
            :y-axis-max="200"
          />
        </div>
      </div>
      <div
        class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      >
        <FirstTitle title="研究生在校学生数" />
        <div class="flex items-center gap-2 mt-2">
          <GradientAreaChart
            :height="'180px'"
            :data="zaixiaoshengData"
            :show-y-axis="true"
            tooltip-title="研究生在校学生数"
            unit="万"
            quantifier="人"
            color="#FF0087"
            :x-axis-interval="0"
            :show-label="true"
            :show-symbol="true"
            :show-y-axis-unit="true"
            :grid="{
              top: '15%',
              left: '0%',
              bottom: '0%',
            }"
            :y-axis-min="0"
            :y-axis-max="600"
          />
        </div>
      </div>
      <div
        class="bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20"
      >
        <FirstTitle title="研究生毕业生数" />
        <div class="flex items-center gap-2 mt-2">
          <GradientAreaChart
            :height="'180px'"
            :data="biyeshengData"
            :show-y-axis="true"
            tooltip-title="研究生毕业生数"
            unit="万"
            quantifier="人"
            :x-axis-interval="0"
            :show-label="true"
            :show-symbol="true"
            :show-y-axis-unit="true"
            :grid="{
              top: '15%',
              left: '0%',
              bottom: '0%',
            }"
            :y-axis-min="0"
            :y-axis-max="150"
          />
        </div>
      </div>
    </div>
  </div>
</template>
