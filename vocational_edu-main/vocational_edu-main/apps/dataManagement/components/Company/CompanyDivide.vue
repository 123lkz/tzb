<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import Card from '../common/Card.vue'

// Mock数据 - 公司规模
const companySizeData = ref([
  {
    name: '大型企业',
    values: [
      { name: '单位总个数', value: 1250 },
      { name: '招聘总人数', value: 15600 },
    ],
  },
  {
    name: '中型企业',
    values: [
      { name: '单位总个数', value: 3200 },
      { name: '招聘总人数', value: 28900 },
    ],
  },
  {
    name: '小微企业',
    values: [
      { name: '单位总个数', value: 5800 },
      { name: '招聘总人数', value: 42300 },
    ],
  },
])

// Mock数据 - 企业登记注册类型
const companyTypeData = ref([
  {
    name: '国有',
    values: [
      { name: '单位总个数', value: 6800 },
      { name: '招聘总人数', value: 52300 },
    ],
  },
  {
    name: '私营',
    values: [
      { name: '单位总个数', value: 2100 },
      { name: '招聘总人数', value: 18900 },
    ],
  },
  {
    name: '集体',
    values: [
      { name: '单位总个数', value: 4200 },
      { name: '招聘总人数', value: 31200 },
    ],
  },
  {
    name: '外商投资',
    values: [
      { name: '单位总个数', value: 1800 },
      { name: '招聘总人数', value: 15600 },
    ],
  },

  {
    name: '个体',
    values: [
      { name: '单位总个数', value: 950 },
      { name: '招聘总人数', value: 8900 },
    ],
  },
  {
    name: '港澳台投资',
    values: [
      { name: '单位总个数', value: 950 },
      { name: '招聘总人数', value: 8900 },
    ],
  },
  {
    name: '其他',
    values: [
      { name: '单位总个数', value: 950 },
      { name: '招聘总人数', value: 8900 },
    ],
  },
])

// Mock数据 - 融资情况
const financingData = ref([
  {
    name: '未融资',
    values: [
      { name: '单位总个数', value: 9500 },
      { name: '招聘总人数', value: 15600 },
    ],
  },
  {
    name: '天使轮',
    values: [
      { name: '单位总个数', value: 3200 },
      { name: '招聘总人数', value: 28900 },
    ],
  },
  {
    name: 'A轮',
    values: [
      { name: '单位总个数', value: 5800 },
      { name: '招聘总人数', value: 42300 },
    ],
  },
  {
    name: 'B轮',
    values: [
      { name: '单位总个数', value: 450 },
      { name: '招聘总人数', value: 4100 },
    ],
  },
  {
    name: 'C轮',
    values: [
      { name: '单位总个数', value: 250 },
      { name: '招聘总人数', value: 2300 },
    ],
  },
  {
    name: 'D轮及以上',
    values: [
      { name: '单位总个数', value: 250 },
      { name: '招聘总人数', value: 2300 },
    ],
  },
  {
    name: '已上市',
    values: [
      { name: '单位总个数', value: 180 },
      { name: '招聘总人数', value: 1680 },
    ],
  },
  {
    name: '自有资金',
    values: [
      { name: '单位总个数', value: 1800 },
      { name: '招聘总人数', value: 1680 },
    ],
  },
])
</script>

<template>
  <div class="w-full bg-white/5 backdrop-blur-sm rounded-lg p-4 mt-6">
    <!-- 主标题 -->
    <FifthTitle
      title="不同划分方式的招聘单位总个数分布"
      size="md"
      icon="icon-a-zhuxingtu2"
      suffix-icon="icon-ding"
    />
    <!-- 图表卡片区域 -->
    <div class="grid grid-cols-12 gap-4 mt-4">
      <!-- 第一个图表卡片 - 公司规模 -->
      <Card class="col-span-3">
        <FirstTitle title="公司规模" class="mb-4" />
        <LineBarDualAxisChart
          :data="companySizeData"
          left-unit=""
          left-quantifier="个"
          right-unit=""
          right-quantifier="人"
          title="公司规模分布"
          left-color="#5470c6"
          right-color="#91cc75"
          is-smooth-line
          tooltip-title="公司规模"
          height="240px"
          :grid="{
            top: '28%',
            left: '1%',
            right: '1%',
            bottom: '2%',
          }"
          :legend="{
            top: '0%',
          }"
        />
      </Card>

      <!-- 第二个图表卡片 - 企业登记注册类型 -->
      <Card class="col-span-5">
        <FirstTitle title="企业登记注册类型" class="mb-4" />
        <LineBarDualAxisChart
          :data="companyTypeData"
          left-unit=""
          left-quantifier="个"
          right-unit=""
          right-quantifier="人"
          title="企业类型分布"
          left-color="#fac858"
          right-color="#ee6666"
          is-smooth-line
          tooltip-title="企业类型"
          height="240px"
          :grid="{
            top: '28%',
            left: '1%',
            right: '1%',
            bottom: '2%',
          }"
          :legend="{
            top: '0%',
          }"
        />
      </Card>

      <!-- 第三个图表卡片 - 融资情况 -->
      <Card class="col-span-4">
        <FirstTitle title="融资情况" class="mb-4" />
        <LineBarDualAxisChart
          :data="financingData"
          left-unit=""
          left-quantifier="个"
          right-unit=""
          right-quantifier="人"
          title="融资情况分布"
          left-color="#73c0de"
          right-color="#3ba272"
          is-smooth-line
          tooltip-title="融资情况"
          height="240px"
          :x-axis-label-rotate="45"
          :grid="{
            top: '28%',
            left: '1%',
            right: '1%',
            bottom: '2%',
          }"
          :legend="{
            top: '0%',
          }"
        />
      </Card>
    </div>
  </div>
</template>
