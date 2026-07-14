<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import CareerFilter from '@/components/common/Filter/CareerFilter.vue'
import DashboardButton from '~/components/common/DashboardButton.vue'
import CareerTop from '@/components/Career/CareerTop.vue'
import CareerMiddle from '~/components/Career/CareerMiddle.vue'
import CareerDiffSituation from '~/components/Career/CareerDiffSituation.vue'
import CareerBottom from '@/components/Career/CareerBottom.vue'
import CareerLevel from '~/components/Career/CareerLevel.vue'
import Modal from '~/components/common/Modal.vue'
import TreeChart from '@/components/Echart/TreeChart.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '标准职业信息', path: '/career' },
]

const career = ref('')
const careerLabel = ref('')
const careerLevel = ref('1')
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

const handleCareerChange = (value: string, label: string, level: string) => {
  career.value = value
  careerLabel.value = label
  careerLevel.value = level
}
const handleDashboardClick = () => {
  useRouter().push('/career-list')
}

const handleClickZhiYe = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const careerDictionary = ref({
  name: '职业大典',
  code: '',
  children: [
    {
      name: '党的机关、国家机关、群众团体和社会组织、企事业单位负责人',
      code: '1',
      children: [
        {
          name: '中国共产党机关负责人',
          code: '1-01',
          children: [
            {
              name: '中国共产党机关负责人',
              code: '1-01-00',
              children: [
                {
                  name: '中央国家权力机关负责人',
                  code: '1-01-00-01',
                },
                {
                  name: '中国共产党基层组织负责人',
                  code: '1-01-00-02',
                },
              ],
            },
          ],
        },
        {
          name: '国家机关负责人',
          code: '1-02',
          children: [
            {
              name: '国家权力机关负责人',
              code: '1-02-01',
              children: [
                {
                  name: '国家权力机关负责人',
                  code: '1-02-01-00',
                },
              ],
            },
            {
              name: '国家行政机关负责人',
              code: '1-02-02',
              children: [
                {
                  name: '国家行政机关负责人',
                  code: '1-02-02-00',
                },
              ],
            },
          ],
        },
      ],
    },
    {
      name: '专业技术人员',
      code: '2',
      children: [
        {
          name: '科学研究人员',
          code: '2-01',
          children: [
            {
              name: '哲学研究人员',
              code: '2-01-01',
              children: [
                {
                  name: '哲学研究人员',
                  code: '2-01-01-00',
                },
              ],
            },
            {
              name: '经济学研究人员',
              code: '2-01-02',
              children: [
                {
                  name: '经济学研究人员',
                  code: '2-01-02-00',
                },
              ],
            },
            {
              name: '法学研究人员',
              code: '2-01-03',
              children: [
                {
                  name: '法学研究人员',
                  code: '2-01-03-00',
                },
              ],
            },
            {
              name: '教育学研究人员',
              code: '2-01-04',
              children: [
                {
                  name: '教育学研究人员',
                  code: '2-01-04-00',
                },
              ],
            },
            {
              name: '历史学研究人员',
              code: '2-01-05',
              children: [
                {
                  name: '历史学研究人员',
                  code: '2-01-05-00',
                },
              ],
            },
            {
              name: '自然科学和地球科学研究人员',
              code: '2-01-06',
              children: [
                {
                  name: '自然科学和地球科学研究人员',
                  code: '2-01-06-00',
                },
              ],
            },
            {
              name: '农业科学研究人员',
              code: '2-01-07',
              children: [
                {
                  name: '农业科学研究人员',
                  code: '2-01-07-00',
                },
              ],
            },
            {
              name: '医学研究人员',
              code: '2-01-08',
              children: [
                {
                  name: '医学研究人员',
                  code: '2-01-08-00',
                },
              ],
            },
            {
              name: '管理学研究人员',
              code: '2-01-09',
              children: [
                {
                  name: '管理学研究人员',
                  code: '2-01-09-00',
                },
              ],
            },
            {
              name: '文学、艺术学研究人员',
              code: '2-01-10',
              children: [
                {
                  name: '文学、艺术学研究人员',
                  code: '2-01-10-00',
                },
              ],
            },
            {
              name: '军事学研究人员',
              code: '2-01-11',
              children: [
                {
                  name: '军事学研究人员',
                  code: '2-01-11-00',
                },
              ],
            },
            {
              name: '其他科学研究人员',
              code: '2-01-99',
              children: [
                {
                  name: '其他科学研究人员',
                  code: '2-01-99-00',
                },
              ],
            },
          ],
        },
        {
          name: '工程技术人员',
          code: '2-02',
          children: [
            {
              name: '地质勘探工程技术人员',
              code: '2-02-01',
              children: [
                {
                  name: '地质勘探工程技术人员',
                  code: '2-02-01-00',
                },
              ],
            },
            {
              name: '测绘和地理信息工程技术人员',
              code: '2-02-02',
              children: [
                {
                  name: '测绘和地理信息工程技术人员',
                  code: '2-02-02-00',
                },
              ],
            },
            {
              name: '矿山工程技术人员',
              code: '2-02-03',
              children: [
                {
                  name: '矿山工程技术人员',
                  code: '2-02-03-00',
                },
              ],
            },
            {
              name: '石油天然气工程技术人员',
              code: '2-02-04',
              children: [
                {
                  name: '石油天然气工程技术人员',
                  code: '2-02-04-00',
                },
              ],
            },
            {
              name: '冶金工程技术人员',
              code: '2-02-05',
              children: [
                {
                  name: '冶金工程技术人员',
                  code: '2-02-05-00',
                },
              ],
            },
            {
              name: '化工工程技术人员',
              code: '2-02-06',
              children: [
                {
                  name: '化工工程技术人员',
                  code: '2-02-06-00',
                },
              ],
            },
            {
              name: '机械工程技术人员',
              code: '2-02-07',
              children: [
                {
                  name: '机械工程技术人员',
                  code: '2-02-07-00',
                },
              ],
            },
            {
              name: '航空工程技术人员',
              code: '2-02-08',
              children: [
                {
                  name: '航空工程技术人员',
                  code: '2-02-08-00',
                },
              ],
            },
            {
              name: '电子工程技术人员',
              code: '2-02-09',
              children: [
                {
                  name: '电子工程技术人员',
                  code: '2-02-09-00',
                },
              ],
            },
            {
              name: '信息和通信工程技术人员',
              code: '2-02-10',
              children: [
                {
                  name: '信息和通信工程技术人员',
                  code: '2-02-10-00',
                },
              ],
            },
            {
              name: '电气工程技术人员',
              code: '2-02-11',
              children: [
                {
                  name: '电气工程技术人员',
                  code: '2-02-11-00',
                },
              ],
            },
            {
              name: '电力工程技术人员',
              code: '2-02-12',
              children: [
                {
                  name: '电力工程技术人员',
                  code: '2-02-12-00',
                },
              ],
            },
            {
              name: '邮政和快递工程技术人员',
              code: '2-02-13',
              children: [
                {
                  name: '邮政和快递工程技术人员',
                  code: '2-02-13-00',
                },
              ],
            },
            {
              name: '广播电影电视及演艺设备工程技术人员',
              code: '2-02-14',
              children: [
                {
                  name: '广播电影电视及演艺设备工程技术人员',
                  code: '2-02-14-00',
                },
              ],
            },
            {
              name: '道路和水上运输工程技术人员',
              code: '2-02-15',
              children: [
                {
                  name: '道路和水上运输工程技术人员',
                  code: '2-02-15-00',
                },
              ],
            },
            {
              name: '民用航空工程技术人员',
              code: '2-02-16',
              children: [
                {
                  name: '民用航空工程技术人员',
                  code: '2-02-16-00',
                },
              ],
            },
            {
              name: '铁道工程技术人员',
              code: '2-02-17',
              children: [
                {
                  name: '铁道工程技术人员',
                  code: '2-02-17-00',
                },
              ],
            },
            {
              name: '建筑工程技术人员',
              code: '2-02-18',
              children: [
                {
                  name: '建筑工程技术人员',
                  code: '2-02-18-00',
                },
              ],
            },
            {
              name: '建材工程技术人员',
              code: '2-02-19',
              children: [
                {
                  name: '建材工程技术人员',
                  code: '2-02-19-00',
                },
              ],
            },
            {
              name: '林草工程技术人员',
              code: '2-02-20',
              children: [
                {
                  name: '林草工程技术人员',
                  code: '2-02-20-00',
                },
              ],
            },
            {
              name: '水利工程技术人员',
              code: '2-02-21',
              children: [
                {
                  name: '水利工程技术人员',
                  code: '2-02-21-00',
                },
              ],
            },
            {
              name: '海洋工程技术人员',
              code: '2-02-22',
              children: [
                {
                  name: '海洋工程技术人员',
                  code: '2-02-22-00',
                },
              ],
            },
            {
              name: '纺织服装工程技术人员',
              code: '2-02-23',
              children: [
                {
                  name: '纺织服装工程技术人员',
                  code: '2-02-23-00',
                },
              ],
            },
            {
              name: '食品工程技术人员',
              code: '2-02-24',
              children: [
                {
                  name: '食品工程技术人员',
                  code: '2-02-24-00',
                },
              ],
            },
            {
              name: '气象工程技术人员',
              code: '2-02-25',
              children: [
                {
                  name: '气象工程技术人员',
                  code: '2-02-25-00',
                },
              ],
            },
            {
              name: '地震工程技术人员',
              code: '2-02-26',
              children: [
                {
                  name: '地震工程技术人员',
                  code: '2-02-26-00',
                },
              ],
            },
            {
              name: '环境保护工程技术人员',
              code: '2-02-27',
              children: [
                {
                  name: '环境保护工程技术人员',
                  code: '2-02-27-00',
                },
              ],
            },
            {
              name: '安全工程技术人员',
              code: '2-02-28',
              children: [
                {
                  name: '安全工程技术人员',
                  code: '2-02-28-00',
                },
              ],
            },
            {
              name: '标准化、计量、质量和认证认可工程技术人员',
              code: '2-02-29',
              children: [
                {
                  name: '标准化、计量、质量和认证认可工程技术人员',
                  code: '2-02-29-00',
                },
              ],
            },
            {
              name: '管理(工业)工程技术人员',
              code: '2-02-30',
              children: [
                {
                  name: '管理(工业)工程技术人员',
                  code: '2-02-30-00',
                },
              ],
            },
            {
              name: '检验检疫工程技术人员',
              code: '2-02-31',
              children: [
                {
                  name: '检验检疫工程技术人员',
                  code: '2-02-31-00',
                },
              ],
            },
            {
              name: '制药工程技术人员',
              code: '2-02-32',
              children: [
                {
                  name: '制药工程技术人员',
                  code: '2-02-32-00',
                },
              ],
            },
            {
              name: '印刷复制工程技术人员',
              code: '2-02-33',
              children: [
                {
                  name: '印刷复制工程技术人员',
                  code: '2-02-33-00',
                },
              ],
            },
            {
              name: '工业(产品)设计工程技术人员',
              code: '2-02-34',
              children: [
                {
                  name: '工业(产品)设计工程技术人员',
                  code: '2-02-34-00',
                },
              ],
            },
            {
              name: '康复辅具工程技术人员',
              code: '2-02-35',
              children: [
                {
                  name: '康复辅具工程技术人员',
                  code: '2-02-35-00',
                },
              ],
            },
            {
              name: '轻工工程技术人员',
              code: '2-02-36',
              children: [
                {
                  name: '轻工工程技术人员',
                  code: '2-02-36-00',
                },
              ],
            },
            {
              name: '国土空间规划与生态修复工程技术人员',
              code: '2-02-37',
              children: [
                {
                  name: '国土空间规划与生态修复工程技术人员',
                  code: '2-02-37-00',
                },
              ],
            },
            {
              name: '数字技术工程技术人员',
              code: '2-02-38',
              children: [
                {
                  name: '数字技术工程技术人员',
                  code: '2-02-38-00',
                },
              ],
            },
            {
              name: '其他工程技术人员',
              code: '2-02-99',
              children: [
                {
                  name: '其他工程技术人员',
                  code: '2-02-99-00',
                },
              ],
            },
          ],
        },
        {
          name: '农业技术人员',
          code: '2-03',
          children: [
            {
              name: '土壤肥料技术人员',
              code: '2-03-01',
              children: [
                {
                  name: '土壤肥料技术人员',
                  code: '2-03-01-00',
                },
              ],
            },
            {
              name: '农业技术指导人员',
              code: '2-03-02',
              children: [
                {
                  name: '农业技术指导人员',
                  code: '2-03-02-00',
                },
              ],
            },
            {
              name: '植物保护技术人员',
              code: '2-03-03',
              children: [
                {
                  name: '植物保护技术人员',
                  code: '2-03-03-00',
                },
              ],
            },
            {
              name: '园艺技术人员',
              code: '2-03-04',
              children: [
                {
                  name: '园艺技术人员',
                  code: '2-03-04-00',
                },
              ],
            },
            {
              name: '作物遗传育种栽培技术人员',
              code: '2-03-05',
              children: [
                {
                  name: '作物遗传育种栽培技术人员',
                  code: '2-03-05-00',
                },
              ],
            },
            {
              name: '兽医兽药技术人员',
              code: '2-03-06',
              children: [
                {
                  name: '兽医兽药技术人员',
                  code: '2-03-06-00',
                },
              ],
            },
            {
              name: '畜牧与草业技术人员',
              code: '2-03-07',
              children: [
                {
                  name: '畜牧与草业技术人员',
                  code: '2-03-07-00',
                },
              ],
            },
            {
              name: '水产技术人员',
              code: '2-03-08',
              children: [
                {
                  name: '水产技术人员',
                  code: '2-03-08-00',
                },
              ],
            },
            {
              name: '农业工程技术人员',
              code: '2-03-09',
              children: [
                {
                  name: '农业工程技术人员',
                  code: '2-03-09-00',
                },
              ],
            },
            {
              name: '其他农业技术人员',
              code: '2-03-99',
              children: [
                {
                  name: '其他农业技术人员',
                  code: '2-03-99-00',
                },
              ],
            },
          ],
        },
        {
          name: '飞机和船舶技术人员',
          code: '2-04',
          children: [
            {
              name: '飞机和船舶技术人员',
              code: '2-04-00',
              children: [
                {
                  name: '飞机和船舶技术人员',
                  code: '2-04-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '卫生专业技术人员',
          code: '2-05',
          children: [
            {
              name: '卫生专业技术人员',
              code: '2-05-00',
              children: [
                {
                  name: '卫生专业技术人员',
                  code: '2-05-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '经济和金融专业人员',
          code: '2-06',
          children: [
            {
              name: '经济和金融专业人员',
              code: '2-06-00',
              children: [
                {
                  name: '经济和金融专业人员',
                  code: '2-06-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '监察、法律、社会和宗教专业人员',
          code: '2-07',
          children: [
            {
              name: '监察、法律、社会和宗教专业人员',
              code: '2-07-00',
              children: [
                {
                  name: '监察、法律、社会和宗教专业人员',
                  code: '2-07-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '教学人员',
          code: '2-08',
          children: [
            {
              name: '教学人员',
              code: '2-08-00',
              children: [
                {
                  name: '教学人员',
                  code: '2-08-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '文学艺术、体育专业人员',
          code: '2-09',
          children: [
            {
              name: '文学艺术、体育专业人员',
              code: '2-09-00',
              children: [
                {
                  name: '文学艺术、体育专业人员',
                  code: '2-09-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '新闻出版、文化专业人员',
          code: '2-10',
          children: [
            {
              name: '新闻出版、文化专业人员',
              code: '2-10-00',
              children: [
                {
                  name: '新闻出版、文化专业人员',
                  code: '2-10-00-00',
                },
              ],
            },
          ],
        },
        {
          name: '其他专业技术人员',
          code: '2-99',
          children: [
            {
              name: '其他专业技术人员',
              code: '2-99-00',
              children: [
                {
                  name: '其他专业技术人员',
                  code: '2-99-00-00',
                },
              ],
            },
          ],
        },
      ],
    },
  ],
})

// 根据选中的产业生成树形数据
const getIndustryTreeData = (career: string) => {
  if (!career) {
    return careerDictionary.value
  }

  const targetItem = careerDictionary.value.children.find(item => item.code === career)

  // 直接使用传入的数据结构，转换为树形图需要的格式
  return targetItem || careerDictionary.value
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
        <CareerFilter v-model="career" @change="handleCareerChange" />
      </template>
      <template #right-button>
        <DashboardButton text="职业大典" icon="icon-zhiye" @click="handleClickZhiYe" />
        <DashboardButton text="职业列表" icon="icon-liebiao" @click="handleDashboardClick" />
      </template>
    </Header>
    <div class="w-full pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
      <CareerTop
        :province="province"
        :time="time"
        :scope="scope"
        :career-label="careerLabel"
        :career-level="careerLevel"
      />
      <CareerMiddle
        :province="province"
        :time="time"
        :scope="scope"
        :career-label="careerLabel"
        :career-level="careerLevel"
      />
      <CareerDiffSituation
        :province="province"
        :time="time"
        :scope="scope"
        :career-label="careerLabel"
        :career-level="careerLevel"
      />
      <CareerBottom :career-label="careerLabel" :career-level="careerLevel" />
      <CareerLevel
        :province="province"
        :time="time"
        :scope="scope"
        :career-label="careerLabel"
        :career-level="careerLevel"
      />
      <CareerGovStats
        :province="province"
        :time="time"
        :scope="scope"
        :career-label="careerLabel"
        :career-level="careerLevel"
      />
    </div>
    <Modal :show="showModal" title="职业大典" width="90%" height="90%" @close="closeModal">
      <TreeChart :data="getIndustryTreeData(career)" text-color="#00ffff" :selected="career" />
    </Modal>
  </div>
</template>
