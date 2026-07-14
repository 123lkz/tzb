<script setup lang="ts">
import HomeBottomCard from './HomeBottomCard.vue'
import HomeCrawler from './HomeCrawler.vue'

// Props 接口定义
interface Props {
  cardCount?: number
  showTitle?: boolean
  title?: string
}

// 默认Props
const props = withDefaults(defineProps<Props>(), {
  cardCount: 5,
  showTitle: true,
  title: '招聘平台数据概览',
})

// Emits 事件定义
const emit = defineEmits<{
  'card-click': [cardId: number, cardData: any]
}>()

// 招聘平台数据
const platformData = ref({
  // 第一个卡片：招聘平台总量
  totalPlatforms: {
    id: 1,
    title: '招聘平台总量',
    value: 4,
    unit: '个',
    platforms: ['智联招聘', 'Boss直聘', '58同城', '前程无忧'],
    icon: '🌐',
    description: '覆盖主流招聘平台',
  },

  // 第二个卡片：职位列表总量
  totalJobListings: {
    id: 2,
    title: '职位列表总量',
    value: 156789,
    unit: '条',
    trend: 12.5,
    trendType: 'up',
    period: '近一周',
    icon: '📋',
    description: '爬取职位列表数据',
  },

  // 第三个卡片：职位详情总量
  totalJobDetails: {
    id: 3,
    title: '职位详情总量',
    value: 98765,
    unit: '条',
    trend: 8.3,
    trendType: 'up',
    period: '近一周',
    icon: '📄',
    description: '爬取职位详情数据',
  },

  // 第四个卡片：智联数据
  zhilianData: {
    id: 4,
    title: '智联招聘数据',
    value: 45678,
    unit: '条',
    newCount: 2345,
    newUnit: '条',
    period: '上周新增',
    icon: '🔗',
    description: '智联招聘平台数据',
    breakdown: {
      listings: 28901,
      details: 16777,
    },
  },

  // 第五个卡片：Boss数据
  bossData: {
    id: 5,
    title: 'Boss直聘数据',
    value: 67890,
    unit: '条',
    newCount: 3456,
    newUnit: '条',
    period: '上周新增',
    icon: '💼',
    description: 'Boss直聘平台数据',
    breakdown: {
      listings: 42345,
      details: 25545,
    },
  },
})

// 格式化数字
const formatNumber = (num: number) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toLocaleString()
}

// 获取趋势颜色和图标
const getTrendInfo = (trend: number) => {
  const isPositive = trend > 0
  return {
    color: isPositive ? 'text-green-400' : 'text-red-400',
    icon: isPositive ? '↗' : '↘',
    text: isPositive ? `+${trend}%` : `${trend}%`,
  }
}

// 方法
const handleCardClick = (cardId: number) => {
  emit('card-click', cardId, platformData.value)
}

const refreshData = () => {
  // 模拟数据刷新
  platformData.value.totalJobListings.trend = Math.random() * 20 - 5
  platformData.value.totalJobDetails.trend = Math.random() * 20 - 5
  platformData.value.zhilianData.newCount = Math.floor(Math.random() * 5000) + 1000
  platformData.value.bossData.newCount = Math.floor(Math.random() * 5000) + 1000
}

const mockData1 = [
  {
    name: '2024-08',
    value: 12580,
  },
  {
    name: '2024-09',
    value: 14500,
  },
  {
    name: '2024-10',
    value: 8000,
  },
  {
    name: '2024-11',
    value: 11000,
  },
  {
    name: '2024-12',
    value: 12000,
  },
  {
    name: '2025-01',
    value: 15000,
  },
  {
    name: '2025-02',
    value: 6000,
  },
  {
    name: '2025-03',
    value: 10000,
  },
  {
    name: '2025-04',
    value: 7500,
  },
  {
    name: '2025-05',
    value: 9000,
  },
  {
    name: '2025-06',
    value: 17500,
  },
  {
    name: '2025-07',
    value: 18000,
  },
]

const mockData2 = [
  {
    name: '2024-08',
    value: 8500,
  },
  {
    name: '2024-09',
    value: 12000,
  },
  {
    name: '2024-10',
    value: 12500,
  },
  {
    name: '2024-11',
    value: 10000,
  },
  {
    name: '2024-12',
    value: 7000,
  },
  {
    name: '2025-01',
    value: 11000,
  },
  {
    name: '2025-02',
    value: 8000,
  },
  {
    name: '2025-03',
    value: 7000,
  },
  {
    name: '2025-04',
    value: 12500,
  },
  {
    name: '2025-05',
    value: 13000,
  },
  {
    name: '2025-06',
    value: 6000,
  },
  {
    name: '2025-07',
    value: 14000,
  },
]
</script>

<template>
  <div class="w-full h-40">
    <div class="flex gap-4 h-full w-full">
      <div style="width: 22%">
        <HomeBottomCard
          icon="icon-zhiye"
          title="招聘标准职业个数"
          :value="12580"
          indicator-desc="职位数量"
          quantifier="个"
          :chart-data="mockData1"
          :change-rate="12.5"
          change-label="较上月"
          :color="'#80FFA5'"
        />
      </div>
      <div style="width: 22%">
        <HomeBottomCard
          icon="icon-dianlihangye"
          title="招聘标准行业个数"
          :value="8500"
          indicator-desc="招聘总人数"
          quantifier="人"
          :chart-data="mockData2"
          :change-rate="-3.2"
          change-label="较上月"
          :color="'#FFBF00'"
        />
      </div>
      <div style="width: 56%">
        <HomeCrawler />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片悬停效果 */
.grid > div {
  animation: fadeInUp 0.6s ease-out;
}

.grid > div:nth-child(1) {
  animation-delay: 0.1s;
}
.grid > div:nth-child(2) {
  animation-delay: 0.2s;
}
.grid > div:nth-child(3) {
  animation-delay: 0.3s;
}
.grid > div:nth-child(4) {
  animation-delay: 0.4s;
}
.grid > div:nth-child(5) {
  animation-delay: 0.5s;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .h-32 {
    height: auto;
    min-height: 8rem;
  }
}

@media (max-width: 480px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
