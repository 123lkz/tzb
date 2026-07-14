<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNumberAnimation } from '~/composables/useNumberAnimation'
import { $position, $salary } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'
import { getStatisticalTime } from '~/utils/time'

const emits = defineEmits<{
  'on-tab-click': ['position' | 'salary' | 'education']
  'on-change': [
    {
      quantity: 'all' | 'college'
      date: 'year' | 'month'
    }
  ]
}>()

const route = useRoute()
const router = useRouter()

// const vocationalEducationDataManager = new VocationalEducationDataManager()

const tabs: Array<{ id: 'position' | 'salary' | 'education'; name: string; icon: string }> = [
  {
    id: 'position',
    name: '职位信息',
    icon: 'M3 3v18h18 M19 9l-5 5-4-4-3 3'
  },
  {
    id: 'salary',
    name: '薪酬信息',
    icon: 'M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'
  },
  {
    id: 'education',
    name: '教育供给',
    icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z M12 7v10 M8 9v6 M16 9v6'
  }
]

// 当前选中的tab
const activeTab = ref(tabs[0].id)
// 统计口径
const filterQuantityType = ref<'all' | 'college'>('all')
// 统计时间
const filterDateType = ref<'year' | 'month'>('month')
// 为每个数据项创建动画实例
const animationInstances = ref<Array<ReturnType<typeof useNumberAnimation>>>([])

const { data: positionData } = useApiData(() =>
  $position.GetScreenTotalData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

const { data: salaryData } = useApiData(() =>
  $salary.GetScreenTotalData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

// 暂时使用本地数据，等待教育数据API接口
const educationData = ref(null)

// 获取统计时间信息
const statisticalTime = computed(() => getStatisticalTime(filterDateType.value))

// tab切换
const handleTabClick = (id: 'position' | 'salary' | 'education') => {
  activeTab.value = id
  emits('on-tab-click', id)
  router.push(`/${id}`)
}

// 统计口径切换
const handleQuantityFilterChange = (type: 'all' | 'college') => {
  filterQuantityType.value = type
  // totalData.value = vocationalEducationDataManager.getTotalData(filterDateType.value, type)
  emits('on-change', {
    quantity: filterQuantityType.value,
    date: filterDateType.value
  })
}

// 统计时间切换
const handleDateFilterChange = (type: 'year' | 'month') => {
  filterDateType.value = type
  // totalData.value = vocationalEducationDataManager.getTotalData(type, filterQuantityType.value)
  emits('on-change', {
    quantity: filterQuantityType.value,
    date: filterDateType.value
  })
}

const panelConfig = {
  position: [
    { key: 'totalPositions', unit: '个', prefix: '', label: '招聘职位总个数' },
    { key: 'totalRecruitment', unit: '人', prefix: '', label: '招聘需求总人数' },
    { key: 'totalCompanies', unit: '家', prefix: '', label: '招聘单位总数量' }
  ],
  salary: [
    { key: 'p25Salary', unit: '元', prefix: '', label: '招聘薪资25%分位数' },
    { key: 'p50Salary', unit: '元', prefix: '', label: '招聘薪资中位数' },
    { key: 'p75Salary', unit: '元', prefix: '', label: '招聘薪资75%分位数' }
  ],
  education: [
    { key: 'totalJuniorCollegeStudents', unit: '人', prefix: '', label: '在校总人数' },
    { key: 'totalJuniorCollegeProfession', unit: '个', prefix: '', label: '招聘职位总个数' },
    { key: 'juniorCollegeSalaryMedian', unit: '元', prefix: '', label: '招聘薪资中位数' }
  ]
}

const getPanelData = (
  tab: 'position' | 'salary' | 'education',
  dateType: 'year' | 'month',
  quantityType: 'all' | 'college'
) => {
  // 只处理 position/salary/education 三个 tab
  if (!panelConfig[tab]) return []

  // 获取对应的API数据
  let data: any = null
  if (tab === 'position' && positionData.value) {
    data = positionData.value
  } else if (tab === 'salary' && salaryData.value) {
    data = salaryData.value
  } else if (tab === 'education' && educationData.value) {
    data = educationData.value
  }

  if (!data) return []

  // 统计时间 - 使用统一的时间处理函数
  const timeInfo = getStatisticalTime(dateType)
  const statisticalDateText = timeInfo.displayText
  const statisticalStudentYear = data.staticStudentYear ? `${data.staticStudentYear}年` : ''

  // 生成前缀的通用函数
  const generatePrefix = (tab: string, quantityType: string, statisticalDateText: string) => {
    const isAll = quantityType === 'all'
    const isEducation = tab === 'education'

    // 教育模块的特殊处理
    if (isEducation) {
      return isAll ? `${statisticalDateText}全国大专生` : `${statisticalDateText}应届大专生`
    }

    // 职位和薪酬模块的处理
    return isAll ? statisticalDateText : `${statisticalDateText}应届大专生`
  }

  // label 前缀
  const prefix = generatePrefix(tab, quantityType, statisticalDateText)

  // 组装面板数据
  return panelConfig[tab].map((item, index) => {
    // 教育模块第一个项目使用特殊前缀
    const itemPrefix = tab === 'education' && index === 0 ? `${statisticalStudentYear}全国大专生` : prefix

    return {
      value: (data as any)[item.key]?.toLocaleString?.() ?? '-',
      unit: item.unit,
      prefix: itemPrefix,
      label: item.label
    }
  })
}

// 创建面板数据的通用函数
const createPanelData = (tab: 'position' | 'salary' | 'education', data: any) => {
  if (!data) return []
  return getPanelData(tab, filterDateType.value, filterQuantityType.value)
}

// 职位数据面板
const positionPanel = computed(() => createPanelData('position', positionData.value))

// 薪酬数据面板
const salaryPanel = computed(() => createPanelData('salary', salaryData.value))

// 教育数据面板
const educationPanel = computed(() => createPanelData('education', educationData.value))

// 当前激活的数据面板
const currentDataPanel = computed(() => {
  const panelMap = {
    position: positionPanel.value,
    salary: salaryPanel.value,
    education: educationPanel.value
  }
  return panelMap[activeTab.value] || []
})

const navigateToDataCenter = () => {
  window.open('https://tte.smartedu.work/zjdata', '_blank')
}

// 创建动画实例的函数
const createAnimationInstances = (dataLength: number) => {
  const instances = []
  for (let i = 0; i < dataLength; i++) {
    instances.push(useNumberAnimation())
  }
  return instances
}

// 监听当前激活的数据面板变化，触发动画
watch(
  currentDataPanel,
  (newData) => {
    // 清理之前的动画实例
    animationInstances.value.forEach((instance) => instance.clearTimer())
    // 为每个数据项创建新的动画实例
    animationInstances.value = createAnimationInstances(newData.length)
    // 延迟启动动画，确保DOM更新完成
    nextTick(() => {
      newData.forEach((item, index) => {
        const instance = animationInstances.value[index]
        if (instance) {
          // 提取数字值（移除逗号）
          const numericValue = parseInt(item.value.replace(/,/g, ''))
          instance.animateNumber(numericValue, 1000)
        }
      })
    })
  },
  { immediate: true }
)

defineExpose({
  handleQuantityFilterChange,
  filterQuantityType,
  handleDateFilterChange,
  filterDateType,
  handleTabClick,
  activeTab,
  tabs
})

onMounted(() => {
  const path = route.path
  if (path.includes('/position')) {
    activeTab.value = 'position'
    filterQuantityType.value = 'all'
    filterDateType.value = 'month'
  } else if (path.includes('/salary')) {
    activeTab.value = 'salary'
    filterQuantityType.value = 'all'
    filterDateType.value = 'month'
  } else if (path.includes('/education')) {
    activeTab.value = 'education'
    filterQuantityType.value = 'all'
    filterDateType.value = 'month'
  }
})

// 组件卸载时清理动画实例
onBeforeUnmount(() => {
  animationInstances.value.forEach((instance) => instance.clearTimer())
})
</script>

<template>
  <div class="tabs-container">
    <!-- 左侧数据展示 -->
    <div class="data-container">
      <div class="data-wrapper">
        <!-- 职位信息数据面板 -->
        <template v-if="activeTab === 'position'">
          <div
            v-for="(item, idx) in positionPanel"
            :key="'position-' + item.label + item.value + item.unit"
            style="flex: 1"
            class="data-item"
            :class="{
              'total-item': idx === 0,
              'platform-item': idx === 1,
              'time-item': idx === 2
            }"
          >
            <div class="corner-decoration top-left"></div>
            <div class="corner-decoration top-right"></div>
            <div class="corner-decoration bottom-left"></div>
            <div class="corner-decoration bottom-right"></div>
            <div class="data-value">
              <span class="font-bold">
                {{ animationInstances[idx]?.formattedValue || '0' }}
              </span>
              <span class="text-xs opacity-50 ml-1">{{ item.unit }}</span>
            </div>
            <div class="data-label">
              <p class="opacity-90 text-xs">{{ item.prefix }}</p>
              <p>{{ item.label }}</p>
            </div>
          </div>
        </template>

        <!-- 薪酬信息数据面板 -->
        <template v-if="activeTab === 'salary'">
          <div
            v-for="(item, idx) in salaryPanel"
            :key="'salary-' + item.label + item.value + item.unit"
            style="flex: 1"
            class="data-item"
            :class="{
              'total-item': idx === 0,
              'platform-item': idx === 1,
              'time-item': idx === 2
            }"
          >
            <div class="corner-decoration top-left"></div>
            <div class="corner-decoration top-right"></div>
            <div class="corner-decoration bottom-left"></div>
            <div class="corner-decoration bottom-right"></div>
            <div class="data-value">
              <span class="font-bold">
                {{ animationInstances[idx]?.formattedValue || '0' }}
              </span>
              <span class="text-xs opacity-50 ml-1">{{ item.unit }}</span>
            </div>
            <div class="data-label">
              <p class="opacity-90 text-xs">{{ item.prefix }}</p>
              <p>{{ item.label }}</p>
            </div>
          </div>
        </template>

        <!-- 教育供给数据面板 -->
        <div
          v-for="(item, idx) in educationPanel"
          v-if="activeTab === 'education'"
          :key="'education-' + item.label + item.value + item.unit"
          style="flex: 1"
          class="data-item"
          :class="{
            'total-item': idx === 0,
            'platform-item': idx === 1,
            'time-item': idx === 2
          }"
        >
          <div class="corner-decoration top-left"></div>
          <div class="corner-decoration top-right"></div>
          <div class="corner-decoration bottom-left"></div>
          <div class="corner-decoration bottom-right"></div>
          <div class="data-value">
            <span class="font-bold">
              {{ animationInstances[idx]?.formattedValue || '0' }}
            </span>
            <span class="text-xs opacity-50 ml-1">{{ item.unit }}</span>
          </div>
          <div class="data-label">
            <p class="opacity-90 text-xs">{{ item.prefix }}</p>
            <p>{{ item.label }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计口径过滤条件 全口径和应届大专生 -->
    <div class="filter-container quantity-filter-container">
      <div class="filter-wrapper">
        <div
          class="filter-item"
          :class="{ active: filterQuantityType === 'all' }"
          @click="handleQuantityFilterChange('all')"
        >
          <div class="radio-box">
            <div class="radio-inner"></div>
          </div>
          <span class="filter-text">全口径</span>
        </div>
        <div
          class="filter-item"
          :class="{ active: filterQuantityType === 'college' }"
          @click="handleQuantityFilterChange('college')"
        >
          <div class="radio-box">
            <div class="radio-inner"></div>
          </div>
          <span class="filter-text">应届大专生</span>
        </div>
      </div>
    </div>

    <!-- 主要的tabs -->
    <div class="tabs-wrapper">
      <div class="rotating-border"></div>
      <div
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-item"
        :class="{ active: activeTab === tab.id }"
        @click="handleTabClick(tab.id)"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" width="20" height="20">
          <path
            :d="tab.icon"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <span class="tab-name">{{ tab.name }}</span>
        <div class="tab-border"></div>
      </div>
    </div>

    <!-- 日期过滤条件 年份和月份 -->
    <div class="filter-container date-filter-container">
      <div class="filter-wrapper">
        <div
          class="filter-item"
          :class="{ active: filterDateType === 'month' }"
          @click="handleDateFilterChange('month')"
        >
          <div class="radio-box">
            <div class="radio-inner"></div>
          </div>
          <span class="filter-text">月度</span>
        </div>
        <div class="filter-item" :class="{ active: filterDateType === 'year' }" @click="handleDateFilterChange('year')">
          <div class="radio-box">
            <div class="radio-inner"></div>
          </div>
          <span class="filter-text">年度</span>
        </div>
      </div>
      <div class="filter-text-container">
        <template v-if="filterDateType === 'year'">
          <span class="text-white/70">统计年度：</span>
          <span>{{ statisticalTime.displayText }}</span>
        </template>
        <template v-else>
          <span class="text-white/70">统计月度：</span>
          <span>{{ statisticalTime.displayText }}</span>
        </template>
      </div>
    </div>

    <div
      class="data-center-entry"
      style="cursor: pointer; display: flex; align-items: center; padding: 4px 16px"
      @click="navigateToDataCenter"
    >
      <span
        class="data-center-entry-text"
        style="
          color: #d0ffff;
          font-weight: 500;
          font-size: 15px;
          transition: color 0.3s, text-shadow 0.3s, transform 0.3s;
          cursor: pointer;
          display: inline-block;
        "
      >
        数据中台入口
      </span>
      <img src="@/assets/images/enter.png" alt="entrance" class="w-5 h-5" />
    </div>
  </div>
</template>

<style scoped>
.tabs-container {
  position: relative;
  display: flex;
  justify-content: center;
  height: 3.5rem;
}

.tabs-wrapper {
  top: 10px;
  display: flex;
  gap: 20px;
  background: rgba(0, 255, 255, 0.05);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
  }
  100% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  }
}

.rotating-border {
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  border-radius: 10px;
  background: linear-gradient(90deg, #00ffff, #00bfff, #0080ff, #00bfff, #00ffff);
  background-size: 400% 400%;
  animation: rotate 8s linear infinite;
  z-index: 0;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  padding: 0;
}

@keyframes rotate {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.tab-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 6px;
  z-index: 1;
}

.tab-item:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  transform: translateY(-1px);
}

.tab-item.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.15);
  transform: translateY(-1px);
}

.tab-item.active .tab-border {
  opacity: 1;
  transform: scaleX(1);
}

.tab-icon {
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.3));
  transition: transform 0.3s ease;
}

.tab-item:hover .tab-icon {
  transform: scale(1.1);
}

.tab-name {
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
}

.tab-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, rgba(0, 255, 255, 0) 0%, rgba(0, 255, 255, 1) 50%, rgba(0, 255, 255, 0) 100%);
  opacity: 0;
  transform: scaleX(0);
  transition: all 0.3s ease;
}

.tab-item:hover .tab-border {
  opacity: 0.5;
  transform: scaleX(0.8);
}

/* 过滤条件样式 */
.filter-container {
  position: absolute;
  z-index: 10;
}

.quantity-filter-container {
  top: 85px;
  left: 45%;
}

.date-filter-container {
  top: 35%;
  left: 65%;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-wrapper {
  display: flex;
  gap: 10px;
  background: rgba(0, 255, 255, 0.05);
  padding: 0;
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.filter-text-container {
  display: flex;
  padding: 0;
  border-radius: 8px;
  color: #00ffff;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 4px;
  position: relative;
}

.filter-item:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  transform: translateY(-1px);
}

.filter-item.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.15);
  transform: translateY(-1px);
}

.radio-box {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

.filter-item:hover .radio-box {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
}

.filter-item.active .radio-box {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
}

.radio-inner {
  width: 8px;
  height: 8px;
  background: #00ffff;
  border-radius: 1px;
  opacity: 0;
  transition: all 0.3s ease;
  transform: scale(0);
}

.filter-item.active .radio-inner {
  opacity: 1;
  transform: scale(1);
}

.filter-text {
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

/* 数据展示样式 */
.data-container {
  position: absolute;
  left: 0.5rem;
  top: 10px;
  transform: translateY(-50%);
  z-index: 10;
}

.data-wrapper {
  padding: 16px 10px;
  border-radius: 8px;
  position: relative;
  min-width: 550px;
  display: flex;
  gap: 16px;
  width: 100%;
}

/* 四个角的直角修饰框 */
.corner-decoration {
  position: absolute;
  width: 8px;
  height: 8px;
  border: 1px solid;
}

.corner-decoration.top-left {
  top: 4px;
  left: 4px;
  border-right: none;
  border-bottom: none;
}

.corner-decoration.top-right {
  top: 4px;
  right: 4px;
  border-left: none;
  border-bottom: none;
}

.corner-decoration.bottom-left {
  bottom: 4px;
  left: 4px;
  border-right: none;
  border-top: none;
}

.corner-decoration.bottom-right {
  bottom: 4px;
  right: 4px;
  border-left: none;
  border-top: none;
}

/* 数据项样式 */
.data-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 180px;
  height: 70px;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  flex: 1;
  min-width: 0;
  text-align: center;
}

.data-value {
  font-size: 1rem;
  font-weight: bold;
  line-height: 1;
  white-space: nowrap;
}

.data-label {
  font-size: 0.75rem;
  font-weight: 500;
  opacity: 0.8;
  letter-spacing: 1px;
  text-align: center;
  word-wrap: break-word;
  word-break: break-all;
  line-height: 1.2;
  max-width: 100%;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 总量样式 - 青色 */
.total-item {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.total-item .data-value {
  color: #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
}

.total-item .data-label {
  color: rgba(0, 255, 255, 0.8);
}

.total-item .corner-decoration {
  border-color: #00ffff;
}

/* 招聘平台总量样式 - 亮黄色 */
.platform-item {
  background: rgba(255, 255, 0, 0.1);
  border: 1px solid rgba(255, 255, 0, 0.3);
}

.platform-item .data-value {
  color: #ffff00;
  text-shadow: 0 0 8px rgba(255, 255, 0, 0.6);
}

.platform-item .data-label {
  color: rgba(255, 255, 0, 0.8);
}

.platform-item .corner-decoration {
  border-color: #ffff00;
}

/* 更新时间样式 - 亮蓝色 */
.time-item {
  background: rgba(0, 191, 255, 0.1);
  border: 1px solid rgba(0, 191, 255, 0.3);
}

.time-item .data-value {
  color: #00bfff;
  text-shadow: 0 0 8px rgba(0, 191, 255, 0.6);
  font-size: 1rem;
}

.time-item .data-label {
  color: rgba(0, 191, 255, 0.8);
}

.time-item .corner-decoration {
  border-color: #00bfff;
}

/* 数据区切换动画 */
.data-fade-item-enter-active,
.data-fade-item-leave-active {
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.data-fade-item-enter-from,
.data-fade-item-leave-to {
  opacity: 0;
}
.data-fade-item-enter-to,
.data-fade-item-leave-from {
  opacity: 1;
}

.data-center-entry {
  position: absolute;
  right: 20px;
  top: 12px;
  z-index: 10;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 8px;
  padding: 4px 12px;
  background: rgba(0, 255, 255, 0.1);
  border: 0.5px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.data-center-entry:hover {
  transform: scale(1.08);
  animation: entry-bounce 0.4s;
  background: rgba(0, 255, 255, 0.2);
  border: 1px solid rgba(0, 255, 255, 0.4);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
}

.data-center-entry:hover .data-center-entry-text {
  color: #00ffff;
}

@keyframes entry-bounce {
  0% {
    transform: scale(1) rotate(0deg);
  }
  40% {
    transform: scale(1.12) rotate(-1deg);
  }
  60% {
    transform: scale(1.05) rotate(1deg);
  }
  100% {
    transform: scale(1.08) rotate(-1deg);
  }
}
</style>
