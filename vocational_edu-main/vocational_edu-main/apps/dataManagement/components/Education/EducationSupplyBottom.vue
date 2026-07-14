<script setup lang="ts">
import SecondTitle from '../common/Title/SecondTitle.vue'
import RankList from '../common/RankList/RankList.vue'
import ProportionCard from '../common/ProportionCard.vue'
import PieChart from '../Echart/PieChart.vue'
import NightingaleChart from '../Echart/NightingaleChart.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import { schoolTypeMap } from '~/utils/constants'

const props = withDefaults(
  defineProps<{
    schoolType: string
    year: string
  }>(),
  {
    schoolType: 'all',
    year: '2023',
  }
)

const changeRate = ref(14.52)
const proportionBarChartData = ref([
  {
    name: '2024',
    values: [
      {
        name: '本科院校',
        value: 124,
      },
      {
        name: '专科院校',
        value: 100,
      },
    ],
  },
  {
    name: '2023',
    values: [
      {
        name: '本科院校',
        value: 145,
      },
      {
        name: '专科院校',
        value: 100,
      },
    ],
  },
  {
    name: '2022',
    values: [
      {
        name: '本科院校',
        value: 150,
      },
      {
        name: '专科院校',
        value: 150,
      },
    ],
  },
  {
    name: '2021',
    values: [
      {
        name: '本科院校',
        value: 150,
      },
      {
        name: '专科院校',
        value: 100,
      },
    ],
  },
  {
    name: '2020',
    values: [
      {
        name: '本科院校',
        value: 100,
      },
      {
        name: '专科院校',
        value: 100,
      },
    ],
  },
])

const rankListTitle = computed(() => {
  return `${
    props.schoolType === 'all'
      ? '全部专业'
      : props.schoolType === 'undergraduate'
      ? '本科专业'
      : '专科专业'
  }学生数排行`
})

const majorStudentRecruitmentData = ref([
  {
    name: '护理',
    value: 148014,
  },
  {
    name: '大数据与会计',
    value: 84417,
  },
  {
    name: '电子商务',
    value: 71159,
  },
  {
    name: '工程造价',
    value: 62915,
  },
  {
    name: '计算机应用技术',
    value: 62653,
  },
  {
    name: '学前教育（师范类）',
    value: 58336,
  },
  {
    name: '会计',
    value: 53445,
  },
  {
    name: '机电一体化技术',
    value: 52023,
  },
  {
    name: '软件技术',
    value: 51481,
  },
  {
    name: '学前教育',
    value: 51292,
  },
  {
    name: '院校整体（普通类 ）',
    value: 51088,
  },
  {
    name: '临床医学',
    value: 45197,
  },
  {
    name: '计算机网络技术',
    value: 42777,
  },
  {
    name: '建筑工程技术',
    value: 42656,
  },
  {
    name: '市场营销',
    value: 36226,
  },
  {
    name: '口腔医学',
    value: 35288,
  },
  {
    name: '电气自动化技术',
    value: 33929,
  },
  {
    name: '药学',
    value: 32681,
  },
  {
    name: '旅游管理',
    value: 29696,
  },
  {
    name: '大数据技术',
    value: 28072,
  },
  {
    name: '新能源汽车技术',
    value: 27634,
  },
  {
    name: '物联网应用技术',
    value: 27402,
  },
  {
    name: '工业机器人技术',
    value: 25081,
  },
  {
    name: '商务英语',
    value: 24496,
  },
  {
    name: '医学检验技术',
    value: 23801,
  },
  {
    name: '现代物流管理',
    value: 23674,
  },
  {
    name: '建筑室内设计',
    value: 23474,
  },
  {
    name: '康复治疗技术',
    value: 22382,
  },
  {
    name: '医学影像技术',
    value: 19798,
  },
  {
    name: '中药学',
    value: 19566,
  },
  {
    name: '汽车检测与维修技术',
    value: 19367,
  },
  {
    name: '学前教育（师范）',
    value: 18717,
  },
  {
    name: '大数据与财务管理',
    value: 17680,
  },
  {
    name: '中医学',
    value: 17159,
  },
  {
    name: '数控技术',
    value: 16634,
  },
  {
    name: '数字媒体技术',
    value: 16134,
  },
  {
    name: '小学教育（师范类）',
    value: 15672,
  },
  {
    name: '动漫制作技术',
    value: 15413,
  },
  {
    name: '空中乘务',
    value: 15189,
  },
  {
    name: '城市轨道交通运营管理',
    value: 15126,
  },
  {
    name: '工商企业管理',
    value: 15100,
  },
  {
    name: '电子信息工程技术',
    value: 15003,
  },
  {
    name: '机械制造及自动化',
    value: 14600,
  },
  {
    name: '酒店管理与数字化运营',
    value: 14597,
  },
  {
    name: '物流管理',
    value: 14552,
  },
  {
    name: '助产',
    value: 14162,
  },
  {
    name: '口腔医学技术',
    value: 13884,
  },
  {
    name: '婴幼儿托育服务与管理',
    value: 12918,
  },
  {
    name: '大数据技术与应用',
    value: 12793,
  },
  {
    name: '无人机应用技术',
    value: 12778,
  },
  {
    name: '建设工程管理',
    value: 12649,
  },
  {
    name: '针灸推拿',
    value: 12601,
  },
  {
    name: '金融服务与管理',
    value: 11999,
  },
  {
    name: '小学教育（师范）',
    value: 11824,
  },
  {
    name: '法律事务',
    value: 11606,
  },
  {
    name: '人工智能技术应用',
    value: 11502,
  },
  {
    name: '财务管理',
    value: 11301,
  },
  {
    name: '跨境电子商务',
    value: 10972,
  },
  {
    name: '建筑装饰工程技术',
    value: 10829,
  },
  {
    name: '国际经济与贸易',
    value: 10311,
  },
  {
    name: '药品经营与管理',
    value: 10149,
  },
  {
    name: '应用化工技术',
    value: 9767,
  },
  {
    name: '智能控制技术',
    value: 9608,
  },
  {
    name: '畜牧兽医',
    value: 9264,
  },
  {
    name: '应用电子技术',
    value: 9258,
  },
  {
    name: '药品生产技术',
    value: 9251,
  },
  {
    name: '人力资源管理',
    value: 9166,
  },
  {
    name: '小学语文教育（师范类）',
    value: 8965,
  },
  {
    name: '应用英语',
    value: 8821,
  },
  {
    name: '小学教育',
    value: 8814,
  },
  {
    name: '酒店管理',
    value: 8647,
  },
  {
    name: '机械设计与制造',
    value: 8625,
  },
  {
    name: '汽车制造与试验技术',
    value: 8531,
  },
  {
    name: '云计算技术应用',
    value: 8528,
  },
  {
    name: '工程测量技术',
    value: 8298,
  },
  {
    name: '机械制造与自动化',
    value: 8119,
  },
  {
    name: '道路与桥梁工程技术',
    value: 8095,
  },
  {
    name: '高速铁路客运服务',
    value: 7818,
  },
  {
    name: '金融管理',
    value: 7721,
  },
  {
    name: '动物医学',
    value: 7693,
  },
  {
    name: '数字媒体应用技术',
    value: 7570,
  },
  {
    name: '环境工程技术',
    value: 7355,
  },
  {
    name: '食品检验检测技术',
    value: 7068,
  },
  {
    name: '新闻采编与制作',
    value: 6944,
  },
  {
    name: '信息安全技术应用',
    value: 6843,
  },
  {
    name: '建筑设计',
    value: 6800,
  },
  {
    name: '医学美容技术',
    value: 6698,
  },
  {
    name: '模具设计与制造',
    value: 6658,
  },
  {
    name: '眼视光技术',
    value: 6608,
  },
  {
    name: '幼儿发展与健康管理',
    value: 6441,
  },
  {
    name: '中医康复技术',
    value: 6373,
  },
  {
    name: '早期教育',
    value: 6224,
  },
  {
    name: '健康管理',
    value: 6211,
  },
  {
    name: '小学英语教育（师范类）',
    value: 6115,
  },
  {
    name: '电力系统自动化技术',
    value: 5836,
  },
  {
    name: '园林技术',
    value: 5783,
  },
  {
    name: '发电厂及电力系统',
    value: 5604,
  },
  {
    name: '城市轨道交通工程技术',
    value: 5535,
  },
  {
    name: '会计信息管理',
    value: 5490,
  },
  {
    name: '语文教育（师范类）',
    value: 5480,
  },
])

const pieChartData = ref([
  {
    name: '本科院校',
    value: 1275,
  },
  {
    name: '专科院校',
    value: 1545,
  },
])

const pie2ChartData = ref([
  {
    name: '双一流院校',
    value: 147,
  },
  {
    name: '普通本科院校',
    value: 1128,
  },
  {
    name: '双高计划院校',
    value: 197,
  },
  {
    name: '普通专科院校',
    value: 1348,
  },
])
</script>

<template>
  <div class="grid grid-cols-4 gap-4 mt-4">
    <div class="col-span-1">
      <div class="card">
        <SecondTitle
          :title="rankListTitle"
          type="circle"
          icon="icon-paihang"
          :icon-size="20"
          subtext="按专业的学生人数排行"
          :show-text-button="false"
        />
        <div class="relative flex flex-col flex-1 min-h-0 text-white/80">
          <RankList
            :data="majorStudentRecruitmentData"
            tooltip-title="学生人数"
            unit="人"
            :show-count="20"
            period="5"
          />
        </div>
      </div>
    </div>
    <div class="col-span-3 grid grid-cols-1 grid-rows-2 gap-4">
      <div class="grid grid-cols-3 gap-4">
        <ProportionCard
          :title="`${year}年${schoolTypeMap[schoolType]}招生数`"
          :tooltip-title="`年${schoolTypeMap[schoolType]}招生数`"
          :total="1234"
          unit="万"
          quantifier="人"
          :chart-data="proportionBarChartData"
          :change-rate="45"
        />
        <ProportionCard
          :title="`${year}年${schoolTypeMap[schoolType]}在校生数`"
          :tooltip-title="`年${schoolTypeMap[schoolType]}在校生数`"
          :total="3456"
          unit="万"
          quantifier="人"
          :chart-data="proportionBarChartData"
          :change-rate="-45"
          :colors="['#f7ab5a', '#fae62c']"
        />
        <ProportionCard
          :title="`${year}年${schoolTypeMap[schoolType]}毕业生数`"
          :tooltip-title="`年${schoolTypeMap[schoolType]}毕业生数`"
          :total="1234"
          unit="万"
          quantifier="人"
          :chart-data="proportionBarChartData"
          :change-rate="0"
          :colors="['#55bd96', '#48b6f3']"
        />
      </div>
      <div class="grid grid-cols-3 gap-4">
        <div
          class="col-span-2 h-full bg-[#00ffff]/10 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full flex-1 flex flex-col"
        >
          <FirstTitle title="学校总数量" />
          <div class="flex items-baseline justify-between gap-1 my-2">
            <div class="flex items-baseline justify-between gap-1 my-2">
              <div class="flex items-baseline gap-1">
                <span class="text-xl font-DIN-Medium font-bold text-[#00ffff]">{{
                  123456?.toLocaleString?.() ?? 0
                }}</span>
                <span class="text-xs text-white/70">所</span>
              </div>
            </div>
            <div class="flex items-center justify-between pt-3 gap-3">
              <span class="text-xs text-gray-300">较上一年</span>
              <div class="flex items-center gap-1">
                <Icon
                  v-if="changeRate > 0"
                  name="icon-shangsheng"
                  color="text-green-400"
                  :size="12"
                />
                <Icon
                  v-else-if="changeRate < 0"
                  name="icon-xiajiang"
                  color="text-red-400"
                  :size="12"
                />
                <span
                  class="text-xs font-medium"
                  :class="
                    changeRate > 0
                      ? 'text-green-400'
                      : changeRate < 0
                      ? 'text-red-400'
                      : 'text-gray-400'
                  "
                >
                  {{
                    changeRate === 0
                      ? '无变化'
                      : changeRate > 0
                      ? `+${changeRate.toFixed(2)}%`
                      : `${changeRate.toFixed(2)}%`
                  }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex">
            <PieChart
              title="按照本科/专科院校分类"
              :data="pieChartData"
              legend-position="bottom"
              height="200px"
              quantifier="所"
            />
            <NightingaleChart
              title="按照双一流/双高计划/普通本科专科分类"
              :data="pie2ChartData"
              legend-position="bottom"
              height="200px"
              quantifier="所"
              :radius="[10, 60]"
              :center="['50%', '50%']"
            />
          </div>
        </div>
        <div class="col-span-1">
          <ProportionCard
            :title="`${year}年${schoolTypeMap[schoolType]}教职工数`"
            :tooltip-title="`年${schoolTypeMap[schoolType]}教职工数`"
            :total="1234"
            unit="万"
            chart-height="210px"
            quantifier="人"
            :chart-data="proportionBarChartData"
            :change-rate="0"
            :colors="['#f67299', '#8466be']"
          />
        </div>
      </div>
    </div>
  </div>
</template>
