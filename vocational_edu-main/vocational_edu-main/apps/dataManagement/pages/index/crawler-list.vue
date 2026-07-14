<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '爬虫管理', path: '/crawler' },
  { label: '爬虫列表', path: '/crawler-list' },
]

const columns = [
  {
    title: '平台名称',
    key: 'name',
    search: true,
  },
  {
    title: '列表爬取数量',
    key: 'crawlCount',
  },
  {
    title: '列表成功数量',
    key: 'successCount',
  },
  {
    title: '列表失败数量',
    key: 'failCount',
  },
  {
    title: '列表爬取状态',
    key: 'listStatus',
    search: {
      type: 'select' as const,
      options: [
        { label: '运行中', value: 'running' },
        { label: '已停止', value: 'stopped' },
        { label: '异常', value: 'error' },
        { label: '已完成', value: 'completed' },
      ],
    },
  },
  {
    title: '详情爬取数量',
    key: 'detailCrawlCount',
  },
  {
    title: '详情成功数量',
    key: 'detailSuccessCount',
  },
  {
    title: '详情失败数量',
    key: 'detailFailCount',
  },
  {
    title: '详情爬取状态',
    key: 'detailStatus',
  },
  {
    title: '公司爬取数量',
    key: 'detailCrawlCount',
  },
  {
    title: '公司成功数量',
    key: 'detailSuccessCount',
  },
  {
    title: '公司失败数量',
    key: 'detailFailCount',
  },
  {
    title: '公司爬取状态',
    key: 'detailStatus',
  },
  {
    title: '爬取频率',
    key: 'frequency',
  },
  {
    title: '开始时间',
    key: 'startTime',
  },
  {
    title: '结束时间',
    key: 'endTime',
  },
]

const mockData = [
  {
    name: '智联招聘职位爬虫',
    type: '职位爬虫',
    targetSite: 'https://www.zhaopin.com',
    status: '运行中',
    startTime: '2024-01-15 09:00:00',
    endTime: '-',
    crawlCount: 15000,
    successCount: 14800,
    failCount: 200,
    successRate: '98.67%',
    frequency: '每小时',
    config: '{"maxPages": 1000, "delay": 2000}',
    errorMessage: '-',
    createTime: '2024-01-15 08:30:00',
    updateTime: '2024-01-20 14:30:00',
  },
  {
    name: '前程无忧企业爬虫',
    type: '企业爬虫',
    targetSite: 'https://www.51job.com',
    status: '已完成',
    startTime: '2024-01-10 10:00:00',
    endTime: '2024-01-12 18:00:00',
    crawlCount: 5000,
    successCount: 4950,
    failCount: 50,
    successRate: '99.00%',
    frequency: '每30分钟',
    config: '{"maxPages": 500, "delay": 1000}',
    errorMessage: '-',
    createTime: '2024-01-10 09:30:00',
    updateTime: '2024-01-12 18:30:00',
  },
  {
    name: '拉勾网行业爬虫',
    type: '行业爬虫',
    targetSite: 'https://www.lagou.com',
    status: '异常',
    startTime: '2024-01-18 14:00:00',
    endTime: '-',
    crawlCount: 3000,
    successCount: 2800,
    failCount: 200,
    successRate: '93.33%',
    frequency: '每2小时',
    config: '{"maxPages": 200, "delay": 3000}',
    errorMessage: '网络连接超时',
    createTime: '2024-01-18 13:30:00',
    updateTime: '2024-01-20 16:45:00',
  },
  {
    name: 'BOSS直聘薪资爬虫',
    type: '薪资爬虫',
    targetSite: 'https://www.zhipin.com',
    status: '已停止',
    startTime: '2024-01-05 08:00:00',
    endTime: '2024-01-08 20:00:00',
    crawlCount: 8000,
    successCount: 7600,
    failCount: 400,
    successRate: '95.00%',
    frequency: '每45分钟',
    config: '{"maxPages": 800, "delay": 1500}',
    errorMessage: '-',
    createTime: '2024-01-05 07:30:00',
    updateTime: '2024-01-08 20:30:00',
  },
  {
    name: '猎聘网职位爬虫',
    type: '职位爬虫',
    targetSite: 'https://www.liepin.com',
    status: '运行中',
    startTime: '2024-01-20 09:30:00',
    endTime: '-',
    crawlCount: 2000,
    successCount: 1950,
    failCount: 50,
    successRate: '97.50%',
    frequency: '每1小时',
    config: '{"maxPages": 300, "delay": 2500}',
    errorMessage: '-',
    createTime: '2024-01-20 09:00:00',
    updateTime: '2024-01-20 15:20:00',
  },
]

// 处理新增爬虫
const handleAddCrawler = () => {
  alert('新增爬虫功能')
}

// 处理导出爬虫数据
const handleExportCrawlers = () => {
  alert('导出爬虫数据功能')
}

// 处理启动爬虫
const handleStartCrawler = (crawler: any) => {
  alert(`启动爬虫: ${crawler.name}`)
}

// 处理停止爬虫
const handleStopCrawler = (crawler: any) => {
  alert(`停止爬虫: ${crawler.name}`)
}
</script>

<template>
  <div
    class="flex flex-col h-full mt-4 px-4"
    :style="{ boxSizing: 'border-box', width: 'calc(100vw - 200px - 1rem)' }"
  >
    <div class="flex-shrink-0 pr-4 mb-4">
      <Header
        :breadcrumbs="breadcrumbs"
        :show-scope="false"
        :show-province="false"
        :show-time="false"
      >
      </Header>
    </div>
    <div class="w-full pr-4 pb-4 overflow-hidden" :style="`height: calc(100vh - 1rem - 48px`">
      <VTable
        :columns="columns"
        :data="mockData"
        title="爬虫列表"
        @add="handleAddCrawler"
        @export="handleExportCrawlers"
      />
    </div>
  </div>
</template>
