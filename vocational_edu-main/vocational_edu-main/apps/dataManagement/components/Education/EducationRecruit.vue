<script setup lang="ts">
import EducationRecruitTop from './EducationRecruitTop.vue'
import EducationRecruitMiddle from './EducationRecruitMiddle.vue'
import EducationRecruitBottom from './EducationRecruitBottom.vue'

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
  <div class="mb-8">
    <EducationRecruitTop :province="province" :time="time" :scope="scope" />
    <EducationRecruitMiddle :province="province" :time="time" :scope="scope" />
    <EducationRecruitBottom :province="province" :time="time" :scope="scope" />
  </div>
</template>
