<script setup lang="ts">
import MapChart from '../Echart/MapChart.vue'
import PositionTrendCard from './PositionTrendCard.vue'
import PositionRankCard from './PositionRankCard.vue'

const props = withDefaults(
  defineProps<{
    province: string
    time: string
    scope: string
  }>(),
  {
    province: '全国',
    time: 'month',
    scope: 'all',
  }
)

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
    <div class="font-bold text-gray-800">${params.name}职位数据概览</div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-green-400 to-lime-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘职位排行：</span>
      <span class="font-bold text-green-600">第1名</span>
    </div>
    <div class="flex items-center mt-1.5">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-orange-400 to-yellow-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘职位总个数：</span>
      <span class="font-bold font-DIN-Medium text-orange-600">${454511}个</span>
    </div>
     <div class="flex items-center mt-2">
      <span class="inline-block w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘总人数：</span>
      <span class="font-bold font-DIN-Medium text-blue-600">${
        params.value?.toLocaleString?.() ?? 0
      }人</span>
    </div>
  `
}

const chart1Data = ref([
  { name: '2025-01', value: 120000 },
  { name: '2025-02', value: 300000 },
  { name: '2025-03', value: 160000 },
  { name: '2025-04', value: 180000 },
  { name: '2025-05', value: 200000 },
  { name: '2025-06', value: 220000 },
  { name: '2025-07', value: 240000 },
])

const chart2Data = ref([
  { name: '山东省', value: 1200, group: 1 },
  { name: '江苏省', value: 1400, group: 2 },
  { name: '河南省', value: 1600, group: 3 },
  { name: '河北省', value: 1800, group: 4 },
  { name: '浙江省', value: 2000, group: 5 },
  { name: '广东省', value: 2200, group: 6 },
  { name: '四川省', value: 2400, group: 7 },
  { name: '湖南省', value: 2600, group: 8 },
  { name: '湖北省', value: 2800, group: 9 },
  { name: '安徽省', value: 3000, group: 10 },
  { name: '福建省', value: 3200, group: 11 },
  { name: '江西省', value: 3400, group: 12 },
  { name: '陕西省', value: 3600, group: 13 },
  { name: '黑龙江省', value: 3800, group: 14 },
  { name: '山西省', value: 4000, group: 15 },
  { name: '内蒙古自治区', value: 4200, group: 16 },
  { name: '吉林省', value: 4400, group: 17 },
  { name: '辽宁省', value: 4600, group: 18 },
  { name: '海南省', value: 4800, group: 19 },
  { name: '宁夏回族自治区', value: 5000, group: 20 },
  { name: '青海省', value: 5200, group: 21 },
  { name: '西藏自治区', value: 5400, group: 22 },
  { name: '台湾省', value: 5600, group: 23 },
  { name: '香港特别行政区', value: 5800, group: 24 },
  { name: '澳门特别行政区', value: 6000, group: 25 },
])
</script>

<template>
  <div class="w-full flex h-[700px]">
    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <PositionTrendCard
        title="招聘职位总个数"
        :value="12580"
        indicator-desc="职位数量"
        quantifier="个"
        :chart-data="chart1Data"
        :change-rate="12.5"
        change-label="较上月"
        :colors="['#80FFA5']"
      />
      <PositionRankCard
        title-icon="icon-gangwei"
        title-icon-size="22px"
        title="招聘职位总个数排行"
        subtext="按照省份排行"
        indicator-desc="职位数量"
        quantifier="个"
        :chart-data="chart2Data"
        :bar-colors="['rgba(128, 255, 165, 0.9)', 'rgba(173, 253, 197, 0.4)']"
        tooltip-title="招聘职位个数"
        :is-stat-all="true"
        :is-stat-year="false"
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
          :title="props.province"
          :data="mapData"
          :map-name="mapName"
          legend-title="招聘总人数"
          quantifier="人"
          :zoom="mapName === 'china' ? 1.2 : 0.8"
          :center="mapName === 'china' ? ['50%', '60%'] : ['40%', '45%']"
          :tooltip-formatter="tooltipFormatter"
        />
      </div>
    </div>

    <div class="w-[21%] h-full grid grid-cols-1 grid-rows-2 gap-4">
      <PositionTrendCard
        title="招聘需求总人数"
        :value="12580"
        indicator-desc="招聘需求总人数"
        quantifier="人"
        :chart-data="chart1Data"
        :change-rate="12.5"
        change-label="较上月"
        :colors="['#FFBF00']"
      />
      <PositionRankCard
        title-icon="icon-renyuan"
        title-icon-size="22px"
        title="招聘总人数排行"
        subtext="按照省份排行"
        indicator-desc="招聘总人数"
        quantifier="人"
        :chart-data="chart2Data"
        :bar-colors="['rgba(255, 191, 0, 0.9)', 'rgba(255, 191, 0, 0.4)']"
        tooltip-title="招聘总人数"
        :is-stat-all="true"
        :is-stat-year="false"
      />
    </div>
  </div>
</template>
