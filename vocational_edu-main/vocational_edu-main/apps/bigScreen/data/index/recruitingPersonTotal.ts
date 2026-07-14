// 招聘需求总人数数据 - 包含年度和月度的全口径和应届大专生数据
export interface PersonData {
  year: {
    all: YearlyPersonAllData[]
    college: YearlyPersonFreshGraduateData[]
  }
  month: {
    all: MonthlyPersonAllData[]
    college: MonthlyPersonFreshGraduateData[]
  }
}

// 年度全口径招聘需求人数数据
export interface YearlyPersonAllData {
  name: string
  value: number // 招聘需求总人数
}

// 年度应届大专生招聘需求人数数据
export interface YearlyPersonFreshGraduateData {
  name: string
  value: number // 应届大专生招聘需求总人数
}

// 月度全口径招聘需求人数数据
export interface MonthlyPersonAllData {
  name: string
  value: number // 招聘需求总人数
}

// 月度应届大专生招聘需求人数数据
export interface MonthlyPersonFreshGraduateData {
  name: string
  value: number // 应届大专生招聘需求总人数
}

// 真实数据
export const personData: PersonData = {
  year: {
    // 真实数据
    all: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 12175374 },
    ],
    // 真实数据
    college: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 8843529 },
    ],
  },
  month: {
    // 真实数据
    all: [
      { name: '2025-01', value: 198889 },
      { name: '2025-02', value: 732547 },
      { name: '2025-03', value: 1526750 },
      { name: '2025-04', value: 5558113 },
      { name: '2025-05', value: 4159075 },
    ],
    // 真实数据
    college: [
      { name: '2025-01', value: 77260 },
      { name: '2025-02', value: 361998 },
      { name: '2025-03', value: 910314 },
      { name: '2025-04', value: 3947628 },
      { name: '2025-05', value: 3546329 },
    ],
  },
}

export default personData
