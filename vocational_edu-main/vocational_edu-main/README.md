## 使用阿里巴巴图标

### 基本使用方式

```vue
<template>
  <div>
    <!-- 使用 svg 图标 -->
    <Icon name="Icon:icon-name" />

    <!-- 带样式的图标 -->
    <Icon name="Icon:icon-name" size="24" color="#ff0000" class="custom-class" />

    <!-- 使用原始 i 标签方式 -->
    <svg class="icon" aria-hidden="true">
      <use xlink:href="#icon-name"></use>
    </svg>
  </div>
</template>

<style>
.icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}
</style>
```

### 动态使用图标

```vue
<script setup>
const iconName = ref('home')
</script>

<template>
  <Icon :name="`Icon:icon-${iconName}`" />
</template>
```

### 批量导入图标 (推荐)

创建 composables/useIcons.ts：

```ts
// composables/useIcons.ts
export const useIcons = () => {
  const icons = {
    home: 'icon-home',
    user: 'icon-user',
    settings: 'icon-settings',
    // 添加更多图标...
  }

  const getIcon = (name: keyof typeof icons) => `Icon:${icons[name]}`

  return { icons, getIcon }
}
```

然后在组件中使用：

```vue
<script setup>
const { getIcon } = useIcons()
</script>

<template>
  <Icon :name="getIcon('home')" />
</template>
```
