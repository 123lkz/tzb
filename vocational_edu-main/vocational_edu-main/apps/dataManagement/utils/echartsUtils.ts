import * as echarts from 'echarts'

/**
 * 安全的 ECharts 初始化方法
 * 避免 passive event listener 警告
 */
export const safeEchartsInit = (
  element: HTMLElement,
  theme?: string | object,
  opts?: {
    renderer?: 'canvas' | 'svg'
    devicePixelRatio?: number
    useCoarsePointer?: boolean
    useDirtyRect?: boolean
  }
) => {
  // 创建图表实例
  const chart = echarts.init(element, theme, {
    renderer: 'canvas',
    devicePixelRatio: window.devicePixelRatio,
    useCoarsePointer: true,
    useDirtyRect: true,
    ...opts,
  })

  // 设置基础配置以禁用滚轮缩放
  const baseOption: echarts.EChartsOption = {
    // 禁用滚轮缩放，避免 passive 警告
    dataZoom: [],
    // 确保网格配置正确
    grid: {
      containLabel: true,
    },
  }

  // 应用基础配置
  chart.setOption(baseOption, true)

  return chart
}

/**
 * 为 ECharts 选项添加禁用滚轮缩放的配置
 */
export const addNoWheelZoomOption = (option: echarts.EChartsOption): echarts.EChartsOption => {
  return {
    ...option,
    // 禁用滚轮缩放，避免 passive 警告
    dataZoom: [],
  }
}
