/**
 * 时间处理工具函数
 */

/**
 * 获取当前年份
 */
export function getCurrentYear(): number {
  return new Date().getFullYear()
}

/**
 * 获取上个月的年份和月份
 */
export function getLastMonth(): { year: number; month: number } {
  const now = new Date()
  const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1)
  return {
    year: lastMonth.getFullYear(),
    month: lastMonth.getMonth() + 1
  }
}

/**
 * 获取统计时间信息
 * @param dateType 统计类型：'year' | 'month'
 * @returns 统计时间信息
 */
export function getStatisticalTime(dateType: 'year' | 'month'): {
  year: number
  month?: number
  displayText: string
  apiParams: { year: number; month?: number }
} {
  if (dateType === 'year') {
    const year = getCurrentYear()
    return {
      year,
      displayText: `${year}年`,
      apiParams: { year }
    }
  } else {
    const { year, month } = getLastMonth()
    return {
      year,
      month,
      displayText: `${year}年${month}月`,
      apiParams: { year, month }
    }
  }
}

/**
 * 格式化统计时间显示
 * @param dateType 统计类型
 * @param year 年份
 * @param month 月份（可选）
 * @returns 格式化的显示文本
 */
export function formatStatisticalTime(dateType: 'year' | 'month', year: number, month?: number): string {
  if (dateType === 'year') {
    return `${year}年`
  } else {
    return `${year}年${month}月`
  }
}
