<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '薪资信息', path: '/salary' },
  { label: '薪资列表', path: '/salary-list' }
]

const columns = [
  {
    title: '薪资区间（平均月薪）',
    key: 'salaryRange',
    width: 180,
    search: true
  },
  {
    title: '职位总个数',
    key: 'jobCount',
    width: 130
  },
  {
    title: '招聘总人数',
    key: 'recruitCount',
    width: 120
  },
  {
    title: '单位总个数',
    key: 'totalCompanies',
    width: 100
  },
  {
    title: '行业总个数',
    key: 'industryCount',
    width: 100
  },
  {
    title: '职业总个数',
    key: 'careerCount',
    width: 100
  },
  {
    title: '单位规模分布',
    key: 'companySizeDistribution',
    width: 200
  },
  {
    title: '学历要求分布',
    key: 'educationDistribution',
    width: 200
  },
  {
    title: '工作年限分布',
    key: 'workYearDistribution',
    width: 200
  },
  {
    title: '平均薪资',
    key: 'averageSalary',
    width: 100
  },
  {
    title: '薪资25%分位数',
    key: 'salary25',
    width: 120
  },
  {
    title: '薪资中位数',
    key: 'medianSalary',
    width: 120
  },
  {
    title: '薪资75%分位数',
    key: 'salary75',
    width: 120
  },
  {
    title: '薪资标准差',
    key: 'salaryStdDev',
    width: 120
  },
  {
    title: '薪资变异系数',
    key: 'salaryCoefficient',
    width: 130
  }
]

const mockData = []

// 处理新增薪资数据
const handleAddSalary = () => {
  alert('新增薪资数据功能')
}

// 处理导出薪资数据
const handleExportSalaries = () => {
  alert('导出薪资数据功能')
}
</script>

<template>
  <div class="flex flex-col h-full mt-4 px-4" :style="{ boxSizing: 'border-box', width: 'calc(100vw - 200px - 1rem)' }">
    <div class="flex-shrink-0 pr-4 mb-4">
      <Header :breadcrumbs="breadcrumbs" :show-scope="false" :show-province="false" :show-time="false"></Header>
    </div>
    <div class="w-full pr-4 pb-4 overflow-hidden" :style="`height: calc(100vh - 1rem - 48px`">
      <VTable
        :columns="columns"
        :data="mockData"
        title="薪资列表"
        @add="handleAddSalary"
        @export="handleExportSalaries"
      />
    </div>
  </div>
</template>
