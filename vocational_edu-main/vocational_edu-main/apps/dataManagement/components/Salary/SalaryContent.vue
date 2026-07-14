<script setup lang="ts">
import SalaryTop from './SalaryTop.vue'
import SalaryMiddle from './SalaryMiddle.vue'
import SalaryBottom from './SalaryBottom.vue'

const props = withDefaults(
  defineProps<{
    province: string
    time: string
    scope: string
  }>(),
  {
    province: '全国',
    time: 'month',
    scope: 'all',
  }
)
</script>

<template>
  <div class="w-full my-4 pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
    <SalaryTop :province="province" :time="time" :scope="scope" />
    <SalaryMiddle :province="province" :time="time" :scope="scope" />
    <SalaryBottom :province="province" :time="time" :scope="scope" />
  </div>
</template>
