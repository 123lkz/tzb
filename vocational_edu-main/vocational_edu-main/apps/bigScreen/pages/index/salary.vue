<script setup lang="ts">
import { computed } from 'vue'
import { $salary, $position } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'
import SalaryMiddleTop from '~/components/Salary/SalaryMiddleTop.vue'
import SalaryMiddleBottom from '~/components/Salary/SalaryMiddleBottom.vue'
import { getStatisticalTime } from '~/utils/time'
import { getProvinceName } from '~/utils/name'

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

// 使用 time.ts 中的函数获取统计时间信息
const statisticalTime = computed(() => getStatisticalTime(filterDateType.value))

const { data: detailedSalaryData } = useApiData(() =>
  $salary.GetScreenTotalData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

const { data: detailedProvinceData } = useApiData(() =>
  $salary.GetScreenProvinceData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

const { data: detailedCareerData } = useApiData(() =>
  $salary.GetScreenCareerData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

const { data: detailedIndustryData } = useApiData(() =>
  $salary.GetScreenIndustryData({ dateType: filterDateType.value, caliberType: filterQuantityType.value })
)

/** 薪酬信息上面的数据
 * 1. 薪酬省份地图数据
 * 2. 薪资中位数排行（按省份）
 * 3. 薪资中位数职业排行（标准职业分类第三级）
 * 4. 薪资中位数行业排行（标准行业分类第三级）
 * 5. 高薪职业对应专业词云图
 */
const nationalMedianSalaryValue = computed(() => {
  return detailedSalaryData.value?.p50Salary
})

// 薪酬省份地图数据
const formatProvinceMapData = computed(() => {
  if (!detailedProvinceData.value?.provinceData) return []

  return detailedProvinceData.value.provinceData.map((item) => ({
    name: getProvinceName(item.province),
    value: item.medianSalary,
    rank: item.rank,
    percent: (((item.medianSalary - nationalMedianSalaryValue.value) / nationalMedianSalaryValue.value) * 100).toFixed(
      2
    )
  }))
})

// 薪资中位数职业排行（标准职业分类第三级）
const professionRecruitmentData = computed(() => {
  return detailedCareerData.value?.standardXiaoleiRanking || []
})

// 薪资中位数行业排行（标准行业分类第三级），前20名
const industryRecruitmentData = computed(() => {
  return detailedIndustryData.value?.industryRankBySalary || []
})

/** 岗位信息下面的数据
 * 1. 招聘单位/公司规模
 * 2. 工作岗位经验要求
 * 3. 工作岗位学历要求
 */
const { data: detailedDistributionData } = useApiData(() =>
  $position.GetScreenDistributionData({
    dateType: props.isStatYear ? 'year' : 'month',
    caliberType: props.isStatAll ? 'all' : 'college'
  })
)

// 招聘单位/公司规模
const companyData = computed(() => {
  return (
    detailedDistributionData.value?.companySizeDistribution?.map((item) => ({
      name: item.name === '-' ? '其他' : item.name,
      value: item.value
    })) || []
  )
})

// 工作岗位经验要求
const experienceData = computed(() => {
  return detailedDistributionData.value?.workingExpRequirement || []
})

// 工作岗位学历要求
const educationData = computed(() => {
  return detailedDistributionData.value?.educationRequirement || []
})

// 三大产业薪资中位数
const threeIndustrySalaryData = computed(() => {
  return detailedIndustryData.value?.threeIndustriesBySalary || []
})
</script>

<template>
  <div class="grid grid-rows-11 gap-4 h-full pt-4">
    <div class="row-span-8">
      <SalaryMiddleTop
        :province-map-data="formatProvinceMapData"
        :profession-recruitment-data="professionRecruitmentData"
        :industry-recruitment-data="industryRecruitmentData"
      />
    </div>
    <div class="row-span-3">
      <SalaryMiddleBottom
        :is-stat-all="isStatAll"
        :is-stat-year="isStatYear"
        :year="statisticalTime.year"
        :month="statisticalTime.month || 1"
        :company-data="companyData"
        :experience-data="experienceData"
        :education-data="educationData"
        :three-industry-salary-data="threeIndustrySalaryData"
      />
    </div>
  </div>
</template>
