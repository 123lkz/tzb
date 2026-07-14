<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import Modal from '~/components/Modal.vue'
import TreeChart from '~/components/Echart/TreeChart.vue'

interface IndustrySubItem {
  name: string
}

interface IndustryItem {
  name: string
  industries: IndustrySubItem[]
}

interface IndustryData {
  name: string
  color?: string
  industries: IndustryItem[]
}

const props = defineProps<{
  data: IndustryData[]
}>()

const activeTab = ref(0)
const scrollContainer = ref<HTMLElement>()
const isScrolling = ref(false)
const showModal = ref(false)
const selectedIndustry = ref<IndustryData | null>(null)

const switchTab = (index: number) => {
  activeTab.value = index
  isScrolling.value = true

  // 滚动到对应的产业位置
  nextTick(() => {
    const targetElement = document.getElementById(`industry-${index}`)
    if (targetElement && scrollContainer.value) {
      const container = scrollContainer.value
      const elementTop = targetElement.offsetTop
      const containerHeight = container.clientHeight
      const scrollHeight = container.scrollHeight

      // 计算滚动位置，确保标题在顶部可见
      let scrollTop = elementTop

      // 如果是最后一个产业，确保不会滚动超出范围
      if (index === props.data.length - 1) {
        const maxScrollTop = scrollHeight - containerHeight
        scrollTop = Math.min(elementTop, maxScrollTop)
      }

      container.scrollTo({
        top: Math.max(0, scrollTop),
        behavior: 'smooth',
      })

      // 滚动完成后重新启用滚动监听
      setTimeout(() => {
        isScrolling.value = false
      }, 500)
    }
  })
}

// 监听滚动事件，更新当前活跃的标签
const handleScroll = () => {
  if (!scrollContainer.value || isScrolling.value) return

  const container = scrollContainer.value
  const scrollTop = container.scrollTop
  const containerHeight = container.clientHeight
  const scrollHeight = container.scrollHeight

  // 如果滚动到顶部，直接设置为第一个产业
  if (scrollTop <= 10) {
    activeTab.value = 0
    return
  }

  // 如果滚动到底部，直接设置为最后一个产业
  if (scrollTop + containerHeight >= scrollHeight - 10) {
    activeTab.value = props.data.length - 1
    return
  }

  // 找到最接近容器中心的产业
  let closestIndex = 0
  let minDistance = Infinity

  props.data.forEach((_, index) => {
    const element = document.getElementById(`industry-${index}`)
    if (element) {
      const elementTop = element.offsetTop
      const elementHeight = element.offsetHeight
      const elementCenter = elementTop + elementHeight / 2
      const containerCenter = scrollTop + containerHeight / 2
      const distance = Math.abs(elementCenter - containerCenter)

      if (distance < minDistance) {
        minDistance = distance
        closestIndex = index
      }
    }
  })

  activeTab.value = closestIndex
}

const handleIndustryClick = (industry: IndustryData) => {
  selectedIndustry.value = industry
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedIndustry.value = null
}

// 根据选中的产业生成树形数据
const getIndustryTreeData = (industry: IndustryData | null) => {
  if (!industry) {
    return {
      name: '产业分类',
      children: [],
    }
  }

  // 直接使用传入的数据结构，转换为树形图需要的格式
  return {
    name: `${industry.name}`,
    children: industry.industries.map(item => ({
      name: item.name,
      children: item.industries ? item.industries.map(subItem => ({ name: subItem.name })) : [],
    })),
  }
}

onMounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('scroll', handleScroll, { passive: true })
  }
})

onUnmounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('scroll', handleScroll)
  }
})
</script>

<template>
  <div
    class="flex-1 flex overflow-hidden cursor-drop mt-2 relative"
    style="height: calc(100% - 40px)"
  >
    <!-- 左侧内容区域 -->
    <div ref="scrollContainer" class="flex-1 overflow-y-auto pr-4 min-h-0 scrollbar">
      <div v-for="(item, index) in props.data" :id="`industry-${index}`" :key="index" class="mb-4">
        <!-- 产业名称和值 -->
        <div
          class="flex items-center gap-2 mb-3 text-xs font-bold opacity-75 cursor-pointer hover:opacity-100 transition-opacity"
          :style="{ color: item.color }"
          @click="handleIndustryClick(item)"
        >
          {{ item.name }}
        </div>

        <!-- 子行业列表 -->
        <div class="space-y-2">
          <div
            v-for="(child, childIndex) in item.industries"
            :key="childIndex"
            class="flex items-center text-xs opacity-75 cursor-pointer hover:opacity-100 transition-opacity"
            :style="{ color: item.color }"
            @click="handleIndustryClick(item)"
          >
            <span>{{ child.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧按钮区域 -->
    <div
      class="w-8 my-6 grid grid-cols-1 grid-rows-3 gap-4 flex-shrink-0 justify-center shadow-lg absolute right-2 top-0"
    >
      <button
        v-for="(item, index) in props.data"
        :key="item.name"
        class="w-6 h-6 rounded-md font-bold text-gray-300 border border-gray-100/10 transition-all duration-300 flex items-center justify-center relative overflow-hidden"
        :class="{
          'tech-button-active': activeTab === index,
          'tech-button-inactive': activeTab !== index,
        }"
        @click="switchTab(index)"
      >
        <span class="relative z-10 text-xs font-bold">{{
          index === 0 ? '一' : index === 1 ? '二' : '三'
        }}</span>
      </button>
    </div>
  </div>

  <!-- 弹框 -->
  <Modal
    :show="showModal"
    :title="selectedIndustry?.name + '和标准行业分类'"
    width="70%"
    height="85%"
    @close="closeModal"
  >
    <TreeChart
      :data="getIndustryTreeData(selectedIndustry)"
      :text-color="selectedIndustry?.color || '#00ffff'"
      :selected-industry="selectedIndustry?.name"
    />
  </Modal>
</template>

<style scoped>
.scrollbar::-webkit-scrollbar {
  width: 4px;
  background: transparent;
  cursor: drop;
}
.scrollbar::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 255, 0.25);
  border-radius: 4px;
}
.scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.tech-button-active {
  color: #00ffff;
  background-color: rgba(0, 255, 255, 0.15);
  transform: scale(1.1);
}

.tech-button-inactive {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.tech-button-inactive:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3), 0 0 30px rgba(0, 255, 255, 0.1),
    0 4px 8px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

@keyframes pulse-glow {
  0% {
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.4), 0 0 40px rgba(0, 255, 255, 0.2),
      0 0 60px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.1);
  }
  100% {
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.6), 0 0 50px rgba(0, 255, 255, 0.3),
      0 0 75px rgba(0, 255, 255, 0.2), inset 0 0 25px rgba(0, 255, 255, 0.2);
  }
}

/* 添加按钮点击效果 */
button:active {
  transform: scale(0.95);
  transition: transform 0.1s ease;
}

/* 添加数字文字的发光效果 */
.tech-button-active span {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
  animation: text-glow 2s ease-in-out infinite alternate;
}

@keyframes text-glow {
  0% {
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
  }
  100% {
    text-shadow: 0 0 15px rgba(255, 255, 255, 1), 0 0 25px rgba(0, 255, 255, 0.8);
  }
}
</style>
