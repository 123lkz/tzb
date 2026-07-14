<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: string
    showWeekly: boolean
  }>(),
  {
    modelValue: 'month',
    showWeekly: false,
  }
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const handleChange = (value: string) => {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="flex items-center gap-2">
    <label class="text-sm text-[#00eaff] font-medium uppercase tracking-wider">时间：</label>
    <div class="flex gap-2">
      <label
        v-if="showWeekly"
        class="flex items-center gap-2 cursor-pointer py-1 px-2 rounded transition-all duration-300 ease-in-out bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.2)] hover:bg-[rgba(0,255,255,0.1)] hover:border-[rgba(0,255,255,0.3)]"
      >
        <input
          :checked="props.modelValue === 'weekly'"
          type="radio"
          name="timeDimension"
          value="weekly"
          class="appearance-none w-3 h-3 border-[1.5px] border-[rgba(0,255,255,0.3)] rounded-full bg-transparent cursor-pointer relative transition-all duration-300 ease-in-out checked:border-[#00eaff] checked:bg-[#00eaff]"
          @change="handleChange('weekly')"
        />
        <span
          class="text-xs text-[rgba(176,196,222,0.9)] font-medium transition-colors duration-300 ease-in-out"
          >周度</span
        >
      </label>
      <label
        class="flex items-center gap-2 cursor-pointer py-1 px-2 rounded transition-all duration-300 ease-in-out bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.2)] hover:bg-[rgba(0,255,255,0.1)] hover:border-[rgba(0,255,255,0.3)]"
      >
        <input
          :checked="props.modelValue === 'month'"
          type="radio"
          name="timeDimension"
          value="month"
          class="appearance-none w-3 h-3 border-[1.5px] border-[rgba(0,255,255,0.3)] rounded-full bg-transparent cursor-pointer relative transition-all duration-300 ease-in-out checked:border-[#00eaff] checked:bg-[#00eaff]"
          @change="handleChange('month')"
        />
        <span
          class="text-xs text-[rgba(176,196,222,0.9)] font-medium transition-colors duration-300 ease-in-out"
          >月度</span
        >
      </label>
      <label
        class="flex items-center gap-2 cursor-pointer py-1 px-2 rounded transition-all duration-300 ease-in-out bg-[rgba(0,255,255,0.05)] border border-[rgba(0,255,255,0.2)] hover:bg-[rgba(0,255,255,0.1)] hover:border-[rgba(0,255,255,0.3)]"
      >
        <input
          :checked="props.modelValue === 'year'"
          type="radio"
          name="timeDimension"
          value="year"
          class="appearance-none w-3 h-3 border-[1.5px] border-[rgba(0,255,255,0.3)] rounded-full bg-transparent cursor-pointer relative transition-all duration-300 ease-in-out checked:border-[#00eaff] checked:bg-[#00eaff]"
          @change="handleChange('year')"
        />
        <span
          class="text-xs text-[rgba(176,196,222,0.9)] font-medium transition-colors duration-300 ease-in-out"
          >年度</span
        >
      </label>
    </div>
  </div>
</template>

<style scoped>
/* 自定义单选按钮选中状态的内圆点 */
input[type='radio']:checked::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 4px;
  height: 4px;
  background: #1a2980;
  border-radius: 50%;
}

/* 单选按钮选中时文字颜色变化 */
input[type='radio']:checked + span {
  color: #00eaff;
}
</style>
