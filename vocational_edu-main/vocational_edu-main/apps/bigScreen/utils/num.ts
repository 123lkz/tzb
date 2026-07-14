// console.log(roundToNearestThousand(14520)); // 输出: 15000
// console.log(roundToNearestThousand(1740));  // 输出: 2000
export const roundToThousand = (num: number) => {
  return Math.round(num / 1000) * 1000
}

// console.log(floorToThousand(14520)); // 输出: 14000
// console.log(floorToThousand(1740));  // 输出: 1000
export const floorToThousand = (num: number) => {
  return Math.floor(num / 1000) * 1000
}

// formatNumber(123456) => 123,456
export const formatNumber = (num: number | string) => {
  if (num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  }
  return num
}

/**
 * 格式化大数，超过1万显示为“万”，超过1亿显示为“亿”
 * @param num 数值
 * @returns 格式化后的字符串
 * formatLargeNumber(123456) => 1234
 * formatLargeNumber(1234567890) => 12.35亿
 * formatLargeNumber(1234567890123) => 123.46万亿
 */
export const formatLargeNumber = (num: number | string, fixed: number = 0): string => {
  const n = typeof num === 'string' ? Number(num) : num
  if (isNaN(n)) return String(num)
  if (n >= 1e8) {
    return (n / 1e8).toFixed(fixed).replace(/\.00$/, '') + '亿'
  }
  if (n >= 1e4) {
    return (n / 1e4).toFixed(fixed).replace(/\.00$/, '') + '万'
  }
  return n.toString()
}

/**
 * 计算变化率
 * @param data 数据
 * @returns 变化率
 */
export const generateChangeRateData = (prev: number, current: number) => {
  if (prev === 0) return 0
  const changeRate = ((current - prev) / prev) * 100
  return Math.round(changeRate * 100) / 100
}
