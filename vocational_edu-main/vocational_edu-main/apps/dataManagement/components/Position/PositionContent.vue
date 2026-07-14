<script setup lang="ts">
import PositionTop from './PositionTop.vue'
import PositionMiddle from './PositionMiddle.vue'
import PositionRank from './PositionRank.vue'
import PositionBottom from './PositionBottom.vue'

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
  <div class="w-full my-4 pr-4 flex flex-col overflow-y-auto custom-scrollbar">
    <PositionTop :province="province" :time="time" :scope="scope" />
    <PositionMiddle />
    <PositionRank />
    <PositionBottom />
  </div>
</template>
