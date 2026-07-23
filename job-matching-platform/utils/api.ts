import { filterPositions, generateMockReport, mockResume, mockGraphData, getPositionById, mockPositions } from "~/utils/mockData"
import type { PositionInfo, ResumeProfile, MatchReport, GraphData } from "~/types"

// ===== Mock API (always available) =====

export async function fetchPositions(params: any): Promise<any> {
  const result = await callApi('/positions?search=' + encodeURIComponent((params.keyword || '').trim()))
  if (result?.items && result.items.length > 0) {
    let items = result.items.slice(0, 100)
    if (params.industry) items = items.filter(p => p.industry === params.industry)
    if (params.province) items = items.filter(p => p.province === params.province)
    if (params.education) items = items.filter(p => p.education.includes((params.education || '').replace('及以上','')))
    if (params.experience) items = items.filter(p => p.experience === params.experience)
    if (params.salaryMin) items = items.filter(p => p.salaryMax >= params.salaryMin)
    if (params.salaryMax) items = items.filter(p => p.salaryMin <= params.salaryMax)
    if (params.sortBy === 'salary_asc') items.sort((a,b) => (a.salaryMin||0) - (b.salaryMin||0))
    else if (params.sortBy === 'salary_desc') items.sort((a,b) => (b.salaryMax||0) - (a.salaryMax||0))
    else if (params.sortBy === 'date_desc') items.sort((a,b) => b.publishDate.localeCompare(a.publishDate))
    else if (params.sortBy === 'recruit_desc') items.sort((a,b) => (b.recruitNumber||0) - (a.recruitNumber||0))
    const total = items.length
    const pageSize = params.pageSize || 12
    const start = ((params.page || 1) - 1) * pageSize
    return { items: items.slice(start, start + pageSize), total, page: params.page || 1, pageSize, totalPages: Math.ceil(total / pageSize), allItems: items }
  }
  return filterPositions(params)
  }
export async function fetchPositionById(id: string): Promise<PositionInfo | undefined> {
  return new Promise(resolve => setTimeout(() => resolve(getPositionById(id)), 200))
}
export async function fetchGraphData(): Promise<GraphData> {
  return new Promise(resolve => setTimeout(() => resolve(mockGraphData), 800))
}

// ===== Agent3 Backend API (try first, fall back to mock) =====

const API_BASE = "http://localhost:8720/api"
const USE_BACKEND = true  // Set to false when backend is running

export interface BackendStatus {
  ok: boolean
  available: boolean
}

async function callApi(endpoint: string, options?: RequestInit): Promise<any | null> {
  try {
    const res = await fetch(API_BASE + endpoint, {
      ...options,
      signal: typeof AbortSignal !== 'undefined' ? AbortSignal.timeout(15000) : undefined,
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

export async function checkBackendStatus(): Promise<BackendStatus> {
  const result = await callApi("/health")
  return { ok: !!result, available: result?.agent3_available || false }
}

export async function searchPositions(keyword: string): Promise<{ items: PositionInfo[], total: number }> {
  if (USE_BACKEND) {
    const result = await callApi("/positions?search=" + encodeURIComponent(keyword))
    if (result) return result
  }
  const kw = keyword.toLowerCase()
  const items = mockPositions.filter(p =>
    p.name.toLowerCase().includes(kw) ||
    p.company.toLowerCase().includes(kw) ||
    p.industry.toLowerCase().includes(kw) ||
    p.tags.some(t => t.toLowerCase().includes(kw))
  )
  return { items, total: items.length }
}

export async function parseResume(file: File): Promise<ResumeProfile> {
  if (USE_BACKEND) {
    const form = new FormData()
    form.append("file", file)
    const result = await callApi("/parse-resume", { method: "POST", body: form })
    if (result?.ok) return result.data
  }
  return new Promise(resolve => setTimeout(() => resolve({ ...mockResume }), 1500))
}

export async function matchResumeToPosition(
  resumeProfile: ResumeProfile,
  positionName: string
): Promise<MatchReport> {
  if (USE_BACKEND) {
    // For backend, we need the original file. Use mock as fallback.
  }
  const pos = mockPositions.find(p => p.name === positionName)
  return new Promise(resolve =>
    setTimeout(() => resolve(generateMockReport(pos?.name || positionName)), 2000)
  )
}

export async function matchResumeToAll(resumeProfile: ResumeProfile): Promise<MatchReport[]> {
  if (USE_BACKEND) {
    // For backend, we need the original file.
  }
  return new Promise(resolve =>
    setTimeout(() => resolve(
      mockPositions.slice(0, 5).map(p => generateMockReport(p.name))
    ), 3000)
  )
}

// ===== Agent3 real matching API (requires backend + Agent3) =====

export async function agent3ParseResume(file: File): Promise<any> {
  const form = new FormData()
  form.append("file", file)
  const result = await callApi("/parse-resume", { method: "POST", body: form })
  if (result?.ok) return result.data
  // Fallback to mock
  return new Promise(resolve => setTimeout(() => resolve({ ...mockResume }), 1500))
}

export async function agent3MatchPosition(file: File, positionName: string): Promise<MatchReport[]> {
  const form = new FormData()
  form.append("file", file)
  form.append("position", positionName)
  const result = await callApi("/match-position", { method: "POST", body: form })
  if (result?.ok) return result.data
  // Fallback
  const pos = mockPositions.find(p => p.name === positionName)
  return [await new Promise(resolve =>
    setTimeout(() => resolve(generateMockReport(pos?.name || positionName)), 2000)
  )]
}

export async function agent3MatchAll(file: File): Promise<MatchReport[]> {
  const form = new FormData()
  form.append("file", file)
  const result = await callApi("/match-all", { method: "POST", body: form })
  if (result?.ok) return result.data
  // Fallback
  return await new Promise(resolve =>
    setTimeout(() => resolve(
      mockPositions.slice(0, 5).map(p => generateMockReport(p.name))
    ), 3000)
  )
}

// ===== Insights API (Agent1 + Agent2) =====

export async function fetchOverview(): Promise<any> {
  const result = await callApi("/insights/overview")
  if (result?.ok) return result.data
  return {
    totalPositions: 20, totalSkills: 35, newPositionCount: 3,
    pendingAudit: 4, qualityScore: 86,
    newPositions: (() => {
      const base = {confidence:0.85,verified:false,status:"pending",clusterSize:0,noveltyScore:0,evidenceSamples:[],typicalSalaryRange:{},typicalExperience:"",relatedSkills:[],skillGap:[],improvementSuggestions:[],learningPath:[]}
      return [
        {id:"np-001",name:"多模态AI工程师",description:"负责多模态大模型（文本+图像+语音）的研发与落地。",requiredSkills:["Python","PyTorch","多模态Transformer","CLIP","语音识别"],optionalSkills:["TensorRT","ONNX"],coreResponsibilities:["多模态模型训练与优化","跨模态对齐","数据预处理"],typicalApplications:["智能客服","内容审核","自动驾驶感知"],...base},
        {id:"np-002",name:"AI数据标注师",description:"负责AI训练数据的标注、质检与管理。",requiredSkills:["Python","数据分析","标注工具","质量评估"],optionalSkills:["SQL","Excel"],coreResponsibilities:["数据标注与质检","标注工具优化","模型效果评估"],typicalApplications:["自动驾驶标注","NLP标注","图像标注"],...base},
        {id:"np-003",name:"联邦学习工程师",description:"负责联邦学习系统的设计与实现。",requiredSkills:["Python","TensorFlow","联邦学习","密码学","分布式系统"],optionalSkills:["PyTorch","Kubernetes"],coreResponsibilities:["联邦学习算法研发","安全聚合协议实现","分布式训练系统搭建"],typicalApplications:["医疗隐私计算","金融风控联","IoT边缘智能"],...base},
      ]
    })()
  }
}

  export async function fetchSkillTrend(position: string): Promise<any> {
  const result = await callApi("/insights/skills-trend?position=" + encodeURIComponent(position))
  if (result?.ok) return result.data
  return {
    periods: ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"],
    skills: {
      "Python": {frequency:[65,70,72,75,78,82],change:"rising",pct:"+12%"},
      "PyTorch": {frequency:[40,45,50,55,58,60],change:"rising",pct:"+8%"},
      "RAG": {frequency:[0,0,2,8,15,25],change:"new",pct:"新增"},
    }
  }
}

export async function fetchInsightsPositions(): Promise<string[]> {
  const result = await callApi("/insights/positions")
  if (result?.ok && Array.isArray(result.data) && result.data.length > 0) return result.data
  return mockPositions.map(p => p.name)
}

export async function fetchNewPositions(): Promise<any> {
  const result = await callApi("/insights/new-positions")
  if (result?.ok) return result.data
  return [
    {id:"np-001",name:"多模态AI工程师",confidence:0.82,verified:true,status:"pending"},
    {id:"np-002",name:"AI数据标注师",confidence:0.65,verified:false,status:"pending"},
  ]
}

export async function handleNewPosition(id: string, action: string): Promise<any> {
  const result = await callApi("/insights/new-positions/" + action + "?position_id=" + id, {method:"POST"})
  if (result?.ok) return result.data
  return {id, status: action}
}

export async function runDiscovery(): Promise<any> {
  const result = await callApi("/insights/run-discovery", {method:"POST"})
  if (result?.ok) return result.data
  return {status:"completed",summary:{newPositions:3,qualityScore:86}}
}

export async function fetchQuality(): Promise<any> {
  const result = await callApi("/insights/quality")
  if (result?.ok) return result.data
  return {
    overallScore:86, checkerHistory:[
      {name:"完整性",passRate:92},{name:"一致性",passRate:78},
      {name:"时效性",passRate:96},{name:"抄袭检测",passRate:100},{name:"噪声检测",passRate:85}
    ]
  }
}

export async function fetchAuditQueue(): Promise<any> {
  const result = await callApi("/insights/audit")
  if (result?.ok) return result.data
  return [{id:"aq-001",positionName:"多模态AI工程师",skillName:"CLIP",confidence:0.82,status:"pending"}]
}

export async function handleAudit(id: string, action: string): Promise<any> {
  const result = await callApi("/insights/audit/" + action, {method:"POST"})
  if (result?.ok) return result.data
  return {id, status: action}
}

export async function fetchAuditItems(): Promise<any> {
  const result = await callApi("/insights/audit-queue")
  if (result?.ok) return result.data
  return []
}

export async function approveAuditItem(id: string): Promise<any> {
  const result = await callApi("/insights/audit-queue/approve?id=" + id, {method:"POST"})
  return result || {ok:false}
}
