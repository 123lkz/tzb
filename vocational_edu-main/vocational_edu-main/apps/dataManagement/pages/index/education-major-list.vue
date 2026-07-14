<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '教育信息', path: '/education' },
  { label: '专业列表', path: '/education-major-list' },
]

const columns = [
  {
    title: '专业名称',
    key: 'name',
    search: true,
  },
  {
    title: '专业代码',
    key: 'code',
    search: true,
  },
  {
    title: '专业类型',
    key: 'type',
    search: {
      type: 'select' as const,
      options: [
        { label: '本科专业', value: 'undergraduate' },
        { label: '专科专业', value: 'college' },
        { label: '职业专业', value: 'vocational' },
      ],
    },
  },
  {
    title: '学科门类',
    key: 'category',
    search: {
      type: 'select' as const,
      options: [
        { label: '工学', value: 'engineering' },
        { label: '理学', value: 'science' },
        { label: '文学', value: 'literature' },
        { label: '经济学', value: 'economics' },
        { label: '管理学', value: 'management' },
        { label: '法学', value: 'law' },
        { label: '教育学', value: 'education' },
        { label: '艺术学', value: 'arts' },
        { label: '农学', value: 'agriculture' },
        { label: '医学', value: 'medicine' },
      ],
    },
  },
  {
    title: '专业方向',
    key: 'direction',
  },
  {
    title: '年招生人数',
    key: 'enrollment',
  },
  {
    title: '在校学生数',
    key: 'studentCount',
  },
  {
    title: '年毕业生数',
    key: 'graduateCount',
  },
  {
    title: '就业率',
    key: 'employmentRate',
  },
  {
    title: '平均起薪',
    key: 'averageSalary',
  },
  {
    title: '升学率',
    key: 'promotionRate',
  },
  {
    title: '性别比例',
    key: 'genderRatio',
  },
  {
    title: '师资人数',
    key: 'teacherCount',
  },
  {
    title: '实验室数量',
    key: 'laboratoryCount',
  },
  {
    title: '核心课程',
    key: 'coreCourse',
  },
  {
    title: '专业介绍',
    key: 'introduction',
  },
  {
    title: '授予学位',
    key: 'degree',
  },
  {
    title: '修业年限',
    key: 'duration',
  },
  {
    title: '认证状态',
    key: 'certificationStatus',
  },
  {
    title: '行业分布',
    key: 'industryDistribution',
  },
  {
    title: '就业方向',
    key: 'employmentDirection',
  },
  {
    title: '就业地域',
    key: 'employmentRegion',
  },
  {
    title: '就业城市',
    key: 'employmentCity',
  },
]

const mockData = [
  {
    name: '计算机科学与技术',
    code: '080901',
    type: '本科专业',
    category: '工学',
    direction: '软件工程',
    enrollment: 5000,
    studentCount: 20000,
    graduateCount: 4800,
    employmentRate: '95.5%',
    averageSalary: 12000,
    promotionRate: '25%',
    genderRatio: '男:女 = 7:3',
    teacherCount: 800,
    laboratoryCount: 25,
    coreCourse: '数据结构,算法设计,操作系统,数据库原理',
    introduction:
      '培养具有良好的科学素养，系统地掌握计算机科学与技术的基本理论、基本知识和基本技能与方法',
    degree: '工学学士',
    duration: '4年',
    certificationStatus: '已认证',
    industryDistribution: '互联网/软件: 60%, 金融: 15%, 制造业: 10%, 其他: 15%',
    employmentDirection: '软件开发,系统分析,网络工程,数据库管理',
    employmentRegion: '一线城市: 70%, 新一线城市: 20%, 其他: 10%',
    employmentCity: '北京,上海,深圳,杭州',
  },
  {
    name: '软件工程',
    code: '080902',
    type: '本科专业',
    category: '工学',
    direction: '移动应用开发',
    enrollment: 4500,
    studentCount: 18000,
    graduateCount: 4300,
    employmentRate: '96.8%',
    averageSalary: 13000,
    promotionRate: '22%',
    genderRatio: '男:女 = 6:4',
    teacherCount: 700,
    laboratoryCount: 20,
    coreCourse: '软件工程,软件测试,软件项目管理,人机交互',
    introduction:
      '培养适应计算机应用学科的发展，特别是软件产业的发展，具备计算机软件的基础理论、基本知识和基本技能',
    degree: '工学学士',
    duration: '4年',
    certificationStatus: '已认证',
    industryDistribution: '互联网/软件: 65%, 金融: 12%, 制造业: 8%, 其他: 15%',
    employmentDirection: '软件开发,软件测试,项目管理,产品经理',
    employmentRegion: '一线城市: 75%, 新一线城市: 18%, 其他: 7%',
    employmentCity: '北京,上海,深圳,杭州,成都',
  },
  {
    name: '电子信息工程',
    code: '080701',
    type: '本科专业',
    category: '工学',
    direction: '通信工程',
    enrollment: 4000,
    studentCount: 16000,
    graduateCount: 3800,
    employmentRate: '94.2%',
    averageSalary: 11000,
    promotionRate: '28%',
    genderRatio: '男:女 = 8:2',
    teacherCount: 600,
    laboratoryCount: 18,
    coreCourse: '电路分析,信号与系统,通信原理,数字信号处理',
    introduction:
      '培养具备电子技术和信息系统的基础知识，能从事各类电子设备和信息系统的研究、设计、制造、应用和开发',
    degree: '工学学士',
    duration: '4年',
    certificationStatus: '已认证',
    industryDistribution: '通信设备: 40%, 电子制造: 25%, 互联网: 20%, 其他: 15%',
    employmentDirection: '硬件设计,通信工程,电子制造,系统集成',
    employmentRegion: '一线城市: 60%, 新一线城市: 25%, 其他: 15%',
    employmentCity: '深圳,北京,上海,西安,成都',
  },
  {
    name: '机械工程',
    code: '080201',
    type: '本科专业',
    category: '工学',
    direction: '机械设计制造',
    enrollment: 3500,
    studentCount: 14000,
    graduateCount: 3300,
    employmentRate: '92.8%',
    averageSalary: 9000,
    promotionRate: '15%',
    genderRatio: '男:女 = 9:1',
    teacherCount: 500,
    laboratoryCount: 15,
    coreCourse: '机械设计,机械制造,材料力学,机械原理',
    introduction:
      '培养具备机械设计、制造、自动化基础知识与应用能力，能在工业生产第一线从事机械制造领域内的设计制造',
    degree: '工学学士',
    duration: '4年',
    certificationStatus: '已认证',
    industryDistribution: '制造业: 50%, 汽车: 20%, 航空航天: 15%, 其他: 15%',
    employmentDirection: '机械设计,制造工艺,设备维护,项目管理',
    employmentRegion: '一线城市: 45%, 新一线城市: 35%, 其他: 20%',
    employmentCity: '上海,深圳,北京,苏州,重庆',
  },
  {
    name: '工商管理',
    code: '120201',
    type: '本科专业',
    category: '管理学',
    direction: '企业管理',
    enrollment: 3000,
    studentCount: 12000,
    graduateCount: 2800,
    employmentRate: '90.5%',
    averageSalary: 8500,
    promotionRate: '18%',
    genderRatio: '男:女 = 4:6',
    teacherCount: 400,
    laboratoryCount: 8,
    coreCourse: '管理学,经济学,市场营销,财务管理',
    introduction:
      '培养具备管理、经济、法律及企业管理方面的知识和能力，能在企、事业单位及政府部门从事管理以及教学、科研',
    degree: '管理学学士',
    duration: '4年',
    certificationStatus: '已认证',
    industryDistribution: '金融: 25%, 制造业: 20%, 服务业: 30%, 其他: 25%',
    employmentDirection: '企业管理,市场营销,人力资源,财务管理',
    employmentRegion: '一线城市: 55%, 新一线城市: 30%, 其他: 15%',
    employmentCity: '北京,上海,深圳,广州,杭州',
  },
]

// 处理新增专业
const handleAddMajor = () => {
  alert('新增专业功能')
}

// 处理导出专业数据
const handleExportMajors = () => {
  alert('导出专业数据功能')
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
        title="专业列表"
        @add="handleAddMajor"
        @export="handleExportMajors"
      />
    </div>
  </div>
</template>
