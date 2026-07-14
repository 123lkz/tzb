<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'

interface Professions {
  name: string
  value: number
}

export interface DataItem {
  value: number
  name: string
  professions?: Professions[]
}

const props = withDefaults(
  defineProps<{
    width?: number
    height?: number
    tooltipTitle?: string
    data?: DataItem[]
  }>(),
  {
    tooltipTitle: '热门标准职业',
    width: 300,
    height: 200,
    data: () => [],
  }
)

const chartRef = ref<HTMLDivElement>()
let chartInstance: ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const data = params.data
        return `
          <div>
            <span style="color: #333; font-weight: bold;">${params.name}专业</span>
          </div>
          ${
            data.professions
              ? `<div style="margin: 10px 0;">
                  <div style="margin-bottom: 8px;">对应的三级标准职业和${
                    props.tooltipTitle == '热门标准职业' ? '招聘总人数' : '月薪资中位数'
                  }如下:</div>
                  <div style="display: flex; flex-direction: column; gap: 5px;">
                    ${data.professions
                      .map((profession: Professions) => {
                        return `<div style="display: flex; align-items: center;">
                        <span style="display: inline-block; margin-right: 8px; border-radius: 50%; width: 8px; height: 8px; background-color: ${
                          params.color
                        };"></span>
                        <span style="color: #666; font-weight: bold;">${profession.name}：</span>
                        <span style="color: #666;">
                        ${profession.value}${props.tooltipTitle == '热门标准职业' ? '人' : '元'}
                        </span>
                      </div>`
                      })
                      .join('')}
                  </div>
                </div>`
              : ''
          }
        `
      },
    },
    legend: {
      show: false, // 隐藏图例
    },
    series: [
      {
        type: 'wordCloud',
        gridSize: 14,
        sizeRange: [10, 20],
        rotationRange: [0, 0],
        shape: 'circle',
        width: props.width || '100%',
        height: props.height || '100%',
        left: '0',
        top: '15%',
        drawOutOfBound: false,
        textStyle: {
          color: function () {
            // 使用明亮、浅色的颜色，避免深色
            const colors = [
              '#FF6B6B', // 浅红色
              '#4ECDC4', // 浅青色
              '#45B7D1', // 浅蓝色
              '#96CEB4', // 浅绿色
              '#FFEAA7', // 浅黄色
              '#DDA0DD', // 浅紫色
              '#F8BBD9', // 浅粉色
              '#B2DFDB', // 薄荷绿
              '#FFCC80', // 浅橙色
              '#C8E6C9', // 浅绿色
              '#BBDEFB', // 浅蓝色
              '#E1BEE7', // 浅紫色
              '#FFCDD2', // 浅红色
              '#FFF9C4', // 浅黄色
              '#D1C4E9', // 浅紫色
              '#FF8A80', // 浅红色
              '#FFD180', // 浅橙色
              '#FFAB91', // 浅红色
              '#FFE0B2', // 浅橙色
              '#FFCCBC', // 浅红色
            ]
            return colors[Math.floor(Math.random() * colors.length)]
          },
        },
        emphasis: {
          textStyle: {},
        },
        data: props.data,
      },
    ],
    // 响应式配置
    responsive: true,
    // 动画配置
    animation: true,
    animationDuration: 1000,
    animationEasing: 'cubicInOut',
  }

  chartInstance.setOption(option)
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  chartInstance?.resize()
}

// 监听数据变化
watch(
  () => props.data,
  (newData: DataItem[] | undefined) => {
    if (chartInstance && newData) {
      chartInstance.setOption({
        series: [
          {
            data: newData,
          },
        ],
        legend: {
          data: newData.map((item: DataItem) => item.name),
        },
      })
    }
  },
  { deep: true }
)

onMounted(async () => {
  await import('echarts-wordcloud')
  initChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full"></div>
</template>
