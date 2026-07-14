<template>
  <div class="h-screen bg-[#140222] overflow-hidden">
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
// 应用入口
const router = useRouter()

onMounted(() => {
  // 获取当前路由路径
  const currentPath = router.currentRoute.value.path

  // 如果当前路径不是 /position，则跳转到 /position
  if (currentPath === '/') {
    router.push('/position')
  }
})
</script>
