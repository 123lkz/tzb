<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import FifthTitle from '~/components/common/Title/FifthTitle.vue'
import Card from '~/components/common/Card.vue'
import SecondTitle from '~/components/common/Title/SecondTitle.vue'
import GradientBarChart from '~/components/Echart/GradientBarChart.vue'
import TwoFilter from '~/components/common/Filter/TwoFilter.vue'

interface Props {
  province?: string
  time?: string
  scope?: string
  industryLabel?: string
  industryLevel?: string
}

const _props = withDefaults(defineProps<Props>(), {
  province: '全国',
  time: 'month',
  scope: 'all',
  industryLabel: '',
  industryLevel: '1'
})

// 三大产业选项
const threeIndustriesOptions = [
  { value: '1', label: '第一产业' },
  { value: '2', label: '第二产业' },
  { value: '3', label: '第三产业' }
]

// 分行业选项
const subIndustryOptions = [
  { value: 'A', label: '农、林、牧、渔业' },
  { value: 'B', label: '采矿业' },
  { value: 'C', label: '制造业' },
  { value: 'D', label: '电力、热力、燃气及水生产和供应业' },
  { value: 'E', label: '建筑业' },
  { value: 'F', label: '批发和零售业' },
  { value: 'G', label: '交通运输、仓储和邮政业' },
  { value: 'H', label: '住宿和餐饮业' },
  { value: 'I', label: '信息传输、软件和信息技术服务业' },
  { value: 'J', label: '金融业' },
  { value: 'K', label: '房地产业' },
  { value: 'L', label: '租赁和商务服务业' },
  { value: 'M', label: '科学研究和技术服务业' },
  { value: 'N', label: '水利、环境和公共设施管理业' },
  { value: 'O', label: '居民服务、修理和其他服务业' },
  { value: 'P', label: '教育' },
  { value: 'Q', label: '卫生和社会工作' },
  { value: 'R', label: '文化、体育和娱乐业' },
  { value: 'S', label: '公共管理、社会保障和社会组织' },
  { value: 'T', label: '国际组织' }
]

// 选择器状态
const selectedThreeIndustries = ref('1')
const selectedSubIndustry1 = ref('A')
const selectedSubIndustry2 = ref('B')
const selectedSubIndustry3 = ref('C')
const selectedSubIndustry4 = ref('D')

// 图表引用
const chartRef1 = ref<HTMLElement>()
const chartRef2 = ref<HTMLElement>()
const chartRef3 = ref<HTMLElement>()
const chartRef4 = ref<HTMLElement>()

let chart1: echarts.ECharts
let chart2: echarts.ECharts
let chart3: echarts.ECharts
let chart4: echarts.ECharts

// 初始化第一个图表（柱状图）
const initChart1 = () => {
  if (!chartRef1.value) return

  chart1 = (echarts as any).init(chartRef1.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月'],
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#666'
      }
    },
    series: [
      {
        name: '就业人数',
        type: 'bar',
        data: [120, 132, 101, 134, 90, 230],
        itemStyle: {
          color: new (echarts as any).graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        }
      }
    ]
  }

  chart1.setOption(option)
}

// 初始化第二个图表（折线图）
const initChart2 = () => {
  if (!chartRef2.value) return

  chart2 = (echarts as any).init(chartRef2.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月'],
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#666'
      }
    },
    series: [
      {
        name: '薪资水平',
        type: 'line',
        data: [820, 932, 901, 934, 1290, 1330],
        smooth: true,
        lineStyle: {
          color: '#91cc75',
          width: 3
        },
        itemStyle: {
          color: '#91cc75'
        }
      }
    ]
  }

  chart2.setOption(option)
}

// 初始化第三个图表（饼图）
const initChart3 = () => {
  if (!chartRef3.value) return

  chart3 = (echarts as any).init(chartRef3.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: {
        color: '#666'
      }
    },
    series: [
      {
        name: '行业分布',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 1048, name: '制造业' },
          { value: 735, name: '服务业' },
          { value: 580, name: '农业' },
          { value: 484, name: '建筑业' },
          { value: 300, name: '其他' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  chart3.setOption(option)
}

// 初始化第四个图表（雷达图）
const initChart4 = () => {
  if (!chartRef4.value) return

  chart4 = (echarts as any).init(chartRef4.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: [
        { name: '就业机会', max: 100 },
        { name: '薪资水平', max: 100 },
        { name: '发展前景', max: 100 },
        { name: '工作环境', max: 100 },
        { name: '技能要求', max: 100 }
      ],
      axisName: {
        color: '#666'
      }
    },
    series: [
      {
        name: '行业评估',
        type: 'radar',
        data: [
          {
            value: [85, 90, 80, 75, 85],
            name: '当前行业'
          }
        ],
        areaStyle: {
          color: 'rgba(255, 193, 7, 0.3)'
        },
        lineStyle: {
          color: '#ffc107'
        },
        itemStyle: {
          color: '#ffc107'
        }
      }
    ]
  }

  chart4.setOption(option)
}

// 监听选择器变化
watch(
  [selectedThreeIndustries, selectedSubIndustry1, selectedSubIndustry2, selectedSubIndustry3, selectedSubIndustry4],
  () => {
    // 这里可以添加数据更新逻辑
    console.log('选择器变化:', {
      threeIndustries: selectedThreeIndustries.value,
      subIndustry1: selectedSubIndustry1.value,
      subIndustry2: selectedSubIndustry2.value,
      subIndustry3: selectedSubIndustry3.value,
      subIndustry4: selectedSubIndustry4.value
    })
  }
)

const pieData1 = ref([
  { value: 1048, name: '第一产业' },
  { value: 735, name: '第二产业' },
  { value: 580, name: '第三产业' }
])

const pieData2 = ref([
  { value: 1048, name: '农林牧渔业' },
  { value: 735, name: '采矿业' },
  { value: 580, name: '建筑业' },
  { value: 580, name: '批发和零售业' },
  { value: 580, name: '交通运输、仓储和邮政业' },
  { value: 580, name: '住宿和餐饮业' },
  { value: 580, name: '信息传输、软件和信息技术服务业' },
  { value: 580, name: '金融业' },
  { value: 580, name: '房地产业' },
  { value: 580, name: '制造业' },
  { value: 580, name: '电力、热力、燃气及水生产和供应业' }
])

onMounted(() => {
  initChart1()
  initChart2()
  initChart3()
  initChart4()

  // 窗口大小变化时重绘
  window.addEventListener('resize', () => {
    chart1?.resize()
    chart2?.resize()
    chart3?.resize()
    chart4?.resize()
  })
})

const filterType = ref('tertiaryIndustry')

const filterOptions = ref([
  { value: 'tertiaryIndustry', label: '按照三次产业' },
  { value: 'industryCategory', label: '按照国民经济行业门类' }
])

const handleThreeIndustriesChange = (type: string) => {
  filterType.value = type
}
</script>

<template>
  <div class="w-full flex flex-col bg-white/10 p-4 rounded-lg">
    <!-- 上部分：标题区域 -->
    <div class="relative mb-4">
      <FifthTitle
        title="国家统计局行业统计数据"
        icon="icon-quyu"
        suffix-icon="icon-ding"
        size="md"
        :show-btm-line="false"
      />
      <div class="absolute left-60 top-1">
        <TwoFilter :options="filterOptions" @on-change="handleThreeIndustriesChange" />
      </div>
    </div>

    <div class="grid gap-4" :class="[filterType === 'tertiaryIndustry' ? 'grid-cols-4' : 'grid-cols-2']">
      <Card>
        <SecondTitle
          title="就业人数统计"
          icon="icon-hrcollegepeopleCardingRange"
          icon-size="20"
          class="mb-4"
          size="md"
          subtext="2023年就业人数(最新统计)"
        />
        <GradientBarChart
          :key="filterType"
          height="200px"
          :data="filterType === 'tertiaryIndustry' ? pieData1 : pieData2"
          :x-axis-rotate="filterType === 'tertiaryIndustry' ? 0 : 45"
          :bar-gradient="{
            startColor: '#6dd0ed',
            endColor: '#92e4d0'
          }"
          :grid="{
            top: '20%',
            bottom: '2%',
            left: '3%',
            right: '3%'
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed'
          }"
          tooltip-title="就业人数"
          quantifier="人"
          :text-truncation="true"
          :auto-scroll="true"
        />
      </Card>

      <Card>
        <SecondTitle
          title="就业人员平均工资"
          icon="icon-hrcollegepeopleCardingRange"
          icon-size="20"
          class="mb-4"
          size="md"
          subtext="2023年就业人员平均工资(最新统计)"
        />
        <GradientBarChart
          :key="filterType"
          height="200px"
          :data="filterType === 'tertiaryIndustry' ? pieData1 : pieData2"
          :x-axis-rotate="filterType === 'tertiaryIndustry' ? 0 : 45"
          :bar-gradient="{
            startColor: '#b39ddb',
            endColor: '#e1bee7'
          }"
          :grid="{
            top: '20%',
            bottom: '2%',
            left: '3%',
            right: '3%'
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed'
          }"
          tooltip-title="就业人员平均工资"
          quantifier="元"
          :text-truncation="true"
          :auto-scroll="true"
        />
      </Card>

      <Card>
        <SecondTitle
          title="法人单位数"
          icon="icon-hrcollegepeopleCardingRange"
          icon-size="20"
          class="mb-4"
          size="md"
          subtext="2023年法人单位数(最新统计)"
        />
        <GradientBarChart
          :key="filterType"
          height="200px"
          :data="filterType === 'tertiaryIndustry' ? pieData1 : pieData2"
          :x-axis-rotate="filterType === 'tertiaryIndustry' ? 0 : 45"
          :grid="{
            top: '20%',
            bottom: '2%',
            left: '3%',
            right: '3%'
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed'
          }"
          tooltip-title="法人单位数"
          quantifier="个"
          :text-truncation="true"
          :auto-scroll="true"
        />
      </Card>

      <Card>
        <SecondTitle
          title="国内生产总值"
          icon="icon-hrcollegepeopleCardingRange"
          icon-size="20"
          class="mb-4"
          size="md"
          subtext="2024年国内生产总值(最新统计)"
        />
        <GradientBarChart
          :key="filterType"
          height="200px"
          :data="filterType === 'tertiaryIndustry' ? pieData1 : pieData2"
          :x-axis-rotate="filterType === 'tertiaryIndustry' ? 0 : 45"
          :bar-gradient="{
            startColor: '#80FFA5',
            endColor: '#adfdc5'
          }"
          :grid="{
            top: '20%',
            bottom: '2%',
            left: '3%',
            right: '3%'
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed'
          }"
          tooltip-title="国内生产总值"
          quantifier="亿元"
          :text-truncation="true"
          :auto-scroll="true"
        />
      </Card>
    </div>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
