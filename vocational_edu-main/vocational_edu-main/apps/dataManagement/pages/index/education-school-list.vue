<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '教育信息', path: '/education' },
  { label: '学校列表', path: '/education-school-list' },
]

const columns = [
  {
    title: '学校名称',
    key: 'name',
    width: 200,
    search: true,
  },
  {
    title: '学校类型',
    key: 'type',
    width: 120,
    search: {
      type: 'select' as const,
      options: [
        { label: '本科院校', value: 'undergraduate' },
        { label: '专科院校', value: 'college' },
        { label: '职业院校', value: 'vocational' },
      ],
    },
  },
  {
    title: '学校级别',
    key: 'level',
    width: 120,
    search: {
      type: 'select' as const,
      options: [
        { label: '双一流', value: 'double-first-class' },
        { label: '双高', value: 'double-high' },
        { label: '普通本科', value: 'regular-undergraduate' },
        { label: '普通专科', value: 'regular-college' },
      ],
    },
  },
  {
    title: '学校所在地',
    key: 'location',
    width: 120,
    search: true,
  },
  {
    title: '招生数',
    key: 'enrollment',
    width: 100,
  },
  {
    title: '在校学生数',
    key: 'studentCount',
    width: 120,
  },
  {
    title: '毕业生数',
    key: 'graduateCount',
    width: 100,
  },
  {
    title: '就业率',
    key: 'employmentRate',
    width: 100,
  },
  {
    title: '教职工数',
    key: 'teacherCount',
    width: 100,
  },
  {
    title: '生师比',
    key: 'studentTeacherRatio',
    width: 100,
  },
  {
    title: '专业数量',
    key: 'majorCount',
    width: 100,
  },
  {
    title: '优势专业',
    key: 'topMajors',
    width: 200,
  },
  {
    title: '新生高考平均分',
    key: 'avgFreshmanScore',
    width: 130,
  },
  {
    title: '本省生源占比',
    key: 'localStudentRatio',
    width: 120,
  },
  {
    title: '毕业生平均起薪',
    key: 'avgStartingSalary',
    width: 130,
  },
  {
    title: '专业对口率',
    key: 'jobMajorMatchRate',
    width: 120,
  },
  {
    title: '主要就业行业',
    key: 'topIndustries',
    width: 200,
  },
  {
    title: '主要就业城市',
    key: 'topEmploymentCities',
    width: 200,
  },
  {
    title: '重点雇主',
    key: 'keyEmployers',
    width: 200,
  },
  {
    title: '应届生岗位需求量',
    key: 'jobDemand',
    width: 150,
  },
  {
    title: '考研率',
    key: 'postgraduateRate',
    width: 100,
  },
  {
    title: '自主创业率',
    key: 'entrepreneurshipRate',
    width: 120,
  },
  {
    title: '毕业三年后平均薪资',
    key: 'avgSalaryAfter3Years',
    width: 150,
  },
  {
    title: '校友发展指数',
    key: 'alumniDevelopmentIndex',
    width: 130,
  },
]

const mockData = [
  {
    name: '清华大学',
    type: '本科院校',
    level: '双一流',
    location: '北京市',
    enrollment: 3800,
    studentCount: 15000,
    graduateCount: 3600,
    employmentRate: '98.5%',
    teacherCount: 3500,
    studentTeacherRatio: '4.3:1',
    majorCount: 81,
    topMajors: '计算机科学与技术,电子信息工程,机械工程',
    avgFreshmanScore: 680,
    localStudentRatio: '15%',
    avgStartingSalary: 15000,
    jobMajorMatchRate: '85%',
    topIndustries: '互联网/软件,金融,科研院所',
    topEmploymentCities: '北京,上海,深圳',
    keyEmployers: '华为,腾讯,百度,中科院',
    jobDemand: 2500,
    postgraduateRate: '70%',
    entrepreneurshipRate: '5%',
    avgSalaryAfter3Years: 25000,
    alumniDevelopmentIndex: 95,
  },
  {
    name: '北京大学',
    type: '本科院校',
    level: '双一流',
    location: '北京市',
    enrollment: 4000,
    studentCount: 16000,
    graduateCount: 3800,
    employmentRate: '98.2%',
    teacherCount: 3800,
    studentTeacherRatio: '4.2:1',
    majorCount: 125,
    topMajors: '数学,物理,化学,经济学',
    avgFreshmanScore: 675,
    localStudentRatio: '18%',
    avgStartingSalary: 14500,
    jobMajorMatchRate: '82%',
    topIndustries: '金融,教育,科研院所',
    topEmploymentCities: '北京,上海,深圳',
    keyEmployers: '中科院,北大方正,中信证券',
    jobDemand: 2200,
    postgraduateRate: '75%',
    entrepreneurshipRate: '4%',
    avgSalaryAfter3Years: 24000,
    alumniDevelopmentIndex: 98,
  },
  {
    name: '深圳职业技术学院',
    type: '专科院校',
    level: '双高',
    location: '深圳市',
    enrollment: 5000,
    studentCount: 18000,
    graduateCount: 4800,
    employmentRate: '96.8%',
    teacherCount: 1200,
    studentTeacherRatio: '15:1',
    majorCount: 85,
    topMajors: '电子信息工程技术,软件技术,数字媒体技术',
    avgFreshmanScore: 450,
    localStudentRatio: '60%',
    avgStartingSalary: 8000,
    jobMajorMatchRate: '78%',
    topIndustries: '制造业,信息技术,服务业',
    topEmploymentCities: '深圳,广州,东莞',
    keyEmployers: '华为,腾讯,比亚迪,富士康',
    jobDemand: 3200,
    postgraduateRate: '15%',
    entrepreneurshipRate: '8%',
    avgSalaryAfter3Years: 12000,
    alumniDevelopmentIndex: 75,
  },
  {
    name: '上海交通大学',
    type: '本科院校',
    level: '双一流',
    location: '上海市',
    enrollment: 4200,
    studentCount: 17000,
    graduateCount: 4000,
    employmentRate: '97.8%',
    teacherCount: 3200,
    studentTeacherRatio: '5.3:1',
    majorCount: 67,
    topMajors: '船舶与海洋工程,机械工程,电子信息',
    avgFreshmanScore: 670,
    localStudentRatio: '25%',
    avgStartingSalary: 14000,
    jobMajorMatchRate: '88%',
    topIndustries: '制造业,金融,信息技术',
    topEmploymentCities: '上海,北京,深圳',
    keyEmployers: '上汽集团,宝钢,中船集团',
    jobDemand: 2800,
    postgraduateRate: '65%',
    entrepreneurshipRate: '6%',
    avgSalaryAfter3Years: 23000,
    alumniDevelopmentIndex: 92,
  },
  {
    name: '北京工业职业技术学院',
    type: '专科院校',
    level: '双高',
    location: '北京市',
    enrollment: 3500,
    studentCount: 12000,
    graduateCount: 3200,
    employmentRate: '95.5%',
    teacherCount: 800,
    studentTeacherRatio: '15:1',
    majorCount: 45,
    topMajors: '机电一体化技术,数控技术,汽车检测与维修',
    avgFreshmanScore: 380,
    localStudentRatio: '70%',
    avgStartingSalary: 7500,
    jobMajorMatchRate: '80%',
    topIndustries: '制造业,汽车,机械',
    topEmploymentCities: '北京,天津,河北',
    keyEmployers: '北汽集团,首钢,中车集团',
    jobDemand: 1800,
    postgraduateRate: '12%',
    entrepreneurshipRate: '6%',
    avgSalaryAfter3Years: 11000,
    alumniDevelopmentIndex: 68,
  },
]

// 处理新增学校
const handleAddSchool = () => {
  alert('新增学校功能')
}

// 处理导出学校数据
const handleExportSchools = () => {
  alert('导出学校数据功能')
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
        title="学校列表"
        @add="handleAddSchool"
        @export="handleExportSchools"
      />
    </div>
  </div>
</template>
