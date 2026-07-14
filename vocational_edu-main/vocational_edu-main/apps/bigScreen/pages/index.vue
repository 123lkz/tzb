<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import Loading from '~/components/Loading.vue'
import ResponsiveScreen from '~/components/Layout/ResponsiveScreen.vue'
import Header from '~/components/Layout/Header.vue'
import IndexTab from '~/components/Index/IndexTab.vue'
import IndexLeft from '~/components/Index/IndexLeft.vue'
import IndexRight from '~/components/Index/IndexRight.vue'
import { $position } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'

const loading = ref(true)
const isStatAll = ref(true) // 统计口径是否为全口径
const isStatYear = ref(false) // 统计时间是否为年度
const dateType = computed(() => (isStatYear.value ? 'year' : 'month'))
const caliberType = computed(() => (isStatAll.value ? 'all' : 'college'))

const { data: trendData } = useApiData(() =>
  $position.GetScreenTrendData({ dateType: dateType.value, caliberType: caliberType.value })
)

const companyData = computed(() => {
  return {
    months: trendData.value?.months || [],
    totalCount: (trendData.value?.companies || []).map(Number),
    changeRate: (trendData.value?.companyChangeRate || []).map(Number)
  }
})

const peopleData = computed(() => {
  return {
    months: trendData.value?.months || [],
    totalCount: (trendData.value?.recruitment || []).map(Number),
    changeRate: (trendData.value?.recruitmentChangeRate || []).map(Number)
  }
})

const professionData = computed(() => {
  return {
    months: trendData.value?.months || [],
    totalCount: (trendData.value?.positions || []).map(Number),
    changeRate: (trendData.value?.positionChangeRate || []).map(Number)
  }
})

/* 右侧数据 - 数据来自于统计局
  1. 三大产业产值比重（近5年）
  2. 三大产业和行业分类的关系对应
  3. 行业产值（一级行业分类）
  4. 行业从业人员数（一级行业分类）
*/
// 三大产业产值比重（近5年的数据）
const threeIndustriesValue = ref({
  years: ['2020', '2021', '2022', '2023', '2024'] as string[],
  primary: [78030.9, 83216.5, 88207.0, 89169.1, 91413.9] as number[],
  secondary: [381985.8, 447138.2, 467629.6, 475936.1, 492087.1] as number[],
  tertiary: [574850.9, 643468.4, 678192.7, 729166.5, 765582.5] as number[]
})

// 三大产业和行业分类的关系对应图
const threeIndustriesIncludes = ref([
  {
    name: '第一产业',
    color: '#FFCC80',
    industries: [
      {
        name: '农、林、牧、渔业',
        industries: [
          {
            name: '农业'
          },
          {
            name: '林业'
          },
          {
            name: '畜牧业'
          },
          {
            name: '渔业'
          },
          {
            name: '农、林、牧、渔专业及辅助性活动'
          }
        ]
      }
    ]
  },
  {
    name: '第二产业',
    color: '#B2DFDB',
    industries: [
      {
        name: '采矿业',
        industries: [
          {
            name: '煤炭开采和洗选业'
          },
          {
            name: '石油和天然气开采业'
          },
          {
            name: '黑色金属矿采选业'
          },
          {
            name: '有色金属矿采选业'
          },
          {
            name: '非金属矿采选业'
          },
          {
            name: '开采专业及辅助性活动'
          },
          {
            name: '其他采矿业'
          }
        ]
      },
      {
        name: '制造业',
        industries: [
          {
            name: '农副食品加工业'
          },
          {
            name: '食品制造业'
          },
          {
            name: '酒、饮料和精制茶制造业'
          },
          {
            name: '烟草制品业'
          },
          {
            name: '纺织业'
          },
          {
            name: '纺织服装、服饰业'
          },
          {
            name: '皮革、毛皮、羽毛及其制品和制鞋业'
          },
          {
            name: '木材加工和木、竹、藤、棕、草制品业'
          },
          {
            name: '家具制造业'
          },
          {
            name: '造纸和纸制品业'
          },
          {
            name: '印刷和记录媒介复制业'
          },
          {
            name: '文教、工美、体育和娱乐用品制造业'
          },
          {
            name: '石油、煤炭及其他燃料加工业'
          },
          {
            name: '化学原料和化学制品制造业'
          },
          {
            name: '医药制造业'
          },
          {
            name: '化学纤维制造业'
          },
          {
            name: '橡胶和塑料制品业'
          },
          {
            name: '非金属矿物制品业'
          },
          {
            name: '黑色金属冶炼和压延加工业'
          },
          {
            name: '有色金属冶炼和压延加工业'
          },
          {
            name: '金属制品业'
          },
          {
            name: '通用设备制造业'
          },
          {
            name: '专用设备制造业'
          },
          {
            name: '汽车制造业'
          },
          {
            name: '铁路、船舶、航空航天和其他运输设备制造业'
          },
          {
            name: '电气机械和器材制造业'
          },
          {
            name: '计算机、通信和其他电子设备制造业'
          },
          {
            name: '仪器仪表制造业'
          },
          {
            name: '其他制造业'
          },
          {
            name: '废弃资源综合利用业'
          },
          {
            name: '金属制品、机械和设备修理业'
          }
        ]
      },
      {
        name: '电力、热力、燃气及水生产和供应业',
        industries: [
          {
            name: '电力、热力生产和供应业'
          },
          {
            name: '燃气生产和供应业'
          },
          {
            name: '水的生产和供应业'
          }
        ]
      },
      {
        name: '建筑业',
        industries: [
          {
            name: '房屋建筑业'
          },
          {
            name: '土木工程建筑业'
          },
          {
            name: '建筑安装业'
          },
          {
            name: '建筑装饰、装修和其他建筑业'
          }
        ]
      }
    ]
  },
  {
    name: '第三产业',
    color: '#E1BEE7',
    industries: [
      {
        name: '批发和零售业',
        industries: [
          {
            name: '批发业'
          },
          {
            name: '零售业'
          }
        ]
      },
      {
        name: '交通运输、仓储和邮政业',
        industries: [
          {
            name: '铁路运输业'
          },
          {
            name: '道路运输业'
          },
          {
            name: '水上运输业'
          },
          {
            name: '航空运输业'
          },
          {
            name: '管道运输业'
          },
          {
            name: '多式联运和运输代理业'
          },
          {
            name: '装卸搬运和仓储业'
          },
          {
            name: '邮政业'
          }
        ]
      },
      {
        name: '住宿和餐饮业',
        industries: [
          {
            name: '住宿业'
          },
          {
            name: '餐饮业'
          }
        ]
      },
      {
        name: '信息传输、软件和信息技术服务业',
        industries: [
          {
            name: '电信、广播电视和卫星传输服务'
          },
          {
            name: '互联网和相关服务'
          },
          {
            name: '软件和信息技术服务业'
          }
        ]
      },
      {
        name: '金融业',
        industries: [
          {
            name: '货币金融服务'
          },
          {
            name: '资本市场服务'
          },
          {
            name: '保险业'
          },
          {
            name: '其他金融业'
          }
        ]
      },
      {
        name: '房地产业',
        industries: [
          {
            name: '房地产业'
          }
        ]
      },
      {
        name: '租赁和商务服务业',
        industries: [
          {
            name: '租赁业'
          },
          {
            name: '商务服务业'
          }
        ]
      },
      {
        name: '科学研究和技术服务业',
        industries: [
          {
            name: '研究与试验发展'
          },
          {
            name: '专业技术服务业'
          },
          {
            name: '科技推广和应用服务业'
          }
        ]
      },
      {
        name: '水利、环境和公共设施管理业',
        industries: [
          {
            name: '水利管理业'
          },
          {
            name: '生态保护和环境治理业'
          },
          {
            name: '公共设施管理业'
          },
          {
            name: '土地管理业'
          }
        ]
      },
      {
        name: '居民服务、修理和其他服务业',
        industries: [
          {
            name: '居民服务业'
          },
          {
            name: '机动车、电子产品和日用产品修理业'
          },
          {
            name: '其他服务业'
          }
        ]
      },
      {
        name: '教育',
        industries: [
          {
            name: '教育'
          }
        ]
      },
      {
        name: '卫生和社会工作',
        industries: [
          {
            name: '卫生'
          },
          {
            name: '社会工作'
          }
        ]
      },
      {
        name: '文化、体育和娱乐业',
        industries: [
          {
            name: '新闻和出版业'
          },
          {
            name: '广播、电视、电影和录音制作业'
          },
          {
            name: '文化艺术业'
          },
          {
            name: '体育'
          },
          {
            name: '娱乐业'
          }
        ]
      },
      {
        name: '公共管理、社会保障和社会组织',
        industries: [
          {
            name: '中国共产党机关'
          },
          {
            name: '国家机构'
          },
          {
            name: '人民政协、民主党派'
          },
          {
            name: '社会保障'
          },
          {
            name: '群众团体、社会团体和其他成员组织'
          },
          {
            name: '基层群众自治组织'
          }
        ]
      },
      {
        name: '国际组织',
        industries: [
          {
            name: '国际组织'
          }
        ]
      }
    ]
  }
])

// 行业产值（一级行业分类）统计局数据
const primaryIndustryValueData = ref([
  { name: '农、林、牧、渔业', value: 96612.9 },
  { name: '工业', value: 405442.1 },
  { name: '建筑业', value: 89949.3 },
  { name: '批发和零售业', value: 137980.9 },
  { name: '交通运输、仓储和邮政业', value: 59232.2 },
  { name: '住宿和餐饮业', value: 24728.8 },
  { name: '金融业', value: 98544.2 },
  { name: '房地产业', value: 84565.2 },
  { name: '其他行业', value: 352027.9 }
])

// 行业从业人员数（一级行业分类）统计局数据
const primaryIndustryPeopleData = ref([
  { name: '农、林、牧、渔业', value: 13496012, percent: 20.56 },
  { name: '采矿业', value: 568658, percent: 0.87 },
  { name: '制造业', value: 11853428, percent: 18.06 },
  { name: '电力、热力、燃气及水生产和供应业', value: 573235, percent: 0.87 },
  { name: '建筑业', value: 7400010, percent: 11.28 },
  { name: '批发和零售业', value: 9262396, percent: 14.11 },
  { name: '交通运输、仓储和邮政业', value: 3277208, percent: 4.99 },
  { name: '住宿和餐饮业', value: 3217357, percent: 4.9 },
  { name: '信息传输、软件和信息技术服务业', value: 1129543, percent: 1.72 },
  { name: '金融业', value: 962580, percent: 1.47 },
  { name: '房地产业', value: 1251428, percent: 1.91 },
  { name: '租赁和商务服务业', value: 1799653, percent: 2.74 },
  { name: '科学研究和技术服务业', value: 844905, percent: 1.29 },
  { name: '水利、环境和公共设施管理业', value: 517888, percent: 0.79 },
  { name: '居民服务、修理和其他服务业', value: 2289351, percent: 3.49 },
  { name: '教育', value: 2715648, percent: 4.14 },
  { name: '卫生和社会工作', value: 1341482, percent: 2.04 },
  { name: '文化、体育和娱乐业', value: 472194, percent: 0.72 },
  { name: '公共管理、社会保障和社会组织', value: 2658248, percent: 4.05 },
  { name: '国际组织', value: 562, percent: 0.0 }
])

const handleTabClick = () => {}

const handleChange = (data: { quantity: 'all' | 'college'; date: 'year' | 'month' }) => {
  isStatAll.value = data.quantity === 'all'
  isStatYear.value = data.date === 'year'
  // 数据会通过 computed 自动更新，因为 dateType 和 caliberType 已经改变
}

onMounted(() => {
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<template>
  <Loading v-if="loading" />
  <ResponsiveScreen v-else>
    <!-- 顶部标题栏 -->
    <Header />
    <!-- 顶部 TAB 切换 -->
    <IndexTab @on-tab-click="handleTabClick" @on-change="handleChange" />
    <!-- 主体内容区域 -->
    <div style="height: calc(100% - 8.5rem)">
      <div class="grid grid-cols-11 gap-3 px-4" style="height: 100%">
        <!-- 左侧区域 -->
        <div class="col-span-2" style="height: 100%">
          <IndexLeft
            :is-stat-all="isStatAll"
            :is-stat-year="isStatYear"
            :company-chart-data="companyData"
            :people-chart-data="peopleData"
            :profession-chart-data="professionData"
          />
        </div>
        <!-- 中间区域 - 通过NuxtPage显示 -->
        <div class="col-span-7 relative" style="height: 100%">
          <div class="absolute top-0 left-0 w-full z-0">
            <img src="@/assets/images/bg.jpg" alt="bg" class="w-full h-full object-cover opacity-10" />
          </div>
          <NuxtPage :key="`${isStatAll}-${isStatYear}`" :is-stat-all="isStatAll" :is-stat-year="isStatYear" />
        </div>
        <!-- 右侧区域 -->
        <div class="relative col-span-2 z-10" style="height: 100%">
          <IndexRight
            :three-industries-value="threeIndustriesValue"
            :three-industries-includes="threeIndustriesIncludes"
            :primary-industry-value-data="primaryIndustryValueData"
            :primary-industry-people-data="primaryIndustryPeopleData"
          />
        </div>
      </div>
    </div>
  </ResponsiveScreen>
</template>
