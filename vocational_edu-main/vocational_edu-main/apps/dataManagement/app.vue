<template>
  <div class="h-screen bg-[#140222] overflow-hidden">
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import { useHead } from '#imports'

const router = useRouter()

// 动态获取 baseURL
const config = useRuntimeConfig()
const baseURL = config.app.baseURL || ''

useHead({
  script: [{ src: `${baseURL}/icons/iconfont.js` }]
})

onMounted(() => {
  // 获取当前路由路径
  const currentPath = router.currentRoute.value.path

  if (currentPath === '/') {
    router.push('/position-list')
  }
})
</script>
