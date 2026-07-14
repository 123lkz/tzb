<template>
  <div class="flex items-center gap-4 w-96">
    <div class="flex items-center rounded-md bg-gray-700/50 p-1 text-sm text-gray-300">
      <span
        class="cursor-pointer rounded px-3 py-1"
        :class="{ 'bg-blue-600 !text-white': modelDateType === 'year' }"
        @click="$emit('update:dateType', 'year')"
      >
        年份
      </span>
      <span
        class="cursor-pointer rounded px-3 py-1"
        :class="{ 'bg-blue-600 !text-white': modelDateType === 'month' }"
        @click="$emit('update:dateType', 'month')"
      >
        月份
      </span>
      <span
        class="cursor-pointer rounded px-3 py-1"
        :class="{ 'bg-blue-600 !text-white': modelDateType === '5years' }"
        @click="$emit('update:dateType', '5years')"
      >
        近5年
      </span>
    </div>
    <div v-if="modelDateType === 'year'" class="relative">
      <div
        class="w-28 cursor-pointer rounded border-none bg-gray-800 px-2 py-1 text-center text-white"
        @click.stop="showYearPanel = !showYearPanel"
      >
        {{ modelYear }}
      </div>
      <YearSelectModal :show="showYearPanel" :selected="modelYear" @select="onYearSelect" />
    </div>
    <input
      v-else-if="modelDateType === 'month'"
      type="month"
      :value="modelMonth"
      @input="onMonthChange"
      class="rounded border-none bg-gray-800 px-2 py-1 text-center text-white"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import YearSelectModal from './YearSelectModal.vue'

const props = defineProps<{
  dateType: 'year' | 'month' | '5years'
  year: number
  month: string
}>()
const emit = defineEmits<{
  (e: 'update:dateType', val: 'year' | 'month' | '5years'): void
  (e: 'update:year', val: number): void
  (e: 'update:month', val: string): void
}>()

const showYearPanel = ref(false)

const modelDateType = computed(() => props.dateType)
const modelYear = computed(() => props.year)
const modelMonth = computed(() => props.month)

function onYearSelect(year: number) {
  emit('update:year', year)
  showYearPanel.value = false
}
function onMonthChange(e: Event) {
  emit('update:month', (e.target as HTMLInputElement).value)
}

// Hide year panel on outside click
watch(showYearPanel, val => {
  if (val) {
    const handler = () => (showYearPanel.value = false)
    window.addEventListener('click', handler, { once: true })
  }
})
</script>
