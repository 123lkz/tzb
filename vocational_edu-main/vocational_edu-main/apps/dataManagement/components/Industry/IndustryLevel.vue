<script setup lang="ts">
import Card from '../common/Card.vue'
import FifthTitle from '../common/Title/FifthTitle.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import Select from '../common/Select.vue'
import { industryMediumCategoryOptions } from '../../utils/constants'

const menleiData = ref([
  {
    name: '农、林、牧、渔业',
    value: 'A',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '采矿业',
    value: 'B',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '制造业',
    value: 'C',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '电力、热力、燃气及水生产和供应业',
    value: 'D',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '建筑业',
    value: 'E',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '批发和零售业',
    value: 'F',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '交通运输、仓储和邮政业',
    value: 'G',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '住宿和餐饮业',
    value: 'H',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '信息传输、软件和信息技术服务业 ',
    value: 'I',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '金融业 ',
    value: 'J',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '房地产业',
    value: 'K',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '租赁和商务服务业',
    value: 'L',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
])

const daleiData = ref([
  {
    name: '农业',
    value: 'A-01',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '林业',
    value: 'A-02',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '畜牧业',
    value: 'A-03',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '渔业',
    value: 'A-04',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '农、林、牧、渔专业及辅助性活动',
    value: 'A-05',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '煤炭开采和洗选业',
    value: 'B-06',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '石油和天然气开采业',
    value: 'B-07',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '黑色金属矿采选业',
    value: 'B-08',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '有色金属矿采选业',
    value: 'B-09',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '非金属矿采选业',
    value: 'B-10',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '开采专业及辅助性活动',
    value: 'B-11',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '其他采矿业',
    value: 'B-12',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '农副食品加工业',
    value: 'C-13',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '食品制造业',
    value: 'C-14',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '酒、饮料和精制茶制造业',
    value: 'C-15',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '烟草制品业',
    value: 'C-16',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '纺织业',
    value: 'C-17',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '纺织服装、服饰业',
    value: 'C-18',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '皮革、毛皮、羽毛及其制品和制鞋业',
    value: 'C-19',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '木材加工和木、竹、藤、棕、草制品业',
    value: 'C-20',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
  {
    name: '家具制造业',
    value: 'C-21',
    values: [
      { name: '招聘总人数', value: 8000 },
      { name: '薪资中位数', value: 13000 },
    ],
  },
])

const selectedMajorCategory = ref('')
const selectedMajorCategoryName = ref('')
const majorCategoryData = computed(() => {
  const data = [{ value: '', label: '全部大类' }, ...industryMediumCategoryOptions]
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
      <FifthTitle
        title="国民经济行业全部门类数据概览"
        icon="icon-zhuxingtu"
        size="md"
        class="mt-2"
      />
      <div class="w-full h-[300px]">
        <LineBarDualAxisChart
          :data="menleiData"
          left-unit="万"
          left-quantifier="人"
          right-unit=""
          right-quantifier="元"
          title="国民经济行业全部门类数据概览"
          left-color="#f69c54"
          right-color="#f8d329"
          is-smooth-line
          tooltip-title="国民经济行业全部门类"
          height="300px"
        />
      </div>
    </Card>
    <Card>
      <div class="relative flex items-center">
        <FifthTitle
          :title="`国民经济行业${selectedMajorCategoryName || '全部大类'}数据概览`"
          icon="icon-zhuxingtu"
          size="md"
          class="mt-2 w-full"
        />
        <div class="absolute right-12 top-2 flex items-center gap-2 z-10">
          <label class="text-[#00ffff] font-medium flex-shrink-0">选择大类：</label>
          <Select
            v-model="selectedMajorCategory"
            :options="majorCategoryData"
            size="sm"
            placeholder="选择大类"
            @change="handleMajorChange"
          />
        </div>
      </div>
      <div class="w-full h-[300px]">
        <LineBarDualAxisChart
          :data="daleiData"
          left-unit="万"
          left-quantifier="人"
          right-unit=""
          right-quantifier="元"
          title="国民经济行业大类数据概览"
          left-color="#00ffff"
          right-color="#AAD8E8"
          is-smooth-line
          tooltip-title="国民经济行业大类"
          height="300px"
        />
      </div>
    </Card>
  </div>
</template>
