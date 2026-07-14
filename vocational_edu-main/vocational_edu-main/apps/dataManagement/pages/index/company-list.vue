<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '企业信息', path: '/company' },
  { label: '企业列表', path: '/company-list' },
]

const columns = [
  {
    title: '单位ID',
    key: 'id',
    width: 120,
  },
  {
    title: '单位全称',
    key: 'name',
    width: 200,
    search: true,
  },
  {
    title: '单位简称',
    key: 'shortName',
    width: 200,
    search: true,
  },
  {
    title: '单位规模',
    key: 'size',
    width: 120,
    search: {
      type: 'select' as const,
      options: [
        { label: '小微型企业', value: 'small' },
        { label: '中型企业', value: 'medium' },
        { label: '大型企业', value: 'large' },
      ],
    },
  },
  {
    title: '单位性质',
    key: 'nature',
    width: 120,
    search: {
      type: 'select' as const,
      options: [
        { label: '国有企业', value: 'state-owned' },
        { label: '民营企业', value: 'private' },
        { label: '外资企业', value: 'foreign' },
        { label: '合资企业', value: 'joint-venture' },
        { label: '事业单位', value: 'institution' },
      ],
    },
  },
  {
    title: '单位融资情况',
    key: 'finance',
    width: 120,
    search: {
      type: 'select' as const,
      options: [
        { label: '未融资', value: '未融资' },
        { label: '天使轮', value: '天使轮' },
        { label: 'A轮', value: 'A' },
        { label: 'B轮', value: 'B' },
        { label: 'C轮', value: 'C' },
        { label: 'D轮及以上', value: 'D' },
        { label: '已上市', value: '已上市' },
        { label: '自有资金', value: '自有资金' },
      ],
    },
  },
  {
    title: '所属行业第四级(小类)',
    key: 'industryMinor',
    width: 150,
  },
  {
    title: '所属行业第四级(小类)代码',
    key: 'industryMinorCode',
    width: 150,
  },
  {
    title: '所属行业第三级(中类)',
    key: 'industryMedium',
    width: 150,
  },
  {
    title: '所属行业第三级(中类)代码',
    key: 'industryMediumCode',
    width: 150,
  },
  {
    title: '所属行业第二级(大类)',
    key: 'industryMajor',
    width: 150,
  },
  {
    title: '所属行业第二级(大类)代码',
    key: 'industryMajorCode',
    width: 150,
  },
  {
    title: '所属行业第一级(门类)',
    key: 'industryCategory',
    width: 150,
  },
  {
    title: '所属行业第一级(门类)代码',
    key: 'industryCategoryCode',
    width: 150,
  },
  {
    title: '所属三大产业',
    key: 'threeIndustries',
    width: 150,
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
    title: '单位人数',
    key: 'employeeCount',
    width: 100,
  },
  {
    title: '单位介绍',
    key: 'description',
    width: 300,
  },
  {
    title: '主营业务',
    key: 'mainBusiness',
    width: 200,
  },
  {
    title: '单位地址',
    key: 'address',
    width: 200,
  },
  {
    title: '成立时间',
    key: 'establishTime',
    width: 120,
  },
  {
    title: '注册资本',
    key: 'registeredCapital',
    width: 120,
  },
  {
    title: '招聘职位数',
    key: 'jobCount',
    width: 120,
  },
  {
    title: '招聘人数',
    key: 'recruitCount',
    width: 120,
  },
  {
    title: '平均薪资',
    key: 'averageSalary',
    width: 120,
  },
  {
    title: '薪资中位数',
    key: 'salary50',
    width: 120,
  },
  {
    title: '招聘涉及的行业(中类)',
    key: 'industry',
    width: 120,
  },
  {
    title: '招聘涉及的职业(小类)',
    key: 'career',
    width: 120,
  },
  {
    title: '学历要求',
    key: 'educationDistribution',
    width: 200,
  },
  {
    title: '工作年限',
    key: 'workYearDistribution',
    width: 200,
  },
  {
    title: '福利待遇',
    key: 'benefits',
    width: 250,
  },
  {
    title: '联系方式',
    key: 'contact',
    width: 120,
  },
  {
    title: '官网地址',
    key: 'website',
    width: 200,
  },
  {
    title: '法定代表人',
    key: 'legalRepresentative',
    width: 120,
  },
  {
    title: '统一社会信用代码',
    key: 'creditCode',
    width: 120,
  },
]

const mockData = [
  {
    name: '腾讯科技（深圳）有限单位',
    nature: '民营企业',
    size: '大型企业',
    industry: '互联网/软件',
    address: '深圳市南山区科技园',
    establishTime: '1998-11-11',
    registeredCapital: '2000万人民币',
    employeeCount: 100000,
    mainBusiness: '互联网综合服务',
    description: '腾讯是一家以互联网为基础的科技与文化单位',
    jobCount: 2500,
    recruitCount: 5000,
    averageSalary: 25000,
    educationDistribution: '本科及以上: 85%, 硕士及以上: 15%',
    workYearDistribution: '应届生: 20%, 1-3年: 40%, 3-5年: 30%, 5年以上: 10%',
    benefits: '五险一金, 年终奖, 股票期权, 带薪年假',
    contact: '0755-86013388',
    website: 'https://www.tencent.com',
  },
  {
    name: '阿里巴巴（中国）有限单位',
    nature: '民营企业',
    size: '大型企业',
    industry: '电子商务/互联网',
    address: '杭州市余杭区文一西路969号',
    establishTime: '1999-09-09',
    registeredCapital: '5000万人民币',
    employeeCount: 120000,
    mainBusiness: '电子商务平台运营',
    description: '阿里巴巴集团是以曾担任英语教师的马云为首的18人于1999年在浙江杭州创立的单位',
    jobCount: 3200,
    recruitCount: 6000,
    averageSalary: 28000,
    educationDistribution: '本科及以上: 80%, 硕士及以上: 20%',
    workYearDistribution: '应届生: 15%, 1-3年: 35%, 3-5年: 35%, 5年以上: 15%',
    benefits: '五险一金, 年终奖, 股权激励, 免费班车',
    contact: '0571-85022088',
    website: 'https://www.alibaba.com',
  },
  {
    name: '华为技术有限单位',
    nature: '民营企业',
    size: '大型企业',
    industry: '通信设备/电子',
    address: '深圳市龙岗区坂田华为基地',
    establishTime: '1987-09-15',
    registeredCapital: '403.08亿人民币',
    employeeCount: 197000,
    mainBusiness: '通信设备制造',
    description: '华为是全球领先的ICT（信息与通信）基础设施和智能终端提供商',
    jobCount: 1800,
    recruitCount: 3500,
    averageSalary: 30000,
    educationDistribution: '本科及以上: 70%, 硕士及以上: 30%',
    workYearDistribution: '应届生: 10%, 1-3年: 25%, 3-5年: 40%, 5年以上: 25%',
    benefits: '五险一金, 年终奖, 股权分红, 海外工作机会',
    contact: '0755-28780808',
    website: 'https://www.huawei.com',
  },
  {
    name: '字节跳动科技有限单位',
    nature: '民营企业',
    size: '大型企业',
    industry: '互联网/移动互联网',
    address: '北京市海淀区知春路63号',
    establishTime: '2012-03-09',
    registeredCapital: '1000万人民币',
    employeeCount: 150000,
    mainBusiness: '移动互联网产品研发',
    description: '字节跳动是一家全球化的互联网技术单位',
    jobCount: 2800,
    recruitCount: 4500,
    averageSalary: 32000,
    educationDistribution: '本科及以上: 75%, 硕士及以上: 25%',
    workYearDistribution: '应届生: 25%, 1-3年: 45%, 3-5年: 25%, 5年以上: 5%',
    benefits: '五险一金, 年终奖, 股票期权, 免费三餐',
    contact: '010-82829999',
    website: 'https://www.bytedance.com',
  },
  {
    name: '百度在线网络技术（北京）有限单位',
    nature: '民营企业',
    size: '大型企业',
    industry: '互联网/人工智能',
    address: '北京市海淀区上地十街10号',
    establishTime: '2000-01-01',
    registeredCapital: '2000万人民币',
    employeeCount: 45000,
    mainBusiness: '搜索引擎和人工智能',
    description: '百度是全球最大的中文搜索引擎、最大的中文网站',
    jobCount: 1200,
    recruitCount: 2000,
    averageSalary: 22000,
    educationDistribution: '本科及以上: 80%, 硕士及以上: 20%',
    workYearDistribution: '应届生: 20%, 1-3年: 40%, 3-5年: 30%, 5年以上: 10%',
    benefits: '五险一金, 年终奖, 股票期权, 技术培训',
    contact: '010-59928888',
    website: 'https://www.baidu.com',
  },
]

// 处理新增企业
const handleAddCompany = () => {
  alert('新增企业功能')
}

// 处理导出企业数据
const handleExportCompanies = () => {
  alert('导出企业数据功能')
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
        title="企业列表"
        @add="handleAddCompany"
        @export="handleExportCompanies"
      />
    </div>
  </div>
</template>
