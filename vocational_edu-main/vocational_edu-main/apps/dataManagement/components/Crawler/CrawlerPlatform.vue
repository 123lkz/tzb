<script setup lang="ts">
// import dayjs from 'dayjs'
import FifthTitle from '../common/Title/FifthTitle.vue'
import Card from '../common/Card.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import LineBarDualAxisChart from '../Echart/LineBarDualAxisChart.vue'
import Icon from '../common/Icon.vue'
import { useNumberAnimation } from '~/composables/useNumberAnimation'

const props = withDefaults(
  defineProps<{
    isCleaned: boolean
    time: string
  }>(),
  {
    isCleaned: false,
    time: 'month',
  }
)

const comparedTitle = computed(() => {
  return comparedMap[props.time]
})

// 定义平台颜色配置
const platformColors = [
  { left: '#00ffff' }, // BOSS直聘 - 青色
  { left: '#ffa500' }, // 智联招聘 - 橙色
  { left: '#27ae60' }, // 58同城 - 绿色
  { left: '#a9a9b3' }, // 前程无忧 - 偏灰紫色
  { left: '#a9a9b3' }, // 拉勾网 - 偏灰紫色
  { left: '#a9a9b3' }, // 猎聘网 - 偏灰紫色
]

const data = ref([
  {
    name: 'BOSS直聘',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 1752436 },
          { name: '单位总个数', value: 73000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 1825436 },
          { name: '单位总个数', value: 73000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 1889436 },
          { name: '单位总个数', value: 64000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 1979436 },
          { name: '单位总个数', value: 90000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 2049436 },
          { name: '单位总个数', value: 70000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 2129436 },
          { name: '单位总个数', value: 80000 },
        ],
      },
    ],
  },
  {
    name: '智联招聘',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 2142523 },
          { name: '单位总个数', value: 65000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 2292523 },
          { name: '单位总个数', value: 67000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 2492523 },
          { name: '单位总个数', value: 69000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 2592523 },
          { name: '单位总个数', value: 71000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 2842523 },
          { name: '单位总个数', value: 73000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 2992523 },
          { name: '单位总个数', value: 75000 },
        ],
      },
    ],
  },
  {
    name: '58同城',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 187629 },
          { name: '单位总个数', value: 12000 },
        ],
      },
    ],
  },
  {
    name: '前程无忧',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 22200 },
          { name: '单位总个数', value: 3000 },
        ],
      },
    ],
  },
  {
    name: '拉勾网',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 87843 },
          { name: '单位总个数', value: 8000 },
        ],
      },
    ],
  },
  {
    name: '猎聘网',
    values: [
      {
        name: '第35周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
      {
        name: '第36周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
      {
        name: '第37周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
      {
        name: '第38周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
      {
        name: '第39周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
      {
        name: '第40周',
        values: [
          { name: '职位总个数', value: 3796507 },
          { name: '单位总个数', value: 50000 },
        ],
      },
    ],
  },
])

const formattedData = computed(() => {
  return data.value.map(item => {
    // 获取最后一周和倒数第二周的数据
    const len = item.values.length
    const last = item.values[len - 1]
    const prev = item.values[len - 2] || last

    // 获取职位总个数
    const lastPosition = last.values.find(v => v.name === '职位总个数')?.value ?? 0
    const prevPosition = prev.values.find(v => v.name === '职位总个数')?.value ?? 0
    // 获取单位总个数
    const lastCompany = last.values.find(v => v.name === '单位总个数')?.value ?? 0
    const prevCompany = prev.values.find(v => v.name === '单位总个数')?.value ?? 0

    return {
      ...item,
      value: lastPosition, // 这里保留原有的value逻辑（如需调整可修改）
      increaseCount: lastPosition - prevPosition, // 这里保留原有的increaseCount逻辑（如需调整可修改）
      position: {
        value: lastPosition,
        increaseCount: lastPosition - prevPosition,
      },
      company: {
        value: lastCompany,
        increaseCount: lastCompany - prevCompany,
      },
      data: item.values,
    }
  })
})

// 为每个平台创建动画实例
const animationInstances = data.value.map(() => {
  const { animatedValue, formattedValue, animateNumber } = useNumberAnimation()
  return { animatedValue, formattedValue, animateNumber }
})

// 为增长数量创建动画实例
const increaseAnimationInstances = data.value.map(() => {
  const { animatedValue, formattedValue, animateNumber } = useNumberAnimation()
  return { animatedValue, formattedValue, animateNumber }
})

// 启动动画
const startAnimations = () => {
  formattedData.value.forEach((item, index) => {
    // 延迟启动每个动画，创造错落有致的效果
    setTimeout(() => {
      animationInstances[index].animateNumber(item.value, 1000)
      if (item.increaseCount > 0) {
        increaseAnimationInstances[index].animateNumber(item.increaseCount, 800, true)
      }
    }, index * 150)
  })
}

// 组件挂载时启动动画
onMounted(() => {
  startAnimations()
})

// 监听数据变化重新启动动画
watch(
  () => formattedData.value,
  () => {
    startAnimations()
  },
  { deep: true }
)
</script>

<template>
  <div class="mt-8">
    <FifthTitle title="招聘平台和爬取数据" icon="icon-gangwei2" :icon-size="14" size="md" />
    <div class="grid grid-cols-3 gap-6 mt-4">
      <Card
        v-for="(item, index) in formattedData"
        :key="item.name"
        :title="item.name"
        :value="item.value"
      >
        <FirstTitle :title="item.name" class="mb-4" />
        <div class="flex w-full flex-col">
          <div class="grid grid-cols-2 gap-4 w-full">
            <!-- 职位总个数卡片 -->
            <div
              class="flex flex-col rounded-lg p-4 bg-gradient-to-br from-cyan-900/30 to-cyan-400/10 shadow-lg"
            >
              <div class="flex items-center mb-2 gap-1">
                <Icon name="icon-zhiye" color="text-cyan-400" class="-ml-1" />
                <span class="text-sm font-semibold text-cyan-200">职位总个数</span>
              </div>
              <div class="flex items-baseline gap-1 mb-1">
                <span class="font-DIN-Medium text-lg text-cyan-300">{{ item.position.value }}</span>
                <span class="text-sm text-cyan-100">个</span>
              </div>
              <div class="flex items-baseline">
                <span class="text-xs text-cyan-100">{{
                  comparedTitle + (item.position.increaseCount > 0 ? '' : '无变化')
                }}</span>
                <div
                  v-if="item.position.increaseCount > 0"
                  class="flex items-baseline text-sm ml-1"
                >
                  <span class="text-base text-green-400">+</span>
                  <span class="font-DIN-Medium text-green-400">
                    {{ item.position.increaseCount }}
                  </span>
                  <span class="text-xs text-cyan-100 ml-1">个</span>
                </div>
              </div>
            </div>
            <!-- 单位总个数卡片 -->
            <div
              class="flex flex-col rounded-lg p-4 bg-gradient-to-br from-amber-900/30 to-amber-400/10 shadow-lg"
            >
              <div class="flex items-center mb-2 gap-1">
                <Icon name="icon-gongsi" color="text-amber-400" />
                <span class="text-sm font-semibold text-amber-200">单位总个数</span>
              </div>
              <div class="flex items-baseline gap-1 mb-1">
                <span class="font-DIN-Medium text-lg text-amber-300">{{ item.company.value }}</span>
                <span class="text-sm text-amber-100">个</span>
              </div>
              <div class="flex items-baseline">
                <span class="text-xs text-amber-100">{{
                  comparedTitle + (item.company.increaseCount > 0 ? '' : '无变化')
                }}</span>
                <div v-if="item.company.increaseCount > 0" class="flex items-baseline text-sm ml-1">
                  <span class="text-base text-green-400">+</span>
                  <span class="font-DIN-Medium text-green-400">
                    {{ item.company.increaseCount }}
                  </span>
                  <span class="text-xs text-amber-100 ml-1">个</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex-1 w-full min-h-0 mb-2 mt-6">
            <LineBarDualAxisChart
              :data="item.data"
              left-unit="万"
              left-quantifier="个"
              right-unit=""
              right-quantifier="家"
              :left-color="platformColors[index]?.left || '#00ffff'"
              :right-color="platformColors[index]?.right || '#AAD8E8'"
              is-smooth-line
              tooltip-title="招聘平台和爬取数据"
              height="240px"
              :x-axis-label-rotate="data.length < 11 ? 0 : 30"
              :grid="{
                top: '30%',
              }"
              :legend="{
                top: '0%',
              }"
            />
          </div>

          <div class="border-b border-[#00ffff]/20 mb-2"></div>

          <div class="flex items-center justify-between h-6">
            <span class="text-xs text-gray-300">更新时间</span>
            <span class="text-xs text-gray-300">{{ new Date().toLocaleDateString('zh-CN') }}</span>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>
