<template>
  <div class="fade-in space-y-4 pb-6">
    <Header :breadcrumbs="breadcrumbs" />

    <div v-if="loading" class="flex-center py-20">
      <Loading text="加载洞察数据..." />
    </div>

    <template v-else>
      <div class="grid grid-cols-5 gap-3">
        <Card hover>
          <div class="text-center">
            <div class="text-xs text-[rgba(176,196,222,0.5)] mb-1">岗位画像</div>
            <div class="text-2xl font-bold text-[#00ffff]">{{ overview?.totalPositions ?? '-' }}</div>
          </div>
        </Card>
        <Card hover>
          <div class="text-center">
            <div class="text-xs text-[rgba(176,196,222,0.5)] mb-1">技能总数</div>
            <div class="text-2xl font-bold text-[#6bcb77]">{{ overview?.totalSkills ?? '-' }}</div>
          </div>
        </Card>
        <Card hover @click="openAuditModal" class="cursor-pointer">
          <div class="text-center">
            <div class="text-xs text-[rgba(176,196,222,0.5)] mb-1">待审核</div>
            <div class="text-2xl font-bold text-[#ffd93d]">{{ overview?.pendingAudit ?? '-' }}</div>
          </div>
        </Card>
        <Card hover>
          <div class="text-center">
            <div class="text-xs text-[rgba(176,196,222,0.5)] mb-1">新发现</div>
            <div class="text-2xl font-bold text-[#6bcb77]">{{ overview?.newPositionCount ?? '-' }}</div>
          </div>
        </Card>
        <Card hover>
          <div class="text-center">
            <div class="text-xs text-[rgba(176,196,222,0.5)] mb-1">质量评分</div>
            <div class="text-2xl font-bold text-[#ff6b6b]">{{ overview?.qualityScore ?? '-' }}<span class="text-sm">分</span></div>
          </div>
        </Card>
      </div>

      <div class="flex items-center gap-4 justify-end">
        <button @click="trigger" :disabled="running"
          class="px-4 py-2 bg-[rgba(0,255,255,0.15)] border border-[rgba(0,255,255,0.3)] rounded-lg text-sm text-[#00eaff] hover:bg-[rgba(0,255,255,0.25)] disabled:opacity-50 transition-all">
          {{ running ? '分析中...' : '触发新岗位分析' }}
        </button>
        <span v-if="running" class="text-xs text-[rgba(176,196,222,0.4)]">正在进行分析，请稍候...</span>
      </div>

      <div class="grid grid-cols-2 gap-4">
      <Card>
        <div class="flex items-center gap-3 mb-3">
          <span class="text-xs text-[rgba(176,196,222,0.5)]">技能趋势分析</span>
          <select v-model="selectedPosition" @change="loadTrend"
            class="bg-[rgba(0,0,0,0.3)] border border-[rgba(0,255,255,0.2)] rounded px-2 py-1 text-xs text-[rgba(176,196,222,0.8)] outline-none" style="color-scheme:dark;background:rgba(10,5,20,0.9)">
            <option v-for="p in positions" :key="p" :value="p">{{ p }}</option>
          </select>
        </div>
        <div ref="trendRef" class="h-72 w-full" style="background:rgba(0,255,255,0.03);border-radius:4px"></div>
        <div v-if="skillTrend?.skills" class="flex flex-wrap gap-3 mt-2">
          <span v-for="(d, n) in skillTrend.skills" :key="n" class="text-xs" :style="{ color: gc(d.change) }">
            {{ n }} ({{ d.pct || '' }})
          </span>
        </div>
      </Card>

      <div v-if="newPositions.length > 0">
        <div class="text-xs text-[rgba(176,196,222,0.5)] mb-2">新发现岗位 ({{ newPositions.filter(p => p.status === 'pending').length }} 个待确认)</div>
        <div class="max-h-[420px] overflow-y-auto custom-scrollbar pr-1">
          <div class="grid grid-cols-1 gap-3">
            <Card v-for="np in newPositions" :key="np.id" hover>
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-sm font-semibold text-white">{{ np.name }}</span>
                  <span v-if="np.confidence" class="text-xs px-1.5 py-0.5 rounded bg-[rgba(0,255,255,0.1)] text-[#00ffff]">
                    置信度: {{ (np.confidence * 100).toFixed(0) }}%
                  </span>
                  <span v-if="np.status === 'confirmed'" class="text-xs text-[#6bcb77]">已确认</span>
                  <span v-if="np.status === 'dismissed'" class="text-xs text-[rgba(176,196,222,0.4)]">已忽略</span>
                </div>
                <p v-if="np.description" class="text-xs text-[rgba(176,196,222,0.6)] mb-2">{{ np.description }}</p>
                <div class="flex flex-wrap gap-3 text-xs">
                  <div v-if="np.coreResponsibilities?.length">
                    <span class="text-[rgba(176,196,222,0.4)]">核心职责: </span>
                    <span class="text-[rgba(176,196,222,0.7)]">{{ np.coreResponsibilities.join('、') }}</span>
                  </div>
                  <div v-if="np.requiredSkills?.length">
                    <span class="text-[rgba(176,196,222,0.4)]">必备技能: </span>
                    <span class="text-[#6bcb77]">{{ np.requiredSkills.join('、') }}</span>
                  </div>
                  <div v-if="np.optionalSkills?.length">
                    <span class="text-[rgba(176,196,222,0.4)]">加分技能: </span>
                    <span class="text-[#ffd93d]">{{ np.optionalSkills.join('、') }}</span>
                  </div>
                  <div v-if="np.typicalApplications?.length">
                    <span class="text-[rgba(176,196,222,0.4)]">典型应用场景: </span>
                    <span class="text-[rgba(176,196,222,0.7)]">{{ np.typicalApplications.join('、') }}</span>
                  </div>
                </div>
              </div>
              <div v-if="np.status === 'pending'" class="flex gap-2 ml-3">
                <button @click="handleNP(np.id, 'confirm')"
                  class="px-3 py-1 text-xs bg-[rgba(107,203,119,0.2)] border border-[rgba(107,203,119,0.3)] rounded text-[#6bcb77] hover:bg-[rgba(107,203,119,0.3)] transition-all">
                  确认
                </button>
                <button @click="handleNP(np.id, 'dismiss')"
                  class="px-3 py-1 text-xs bg-[rgba(255,107,107,0.2)] border border-[rgba(255,107,107,0.3)] rounded text-[#ff6b6b] hover:bg-[rgba(255,107,107,0.3)] transition-all">
                  忽略
                </button>
              </div>
            </div>
          </Card>
          </div>
        </div>
      </div>
    </div>


    </template>

    <Teleport to="body">
      <div v-if="showAuditModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
        @click.self="showAuditModal = false">
        <div class="bg-[#1a0a2e] border border-[rgba(0,255,255,0.2)] rounded-lg w-[600px] max-h-[80vh] overflow-y-auto p-4">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm font-semibold text-white">待审核关系画像</span>
            <button @click="showAuditModal = false" class="text-[rgba(176,196,222,0.4)] hover:text-white text-sm">X</button>
          </div>
          <div v-if="auditLoading" class="flex-center py-10">
            <Loading text="加载待审核数据..." />
          </div>
          <div v-else-if="auditItems.length === 0" class="text-center py-10 text-xs text-[rgba(176,196,222,0.4)]">
            暂无待审核项
          </div>
          <div v-else class="space-y-2">
            <div v-for="item in auditItems" :key="item.id"
              class="flex items-center justify-between p-3 bg-[rgba(0,0,0,0.2)] rounded border border-[rgba(0,255,255,0.05)]">
              <div class="flex-1">
                <div class="text-xs text-white">{{ item.targetName || '未知' }}</div>
                <div v-if="item.sourceName" class="text-xs text-[rgba(176,196,222,0.5)] mt-0.5">关联技能: {{ item.sourceName }}</div>
                <div v-if="item.confidence" class="text-xs text-[rgba(176,196,222,0.3)] mt-0.5">
                  置信度: {{ (item.confidence * 100).toFixed(0) }}%
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="doApprove(item.id)"
                  class="px-3 py-1 text-xs bg-[rgba(107,203,119,0.2)] border border-[rgba(107,203,119,0.3)] rounded text-[#6bcb77] hover:bg-[rgba(107,203,119,0.3)] transition-all">
                  通过
                </button>
                <button @click="doSkip(item)"
                  class="px-3 py-1 text-xs bg-[rgba(255,255,255,0.1)] border border-[rgba(255,255,255,0.15)] rounded text-[rgba(176,196,222,0.4)] hover:bg-[rgba(255,255,255,0.15)] transition-all">
                  跳过
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

﻿<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import Loading from "~/components/Common/Loading.vue"
import { fetchOverview, fetchSkillTrend, fetchNewPositions, handleNewPosition, runDiscovery, fetchInsightsPositions, fetchAuditItems, approveAuditItem } from "~/utils/api"

const breadcrumbs = [{label:"首页",path:"/"},{label:"能力洞察",path:"/insights"}]
const loading = ref(true)
const overview = ref<any>(null)
const skillTrend = ref<any>(null)
const selectedPosition = ref("大模型算法工程师")
const newPositions = ref<any[]>([])
const positions = ref<string[]>([])
const trendRef = ref<HTMLElement | null>(null)
let chart: any = null
const running = ref(false)
const showAuditModal = ref(false)
const auditItems = ref<any[]>([])
const auditLoading = ref(false)

onMounted(async () => {
  overview.value = await fetchOverview()
  newPositions.value = overview.value?.newPositions || []
  positions.value = await fetchInsightsPositions()
  if (positions.value.length > 0) {
    selectedPosition.value = positions.value[0]
  }
  await loadTrend()
  loading.value = false
})
async function openAuditModal() {
  showAuditModal.value = true
  auditLoading.value = true
  const items = await fetchAuditItems()
  if (Array.isArray(items)) auditItems.value = items
  auditLoading.value = false
}
async function doApprove(id) {
  await approveAuditItem(id)
  auditItems.value = auditItems.value.filter(i => i.id !== id)
  if (overview.value) overview.value.pendingAudit = auditItems.value.length
}
function doSkip(item) {
  auditItems.value = auditItems.value.filter(i => i.id !== item.id)
}
onUnmounted(() => { if (chart) chart.dispose() })

async function loadTrend() {
  skillTrend.value = await fetchSkillTrend(selectedPosition.value)
  renderChart()
}

function renderChart() {
  if (!trendRef.value || !skillTrend.value) return
  import("echarts").then((e: any) => {
    if (chart) chart.dispose()
    chart = e.init(trendRef.value!)
    const periods = skillTrend.value.periods || []
    const skills = skillTrend.value.skills || {}
    const colors = {new:"#6bcb77",rising:"#00ffff",declining:"#ffd93d",stable:"#546e7a",dying:"#ff6b6b"}
    const series = Object.entries(skills).slice(0,5).map(([n, d]: [string, any]) => ({
      name: n, type: "line", smooth: true,
      data: d.frequency || [], symbol: "circle", symbolSize: 5,
      lineStyle: { width: 2, color: colors[d.change] || "#546e7a" },
      itemStyle: { color: colors[d.change] || "#546e7a" },
    }))
    chart.setOption({
      tooltip: { trigger: "axis", backgroundColor: "rgba(10,22,40,0.9)", borderColor: "rgba(0,255,255,0.2)", textStyle: { color: "rgba(176,196,222,0.8)", fontSize: 11 } },
      legend: { data: Object.keys(skills).slice(0,5), bottom: 0, textStyle: { color: "rgba(176,196,222,0.5)", fontSize: 10 } },
      grid: { left: 40, right: 15, top: 20, bottom: 40 },
      xAxis: { type: "category", data: periods, axisLine: { lineStyle: { color: "rgba(0,255,255,0.1)" } }, axisLabel: { color: "rgba(176,196,222,0.4)", fontSize: 9 } },
      yAxis: { type: "value", splitLine: { lineStyle: { color: "rgba(0,255,255,0.05)", type: "dashed" } }, axisLabel: { color: "rgba(176,196,222,0.4)", fontSize: 9 } },
      series
    })
  })
}

function gc(c: string): string {
  const m = {new:"#6bcb77",rising:"#00ffff",declining:"#ffd93d",dying:"#ff6b6b",stable:"#546e7a"}
  return m[c] || "#546e7a"
}

async function handleNP(id: string, a: string) {
  await handleNewPosition(id, a)
  newPositions.value = newPositions.value.map(p => p.id === id ? { ...p, status: a === "confirm" ? "confirmed" : "dismissed" } : p)
}

async function trigger() {
  running.value = true
  await runDiscovery()
  overview.value = await fetchOverview()
  newPositions.value = overview.value?.newPositions || []
  positions.value = await fetchInsightsPositions()
  if (positions.value.length > 0 && !selectedPosition.value) {
    selectedPosition.value = positions.value[0]
  }
  running.value = false
}
</script>
