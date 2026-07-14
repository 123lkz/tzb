<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, ref, watch, toRefs } from 'vue'

interface TreeNode {
  name: string
  value?: number
  children?: TreeNode[]
  collapsed?: boolean
  itemStyle?: {
    color?: string
  }
}

const props = defineProps<{
  data: TreeNode
  textColor?: string // 文字颜色
  selectedIndustry?: string // 当前选中的产业名称
}>()

const { data, selectedIndustry } = toRefs(props)
const textColor = props.textColor || '#00ffff'
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts

// 处理数据，为指定层级节点添加颜色
const processData = (data: TreeNode, level: number = 0): TreeNode => {
  const newNode = { ...data }

  // 为第一级分类节点设置颜色
  if (level === 1) {
    newNode.itemStyle = {
      color: textColor,
    }
  }

  if (newNode.children) {
    newNode.children = newNode.children.map(child => processData(child, level + 1))
  }

  return newNode
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  const processedData = processData(data.value)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
      formatter: function (params: any) {
        const { name, treeAncestors } = params
        return `
        <div style="display: flex; flex-direction: column; gap: 5px;">
          <div style="font-size: 16px; font-weight: bold;">${name}</div>
          <div style="font-size: 14px; color: #666;">
            ${treeAncestors
              .map((item: any, idx: number) =>
                idx === 0 || idx === 1 ? item.name : ' > ' + item.name
              )
              .join('')}
          </div>
        </div>
        `
      },
    },
    series: [
      {
        type: 'tree',
        data: [processedData],
        top: 0,
        left: '10%',
        bottom: '5%',
        right: '20%',
        symbolSize: 10,
        label: {
          position: 'bottom',
          verticalAlign: 'middle',
          align: 'center',
          fontSize: 12,
          color: textColor,
          distance: 10, // 增加文字和节点的距离
        },
        leaves: {
          label: {
            position: 'right',
            verticalAlign: 'middle',
            align: 'left',
            fontSize: 9,
          },
        },
        emphasis: {
          focus: 'descendant',
          itemStyle: {
            color: '#ff4d4f', // 悬停颜色
          },
        },
        expandAndCollapse: true,
        animationDuration: 550,
        animationDurationUpdate: 750,
        itemStyle: {
          color: '#d9d9d9', // 默认颜色
          borderColor: '#8c8c8c',
        },
        lineStyle: {
          color: '#8c8c8c',
        },
      },
    ],
  }

  chart.setOption(option)

  // 展开所有节点以显示完整的行业分类
  setTimeout(() => {
    try {
      const nodes = (chart as any)._chartsViews[0]._data.tree._nodes

      // 展开所有节点
      nodes.forEach((node: any) => {
        if (node.depth <= 2) {
          // 展开根节点和第一级分类
          chart.dispatchAction({
            type: 'expandAndCollapse',
            dataIndex: node.dataIndex,
          })
        }
      })
    } catch (error) {
      console.warn('Failed to expand tree nodes:', error)
    }
  }, 500)
}

// 响应式更新
watch(
  [data, selectedIndustry],
  ([newData, newSelectedIndustry]) => {
    if (chart && newData) {
      const processedData = processData(newData)
      chart.setOption({
        series: [
          {
            data: [processedData],
          },
        ],
      })

      // 展开所有节点以显示完整的行业分类
      setTimeout(() => {
        try {
          const nodes = (chart as any)._chartsViews[0]._data.tree._nodes

          // 展开所有节点
          nodes.forEach((node: any) => {
            if (node.depth <= 2) {
              // 展开根节点和第一级分类
              chart.dispatchAction({
                type: 'expandAndCollapse',
                dataIndex: node.dataIndex,
              })
            }
          })
        } catch (error) {
          console.warn('Failed to update tree node states:', error)
        }
      }, 100)
    }
  },
  { deep: true }
)

onMounted(() => {
  initChart()

  // 窗口大小变化时重绘
  window.addEventListener('resize', () => {
    chart?.resize()
  })
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full min-h-[400px]" />
</template>

<style scoped>
/* 可以添加自定义样式 */
</style>
