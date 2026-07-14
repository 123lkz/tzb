<template>
  <svg class="iconfont" :class="iconClasses" :style="iconStyle" aria-hidden="true">
    <use :xlink:href="iconName"></use>
  </svg>
</template>

<script setup lang="ts">
/**
 * Icon 组件
 *
 * 使用说明：
 * 1. name: 图标名称，对应 iconfont.js 中的 symbol id
 * 2. size: 图标大小，可以是数字（像素）或字符串（如 '16px', '1rem'），优先使用
 * 3. width: 图标宽度，可以是数字（像素）或字符串（如 '16px', '1rem', '100%'）
 * 4. height: 图标高度，可以是数字（像素）或字符串（如 '16px', '1rem', '100%'）
 * 5. color: 图标颜色，支持任何有效的 CSS 颜色值或 Tailwind 颜色类
 *
 * 优先级：size > width/height
 * 默认大小：16px（当没有设置 size、width、height 时）
 *
 * 示例：
 * <Icon name="icon-sousuo" size="24" color="#ff0000" />
 * <Icon name="icon-guanbi" size="32" color="red" />
 * <Icon name="icon-fanhui" size="1rem" color="currentColor" />
 * <Icon name="icon-sousuo" size="24" color="text-red-500" />
 * <Icon name="icon-guanbi" size="32" color="text-blue-600" />
 * <Icon name="icon-rectangle" width="100" height="50" color="#00ff00" />
 * <Icon name="icon-custom" width="2rem" height="1rem" color="text-purple-500" />
 * <Icon name="icon-full" width="100%" color="#ff0000" />
 */
interface Props {
  name: string
  size?: string | number
  width?: string | number
  height?: string | number
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: undefined,
  width: undefined,
  height: undefined,
  color: 'currentColor',
})

const iconName = computed(() => `#${props.name}`)

// 检查是否为 Tailwind 颜色类
const isTailwindColor = computed(() => {
  return (
    props.color.startsWith('text-') || props.color.startsWith('bg-') || props.color.includes('-')
  )
})

// 计算图标类名
const iconClasses = computed(() => {
  if (isTailwindColor.value) {
    return [props.color]
  }
  return []
})

const iconStyle = computed(() => {
  // 优先使用 size，如果没有 size 则使用 width 和 height
  let width: string
  let height: string

  if (props.size !== undefined && props.size !== null) {
    // 使用 size
    const sizeValue = typeof props.size === 'number' ? `${props.size}px` : props.size
    width = sizeValue
    height = sizeValue
  } else {
    // 使用 width 和 height
    width = props.width
      ? typeof props.width === 'number'
        ? `${props.width}px`
        : props.width
      : '16px'
    height = props.height
      ? typeof props.height === 'number'
        ? `${props.height}px`
        : props.height
      : width // 如果没有设置 height，使用 width 的值
  }

  const baseStyle = {
    width,
    height,
  }

  // 如果不是 Tailwind 颜色类，则使用内联样式
  if (!isTailwindColor.value) {
    return {
      ...baseStyle,
      color: props.color,
      fill: props.color,
    }
  }

  return baseStyle
})
</script>

<style scoped>
/* 基础样式 */
.iconfont {
  display: inline-block;
  vertical-align: -0.1em;
}

/* Tailwind 颜色类支持 */
.iconfont.text-red-500 {
  color: #ef4444;
}

.iconfont.text-red-600 {
  color: #dc2626;
}

.iconfont.text-blue-500 {
  color: #3b82f6;
}

.iconfont.text-blue-600 {
  color: #2563eb;
}

.iconfont.text-green-500 {
  color: #10b981;
}

.iconfont.text-green-600 {
  color: #059669;
}

.iconfont.text-yellow-500 {
  color: #eab308;
}

.iconfont.text-yellow-600 {
  color: #ca8a04;
}

.iconfont.text-purple-500 {
  color: #8b5cf6;
}

.iconfont.text-purple-600 {
  color: #7c3aed;
}

.iconfont.text-pink-500 {
  color: #ec4899;
}

.iconfont.text-pink-600 {
  color: #db2777;
}

.iconfont.text-indigo-500 {
  color: #6366f1;
}

.iconfont.text-indigo-600 {
  color: #4f46e5;
}

.iconfont.text-gray-500 {
  color: #6b7280;
}

.iconfont.text-gray-600 {
  color: #4b5563;
}

.iconfont.text-white {
  color: #ffffff;
}

.iconfont.text-black {
  color: #000000;
}

.iconfont.text-cyan-500 {
  color: #06b6d4;
}

.iconfont.text-cyan-600 {
  color: #0891b2;
}

.iconfont.text-emerald-500 {
  color: #10b981;
}

.iconfont.text-emerald-600 {
  color: #059669;
}

.iconfont.text-orange-500 {
  color: #f97316;
}

.iconfont.text-orange-600 {
  color: #ea580c;
}

.iconfont.text-teal-500 {
  color: #14b8a6;
}

.iconfont.text-teal-600 {
  color: #0d9488;
}

.iconfont.text-lime-500 {
  color: #84cc16;
}

.iconfont.text-lime-600 {
  color: #65a30d;
}

.iconfont.text-amber-500 {
  color: #f59e0b;
}

.iconfont.text-amber-600 {
  color: #d97706;
}
</style>
