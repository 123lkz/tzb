<script setup lang="ts">
import { type DataItem } from '../Echart/HotWordCloud.vue'
import EducationBottomLeft from './EducationBottomLeft.vue'
import EducationBottomMiddle from './EducationBottomMiddle.vue'
import EducationBottomRight from './EducationBottomRight.vue'

interface Props {
  schoolData: Array<{ value: number; name: string }>
  schoolStudentData: Array<{ value: number; name: string }>
  totalGraduateData: Array<{ year: string; doubleHigh: number; nonDoubleHigh: number }>
  hotProfessionData: DataItem[]
  highSalaryMajorData: DataItem[]
}

const props = defineProps<Props>()
</script>

<template>
  <div class="grid grid-cols-3 gap-4 h-full">
    <!-- 双高/非双高院校数据统计 -->
    <EducationBottomLeft
      :school-data="props.schoolData"
      :school-student-data="props.schoolStudentData"
      :total-graduate-data="props.totalGraduateData"
      :height="200"
    />
    <!-- 热门对应的关键词云图 -->
    <EducationBottomMiddle
      :hot-profession-data="props.hotProfessionData"
      :high-salary-major-data="props.highSalaryMajorData"
    />
    <!-- 工作岗位学历要求情况 -->
    <EducationBottomRight />
  </div>
</template>

<style scoped lang="scss"></style>
