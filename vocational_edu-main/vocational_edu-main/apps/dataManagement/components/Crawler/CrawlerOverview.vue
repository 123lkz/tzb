<script setup lang="ts">
import FifthTitle from '@/components/common/Title/FifthTitle.vue'
import Icon from '@/components/common/Icon.vue'
import { useNumberAnimation } from '@/composables/useNumberAnimation'
import { comparedMap } from '@/utils/constants'

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

const title = computed(() => {
  return props.isCleaned ? '已清洗' : '全部'
})

const data = ref([
  {
    title: '职位(列表)总数量',
    value: 3200000,
    increaseNumber: 25000,
    unit: '个',
    bgColor: 'from-blue-500/15 to-cyan-500/15',
    borderColor: 'border-blue-400/30',
    iconColor: 'text-blue-400',
  },
  {
    title: '职位详情总量',
    value: 1980000,
    increaseNumber: 22000,
    unit: '条',
    bgColor: 'from-purple-500/15 to-violet-500/15',
    borderColor: 'border-purple-400/30',
    iconColor: 'text-purple-400',
  },
  {
    title: '单位总数量',
    value: 156000,
    increaseNumber: 0,
    unit: '家',
    bgColor: 'from-orange-500/15 to-amber-500/15',
    borderColor: 'border-orange-400/30',
    iconColor: 'text-orange-400',
  },
  {
    title: '爬取任务总数',
    value: 3500000,
    increaseNumber: 30000,
    unit: '个',
    bgColor: 'from-pink-500/15 to-rose-500/15',
    borderColor: 'border-pink-400/30',
    iconColor: 'text-pink-400',
  },
])

// 为每个数据项创建动画实例
const animationInstances = data.value.map(() => useNumberAnimation())
const increaseAnimationInstances = data.value.map(() => useNumberAnimation())

// 组件挂载时启动动画
onMounted(() => {
  data.value.forEach((item, index) => {
    // 延迟启动动画，创造依次出现的效果
    setTimeout(() => {
      animationInstances[index].animateNumber(item.value, 1000)
      increaseAnimationInstances[index].animateNumber(item.increaseNumber, 800)
    }, index * 200)
  })
})
</script>

<template>
  <div class="space-y-4">
    <FifthTitle title="爬取数据总览" icon="icon-gaikuang" :icon-size="14" size="md" />
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="(item, index) in data" :key="item.title" class="group relative h-32">
        <div
          :class="[
            'relative h-full bg-gradient-to-br backdrop-blur-sm rounded-xl p-4 border shadow-lg hover:shadow-xl transition-all duration-300 hover:transform hover:-translate-y-1 overflow-hidden',
            item.bgColor,
            item.borderColor,
          ]"
        >
          <div class="relative z-10 flex flex-col justify-between h-full">
            <div class="flex flex-col justify-between gap-2">
              <div class="w-full flex items-center justify-between">
                <div class="text-sm font-DIN-Medium text-gray-200 flex items-center">
                  {{ item.title }}
                  <span class="text-gray-300 text-xs">（{{ title }}）</span>
                </div>
                <div
                  v-if="item.increaseNumber > 0"
                  class="px-2 py-1 rounded-full text-xs bg-white/15 scale-75 origin-right"
                  :class="item.iconColor"
                >
                  NEW
                </div>
              </div>

              <div class="flex items-baseline space-x-1">
                <span class="text-2xl font-bold text-white">
                  {{ animationInstances[index].formattedValue }}
                </span>
                <span class="text-sm text-gray-400">{{ item.unit }}</span>
              </div>
            </div>
            <div class="flex items-center">
              <span class="text-xs text-gray-500"> {{ comparedTitle }} </span>
              <div v-if="item.increaseNumber > 0" class="flex items-center space-x-3">
                <span class="text-xs text-gray-500">新增</span>
                <div class="flex items-center space-x-1">
                  <Icon name="icon-shangsheng" color="text-green-400" :size="12" />
                  <span class="text-sm text-green-400 font-DIN-Medium">
                    +{{ increaseAnimationInstances[index].formattedValue }}
                  </span>
                  <span class="text-xs text-gray-500">
                    {{ item.unit }}
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-gray-500">无新增</div>
            </div>
          </div>

          <!-- 悬停光效 -->
          <div
            :class="[
              'absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl',
            ]"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>
