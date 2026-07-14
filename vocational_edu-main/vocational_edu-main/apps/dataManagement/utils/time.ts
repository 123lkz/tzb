/**
 * 格式化日期，格式为“年-月-日”
 * @param date 日期
 * @returns 格式化后的字符串
 * formatDate('2025') => 2025年
 * formatDate('2025-01') => 2025年1月
 * formatDate('2025-01-01') => 2025年1月1日
 * formatDate('2025-01-01 12:00:00') => 2025年1月1日 12:00:00
 * formatDate('2025.01.01', '.') => 2025年1月1日
 * formatDate('2025/01/01', '/') => 2025年1月1日
 */
export const formatDate = (date: string, separator: string = '-') => {
  // 根据分隔符分割日期
  const parts = date.split(separator)
  const [year, month, day] = parts

  // 默认中文格式
  if (year && month && day) {
    // 处理时间部分
    const timePart = date.includes(' ') ? ` ${date.split(' ')[1]}` : ''
    return `${year}年${parseInt(month)}月${parseInt(day)}日${timePart}`
  } else if (year && month) {
    return `${year}年${parseInt(month)}月`
  } else if (year) {
    return `${year}年`
  }

  return ''
}
