<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { createPopper } from '@popperjs/core'
import type { Placement, Instance } from '@popperjs/core'

interface Props {
  content?: string | (() => any) // 支持字符串或渲染函数
  placement?: Placement
  delay?: number
  disabled?: boolean
  // 新增：是否使用默认的触发元素样式
  useDefaultTriggerStyle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  content: 'Tooltip content',
  placement: 'top',
  delay: 100,
  disabled: false,
  useDefaultTriggerStyle: true,
})

const show = ref(false)
const triggerRef = ref<HTMLElement | null>(null)
const tooltipRef = ref<HTMLElement | null>(null)
const tooltipContainer = ref<HTMLElement | null>(null)
let popperInstance: Instance | null = null
let timeout: NodeJS.Timeout | null = null

// 计算 content 是否为函数
const isContentFunction = computed(() => typeof props.content === 'function')

onMounted(() => {
  // 创建 tooltip 容器并添加到 body
  if (!tooltipContainer.value) {
    tooltipContainer.value = document.createElement('div')
    tooltipContainer.value.id = 'tooltip-container'
    tooltipContainer.value.style.position = 'fixed'
    tooltipContainer.value.style.top = '0'
    tooltipContainer.value.style.left = '0'
    tooltipContainer.value.style.width = '100%'
    tooltipContainer.value.style.height = '100%'
    tooltipContainer.value.style.pointerEvents = 'none'
    tooltipContainer.value.style.zIndex = '999999'
    document.body.appendChild(tooltipContainer.value)
  }

  nextTick(() => {
    if (triggerRef.value && tooltipRef.value && tooltipContainer.value) {
      // 将 tooltip 移动到 body 层级
      tooltipContainer.value.appendChild(tooltipRef.value)

      popperInstance = createPopper(triggerRef.value, tooltipRef.value, {
        placement: props.placement,
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 8],
            },
          },
          {
            name: 'preventOverflow',
            options: {
              padding: 16,
            },
          },
          {
            name: 'flip',
            options: {
              fallbackPlacements: ['top', 'right', 'bottom', 'left'],
            },
          },
        ],
      })
    }
  })
})

onBeforeUnmount(() => {
  if (popperInstance) {
    popperInstance.destroy()
  }
  if (timeout) {
    clearTimeout(timeout)
  }
  // 清理 tooltip 容器
  if (tooltipContainer.value) {
    document.body.removeChild(tooltipContainer.value)
    tooltipContainer.value = null
  }
})

const enterHandler = () => {
  if (props.disabled) return
  if (timeout) clearTimeout(timeout)
  timeout = setTimeout(() => {
    show.value = true
    nextTick(() => {
      popperInstance?.update()
    })
  }, props.delay)
}

const leaveHandler = () => {
  if (timeout) clearTimeout(timeout)
  show.value = false
}

// 点击外部关闭tooltip
const handleClickOutside = (event: MouseEvent) => {
  if (tooltipRef.value && !tooltipRef.value.contains(event.target as Node)) {
    show.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="tooltip-container relative inline-block">
    <div
      ref="triggerRef"
      class="trigger-element"
      :class="{
        'text-blue-600 cursor-pointer underline decoration-dotted':
          useDefaultTriggerStyle && !$slots.trigger,
      }"
      @mouseenter="enterHandler"
      @mouseleave="leaveHandler"
      @click="show = !show"
    >
      <!-- 优先使用具名插槽 trigger -->
      <slot name="trigger">
        <!-- 如果 content 是函数，渲染函数内容 -->
        <component v-if="isContentFunction" :is="content" />
        <!-- 否则显示字符串内容 -->
        <span class="text-gray-600 text-xs whitespace-nowrap break-all" v-else>
          {{ content }}
        </span>
      </slot>
    </div>

    <div
      ref="tooltipRef"
      class="tooltip"
      :class="{
        'opacity-100 visible': show,
        'opacity-0 invisible': !show,
      }"
      role="tooltip"
      style="position: absolute; z-index: 999999"
    >
      <div
        class="tooltip-content bg-white text-black text-sm py-2 px-3 rounded-md shadow-lg border border-gray-200"
      >
        <!-- 优先使用默认插槽 -->
        <slot>
          <!-- 如果 content 是函数，渲染函数内容 -->
          <component v-if="isContentFunction" :is="content" />
          <!-- 否则显示字符串内容 -->
          <span class="text-gray-600 text-xs whitespace-nowrap break-all" v-else>
            {{ content }}
          </span>
        </slot>
      </div>
      <div class="tooltip-arrow" data-popper-arrow></div>
    </div>
  </div>
</template>

<style scoped>
.tooltip {
  position: absolute;
  z-index: 999999;
  transition: opacity 0.2s ease, visibility 0.2s ease;
  pointer-events: none;
}

.tooltip-content {
  position: relative;
  z-index: 10;
  pointer-events: auto;
}

.tooltip-arrow,
.tooltip-arrow::before {
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
  z-index: -1;
}

.tooltip-arrow::before {
  content: '';
  transform: rotate(45deg);
  background: #fff;
}

.tooltip[data-popper-placement^='top'] > .tooltip-arrow {
  bottom: -4px;
}

.tooltip[data-popper-placement^='bottom'] > .tooltip-arrow {
  top: -4px;
}

.tooltip[data-popper-placement^='left'] > .tooltip-arrow {
  right: -4px;
}

.tooltip[data-popper-placement^='right'] > .tooltip-arrow {
  left: -4px;
}
</style>
