<script setup lang="ts">
import Card from '../common/Card.vue'
import FifthTitle from '../common/Title/FifthTitle.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import Select from '../common/Select.vue'
import { careerMajorCategoryOptions } from '../../utils/constants'

const daleiData = ref([
  {
    name: '党的机关、国家机关、群众团体和社会组织、企事业单位负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '专业技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '办事人员和有关人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '社会生产服务和生活服务人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '农、林、牧、渔业生产及辅助人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '生产制造及有关人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '军队人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '不便分类的其他从业人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
])

const zhongleiData = ref([
  {
    name: '中国共产党机关负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '国家机关负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '民主党派和工商联负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '人民团体和群众团体、社会组织及其他成员组织负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '基层群众自治组织负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '企事业单位负责人',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '科学研究人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '工程技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '农业技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '飞机和船舶技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '卫生专业技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '经济和金融专业人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '监察、法律、社会和宗教专业人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '教学人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '文学艺术、体育专业人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '新闻出版、文化专业人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '其他专业技术人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '行政办事及辅助人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '安全和消防及辅助人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '法律事务及辅助人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '其他办事人员和有关人员',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
])

const selectedMajorCategory = ref('')
const selectedMajorCategoryName = ref('')
const majorCategoryData = computed(() => {
  const data = [{ value: '', label: '全部大类' }, ...careerMajorCategoryOptions]
  return data
})

const handleMajorChange = (value: string, option: any) => {
  selectedMajorCategory.value = value
  selectedMajorCategoryName.value = option.label
}
</script>

<template>
  <div class="my-4 flex flex-col gap-4">
    <Card>
      <FifthTitle title="职业大典全部大类数据概览" icon="icon-zhuxingtu" size="md" class="mt-2" />
      <div class="w-full h-[300px]">
        <LineBarDualAxisChart
          :data="daleiData"
          left-unit="万"
          left-quantifier="人"
          right-unit=""
          right-quantifier="元"
          title="职业大典大类数据概览"
          left-color="#f69c54"
          right-color="#f8d329"
          is-smooth-line
          tooltip-title="职业大典大类"
          height="300px"
        />
      </div>
    </Card>
    <Card>
      <div class="relative flex items-center">
        <FifthTitle
          :title="`职业大典${selectedMajorCategoryName || '全部中类'}数据概览`"
          icon="icon-zhuxingtu"
          size="md"
          class="mt-2 w-full"
        />
        <div class="absolute right-12 top-2 flex items-center gap-2 z-10">
          <label class="text-[#00ffff] font-medium flex-shrink-0">选择职业中类：</label>
          <Select
            v-model="selectedMajorCategory"
            :options="majorCategoryData"
            size="sm"
            placeholder="选择职业中类"
            @change="handleMajorChange"
          />
        </div>
      </div>
      <div class="w-full h-[300px]">
        <LineBarDualAxisChart
          :data="zhongleiData"
          left-unit="万"
          left-quantifier="人"
          right-unit=""
          right-quantifier="元"
          title="职业大典中类数据概览"
          left-color="#00ffff"
          right-color="#AAD8E8"
          is-smooth-line
          tooltip-title="职业大典中类"
          height="300px"
        />
      </div>
    </Card>
  </div>
</template>
