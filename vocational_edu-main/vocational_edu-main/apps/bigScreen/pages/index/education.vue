<script setup lang="ts">
import EducationMiddleTop from '~/components/Education/EducationMiddleTop.vue'
import EducationMiddleBottom from '~/components/Education/EducationMiddleBottom.vue'
import positionData from '~/data/position'
import salaryData from '~/data/salary'
import { processHotWordsData } from '~/utils/wordsData'
import { $schoolEnrollment } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'
import { getProvinceName } from '~/utils/name'

interface ProvinceMapData {
  name: string
  value: number
  doubleHighValue: number
  juniorCollegesValue: number
}

const props = withDefaults(
  defineProps<{
    isStatAll: boolean
    isStatYear: boolean
  }>(),
  {
    isStatAll: true,
    isStatYear: false
  }
)
const filterQuantityType = computed(() => (props.isStatAll ? 'all' : 'college'))
const filterDateType = computed(() => (props.isStatYear ? 'year' : 'month'))

const hotProfessionData = computed(() => {
  if (positionData[filterDateType.value][filterQuantityType.value]) {
    return processHotWordsData(positionData[filterDateType.value][filterQuantityType.value].hotWordsData as any)
  }
})

const highSalaryWordsData = computed(() => {
  if (salaryData[filterDateType.value][filterQuantityType.value]) {
    return processHotWordsData(salaryData[filterDateType.value][filterQuantityType.value].highSalaryWordsData as any)
  }
})

// 大专职业院校在校人数省份地图数据
const provinceMapData = ref<ProvinceMapData[]>([])

type RemoteProvinceItem = {
  name: string
  value: number
  rank?: number
  doubleHighNum?: number
}

// 各省学生数
const { data: remoteProvinceData } = useApiData(() => $schoolEnrollment.GetStudentNumByProvince({ category: '专科' }))

// 各省学校数
const { data: schoolProvinceData } = useApiData(() =>
  $schoolEnrollment.GetSchoolNumByProvince({
    category: '专科',
    year: 2022
  })
)

// 各专业学生数
const { data: StudentNumByMajorData } = useApiData(() => $schoolEnrollment.GetStudentNumByMajor({ category: '专科' }))

// 各年学生数 在校生、毕业生、招生数
const { data: StudentNumByYearData } = useApiData(() => $schoolEnrollment.GetStudentNumByYear({ category: '专科' }))

// 双高/非双高学校数
const { data: SchoolNumData } = useApiData(() => $schoolEnrollment.GetSchoolNum({}))

watchEffect(() => {
  const studentList = remoteProvinceData?.value
  const schoolList = (globalThis as any).structuredClone
    ? (schoolProvinceData?.value as RemoteProvinceItem[] | undefined)
    : schoolProvinceData?.value

  if (Array.isArray(studentList) || Array.isArray(schoolList)) {
    const byName: Record<string, ProvinceMapData> = {}

    if (Array.isArray(studentList)) {
      studentList.forEach((item) => {
        const name = getProvinceName(item.name)
        byName[name] = {
          name,
          value: Number(item.value ?? 0),
          doubleHighValue: 0,
          juniorCollegesValue: 0
        }
      })
    }

    if (Array.isArray(schoolList)) {
      schoolList.forEach((item) => {
        const name = getProvinceName(item.name)
        const target = byName[name] || {
          name,
          value: 0,
          doubleHighValue: 0,
          juniorCollegesValue: 0
        }
        target.juniorCollegesValue = Number(item.value ?? 0)
        target.doubleHighValue = Number((item as any).doubleHighNum ?? 0)
        byName[name] = target
      })
    }

    provinceMapData.value = Object.values(byName)
  }
})

const formatProvinceMapData = computed(() => {
  return provinceMapData.value.map((item: ProvinceMapData, index: number) => {
    return {
      ...item,
      rank: index + 1
    }
  })
})

// 各省各省大专职业院校数排行（单位：个）
const schoolNumberRecruitmentData = computed(() => {
  return schoolProvinceData.value.map((item: ProvinceMapData) => {
    return {
      name: item.name,
      value: item.value,
      rank: item.rank
    }
  })
})

// 双高/非双高院校在校生数（来自 2022 年数据）
const school2022Data = computed(() => StudentNumByYearData.value?.list?.find((item: any) => item.year === 2022))
const schoolStudentData = computed(() => [
  {
    name: '双高大专院校在校生数',
    value: Number(school2022Data.value?.dhInSchoolNum ?? 0)
  },
  {
    name: '非双高大专院校在校生数',
    value: Number(school2022Data.value?.ndhInSchoolNum ?? 0)
  }
])

// 总毕业生（按接口返回映射 dhGraduateNum / ndhGraduateNum）
const totalGraduateData = computed(() => {
  const list: any[] = StudentNumByYearData.value?.list ?? []
  return list.map((item) => ({
    year: String(item.year),
    total: Number(item.dhGraduateNum ?? 0) + Number(item.ndhGraduateNum ?? 0),
    doubleHigh: Number(item.dhGraduateNum ?? 0),
    nonDoubleHigh: Number(item.ndhGraduateNum ?? 0)
  }))
})
</script>

<template>
  <div class="grid grid-rows-11 gap-4 h-full pt-4">
    <div v-if="formatProvinceMapData && StudentNumByMajorData && SchoolNumData" class="row-span-8">
      <EducationMiddleTop
        :province-map-data="formatProvinceMapData"
        :school-number-recruitment-data="schoolNumberRecruitmentData"
        :major-student-recruitment-data="StudentNumByMajorData"
      />
    </div>
    <div
      v-if="SchoolNumData && schoolStudentData && totalGraduateData && hotProfessionData && highSalaryWordsData"
      class="row-span-3"
    >
      <EducationMiddleBottom
        :school-data="SchoolNumData"
        :school-student-data="schoolStudentData"
        :total-graduate-data="totalGraduateData"
        :hot-profession-data="hotProfessionData"
        :high-salary-major-data="highSalaryWordsData"
      />
    </div>
  </div>
</template>
