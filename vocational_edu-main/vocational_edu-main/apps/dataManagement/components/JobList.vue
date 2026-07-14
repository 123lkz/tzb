<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import jobListData from '~/data/jobListData.json'

interface JobItem {
  job_id: string
  city: string
  company: string
  title: string
  salary: string
  education: string
  experience: string
  company_size: string
  company_type: string
  job_tags: string[]
  recruit_count: number
  publish_time: string
  district: string
  industry_name: string
}

const jobList = ref<JobItem[]>(jobListData.jobList)
const searchKeyword = ref('')
const selectedCity = ref('')
const selectedIndustry = ref('')
const selectedEducation = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const sortOption = ref('')
const sortOptions = [
  { label: '默认排序', value: '' },
  { label: '工资从高到低', value: 'salary_desc' },
  { label: '工资从低到高', value: 'salary_asc' },
  { label: '招聘总人数从高到低', value: 'recruit_desc' },
  { label: '招聘总人数从低到高', value: 'recruit_asc' },
]

// 获取所有城市和行业选项
const cities = computed(() => [...new Set(jobList.value.map(job => job.city))])
const industries = computed(() => [...new Set(jobList.value.map(job => job.industry_name))])
const educations = computed(() => [...new Set(jobList.value.map(job => job.education))])

// 筛选后的数据
const filteredJobList = computed(() => {
  let filtered = jobList.value

  // 关键词搜索
  if (searchKeyword.value) {
    filtered = filtered.filter(
      job =>
        job.title.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
        job.company.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
        job.job_tags.some(tag => tag.toLowerCase().includes(searchKeyword.value.toLowerCase()))
    )
  }

  // 城市筛选
  if (selectedCity.value) {
    filtered = filtered.filter(job => job.city === selectedCity.value)
  }

  // 行业筛选
  if (selectedIndustry.value) {
    filtered = filtered.filter(job => job.industry_name === selectedIndustry.value)
  }

  // 学历筛选
  if (selectedEducation.value) {
    filtered = filtered.filter(job => job.education === selectedEducation.value)
  }

  // 排序
  if (sortOption.value === 'salary_desc') {
    filtered = [...filtered].sort((a, b) => (b.salary_max || 0) - (a.salary_max || 0))
  } else if (sortOption.value === 'salary_asc') {
    filtered = [...filtered].sort((a, b) => (a.salary_min || 0) - (b.salary_min || 0))
  } else if (sortOption.value === 'recruit_desc') {
    filtered = [...filtered].sort((a, b) => (b.recruit_count || 0) - (a.recruit_count || 0))
  } else if (sortOption.value === 'recruit_asc') {
    filtered = [...filtered].sort((a, b) => (a.recruit_count || 0) - (b.recruit_count || 0))
  }

  return filtered
})

// 分页数据
const paginatedJobList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredJobList.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => Math.ceil(filteredJobList.value.length / pageSize.value))

// 统计信息
const statistics = computed(() => {
  const totalJobs = filteredJobList.value.length
  const totalRecruit = filteredJobList.value.reduce((sum, job) => sum + job.recruit_count, 0)
  const avgSalary =
    totalJobs > 0
      ? filteredJobList.value.reduce((sum, job) => {
          const min = job.salary_min || 0
          const max = job.salary_max || 0
          return sum + (min + max) / 2
        }, 0) / totalJobs
      : 0

  return {
    totalJobs,
    totalRecruit,
    avgSalary: Math.round(avgSalary),
  }
})

// 重置筛选
const resetFilters = () => {
  searchKeyword.value = ''
  selectedCity.value = ''
  selectedIndustry.value = ''
  selectedEducation.value = ''
  currentPage.value = 1
}

// 跳转到岗位详情
const goToJobDetail = (jobId: string) => {
  // 这里可以跳转到岗位详情页面
  console.log('跳转到岗位详情:', jobId)
}

// 格式化标签显示
const formatTags = (tags: string[]) => {
  return tags.slice(0, 3).join('、') + (tags.length > 3 ? '...' : '')
}

const router = useRouter()

// 返回上一页
const goBack = () => {
  router.back()
}

// 模拟加载数据
const loadData = async () => {
  loading.value = true
  // 模拟异步加载
  await new Promise(resolve => setTimeout(resolve, 500))
  loading.value = false
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="p-6 bg-black w-full h-full overflow-auto">
    <!-- 页面标题 -->
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button
          @click="goBack"
          class="px-4 py-2 bg-[#25395ecc] text-cyan-300 rounded-lg hover:bg-[#00eaff20] transition-all duration-200 border border-cyan-400/30"
        >
          ← 返回
        </button>
        <div>
          <h1 class="text-2xl font-bold text-cyan-300 mb-2">岗位列表</h1>
          <p class="text-gray-400">共 {{ filteredJobList.length }} 个岗位</p>
        </div>
      </div>
    </div>

    <!-- 统计信息卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-4 border border-cyan-400/30"
      >
        <div class="text-cyan-300 text-sm mb-1">总岗位数</div>
        <div class="text-2xl font-bold text-white">{{ statistics.totalJobs }}</div>
      </div>
      <div
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-4 border border-cyan-400/30"
      >
        <div class="text-cyan-300 text-sm mb-1">招聘需求总人数</div>
        <div class="text-2xl font-bold text-white">{{ statistics.totalRecruit }}</div>
      </div>
      <div
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-4 border border-cyan-400/30"
      >
        <div class="text-cyan-300 text-sm mb-1">平均薪资</div>
        <div class="text-2xl font-bold text-white">{{ statistics.avgSalary }}K</div>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <!-- 关键词搜索 -->
        <div>
          <label class="block text-sm font-medium text-cyan-300 mb-2">关键词搜索</label>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索岗位、公司、技能标签..."
            class="w-full px-3 py-2 bg-[#25395ecc] border border-cyan-400/30 rounded-md text-white placeholder-gray-400 focus:outline-none focus:border-cyan-400"
          />
        </div>
        <!-- 城市筛选 -->
        <div>
          <label class="block text-sm font-medium text-cyan-300 mb-2">城市</label>
          <select
            v-model="selectedCity"
            class="w-full px-3 py-2 bg-[#25395ecc] border border-cyan-400/30 rounded-md text-white focus:outline-none focus:border-cyan-400"
          >
            <option value="">全部城市</option>
            <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
          </select>
        </div>
        <!-- 行业筛选 -->
        <div>
          <label class="block text-sm font-medium text-cyan-300 mb-2">行业</label>
          <select
            v-model="selectedIndustry"
            class="w-full px-3 py-2 bg-[#25395ecc] border border-cyan-400/30 rounded-md text-white focus:outline-none focus:border-cyan-400"
          >
            <option value="">全部行业</option>
            <option v-for="industry in industries" :key="industry" :value="industry">
              {{ industry }}
            </option>
          </select>
        </div>
        <!-- 学历筛选 -->
        <div>
          <label class="block text-sm font-medium text-cyan-300 mb-2">学历要求</label>
          <select
            v-model="selectedEducation"
            class="w-full px-3 py-2 bg-[#25395ecc] border border-cyan-400/30 rounded-md text-white focus:outline-none focus:border-cyan-400"
          >
            <option value="">全部学历</option>
            <option v-for="education in educations" :key="education" :value="education">
              {{ education }}
            </option>
          </select>
        </div>
        <!-- 排序 -->
        <div>
          <label class="block text-sm font-medium text-cyan-300 mb-2">排序</label>
          <select
            v-model="sortOption"
            class="w-full px-3 py-2 bg-[#25395ecc] border border-cyan-400/30 rounded-md text-white focus:outline-none focus:border-cyan-400"
          >
            <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <!-- 重置按钮 -->
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="w-full px-4 py-2 bg-gradient-to-r from-cyan-400 to-blue-500 text-white rounded-md hover:from-cyan-500 hover:to-blue-600 transition-all duration-200"
          >
            重置筛选
          </button>
        </div>
      </div>
    </div>

    <!-- 岗位列表 -->
    <div class="space-y-4">
      <!-- 加载状态 -->
      <div
        v-if="loading"
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-8 text-center"
      >
        <div class="text-cyan-300 text-lg mb-2">加载中...</div>
        <div
          class="animate-spin w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full mx-auto"
        ></div>
      </div>

      <div
        v-else-if="paginatedJobList.length === 0"
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-8 text-center"
      >
        <div class="text-cyan-300 text-lg mb-2">暂无符合条件的岗位</div>
        <div class="text-gray-400 text-sm">请尝试调整筛选条件或搜索关键词</div>
      </div>

      <div
        v-else
        v-for="job in paginatedJobList"
        :key="job.job_id"
        class="bg-gradient-to-r from-[#182848cc] to-[#1a2980cc] rounded-lg p-4 hover:from-[#00eaff20] hover:to-[#00eaff10] transition-all duration-200 cursor-pointer border border-transparent hover:border-cyan-400/30"
        @click="goToJobDetail(job.job_id)"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-cyan-300 mb-1">{{ job.title }}</h3>
            <p class="text-gray-400 text-sm">{{ job.company }}</p>
          </div>
          <div class="text-right">
            <div class="text-xl font-bold text-yellow-400">{{ job.salary }}</div>
            <div class="text-sm text-gray-400">{{ job.recruit_count }}人</div>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span class="text-gray-400">地点：</span>
            <span class="text-white">{{ job.city }} {{ job.district }}</span>
          </div>
          <div>
            <span class="text-gray-400">行业：</span>
            <span class="text-white">{{ job.industry_name }}</span>
          </div>
          <div>
            <span class="text-gray-400">学历：</span>
            <span class="text-white">{{ job.education }}</span>
          </div>
          <div>
            <span class="text-gray-400">经验：</span>
            <span class="text-white">{{ job.experience }}</span>
          </div>
        </div>

        <div class="mt-3">
          <span class="text-gray-400 text-sm">技能标签：</span>
          <span class="text-cyan-300 text-sm">{{ formatTags(job.job_tags) }}</span>
        </div>

        <div class="mt-3 flex justify-between items-center text-xs text-gray-400">
          <span>{{ job.company_size }} | {{ job.company_type }}</span>
          <span>发布时间：{{ job.publish_time }}</span>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="mt-6 flex justify-center">
      <div class="flex space-x-2">
        <button
          @click="currentPage = Math.max(1, currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-2 bg-[#25395ecc] text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#00eaff20] transition-all duration-200"
        >
          上一页
        </button>

        <span class="px-3 py-2 text-cyan-300">
          第 {{ currentPage }} 页，共 {{ totalPages }} 页
        </span>

        <button
          @click="currentPage = Math.min(totalPages, currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-2 bg-[#25395ecc] text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#00eaff20] transition-all duration-200"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
