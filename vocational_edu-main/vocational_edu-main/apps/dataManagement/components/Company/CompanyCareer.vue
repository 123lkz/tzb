<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import Card from '../common/Card.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import CareerFilter from '../common/Filter/CareerFilter.vue'
import Icon from '../common/Icon.vue'
import Tooltip from '../common/Tooltip.vue'
import { careerCategoryMap } from '../../utils/constants'

const props = defineProps<{
  companyScaleName: string
  province: string
  time: string
  scope: string
}>()

const career = ref('')
const careerLabel = ref('')
const careerLevel = ref('')
const title = ref('全规模单位的标准职业（全部大类）关键数据分布')
const tooltipTitle = ref('')
const data = ref([])

const mockDaleiData = [
  {
    name: '党的机关、国家机关、群众团体和社会组织、企事业单位负责人',
    values: [
      { name: '单位总个数', value: 8200 },
      { name: '招聘总人数', value: 13500 },
    ],
  },
  {
    name: '专业技术人员',
    values: [
      { name: '单位总个数', value: 15000 },
      { name: '招聘总人数', value: 16000 },
    ],
  },
  {
    name: '办事人员和有关人员',
    values: [
      { name: '单位总个数', value: 9500 },
      { name: '招聘总人数', value: 12000 },
    ],
  },
  {
    name: '社会生产服务和生活服务人员',
    values: [
      { name: '单位总个数', value: 11000 },
      { name: '招聘总人数', value: 10500 },
    ],
  },
  {
    name: '农、林、牧、渔业生产及辅助人员',
    values: [
      { name: '单位总个数', value: 7000 },
      { name: '招聘总人数', value: 9000 },
    ],
  },
  {
    name: '生产制造及有关人员',
    values: [
      { name: '单位总个数', value: 13000 },
      { name: '招聘总人数', value: 14000 },
    ],
  },
  {
    name: '军队人员',
    values: [
      { name: '单位总个数', value: 3000 },
      { name: '招聘总人数', value: 17000 },
    ],
  },
  {
    name: '不便分类的其他从业人员',
    values: [
      { name: '单位总个数', value: 5000 },
      { name: '招聘总人数', value: 10000 },
    ],
  },
]

const mockDangdejiguanZhongleiData = [
  {
    name: '中国共产党机关负责人',
    values: [
      { name: '单位总个数', value: 5 },
      { name: '招聘总人数', value: 10 },
    ],
  },
  {
    name: '国家机关负责人',
    values: [
      { name: '单位总个数', value: 2 },
      { name: '招聘总人数', value: 4 },
    ],
  },
]

const handleCareerChange = (value: string, label: string, level: string) => {
  career.value = value
  careerLabel.value = label
  careerLevel.value = level
  title.value =
    (props.companyScaleName || '全部规模') + `单位的标准职业（${label || '全部大类'}）关键数据分布`

  if (level === '1') {
    data.value = mockDangdejiguanZhongleiData
  } else {
    data.value = mockDaleiData
  }
}

onMounted(() => {
  data.value = mockDaleiData
})

watch(
  () => props.companyScaleName,
  newValue => {
    title.value =
      (newValue || '全部规模') + `单位的标准职业（${careerLabel.value || '全部大类'}）关键数据分布`
    tooltipTitle.value = newValue ? `（仅${newValue}规模单位）` : '（全部规模单位）'
  }
)
</script>

<template>
  <div class="w-full bg-white/5 backdrop-blur-sm rounded-lg p-4 mt-6">
    <!-- 主标题 -->
    <FifthTitle title="招聘单位和标准职业" size="md" icon="icon-dianlihangye" />
    <!-- 图表卡片区域 -->
    <div>
      <Card class="mt-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2 max-w-[500px]">
              <div
                class="w-10 h-10 rounded-full bg-[#00ffff]/10 flex items-center justify-center flex-shrink-0"
              >
                <Icon name="icon-a-zhexiantu4" size="20" color="#00ffff" />
              </div>
              <span class="text-sm font-medium text-[#00ffff] flex-1 whitespace-wrap">{{
                title
              }}</span>
            </div>
            <CareerFilter v-model="career" @change="handleCareerChange" />
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
                  <span>标准职业：</span>
                  <span class="font-bold"
                    >{{ careerLabel || '全部'
                    }}{{ careerLabel ? `（${careerCategoryMap[careerLevel]}）` : '' }}</span
                  >
                </div>
                <div class="text-xs text-gray-400 whitespace-nowrap break-all">
                  <span>图表数据：</span>
                  <span class="font-bold"
                    >{{ careerLabel ? '该标准职业' : ''
                    }}{{
                      careerLevel === '1'
                        ? '下的所有中类职业'
                        : careerLevel === '2'
                        ? '下的所有小类职业'
                        : careerLevel === '3'
                        ? '下的所有细类职业'
                        : '标准职业所有大类'
                    }}的招聘单位总个数和招聘总人数分布</span
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
            left-color="#00ffff"
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
