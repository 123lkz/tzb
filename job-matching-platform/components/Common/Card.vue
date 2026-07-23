<script setup lang="ts">defineProps<{hover?:boolean}>()</script>
<template><div class="bg-[rgba(0,255,255,0.08)] backdrop-blur-sm rounded-lg border border-[rgba(0,255,255,0.15)] p-4" :class="{'card-hover':hover}"><slot/></div></template>
<style scoped>.card-hover{transition:all 0.3s ease}.card-hover:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(0,255,255,0.15)}</style>
