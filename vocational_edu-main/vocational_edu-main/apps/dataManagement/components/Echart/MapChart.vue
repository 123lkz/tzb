<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import chinaMap from '~/data/china.json'
import { getShortProvinceName } from '~/utils/map'

interface PropsType {
  mapName: string
  title?: string
  legendTitle: string
  unit?: string
  quantifier: string
  tooltipFormatter?: (params: any) => string
  data: Array<{ name: string; value: number }>
  enableZoom?: boolean
  zoom?: number
  center?: [string, string]
}

const props = withDefaults(defineProps<PropsType>(), {
  mapName: 'china',
  title: '',
  legendTitle: '',
  unit: '',
  quantifier: '',
  tooltipFormatter: () => '',
  data: () => [],
  enableZoom: false,
  center: () => ['50%', '60%'],
})

const mapRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null
const timer = ref<NodeJS.Timeout | null>(null)
const currentIndex = ref(0)
const tooltipEnabled = ref(true)

function formatIntervalLabel(min: number, max: number, useWan: boolean): string {
  if (useWan) {
    const minWan = Math.round((min / 10000) * 10) / 10
    const maxWan = Math.round((max / 10000) * 10) / 10
    return `${minWan} - ${maxWan}万`
  }
  return `${min} - ${max}`
}

async function getGeoJson(mapName: string) {
  if (mapName === 'china') return chinaMap
  try {
    const geo = await import(`~/data/${mapName}.json`)
    return geo.default
  } catch {
    return chinaMap
  }
}

const startCarousel = () => {
  if (timer.value) clearInterval(timer.value)
  timer.value = setInterval(() => {
    if (!chart) return
    chart.dispatchAction({ type: 'downplay', seriesIndex: 0 })
    chart.dispatchAction({ type: 'highlight', seriesIndex: 0, dataIndex: currentIndex.value })
    chart.dispatchAction({ type: 'showTip', seriesIndex: 0, dataIndex: currentIndex.value })
    currentIndex.value = (currentIndex.value + 1) % (props.data?.length || 1)
  }, 2000)
}

const pauseCarousel = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

function defaultTooltipFormatter(params: any) {
  return `
    <div class="font-bold text-lg text-gray-800">${params.name}</div>
    <div class="flex items-center mt-2">
      <span class="inline-block w-4 h-4 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full mr-2"></span>
      <span class="text-gray-700">招聘总人数：</span>
      <span class="font-bold text-lg text-blue-600">${params.value?.toLocaleString?.() ?? 0}</span>
    </div>
  `
}

const legendIntervals = computed(() => {
  const values = props.data.map((d: any) => d.value).filter((v: any) => typeof v === 'number')
  if (!values.length) return []
  const min = Math.min(...values)
  const max = Math.max(...values)
  const useWan = props.unit === '万'

  if (min === max) {
    return [
      {
        min,
        max: max + '以上',
        color: '#313695',
        label: formatIntervalLabel(min, max, useWan),
      },
    ]
  }

  // 8段分位点
  const sorted = [...values].sort((a, b) => a - b)
  const getQuantile = (q: number) => {
    const pos = (sorted.length - 1) * q
    const base = Math.floor(pos)
    const rest = pos - base
    if (sorted[base + 1] !== undefined) {
      return sorted[base] + rest * (sorted[base + 1] - sorted[base])
    } else {
      return sorted[base]
    }
  }
  const quantiles = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1].map(getQuantile)
  const colors = [
    '#04D4FF',
    '#06AAE6',
    '#0D86CC',
    '#0F67B3',
    '#124D99',
    '#133880',
    '#122666',
    '#10184D',
  ]
  const intervals = []
  for (let i = 0; i < 8; i++) {
    const minVal = Math.round(quantiles[i] / 100) * 100
    const maxVal = i === 7 ? max : Math.round(quantiles[i + 1] / 100) * 100
    intervals.push({
      min: minVal,
      max: maxVal,
      color: colors[i],
      label: formatIntervalLabel(minVal, maxVal, useWan),
    })
  }
  return intervals.reverse()
})

async function renderMap() {
  if (!chart || !props.data) return
  const geoJson = await getGeoJson(props.mapName)
  echarts.registerMap(props.mapName, geoJson as any)
  const option = {
    backgroundColor: 'transparent',
    title: {
      text: props.title || '',
      left: 'center',
      top: 20,
      textStyle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#e2e8f0',
        textShadow: '0 0 10px rgba(56, 189, 248, 0.7)',
      },
    },
    tooltip: tooltipEnabled.value
      ? {
          trigger: 'item',
          formatter: props.tooltipFormatter || defaultTooltipFormatter,
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#38bdf8',
          borderWidth: 1,
          padding: [10, 12],
          textStyle: {
            color: '#333',
            fontSize: 13,
            // 支持文字换行
            overflow: 'break',
            width: 300, // 可根据实际需要调整宽度
            rich: {},
          },
          extraCssText:
            'box-shadow: 0 0 20px rgba(56, 189, 248, 0.5); border-radius: 8px; white-space: wrap; word-break: break-all; max-width: 320px;',
        }
      : { show: false },
    visualMap: {
      type: 'piecewise',
      show: false, // 使用自定义图例
      pieces: legendIntervals.value.map(interval => ({
        min: interval.min,
        max: interval.max,
        color: interval.color,
        label: interval.label,
      })),
      left: '10%',
      bottom: '2%',
      orient: 'vertical',
      textStyle: {
        color: 'rgba(255, 255, 255, 0.7)',
        fontSize: 12,
      },
      borderColor: 'rgba(0, 255, 255, 0.3)',
      borderWidth: 1,
      borderRadius: 8,
      backgroundColor: 'rgba(0, 0, 0, 0.3)',
      padding: 10,
      itemGap: 8,
    },
    series: [
      {
        type: 'map',
        map: props.mapName,
        roam: props.enableZoom,
        zoom: props.zoom,
        center: props.center,
        label: {
          show: true,
          fontSize: 9,
          color: '#fff',
          formatter: (params: any) => {
            return getShortProvinceName(params.name)
          },
        },
        emphasis: {
          label: {
            show: true,
            color: '#fff',
            fontSize: 12,
            fontWeight: 'bold',
          },
          itemStyle: {
            areaColor: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: '#fcd34d' },
                { offset: 1, color: '#f59e0b' },
              ],
            },
            borderColor: '#fcd34d',
            borderWidth: 2,
            shadowColor: 'rgba(251, 191, 36, 0.5)',
            shadowBlur: 20,
          },
        },
        itemStyle: {
          areaColor: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: '#1d4ed8' },
              { offset: 1, color: '#0c4a6e' },
            ],
          },
          borderColor: '#1e40af',
          borderWidth: 1,
        },
        data: props.data,
      },
    ],
  }
  chart.setOption(option, true) // 关键：notMerge = true
}

onMounted(() => {
  if (mapRef.value) {
    chart = echarts.init(mapRef.value)
    renderMap()
    startCarousel()
    window.addEventListener('resize', resizeChart)
  }
})

watch([() => props.data, () => props.mapName], () => {
  renderMap()
})

function resizeChart() {
  if (chart) chart.resize()
}

// 根据数值范围高亮对应的省份
function highlightProvincesByRange(min: number, max: number | string) {
  if (!chart) return

  // 先清除所有高亮
  chart.dispatchAction({ type: 'downplay', seriesIndex: 0 })

  // 找到在指定范围内的省份并高亮
  const provincesToHighlight = props.data
    .filter(item => {
      const value = item.value
      if (typeof value === 'number') {
        if (typeof max === 'string' && max.includes('以上')) {
          return value >= min
        }
        if (typeof max === 'number') {
          return value >= min && value <= max
        }
      }
      return false
    })
    .map(item => item.name)

  // 高亮对应的省份
  provincesToHighlight.forEach(provinceName => {
    chart?.dispatchAction({
      type: 'highlight',
      seriesIndex: 0,
      name: provinceName,
    })
  })
}

// 清除所有高亮
function clearHighlight() {
  if (!chart) return
  chart.dispatchAction({ type: 'downplay', seriesIndex: 0 })
}

onBeforeUnmount(() => {
  if (timer.value) clearInterval(timer.value)
  if (chart) {
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', resizeChart)
})
</script>

<template>
  <div
    class="w-full h-full animate-mapfadein relative z-10"
    @mouseenter="pauseCarousel"
    @mouseleave="startCarousel"
  >
    <div ref="mapRef" class="w-full h-full" />
    <div class="absolute bottom-2 left-6 z-20">
      <div
        class="shadow-[inset_0_0_10px_rgba(0,255,255,0.4)] backdrop-blur-sm rounded-lg p-3 border border-white/20"
      >
        <div class="text-xs px-1 mb-3 text-white/80">
          {{ props.legendTitle }}（单位：{{ props.quantifier }}）
        </div>
        <div class="space-y-1">
          <!-- @ts-ignore -->
          <template v-for="(interval, idx) in legendIntervals" :key="idx">
            <div
              v-if="interval.min && interval.max && interval.min !== interval.max"
              class="flex items-center space-x-2 opacity-0 animate-fadein cursor-pointer hover:bg-white/10 rounded transition-colors"
              :style="{ animationDelay: idx * 80 + 'ms', animationFillMode: 'forwards' }"
              @mouseenter="highlightProvincesByRange(interval.min, interval.max)"
              @mouseleave="clearHighlight"
            >
              <div class="w-3 h-3 rounded-sm" :style="{ backgroundColor: interval.color }"></div>
              <span class="text-white/70 text-xs font-DIN-Regular">{{ interval.label }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadein {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fadein {
  animation: fadein 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes mapfadein {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-mapfadein {
  animation: mapfadein 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
