// 招聘职位总个数数据 - 包含年度和月度的全口径和应届大专生数据
export interface ProfessionData {
  year: {
    all: YearlyProfessionAllData[]
    college: YearlyProfessionFreshGraduateData[]
  }
  month: {
    all: MonthlyProfessionAllData[]
    college: MonthlyProfessionFreshGraduateData[]
  }
}

// 年度全口径招聘职业个数数据
export interface YearlyProfessionAllData {
  name: string
  value: number // 招聘职位总个数
}

// 年度应届大专生招聘职业个数数据
export interface YearlyProfessionFreshGraduateData {
  name: string
  value: number // 应届大专生招聘职位总个数
}

// 月度全口径招聘职业个数数据
export interface MonthlyProfessionAllData {
  name: string
  value: number // 招聘职位总个数
}

// 月度应届大专生招聘职业个数数据
export interface MonthlyProfessionFreshGraduateData {
  name: string
  value: number // 应届大专生招聘职位总个数
}

export const professionData: ProfessionData = {
  year: {
    // 真实数据
    all: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 982366 },
    ],
    // 真实数据
    college: [
      { name: '2021', value: 0 },
      { name: '2022', value: 0 },
      { name: '2023', value: 0 },
      { name: '2024', value: 0 },
      { name: '2025', value: 370883 }, // FIXME: 跟总数有点差异，需要确认
    ],
  },
  month: {
    // 真实数据
    all: [
      { name: '2025-01', value: 24750 },
      { name: '2025-02', value: 102252 },
      { name: '2025-03', value: 165892 },
      { name: '2025-04', value: 471587 },
      { name: '2025-05', value: 217885 },
    ],
    // 真实数据
    college: [
      { name: '2025-01', value: 5388 },
      { name: '2025-02', value: 29063 },
      { name: '2025-03', value: 52375 },
      { name: '2025-04', value: 175477 },
      { name: '2025-05', value: 108580 },
    ],
  },
}

export default professionData
