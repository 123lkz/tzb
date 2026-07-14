<script setup lang="ts">
import * as echarts from 'echarts'
import { registerChinaMap } from '~/utils/echartsMap'
import { formatLargeNumber } from '~/utils/num'

const props = defineProps<{
  type?: 'position' | 'salary' | 'education'
  data: Array<{ name: string; value: number; rank: number; positionCount?: number; totalCompanies?: number }>
  theme?: object
  highlightProvince?: string // 新增高亮省份
  maxProvince?: string // 新增：最大值省份
  circleProvinces?: string[] // 新增：需要圆圈标注的省份
  circleSize?: number // 圆圈大小
  beijingHighlightColor?: string
  unit?: string
  unitOfAccount?: string
  quantifier?: string
}>()

const emit = defineEmits(['province-click', 'province-hover', 'province-mouseout'])

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  registerChinaMap() // 注册地图数据
  chart = echarts.init(chartRef.value)
  chart.on('click', (params: any) => {
    if (params.componentType === 'series' && params.seriesType === 'map') {
      emit('province-click', params.name)
    }
  })
  // 添加鼠标移入移出事件
  chart.on('mouseover', (params: any) => {
    if (params.componentType === 'series' && params.seriesType === 'map') {
      emit('province-hover', params.name)
    }
  })
  chart.on('mouseout', (params: any) => {
    if (params.componentType === 'series' && params.seriesType === 'map') {
      emit('province-mouseout', params.name)
    }
  })
  updateChart()
}

const positionTooltip = (data: any) => {
  // 根据数值大小选择合适的格式化方式
  const formatValue = (value: number) => {
    if (value >= 10000) {
      return (value / 10000).toFixed(2) + '万人'
    }
    return value.toFixed(0) + '人'
  }

  return `
          <div style="font-weight:bold;font-size:14px;margin-bottom:6px;">${
            data.name + (data.dateText || '') + '数据'
          }</div>
          <div style="padding-left:4px;font-size:12px;margin:0;display:flex;flex-direction:column;gap:4px;">
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#91CC75;border-radius:50%;"></span>
              <span style="margin:0 4px;">招聘总人数排名:</span>
              <span style="color: #000; font-weight:bold;">${data.rank}</span>
            </div>
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#FEC857;border-radius:50%;"></span>
              <span style="margin:0 4px;">招聘总人数:</span>
              <span style="color: #000; font-weight:bold;">
              ${formatValue(data.value)}</span>
            </div>
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#EE6666;border-radius:50%;"></span>
              <span style="margin:0 4px;">招聘单位总数量:</span>
              <span style="color: #000; font-weight:bold;" >${data.totalCompanies || '-'}家</span>
            </div>
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#5371C6;border-radius:50%;"></span>
              <span style="margin:0 4px;">招聘职位总个数:</span>
              <span style="color: #000; font-weight:bold;">${data.positionCount || '-'}个</span>
            </div>
          </div>
        `
}

const salaryTooltip = (data: any) => {
  return `
          <div style="font-weight:bold;font-size:14px;margin-bottom:6px;">${
            data.name + (data.dateText || '') + '薪酬数据'
          }</div>
          <div style="padding-left:4px;font-size:12px;margin:0;display:flex;flex-direction:column;gap:4px;">
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#91CC75;border-radius:50%;"></span>
              <span style="margin:0 4px;">薪资中位数排名:</span>
              <span style="color: #000; font-weight:bold;">${data.rank}</span>
            </div>
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#FEC857;border-radius:50%;"></span>
              <span style="margin:0 4px;">薪资中位数:</span>
              <span style="color: #000; font-weight:bold;">
              ${data.value}元</span>
            </div>
            <div style="display:flex;align-items:center;">
              <span style="display:inline-block;width:6px;height:6px;background-color:#EE6666;border-radius:50%;"></span>
              <span style="margin-left:4px;font-weight:bold; color: ${
                data.percent > 0 ? '#00C62F' : data.percent < 0 ? '#EE2222' : '#000'
              };">${data.percent > 0 ? '高于' : data.percent < 0 ? '低于' : '与'}</span>
              <span style="margin-right:2px;">全国薪资中位数</span>
              <span style="color: ${
                data.percent > 0 ? '#00C62F' : data.percent < 0 ? '#EE2222' : '#000'
              };font-weight:bold;" >${data.percent != 0 ? Math.abs(data.percent) + '%' : '持平'}</span>
            </div>
          </div>
        `
}

const educationTooltip = (data: any) => {
  return `
    <div style="font-weight:bold;font-size:14px;margin-bottom:6px;">${data.name + (data.dateText || '') + '数据'}</div>
    <div style="padding-left:4px;font-size:12px;margin:0;display:flex;flex-direction:column;gap:4px;">
      <div style="display:flex;align-items:center;">
        <span style="display:inline-block;width:6px;height:6px;background-color:#91CC75;border-radius:50%;"></span>
        <span style="margin:0 4px;">大专职业院校学生数排名:</span>
        <span style="color: #000; font-weight:bold;">${data.rank}</span>
      </div>
      <div style="display:flex;align-items:center;">
        <span style="display:inline-block;width:6px;height:6px;background-color:#EE6665;border-radius:50%;"></span>
        <span style="margin:0 4px;">大专职业院校学生数:</span>
        <span style="color: #000; font-weight:bold;">
        ${formatLargeNumber(data.value)}人</span>
      </div>
      <div style="display:flex;align-items:center;">
        <span style="display:inline-block;width:6px;height:6px;background-color:#FEC857;border-radius:50%;"></span>
        <span style="margin:0 4px;">大专职业院校总数:</span>
        <span style="color: #000; font-weight:bold;">
        ${formatLargeNumber(data.juniorCollegesValue)}所</span>
      </div>
      <div style="display:flex;align-items:center;">
        <span style="display:inline-block;width:6px;height:6px;background-color:#5370C6;border-radius:50%;"></span>
        <span style="margin:0 4px;">双高院校总数:</span>
        <span style="color: #000; font-weight:bold;">
        ${formatLargeNumber(data.doubleHighValue)}所</span>
      </div>
    </div>
    `
}

// 更新图表配置
const updateChart = () => {
  if (!chart) return

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        // 处理地图区域的 tooltip
        if (params.seriesType === 'map') {
          const data = params.data
          const provinceName = params.name

          // 检查是否有有效的数据（value 不为 0 或存在其他业务数据）
          const hasValidData =
            data &&
            ((data.value && data.value > 0) ||
              data.company !== undefined ||
              data.job !== undefined ||
              data.percent !== undefined ||
              data.total !== undefined ||
              data.doubleHigh !== undefined)

          if (hasValidData) {
            // 如果有有效数据，使用对应的 tooltip 函数
            return props.type === 'position'
              ? positionTooltip(data)
              : props.type === 'salary'
              ? salaryTooltip(data)
              : educationTooltip(data)
          }
          // 如果没有有效数据，显示默认的省份信息
          return `
              <div style="font-weight:bold;font-size:14px;margin-bottom:6px;">${provinceName}数据</div>
              <div style="padding-left:4px;font-size:12px;margin:0;display:flex;flex-direction:column;gap:4px;">
                <div style="display:flex;align-items:center;">
                  <span style="display:inline-block;width:6px;height:6px;background-color:#91CC75;border-radius:50%;"></span>
                  <span style="margin:0 4px;">暂无数据</span>
                </div>
              </div>
            `
        }

        return ''
      }
    },
    visualMap: {
      type: 'piecewise',
      pieces: legendIntervals.value.map((interval) => ({
        min: interval.min, // 这里是元
        max: interval.max, // 这里是元
        color: interval.color,
        label: interval.label
      })),
      left: 50,
      bottom: 150,
      show: false, // 只需将这里设为 false
      orient: 'vertical',
      textStyle: {
        color: '#fff'
      }
    },
    geo: {
      map: 'china',
      roam: false,
      zoom: 1.2,
      center: [104, 32],
      aspectScale: 0.8,
      scaleLimit: {
        min: 1,
        max: 3
      },
      itemStyle: {
        areaColor: '#CDE9F3',
        borderColor: 'rgba(255, 255, 255, 0.8)',
        borderWidth: 0.5
      },
      emphasis: {
        label: {
          show: true,
          color: '#FFF',
          fontSize: 12,
          fontWeight: 'bold'
        },
        itemStyle: {
          borderColor: 'rgba(255, 255, 255, 0.8)',
          borderWidth: 0.5
        }
      },
      zlevel: 1,
      regions: [
        {
          name: '北京',
          itemStyle: {
            areaColor: props.beijingHighlightColor || undefined
          },
          label: {
            show: false // 可选：是否显示标签
          }
        },
        {
          name: '南海',
          itemStyle: {
            areaColor: '#e0f3f8'
          },
          label: {
            show: false // 可选：是否显示标签
          }
        }
      ]
    },
    series: [
      {
        name: '中国地图',
        type: 'map',
        map: 'china',
        roam: false,
        zoom: 1.2,
        center: [104, 32],
        aspectScale: 0.8,
        scaleLimit: {
          min: 1,
          max: 3
        },
        selectedMode: false, // 禁用点击选中
        label: {
          show: true, // 关键：显示省份名称
          color: '#FFF', // 文字颜色
          fontSize: 9,
          formatter: function (params) {
            return getProvinceSimpleName(params.name)
          }
        },
        emphasis: {
          label: {
            show: true,
            color: '#FFF',
            fontSize: 12,
            fontWeight: 'bold'
          },
          itemStyle: {
            areaColor: '#FCB45D',
            borderColor: 'rgba(255, 255, 255, 0.8)',
            borderWidth: 0.5
          }
        },
        data: mapData.value,
        itemStyle: {
          areaColor: '#CDE9F3',
          borderColor: 'rgba(255, 255, 255, 0.8)',
          borderWidth: 0.5
        },
        zlevel: 1, // 地图层级
        silent: false // 确保可以触发事件
      }
    ]
  }

  // 确保地图加载完成后再设置散点数据
  chart.on('mapRegionUpdated', () => {
    const geoComponent = chart.getModel().getComponent('geo')
    if (geoComponent) {
      const geoModel = geoComponent.getModel()
      const geoMapData = geoModel.get('map')

      // 更新散点数据
      const updatedCapitalCities = props.data
        .map((item) => {
          const region = geoMapData.features.find((f: any) => f.properties.name === item.name)
          if (region && region.properties.center) {
            return {
              ...item,
              value: region.properties.center
            }
          }
          return item
        })
        .filter((item) => item.value[0] !== 0 && item.value[1] !== 0)

      // 更新散点数据
      chart.setOption(
        {
          series: [
            {
              name: '省会城市',
              data: updatedCapitalCities
            }
          ]
        },
        {
          replaceMerge: ['series']
        }
      )
    }
  })

  chart.setOption(option)

  // 单独高亮hover/click省份
  if (props.highlightProvince) {
    chart.dispatchAction({
      type: 'highlight',
      seriesIndex: 0,
      name: props.highlightProvince
    })
    chart.dispatchAction({
      type: 'showTip',
      seriesIndex: 0,
      name: props.highlightProvince
    })
  }
}

const useWan = computed(() => {
  return props.unitOfAccount === '万'
})

// 动态生成区间
function formatIntervalLabel(min: number, max: number, useWan: boolean) {
  return `${formatLargeNumber(min)} - ${formatLargeNumber(max)}`
}

// @ts-ignore
const legendIntervals = computed(() => {
  const values = props.data.map((d: any) => d.value).filter((v: any) => typeof v === 'number')
  if (!values.length) return []
  const min = Math.min(...values)
  const max = Math.max(...values)
  const useWan = props.unitOfAccount === '万'

  if (min === max) {
    return [
      {
        min,
        max,
        color: '#313695',
        label: formatIntervalLabel(min, max, useWan)
      }
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
    }
    return sorted[base]
  }
  const quantiles = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1].map(getQuantile)
  const colors = ['#04D4FF', '#06AAE6', '#0D86CC', '#0F67B3', '#124D99', '#133880', '#122666', '#10184D']
  const intervals = []
  for (let i = 0; i < 8; i++) {
    const minVal = Math.round(quantiles[i] / 100) * 100
    const maxVal = i === 7 ? max : Math.round(quantiles[i + 1] / 100) * 100
    intervals.push({
      min: minVal,
      max: maxVal,
      color: colors[i],
      label: formatIntervalLabel(minVal, maxVal, useWan)
    })
  }
  return intervals.reverse()
})

// 确保所有省份都有数据，即使原始数据中没有的省份也要包含
const mapData = computed(() => {
  // 创建数据映射，直接使用原始名称
  const dataMap = new Map()
  props.data.forEach((item) => {
    dataMap.set(item.name, item)
  })

  // 所有省份名称列表
  const allProvinces = Object.keys(provinceCoords)

  const result = allProvinces.map((provinceName) => {
    const existingData = dataMap.get(provinceName)
    if (existingData) {
      return existingData
    }
    // 为没有数据的省份创建默认数据
    return {
      name: provinceName,
      value: 0, // 默认值为0
      rank: 0 // 默认分组为0
    }
  })

  return result
})

const provinceCoords: Record<string, { center: [number, number]; capital: [number, number] }> = {
  北京市: { center: [116.405285, 39.904989], capital: [116.405285, 39.904989] },
  天津市: { center: [117.2, 39.13], capital: [117.190182, 39.125596] },
  河北省: { center: [114.52, 38.05], capital: [114.502461, 38.045474] },
  山西省: { center: [112.53, 37.87], capital: [112.549248, 37.857014] },
  内蒙古自治区: { center: [111.65, 40.82], capital: [111.670801, 40.818311] },
  辽宁省: { center: [123.38, 41.8], capital: [123.429096, 41.796767] },
  吉林省: { center: [125.35, 43.88], capital: [125.3245, 43.886841] },
  黑龙江省: { center: [126.63, 45.75], capital: [126.642464, 45.756967] },
  上海市: { center: [121.48, 31.22], capital: [121.472644, 31.231706] },
  江苏省: { center: [118.78, 32.04], capital: [118.767413, 32.041544] },
  浙江省: { center: [120.19, 30.26], capital: [120.153576, 30.287459] },
  安徽省: { center: [117.27, 31.86], capital: [117.283042, 31.86119] },
  福建省: { center: [119.3, 26.08], capital: [119.306239, 26.075302] },
  江西省: { center: [115.89, 28.68], capital: [115.892151, 28.676493] },
  山东省: { center: [117.0, 36.65], capital: [117.000923, 36.675807] },
  河南省: { center: [113.65, 34.76], capital: [113.665412, 34.757975] },
  湖北省: { center: [114.31, 30.52], capital: [114.298572, 30.584355] },
  湖南省: { center: [112.94, 28.23], capital: [112.982279, 28.19409] },
  广东省: { center: [113.23, 23.16], capital: [113.280637, 23.125178] },
  广西壮族自治区: { center: [108.33, 22.84], capital: [108.320004, 22.82402] },
  海南省: { center: [110.35, 20.02], capital: [110.33119, 20.031971] },
  重庆市: { center: [106.54, 29.59], capital: [106.504962, 29.533155] },
  四川省: { center: [104.06, 30.67], capital: [104.065735, 30.659462] },
  贵州省: { center: [106.71, 26.57], capital: [106.713478, 26.578343] },
  云南省: { center: [102.73, 25.04], capital: [102.712251, 25.040609] },
  西藏自治区: { center: [91.11, 29.97], capital: [91.132212, 29.660361] },
  陕西省: { center: [108.95, 34.27], capital: [108.948024, 34.263161] },
  甘肃省: { center: [103.73, 36.03], capital: [103.823557, 36.058039] },
  青海省: { center: [101.74, 36.56], capital: [101.778916, 36.623178] },
  宁夏回族自治区: { center: [106.27, 38.47], capital: [106.278179, 38.46637] },
  新疆维吾尔自治区: { center: [87.68, 43.77], capital: [87.617733, 43.792818] },
  台湾省: { center: [121.5, 25.05], capital: [121.509062, 25.044332] },
  香港特别行政区: { center: [114.17, 22.28], capital: [114.173355, 22.320048] },
  澳门特别行政区: { center: [113.54, 22.19], capital: [113.54909, 22.198951] }
}

// 导入省份名称工具函数
import { getProvinceSimpleName } from '~/utils/name'

// 响应窗口变化
const handleResize = () => {
  chart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.off('click')
  chart?.dispose()
})

watch(() => props.data, updateChart, { deep: true })
watch(() => props.highlightProvince, updateChart)

defineExpose({ legendIntervals })
</script>

<template>
  <div class="relative h-[700px] animate-mapfadein">
    <div ref="chartRef" class="w-full h-[700px]" />
    <div class="absolute bottom-10 left-1/4 z-20">
      <div class="shadow-[inset_0_0_10px_rgba(0,255,255,0.2)] backdrop-blur-sm rounded-lg p-3 border border-white/20">
        <div class="text-xs px-1 mb-2 text-gray-400">单位：{{ props.quantifier }}</div>
        <div class="space-y-1">
          <!-- @ts-ignore -->
          <template v-for="(interval, idx) in legendIntervals" :key="idx">
            <div
              v-if="interval.min && interval.max && interval.min !== interval.max"
              class="flex items-center space-x-2 opacity-0 animate-fadein"
              :style="{ animationDelay: idx * 80 + 'ms', animationFillMode: 'forwards' }"
            >
              <div class="w-3 h-3 rounded-sm" :style="{ backgroundColor: interval.color }"></div>
              <span class="text-white text-xs">{{ interval.label }}</span>
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
