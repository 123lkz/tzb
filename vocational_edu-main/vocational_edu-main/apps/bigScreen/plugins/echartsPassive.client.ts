export default defineNuxtPlugin(() => {
  if (process.client) {
    // 重写 EventTarget.prototype.addEventListener 来强制设置 passive 选项
    const originalAddEventListener = EventTarget.prototype.addEventListener
    
    EventTarget.prototype.addEventListener = function(
      type: string,
      listener: EventListenerOrEventListenerObject,
      options?: boolean | AddEventListenerOptions
    ) {
      // 对于滚轮相关事件，强制设置为 passive
      if (type === 'wheel' || type === 'mousewheel' || type === 'DOMMouseScroll') {
        const passiveOptions = typeof options === 'object' ? { ...options, passive: true } : { passive: true }
        return originalAddEventListener.call(this, type, listener, passiveOptions)
      }
      return originalAddEventListener.call(this, type, listener, options)
    }
  }
})
