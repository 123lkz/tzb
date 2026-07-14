<template>
  <div :id="chartId" ref="el" :class="className" :style="{ height: height, width: width }" />
</template>

<script lang="ts" setup>
import type { EChartsCoreOption, EChartsType } from 'echarts'
import * as echarts from 'echarts'
import _ from 'lodash'

const props = withDefaults(
  defineProps<{
    className?: string
    width?: string
    height?: string
    options?: EChartsCoreOption
  }>(),
  {
    className: 'chart',
    width: '100%',
    height: '2.5rem',
    options: () => ({}),
  }
)

const chartId = _.uniqueId('echart-')

const chart = ref<EChartsType | null>()
const el = ref<HTMLElement | null>(null)

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  if (chart.value) {
    chart.value.dispose()
  }
  chart.value = null
})

watch(
  () => props.options,
  () => {
    chart.value?.setOption(props.options, true)
  }
)

function initChart() {
  // eslint-disable-next-line
  chart.value = echarts.init(el.value, null, {
    renderer: 'svg',
  })
  chart.value.setOption(props.options, true)
}

defineExpose({
  chart,
})
</script>
