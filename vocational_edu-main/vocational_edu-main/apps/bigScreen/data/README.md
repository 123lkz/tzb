# 职业教育大数据展示系统 - 数据结构说明

## 概述

本系统维护四组核心数据，每组数据都包含年度和月度两个维度，以及全口径和应届大专生两个统计范围。

## 四组数据结构

### 1. 数据维度

- **年度数据 (year)**: 按年度统计的汇总数据
- **月度数据 (month)**: 按月度统计的详细数据

### 2. 统计范围

- **全口径 (all)**: 包含所有招聘数据的统计
- **应届大专生 (freshGraduateJuniorCollege)**: 专门针对应届大专生的统计

## 数据分类

### 1. 总览数据 (`/index/`)

- **total.ts**: 总览数据，包含招聘职位数量、需求人数、单位数量、薪资分位数等
- **recruitingCompanyTotal.ts**: 招聘单位总数量数据
- **recruitingPersonTotal.ts**: 招聘需求总人数数据
- **recruitingProfessionTotal.ts**: 招聘职位总个数数据

### 2. 职位信息数据 (`/position/`)

- **index.ts**: 职位相关信息，包含：
  - 省份地图数据
  - 招聘总人数排行（按省份）
  - 招聘总人数职业排行
  - 招聘总人数行业排行
  - 热门职业对应专业词云图
  - 招聘单位/公司规模
  - 工作岗位经验要求
  - 工作岗位学历要求

### 3. 薪酬信息数据 (`/salary/`)

- **index.ts**: 薪酬相关信息，包含：
  - 全国薪资中位数
  - 薪酬省份地图数据
  - 薪资中位数排行（按省份）
  - 薪资中位数职业排行
  - 薪资中位数行业排行
  - 高薪职业对应专业词云图
  - 招聘单位/公司规模
  - 工作岗位经验要求
  - 工作岗位学历要求

### 4. 教育供给数据 (`/education/`)

- **index.ts**: 教育相关信息，包含：
  - 大专职业院校在校人数省份地图数据
  - 各省大专职业院校数排行
  - 大专专业学生数排行
  - 双高/非双高学校数量
  - 双高/非双高院校在校生数
  - 总毕业生（最近 5 年）

## 数据管理工具

### 数据管理器 (`/index.ts`)

提供了统一的数据管理接口：

```typescript
import dataManager from './data/index'

// 获取年度全口径总览数据
const yearlyAllTotalData = dataManager.getTotalData('year', 'all')

// 获取月度应届大专生职位数据
const monthlyFreshPositionData = dataManager.getPositionData('month', 'freshGraduateJuniorCollege')

// 获取所有数据
const allData = dataManager.getAllData('year', 'all')
```

### 主要方法

- `getTotalData(type, scope)`: 获取总览数据
- `getCompanyData(type, scope)`: 获取招聘单位总数量据
- `getPersonData(type, scope)`: 获取招聘总人数数据
- `getProfessionData(type, scope)`: 获取招聘职业数据
- `getPositionData(type, scope)`: 获取职位信息数据
- `getSalaryData(type, scope)`: 获取薪酬信息数据
- `getEducationData(type, scope)`: 获取教育供给数据
- `getAllData(type, scope)`: 获取所有数据
- `updateData(category, type, scope, newData)`: 更新数据

## 数据类型

### 参数类型

- `type`: 'year' | 'month' - 数据维度
- `scope`: 'all' | 'freshGraduateJuniorCollege' - 统计范围

### 数据接口

每个数据文件都导出了相应的 TypeScript 接口，确保类型安全。

## 使用示例

```typescript
// 在Vue组件中使用
import { dataManager } from '~/data'

export default {
  setup() {
    // 获取当前筛选条件下的数据
    const getCurrentData = (
      dateType: 'year' | 'month',
      scopeType: 'all' | 'freshGraduateJuniorCollege'
    ) => {
      return {
        total: dataManager.getTotalData(dateType, scopeType),
        position: dataManager.getPositionData(dateType, scopeType),
        salary: dataManager.getSalaryData(dateType, scopeType),
        education: dataManager.getEducationData(dateType, scopeType),
      }
    }

    return {
      getCurrentData,
    }
  },
}
```

## 数据更新

系统支持动态更新数据，可以通过`updateData`方法更新特定类别的数据：

```typescript
// 更新年度全口径总览数据
dataManager.updateData('total', 'year', 'all', newTotalData)

// 更新月度应届大专生职位数据
dataManager.updateData('position', 'month', 'freshGraduateJuniorCollege', newPositionData)
```

## 注意事项

1. 所有数据都采用 TypeScript 接口定义，确保类型安全
2. 月度数据通常包含 12 个月的数据数组
3. 年度数据包含汇总统计和同比增长率
4. 数据更新会直接修改内存中的数据，如需持久化请配合后端 API
5. 建议在开发环境中使用示例数据，生产环境中替换为真实数据
