interface Professions {
  name: string
  value: number
}

interface HotWordsData {
  name: string
  professions: Professions[]
  value: number
}

/**
 * 合并的去重和格式化数据方法
 * 1. 去重：比较 name 和 professionName 数组内容是否相同
 * 2. 保证 name 的值是唯一的
 * 3. professionName 只保留前三个值
 * 4. 如果 name 相同且 professionName 前三个值相同，合并并累加 value
 * 5. 计算每个 name 下所有 professions 的 value 总和
 * 6. 按照总 value 进行排序
 * 7. 最后数组只取前50个
 */
export const processHotWordsData = (arr: HotWordsData[]) => {
  if (!arr || arr.length === 0) return []

  // 第一步：去重
  const deduplicatedData = arr.filter((item, index, self) => {
    return (
      index ===
      self.findIndex(t => {
        // 比较 name
        if (t.name !== item.name) return false

        // 比较 professionName 数组
        if (!Array.isArray(t.professionName) || !Array.isArray(item.professionName)) {
          return t.professionName === item.professionName
        }

        // 数组长度不同
        if (t.professionName.length !== item.professionName.length) return false

        // 比较数组内容
        return t.professionName.every((prof, idx) => prof === item.professionName[idx])
      })
    )
  })

  // 第二步：按 name 分组并格式化
  const groupedData = deduplicatedData.reduce(
    (
      acc: Record<string, { name: string; professions: { name: string; value: number }[] }>,
      item: HotWordsData
    ) => {
      if (!acc[item.name]) {
        acc[item.name] = {
          name: item.name,
          professions: [],
        }
      }

      // 只保留 professionName 的前三个值
      const professionNameFirstThree = item.professionName.slice(0, 3)
      const professionPath = professionNameFirstThree.join(' > ')

      // 检查是否已存在相同的职业路径
      const existingProfession = acc[item.name].professions.find(p => p.name === professionPath)

      if (existingProfession) {
        // 如果已存在，累加 value
        existingProfession.value += item.value
      } else {
        // 如果不存在，添加新的职业
        acc[item.name].professions.push({
          name: professionPath,
          value: item.value,
        })
      }

      return acc
    },
    {}
  )

  // 第三步：转换为数组格式并计算总 value
  const formattedArray = Object.values(groupedData).map(item => {
    // 计算所有 professions 的 value 总和
    const totalValue = item.professions.reduce((sum, profession) => sum + profession.value, 0)

    return {
      ...item,
      value: totalValue, // 在顶层添加总 value
    }
  })

  // 第四步：按照总 value 进行降序排序
  const sortedArray = formattedArray.sort((a, b) => b.value - a.value)

  // 第五步：只取前50个
  return sortedArray.slice(0, 30)
}
