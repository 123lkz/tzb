<template>
  <div class="fade-in space-y-4 pb-6">
    <Header title="数据概览" />

    <!-- ===== 核心指标卡 8张 ===== -->
    <div class="grid grid-cols-4 gap-3">
      <StatCard v-for="s in statCards" :key="s.label"
        :label="s.label" :value="s.value" :unit="s.unit"
        :color="s.color" :trend="s.trend" />
    </div>

    <!-- ===== 图表区域 R1: 行业分布 + 学历要求 ===== -->
    <div class="grid grid-cols-2 gap-4">
      <Card><div class="h-64"><BarChart :data="industryStats" title="行业分布" /></div></Card>
      <Card><div class="h-64"><DoughnutChart :data="educationStats" title="学历要求" /></div></Card>
    </div>

    <!-- ===== 图表区域 R2: 经验要求 + 薪资分布 ===== -->
    <div class="grid grid-cols-2 gap-4">
      <Card><div class="h-52"><HorizontalBarChart :data="experienceStats" title="经验要求" /></div></Card>
      <Card><div class="h-52"><LineChart :data="salaryStats" title="薪资分布" /></div></Card>
    </div>

    <!-- ===== 图表区域 R3: 省份需求 + 公司排行 ===== -->
    <div class="grid grid-cols-2 gap-4">
      <Card><div class="h-56"><BarChart :data="provinceStats" title="省份需求" color="#ffd93d" /></div></Card>
      <Card>
        <template #default>
          <div class="flex items-center justify-between px-3 pt-2 pb-1">
            <span class="text-xs text-[rgba(176,196,222,0.5)]">公司招聘排行</span>
          </div>
          <RankList :data="companyRank" />
        </template>
      </Card>
    </div>

    <!-- ===== 热门技能标签 ===== -->
    <Card>
      <div class="px-2 py-1">
        <span class="text-xs text-[rgba(176,196,222,0.5)] block mb-3">热门技能</span>
        <div class="flex flex-wrap gap-2">
          <span v-for="s in skillCloud" :key="s.name"
            class="px-2.5 py-1 rounded transition-all duration-200 cursor-default hover:scale-110"
            :style="{ backgroundColor: getSkillBg(s.value), color: '#fff', fontSize: getSkillSize(s.value) + 'px' }">
            {{ s.name }}
          </span>
        </div>
      </div>
    </Card>

    <!-- ===== 最新岗位 ===== -->
    <div>
      <span class="text-xs text-[rgba(176,196,222,0.5)] block mb-2">最新岗位</span>
      <div class="grid grid-cols-4 gap-3">
        <NuxtLink v-for="pos in latestPositions" :key="pos.id"
          :to="'/positions/' + pos.id"
          class="bg-[rgba(0,255,255,0.04)] border border-[rgba(0,255,255,0.1)] rounded-lg p-3 no-underline block hover:bg-[rgba(0,255,255,0.08)] transition-all">
          <div class="text-[#00ffff] text-sm font-medium truncate">{{ pos.name }}</div>
          <div class="text-xs text-[rgba(176,196,222,0.4)] mt-1">{{ pos.company }} / {{ pos.province }}</div>
          <div class="text-xs text-[rgba(176,196,222,0.5)] mt-1">{{ pos.salaryMin }}-{{ pos.salaryMax }}K / {{ pos.education }}</div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import Card from '~/components/Common/Card.vue'
import StatCard from '~/components/Echart/StatCard.vue'
import BarChart from '~/components/Echart/BarChart.vue'
import DoughnutChart from '~/components/Echart/DoughnutChart.vue'
import HorizontalBarChart from '~/components/Echart/HorizontalBarChart.vue'
import LineChart from '~/components/Echart/LineChart.vue'
import RankList from '~/components/Echart/RankList.vue'
import { mockPositions } from '~/utils/mockData'
import { fetchPositions } from '~/utils/api'
import { ref, computed, onMounted } from 'vue'
import type { PositionInfo } from '~/types'
// ===== 核心指标计算（SSR用mock，客户端onMounted刷新）=====
const positionsData = ref<PositionInfo[]>(mockPositions)
const totalPositions = computed(() => positionsData.value.length)
const totalCompanies = computed(() => [...new Set(positionsData.value.map(p => p.company))].length)
const totalIndustries = computed(() => [...new Set(positionsData.value.map(p => p.industry))].length)
const allSkills = computed(() => [...new Set(positionsData.value.flatMap(p => [...p.requiredSkills, ...(p.optionalSkills||[])]))])
const totalSkills = computed(() => allSkills.value.length)
const avgSalary = computed(() => positionsData.value.length ? Math.round(positionsData.value.reduce((s, p) => s + (p.salaryMin + p.salaryMax) / 2, 0) / positionsData.value.length) : 0)
const maxSalary = computed(() => positionsData.value.length ? Math.max(...positionsData.value.map(p => p.salaryMax)) : 0)
const totalRecruit = computed(() => positionsData.value.reduce((s, p) => s + (p.recruitNumber||0), 0))
const topSkill = computed(() => allSkills.value.slice(0, 5).join(', '))



// ===== 图表数据（从positionsData动态计算）=====
const industryStats = computed(() => {
  const counts = {}
  for (const p of positionsData.value) { const k = p.industry || '其他'; counts[k] = (counts[k]||0)+1 }
  return Object.entries(counts).map(([n,v])=>({name:n,value:v})).sort((a,b)=>b.value-a.value)
})
const educationStats = computed(() => {
  const counts = {}
  for (const p of positionsData.value) { const k = p.education || '学历不限'; counts[k] = (counts[k]||0)+1 }
  return Object.entries(counts).map(([n,v])=>({name:n,value:v})).sort((a,b)=>b.value-a.value)
})
const experienceStats = computed(() => {
  const counts = {}
  for (const p of positionsData.value) { const k = p.experience || '经验不限'; counts[k] = (counts[k]||0)+1 }
  return Object.entries(counts).map(([n,v])=>({name:n,value:v})).sort((a,b)=>b.value-a.value)
})
const salaryStats = computed(() => {
  const ranges = [{range:'10K以下',min:0,max:10},{range:'10-20K',min:10,max:20},{range:'20-35K',min:20,max:35},{range:'35-50K',min:35,max:50},{range:'50K以上',min:50,max:999}]
  return ranges.map(r=>({range:r.range,count:positionsData.value.filter(p=>(p.salaryMin||0)>=r.min&&(p.salaryMax||999)<=r.max).length}))
})
const provinceStats = computed(() => {
  const counts = {}
  for (const p of positionsData.value) { const k = p.province || '未知'; counts[k] = (counts[k]||0)+1 }
  return Object.entries(counts).map(([n,v])=>({name:n,value:v})).sort((a,b)=>b.value-a.value)
})
const companyRank = computed(() => {
  const comps = {}
  for (const p of positionsData.value) {
    if (!comps[p.company]) comps[p.company] = { positions:0, totalSalary:0 }
    comps[p.company].positions++; comps[p.company].totalSalary += ((p.salaryMin||0)+(p.salaryMax||0))/2
  }
  return Object.entries(comps).map(([n,d])=>({name:n,positions:d.positions,avgSalary:Math.round(d.totalSalary/d.positions)})).sort((a,b)=>b.positions-a.positions).slice(0,10)
})
const skillCloud = computed(() => {
  const counts = {}
  for (const p of positionsData.value) { for (const sk of (p.requiredSkills||[])) { counts[sk] = (counts[sk]||0)+1 } }
  return Object.entries(counts).map(([n,v])=>({name:n,value:Math.min(v*10,100)})).sort((a,b)=>b.value-a.value).slice(0,30)
})


const statCards = computed(() => [
  { label: '岗位总数', value: totalPositions.value, unit: '个', color: '#00ffff', trend: 0 },
  { label: '招聘公司', value: totalCompanies.value, unit: '家', color: '#6bcb77', trend: 0 },
  { label: '覆盖行业', value: totalIndustries.value, unit: '类', color: '#ffd93d', trend: 0 },
  { label: '技能总数', value: totalSkills.value, unit: '项', color: '#ff6b6b', trend: 0 },
  { label: '平均薪资', value: avgSalary.value, unit: 'K', color: '#845ef7', trend: 0 },
  { label: '最高薪资', value: maxSalary.value, unit: 'K', color: '#ff922b', trend: 0 },
  { label: '招聘人数', value: totalRecruit.value, unit: '人', color: '#339af0', trend: 0 },
  { label: '热门技能', value: topSkill.value, unit: '', color: '#f06595' }
])

// ===== 最新岗位（按发布日期排序）=====
const latestPositions = computed<PositionInfo[]>(() => [...positionsData.value]
  .sort((a, b) => b.publishDate.localeCompare(a.publishDate))
  .slice(0, 4))

if (import.meta.client) {
  fetchPositions({ pageSize: 100 }).then(result => {
    if (result?.items && result.items.length > 0) {
      positionsData.value = result.items
    }
  })
}

// ===== 技能标签样式辅助 =====
const skillColors = ['rgba(0,255,255,0.6)','rgba(255,107,107,0.6)','rgba(255,217,61,0.6)','rgba(107,203,119,0.6)','rgba(132,94,247,0.6)','rgba(255,146,43,0.6)']
function getSkillBg(value: number): string {
  return skillColors[Math.min(Math.floor(value / 15), skillColors.length - 1)]
}
function getSkillSize(value: number): number {
  return 11 + Math.floor(value / 20)
}
</script>
