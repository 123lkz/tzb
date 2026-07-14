// 教育供给数据 - 包含年度和月度的全口径和应届大专生数据
export interface EducationData {
  year: {
    all: YearlyEducationAllData
    college: YearlyEducationFreshGraduateData
  }
  month: {
    all: MonthlyEducationAllData
    college: MonthlyEducationFreshGraduateData
  }
}

// 年度全口径教育数据
export interface YearlyEducationAllData {
  year: string
  schoolData: SchoolData[] // 双高/非双高学校数量
  schoolStudentData: SchoolStudentData[] // 双高/非双高院校在校生数
}

// 年度应届大专生教育数据
export interface YearlyEducationFreshGraduateData {
  year: string
  schoolData: SchoolData[] // 双高/非双高学校数量
  schoolStudentData: SchoolStudentData[] // 双高/非双高院校在校生数
}

// 月度全口径教育数据
export interface MonthlyEducationAllData {
  year: string
  month: string
  schoolData: SchoolData[] // 双高/非双高学校数量
  schoolStudentData: SchoolStudentData[] // 双高/非双高院校在校生数
}

// 月度应届大专生教育数据
export interface MonthlyEducationFreshGraduateData {
  year: string
  month: string
  schoolData: SchoolData[] // 双高/非双高学校数量
  schoolStudentData: SchoolStudentData[] // 双高/非双高院校在校生数
}

// 大专职业院校在校人数省份地图数据
export interface EducationProvinceMapData {
  name: string
  value: number // 在校人数
  doubleHighValue: number // 双高院校数量
  juniorCollegesValue: number // 大专院校数量
}

// 各省大专职业院校数排行
export interface SchoolNumberRecruitmentData {
  name: string
  value: number // 院校数量
}

// 大专专业学生数排行
export interface MajorStudentRecruitmentData {
  name: string
  value: number // 学生数量
}

// 双高/非双高学校数量
export interface SchoolData {
  name: string
  value: number // 学校数量
}

// 双高/非双高院校在校生数
export interface SchoolStudentData {
  name: string
  value: number // 在校生数量
}

// 总毕业生（最近5年）
export interface TotalGraduateData {
  name: string
  value: number // 毕业生数量
}

// 示例数据
export const educationData: EducationData = {
  year: {
    all: {
      year: '2025',
      schoolData: [
        { name: '双高大专院校', value: 195 },
        { name: '非双高大专院校', value: 2046 },
      ],
      schoolStudentData: [
        { name: '双高大专院校在校生数', value: 788718 },
        { name: '非双高大专院校在校生数', value: 3701229 },
      ],
    },
    college: {
      year: '2025',
      schoolData: [
        { name: '双高大专院校', value: 600 },
        { name: '非双高大专院校', value: 1600 },
      ],
      schoolStudentData: [
        { name: '双高大专院校在校生数', value: 600000 },
        { name: '非双高大专院校在校生数', value: 2800000 },
      ],
    },
  },
  month: {
    all: {
      year: '2025',
      month: '05',
      schoolData: [
        { name: '双高大专院校', value: 720 },
        { name: '非双高大专院校', value: 1950 },
      ],
      schoolStudentData: [
        { name: '双高大专院校在校生数', value: 750000 },
        { name: '非双高大专院校在校生数', value: 3500000 },
      ],
    },
    college: {
      year: '2025',
      month: '05',
      schoolData: [
        { name: '双高大专院校', value: 580 },
        { name: '非双高大专院校', value: 1500 },
      ],
      schoolStudentData: [
        { name: '双高大专院校在校生数', value: 580000 },
        { name: '非双高大专院校在校生数', value: 2700000 },
      ],
    },
  },
}

export default educationData
