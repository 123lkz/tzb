// 数据管理工具 - 统一管理四组数据
import totalData from './index/total'
import companyData from './index/recruitingCompanyTotal'
import personData from './index/recruitingPersonTotal'
import professionData from './index/recruitingProfessionTotal'
import positionData from './position/index'
import salaryData from './salary/index'
import educationData from './education/index'
import type { TotalData } from './index/total'
import type { CompanyData } from './index/recruitingCompanyTotal'
import type { PersonData } from './index/recruitingPersonTotal'
import type { ProfessionData } from './index/recruitingProfessionTotal'
import type { PositionData } from './position/index'
import type { SalaryData } from './salary/index'
import type { EducationData } from './education/index'
import { generateChangeRateData } from '../utils/num'

// 数据类型枚举
export type DataType = 'year' | 'month'
export type ScopeType = 'all' | 'college'

// 数据获取接口
export interface DataManager {
  // 获取总览数据
  getTotalData(type: DataType, scope: ScopeType): any
  // 获取招聘单位总数量据
  getCompanyData(type: DataType, scope: ScopeType): any
  // 获取招聘总人数数据
  getPersonData(type: DataType, scope: ScopeType): any
  // 获取招聘职业数据
  getProfessionData(type: DataType, scope: ScopeType): any
  // 获取职位信息数据
  getPositionData(type: DataType, scope: ScopeType): any
  // 获取薪酬信息数据
  getSalaryData(type: DataType, scope: ScopeType): any
  // 获取教育供给数据
  getEducationData(type: DataType, scope: ScopeType): any
}

/**
 * 格式化排名数据
 * @param data 数据
 * @param hasChangeRate 是否包含变化率
 * @returns 格式化后的数据
 */
const formatRankingData = (data: { name: string; value: number }[], { hasChangeRate = false }) => {
  const xAxisValue: string[] = []
  const yAxisValue: number[] = []
  const changeRate: number[] = []

  data.forEach((item: { name: string; value: number }, index: number) => {
    xAxisValue.push(item.name)
    yAxisValue.push(item.value)

    if (hasChangeRate) {
      if (index === 0) {
        changeRate.push(0)
      } else {
        const changeRateNum = generateChangeRateData(data[index - 1].value, item.value)
        changeRate.push(changeRateNum)
      }
    }
  })

  return {
    xAxisValue,
    yAxisValue,
    changeRate,
  }
}

// 数据管理类
export class VocationalEducationDataManager implements DataManager {
  // 获取总览数据
  getTotalData(type: DataType, scope: ScopeType) {
    if (type === 'year') {
      return scope === 'all' ? totalData.year.all : totalData.year.college
    } else {
      return scope === 'all' ? totalData.month.all : totalData.month.college
    }
  }

  // 获取招聘单位总数量据
  getCompanyData(type: DataType, scope: ScopeType) {
    let data
    if (type === 'year') {
      data = scope === 'all' ? companyData.year.all : companyData.year.college
    } else {
      data = scope === 'all' ? companyData.month.all : companyData.month.college
    }
    return formatRankingData(data, { hasChangeRate: true })
  }

  // 获取招聘总人数数据
  getPersonData(type: DataType, scope: ScopeType) {
    let data
    if (type === 'year') {
      data = scope === 'all' ? personData.year.all : personData.year.college
    } else {
      data = scope === 'all' ? personData.month.all : personData.month.college
    }
    return formatRankingData(data, { hasChangeRate: true })
  }

  // 获取招聘职业数据
  getProfessionData(type: DataType, scope: ScopeType) {
    let data
    if (type === 'year') {
      data =
        scope === 'all' ? professionData.year.all : professionData.year.college
    } else {
      data =
        scope === 'all' ? professionData.month.all : professionData.month.college
    }
    return formatRankingData(data, { hasChangeRate: true })
  }

  // 获取职位信息数据
  getPositionData(type: DataType, scope: ScopeType) {
    let data
    if (type === 'year') {
      data = scope === 'all' ? positionData.year.all : positionData.year.college
    } else {
      data =
        scope === 'all' ? positionData.month.all : positionData.month.college
    }
    return formatRankingData(data, { hasChangeRate: true })
  }

  // 获取薪酬信息数据
  getSalaryData(type: DataType, scope: ScopeType) {
    if (type === 'year') {
      return scope === 'all' ? salaryData.year.all : salaryData.year.college
    } else {
      return scope === 'all' ? salaryData.month.all : salaryData.month.college
    }
  }

  // 获取教育供给数据
  getEducationData(type: DataType, scope: ScopeType) {
    if (type === 'year') {
      return scope === 'all'
        ? educationData.year.all
        : educationData.year.college
    } else {
      return scope === 'all'
        ? educationData.month.all
        : educationData.month.college
    }
  }

  // 获取所有数据
  getAllData(type: DataType, scope: ScopeType) {
    return {
      total: this.getTotalData(type, scope),
      company: this.getCompanyData(type, scope),
      person: this.getPersonData(type, scope),
      profession: this.getProfessionData(type, scope),
      position: this.getPositionData(type, scope),
      salary: this.getSalaryData(type, scope),
      education: this.getEducationData(type, scope),
    }
  }

  // 更新数据（用于动态更新数据）
  updateData(category: string, type: DataType, scope: ScopeType, newData: any) {
    switch (category) {
      case 'total':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(totalData.year.all, newData)
          } else {
            Object.assign(totalData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            Object.assign(totalData.month.all, newData)
          } else {
            Object.assign(totalData.month.college, newData)
          }
        }
        break
      case 'company':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(companyData.year.all, newData)
          } else {
            Object.assign(companyData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            companyData.month.all = newData
          } else {
            companyData.month.college = newData
          }
        }
        break
      case 'person':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(personData.year.all, newData)
          } else {
            Object.assign(personData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            personData.month.all = newData
          } else {
            personData.month.college = newData
          }
        }
        break
      case 'profession':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(professionData.year.all, newData)
          } else {
            Object.assign(professionData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            professionData.month.all = newData
          } else {
            professionData.month.college = newData
          }
        }
        break
      case 'position':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(positionData.year.all, newData)
          } else {
            Object.assign(positionData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            Object.assign(positionData.month.all, newData)
          } else {
            Object.assign(positionData.month.college, newData)
          }
        }
        break
      case 'salary':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(salaryData.year.all, newData)
          } else {
            Object.assign(salaryData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            Object.assign(salaryData.month.all, newData)
          } else {
            Object.assign(salaryData.month.college, newData)
          }
        }
        break
      case 'education':
        if (type === 'year') {
          if (scope === 'all') {
            Object.assign(educationData.year.all, newData)
          } else {
            Object.assign(educationData.year.college, newData)
          }
        } else {
          if (scope === 'all') {
            Object.assign(educationData.month.all, newData)
          } else {
            Object.assign(educationData.month.college, newData)
          }
        }
        break
    }
  }
}

// 创建数据管理器实例
export const dataManager = new VocationalEducationDataManager()

// 导出所有数据类型
export type {
  TotalData,
  CompanyData,
  PersonData,
  ProfessionData,
  PositionData,
  SalaryData,
  EducationData,
}

// 导出所有数据
export {
  totalData,
  companyData,
  personData,
  professionData,
  positionData,
  salaryData,
  educationData,
}

export default dataManager
