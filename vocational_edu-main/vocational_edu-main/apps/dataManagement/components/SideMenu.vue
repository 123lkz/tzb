<script setup lang="ts">
// 菜单项配置
const menuItems: Record<string, { label: string; path: string; icon: string }> = {
  // home: { label: '数据总览', path: 'home', icon: '🏠' },
  position: { label: '职位信息', path: 'position-list', icon: '💼' }
  // salary: { label: '薪酬信息', path: 'salary', icon: '💰' },
  // education: { label: '教育供给', path: 'education', icon: '🎓' },
  // career: { label: '标准职业', path: 'career', icon: '👨‍💼' },
  // industry: { label: '标准行业', path: 'industry', icon: '🏭' },
  // company: { label: '公司信息', path: 'company', icon: '🏢' },
  // platform: { label: '平台爬取', path: 'crawler', icon: '🕷️' },
  // tool: { label: '工具助手', path: 'tool', icon: '🔧' }
}

const router = useRouter()
const route = useRoute()

// 收起状态
const collapsed = ref(false)

// 时间相关
const currentTime = ref(
  new Date().toLocaleTimeString('zh-CN', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
)
const currentDate = ref(
  new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    weekday: 'long'
  })
)
const currentWeek = ref(
  new Date().toLocaleDateString('zh-CN', {
    weekday: 'long'
  })
)

// 用户信息
const userName = ref('管理员')

// 菜单项
const currentMenuItems = computed(() => {
  return menuItems
})

// 当前激活的菜单项
const active = ref('home')

// 引导动画状态
const showGuideAnimation = ref(true)

// 切换收起状态
const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}

// 监听路由变化
watch(
  () => route.path,
  (val) => {
    for (const key in currentMenuItems.value) {
      if (val.startsWith('/position-list') && key === 'position') {
        active.value = 'position'
        return
      }
      if (val.startsWith(`/${currentMenuItems.value[key].path}`)) {
        active.value = key
        return
      }
    }
    active.value = Object.keys(currentMenuItems.value)[0] || 'home'
  },
  { immediate: true }
)

function go(path: string, key: string) {
  if (route.path !== `/${path}`) {
    router.push(`/${path}`)
  }
  active.value = key
}

function handleLogout() {
  // 这里可以添加退出登录的逻辑
  // 可以调用退出登录的API
  // await logout()
  // router.push('/login')
}
</script>

<template>
  <div
    :class="[
      'm-4 flex flex-col transition-all duration-300 ease-in-out relative z-10 bg-[#00ffff]/10 backdrop-blur-sm shadow-[0_0_24px_0_rgba(0,255,255,0.25)] border border-[#00ffff]/10 rounded-lg flex-shrink-0',
      collapsed ? 'w-[60px]' : 'w-[200px]'
    ]"
    :style="{
      height: 'calc(100vh - 2rem)'
    }"
  >
    <!-- 内容区域 -->
    <div class="w-full relative z-10 flex flex-col h-full" :class="collapsed ? 'px-0' : 'px-3'" style="width: 100%">
      <!-- 标题区域 -->
      <div class="h-24 flex items-center justify-center border-b border-[#00eaff33]">
        <div class="text-center">
          <div v-if="!collapsed" class="mb-2 animate-fade-in cursor-pointer" @click="toggleCollapse">
            <h1 class="text-lg font-bold text-[#00eaff] mb-1">职教数据中台</h1>
            <p class="text-xs text-[#b0c4de]">国家职业教育人才供需数据中台</p>
          </div>
          <div v-else class="flex justify-center animate-fade-in cursor-pointer" @click="toggleCollapse">
            <div class="w-10 h-10 bg-[#00eaff] rounded-lg flex items-center justify-center">
              <span class="text-[#1a2980] font-bold text-sm">职</span>
            </div>
          </div>
        </div>
      </div>
      <!-- 菜单内容区域 -->
      <div class="w-full flex-1 relative">
        <ul class="py-4 space-y-2">
          <li
            v-for="(item, key) in currentMenuItems"
            :key="key"
            class="menu-item group relative cursor-pointer transition-all duration-300 rounded-lg mx-1 select-none"
            :class="{ active: active === key }"
            @click="go(item.path, key)"
          >
            <div class="flex items-center px-3 py-2.5">
              <span class="text-lg menu-icon" :class="collapsed ? '' : 'mr-3'">{{ item.icon }}</span>
              <span v-if="!collapsed" class="text-sm font-medium menu-name animate-slide-in">
                {{ item.label }}
              </span>
            </div>
            <div class="menu-border"></div>
            <div
              v-if="collapsed"
              class="absolute left-full top-0 transform ml-4 px-4 py-2 bg-[#140222]/70 text-sm rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-50 whitespace-nowrap backdrop-blur-md border border-[#00ffff66] flex items-center justify-center"
              style="min-width: 60px"
            >
              <span class="w-full text-center block">{{ item.label }}</span>
              <div
                class="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-2 h-2 bg-[#140222]/70 rotate-45 border-l border-b border-[#00ffff66]"
              ></div>
            </div>
          </li>
        </ul>
      </div>
      <!-- 底部信息区域 -->
      <div class="py-4 border-t border-[#00eaff33] space-y-6">
        <!-- 当前时间 -->
        <div v-if="!collapsed" class="text-center">
          <div class="text-[#00eaff] font-medium">{{ currentTime }}</div>
          <div class="text-sm text-[#b0c4de] mt-1">{{ currentDate }}</div>
        </div>
        <div v-else class="text-center">
          <div class="text-sm text-[#00eaff] font-medium">
            {{ currentTime.split(':').slice(0, 2).join(':') }}
          </div>
          <div class="text-sm text-[#b0c4de] mt-1">{{ currentWeek }}</div>
        </div>

        <!-- 用户信息和操作按钮 -->
        <div class="flex items-center" :class="collapsed ? 'justify-center flex-col gap-4' : 'justify-between'">
          <div class="flex items-center justify-center">
            <div class="w-8 h-8 bg-[#00eaff] rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-[#1a2980] font-bold text-sm">U</span>
            </div>
            <div v-if="!collapsed" class="ml-2 animate-slide-in">
              <div class="text-sm text-[#00eaff] font-medium">{{ userName }}</div>
            </div>
          </div>

          <div class="flex space-x-2 animate-slide-in">
            <button
              class="px-4 py-2 text-xs bg-[#00eaff22] text-[#00eaff] rounded-md hover:bg-[#00eaff44] active:bg-[#00eaff66] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[#00eaff44] focus:ring-opacity-50"
              @click="handleLogout"
            >
              退出
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- 收起/展开按钮 -->
    <div
      class="absolute top-[9.5%] -right-3 z-20 flex flex-col items-center justify-center cursor-pointer group"
      @click="toggleCollapse"
    >
      <div
        :class="[
          'w-6 h-6 rounded-full flex items-center justify-center shadow-lg bg-gray-700 transition-all duration-300 hover:bg-[rgba(0,255,255,0.4)]'
        ]"
      >
        <svg
          viewBox="0 0 1024 1024"
          width="16"
          height="16"
          :class="['transition-transform duration-300', collapsed ? 'rotate-180' : '']"
        >
          <path
            d="M659.20256 856.832c27.14496 0 49.14944-22.00448 49.14944-49.15456 0-13.2544-5.25952-25.26464-13.78048-34.10944l0.01536-0.01536L433.69216 512.6528 691.2128 255.12704c10.4896-9.00992 17.14048-22.36544 17.14048-37.27488 0-27.14496-22.00448-49.14944-49.14944-49.14944-13.1904 0-25.16864 5.2096-34.00064 13.68064l-0.12928-0.13184L330.16192 477.16224l0.01536 0.02048c-9.27488 8.94464-15.04 21.47456-15.04 35.37024l0 0.1152 0 0.1152c0 13.90976 5.76512 26.41024 15.04 35.37536l-0.01536 0.01536 294.91072 294.90944 0.01408-0.01536C633.91744 851.58784 645.94688 856.832 659.20256 856.832L659.20256 856.832zM659.20256 856.832"
            fill="rgba(255,255,255,0.5)"
          ></path>
        </svg>
      </div>
      <!-- 提示文字 - 右上角 -->
      <div class="absolute -top-8 -right-2 z-50">
        <div
          v-if="!collapsed"
          class="pointer-events-none px-2 py-1 bg-[rgba(0,255,255,0.2)] text-xs text-[#00eaff] rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 delay-100 whitespace-nowrap backdrop-blur-md border border-[#00ffff44] shadow-lg min-w-[32px] text-center"
        >
          <span class="font-medium">收起</span>
        </div>
        <div
          v-else
          class="pointer-events-none px-2 py-1 bg-[rgba(0,255,255,0.2)] text-xs text-[#00eaff] rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300 delay-100 whitespace-nowrap backdrop-blur-md border border-[#00ffff44] shadow-lg min-w-[32px] text-center"
        >
          <span class="font-medium">展开</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 234, 255, 0.3);
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 234, 255, 0.5);
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 滑入动画 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 应用动画类 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

.animate-slide-in {
  animation: slideIn 0.3s ease-out forwards;
}

/* 悬浮动画效果 */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* 脉冲效果 */
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

/* 菜单项样式 - 参考IndexTab */
.menu-item {
  position: relative;
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 6px;
  z-index: 1;
  /* 移除可能产生竖线的边框 */
  border: none;
  outline: none;
}

.menu-item:hover {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  transform: translateY(-1px);
}

.menu-item.active {
  color: #00ffff;
  background: rgba(0, 255, 255, 0.15);
  transform: translateY(-1px);
}

.menu-item.active .menu-border {
  opacity: 1;
  transform: scaleX(1);
}

.menu-icon {
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.3));
  transition: transform 0.3s ease;
}

.menu-item:hover .menu-icon {
  transform: scale(1.1);
}

.menu-name {
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.menu-border {
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

.menu-item:hover .menu-border {
  opacity: 0.5;
  transform: scaleX(0.8);
}

/* 应用悬浮动画 */
.tabs-container {
  animation: float 6s ease-in-out infinite;
}

/* 应用脉冲效果 */
.tabs-wrapper {
  animation: pulse 2s ease-in-out infinite;
}

/* 引导动画效果 */
@keyframes guidePulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

@keyframes guideGlow {
  0%,
  100% {
    box-shadow: 0 0 4px rgba(0, 255, 255, 0.3), 0 0 8px rgba(0, 255, 255, 0.1);
  }
  50% {
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.4), 0 0 8px rgba(0, 255, 255, 0.2);
  }
}

@keyframes guideRotate {
  0% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-3deg);
  }
  75% {
    transform: rotate(3deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

/* 按钮引导动画 */
.guide-animation {
  animation: guidePulse 2.5s ease-in-out infinite, guideGlow 2.5s ease-in-out infinite;
}

.guide-animation svg {
  animation: guideRotate 3s ease-in-out infinite;
}

/* 提示文字动画 */
@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes tooltipFadeInTopRight {
  from {
    opacity: 0;
    transform: translateY(5px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.group:hover .group-hover\:opacity-100 {
  animation: tooltipFadeIn 0.3s ease-out forwards;
}

/* 右上角提示动画 */
.group:hover .group-hover\:opacity-100 {
  animation: tooltipFadeInTopRight 0.3s ease-out forwards;
}

/* 确保没有意外的边框或轮廓 */
* {
  box-sizing: border-box;
}

/* 移除按钮的默认样式 */
button {
  border: none;
  outline: none;
  background: none;
  cursor: pointer;
}

button:focus {
  outline: none;
}

/* 确保用户头像不会产生意外的视觉效果 */
.w-8.h-8 {
  flex-shrink: 0;
  overflow: hidden;
}
</style>
