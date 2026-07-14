<script setup lang="ts">
import { computed } from 'vue'
import { $position } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'
import PositionMiddleTop from '~/components/Position/PositionMiddleTop.vue'
import PositionMiddleBottom from '~/components/Position/PositionMiddleBottom.vue'
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

// 招聘人数省份排行
const { data: detailedProvinceData } = useApiData(() =>
  $position.GetScreenDataByProvince({
    dateType: props.isStatYear ? 'year' : 'month',
    caliberType: props.isStatAll ? 'all' : 'college'
  })
)

const { data: detailedIndustryData } = useApiData(() =>
  $position.GetScreenIndustryData({
    dateType: props.isStatYear ? 'year' : 'month',
    caliberType: props.isStatAll ? 'all' : 'college'
  })
)

const { data: detailedProfessionData } = useApiData(() =>
  $position.GetScreenCareerRank({
    dateType: props.isStatYear ? 'year' : 'month',
    caliberType: props.isStatAll ? 'all' : 'college'
  })
)

// 招聘总人数职业排行（标准职业分类第三级）
const professionRecruitmentData = computed(() => {
  return detailedProfessionData.value?.xiaoleiByRecruitNumber || []
})

// 招聘总人数行业排行（标准行业分类第三级），前20名
const industryRecruitmentData = computed(() => {
  return detailedIndustryData.value?.industryMediumByRecruitNumber || []
})

// 三大产业招聘总人数
const threeIndustryData = computed(() => {
  return detailedIndustryData.value?.threeIndustryByRecruitNumber || []
})

const filterDateType = computed(() => (props.isStatYear ? 'year' : 'month'))

// 使用 time.ts 中的函数获取统计时间信息
const statisticalTime = computed(() => getStatisticalTime(filterDateType.value))

/** 岗位信息上面的数据
 * 1. 省份地图数据
 * 2. 招聘总人数排行（按省份）
 * 3. 招聘总人数职业排行（标准职业分类第三级）
 * 4. 招聘总人数行业排行（标准行业分类第三级）
 * 5. 热门职业对应专业词云图
 */

// 岗位省份地图数据 - 从API获取并格式化
const provinceMapData = computed(() => {
  if (detailedProvinceData.value?.provinceData) {
    return detailedProvinceData.value.provinceData.map((item: any) => ({
      name: getProvinceName(item.province),
      value: item.totalRecruitNumber,
      totalCompanies: item.totalCompanies,
      positionCount: item.totalPositions,
      rank: item.rank
    }))
  }
  return []
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
</script>

<template>
  <div class="grid grid-rows-11 gap-4 h-full pt-4">
    <div class="row-span-8">
      <PositionMiddleTop
        :is-stat-all="isStatAll"
        :is-stat-year="isStatYear"
        :year="statisticalTime.year.toString()"
        :month="statisticalTime.month?.toString() || '1'"
        :province-map-data="provinceMapData"
        :profession-recruitment-data="professionRecruitmentData"
        :industry-recruitment-data="industryRecruitmentData"
      />
    </div>
    <div class="row-span-3">
      <PositionMiddleBottom
        :is-stat-all="isStatAll"
        :is-stat-year="isStatYear"
        :year="statisticalTime.year"
        :month="statisticalTime.month || 1"
        :company-data="companyData"
        :experience-data="experienceData"
        :education-data="educationData"
        :three-industry-data="threeIndustryData"
      />
    </div>
  </div>
</template>
