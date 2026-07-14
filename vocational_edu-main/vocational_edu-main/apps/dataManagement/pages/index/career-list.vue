<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '职业信息', path: '/career' },
  { label: '职业列表', path: '/career-list' },
]

const columns = [
  {
    title: '职业名称',
    key: 'name',
    width: 150,
    search: true,
  },
  {
    title: '职业代码',
    key: 'code',
    width: 120,
    search: true,
  },
  {
    title: '职业等级',
    key: 'level',
    width: 100,
    search: {
      type: 'select' as const,
      options: [
        { label: '大类', value: 'major' },
        { label: '中类', value: 'medium' },
        { label: '小类', value: 'senior' },
        { label: '细类', value: 'detail' },
      ],
    },
  },
  {
    title: '职业大类',
    key: 'major',
    width: 200,
    search: true,
  },
  {
    title: '职业大类代码',
    key: 'majorCode',
    width: 120,
  },
  {
    title: '职业中类',
    key: 'medium',
    width: 150,
    search: true,
  },
  {
    title: '职业中类代码',
    key: 'mediumCode',
    width: 120,
  },
  {
    title: '职业小类',
    key: 'minor',
    width: 120,
    search: true,
  },
  {
    title: '职业小类代码',
    key: 'minorCode',
    width: 120,
  },
  {
    title: '职业细类',
    key: 'detail',
    width: 120,
    search: true,
  },
  {
    title: '职业细类代码',
    key: 'detailCode',
    width: 120,
  },
  {
    title: '招聘职位总个数',
    key: 'recruitProfessionCount',
    width: 130,
  },
  {
    title: '招聘总人数',
    key: 'recruitPersonCount',
    width: 120,
  },
  {
    title: '招聘单位数',
    key: 'recruitCompanyCount',
    width: 120,
  },
  {
    title: '薪资10%分位数',
    key: 'salary10',
    width: 120,
  },
  {
    title: '薪资25%分位数',
    key: 'salary25',
    width: 120,
  },
  {
    title: '薪资中位数',
    key: 'salary50',
    width: 120,
  },
  {
    title: '薪资平均',
    key: 'salaryAverage',
    width: 120,
  },
  {
    title: '薪资75%分位数',
    key: 'salary75',
    width: 120,
  },
  {
    title: '薪资90%分位数',
    key: 'salary90',
    width: 120,
  },
  {
    title: '招聘涉及的行业个数',
    key: 'industryCount',
    width: 120,
  },
  {
    title: '招聘涉及的行业个数', // 如果是细类那就只有一个，如果是中类那就多个，如果是大类那就多个，如果是门类那就多个
    key: 'careerCount',
    width: 120,
  },
  {
    title: '学历要求',
    key: 'educationOptions',
    width: 120,
  },
  {
    title: '工作年限要求',
    key: 'workYearOptions',
    width: 130,
  },
  {
    title: '职业描述',
    key: 'description',
    width: 300,
  },
  {
    title: '关联招聘平台职业',
    key: 'relatedPlatformCareer',
    width: 200,
  },
  {
    title: '关联专业',
    key: 'relatedMajor',
    width: 200,
  },
]

const mockData = [
  {
    name: '软件工程师',
    code: '21301',
    level: '中级',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '软件开发',
    detail: '应用软件开发',
    recruitProfessionCount: 1250,
    recruitPersonCount: 3200,
    recruitCompanyCount: 450,
    salary10: 8000,
    salary25: 12000,
    salary50: 18000,
    salaryAverage: 20000,
    salary75: 25000,
    salary90: 35000,
    educationOptions: '本科及以上',
    workYearOptions: '3-5年',
    relatedMajor: '计算机科学与技术,软件工程',
    description: '负责软件系统的设计、开发和维护工作',
  },
  {
    name: '数据分析师',
    code: '21302',
    level: '中级',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '数据分析',
    detail: '商业数据分析',
    recruitProfessionCount: 680,
    recruitPersonCount: 1200,
    recruitCompanyCount: 280,
    salary10: 10000,
    salary25: 15000,
    salary50: 22000,
    salaryAverage: 25000,
    salary75: 30000,
    salary90: 40000,
    educationOptions: '本科及以上',
    workYearOptions: '2-4年',
    relatedMajor: '统计学,数学,计算机科学与技术',
    description: '负责数据收集、分析和报告工作',
  },
  {
    name: '产品经理',
    code: '21303',
    level: '高级',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '产品管理',
    detail: '互联网产品管理',
    recruitProfessionCount: 450,
    recruitPersonCount: 800,
    recruitCompanyCount: 200,
    salary10: 15000,
    salary25: 20000,
    salary50: 30000,
    salaryAverage: 35000,
    salary75: 45000,
    salary90: 60000,
    educationOptions: '本科及以上',
    workYearOptions: '5-8年',
    relatedMajor: '工商管理,计算机科学与技术',
    description: '负责产品规划、设计和运营管理',
  },
  {
    name: 'UI设计师',
    code: '21304',
    level: '中级',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '视觉设计',
    detail: '用户界面设计',
    recruitProfessionCount: 320,
    recruitPersonCount: 600,
    recruitCompanyCount: 150,
    salary10: 8000,
    salary25: 12000,
    salary50: 18000,
    salaryAverage: 20000,
    salary75: 25000,
    salary90: 35000,
    educationOptions: '本科及以上',
    workYearOptions: '2-5年',
    relatedMajor: '艺术设计,视觉传达设计',
    description: '负责用户界面和交互设计工作',
  },
  {
    name: '测试工程师',
    code: '21305',
    level: '中级',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '软件测试',
    detail: '功能测试',
    recruitProfessionCount: 280,
    recruitPersonCount: 500,
    recruitCompanyCount: 120,
    salary10: 7000,
    salary25: 10000,
    salary50: 15000,
    salaryAverage: 16000,
    salary75: 20000,
    salary90: 28000,
    educationOptions: '本科及以上',
    workYearOptions: '1-3年',
    relatedMajor: '计算机科学与技术,软件工程',
    description: '负责软件产品的测试和质量保证工作',
  },
]

// 处理新增职业
const handleAddCareer = () => {
  alert('新增职业功能')
}

// 处理导出职业数据
const handleExportCareers = () => {
  alert('导出职业数据功能')
}

// 处理职业名称点击
const handleCareerNameClick = (row: any) => {
  // 使用 navigateTo 进行路由跳转
  navigateTo(`/career-detail/${row.code}`)
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
        title="职业列表"
        @add="handleAddCareer"
        @export="handleExportCareers"
        @name-click="handleCareerNameClick"
      />
    </div>
  </div>
</template>
