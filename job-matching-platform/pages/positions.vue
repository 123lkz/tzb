<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import Loading from "~/components/Common/Loading.vue"
import { fetchPositions } from "~/utils/api"
import { mockPositions, industryList as mockIndustryList, provinceList as mockProvinceList, educationOptions as mockEducationOptions, experienceOptions as mockExperienceOptions, salaryRangeOptions } from "~/utils/mockData"

const breadcrumbs = [{label:"首页",path:"/"},{label:"岗位信息",path:"/positions"}]

const keyword = ref("")
const industry = ref("")
const province = ref("")
const education = ref("")
const experience = ref("")
const salaryRange = ref("")
const sortBy = ref("")
const page = ref(1)
const pageSize = 12
const data = ref<any>({ items: mockPositions.slice(0, pageSize), total: mockPositions.length, page: 1, pageSize, totalPages: Math.ceil(mockPositions.length / pageSize) })
const loading = ref(false)

const sortOptions = [
  { label: "默认排序", value: "" },
  { label: "薪资从高到低", value: "salary_desc" },
  { label: "薪资从低到高", value: "salary_asc" },
  { label: "发布时间最新", value: "date_desc" },
  { label: "招聘人数最多", value: "recruit_desc" },
]

const filterParams = computed(() => {
  const params: any = { page: page.value, pageSize }
  if (keyword.value) params.keyword = keyword.value
  if (industry.value) params.industry = industry.value
  if (province.value) params.province = province.value
  if (education.value) params.education = education.value
  if (experience.value) params.experience = experience.value
  if (sortBy.value) params.sortBy = sortBy.value
  const sr = salaryRangeOptions.find(o => o.label === salaryRange.value)
  if (sr) { params.salaryMin = sr.value[0]; params.salaryMax = sr.value[1] }
  return params
})

function loadData() {
  loading.value = true
  fetchPositions(filterParams.value).then(result => {
    data.value = result
    loading.value = false
  })
}

watch([keyword, industry, province, education, experience, salaryRange, sortBy], () => { page.value = 1 })
watch(filterParams, () => { loadData() }, { deep: true })

// ===== 过滤选项（从 jobs_clean 数据动态生成）=====
const industryList = computed(() => {
  const items = data.value?.allItems
  if (items?.length) return [...new Set(items.map(p => p.industry).filter(Boolean))].sort()
  return mockIndustryList
})
const provinceList = computed(() => {
  const items = data.value?.allItems
  if (items?.length) return [...new Set(items.map(p => p.province).filter(Boolean))].sort()
  return mockProvinceList
})
const educationOptions = computed(() => {
  const items = data.value?.allItems
  if (items?.length) return [...new Set(items.map(p => p.education).filter(Boolean))].sort()
  return mockEducationOptions
})
const experienceOptions = computed(() => {
  const items = data.value?.allItems
  if (items?.length) return [...new Set(items.map(p => p.experience).filter(Boolean))].sort()
  return mockExperienceOptions
})

const stats = computed(() => {
  const allItems = data.value?.allItems || data.value?.items || []
  const total = data.value?.total || 0
  const totalRecruit = allItems.reduce((sum, p) => sum + (p.recruitNumber || 0), 0)
  const avgSalary = allItems.length > 0 ? Math.round(allItems.reduce((sum, p) => sum + ((p.salaryMin||0)+(p.salaryMax||0))/2, 0) / allItems.length) : 0
  return { total, totalRecruit, avgSalary }
})

const totalPages = computed(() => data.value?.totalPages || 0)
const totalItems = computed(() => data.value?.total || 0)

const pageRange = computed(() => {
  const cur = page.value; const tot = totalPages.value
  if (tot <= 5) return Array.from({length: tot}, (_,i) => i+1)
  if (cur <= 3) return [1,2,3,4,5]
  if (cur >= tot-2) return [tot-4, tot-3, tot-2, tot-1, tot]
  return [cur-2, cur-1, cur, cur+1, cur+2]
})

function goToPage(p) { if (p>=1 && p<=totalPages.value) page.value = p }
function resetFilters() {
  keyword.value=""; industry.value=""; province.value=""
  education.value=""; experience.value=""; salaryRange.value=""; sortBy.value=""; page.value=1
}

onMounted(() => { loadData() })
</script>

<template>
<div class="fade-in space-y-4 pb-6">
  <Header :breadcrumbs="breadcrumbs" />

  <Card class="!p-4">
    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3 items-end">
      <div class="col-span-2 lg:col-span-2">
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">关键词</label>
        <input v-model="keyword" placeholder="岗位/公司/技能.." class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] placeholder:text-[rgba(176,196,222,0.3)] outline-none focus:border-[#00ffff]"/>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">行业</label>
        <select v-model="industry" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option value="">全部行业</option>
          <option v-for="item in industryList" :key="item" :value="item">{{ item }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">地点</label>
        <select v-model="province" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option value="">全部地点</option>
          <option v-for="item in provinceList" :key="item" :value="item">{{ item }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">学単</label>
        <select v-model="education" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option value="">学历不限</option>
          <option v-for="item in educationOptions" :key="item" :value="item">{{ item }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">工作经验</label>
        <select v-model="experience" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option value="">经验不限</option>
          <option v-for="item in experienceOptions" :key="item" :value="item">{{ item }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">薪资 </label>
        <select v-model="salaryRange" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option value="">薪资不限</option>
          <option v-for="item in salaryRangeOptions" :key="item.label" :value="item.label">{{ item.label }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">排序</label>
        <select v-model="sortBy" class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-2.5 py-1.5 text-xs text-[#00eaff] outline-none focus:border-[#00ffff] appearance-none cursor-pointer">
          <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] text-transparent mb-1">重群</label>
        <button @click="resetFilters" class="w-full px-2.5 py-1.5 text-xs rounded bg-[rgba(0,255,255,0.1)] text-[#00ffff] border border-[rgba(0,255,255,0.2)] hover:bg-[rgba(0,255,255,0.2)] transition-all cursor-pointer">重置筛选</button>
      </div>
    </div>
  </Card>

  <div class="grid grid-cols-3 gap-3">
    <div class="bg-gradient-to-r from-[rgba(0,255,255,0.06)] to-[rgba(0,200,255,0.1)] rounded-lg border border-[rgba(0,255,255,0.15)] p-3">
      <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">筛选岗位数量</div>
      <div class="text-xl font-bold text-[#00ffff]">{{ stats.total }}</div>
    </div>
    <div class="bg-gradient-to-r from-[rgba(0,255,255,0.06)] to-[rgba(0,200,255,0.1)] rounded-lg border border-[rgba(0,255,255,0.15)] p-3">
      <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">招聘需求总人数</div>
      <div class="text-xl font-bold text-[#ffd93d]">{{ stats.totalRecruit }}</div>
    </div>
    <div class="bg-gradient-to-r from-[rgba(0,255,255,0.06)] to-[rgba(0,200,255,0.1)] rounded-lg border border-[rgba(0,255,255,0.15)] p-3">
      <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">平均薪资 </div>
      <div class="text-xl font-bold text-[#6bcb77]">{{ stats.avgSalary }}<span class="text-xs ml-0.5">K</span></div>
    </div>
  </div>

  <Loading v-if="loading" />
  <template v-else>
    <div v-if="data.items.length === 0" class="flex-center py-16">
      <p class="text-sm text-[rgba(176,196,222,0.3)]">暂无符吆用想的岃佝</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      <NuxtLink v-for="pos in data.items" :key="pos.id"
        :to="{path:'/positions/'+pos.id}"
        class="card card-hover no-underline block !p-4 cursor-pointer group">
        <div class="flex items-start justify-between mb-2">
          <div class="min-w-0 flex-1 mr-2">
            <h3 class="text-sm font-semibold text-[#00ffff] truncate group-hover:text-white transition-colors">{{ pos.name }}</h3>
            <p class="text-xs text-[rgba(176,196,222,0.5)] truncate mt-0.5">{{ pos.company }} ·{{ pos.province }} {{ pos.city }}</p>
          </div>
          <div class="text-right flex-shrink-0">
            <span class="text-[#ffd93d] text-sm font-bold">{{ pos.salaryMin }}-{{ pos.salaryMax }}<span class="text-[10px]">K</span></span>
          </div>
        </div>
        <p class="text-xs text-[rgba(176,196,222,0.5)] line-clamp-2 mb-2 leading-relaxed">{{ pos.description }}</p>
        <div class="flex flex-wrap gap-1.5 mb-2">
          <span class="px-1.5 py-0.5 text-[10px] rounded bg-[rgba(0,255,255,0.08)] text-[rgba(0,255,255,0.6)]">{{ pos.education }}</span>
          <span class="px-1.5 py-0.5 text-[10px] rounded bg-[rgba(255,107,107,0.08)] text-[rgba(255,107,107,0.6)]">{{ pos.experience }}</span>
          <span v-for="tag in pos.tags.slice(0,2)" :key="tag" class="px-1.5 py-0.5 text-[10px] rounded bg-[rgba(255,217,61,0.08)] text-[rgba(255,217,61,0.6)]">{{ tag }}</span>
        </div>
        <div class="flex flex-wrap gap-1 mb-2">
          <span v-for="s in pos.requiredSkills.slice(0,3)" :key="s" class="px-1 py-0.5 text-[9px] rounded bg-[rgba(255,107,107,0.06)] text-[rgba(255,107,107,0.5)]">{{ s }}</span>
          <span v-if="pos.requiredSkills.length > 3" class="text-[9px] text-[rgba(176,196,222,0.3)] self-center">+{{ pos.requiredSkills.length-3 }}</span>
        </div>
        <div class="flex justify-between items-center pt-1 border-t border-[rgba(0,255,255,0.06)]">
          <span class="text-[9px] text-[rgba(176,196,222,0.3)]">{{ pos.publishDate }}</span>
          <span class="text-[9px] text-[rgba(176,196,222,0.3)] bg-[rgba(0,255,255,0.04)] px-1.5 py-0.5 rounded">{{ pos.platform }}</span>
        </div>
      </NuxtLink>
    </div>

    <div v-if="totalPages > 1" class="flex items-center justify-between pt-2">
      <span class="text-xs text-[rgba(176,196,222,0.4)]">共 {{ totalItems }} 条，第{{ page }}/{{ totalPages }} 页</span>
      <div class="flex items-center gap-1">
        <button @click="goToPage(page - 1)" :disabled="page <= 1"
          class="px-2 py-1 text-xs rounded border border-[rgba(0,255,255,0.2)] text-[rgba(0,255,255,0.6)] hover:bg-[rgba(0,255,255,0.1)] disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer">上一页</button>
        <button v-for="p in pageRange" :key="p" @click="goToPage(p)"
          class="px-2.5 py-1 text-xs rounded transition-all cursor-pointer"
          :class="p === page ? 'bg-[rgba(0,255,255,0.2)] text-[#00ffff] border border-[rgba(0,255,255,0.3)]' : 'border border-[rgba(0,255,255,0.15)] text-[rgba(176,196,222,0.5)] hover:bg-[rgba(0,255,255,0.08)]'">{{ p }}</button>
        <button @click="goToPage(page + 1)" :disabled="page >= totalPages"
          class="px-2 py-1 text-xs rounded border border-[rgba(0,255,255,0.2)] text-[rgba(0,255,255,0.6)] hover:bg-[rgba(0,255,255,0.1)] disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer">下一页</button>
      </div>
    </div>
  </template>
</div>
</template>

<style scoped>
select option { background: #0a1628; color: #00eaff; }
</style>
