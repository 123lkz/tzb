// 总览数据 - 包含年度和月度的全口径和应届大专生数据
export interface TotalData {
  statisticalYear: string
  statisticalMonth: string
  statisticalStudentYear: string
  year: {
    all: YearlyAllData
    college: YearlyFreshGraduateData
  }
  month: {
    all: MonthlyAllData
    college: MonthlyFreshGraduateData
  }
}

// 年度全口径数据
export interface YearlyAllData {
  year: string
  staticStudentYear: string
  totalRecruitmentProfession: number // 招聘职位总个数
  totalRecruitmentPerson: number // 招聘需求总人数
  totalCompanyCount: number // 总单位数量
  salary25thPercentile: number // 招聘薪资25%分位数
  salaryMedian: number // 招聘薪资中位数
  salary75thPercentile: number // 招聘薪资75%分位数
  totalJuniorCollegeStudents: number // 全国大专生在校人数
  totalJuniorCollegeProfession: number // 全国大专生招聘职位总个数
  juniorCollegeSalaryMedian: number // 全国大专生招聘薪资中位数
}

// 年度应届大专生数据
export interface YearlyFreshGraduateData {
  year: string
  staticStudentYear: string
  totalRecruitmentProfession: number // 应届大专生招聘职位总个数
  totalRecruitmentPerson: number // 应届大专生招聘需求总人数
  totalCompanyCount: number // 应届大专生总单位数量
  salary25thPercentile: number // 招聘薪资25%分位数
  salaryMedian: number // 招聘薪资中位数
  salary75thPercentile: number // 招聘薪资75%分位数
  totalJuniorCollegeStudents: number // 全国大专生在校人数
  totalJuniorCollegeProfession: number // 应届大专生招聘职位总个数
  juniorCollegeSalaryMedian: number // 应届大专生招聘薪资中位数
}

// 月度全口径数据
export interface MonthlyAllData {
  year: string
  month: string
  staticStudentYear: string
  totalRecruitmentProfession: number // 招聘职位总个数
  totalRecruitmentPerson: number // 招聘需求总人数
  totalCompanyCount: number // 总单位数量
  salary25thPercentile: number // 招聘薪资25%分位数
  salaryMedian: number // 招聘薪资中位数
  salary75thPercentile: number // 招聘薪资75%分位数
  totalJuniorCollegeStudents: number // 全国大专生在校人数
  totalJuniorCollegeProfession: number // 全国大专生招聘职位总个数
  juniorCollegeSalaryMedian: number // 全国大专生招聘薪资中位数
}

// 月度应届大专生数据
export interface MonthlyFreshGraduateData {
  year: string
  month: string
  staticStudentYear: string
  totalRecruitmentProfession: number // 应届大专生招聘职位总个数
  totalRecruitmentPerson: number // 应届大专生招聘需求总人数
  totalCompanyCount: number // 应届大专生总单位数量
  salary25thPercentile: number // 招聘薪资25%分位数
  salaryMedian: number // 招聘薪资中位数
  salary75thPercentile: number // 招聘薪资75%分位数
  totalJuniorCollegeStudents: number // 全国大专生在校人数
  totalJuniorCollegeProfession: number // 应届大专生招聘职位总个数
  juniorCollegeSalaryMedian: number // 应届大专生招聘薪资中位数
}

// 真实数据
export const totalData: TotalData = {
  statisticalYear: '2025年',
  statisticalMonth: '2025年5月',
  statisticalStudentYear: '2023年',
  year: {
    all: {
      year: '2025',
      staticStudentYear: '2023',
      totalRecruitmentProfession: 1005994,
      totalRecruitmentPerson: 12175374,
      totalCompanyCount: 255278,
      salary25thPercentile: 6500,
      salaryMedian: 9000,
      salary75thPercentile: 12000,
      totalJuniorCollegeStudents: 4489947,
      totalJuniorCollegeProfession: 720381,
      juniorCollegeSalaryMedian: 8000,
    },
    college: {
      year: '2025',
      staticStudentYear: '2023',
      totalRecruitmentProfession: 376982,
      totalRecruitmentPerson: 9040868,
      totalCompanyCount: 58985,
      salary25thPercentile: 6000,
      salaryMedian: 8000,
      salary75thPercentile: 10500,
      totalJuniorCollegeStudents: 4489947,
      totalJuniorCollegeProfession: 376982,
      juniorCollegeSalaryMedian: 8000,
    },
  },
  month: {
    all: {
      year: '2025',
      month: '05',
      staticStudentYear: '2023',
      totalRecruitmentProfession: 217885,
      totalRecruitmentPerson: 4159075,
      totalCompanyCount: 50436,
      salary25thPercentile: 6500,
      salaryMedian: 8500,
      salary75thPercentile: 11000,
      totalJuniorCollegeStudents: 4489947,
      totalJuniorCollegeProfession: 171101,
      juniorCollegeSalaryMedian: 8000,
    },
    college: {
      year: '2025',
      month: '05',
      staticStudentYear: '2023',
      totalRecruitmentProfession: 181462,
      totalRecruitmentPerson: 3546329,
      totalCompanyCount: 16336,
      salary25thPercentile: 6000,
      salaryMedian: 8000,
      salary75thPercentile: 10500,
      totalJuniorCollegeStudents: 4489947,
      totalJuniorCollegeProfession: 181462,
      juniorCollegeSalaryMedian: 8000,
    },
  },
}

export default totalData
