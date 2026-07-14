<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import IndustryFilter from '~/components/common/Filter/IndustryFilter.vue'
import DashboardButton from '~/components/common/DashboardButton.vue'
import IndustryTop from '~/components/Industry/IndustryTop.vue'
import IndustryMiddle from '~/components/Industry/IndustryMiddle.vue'
import IndustryDiffSituation from '~/components/Industry/IndustryDiffSituation.vue'
import IndustryBottom from '~/components/Industry/IndustryBottom.vue'
import IndustryLevel from '~/components/Industry/IndustryLevel.vue'
import Modal from '~/components/common/Modal.vue'
import TreeChart from '@/components/Echart/TreeChart.vue'
import IndustryGovStats from '@/components/Industry/IndustryGovStats.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '标准行业信息', path: '/industry' },
]

const industry = ref('')
const industryLabel = ref('')
const industryLevel = ref('1')
const province = ref('全国')
const time = ref('month')
const scope = ref('all')
const showModal = ref(false)

const handleProvinceChange = (value: string) => {
  province.value = value
}

const handleTimeChange = (value: string) => {
  time.value = value
}

const handleScopeChange = (value: string) => {
  scope.value = value
}

const handleIndustryChange = (value: string, label: string, level: string) => {
  industry.value = value
  industryLabel.value = label
  industryLevel.value = level
}
const handleDashboardClick = () => {
  useRouter().push('industry-list')
}

const handleClickZhiYe = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const industryDictionary = ref({
  name: '国民经济行业分类',
  code: 'ROOT',
  itemStyle: {
    color: '#00ffff',
  },
  label: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  children: [
    {
      name: '农、林、牧、渔业',
      code: 'A',
      children: [
        {
          name: '农业',
          code: 'A-01',
          children: [
            {
              name: '谷物种植',
              code: 'A-01-01',
              children: [
                { name: '稻谷种植', code: 'A-01-01-01' },
                { name: '小麦种植', code: 'A-01-01-02' },
                { name: '玉米种植', code: 'A-01-01-03' },
                { name: '其他谷物种植', code: 'A-01-01-09' },
              ],
            },
            {
              name: '豆类、油料和薯类种植',
              code: 'A-01-02',
              children: [
                { name: '豆类种植', code: 'A-01-02-01' },
                { name: '油料种植', code: 'A-01-02-02' },
                { name: '薯类种植', code: 'A-01-02-03' },
              ],
            },
            {
              name: '棉、麻、糖、烟草种植',
              code: 'A-01-03',
              children: [
                { name: '棉花种植', code: 'A-01-03-01' },
                { name: '麻类种植', code: 'A-01-03-02' },
                { name: '糖料种植', code: 'A-01-03-03' },
                { name: '烟草种植', code: 'A-01-03-04' },
              ],
            },
            {
              name: '蔬菜、食用菌及园艺作物种植',
              code: 'A-01-04',
              children: [
                { name: '蔬菜种植', code: 'A-01-04-01' },
                { name: '食用菌种植', code: 'A-01-04-02' },
              ],
            },
          ],
        },
        {
          name: '林业',
          code: 'A-02',
          children: [
            {
              name: '林木育种和育苗',
              code: 'A-02-01',
              children: [
                { name: '林木育种', code: 'A-02-01-01' },
                { name: '林木育苗', code: 'A-02-01-02' },
              ],
            },
            {
              name: '森林培育',
              code: 'A-02-02',
              children: [{ name: '森林培育', code: 'A-02-02-00' }],
            },
          ],
        },
        {
          name: '畜牧业',
          code: 'A-03',
          children: [
            {
              name: '牲畜饲养',
              code: 'A-03-01',
              children: [
                { name: '牛的饲养', code: 'A-03-01-01' },
                { name: '马的饲养', code: 'A-03-01-02' },
                { name: '猪的饲养', code: 'A-03-01-03' },
                { name: '羊的饲养', code: 'A-03-01-04' },
              ],
            },
            {
              name: '家禽饲养',
              code: 'A-03-02',
              children: [
                { name: '鸡的饲养', code: 'A-03-02-01' },
                { name: '鸭的饲养', code: 'A-03-02-02' },
                { name: '鹅的饲养', code: 'A-03-02-03' },
              ],
            },
          ],
        },
        {
          name: '渔业',
          code: 'A-04',
          children: [
            {
              name: '水产养殖',
              code: 'A-04-01',
              children: [
                { name: '海水养殖', code: 'A-04-01-01' },
                { name: '内陆养殖', code: 'A-04-01-02' },
              ],
            },
            {
              name: '水产捕捞',
              code: 'A-04-02',
              children: [
                { name: '海水捕捞', code: 'A-04-02-01' },
                { name: '内陆捕捞', code: 'A-04-02-02' },
              ],
            },
          ],
        },
        {
          name: '农、林、牧、渔专业及辅助性活动',
          code: 'A-05',
          children: [
            {
              name: '农业专业及辅助性活动',
              code: 'A-05-01',
              children: [
                { name: '农业机械服务', code: 'A-05-01-01' },
                { name: '农业技术推广服务', code: 'A-05-01-02' },
              ],
            },
            {
              name: '林业专业及辅助性活动',
              code: 'A-05-02',
              children: [
                { name: '林业有害生物防治服务', code: 'A-05-02-01' },
                { name: '森林防火服务', code: 'A-05-02-02' },
              ],
            },
          ],
        },
      ],
    },
    {
      name: '采矿业',
      code: 'B',
      children: [
        {
          name: '煤炭开采和洗选业',
          code: 'B-06',
          children: [
            {
              name: '烟煤和无烟煤开采洗选',
              code: 'B-06-01',
              children: [{ name: '烟煤和无烟煤开采洗选', code: 'B-06-01-00' }],
            },
            {
              name: '褐煤开采洗选',
              code: 'B-06-02',
              children: [{ name: '褐煤开采洗选', code: 'B-06-02-00' }],
            },
          ],
        },
        {
          name: '石油和天然气开采业',
          code: 'B-07',
          children: [
            {
              name: '石油开采',
              code: 'B-07-01',
              children: [
                { name: '陆地石油开采', code: 'B-07-01-01' },
                { name: '海洋石油开采', code: 'B-07-01-02' },
              ],
            },
            {
              name: '天然气开采',
              code: 'B-07-02',
              children: [
                { name: '陆地天然气开采', code: 'B-07-02-01' },
                { name: '海洋天然气开采', code: 'B-07-02-02' },
              ],
            },
          ],
        },
        {
          name: '黑色金属矿采选业',
          code: 'B-08',
          children: [
            {
              name: '铁矿采选',
              code: 'B-08-01',
              children: [{ name: '铁矿采选', code: 'B-08-01-00' }],
            },
            {
              name: '锰矿、铬矿采选',
              code: 'B-08-02',
              children: [{ name: '锰矿、铬矿采选', code: 'B-08-02-00' }],
            },
          ],
        },
        {
          name: '有色金属矿采选业',
          code: 'B-09',
          children: [
            {
              name: '常用有色金属矿采选',
              code: 'B-09-01',
              children: [
                { name: '铜矿采选', code: 'B-09-01-01' },
                { name: '铅锌矿采选', code: 'B-09-01-02' },
                { name: '镍钴矿采选', code: 'B-09-01-03' },
              ],
            },
            {
              name: '贵金属矿采选',
              code: 'B-09-02',
              children: [
                { name: '金矿采选', code: 'B-09-02-01' },
                { name: '银矿采选', code: 'B-09-02-02' },
              ],
            },
          ],
        },
        {
          name: '非金属矿采选业',
          code: 'B-10',
          children: [
            {
              name: '土砂石开采',
              code: 'B-10-01',
              children: [
                { name: '石灰石、石膏开采', code: 'B-10-01-01' },
                { name: '建筑装饰用石开采', code: 'B-10-01-02' },
              ],
            },
            {
              name: '化学矿开采',
              code: 'B-10-02',
              children: [{ name: '化学矿开采', code: 'B-10-02-00' }],
            },
          ],
        },
      ],
    },
    {
      name: '制造业',
      code: 'C',
      children: [
        {
          name: '农副食品加工业',
          code: 'C-13',
          children: [
            {
              name: '谷物磨制',
              code: 'C-13-01',
              children: [{ name: '谷物磨制', code: 'C-13-01-00' }],
            },
            {
              name: '饲料加工',
              code: 'C-13-02',
              children: [{ name: '饲料加工', code: 'C-13-02-00' }],
            },
          ],
        },
        {
          name: '食品制造业',
          code: 'C-14',
          children: [
            {
              name: '焙烤食品制造',
              code: 'C-14-01',
              children: [
                { name: '糕点、面包制造', code: 'C-14-01-01' },
                { name: '饼干及其他焙烤食品制造', code: 'C-14-01-02' },
              ],
            },
            {
              name: '乳制品制造',
              code: 'C-14-02',
              children: [
                { name: '液体乳制造', code: 'C-14-02-01' },
                { name: '乳粉制造', code: 'C-14-02-02' },
              ],
            },
          ],
        },
        {
          name: '酒、饮料和精制茶制造业',
          code: 'C-15',
          children: [
            {
              name: '酒的制造',
              code: 'C-15-01',
              children: [
                { name: '白酒制造', code: 'C-15-01-01' },
                { name: '啤酒制造', code: 'C-15-01-02' },
                { name: '葡萄酒制造', code: 'C-15-01-03' },
              ],
            },
            {
              name: '饮料制造',
              code: 'C-15-02',
              children: [
                { name: '碳酸饮料制造', code: 'C-15-02-01' },
                { name: '瓶（罐）装饮用水制造', code: 'C-15-02-02' },
              ],
            },
          ],
        },
      ],
    },
    {
      name: '电力、热力、燃气及水生产和供应业',
      code: 'D',
      children: [
        {
          name: '电力、热力生产和供应业',
          code: 'D-44',
          children: [
            {
              name: '电力生产',
              code: 'D-44-01',
              children: [
                { name: '火力发电', code: 'D-44-01-01' },
                { name: '水力发电', code: 'D-44-01-02' },
                { name: '核力发电', code: 'D-44-01-03' },
              ],
            },
            {
              name: '电力供应',
              code: 'D-44-02',
              children: [{ name: '电力供应', code: 'D-44-02-00' }],
            },
          ],
        },
        {
          name: '燃气生产和供应业',
          code: 'D-45',
          children: [
            {
              name: '燃气生产和供应',
              code: 'D-45-01',
              children: [{ name: '燃气生产和供应', code: 'D-45-01-00' }],
            },
          ],
        },
        {
          name: '水的生产和供应业',
          code: 'D-46',
          children: [
            {
              name: '自来水生产和供应',
              code: 'D-46-01',
              children: [{ name: '自来水生产和供应', code: 'D-46-01-00' }],
            },
            {
              name: '污水处理及其再生利用',
              code: 'D-46-02',
              children: [{ name: '污水处理及其再生利用', code: 'D-46-02-00' }],
            },
          ],
        },
      ],
    },
    {
      name: '建筑业',
      code: 'E',
      children: [
        {
          name: '房屋建筑业',
          code: 'E-47',
          children: [
            {
              name: '房屋建筑',
              code: 'E-47-01',
              children: [
                { name: '住宅房屋建筑', code: 'E-47-01-01' },
                { name: '体育场馆建筑', code: 'E-47-01-02' },
              ],
            },
          ],
        },
        {
          name: '土木工程建筑业',
          code: 'E-48',
          children: [
            {
              name: '铁路工程建筑',
              code: 'E-48-01',
              children: [{ name: '铁路工程建筑', code: 'E-48-01-00' }],
            },
            {
              name: '公路工程建筑',
              code: 'E-48-02',
              children: [{ name: '公路工程建筑', code: 'E-48-02-00' }],
            },
          ],
        },
      ],
    },
    {
      name: '批发和零售业',
      code: 'F',
      children: [
        {
          name: '批发业',
          code: 'F-51',
          children: [
            {
              name: '农、林、牧、渔产品批发',
              code: 'F-51-01',
              children: [
                { name: '谷物、豆及薯类批发', code: 'F-51-01-01' },
                { name: '种子批发', code: 'F-51-01-02' },
              ],
            },
            {
              name: '食品、饮料及烟草制品批发',
              code: 'F-51-02',
              children: [
                { name: '米、面制品及食用油批发', code: 'F-51-02-01' },
                { name: '糕点、糖果及糖批发', code: 'F-51-02-02' },
              ],
            },
          ],
        },
        {
          name: '零售业',
          code: 'F-52',
          children: [
            {
              name: '综合零售',
              code: 'F-52-01',
              children: [
                { name: '百货零售', code: 'F-52-01-01' },
                { name: '超级市场零售', code: 'F-52-01-02' },
              ],
            },
            {
              name: '食品、饮料及烟草制品专门零售',
              code: 'F-52-02',
              children: [
                { name: '粮油零售', code: 'F-52-02-01' },
                { name: '糕点、面包零售', code: 'F-52-02-02' },
              ],
            },
          ],
        },
      ],
    },
  ],
})

// 根据选中的产业生成树形数据
const getIndustryTreeData = (industry: string) => {
  if (!industry) {
    return industryDictionary.value
  }

  const targetItem = industryDictionary.value.children.find(item => item.code === industry)

  // 直接使用传入的数据结构，转换为树形图需要的格式
  return targetItem || industryDictionary.value
}
</script>

<template>
  <div class="flex flex-col h-full p-4">
    <Header
      :breadcrumbs="breadcrumbs"
      @province-change="handleProvinceChange"
      @time-change="handleTimeChange"
      @scope-change="handleScopeChange"
    >
      <template #right-filter>
        <IndustryFilter v-model="industry" @change="handleIndustryChange" />
      </template>
      <template #right-button>
        <DashboardButton text="国民经济行业分类" icon="icon-zhiye" @click="handleClickZhiYe" />
        <DashboardButton text="行业列表" icon="icon-liebiao" @click="handleDashboardClick" />
      </template>
    </Header>
    <div class="w-full pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
      <IndustryTop
        :province="province"
        :time="time"
        :scope="scope"
        :industry-label="industryLabel"
        :industry-level="industryLevel"
      />
      <IndustryMiddle
        :province="province"
        :time="time"
        :scope="scope"
        :industry-label="industryLabel"
        :industry-level="industryLevel"
      />
      <IndustryDiffSituation
        :province="province"
        :time="time"
        :scope="scope"
        :industry-label="industryLabel"
        :industry-level="industryLevel"
      />
      <IndustryBottom :industry-label="industryLabel" :industry-level="industryLevel" />
      <IndustryLevel
        :province="province"
        :time="time"
        :scope="scope"
        :industry-label="industryLabel"
        :industry-level="industryLevel"
      />
      <IndustryGovStats />
    </div>
    <Modal :show="showModal" title="行业分类大典" width="90%" height="90%" @close="closeModal">
      <TreeChart
        :data="getIndustryTreeData(industry)"
        text-color="#00ffff"
        :selected="industryLabel"
      />
    </Modal>
  </div>
</template>
