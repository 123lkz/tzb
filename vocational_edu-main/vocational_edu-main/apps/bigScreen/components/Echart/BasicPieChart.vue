<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, PieSeriesOption } from 'echarts'
import Modal from '../Modal.vue'

interface PieDataItem {
  value: number
  name: string
  industries?: string[]
}

const props = defineProps<{
  data?: PieDataItem[]
  tooltipTitle?: string
}>()

const emit = defineEmits<{
  (e: 'itemClick', item: PieDataItem): void
}>()

// Modal 相关状态
const showModal = ref(false)
const selectedItem = ref<PieDataItem | null>(null)

// 处理点击事件
const handleItemClick = (item: PieDataItem) => {
  selectedItem.value = item
  showModal.value = true
  emit('itemClick', item)
}

// 关闭 Modal
const closeModal = () => {
  showModal.value = false
  selectedItem.value = null
}

const chartRef = ref<HTMLDivElement>()
let chartInstance: ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value, null, {
    renderer: 'canvas',
    passive: true,
  })

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `
          <div style="font-weight: bold; color: #333; margin-bottom: 8px;">${
            params.name + props.tooltipTitle
          }</div>
          <div style="margin-top: 8px;">
            <div style="color: #666; font-size: 11px; margin-bottom: 4px; font-weight: bold;">
            <span style="display:inline-block;margin-right:8px;border-radius:50%;width:8px;height:8px;background-color:${
              params.color
            };"></span>包含的第一级分类行业:</div>
            <div style="color: #777; font-size: 11px;">
            ${params.data.industries.join('<br/>')}
            </div>
          </div>
        `
      },
    },
    legend: {
      show: false, // 隐藏图例
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '75%',
        center: ['50%', '46%'],
        data: props.data,
        label: {
          show: true,
          position: 'inside', // 让文字显示在扇形内部
          formatter: '{b}', // {b}是名称，{d}%是百分比
          color: '#fff', // 文字颜色
          fontWeight: 'bold',
        },
        labelLine: {
          lineStyle: {
            color: 'rgba(0, 0, 0, 0.3)',
          },
        },
        itemStyle: {
          borderRadius: 5,
          borderColor: '#fff',
          borderWidth: 1,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
          label: {
            fontWeight: 'bold',
          },
        },
      } as PieSeriesOption,
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
  (newData: PieDataItem[] | undefined) => {
    if (chartInstance && newData) {
      chartInstance.setOption({
        series: [
          {
            data: newData,
          },
        ],
        legend: {
          data: newData.map((item: PieDataItem) => item.name),
        },
      })
    }
  },
  { deep: true }
)

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.on('click', (params: any) => {
      handleItemClick(params.data)
    })
  }
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.off('click')
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div ref="chartRef" class="w-full h-full"></div>

  <!-- Modal 组件 -->
  <Modal
    :show="showModal"
    :title="selectedItem?.name || '详细信息'"
    width="700px"
    @close="closeModal"
  >
    <div v-if="selectedItem" class="modal-content-wrapper">
      <div class="item-info">
        <div class="info-row">
          <span class="label">产业名称：</span>
          <span class="value">{{ selectedItem.name }}</span>
        </div>
        <div v-if="selectedItem.industries && selectedItem.industries.length > 0" class="info-row">
          <span class="label">包含标准行业：</span>
          <div class="industries-list">
            <span
              v-for="(industry, index) in selectedItem.industries"
              :key="index"
              class="px-4 py-1 rounded-full text-white text-sm font-medium shadow transition bg-gradient-to-br from-[#00ffff]/30 to-[#00ffff]/60 hover:scale-105"
            >
              {{ industry }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
.modal-content-wrapper {
  color: rgba(255, 255, 255, 0.2);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-row {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  min-width: 90px;
  font-size: 16px;
}

.value {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  font-size: 15px;
  flex: 1;
  line-height: 1.5;
}

.industries-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex: 1;
}
</style>
