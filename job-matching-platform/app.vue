<template>
<div class="h-screen bg-[#140222] overflow-hidden flex text-[rgba(176,196,222,0.9)] font-sans">
  <SideMenu />
  <main class="flex-1 overflow-y-auto custom-scrollbar p-4"><NuxtPage /></main>
</div>
</template>
<script setup lang="ts">
import SideMenu from "~/components/Layout/SideMenu.vue"
</script>
<style>body{margin:0;padding:0;background:#140222}*{box-sizing:border-box}</style>
