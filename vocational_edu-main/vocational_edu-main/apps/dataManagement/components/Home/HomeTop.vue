<script setup lang="ts">
import { ref, computed } from 'vue'
import MapChart from '../Echart/MapChart.vue'
import HomeTopSalary from './HomeTopSalary.vue'
import HomeTopLeft from './HomeTopLeft.vue'

// Props 接口定义
interface Props {
  title?: string
  subtitle?: string
  showLeftPanel?: boolean
  showRightPanel?: boolean
  province?: string
  time?: string
  scope?: string
}

// 默认Props
const props = withDefaults(defineProps<Props>(), {
  title: '数据管理平台',
  subtitle: '职业教育人才供需分析',
  showLeftPanel: true,
  showRightPanel: true,
  province: '全国',
  time: 'month',
  scope: 'all',
})

const mapName = computed(() => {
  return props.province === '全国' ? 'china' : props.province
})

const mapData = ref([
  { name: '北京市', value: 32000 },
  { name: '天津市', value: 12000 },
  { name: '上海市', value: 28000 },
  { name: '重庆市', value: 15000 },
  { name: '河北省', value: 18000 },
  { name: '河南省', value: 22000 },
  { name: '云南省', value: 9000 },
  { name: '辽宁省', value: 11000 },
  { name: '黑龙江省', value: 8000 },
  { name: '湖南省', value: 17000 },
  { name: '安徽省', value: 14000 },
  { name: '山东省', value: 26000 },
  { name: '新疆维吾尔自治区', value: 7000 },
  { name: '江苏省', value: 25000 },
  { name: '浙江省', value: 24000 },
  { name: '江西省', value: 10000 },
  { name: '湖北省', value: 16000 },
  { name: '广西壮族自治区', value: 9000 },
  { name: '甘肃省', value: 6000 },
  { name: '山西省', value: 8000 },
  { name: '内蒙古自治区', value: 7000 },
  { name: '陕西省', value: 12000 },
  { name: '吉林省', value: 9000 },
  { name: '福建省', value: 13000 },
  { name: '贵州省', value: 8000 },
  { name: '广东省', value: 35000 },
  { name: '青海省', value: 4000 },
  { name: '西藏自治区', value: 2000 },
  { name: '四川省', value: 21000 },
  { name: '宁夏回族自治区', value: 3000 },
  { name: '海南省', value: 5000 },
  { name: '台湾省', value: 6000 },
  { name: '香港特别行政区', value: 2000 },
  { name: '澳门特别行政区', value: 1000 },
])

const tooltipFormatter = (params: any) => {
  return `
    <div class="font-bold text-gray-800">${params.name}数据概览</div>
    <div class="flex items-center mt-2">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘总人数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${
        params.value?.toLocaleString?.() ?? 0
      }人</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-orange-400 to-yellow-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘职位总个数：</span>
      <span class="font-bold font-DIN-Medium text-orange-600">${454511}个</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-green-400 to-lime-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘单位总数量：</span>
      <span class="font-bold font-DIN-Medium text-green-600">${123456}家</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘标准行业总个数：</span>
      <span class="font-bold font-DIN-Medium text-purple-600">${12346}个</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-sky-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘标准职业总个数：</span>
      <span class="font-bold font-DIN-Medium text-sky-600">${12346}个</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-red-400 to-pink-400 rounded-full mr-2"></span>
      <span class="text-gray-700">薪资25%分位数：</span>
      <span class="font-bold font-DIN-Medium text-red-600">${1460}元</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-pink-400 to-orange-400 rounded-full mr-2"></span>
      <span class="text-gray-700">薪资中位数：</span>
      <span class="font-bold font-DIN-Medium text-pink-600">${3460}元</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-amber-400 to-yellow-400 rounded-full mr-2"></span>
      <span class="text-gray-700">薪资75%分位数：</span>
      <span class="font-bold font-DIN-Medium text-amber-600">${7460}元</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-lime-400 to-green-400 rounded-full mr-2"></span>
      <span class="text-gray-700">在校学生数：</span>
      <span class="font-bold font-DIN-Medium text-lime-600">${12345678}人</span>
    </div>
  `
}
</script>

<template>
  <div class="w-full flex-1 mb-4 min-h-0 flex mt-4">
    <div class="w-[21%] backdrop-blur-sm flex flex-col min-h-0">
      <HomeTopLeft />
    </div>

    <div class="w-[58%]">
      <div class="relative w-full h-full">
        <img
          src="~/assets/images/bg.png"
          alt=""
          class="absolute top-0 left-0 -z-1 w-full h-full object-cover opacity-25"
        />
        <MapChart
          :title="props.province"
          :data="mapData"
          :map-name="mapName"
          legend-title="招聘总人数"
          quantifier="人"
          :tooltip-formatter="tooltipFormatter"
          :zoom="mapName === 'china' ? 1.2 : 0.8"
          :center="mapName === 'china' ? ['50%', '60%'] : ['40%', '45%']"
        />
      </div>
    </div>

    <div class="w-[21%] backdrop-blur-sm flex flex-col justify-between min-h-0">
      <HomeTopSalary />
      <HomeTopPlatform />
    </div>
  </div>
</template>
