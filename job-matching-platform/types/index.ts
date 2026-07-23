// 类型定义
export interface PositionInfo {
  id: string; name: string; company: string; industry: string
  province: string; city: string; salaryMin: number; salaryMax: number
  education: string; experience: string; publishDate: string; recruitNumber: number
  description: string; responsibilities: string[]; requiredSkills: string[]; optionalSkills: string[]
  tags: string[]; platform: string; positionUrl: string
}
export interface ResumeProfile {
  personalInfo: { name: string; phone: string; email: string; highestEducation: string; workYears: number; currentPosition: string; currentCompany: string }
  education: { school: string; degree: string; major: string; startDate: string; endDate: string }[]
  workExperience: { company: string; position: string; startDate: string; endDate: string; responsibilities: string[]; achievements: string[] }[]
  projectExperience: { name: string; role: string; description: string; techStack: string[]; highlights: string[] }[]
  skills: string[]; parsingMethod: 'llm' | 'rule' | 'hybrid'; confidence: number
}
export interface DimensionScore { skill: number; experience: number; responsibility: number }
export interface SkillMatchItem { skill: string; required: boolean; matched: boolean; evidence: string; gapReason?: string; suggestion?: string }
export interface GapItem { skill: string; importance: 'high' | 'medium' | 'low'; reason: string; suggestion: string }
export type RecommendationLevel = 'highly_recommend' | 'recommend' | 'consider' | 'not_recommend'
export interface MatchReport {
  id: string; resumeId: string; positionId: string; positionName: string; companyName: string
  overallMatchScore: number; dimensionScores: DimensionScore
  requiredSkillMatchRate: number; optionalSkillMatchRate: number
  skillMatches: SkillMatchItem[]; gaps: GapItem[]; strengths: string[]
  recommendation: RecommendationLevel; confidence: number
  provenance: { model: string; timestamp: string }
}
export interface GraphNode { id: string; name: string; type: 'position' | 'skill' | 'industry' | 'company'; category: number; symbolSize: number; description?: string; properties?: Record<string, string> }
export interface GraphEdge { id: string; source: string; target: string; label: string; weight?: number; confidence?: number; evidence?: string }
export interface GraphData { nodes: GraphNode[]; edges: GraphEdge[]; categories: { name: string; itemStyle: { color: string } }[] }
export interface Breadcrumb { label: string; path: string }
export interface MenuItem { label: string; icon: string; path: string }
