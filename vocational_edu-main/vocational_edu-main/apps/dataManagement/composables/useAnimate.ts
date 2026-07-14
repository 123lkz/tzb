import _ from 'lodash'
import { onBeforeUnmount, onMounted, ref } from 'vue'

export const useAnimate = (initValue: number | string) => {
  const value = ref<string | number>(initValue)
  let timer: number | null = null

  onBeforeUnmount(() => {
    if (timer && typeof window !== 'undefined') {
      window.cancelAnimationFrame(timer)
    }
  })

  let endNumber = 0
  let isFloat = false

  function update(newValue: any) {
    // 只在客户端执行
    if (typeof window === 'undefined') {
      value.value = newValue
      return
    }

    if (timer) {
      window.cancelAnimationFrame(timer)
    }
    if (typeof newValue !== 'number') {
      value.value = newValue
      return
    }
    isFloat = !_.isInteger(newValue)
    endNumber = newValue
    start()
  }

  function getOffset(delta: number) {
    if (Math.abs(delta) > 100) return delta / 5
    if (Math.abs(delta) > 20) return delta / 10

    if (isFloat) return delta / 15
    return delta > 0 ? 1 : -1
  }

  function start() {
    if (typeof window === 'undefined') {
      return
    }

    timer = window.requestAnimationFrame(() => {
      let offset = getOffset(endNumber - (value.value as number))
      if (!isFloat) {
        offset = Math.round(offset)
      }
      if (Math.abs(endNumber - (value.value as number)) <= 1) {
        value.value = endNumber
        timer = null
      } else {
        ;(value.value as number) += offset
        start()
      }
    })
  }

  // 在客户端挂载后开始动画
  onMounted(() => {
    if (typeof window !== 'undefined') {
      update(initValue)
    }
  })

  return {
    value,
    update,
  }
}
