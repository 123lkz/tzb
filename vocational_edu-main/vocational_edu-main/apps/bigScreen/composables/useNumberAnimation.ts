import { ref, computed } from 'vue'

export const useNumberAnimation = () => {
  const animatedValue = ref(0)
  let animationTimer: number | null = null

  // 清理定时器
  const clearTimer = () => {
    if (animationTimer) {
      clearTimeout(animationTimer)
      animationTimer = null
    }
  }

  // 数字动画方法
  const animateNumber = (targetValue: number, duration: number = 500) => {
    clearTimer()

    const startValue = 0
    const startTime = Date.now()

    const animate = () => {
      const currentTime = Date.now()
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)

      // 使用缓动函数让动画更自然
      const easeOutQuart = 1 - Math.pow(1 - progress, 4)
      const currentValue = Math.round(startValue + (targetValue - startValue) * easeOutQuart)

      animatedValue.value = currentValue

      if (progress < 1) {
        animationTimer = window.setTimeout(animate, 16) // 约60fps
      } else {
        animatedValue.value = targetValue
      }
    }

    animate()
  }

  // 格式化数字显示（添加千分位分隔符）
  const formatNumber = (num: number): string => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  }

  // 获取格式化后的动画值
  const formattedValue = computed(() => formatNumber(animatedValue.value))

  return {
    animatedValue,
    formattedValue,
    animateNumber,
    clearTimer,
  }
}
