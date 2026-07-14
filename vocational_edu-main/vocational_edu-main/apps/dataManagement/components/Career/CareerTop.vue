<script setup lang="ts">
import MapChart from '../Echart/MapChart.vue'
import RankCard from '../common/RankCard.vue'
import TrendCard from '../common/TrendCard.vue'
import { careerCategoryMap } from '~/utils/constants'

const props = withDefaults(
  defineProps<{
    province: string
    time: string
    scope: string
    careerLabel: string
    careerLevel: string
  }>(),
  {
    province: '全国',
    time: 'month',
    scope: 'all',
    careerLabel: '',
    careerLevel: '1',
  }
)

const subtext = computed(() => {
  return `按${props.province === '全国' ? '省份' : '城市'}排行`
})

const mapName = computed(() => {
  return props.province === '全国' ? 'china' : props.province
})

const chartData = ref([
  {
    name: '北京市',
    value: 320,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '天津市',
    value: 120,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '上海市',
    value: 89,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '重庆市',
    value: 78,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '河北省',
    value: 180,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '河南省',
    value: 220,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '云南省',
    value: 90,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '辽宁省',
    value: 110,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  {
    name: '黑龙江省',
    value: 80,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  { name: '湖南省', value: 170, group: 1 },
  {
    name: '安徽省',
    value: 140,
    group: 1,
    shuangGao: 100,
    feiShuangGao: 220,
    shuangYiLiu: 330,
    feiShuangYiLiu: 440,
  },
  { name: '山东省', value: 260, group: 1 },
  { name: '新疆维吾尔自治区', value: 70, group: 1 },
  { name: '江苏省', value: 250, group: 1 },
  { name: '浙江省', value: 240, group: 1 },
  { name: '江西省', value: 100, group: 1 },
  { name: '湖北省', value: 160, group: 1 },
  { name: '广西壮族自治区', value: 90, group: 1 },
  { name: '甘肃省', value: 60, group: 1 },
  { name: '山西省', value: 80, group: 1 },
  { name: '内蒙古自治区', value: 70, group: 1 },
  { name: '陕西省', value: 120, group: 1 },
  { name: '吉林省', value: 90, group: 1 },
  { name: '福建省', value: 130, group: 1 },
  { name: '贵州省', value: 80, group: 1 },
  { name: '广东省', value: 350, group: 1 },
  { name: '青海省', value: 40, group: 1 },
  { name: '西藏自治区', value: 20, group: 1 },
  { name: '四川省', value: 210, group: 1 },
  { name: '宁夏回族自治区', value: 30, group: 1 },
  { name: '海南省', value: 50, group: 1 },
  { name: '台湾省', value: 60, group: 1 },
  { name: '香港特别行政区', value: 20, group: 1 },
  { name: '澳门特别行政区', value: 10, group: 1 },
])

const tooltipFormatter = (params: any) => {
  const item = params.data || {}

  return `
    <div class="font-bold text-gray-800 text-xs w-[300px]">
      ${params.name} ${
    props.careerLabel
      ? props.careerLabel + '(' + careerCategoryMap[props.careerLevel] + ')'
      : '标准'
  }职业招聘概览
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业招聘总个数排行：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">第${item.group}名</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业招聘总个数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${
        item.value?.toLocaleString?.() ?? 0
      }个</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业的招聘职位个数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${(
        item.value ?? 0
      ).toLocaleString?.()}个</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业的招聘总人数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${(
        item.value ?? 0
      ).toLocaleString?.()}人</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业的薪资中位数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${(
        item.value ?? 0
      ).toLocaleString?.()}元</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">${props.careerLabel ? '该' : '标准'}职业的招聘单位总个数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${(
        item.value ?? 0
      ).toLocaleString?.()}个</span>
    </div>
  `
}

const chart1Data = ref([
  { name: '2025-01', value: 1245 },
  { name: '2025-02', value: 3250 },
  { name: '2025-03', value: 1970 },
  { name: '2025-04', value: 2845 },
  { name: '2025-05', value: 1445 },
  { name: '2025-06', value: 2250 },
])

const totalValue = ref(12345)
const changeRate = ref(12.5)
</script>

<template>
  <div class="w-full h-[640px] mb-4 flex mt-4">
    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <RankCard
        title="标准职业招聘总个数"
        title-icon="icon-renyuan"
        title-icon-size="20"
        :subtext="subtext"
        is-active
        quantifier="个"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#37A2FF', '#7bbcf5']"
        :tooltip-title="`${props.careerLabel}职业招聘总个数`"
        :indicator-desc="`${props.careerLabel}职业招聘总个数`"
        :grid="{
          top: '3%',
        }"
      />
      <RankCard
        title="招聘总人数"
        title-icon="icon-renyuan"
        title-icon-size="20"
        :subtext="subtext"
        quantifier="人"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#FFBF00', '#FFE5B4']"
        :tooltip-title="`${props.careerLabel}职业招聘总人数`"
        :grid="{
          top: '3%',
        }"
      />
    </div>

    <div class="w-[58%]">
      <div class="relative w-full h-full">
        <img
          src="~/assets/images/bg.png"
          alt=""
          class="absolute top-0 left-0 -z-1 w-full h-full object-cover opacity-25"
        />
        <MapChart
          :map-name="mapName"
          legend-title="职业招聘总个数"
          quantifier="个"
          :data="chartData"
          :tooltip-formatter="tooltipFormatter"
          :zoom="mapName === 'china' ? 1.2 : 0.8"
          :center="mapName === 'china' ? ['50%', '60%'] : ['40%', '45%']"
        />
      </div>
    </div>

    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <RankCard
        title="薪资中位数"
        title-icon="icon-renyuan"
        title-icon-size="20"
        :subtext="subtext"
        quantifier="元"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#b39ddb', '#e1bee7']"
        :tooltip-title="`${props.careerLabel}职业薪资中位数`"
        :grid="{
          top: '3%',
        }"
      />
      <RankCard
        title="招聘单位数"
        title-icon="icon-renyuan"
        title-icon-size="20"
        :subtext="subtext"
        quantifier="个"
        chart-height="230px"
        :chart-data="chartData"
        :tooltip-title="`${props.careerLabel}职业招聘单位数`"
        :grid="{
          top: '3%',
        }"
      />
    </div>
  </div>
</template>
