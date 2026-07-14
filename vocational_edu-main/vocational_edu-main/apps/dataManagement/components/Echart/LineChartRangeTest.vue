<script setup lang="ts">
import LineChart, { type DataItem } from '~/components/Echart/LineChart.vue'

// 测试数据 - 不同范围的数据
const testData1 = ref<DataItem[]>([
  { name: '2020', value: 1215 },
  { name: '2021', value: 1350 },
  { name: '2022', value: 1480 },
  { name: '2023', value: 1620 },
  { name: '2024', value: 1750 },
])

const testData2 = ref<DataItem[]>([
  { name: '2020', value: 5840 },
  { name: '2021', value: 6120 },
  { name: '2022', value: 6350 },
  { name: '2023', value: 6580 },
  { name: '2024', value: 6820 },
])

const testData3 = ref<DataItem[]>([
  { name: '2020', value: 110.6551 },
  { name: '2021', value: 117.6526 },
  { name: '2022', value: 124.2479 },
  { name: '2023', value: 130.1679 },
  { name: '2024', value: 135.6778 },
])

const testData4 = ref<DataItem[]>([
  { name: '2020', value: 72.8627 },
  { name: '2021', value: 77.2761 },
  { name: '2022', value: 86.2165 },
  { name: '2023', value: 101.4755 },
  { name: '2024', value: 108.3595 },
])
</script>

<template>
  <div class="grid grid-cols-2 gap-4 p-4">
    <!-- 测试数据1: 1215-1750，应该显示1000-2000 -->
    <div class="bg-gray-800 rounded-lg p-4">
      <h3 class="text-white text-lg mb-4">测试数据1 (1215-1750)</h3>
      <p class="text-gray-300 text-sm mb-2">预期Y轴范围: 1000-2000，区间: 200</p>
      <LineChart
        :data="testData1"
        height="200px"
        :smooth="true"
        :show-symbol="true"
        line-color="#73C0DE"
        unit="人"
      />
    </div>

    <!-- 测试数据2: 5840-6820，应该显示5000-7000 -->
    <div class="bg-gray-800 rounded-lg p-4">
      <h3 class="text-white text-lg mb-4">测试数据2 (5840-6820)</h3>
      <p class="text-gray-300 text-sm mb-2">预期Y轴范围: 5000-7000，区间: 500</p>
      <LineChart
        :data="testData2"
        height="200px"
        :smooth="true"
        :show-symbol="true"
        line-color="#91CC75"
        unit="万元"
      />
    </div>

    <!-- 测试数据3: 110-135，应该显示100-200 -->
    <div class="bg-gray-800 rounded-lg p-4">
      <h3 class="text-white text-lg mb-4">测试数据3 (110-135)</h3>
      <p class="text-gray-300 text-sm mb-2">预期Y轴范围: 100-200，区间: 20</p>
      <LineChart
        :data="testData3"
        height="200px"
        :smooth="true"
        :show-symbol="true"
        line-color="#FAC857"
        unit="万人"
      />
    </div>

    <!-- 测试数据4: 72-108，应该显示70-110 -->
    <div class="bg-gray-800 rounded-lg p-4">
      <h3 class="text-white text-lg mb-4">测试数据4 (72-108)</h3>
      <p class="text-gray-300 text-sm mb-2">预期Y轴范围: 70-110，区间: 10</p>
      <LineChart
        :data="testData4"
        height="200px"
        :smooth="true"
        :show-symbol="true"
        line-color="#EE6666"
        unit="%"
      />
    </div>
  </div>
</template>
