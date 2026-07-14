<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'
import positionData from '~/data/position.json'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '工具助手', path: '/tool' },
  { label: '自定义图表', path: '/tool-chart' },
]

const columns = [
  {
    title: '统计口径',
    key: 'statisticMethod',
    width: 120,
    hidden: true,
    search: {
      type: 'select' as const,
      options: [
        { label: '全口径', value: 'all' },
        { label: '大专生', value: 'college' },
        { label: '应届大专生', value: 'collegeFresh' },
        { label: '本科生', value: 'bachelor' },
        { label: '应届本科生', value: 'bachelorFresh' },
        { label: '研究生及以上', value: 'masterPlus' },
      ],
    },
  },
  {
    title: '职位 ID',
    key: 'id',
    hidden: true,
  },
  {
    title: '职位名称',
    key: 'name',
    search: true,
  },
  {
    title: '发布日期',
    key: 'publishDate',
  },
  {
    title: '薪资范围',
    key: 'salaryRange',
  },
  {
    title: '招聘人数',
    key: 'recruitCount',
  },
  {
    title: '学历要求',
    key: 'education',
    search: {
      type: 'select' as const,
      options: [
        { label: '学历不限', value: '学历不限' },
        { label: '高中及以下', value: '高中及以下' },
        { label: '大专', value: '大专' },
        { label: '本科', value: '本科' },
        { label: '研究生及以上', value: '研究生及以上' },
      ],
    },
  },
  {
    title: '工作年限',
    key: 'workYear',
    search: {
      type: 'select' as const,
      options: [
        { label: '经验不限', value: '经验不限' },
        { label: '1年及无经验', value: '1年及无经验' },
        { label: '1-3年', value: '1-3年' },
        { label: '3-5年', value: '3-5年' },
        { label: '5-10年', value: '5-10年' },
        { label: '10年以上', value: '10年以上' },
      ],
    },
  },
  {
    title: '标准职业第三级(小类)',
    key: 'careerMinor',
  },
  {
    title: '标准职业',
    key: 'standardCareer',
    hidden: true,
    search: {
      type: 'treeSelect' as const,
    },
  },
  {
    title: '标准行业第三级(中类)',
    key: 'industryMedium',
    hidden: true,
    search: {
      type: 'treeSelect' as const,
    },
  },
  {
    title: '单位名称',
    key: 'companyName',
    search: true,
  },
  {
    title: '职位状态',
    key: 'status',
  },
  {
    title: '职位链接',
    key: 'link',
  },
  {
    title: '月薪倍数',
    key: 'salaryMultiple',
  },
  {
    title: '年薪',
    key: 'salaryYearly',
  },
  {
    title: '单位规模',
    key: 'companyScale',
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
    key: 'companyNature',
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
    key: 'companyStage',
  },
  {
    title: '单位人数',
    key: 'companySize',
  },
  {
    title: '单位地址',
    key: 'companyAddress',
  },
  {
    title: '单位行业所属三大产业',
    key: 'threeIndustry',
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
    title: '单位行业所属标准行业第一级（门类）',
    key: 'industryCategory',
    search: true,
  },
  {
    title: '单位行业所属标准行业第一级（门类）代码',
    key: 'industryCategoryCode',
  },
  {
    title: '单位行业所属标准行业第二级（大类）',
    key: 'industryMajor',
    search: true,
  },
  {
    title: '单位行业所属标准行业第二级（大类）代码',
    key: 'industryMajorCode',
  },
  {
    title: '单位行业所属标准行业第三级（中类）代码',
    key: 'industryMediumCode',
  },
  {
    title: '单位行业所属标准行业第四级（小类）',
    key: 'industryMinor',
    search: true,
  },
  {
    title: '单位行业所属标准行业第四级（小类）代码',
    key: 'industryMinorCode',
  },
  {
    title: '对应标准职业第一级（大类）',
    key: 'careerMajor',
    search: true,
  },
  {
    title: '对应标准职业第一级（大类）代码',
    key: 'careerMajorCode',
  },
  {
    title: '对应标准职业第二级（中类）',
    key: 'careerMedium',
    search: true,
  },
  {
    title: '对应标准职业第二级（中类）代码',
    key: 'careerMediumCode',
  },
  {
    title: '对应标准职业第三级（小类）代码',
    key: 'careerMinorCode',
  },
  {
    title: '对应标准职业第四级（细类）',
    key: 'careerDetail',
    search: true,
  },
  {
    title: '对应标准职业第四级（细类）代码',
    key: 'careerDetailCode',
  },
  {
    title: '单位链接',
    key: 'companyLink',
  },
  {
    title: '职位详情',
    key: 'description',
  },
  {
    title: '职位关键词',
    key: 'keywords',
  },
  {
    title: '关联专业',
    key: 'relatedMajor',
  },
  {
    title: '工作地点',
    key: 'workLocation',
  },
  {
    title: '工作省份',
    key: 'workProvince',
    search: true,
  },
  {
    title: '工作城市/区县',
    key: 'workCity',
    search: true,
  },
  {
    title: '职位类型',
    key: 'type',
  },
  {
    title: '员工福利',
    key: 'benefits',
  },
  {
    title: '职位发布人',
    key: 'publisher',
  },
  {
    title: '列表爬取时间',
    key: 'crawlListTime',
  },
  {
    title: '详情爬取时间',
    key: 'crawlDetailTime',
  },
  {
    title: '数据创建时间',
    key: 'createTime',
  },
  {
    title: '数据更新时间',
    key: 'updateTime',
  },
]

// 使用真实的职位数据
const mockData = positionData

// 处理新增职位
const handleAddPosition = () => {
  // 这里可以添加新增职位的逻辑，比如打开弹窗或跳转页面
  // 例如：router.push('/position/add')
  alert('新增职位功能')
}

// 处理导出职位数据
const handleExportPositions = () => {
  // 这里可以添加导出数据的逻辑
  // 例如：导出为 Excel 或 CSV 文件
  alert('导出职位数据功能')
}

// 处理职位名称点击
const handlePositionNameClick = (row: any) => {
  // 使用 navigateTo 进行路由跳转
  navigateTo(`/position-detail/${row.id}`)
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
        title="职位数据"
        @add="handleAddPosition"
        @export="handleExportPositions"
        @name-click="handlePositionNameClick"
      />
    </div>
  </div>
</template>
