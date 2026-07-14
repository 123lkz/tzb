<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '行业信息', path: '/industry' },
  { label: '行业列表', path: '/industry-list' },
]

const columns = [
  {
    title: '行业名称',
    key: 'name',
    search: true,
  },
  {
    title: '行业代码',
    key: 'code',
    search: true,
  },
  {
    title: '行业等级',
    key: 'level',
    search: {
      type: 'select' as const,
      options: [
        { label: '门类', value: 'level1' },
        { label: '大类', value: 'level2' },
        { label: '中类', value: 'level3' },
        { label: '小类', value: 'level4' },
      ],
    },
  },
  {
    title: '所属三大产业',
    key: 'industry',
    search: {
      type: 'select' as const,
      options: [
        { label: '第一产业', value: 'primary' },
        { label: '第二产业', value: 'secondary' },
        { label: '第三产业', value: 'tertiary' },
      ],
    },
  },
  {
    title: '行业门类名称',
    key: 'major',
  },
  {
    title: '行业门类代码',
    key: 'majorCode',
  },
  {
    title: '行业大类名称',
    key: 'medium',
  },
  {
    title: '行业大类代码',
    key: 'mediumCode',
  },
  {
    title: '行业中类名称',
    key: 'minor',
  },
  {
    title: '行业中类代码',
    key: 'minorCode',
  },
  {
    title: '行业小类名称',
    key: 'detail',
  },
  {
    title: '行业小类代码',
    key: 'detailCode',
  },
  {
    title: '招聘职位总个数',
    key: 'recruitProfessionCount',
  },
  {
    title: '招聘总人数',
    key: 'recruitPersonCount',
  },
  {
    title: '招聘单位数',
    key: 'recruitCompanyCount',
  },
  {
    title: '薪资10%分位数',
    key: 'salary10',
  },
  {
    title: '薪资25%分位数',
    key: 'salary25',
  },
  {
    title: '薪资中位数',
    key: 'salary50',
  },
  {
    title: '薪资平均',
    key: 'salaryAverage',
  },
  {
    title: '薪资75%分位数',
    key: 'salary75',
  },
  {
    title: '薪资90%分位数',
    key: 'salary90',
  },
  {
    title: '招聘涉及的行业个数', // 如果是细类那就只有一个，如果是中类那就多个，如果是大类那就多个，如果是门类那就多个
    key: 'industryCount',
  },
  {
    title: '招聘职业总个数',
    key: 'careerCount',
  },
  {
    title: '学历要求',
    key: 'educationOptions',
  },
  {
    title: '工作年限要求',
    key: 'workYearOptions',
  },
  {
    title: '行业描述',
    key: 'description',
  },
]

const mockData = [
  {
    name: '互联网和相关服务',
    code: '64',
    level: '一级行业',
    industry: '第三产业',
    major: '信息传输、软件和信息技术服务业',
    medium: '互联网和相关服务',
    minor: '互联网信息服务',
    detail: '互联网信息服务',
    recruitProfessionCount: 15000,
    recruitPersonCount: 45000,
    recruitCompanyCount: 2500,
    salary10: 8000,
    salary25: 15000,
    salary50: 25000,
    salaryAverage: 28000,
    salary75: 35000,
    salary90: 50000,
    educationOptions: '本科及以上: 85%, 硕士及以上: 15%',
    workYearOptions: '应届生: 20%, 1-3年: 40%, 3-5年: 30%, 5年以上: 10%',
    description: '提供互联网信息服务、数据处理和存储服务、互联网接入服务等',
  },
  {
    name: '软件和信息技术服务业',
    code: '65',
    level: '一级行业',
    industry: '第三产业',
    major: '信息传输、软件和信息技术服务业',
    medium: '软件和信息技术服务业',
    minor: '软件开发',
    detail: '应用软件开发',
    recruitProfessionCount: 12000,
    recruitPersonCount: 35000,
    recruitCompanyCount: 2000,
    salary10: 10000,
    salary25: 18000,
    salary50: 28000,
    salaryAverage: 32000,
    salary75: 40000,
    salary90: 60000,
    educationOptions: '本科及以上: 80%, 硕士及以上: 20%',
    workYearOptions: '应届生: 15%, 1-3年: 35%, 3-5年: 35%, 5年以上: 15%',
    description: '从事软件开发、信息系统集成服务、信息技术咨询服务等',
  },
  {
    name: '金融业',
    code: '66',
    level: '一级行业',
    industry: '第三产业',
    major: '金融业',
    medium: '货币金融服务',
    minor: '银行',
    detail: '商业银行',
    recruitProfessionCount: 8000,
    recruitPersonCount: 20000,
    recruitCompanyCount: 500,
    salary10: 12000,
    salary25: 20000,
    salary50: 30000,
    salaryAverage: 35000,
    salary75: 45000,
    salary90: 70000,
    educationOptions: '本科及以上: 90%, 硕士及以上: 30%',
    workYearOptions: '应届生: 10%, 1-3年: 25%, 3-5年: 40%, 5年以上: 25%',
    description: '从事货币金融服务、资本市场服务、保险业等金融活动',
  },
  {
    name: '制造业',
    code: '13-43',
    level: '一级行业',
    industry: '第二产业',
    major: '制造业',
    medium: '计算机、通信和其他电子设备制造业',
    minor: '计算机制造',
    detail: '计算机整机制造',
    recruitProfessionCount: 10000,
    recruitPersonCount: 30000,
    recruitCompanyCount: 1500,
    salary10: 6000,
    salary25: 10000,
    salary50: 15000,
    salaryAverage: 18000,
    salary75: 25000,
    salary90: 40000,
    educationOptions: '本科及以上: 60%, 专科: 30%, 高中及以下: 10%',
    workYearOptions: '应届生: 25%, 1-3年: 35%, 3-5年: 25%, 5年以上: 15%',
    description: '从事各种制造活动，包括计算机、通信设备、电子设备等制造',
  },
  {
    name: '教育',
    code: '83',
    level: '一级行业',
    industry: '第三产业',
    major: '教育',
    medium: '高等教育',
    minor: '普通高等教育',
    detail: '本科教育',
    recruitProfessionCount: 5000,
    recruitPersonCount: 12000,
    recruitCompanyCount: 800,
    salary10: 5000,
    salary25: 8000,
    salary50: 12000,
    salaryAverage: 15000,
    salary75: 20000,
    salary90: 35000,
    educationOptions: '硕士及以上: 70%, 本科: 30%',
    workYearOptions: '应届生: 30%, 1-3年: 25%, 3-5年: 25%, 5年以上: 20%',
    description: '从事各级各类教育活动，包括学前教育、初等教育、中等教育、高等教育等',
  },
]

// 处理新增行业
const handleAddIndustry = () => {
  alert('新增行业功能')
}

// 处理导出行业数据
const handleExportIndustries = () => {
  alert('导出行业数据功能')
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
        title="行业列表"
        @add="handleAddIndustry"
        @export="handleExportIndustries"
      />
    </div>
  </div>
</template>
