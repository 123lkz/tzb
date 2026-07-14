<script setup lang="ts">
import FifthTitle from '../common/Title/FifthTitle.vue'
import Card from '../common/Card.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import RankList from '../common/RankList/RankList.vue'

const props = withDefaults(
  defineProps<{
    province: string
    time: string
    scope: string
    companyScaleName: string
  }>(),
  {
    province: '全国',
    time: 'month',
    scope: 'all',
    companyScaleName: '全部规模',
  }
)

const zhuanyeData = ref([
  {
    name: '字节跳动',
    value: 1722721,
    group: 1,
  },
  {
    name: '腾讯头条',
    value: 1594630,
    group: 2,
  },
  {
    name: '百度',
    value: 1490752,
    group: 3,
  },
  {
    name: '阿里巴巴',
    value: 1352604,
    group: 4,
  },
  {
    name: '京东',
    value: 986546,
    group: 5,
  },
  {
    name: '网易',
    value: 839964,
    group: 6,
  },
  {
    name: '美团',
    value: 284842,
    group: 7,
  },
  {
    name: '滴滴出行',
    value: 218532,
    group: 8,
  },
  {
    name: '快手',
    value: 206686,
    group: 9,
  },
  {
    name: '新浪',
    value: 194485,
    group: 10,
  },
  {
    name: '搜狐',
    value: 173696,
    group: 11,
  },
  {
    name: '爱奇艺',
    value: 165098,
    group: 12,
  },
  {
    name: '优酷',
    value: 159512,
    group: 13,
  },
  {
    name: '斗鱼',
    value: 151841,
    group: 14,
  },
  {
    name: '虎牙',
    value: 147519,
    group: 15,
  },
  {
    name: '哔哩哔哩',
    value: 141000,
    group: 16,
  },
  {
    name: '小红书',
    value: 135345,
    group: 17,
  },
  {
    name: '58同城',
    value: 126325,
    group: 18,
  },
  {
    name: '赶集网',
    value: 124759,
    group: 19,
  },
  {
    name: '智联招聘',
    value: 117508,
    group: 20,
  },
])
</script>

<template>
  <div class="flex flex-col gap-4 bg-white/5 backdrop-blur-sm rounded-lg p-4 mt-4">
    <FifthTitle
      title="单位排行"
      subtext="(招聘职位数量、招聘人数、薪资中位数)"
      type="circle"
      size="md"
      icon="icon-paihang"
    />
    <div class="grid grid-cols-4 gap-4 text-white/75">
      <Card>
        <SecondTitle
          title="热门单位 TOP100"
          type="circle"
          subtext="按发布的职位数量排行"
          icon="icon-remen"
          icon-size="18"
        />
        <RankList
          :data="zhuanyeData"
          tooltip-title="发布的职位数量"
          unit="个"
          :show-count="10"
          period="5"
        />
      </Card>
      <Card>
        <SecondTitle
          title="热门单位 TOP100"
          type="circle"
          subtext="按招聘人数排行"
          icon="icon-remen"
          icon-size="18"
        />
        <RankList
          :data="zhuanyeData"
          tooltip-title="招聘人数"
          unit="人"
          :show-count="10"
          period="5"
        />
      </Card>
      <Card>
        <SecondTitle
          title="高薪单位 TOP100"
          type="circle"
          subtext="按薪资中位数排行"
          icon="icon-qiandai"
          icon-size="18"
        />
        <RankList
          :data="zhuanyeData"
          tooltip-title="薪资中位数"
          unit="元"
          :show-count="10"
          period="5"
        />
      </Card>
    </div>
  </div>
</template>
