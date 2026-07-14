<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import HorizontalBarChart from '@base/components/Echart/HorizontalBarChart.vue'
import DoughnutChart from '@base/components/Echart/DoughnutChart.vue'
import BarChart from '@base/components/Echart/BarChart.vue'
import LinesChart from '@base/components/Echart/LinesChart.vue'
import StatCard from './common/StatCard.vue'
import MapChart from './Echart/MapChart.vue'
import BarLineChart from './Echart/BarLineChart.vue'
// import HorizontalBarChart from '~/components/Echart/HorizontalBarChart.vue'
import PositionTrend from './Position/PositionTrend.vue'
import CardPanel from './common/CardPanel.vue'
import YearSelectModal from './common/YearSelectModal.vue'
import DateSelect from './common/DateSelect.vue'
import ProvinceSelectModal from '~/components/common/ProvinceSelectModal.vue'
import allMock from '~/data/positionData.json'

import { generateJobData } from '~/utils/mockDataGenerator'

const showModal = ref(false)
const currentRegion = ref('全国')
const selectedStats = ref('岗位数量')

const dateType = ref<'year' | 'month' | '5years'>('year')
const now = new Date()
const currentYear = ref(now.getFullYear())
const currentMonth = ref(`${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`)
const dynamicChartData = ref(generateJobData('全国', now.getFullYear()))
const staticChartData = computed(() => allMock[currentRegion.value] || allMock['全国'])

// 岗位趋势图表数据
const trendData = ref(staticChartData.value.trendData)

watch(
  [currentRegion, dateType, currentYear, currentMonth],
  () => {
    const month = dateType.value === 'month' ? currentMonth.value : undefined
    dynamicChartData.value = generateJobData(currentRegion.value, currentYear.value, month)
    // 岗位趋势图表数据生成逻辑
    if (dateType.value === '5years') {
      // 生成近5年趋势数据
      const years = Array.from({ length: 5 }, (_, i) => currentYear.value - 4 + i)
      trendData.value = years.map((year, idx) => ({
        name: String(year),
        jobCount: Math.round(10000 + Math.random() * 10000 + idx * 2000),
        recruitCount: Math.round(20000 + Math.random() * 10000 + idx * 3000)
      }))
    } else if (dateType.value === 'year') {
      // 生成12个月趋势数据
      trendData.value = Array.from({ length: 12 }, (_, i) => {
        const monthStr = String(i + 1).padStart(2, '0')
        return {
          name: `${currentYear.value}-${monthStr}`,
          jobCount: Math.round(10000 + Math.random() * 10000 + i * 500),
          recruitCount: Math.round(20000 + Math.random() * 10000 + i * 800)
        }
      })
    } else if (dateType.value === 'month') {
      // 生成当前月的每日趋势数据
      const days = 30
      trendData.value = Array.from({ length: days }, (_, i) => {
        const dayStr = String(i + 1).padStart(2, '0')
        return {
          name: `${currentMonth.value}-${dayStr}`,
          jobCount: Math.round(1000 + Math.random() * 500 + i * 10),
          recruitCount: Math.round(2000 + Math.random() * 500 + i * 15)
        }
      })
    }
  },
  { immediate: true }
)

const stats = computed(() => ({
  jobCount: dynamicChartData.value.jobCount,
  totalRecruit: dynamicChartData.value.totalRecruit.toLocaleString()
}))

function openModal(selectedValue: string) {
  selectedStats.value = selectedValue
  showModal.value = true
}

function handleSelect(region) {
  currentRegion.value = region
  showModal.value = false
}

const barTab = ref('region')
const barTabs = [
  { key: 'region', label: '地区' },
  { key: 'industry', label: '标准行业' },
  { key: 'career', label: '标准职业' }
]

const barChartData = computed(() => {
  if (!dynamicChartData.value) return []
  return dynamicChartData.value[barTab.value + 'Ranking'] || []
})

const rightBarTab = ref('education')
const rightBarTabs = [
  { key: 'education', label: '学历' },
  { key: 'experience', label: '工作年限' },
  { key: 'companyType', label: '单位规模' }
]

const router = useRouter()

// 跳转到岗位列表
const goToJobList1 = () => {
  console.log('goToJobList')
  router.push('/position-list')
}
</script>

<template>
  <div class="flex h-full flex-col">
    <!-- 上方统计区 -->
    <div class="mb-4 flex items-center justify-center gap-6 relative">
      <div class="flex gap-4">
        <StatCard
          :title="currentRegion + '岗位总数量'"
          :value="stats.jobCount"
          :highlight="selectedStats === '岗位数量'"
          unit="个"
          @click="openModal('岗位数量')"
        />
        <StatCard
          :title="currentRegion + '招聘需求总人数'"
          :value="stats.totalRecruit"
          :highlight="selectedStats === '招聘总人数'"
          unit="人"
          @click="openModal('招聘总人数')"
        />
      </div>
      <!-- 右侧切换和日期选择 -->
      <DateSelect
        :date-type="dateType"
        :year="currentYear"
        :month="currentMonth"
        class="ml-8 absolute top-3 right-0"
        @update:date-type="(val) => (dateType = val)"
        @update:year="(val) => (currentYear = val)"
        @update:month="(val) => (currentMonth = val)"
      />
    </div>
    <div class="flex flex-1 gap-4">
      <!-- 左侧 -->
      <div class="flex h-full w-1/5 flex-col gap-4">
        <CardPanel class="flex flex-1 flex-col">
          <template #title>{{ currentRegion }}岗位趋势</template>
          <LinesChart
            :data="trendData"
            :series="[
              { name: '岗位数量', dataKey: 'jobCount', color: '#38bdf8' },
              { name: '招聘总人数', dataKey: 'recruitCount', color: '#00eaff' }
            ]"
          />
        </CardPanel>
        <CardPanel class="flex flex-1 flex-col">
          <template #title>
            {{ currentRegion }}{{ selectedStats }}{{ currentRegion === '全国' ? '省份' : '地区' }}排行
          </template>
          <div class="flex items-center justify-end mt-2">
            <div class="flex gap-2">
              <span
                v-for="tab in barTabs"
                :key="tab.key"
                :class="[
                  'cursor-pointer select-none px-4 py-1 rounded-lg text-sm font-semibold transition-all duration-150',
                  barTab === tab.key
                    ? 'bg-gradient-to-r from-cyan-400/60 to-blue-500/60 text-white shadow-lg ring-2 ring-cyan-300'
                    : 'bg-white/5 text-cyan-300 hover:bg-cyan-400/20 hover:text-cyan-200'
                ]"
                style="box-shadow: 0 0 8px 0 #00eaff44"
                @click="barTab = tab.key"
              >
                {{ tab.label }}
              </span>
            </div>
          </div>
          <HorizontalBarChart
            v-if="barChartData"
            :data="barChartData"
            height="230px"
            unit="元"
            tooltip-title="薪资中位数"
            :item-style="{
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: 'red' },
                { offset: 1, color: 'yellow' }
              ]
            }"
          />
        </CardPanel>
        <CardPanel class="flex flex-1 flex-col">
          <template #title>
            {{ selectedStats === '岗位数量' ? '热门岗位Top20' : '岗位招聘总人数Top20' }}
          </template>
          <template #button>
            <span
              class="px-3 py-1 text-xs bg-gradient-to-r from-cyan-400 to-blue-500 text-white rounded hover:from-cyan-500 hover:to-blue-600 transition-all duration-200"
              @click="goToJobList1"
            >
              更多
            </span>
          </template>
          <HorizontalBarChart :data="dynamicChartData.topJob" unit="人" height="230px" />
        </CardPanel>
      </div>
      <!-- 中间地图 -->
      <div class="flex h-full flex-1 items-center justify-center">
        <MapChart
          :data="dynamicChartData.map"
          :title="`${currentRegion}岗位分布`"
          :region="currentRegion"
          :map-name="currentRegion === '全国' ? 'china' : currentRegion"
        />
      </div>
      <!-- 右侧 -->
      <div class="flex h-full w-1/4 flex-col gap-4">
        <CardPanel class="flex flex-1 flex-col">
          <template #title>三大产业对应的{{ selectedStats }}</template>
          <BarChart
            :data="staticChartData.threeIndustry"
            height="220px"
            :tooltip-title="selectedStats"
            :unit="selectedStats === '岗位数量' ? '个' : '人'"
          />
        </CardPanel>
        <!-- 学历、年限下有多少岗位招聘多少人 -->
        <CardPanel class="flex flex-1 flex-col">
          <template #title>学历与年限分布</template>
          <div class="flex items-center justify-end mt-2">
            <div class="flex gap-2">
              <span
                v-for="tab in rightBarTabs"
                :key="tab.key"
                :class="[
                  'cursor-pointer select-none px-4 py-1 rounded-lg text-sm font-semibold transition-all duration-150',
                  rightBarTab === tab.key
                    ? 'bg-gradient-to-r from-cyan-400/60 to-blue-500/60 text-white shadow-lg ring-2 ring-cyan-300'
                    : 'bg-white/5 text-cyan-300 hover:bg-cyan-400/20 hover:text-cyan-200'
                ]"
                style="box-shadow: 0 0 8px 0 #00eaff44"
                @click="rightBarTab = tab.key"
              >
                {{ tab.label }}
              </span>
            </div>
          </div>
          <DoughnutChart
            :data="staticChartData.educationExp[rightBarTab]"
            :tooltip-title="selectedStats"
            height="200px"
            unit="家"
          />
        </CardPanel>
        <!-- 不同规模下招聘总人数和发布的岗位 -->
        <CardPanel class="flex flex-1 flex-col">
          <template #title>单位规模分布</template>
          <DoughnutChart :data="staticChartData.companyType" tooltip-title="招聘单位" height="200px" unit="家" />
        </CardPanel>
      </div>
    </div>
    <ProvinceSelectModal
      :show="showModal"
      :selected="currentRegion"
      @select="handleSelect"
      @close="showModal = false"
    />
  </div>
</template>
