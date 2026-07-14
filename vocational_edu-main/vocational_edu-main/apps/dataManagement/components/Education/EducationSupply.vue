<script setup lang="ts">
import EducationSupplyHeader from './EducationSupplyHeader.vue'
import EducationSupplyTop from './EducationSupplyTop.vue'
import EducationSupplyBottom from './EducationSupplyBottom.vue'
import EducationSupplyPostgraduates from './EducationPostgraduates.vue'

const schoolType = ref('all')
const year = ref('2023')

const handleYearChange = (value: string) => {
  year.value = value
}

const handleSchoolTypeChange = (value: string) => {
  schoolType.value = value
}
</script>

<template>
  <div class="w-full h-full space-y-6">
    <EducationSupplyHeader
      :school-type="schoolType"
      :year="year"
      @update:year="handleYearChange"
      @update:school-type="handleSchoolTypeChange"
    />
    <EducationSupplyTop :school-type="schoolType" :year="year" />
    <EducationSupplyBottom :school-type="schoolType" :year="year" />
    <EducationSupplyPostgraduates />
  </div>
</template>
