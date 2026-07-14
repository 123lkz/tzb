<script setup lang="ts">
import Loading from '~/components/Loading.vue'
import ResponsiveScreen from '~/components/Layout/ResponsiveScreen.vue'
import SideMenu from '~/components/SideMenu.vue'
import Header from '~/components/Layout/Header.vue'

const loading = ref(true)

onMounted(() => {
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<template>
  <!-- <Loading v-if="loading" /> -->
  <!-- <ResponsiveScreen v-else> -->
  <div class="flex w-full h-screen relative">
    <SideMenu />
    <div class="h-full flex-1 relative z-20">
      <NuxtPage />
    </div>
  </div>
  <!-- </ResponsiveScreen> -->
</template>
