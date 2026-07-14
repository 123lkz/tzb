// 招聘单位总数量数据 - 包含年度和月度的全口径和应届大专生数据
export interface CompanyData {
  year: {
    all: YearlyCompanyAllData[]
    college: YearlyCompanyFreshGraduateData[]
  }
  month: {
    all: MonthlyCompanyAllData[]
    college: MonthlyCompanyFreshGraduateData[]
  }
}

// 年度全口径招聘单位总数量据
export interface YearlyCompanyAllData {
  name: string
  value: number // 招聘单位总数量
}

// 年度应届大专生招聘单位总数量据
export interface YearlyCompanyFreshGraduateData {
  name: string
  value: number // 应届大专生招聘单位总数量
}

// 月度全口径招聘单位总数量据
export interface MonthlyCompanyAllData {
  name: string
  value: number // 招聘单位总数量
}

// 月度应届大专生招聘单位总数量据
export interface MonthlyCompanyFreshGraduateData {
  name: string
  value: number // 应届大专生招聘单位总数量
}

// 真实数据
export const companyData: CompanyData = {
  year: {
    // 真实数据
    all: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 255278 },
    ],
    // 真实数据
    college: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 81028 },
    ],
  },
  month: {
    // 真实数据
    all: [
      { name: '2025-01', value: 12019 },
      { name: '2025-02', value: 39076 },
      { name: '2025-03', value: 54748 },
      { name: '2025-04', value: 98822 },
      { name: '2025-05', value: 50613 },
    ],
    // 真实数据
    college: [
      { name: '2025-01', value: 2853 },
      { name: '2025-02', value: 11818 },
      { name: '2025-03', value: 16561 },
      { name: '2025-04', value: 33460 },
      { name: '2025-05', value: 16336 },
    ],
  },
}

export default companyData
