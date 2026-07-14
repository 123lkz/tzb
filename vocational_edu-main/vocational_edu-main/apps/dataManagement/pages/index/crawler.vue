<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import DashboardButton from '@/components/common/DashboardButton.vue'
import TwoFilter from '@/components/common/Filter/TwoFilter.vue'
import CrawlerOverview from '@/components/Crawler/CrawlerOverview.vue'
import CrawlerPlatform from '@/components/Crawler/CrawlerPlatform.vue'
import CrawlerPosition from '@/components/Crawler/CrawlerPosition.vue'
import CrawlerCompany from '@/components/Crawler/CrawlerCompany.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '平台爬取', path: '/crawler' },
]

const time = ref('weekly')
const isCleaned = ref(false)

const handleTimeChange = (value: string) => {
  time.value = value
}

const handleIsCleanedChange = (value: string) => {
  isCleaned.value = value === 'cleaned'
}

const handleDashboardClick = () => {
  useRouter().push('/crawler-list')
}

const options = ref([
  {
    value: 'all',
    label: '全部',
  },
  {
    value: 'cleaned',
    label: '已清洗',
  },
])
</script>

<template>
  <div class="flex flex-col h-full overflow-y-auto overflow-x-hidden pl-4 pt-4">
    <div class="flex-shrink-0 mr-4">
      <Header
        selected-time-dimension="weekly"
        :show-weekly="true"
        :show-scope="false"
        :show-province="false"
        :breadcrumbs="breadcrumbs"
        @time-change="handleTimeChange"
      >
        <template #right-filter>
          <span class="text-sm text-[#00eaff] font-medium uppercase tracking-wider"
            >数据清洗：</span
          >
          <TwoFilter :options="options" @on-change="handleIsCleanedChange" />
        </template>
        <template #right-button>
          <DashboardButton text="平台爬取列表" icon="icon-liebiao" @click="handleDashboardClick" />
        </template>
      </Header>
    </div>
    <div class="w-full my-4 pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
      <CrawlerOverview :is-cleaned="isCleaned" :time="time" />
      <CrawlerPlatform :is-cleaned="isCleaned" :time="time" />
      <CrawlerPosition :is-cleaned="isCleaned" :time="time" />
      <CrawlerCompany :is-cleaned="isCleaned" :time="time" />
    </div>
  </div>
</template>

s
