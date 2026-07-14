<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import Card from '../common/Card.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import IndustryFilter from '../common/Filter/IndustryFilter.vue'
import Icon from '../common/Icon.vue'
import Tooltip from '../common/Tooltip.vue'
import { industryCategoryMap } from '../../utils/constants'

const props = defineProps<{
  companyScaleName: string
  province: string
  time: string
  scope: string
}>()

const pieData = ref([
  { value: 1048, name: '第一产业' },
  { value: 735, name: '第二产业' },
  { value: 580, name: '第三产业' },
])

const mockMenleiData = [
  {
    name: '农、林、牧、渔业',
    values: [
      { name: '招聘单位总个数', value: 8200 },
      { name: '招聘需求总人数', value: 13500 },
    ],
  },
  {
    name: '采矿业',
    values: [
      { name: '招聘单位总个数', value: 3100 },
      { name: '招聘需求总人数', value: 5200 },
    ],
  },
  {
    name: '制造业',
    values: [
      { name: '招聘单位总个数', value: 15000 },
      { name: '招聘需求总人数', value: 21000 },
    ],
  },
  {
    name: '电力、热力、燃气及水生产和供应业',
    values: [
      { name: '招聘单位总个数', value: 4200 },
      { name: '招聘需求总人数', value: 7800 },
    ],
  },
  {
    name: '建筑业',
    values: [
      { name: '招聘单位总个数', value: 9800 },
      { name: '招聘需求总人数', value: 14200 },
    ],
  },
  {
    name: '批发和零售业',
    values: [
      { name: '招聘单位总个数', value: 11200 },
      { name: '招聘需求总人数', value: 16800 },
    ],
  },
  {
    name: '交通运输、仓储和邮政业',
    values: [
      { name: '招聘单位总个数', value: 6700 },
      { name: '招聘需求总人数', value: 10500 },
    ],
  },
  {
    name: '住宿和餐饮业',
    values: [
      { name: '招聘单位总个数', value: 8900 },
      { name: '招聘需求总人数', value: 12300 },
    ],
  },
  {
    name: '信息传输、软件和信息技术服务业 ',
    values: [
      { name: '招聘单位总个数', value: 5400 },
      { name: '招聘需求总人数', value: 9600 },
    ],
  },
  {
    name: '金融业 ',
    values: [
      { name: '招聘单位总个数', value: 3700 },
      { name: '招聘需求总人数', value: 8200 },
    ],
  },
  {
    name: '房地产业',
    values: [
      { name: '招聘单位总个数', value: 6100 },
      { name: '招聘需求总人数', value: 9900 },
    ],
  },
  {
    name: '租赁和商务服务业',
    values: [
      { name: '招聘单位总个数', value: 7600 },
      { name: '招聘需求总人数', value: 11800 },
    ],
  },
]

const mockNLMFYZhongleiData = [
  {
    name: '农业',
    value: 'A-01',
    values: [
      { name: '招聘单位总个数', value: 9500 },
      { name: '招聘需求总人数', value: 12000 },
    ],
  },
  {
    name: '林业',
    value: 'A-02',
    values: [
      { name: '招聘单位总个数', value: 4200 },
      { name: '招聘需求总人数', value: 10500 },
    ],
  },
  {
    name: '畜牧业',
    value: 'A-03',
    values: [
      { name: '招聘单位总个数', value: 6700 },
      { name: '招聘需求总人数', value: 11500 },
    ],
  },
  {
    name: '渔业',
    value: 'A-04',
    values: [
      { name: '招聘单位总个数', value: 3100 },
      { name: '招聘需求总人数', value: 9800 },
    ],
  },
  {
    name: '农、林、牧、渔专业及辅助性活动',
    value: 'A-05',
    values: [
      { name: '招聘单位总个数', value: 5200 },
      { name: '招聘需求总人数', value: 10800 },
    ],
  },
]

const industry = ref('')
const industryLabel = ref('')
const industryLevel = ref('1')
const title = ref('全规模单位的标准行业（全部门类）关键数据分布')
const tooltipTitle = ref('')
const data = ref([])

const handleIndustryChange = (value: string, label: string, level: string) => {
  industry.value = value
  industryLabel.value = label
  industryLevel.value = level
  title.value =
    (props.companyScaleName || '全部规模') + `单位的标准行业（${label || '全部门类'}）关键数据分布`

  if (level === '1') {
    data.value = mockNLMFYZhongleiData
  } else {
    data.value = mockMenleiData
  }
}

onMounted(() => {
  data.value = mockMenleiData
})

watch(
  () => props.companyScaleName,
  newValue => {
    title.value =
      (newValue || '全部规模') +
      `单位的标准行业（${industryLabel.value || '全部门类'}）关键数据分布`
    tooltipTitle.value = newValue ? `（仅${newValue}规模单位）` : '（全部规模单位）'
  }
)
</script>

<template>
  <div class="w-full bg-white/5 backdrop-blur-sm rounded-lg p-4 mt-6">
    <!-- 主标题 -->
    <FifthTitle title="国民经济行业和招聘单位" size="md" icon="icon-dianlihangye" />
    <div class="grid grid-cols-12 gap-4 mt-4">
      <Card class="col-span-3">
        <FirstTitle :title="`三大产业${props.companyScaleName || ''}招聘单位分布`" class="mb-4" />
        <GradientBarChart
          height="240px"
          :data="pieData"
          :x-axis-rotate="0"
          :bar-gradient="{
            startColor: '#6dd0ed',
            endColor: '#92e4d0',
          }"
          :grid="{
            top: '20%',
            bottom: '2%',
            left: '3%',
            right: '3%',
          }"
          :label-style="{
            fontSize: 11,
            color: '#6dd0ed',
          }"
          tooltip-title="标准单位总个数"
          quantifier="个"
        />
      </Card>

      <Card class="col-span-9">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2 max-w-[400px]">
              <div
                class="w-10 h-10 rounded-full bg-[#00ffff]/10 flex items-center justify-center flex-shrink-0"
              >
                <Icon name="icon-a-zhexiantu4" size="20" color="#00ffff" />
              </div>
              <span class="text-sm font-medium text-[#00ffff] flex-1 whitespace-wrap">{{
                title
              }}</span>
            </div>
            <IndustryFilter v-model="industry" @change="handleIndustryChange" />
          </div>
          <div class="cursor-help mr-8">
            <Tooltip placement="bottom">
              <template #trigger>
                <Icon name="icon-tishi" size="24" color="#00ffff" />
              </template>
              <div class="min-w-32">
                <div class="font-bold mb-1 text-sm text-gray-600">指标描述：</div>
                <div class="text-xs text-gray-400 whitespace-nowrap break-all">
                  <span>单位规模：</span>
                  <span class="font-bold">{{ props.companyScaleName || '全部规模' }}</span>
                </div>
                <div class="text-xs text-gray-400 whitespace-nowrap break-all">
                  <span>标准行业：</span>
                  <span class="font-bold"
                    >{{ industryLabel || '全部'
                    }}{{ industryLabel ? `（${industryCategoryMap[industryLevel]}）` : '' }}</span
                  >
                </div>
                <div class="text-xs text-gray-400 whitespace-nowrap break-all">
                  <span>图表数据：</span>
                  <span class="font-bold"
                    >{{ industryLabel ? '该标准行业' : ''
                    }}{{
                      industryLevel === '1'
                        ? '下的所有大类'
                        : industryLevel === '2'
                        ? '下的所有中类'
                        : industryLevel === '3'
                        ? '下的所有小类'
                        : '标准行业所有门类'
                    }}行业的招聘单位总个数和招聘单位总个数分布</span
                  >
                </div>
              </div>
            </Tooltip>
          </div>
        </div>
        <div class="w-full h-[240px]">
          <LineBarDualAxisChart
            :data="data"
            left-unit="万"
            left-quantifier="个"
            right-unit="万"
            right-quantifier="人"
            left-color="#b39ddb"
            right-color="#AAD8E8"
            is-smooth-line
            :tooltip-title="tooltipTitle"
            height="240px"
            :x-axis-label-rotate="data.length < 11 ? 0 : 30"
          />
        </div>
      </Card>
    </div>
  </div>
</template>
