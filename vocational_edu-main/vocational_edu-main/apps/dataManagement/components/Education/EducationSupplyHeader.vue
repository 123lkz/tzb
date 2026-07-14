<script setup lang="ts">
import Icon from '../common/Icon.vue'
import Select from '../common/Select.vue'
import DashboardButton from '../common/DashboardButton.vue'
import { eduYearOptions, schoolTypeOptions } from '~/utils/constants'

const emit = defineEmits<{
  (e: 'update:year', value: string): void
  (e: 'update:school-type', value: string): void
}>()

const props = withDefaults(
  defineProps<{
    schoolType: string
    year: string
  }>(),
  {
    schoolType: 'all',
    year: '2023',
  }
)

const selectedSchoolType = ref(props.schoolType)
const selectedYear = ref(props.year)

const handleYearChange = (value: string) => {
  selectedYear.value = value
  emit('update:year', value)
}

const handleSchoolTypeChange = (value: string) => {
  selectedSchoolType.value = value
  emit('update:school-type', value)
}

const handleSchoolListClick = () => {
  useRouter().push('/education-school-list')
}
</script>

<template>
  <div
    class="flex items-center justify-between p-4 h-12 rounded-lg bg-[#00ffff0d] backdrop-blur-sm border-b border-[#00ffff]/10 shadow-[0_0_24px_0_rgba(0,255,255,0.25)] animate-[fadeInUp_0.6s_ease-out]"
  >
    <div class="flex items-center">
      <Icon name="icon-xuexiao" color="text-[#00ffff]" :size="18" />
      <h1 class="text-lg font-bold text-[#00ffff] ml-2">教育资源</h1>
      <p class="text-xs text-white/60">（数据更新到2023年）</p>
    </div>

    <div class="flex items-center gap-4">
      <!-- 过滤框 -->
      <div class="flex items-center gap-4">
        <!-- 年份选择 -->
        <div class="flex items-center gap-2">
          <label class="text-[#00ffff] font-medium flex-shrink-0">年份：</label>
          <Select
            v-model="selectedYear"
            :options="eduYearOptions"
            size="sm"
            placeholder="选择年份"
            @change="handleYearChange"
          />
        </div>

        <!-- 学校类型选择 -->
        <div class="flex items-center gap-2">
          <label class="text-[#00ffff] font-medium">学校：</label>
          <div
            class="flex gap-0.5 bg-[rgba(0,255,255,0.05)] rounded-md p-0.5 border border-[rgba(0,255,255,0.1)]"
          >
            <button
              v-for="option in schoolTypeOptions"
              :key="option.value"
              :class="[
                'py-1 px-2 border-none text-xs font-medium rounded cursor-pointer transition-all duration-300 ease-in-out whitespace-nowrap hover:text-[#00ffff] hover:bg-[rgba(0,255,255,0.1)]',
                selectedSchoolType === option.value
                  ? 'bg-[rgba(0,255,255,0.2)] text-[#00ffff] shadow-[0_1px_4px_rgba(0,234,255,0.3)]'
                  : 'bg-transparent text-[rgba(176,196,222,0.8)]',
              ]"
              @click="handleSchoolTypeChange(option.value)"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- 学校列表按钮 -->
      <DashboardButton
        text="学校列表"
        icon="icon-arrow-right"
        :icon-size="14"
        @click="handleSchoolListClick"
      />
    </div>
  </div>
</template>
