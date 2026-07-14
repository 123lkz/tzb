// utils/echartsMap.ts
import * as echarts from 'echarts'
import chinaJSON from '~/data/china.json'

// 注册地图
export const registerChinaMap = () => {
  echarts.registerMap('china', chinaJSON as any)
}

// 获取省份名称列表
export const getProvinceNames = () => {
  return chinaJSON.features.map(f => f.properties.name)
}
