<script setup lang="ts">
import MapChart from '../Echart/MapChart.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import Tooltip from '../common/Tooltip.vue'
import HorizontalBarChart from '../Echart/HorizontalBarChart.vue'
import Icon from '../common/Icon.vue'
import FifthTitle from '../common/Title/FifthTitle.vue'
import PieChart from '../Echart/PieChart.vue'
import NightingaleChart from '../Echart/NightingaleChart.vue'
import RankCard from '../common/RankCard.vue'
import { eduYearMap, schoolTypeMap } from '~/utils/constants'

const props = defineProps<{
  schoolType: string
  year: string
}>()

const zaixiaoxueshengTitle = computed(() => {
  return `${schoolTypeMap[props.schoolType]}在校学生数`
})

const xuexiaoTitle = computed(() => {
  return `${schoolTypeMap[props.schoolType]}学校数`
})

const zhaoshengTitle = computed(() => {
  return `${schoolTypeMap[props.schoolType]}招生数`
})

const biyeshengTitle = computed(() => {
  return `${schoolTypeMap[props.schoolType]}毕业生数`
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

const changeRate = ref(12.5)

const pieChartData = ref([
  { name: '本科院校', value: 100 },
  { name: '专科院校', value: 200 },
])

const pie2ChartData = ref([
  { name: '双一流院校', value: 100 },
  { name: '普通本科院校', value: 300 },
  { name: '双高院校', value: 100 },
  { name: '普通专科院校', value: 200 },
])

const tooltipFormatter = (params: any) => {
  const item = params.data || {}

  return `
    <div class="font-bold text-gray-800 text-xs">${params.name}学校概览</div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">普通高等学校数排名：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">第${item.group}名</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">普通高等学校总数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${
        item.value?.toLocaleString?.() ?? 0
      }所</span>
    </div>
    <div class="flex items-center mt-2 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">本科院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${
        item.shuangGao + item.feiShuangGao
      }所</span>
    </div>
    <div class="flex items-center mt-1.5 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-sky-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">双一流院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-sky-600">${item.shuangYiLiu}所</span>
    </div>
    <div class="flex items-center mt-1.5 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-red-400 to-pink-400 rounded-full mr-2"></span>
      <span class="text-gray-700">非双一流院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-red-600">${item.feiShuangYiLiu}所</span>
    </div>
    <div class="flex items-center mt-1.5 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-orange-400 to-yellow-400 rounded-full mr-2"></span>
      <span class="text-gray-700">专科院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-orange-600">${
        item.shuangYiLiu + item.feiShuangYiLiu
      }所</span>
    </div>
    <div class="flex items-center mt-1.5 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-green-400 to-lime-400 rounded-full mr-2"></span>
      <span class="text-gray-700">双高院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-green-600">${item.shuangGao}所</span>
    </div>
    <div class="flex items-center mt-1.5 text-xs">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mr-2"></span>
      <span class="text-gray-700">非双高院校学校数：</span>
      <span class="font-bold font-DIN-Medium text-purple-600">${item.feiShuangGao}所</span>
    </div>
  `
}
</script>

<template>
  <div class="w-full h-[580px] mb-4 flex mt-4">
    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <RankCard
        :title="zaixiaoxueshengTitle"
        title-icon="icon-renyuan"
        title-icon-size="20"
        subtext="按省份排行"
        is-active
        :indicator-desc="`${eduYearMap[props.year]}${
          schoolTypeMap[props.schoolType]
        }在校学生数按照省份排行，数据来源于国家统计局`"
        unit="万"
        quantifier="人"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#80FFA5', '#adfdc5']"
        :tooltip-title="zaixiaoxueshengTitle"
        :grid="{
          top: '3%',
        }"
      />
      <RankCard
        :title="xuexiaoTitle"
        title-icon="icon-xuexiao"
        title-icon-size="15"
        subtext="按省份排行"
        :is-active="false"
        :indicator-desc="`${eduYearMap[props.year]}${
          schoolTypeMap[props.schoolType]
        }学校数按照省份排行，数据来源于国家统计局`"
        quantifier="所"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#FFBF00', '#c6b26c']"
        :tooltip-title="xuexiaoTitle"
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
          map-name="china"
          legend-title="学校数量"
          quantifier="所"
          :data="chartData"
          :tooltip-formatter="tooltipFormatter"
          :zoom="1.1"
          :center="['50%', '60%']"
        />
      </div>
    </div>

    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <RankCard
        :title="zhaoshengTitle"
        title-icon="icon-renyuan"
        title-icon-size="20"
        subtext="按省份排行"
        :is-active="false"
        :indicator-desc="`${eduYearMap[props.year]}${
          schoolTypeMap[props.schoolType]
        }招生数按照省份排行，数据来源于国家统计局`"
        unit="万"
        quantifier="人"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#37A2FF', '#7bbcf5']"
        :tooltip-title="zhaoshengTitle"
        :grid="{
          top: '3%',
        }"
      />
      <RankCard
        :title="biyeshengTitle"
        title-icon="icon-renyuan"
        title-icon-size="20"
        subtext="按省份排行"
        :is-active="false"
        :indicator-desc="`${eduYearMap[props.year]}${
          schoolTypeMap[props.schoolType]
        }毕业生数按照省份排行，数据来源于国家统计局`"
        unit="万"
        quantifier="人"
        chart-height="230px"
        :chart-data="chartData"
        :bar-colors="['#b39ddb', '#e1bee7']"
        :tooltip-title="biyeshengTitle"
        :grid="{
          top: '3%',
        }"
      />
    </div>
  </div>
</template>
