<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import Icon from '~/components/common/Icon.vue'

// 获取路由参数
const route = useRoute()
const positionId = route.params.id as string

// 面包屑导航
const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '职位信息', path: '/position' },
  { label: '职位详情', path: `/position-detail/${positionId}` },
]

// 加载状态
const loading = ref(true)
const error = ref('')

// 职位详情数据接口
interface PositionDetail {
  id: string
  name: string
  status: string
  recruitCount: number
  company: string
  salaryRange: string
  salaryMultiple: number
  education: string
  workYear: string
  workLocation: string
  publishDate: string
  description: string
  requirements: string[]
  responsibilities: string[]
  benefits: string[]
  keywords: string[]
  link: string
  publisher: string
  employeeBenefits: string[]
}

// 公司信息接口
interface CompanyInfo {
  name: string
  type: string
  size: string
  nature: string
  address: string
  introduction: string
  mainBusiness: string
  website: string
  establishedYear: number
  employeeCount: number
}

// 行业信息接口
interface IndustryInfo {
  level1: string
  level2: string
  level3: string
  description: string
  trends: string[]
  relatedCareers: string[]
}

// 职业信息接口
interface CareerInfo {
  level1: string
  level2: string
  level3: string
  description: string
  skills: string[]
  relatedMajors: string[]
  salaryRange: {
    min: number
    max: number
    average: number
  }
}

// 职位详情数据
const positionDetail = ref<PositionDetail>({
  id: positionId,
  name: '',
  status: '',
  recruitCount: 0,
  company: '',
  salaryRange: '',
  salaryMultiple: 0,
  education: '',
  workYear: '',
  workLocation: '',
  publishDate: '',
  description: '',
  requirements: [],
  responsibilities: [],
  benefits: [],
  keywords: [],
  link: '',
  publisher: '',
  employeeBenefits: [],
})

const companyInfo = ref<CompanyInfo>({
  name: '北京科技有限公司',
  type: '大型企业',
  size: '1000人以上',
  nature: '民营企业',
  address: '北京市朝阳区建国路88号',
  introduction:
    '北京科技有限公司成立于2010年，是一家专注于互联网技术创新的高新技术企业。公司致力于为客户提供优质的技术解决方案，在行业内享有良好声誉。',
  mainBusiness: '软件开发、技术咨询、系统集成',
  website: 'https://www.example.com',
  establishedYear: 2010,
  employeeCount: 1200,
})

const industryInfo = ref<IndustryInfo>({
  level1: '信息传输、软件和信息技术服务业',
  level2: '软件和信息技术服务业',
  level3: '软件开发',
  description:
    '软件和信息技术服务业是国民经济的重要支柱产业，随着数字化转型的深入推进，该行业呈现出快速发展的态势。',
  trends: [
    '人工智能技术广泛应用',
    '云计算服务需求增长',
    '移动互联网持续发展',
    '大数据分析技术成熟',
    '物联网应用场景拓展',
  ],
  relatedCareers: [
    '软件工程师',
    '前端开发工程师',
    '后端开发工程师',
    '产品经理',
    'UI/UX设计师',
    '测试工程师',
  ],
})

const careerInfo = ref<CareerInfo>({
  level1: '专业技术人员',
  level2: '软件和信息技术服务人员',
  level3: '计算机软件工程技术人员',
  description:
    '前端开发工程师是负责用户界面开发的专业技术人员，需要具备扎实的编程基础和良好的用户体验意识。',
  skills: [
    'HTML/CSS/JavaScript',
    'Vue.js/React/Angular',
    'TypeScript',
    'Node.js',
    'Webpack/Vite',
    'Git版本控制',
  ],
  relatedMajors: ['计算机科学与技术', '软件工程', '网络工程', '信息管理与信息系统', '数字媒体技术'],
  salaryRange: {
    min: 12000,
    max: 25000,
    average: 18000,
  },
})

// 其他信息
const otherInfo = ref({
  workEnvironment: '现代化办公环境，配备最新开发设备',
  teamSize: '前端团队15人，技术氛围浓厚',
  developmentTools: ['VS Code', 'Chrome DevTools', 'Figma', 'Postman'],
  learningOpportunities: ['技术分享会', '外部培训', '在线课程', '技术大会参与'],
  careerDevelopment: ['技术专家路线', '管理岗位晋升', '产品经理转岗', '创业机会'],
})

// API响应接口
interface ApiResponse {
  id?: string
  name?: string
  title?: string
  status?: string
  recruitCount?: number
  recruit_count?: number
  company?: string
  company_name?: string
  salaryRange?: string
  salary_range?: string
  salaryMultiple?: number
  salary_multiple?: number
  education?: string
  education_requirement?: string
  workYear?: string
  work_year?: string
  workLocation?: string
  work_location?: string
  publishDate?: string
  publish_date?: string
  description?: string
  job_description?: string
  requirements?: string[]
  job_requirements?: string[]
  responsibilities?: string[]
  job_responsibilities?: string[]
  benefits?: string[]
  employee_benefits?: string[]
  keywords?: string[]
  skills?: string[]
  link?: string
  job_link?: string
  publisher?: string
  hr_name?: string
  employeeBenefits?: string[]
  companyInfo?: any
  company_info?: any
  industryInfo?: any
  industry_info?: any
  careerInfo?: any
  career_info?: any
}

// API调用函数
const fetchPositionDetail = async () => {
  try {
    loading.value = true
    error.value = ''

    // 调用API获取职位详情
    const response = await $fetch(
      `http://192.168.1.187:8568/zjdata/position-detail/${positionId}`,
      {
        method: 'GET',
      }
    )

    const data = response as ApiResponse

    if (data) {
      // 更新职位详情数据
      positionDetail.value = {
        id: data.id || positionId,
        name: data.name || data.title || '未知职位',
        status: data.status || '在招',
        recruitCount: data.recruitCount || data.recruit_count || 1,
        company: data.company || data.company_name || '未知公司',
        salaryRange: data.salaryRange || data.salary_range || '面议',
        salaryMultiple: data.salaryMultiple || data.salary_multiple || 1,
        education: data.education || data.education_requirement || '不限',
        workYear: data.workYear || data.work_year || '不限',
        workLocation: data.workLocation || data.work_location || '未知地点',
        publishDate:
          data.publishDate || data.publish_date || new Date().toISOString().split('T')[0],
        description: data.description || data.job_description || '暂无描述',
        requirements: data.requirements || data.job_requirements || [],
        responsibilities: data.responsibilities || data.job_responsibilities || [],
        benefits: data.benefits || data.employee_benefits || [],
        keywords: data.keywords || data.skills || [],
        link: data.link || data.job_link || '',
        publisher: data.publisher || data.hr_name || 'HR部门',
        employeeBenefits: data.employeeBenefits || data.benefits || [],
      }

      // 更新公司信息（如果API返回了公司信息）
      if (data.companyInfo || data.company_info) {
        const company = data.companyInfo || data.company_info
        companyInfo.value = {
          name: company.name || positionDetail.value.company,
          type: company.type || '未知类型',
          size: company.size || '未知规模',
          nature: company.nature || '未知性质',
          address: company.address || '未知地址',
          introduction: company.introduction || company.description || '暂无介绍',
          mainBusiness: company.mainBusiness || company.main_business || '未知业务',
          website: company.website || '',
          establishedYear: company.establishedYear || company.established_year || 0,
          employeeCount: company.employeeCount || company.employee_count || 0,
        }
      }

      // 更新行业信息（如果API返回了行业信息）
      if (data.industryInfo || data.industry_info) {
        const industry = data.industryInfo || data.industry_info
        industryInfo.value = {
          level1: industry.level1 || industry.level_1 || '未知行业',
          level2: industry.level2 || industry.level_2 || '未知子行业',
          level3: industry.level3 || industry.level_3 || '未知细分行业',
          description: industry.description || '暂无描述',
          trends: industry.trends || [],
          relatedCareers: industry.relatedCareers || industry.related_careers || [],
        }
      }

      // 更新职业信息（如果API返回了职业信息）
      if (data.careerInfo || data.career_info) {
        const career = data.careerInfo || data.career_info
        careerInfo.value = {
          level1: career.level1 || career.level_1 || '未知职业',
          level2: career.level2 || career.level_2 || '未知子职业',
          level3: career.level3 || career.level_3 || '未知细分职业',
          description: career.description || '暂无描述',
          skills: career.skills || [],
          relatedMajors: career.relatedMajors || career.related_majors || [],
          salaryRange: career.salaryRange ||
            career.salary_range || {
              min: 0,
              max: 0,
              average: 0,
            },
        }
      }
    }
  } catch (err: any) {
    // eslint-disable-next-line no-console
    console.error('获取职位详情失败:', err)
    error.value = err.message || '获取职位详情失败，请稍后重试'

    // 如果API调用失败，使用默认数据
    positionDetail.value = {
      id: positionId,
      name: '职位详情加载失败',
      status: '未知',
      recruitCount: 0,
      company: '未知公司',
      salaryRange: '面议',
      salaryMultiple: 1,
      education: '不限',
      workYear: '不限',
      workLocation: '未知地点',
      publishDate: new Date().toISOString().split('T')[0],
      description: '抱歉，无法加载职位详情信息。',
      requirements: ['请稍后重试或联系管理员'],
      responsibilities: ['请稍后重试或联系管理员'],
      benefits: [],
      keywords: [],
      link: '',
      publisher: '系统',
      employeeBenefits: [],
    }
  } finally {
    loading.value = false
  }
}

// 处理返回按钮
const handleBack = () => {
  navigateTo('/position-list')
}

// 处理申请职位
const handleApply = () => {
  // 这里可以添加申请职位的逻辑
  alert('申请职位功能')
}

// 处理收藏职位
const handleFavorite = () => {
  // 这里可以添加收藏职位的逻辑
  alert('收藏职位功能')
}

// 处理分享职位
const handleShare = () => {
  // 这里可以添加分享职位的逻辑
  alert('分享职位功能')
}

// 页面加载时获取数据
onMounted(() => {
  fetchPositionDetail()
})
</script>

<template>
  <div class="min-h-screen bg-[#140222] text-white">
    <!-- 头部导航 -->
    <div class="sticky top-0 z-50 bg-[#1f2842] border-b border-[#00ffff]/20">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <Header
          :breadcrumbs="breadcrumbs"
          :show-scope="false"
          :show-province="false"
          :show-time="false"
        />
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="max-w-7xl mx-auto px-4 py-6">
      <div class="flex items-center justify-center min-h-[400px]">
        <div class="text-center">
          <div
            class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#00ffff] mx-auto mb-4"
          ></div>
          <p class="text-[#00ffff] text-lg">正在加载职位详情...</p>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="max-w-7xl mx-auto px-4 py-6">
      <div class="bg-red-500/10 border border-red-500/30 rounded-lg p-6 text-center">
        <Icon name="icon-error" size="48" class="text-red-400 mx-auto mb-4" />
        <h2 class="text-xl font-semibold text-red-400 mb-2">加载失败</h2>
        <p class="text-gray-300 mb-4">{{ error }}</p>
        <button
          class="px-6 py-2 bg-[#00ffff]/20 border border-[#00ffff]/40 rounded-lg text-[#00ffff] hover:bg-[#00ffff]/30 transition-colors"
          @click="fetchPositionDetail"
        >
          重新加载
        </button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div v-else class="max-w-7xl mx-auto px-4 py-6">
      <!-- 职位基本信息卡片 -->
      <div
        class="bg-gradient-to-r from-[#00ffff]/10 to-[#00ffff]/5 rounded-lg p-6 mb-6 border border-[#00ffff]/20"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <h1 class="text-2xl font-bold text-[#00ffff] mb-2">{{ positionDetail.name }}</h1>
            <div class="flex items-center gap-4 text-sm text-gray-300">
              <span class="flex items-center gap-1">
                <Icon name="icon-company" size="16" />
                {{ positionDetail.company }}
              </span>
              <span class="flex items-center gap-1">
                <Icon name="icon-location" size="16" />
                {{ positionDetail.workLocation }}
              </span>
              <span class="flex items-center gap-1">
                <Icon name="icon-time" size="16" />
                {{ positionDetail.publishDate }}
              </span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="px-4 py-2 bg-[#00ffff]/20 border border-[#00ffff]/40 rounded-md text-[#00ffff] hover:bg-[#00ffff]/30 transition-colors"
              @click="handleFavorite"
            >
              <Icon name="icon-heart" size="16" class="mr-1" />
              收藏
            </button>
            <button
              class="px-4 py-2 bg-green-500/20 border border-green-500/40 rounded-md text-green-400 hover:bg-green-500/30 transition-colors"
              @click="handleApply"
            >
              <Icon name="icon-apply" size="16" class="mr-1" />
              立即申请
            </button>
          </div>
        </div>

        <!-- 职位关键信息 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-[#00ffff]/5 rounded-lg p-3">
            <div class="text-sm text-gray-400">薪资范围</div>
            <div class="text-lg font-semibold text-[#00ffff]">{{ positionDetail.salaryRange }}</div>
          </div>
          <div class="bg-[#00ffff]/5 rounded-lg p-3">
            <div class="text-sm text-gray-400">学历要求</div>
            <div class="text-lg font-semibold text-white">{{ positionDetail.education }}</div>
          </div>
          <div class="bg-[#00ffff]/5 rounded-lg p-3">
            <div class="text-sm text-gray-400">工作经验</div>
            <div class="text-lg font-semibold text-white">{{ positionDetail.workYear }}</div>
          </div>
          <div class="bg-[#00ffff]/5 rounded-lg p-3">
            <div class="text-sm text-gray-400">招聘人数</div>
            <div class="text-lg font-semibold text-white">{{ positionDetail.recruitCount }}人</div>
          </div>
        </div>
      </div>

      <!-- 详细信息区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧主要内容 -->
        <div class="lg:col-span-2 space-y-6">
          <!-- 职位描述 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-description" size="20" class="mr-2" />
              职位描述
            </h2>
            <p class="text-gray-300 leading-relaxed">{{ positionDetail.description }}</p>
          </div>

          <!-- 职位要求 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-requirements" size="20" class="mr-2" />
              职位要求
            </h2>
            <ul class="space-y-2">
              <li
                v-for="(requirement, index) in positionDetail.requirements"
                :key="index"
                class="flex items-start gap-2 text-gray-300"
              >
                <Icon name="icon-check" size="16" class="text-[#00ffff] mt-1 flex-shrink-0" />
                {{ requirement }}
              </li>
            </ul>
          </div>

          <!-- 工作职责 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-responsibilities" size="20" class="mr-2" />
              工作职责
            </h2>
            <ul class="space-y-2">
              <li
                v-for="(responsibility, index) in positionDetail.responsibilities"
                :key="index"
                class="flex items-start gap-2 text-gray-300"
              >
                <Icon name="icon-arrow-right" size="16" class="text-[#00ffff] mt-1 flex-shrink-0" />
                {{ responsibility }}
              </li>
            </ul>
          </div>

          <!-- 员工福利 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-benefits" size="20" class="mr-2" />
              员工福利
            </h2>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(benefit, index) in positionDetail.benefits"
                :key="index"
                class="px-3 py-1 bg-[#00ffff]/10 border border-[#00ffff]/30 rounded-full text-sm text-[#00ffff]"
              >
                {{ benefit }}
              </span>
            </div>
          </div>
        </div>

        <!-- 右侧信息栏 -->
        <div class="space-y-6">
          <!-- 公司信息 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-company" size="20" class="mr-2" />
              公司信息
            </h2>
            <div class="space-y-3">
              <div>
                <span class="text-sm text-gray-400">公司名称：</span>
                <span class="text-white">{{ companyInfo.name }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">企业类型：</span>
                <span class="text-white">{{ companyInfo.type }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">企业规模：</span>
                <span class="text-white">{{ companyInfo.size }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">企业性质：</span>
                <span class="text-white">{{ companyInfo.nature }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">公司地址：</span>
                <span class="text-white">{{ companyInfo.address }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">成立时间：</span>
                <span class="text-white">{{ companyInfo.establishedYear }}年</span>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-[#00ffff]/20">
              <h3 class="text-sm font-semibold text-[#00ffff] mb-2">公司简介</h3>
              <p class="text-sm text-gray-300">{{ companyInfo.introduction }}</p>
            </div>
          </div>

          <!-- 行业信息 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-industry" size="20" class="mr-2" />
              行业信息
            </h2>
            <div class="space-y-3">
              <div>
                <span class="text-sm text-gray-400">一级行业：</span>
                <span class="text-white">{{ industryInfo.level1 }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">二级行业：</span>
                <span class="text-white">{{ industryInfo.level2 }}</span>
              </div>
              <div>
                <span class="text-sm text-gray-400">三级行业：</span>
                <span class="text-white">{{ industryInfo.level3 }}</span>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-[#00ffff]/20">
              <h3 class="text-sm font-semibold text-[#00ffff] mb-2">行业趋势</h3>
              <ul class="space-y-1">
                <li
                  v-for="(trend, index) in industryInfo.trends"
                  :key="index"
                  class="text-sm text-gray-300 flex items-center gap-1"
                >
                  <Icon name="icon-trend" size="12" class="text-[#00ffff]" />
                  {{ trend }}
                </li>
              </ul>
            </div>
          </div>

          <!-- 职业信息 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-career" size="20" class="mr-2" />
              职业信息
            </h2>
            <div class="space-y-3">
              <div>
                <span class="text-sm text-gray-400">职业分类：</span>
                <span class="text-white"
                  >{{ careerInfo.level1 }} > {{ careerInfo.level2 }} > {{ careerInfo.level3 }}</span
                >
              </div>
              <div>
                <span class="text-sm text-gray-400">薪资范围：</span>
                <span class="text-white"
                  >{{ careerInfo.salaryRange.min }}K - {{ careerInfo.salaryRange.max }}K</span
                >
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-[#00ffff]/20">
              <h3 class="text-sm font-semibold text-[#00ffff] mb-2">相关专业</h3>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="(major, index) in careerInfo.relatedMajors"
                  :key="index"
                  class="px-2 py-1 bg-[#00ffff]/10 border border-[#00ffff]/30 rounded text-xs text-[#00ffff]"
                >
                  {{ major }}
                </span>
              </div>
            </div>
          </div>

          <!-- 其他信息 -->
          <div class="bg-[#1f2842] rounded-lg p-6 border border-[#00ffff]/10">
            <h2 class="text-xl font-semibold text-[#00ffff] mb-4 flex items-center">
              <Icon name="icon-info" size="20" class="mr-2" />
              其他信息
            </h2>
            <div class="space-y-4">
              <div>
                <h3 class="text-sm font-semibold text-[#00ffff] mb-2">工作环境</h3>
                <p class="text-sm text-gray-300">{{ otherInfo.workEnvironment }}</p>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-[#00ffff] mb-2">团队规模</h3>
                <p class="text-sm text-gray-300">{{ otherInfo.teamSize }}</p>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-[#00ffff] mb-2">学习机会</h3>
                <ul class="space-y-1">
                  <li
                    v-for="(opportunity, index) in otherInfo.learningOpportunities"
                    :key="index"
                    class="text-sm text-gray-300 flex items-center gap-1"
                  >
                    <Icon name="icon-learning" size="12" class="text-[#00ffff]" />
                    {{ opportunity }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作按钮 -->
      <div class="mt-8 flex justify-center gap-4">
        <button
          class="px-6 py-3 bg-[#00ffff]/20 border border-[#00ffff]/40 rounded-lg text-[#00ffff] hover:bg-[#00ffff]/30 transition-colors flex items-center gap-2"
          @click="handleBack"
        >
          <Icon name="icon-arrow-left" size="16" />
          返回列表
        </button>
        <button
          class="px-6 py-3 bg-green-500/20 border border-green-500/40 rounded-lg text-green-400 hover:bg-green-500/30 transition-colors flex items-center gap-2"
          @click="handleApply"
        >
          <Icon name="icon-apply" size="16" />
          立即申请
        </button>
        <button
          class="px-6 py-3 bg-blue-500/20 border border-blue-500/40 rounded-lg text-blue-400 hover:bg-blue-500/30 transition-colors flex items-center gap-2"
          @click="handleShare"
        >
          <Icon name="icon-share" size="16" />
          分享职位
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 255, 0.6);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 255, 255, 0.8);
}

/* 渐变背景动画 */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}

/* 卡片悬停效果 */
.bg-\[#1f2842\] {
  transition: all 0.3s ease;
}

.bg-\[#1f2842\]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 255, 0.1);
}

/* 按钮悬停效果 */
button {
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 255, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }

  .md\:grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }

  .lg\:grid-cols-3 {
    grid-template-columns: 1fr;
  }

  .lg\:col-span-2 {
    grid-column: span 1;
  }
}
</style>
