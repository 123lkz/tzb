<script setup lang="ts">
import TimeFilter from '../common/Filter/TimeFilter.vue'
import caliberFilter from '../common/Filter/CaliberFilter.vue'
import ProvinceFilter from '../common/Filter/ProvinceFilter.vue'

// Props
interface Props {
  selectedTimeDimension?: string
  showWeekly?: boolean
  showScope?: boolean
  showProvince?: boolean
  showTime?: boolean
  pageTitle?: string
  pageSubtitle?: string
  breadcrumbs?: Array<{ label: string; path: string }>
}

const props = withDefaults(defineProps<Props>(), {
  selectedTimeDimension: 'month',
  showWeekly: false,
  showScope: true,
  showProvince: true,
  showTime: true,
  pageTitle: '数据管理',
  pageSubtitle: '职业教育人才供需数据分析',
  breadcrumbs: () => [
    { label: '首页', path: '/' },
    { label: '', path: '/data' },
  ],
})

// Emits
const emit = defineEmits<{
  'time-change': [value: string]
  'scope-change': [value: string]
  'province-change': [value: string]
  back: []
}>()

// Router
const router = useRouter()
const route = useRoute()

// 响应式数据
const timeDimension = ref(props.selectedTimeDimension || 'month') // 默认选择年度
const dataScope = ref('all') // 默认选择全口径
const province = ref('全国') // 默认选择省份
const title = ref('')

// 方法
const handleBack = () => {
  emit('back')
  router.back()
}

const navigateTo = (path: string) => {
  router.push(path)
}

const handleTimeChange = (value: string) => {
  emit('time-change', value)
}

const handleScopeChange = (value: string) => {
  emit('scope-change', value)
}

const handleProvinceChange = (value: string) => {
  emit('province-change', value)
}

// 监听路由变化，更新面包屑
watch(
  () => route.path,
  newPath => {
    // 这里可以根据路由动态更新面包屑
    console.log('路由变化:', newPath)
  }
)

watch(
  () => props.selectedTimeDimension,
  newTimeDimension => {
    timeDimension.value = newTimeDimension || 'month'
  }
)

// 组件挂载时触发默认值的事件
onMounted(() => {
  // 触发默认的时间维度选择事件
  emit('time-change', timeDimension.value)
  // 触发默认的数据范围选择事件
  emit('scope-change', dataScope.value)
  // 触发默认的省份选择事件
  emit('province-change', province.value)
})
</script>

<template>
  <div
    class="flex items-center justify-between py-2 h-12 flex-shrink-0 rounded-lg bg-[#00ffff0d] backdrop-blur-sm border-b border-[#00ffff]/10 shadow-[0_0_24px_0_rgba(0,255,255,0.25)] animate-[fadeInUp_0.6s_ease-out] overflow-hidden"
  >
    <!-- 左侧区域：返回按钮 + 面包屑 -->
    <div class="flex items-center gap-3 flex-shrink-0">
      <div
        class="flex items-center justify-center w-8 h-8 bg-[rgba(0,255,255,0.1)] rounded-lg cursor-pointer transition-all duration-300 ease-in-out text-[#00eaff] hover:bg-[rgba(0,255,255,0.2)] hover:-translate-x-0.5 hover:shadow-[0_4px_12px_rgba(0,255,255,0.3)] focus:outline-none focus:outline-2 focus:outline-[#00eaff] focus:outline-offset-2"
        title="返回上一页"
        @click="handleBack"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </div>
      <nav class="flex items-center" aria-label="面包屑导航">
        <ol class="flex items-center list-none m-0 p-0 gap-2">
          <li v-for="(item, index) in breadcrumbs" :key="index" class="flex items-center gap-1">
            <span
              v-if="index === breadcrumbs.length - 1"
              class="text-[#00eaff] font-semibold text-sm"
            >
              {{ item.label }}
            </span>
            <a
              v-else
              :href="item.path"
              class="text-[rgba(176,196,222,0.8)] no-underline text-sm transition-all duration-300 ease-in-out py-1 px-2 rounded hover:text-[#00eaff] hover:bg-[rgba(0,255,255,0.1)]"
              @click.prevent="navigateTo(item.path)"
            >
              {{ item.label }}
            </a>
            <svg
              v-if="index < breadcrumbs.length - 1"
              class="w-4 h-4 text-[rgba(176,196,222,0.5)]"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          </li>
        </ol>
      </nav>
    </div>
    <div class="flex-1 flex justify-center items-center">
      <span class="text-sm font-bold text-[#00eaff]">{{ title }}</span>
    </div>

    <!-- 右侧区域：选择器和按钮 -->
    <div class="flex items-center gap-4">
      <slot name="right-filter" />
      <TimeFilter
        v-if="showTime"
        v-model="timeDimension"
        :show-weekly="showWeekly"
        @update:model-value="handleTimeChange"
      />
      <caliberFilter v-if="showScope" v-model="dataScope" @update:model-value="handleScopeChange" />
      <ProvinceFilter
        v-if="showProvince"
        v-model="province"
        @update:model-value="handleProvinceChange"
      />
      <div class="flex items-center gap-2">
        <slot name="right-button" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .right-section {
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .breadcrumb-list {
    flex-wrap: wrap;
    justify-content: center;
  }

  .radio-group {
    gap: 0.25rem;
  }

  .toggle-group {
    flex-direction: column;
  }
}
</style>
