<script setup lang="ts">
// 大屏基础尺寸
const baseWidth = 1920
const baseHeight = 1080

// 缩放和拖拽状态
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const screenContainer = ref<HTMLElement | null>(null)

// 计算初始缩放比例和居中偏移
const calculateScaleAndPosition = () => {
  const windowWidth = window.innerWidth
  const windowHeight = window.innerHeight
  const scaleX = windowWidth / baseWidth
  const scaleY = windowHeight / baseHeight
  // 判断屏幕比例
  const windowRatio = windowWidth / windowHeight
  const baseRatio = baseWidth / baseHeight
  let newScale: number

  if (windowRatio > baseRatio) {
    // 屏幕比较宽，高度占满屏幕，宽度按比例自适应
    newScale = scaleY
  } else {
    // 屏幕比较高，宽度占满屏幕，高度按比例自适应
    newScale = scaleX
  }

  // 计算缩放后的实际尺寸
  const scaledWidth = baseWidth * newScale
  const scaledHeight = baseHeight * newScale
  // 计算居中偏移（先translate再scale，所以偏移量不需要除以缩放比例）
  const offsetX = (windowWidth - scaledWidth) / 2
  const offsetY = (windowHeight - scaledHeight) / 2

  return { scale: newScale, offsetX, offsetY }
}

// 初始化缩放和位置
const initScale = () => {
  const { scale: newScale, offsetX, offsetY } = calculateScaleAndPosition()
  scale.value = newScale
  translateX.value = offsetX
  translateY.value = offsetY
}

// 窗口大小变化时重新计算缩放
const handleResize = () => {
  initScale()
}

// 初始化和清理
onMounted(() => {
  initScale()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div class="screen-wrapper h-full">
    <div
      ref="screenContainer"
      class="screen-container h-full"
      :style="{
        width: `${baseWidth}px`,
        height: `${baseHeight}px`,
        paddingBottom: '1rem',
        transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
      }"
    >
      <div class="screen-content w-full h-full relative">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.screen-wrapper {
  @apply w-full h-full overflow-hidden;
  background: linear-gradient(135deg, #0f172a, #1e293b);
}

.screen-container {
  @apply transition-transform duration-300 origin-top-left absolute bg-slate-900 shadow-2xl;
  box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
}

.screen-content {
  @apply relative overflow-hidden;
}
</style>
