<template>
  <div
    v-if="show"
    class="absolute top-full left-1/2 z-50 mt-2 w-64 -translate-x-1/2 transform rounded-lg bg-gray-800 p-4 shadow-xl"
  >
    <div class="grid grid-cols-4 gap-2 text-center">
      <span
        v-for="year in years"
        :key="year"
        class="cursor-pointer rounded-md p-2 text-white transition"
        :class="{
          'bg-blue-600 !text-white': year === selected,
          'hover:bg-gray-700': year !== selected,
        }"
        @click="selectYear(year)"
      >
        {{ year }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  show: boolean
  selected: number
}>()

const emit = defineEmits<{
  (e: 'select', year: number): void
}>()

const currentYear = new Date().getFullYear()
const years = computed(() => {
  const yearList = []
  for (let i = currentYear; i >= 2018; i--) {
    yearList.push(i)
  }
  return yearList
})

function selectYear(year: number) {
  emit('select', year)
}
</script>
