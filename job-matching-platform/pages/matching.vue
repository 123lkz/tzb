
<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue"
import Header from "~/components/Layout/Header.vue"
import Card from "~/components/Common/Card.vue"
import Loading from "~/components/Common/Loading.vue"
import { searchPositions, agent3ParseResume, agent3MatchPosition, agent3MatchAll } from "~/utils/api"
import { mockResume } from "~/utils/mockData"
import type { MatchReport } from "~/types"

const breadcrumbs = [{label:'首页',path:'/'},{label:'简历-岗位匹配',path:'/matching'}]

const step = ref("upload") // upload / parsing / parsed / matching / result
const fileName = ref("")
const resumeFile = ref<File | null>(null)
const dragOver = ref(false)
const matchMode = ref("single") // single / all
const matchResults = ref<MatchReport[]>([])
const uploadedFileForAPI = ref<File | null>(null)
const resumeProfile = ref<any>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)

// Position search
const posSearch = ref("")
const showPosDropdown = ref(false)
const selectedPosName = ref("")
const searchResults = ref<{ name: string; company: string }[]>([])

// Debounced position search
let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(posSearch, (val) => {
  if (searchTimer) clearTimeout(searchTimer)
  if (!val) { searchResults.value = []; showPosDropdown.value = false; return }
  searchTimer = setTimeout(async () => {
    const res = await searchPositions(val)
    searchResults.value = res.items.map((p: any) => ({ name: p.name, company: p.company }))
    showPosDropdown.value = true
  }, 300)
})

function selectPosition(name: string) {
  selectedPosName.value = name
  posSearch.value = name
  showPosDropdown.value = false
}

async function handleFile(file: File) {
  fileName.value = file.name
  resumeFile.value = file
  uploadedFileForAPI.value = file
  // Show mock data immediately (no waiting)
  resumeProfile.value = mockResume
  step.value = "parsed"
  // Try API in background (30s timeout)
  agent3ParseResume(file).then(data => {
    if (data) resumeProfile.value = data
  }).catch(() => {})
}

function handleDrop(e: DragEvent) {
  dragOver.value = false
  const fl = e.dataTransfer?.files?.[0]
  if (fl) handleFile(fl)
}

function handleInput(e: Event) {
  const fl = (e.target as HTMLInputElement).files?.[0]
  if (fl) handleFile(fl)
}

async function startMatch() {
  if (!resumeFile.value) return
  step.value = "matching"

  try {
    if (matchMode.value === "single" && selectedPosName.value) {
      matchResults.value = await agent3MatchPosition(resumeFile.value, selectedPosName.value)
    } else {
      matchResults.value = await agent3MatchAll(resumeFile.value)
    }
  } catch {
    // Fallback
    matchResults.value = []
  }

  step.value = "result"
}

function resetAll() {
  step.value = "upload"
  resumeFile.value = null
  uploadedFileForAPI.value = null
  selectedPosName.value = ""
  posSearch.value = ""
  searchResults.value = []
  matchResults.value = []
  fileName.value = ""
}

function getScoreColor(s: number): string {
  return s >= 0.8 ? "#6bcb77" : s >= 0.6 ? "#ffd93d" : "#ff6b6b"
}

function getRecLabel(r: string): string {
  const map: Record<string, string> = {
    highly_recommend: "强烈推荐",
    recommend: "推荐",
    consider: "可以考虑",
    not_recommend: "暂不推荐",
  }
  return map[r] || r
}

onMounted(async () => {
  const res = await searchPositions('')
  if (res?.items) {
    searchResults.value = res.items.map((p: any) => ({ name: p.name, company: p.company }))
  }
})
</script>

<template>
<div class="fade-in">
  <Header :breadcrumbs="breadcrumbs">
    <template #right>
      <button v-if="step==='result'" class="px-3 py-1 text-xs rounded bg-[rgba(0,255,255,0.1)] text-[#00ffff] hover:bg-[rgba(0,255,255,0.2)] transition-all cursor-pointer" @click="resetAll">重新匹配</button>
    </template>
  </Header>

  <div class="grid grid-cols-5 gap-4 h-[calc(100vh-8rem)]">

    <!-- ===== Left: Upload Area ===== -->
    <div class="col-span-2 flex flex-col gap-4">
      <!-- Upload Zone -->
      <Card v-if="step==='upload'" class="flex-1 flex-center">
        <div class="w-full h-full flex-center flex-col gap-4 border-2 border-dashed rounded-lg cursor-pointer transition-all"
          :class="dragOver?'border-[#00ffff] bg-[rgba(0,255,255,0.1)]':'border-[rgba(0,255,255,0.2)] hover:border-[rgba(0,255,255,0.4)]'"
          @dragover.prevent="dragOver=true" @dragleave="dragOver=false" @drop.prevent="handleDrop"
          @click="fileInputRef?.click()">
          <svg class="w-12 h-12 text-[rgba(0,255,255,0.3)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
          <p class="text-sm text-[rgba(176,196,222,0.5)]">拖拽或点击上传简历</p>
          <p class="text-xs text-[rgba(176,196,222,0.3)]">支持 PDF / Word / TXT 格式</p>
          <div class="flex gap-2 mt-1">
            <span class="px-2 py-0.5 text-[10px] rounded bg-[rgba(0,255,255,0.06)] text-[rgba(0,255,255,0.5)]">.pdf</span>
            <span class="px-2 py-0.5 text-[10px] rounded bg-[rgba(0,255,255,0.06)] text-[rgba(0,255,255,0.5)]">.doc</span>
            <span class="px-2 py-0.5 text-[10px] rounded bg-[rgba(0,255,255,0.06)] text-[rgba(0,255,255,0.5)]">.docx</span>
            <span class="px-2 py-0.5 text-[10px] rounded bg-[rgba(255,217,61,0.06)] text-[rgba(255,217,61,0.6)]">.txt</span>
          </div>
          <input ref="fileInputRef" id="ri" type="file" accept=".pdf,.doc,.docx,.txt" class="hidden" @change="handleInput">
        </div>
      </Card>

      <!-- Parsing -->
      <Card v-if="step==='parsing'" class="flex-1 flex-center">
        <Loading text="正在解析简历..." />
      </Card>

      <!-- Resume Info -->
      <Card v-if="step==='parsed'||step==='matching'||step==='result'" class="flex-1 overflow-y-auto custom-scrollbar">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm text-[#00ffff] font-semibold">简历解析</h3>
          <span class="text-[10px] text-[rgba(176,196,222,0.4)]">{{ fileName }}</span>
        </div>
        <div class="space-y-2 text-xs text-[rgba(176,196,222,0.6)]">
          <div v-if="resumeProfile" class="space-y-2 text-xs">
            <div class="bg-[rgba(0,255,255,0.04)] rounded p-2">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-semibold text-[#00ffff]">{{ resumeProfile.personalInfo?.name || resumeProfile.candidateName || '--' }}</span>
                <span class="text-xs px-1.5 py-0.5 rounded"
                  :class="(resumeProfile.confidence || 0) >= 0.8 ? 'bg-[rgba(107,203,119,0.1)] text-[#6bcb77]' : 'bg-[rgba(255,217,61,0.1)] text-[#ffd93d]'">
                  置信度: {{ Math.round((resumeProfile.confidence || 0) * 100) }}%
                </span>
              </div>
              <div class="grid grid-cols-2 gap-1 text-[rgba(176,196,222,0.6)]">
                <div>学历: {{ resumeProfile.personalInfo?.highestEducation || resumeProfile.personalInfo?.educationLevel || '--' }}</div>
                <div>经验: {{ resumeProfile.personalInfo?.workYears || resumeProfile.personalInfo?.yearsOfExperience || '--' }} 年</div>
              </div>
            </div>
            <div v-if="(resumeProfile.skills || []).length > 0">
              <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">技能（{{ (resumeProfile.skills || []).length }} 项）</div>
              <div class="flex flex-wrap gap-1">
                <span v-for="s in (resumeProfile.skills || [])" :key="s"
                  class="px-1.5 py-0.5 text-xs rounded bg-[rgba(0,255,255,0.08)] text-[rgba(0,255,255,0.6)]">{{ s }}</span>
              </div>
            </div>
            <div v-if="(resumeProfile.education || []).length > 0">
              <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">教育背景</div>
              <div v-for="(edu, i) in (resumeProfile.education || []).slice(0, 2)" :key="i"
                class="flex items-start gap-2 bg-[rgba(0,255,255,0.03)] rounded p-1.5 mb-1">
                <div class="w-1.5 h-1.5 rounded-full bg-[rgba(0,255,255,0.3)] mt-1 flex-shrink-0"></div>
                <div>
                  <div class="text-[rgba(176,196,222,0.7)]">{{ edu.school }}</div>
                  <div class="text-xs text-[rgba(176,196,222,0.4)]">{{ edu.degree }} · {{ edu.major }}</div>
                </div>
              </div>
            </div>
            <div v-if="((resumeProfile.workExperience || resumeProfile.workExperiences || [])).length > 0">
              <div class="text-[10px] text-[rgba(176,196,222,0.4)] mb-1">工作经历</div>
              <div v-for="(we, i) in (resumeProfile.workExperience || resumeProfile.workExperiences || []).slice(0, 1)" :key="i"
                class="flex items-start gap-2 bg-[rgba(255,107,107,0.03)] rounded p-1.5 mb-1">
                <div class="w-1.5 h-1.5 rounded-full bg-[rgba(255,107,107,0.3)] mt-1 flex-shrink-0"></div>
                <div>
                  <div class="text-[rgba(176,196,222,0.7)]">{{ we.company }} · {{ we.position }}</div>
                  <div v-if="we.responsibilities" class="text-xs text-[rgba(176,196,222,0.4)]">{{ (we.responsibilities || []).slice(0, 2).join(' · ') }}</div>
                </div>
              </div>
            </div>
            <div class="text-xs text-[rgba(176,196,222,0.2)] pt-1 border-t border-[rgba(0,255,255,0.06)]">
              解析引擎: Agent3 · {{ resumeProfile.parsingMethod || 'mock' }} 模式
              <span v-if="step==='result'" class="text-[#6bcb77] ml-2">已匹配</span>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- ===== Right: Matching Area ===== -->
    <div class="col-span-3 flex flex-col gap-4">

      <!-- Configuration (shown after parse) -->
      <Card v-if="step==='parsed'">
        <div class="flex items-center gap-4 mb-3">
          <h3 class="text-sm text-[#00ffff]">匹配方式</h3>
          <div class="flex gap-1 bg-[rgba(0,255,255,0.05)] rounded p-0.5">
            <button class="px-3 py-1 text-xs rounded transition-all cursor-pointer"
              :class="matchMode==='single'?'bg-[rgba(0,255,255,0.15)] text-[#00ffff]':'text-[rgba(176,196,222,0.5)] hover:text-[rgba(176,196,222,0.8)]'"
              @click="matchMode='single'">指定岗位</button>
            <button class="px-3 py-1 text-xs rounded transition-all cursor-pointer"
              :class="matchMode==='all'?'bg-[rgba(0,255,255,0.15)] text-[#00ffff]':'text-[rgba(176,196,222,0.5)] hover:text-[rgba(176,196,222,0.8)]'"
              @click="matchMode='all'">全局匹配</button>
          </div>
        </div>

        <!-- Single position: Searchable input -->
        <div v-if="matchMode==='single'" class="relative">
          <label class="block text-[10px] text-[rgba(176,196,222,0.4)] mb-1">搜索岗位名称</label>
          <input v-model="posSearch"
            placeholder="输入岗位名称搜索..."
            @focus="showPosDropdown = searchResults.length > 0"
            @blur="setTimeout(() => showPosDropdown = false, 200)"
            class="w-full bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.15)] rounded px-3 py-1.5 text-xs text-[#00eaff] placeholder:text-[rgba(176,196,222,0.3)] outline-none focus:border-[#00ffff]"/>

          <!-- Search dropdown -->
          <div v-if="showPosDropdown && searchResults.length > 0"
            class="absolute z-50 w-full mt-1 bg-[#0d1b2a] border border-[rgba(0,255,255,0.2)] rounded-lg max-h-48 overflow-y-auto custom-scrollbar">
            <button v-for="item in searchResults" :key="item.name"
              @mousedown.prevent="selectPosition(item.name)"
              class="w-full text-left px-3 py-2 text-xs text-[rgba(176,196,222,0.7)] hover:bg-[rgba(0,255,255,0.08)] hover:text-[#00ffff] transition-colors cursor-pointer border-b border-[rgba(0,255,255,0.05)] last:border-0">
              <span class="font-medium">{{ item.name }}</span>
              <span class="ml-2 text-[10px] text-[rgba(176,196,222,0.3)]">{{ item.company }}</span>
            </button>
          </div>
          <p v-if="selectedPosName && matchMode==='single'" class="text-[10px] text-[#6bcb77] mt-1">
           已选择: {{ selectedPosName }}
          </p>
        </div>

        <!-- Global mode info -->
        <div v-else class="text-xs text-[rgba(176,196,222,0.4)] bg-[rgba(0,255,255,0.04)] rounded p-2">
          系统将对所有岗位进行全量匹配，推荐最优 Top-5 岗位。
        </div>

        <button class="mt-3 w-full py-2 text-sm rounded bg-[rgba(0,255,255,0.15)] text-[#00ffff] border border-[rgba(0,255,255,0.3)] hover:bg-[rgba(0,255,255,0.25)] disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer"
          :disabled="matchMode==='single' && !selectedPosName"
          @click="startMatch">
          {{ matchMode==='single' ? '开始匹配' : '开始全局匹配' }}
        </button>
      </Card>

      <!-- Loading -->
      <Card v-if="step==='matching'" class="flex-1 flex-center">
        <Loading text="正在计算匹配结果..." />
        <p class="text-[10px] text-[rgba(176,196,222,0.25)] mt-2">匹配引擎: Agent3 · 三维匹配体系</p>
      </Card>

      <!-- Results -->
      <div v-if="step==='result'" class="flex-1 overflow-y-auto custom-scrollbar space-y-3">
        <div class="text-xs text-[rgba(176,196,222,0.4)] mb-1">
          共 {{ matchResults.length }} 个匹配结果
          <span class="ml-2 text-[10px] text-[rgba(176,196,222,0.2)]">匹配引擎: Agent3</span>
        </div>

        <NuxtLink v-for="(r, i) in matchResults" :key="r.id || i"
          :to="'/matching/' + (r.id || 'report-' + i)"
          class="card card-hover no-underline block !p-4 cursor-pointer group">

          <div class="flex items-center justify-between mb-2">
            <div class="min-w-0 flex-1 mr-3">
              <div class="flex items-center gap-2">
                <span class="text-[10px] px-1.5 py-0.5 rounded bg-[rgba(0,255,255,0.1)] text-[rgba(0,255,255,0.5)]">#{{ i+1 }}</span>
                <h3 class="text-sm font-semibold text-[#00ffff] truncate group-hover:text-white transition-colors">{{ r.positionName }}</h3>
              </div>
              <p class="text-xs text-[rgba(176,196,222,0.4)] mt-0.5">{{ r.companyName || r.positionName }}</p>
            </div>
            <div class="text-center flex-shrink-0">
              <div class="text-xl font-bold" :style="{ color: getScoreColor(r.overallMatchScore) }">
                {{ Math.round(r.overallMatchScore * 100) }}%
              </div>
              <span class="text-xs text-[rgba(176,196,222,0.3)]">{{ getRecLabel(r.recommendation) }}</span>
            </div>
          </div>

          <!-- Dimension bars -->
          <div class="flex gap-3 mb-2" v-if="r.dimensionScores">
            <div v-for="(d, di) in r.dimensionScores" :key="di" class="flex-1">
              <div class="flex justify-between text-xs mb-0.5">
                <span class="text-[rgba(176,196,222,0.3)]">{{ d.dimension || di }}</span>
                <span class="text-[rgba(176,196,222,0.5)]">{{ Math.round((d.score || 0) * 100) }}%</span>
              </div>
              <div class="w-full bg-[rgba(0,255,255,0.1)] rounded h-1">
                <div class="h-full rounded" :style="{ width: (d.score || 0) * 100 + '%', background: getScoreColor(d.score || 0) }"></div>
              </div>
            </div>
          </div>

          <!-- Skills match -->
          <div v-if="r.skillMatches" class="flex flex-wrap gap-1 mb-2">
            <span v-for="s in r.skillMatches.slice(0, 5)" :key="s.skill_name || s.skill"
              class="px-1.5 py-0.5 text-xs rounded"
              :class="s.matched ? 'bg-[rgba(107,203,119,0.1)] text-[#6bcb77]' : 'bg-[rgba(255,107,107,0.1)] text-[#ff6b6b]'">
              {{ s.skill_name || s.skill }}
            </span>
            <span v-if="r.skillMatches.length > 5" class="text-xs text-[rgba(176,196,222,0.3)] self-center">+{{ r.skillMatches.length - 5 }}</span>
          </div>

          <!-- Bottom info -->
          <div class="flex justify-between items-center pt-1 border-t border-[rgba(0,255,255,0.06)]">
            <span class="text-xs text-[rgba(176,196,222,0.3)]">
              必需技能匹配: {{ Math.round((r.requiredSkillsMatchRate || r.requiredSkillMatchRate || 0) * 100) }}%
            </span>
            <span v-if="r.gaps && r.gaps.length > 0" class="text-xs text-[#ff6b6b]">
              差距: {{ r.gaps.length }} 项
            </span>
            <span v-else class="text-xs text-[#6bcb77]">无明显差距</span>
          </div>

          <!-- Strengths -->
          <div v-if="r.strengths?.length" class="mt-2">
            <div class="text-[11px] text-[rgba(107,203,119,0.5)] mb-0.5">优势</div>
            <div class="space-y-1">
              <div v-for="s in r.strengths.slice(0,3)" :key="s" class="bg-[rgba(107,203,119,0.06)] rounded p-1.5 text-[11px] text-[#6bcb77]">{{ s }}</div>
            </div>
          </div>

          <!-- Gap details -->
          <div v-if="r.gaps?.length" class="mt-2">
            <div class="text-[11px] text-[rgba(255,107,107,0.5)] mb-0.5">差距分析（{{ r.gaps.length }} 项）</div>
            <div class="space-y-1">
              <div v-for="g in r.gaps.slice(0,3)" :key="g.skill_name || g.skill" class="bg-[rgba(255,107,107,0.04)] rounded p-1.5">
                <div class="flex items-center gap-1 mb-0.5">
                  <span class="w-1 h-1 rounded-full flex-shrink-0" :class="g.importance==='high'?'bg-[#ff6b6b]':g.importance==='medium'?'bg-[#ffd93d]':'bg-[rgba(176,196,222,0.3)]'"></span>
                  <span class="text-[11px] text-[rgba(176,196,222,0.6)]">{{ g.skill_name || g.skill }}</span>
                  <span v-if="g.importance" class="text-[10px] px-1 rounded ml-auto" :class="g.importance==='high'?'text-[#ff6b6b] bg-[rgba(255,107,107,0.1)]':g.importance==='medium'?'text-[#ffd93d] bg-[rgba(255,217,61,0.1)]':'text-[rgba(176,196,222,0.3)] bg-[rgba(176,196,222,0.05)]'">{{ g.importance==='high'?'重要':g.importance==='medium'?'一般':'可选' }}</span>
                </div>
                <div v-if="g.suggestion" class="text-[10px] text-[rgba(176,196,222,0.35)] ml-1.5">{{ g.suggestion }}</div>
              </div>
            </div>
          </div>

          <!-- Summary -->
          <div v-if="r.summary" class="mt-2 pt-2 border-t border-[rgba(0,255,255,0.06)]">
            <div class="text-[11px] text-[rgba(176,196,222,0.3)] leading-relaxed italic">「{{ r.summary }}」</div>
          </div>
        </NuxtLink>
      </div>

      <!-- Placeholder (before upload) -->
      <Card v-if="step==='upload'" class="flex-1 flex-center">
        <div class="text-center">
          <svg class="w-16 h-16 mx-auto text-[rgba(0,255,255,0.1)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
          <p class="text-sm text-[rgba(176,196,222,0.3)] mt-2">左侧上传简历后即可进行岗位匹配</p>
          <p class="text-xs text-[rgba(176,196,222,0.2)] mt-1">支持指定岗位匹配 或 全局最优匹配</p>
        </div>
      </Card>
    </div>
  </div>
</div>
</template>

<style scoped>
select option { background: #0a1628; color: #00eaff; }
</style>
