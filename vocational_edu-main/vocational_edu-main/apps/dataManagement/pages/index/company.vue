<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import CompanyFilter from '~/components/common/Filter/CompanyFilter.vue'
import DashboardButton from '~/components/common/DashboardButton.vue'
import CompanyTop from '~/components/Company/CompanyTop.vue'
import CompanyMiddle from '@/components/Company/CompanyMiddle.vue'
import CompanyIndustry from '@/components/Company/CompanyIndustry.vue'
import CompanyCareer from '@/components/Company/CompanyCareer.vue'
// import CompanyDiffSituation from '~/components/Company/CompanyDiffSituation.vue'
// import CompanyBottom from '@/components/Company/CompanyBottom.vue'
// import CompanyLevel from '~/components/Company/CompanyLevel.vue'
// import Modal from '~/components/common/Modal.vue'
// import TreeChart from '@/components/Echart/TreeChart.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '单位信息', path: '/company' }
]

const province = ref('全国')
const time = ref('month')
const scope = ref('all')
const companyId = ref('')
const companyScaleName = ref('')

const handleProvinceChange = (value: string) => {
  province.value = value
}

const handleTimeChange = (value: string) => {
  time.value = value
}

const handleScopeChange = (value: string) => {
  scope.value = value
}

const handleCompanyChange = (value: string, label: string) => {
  companyId.value = value
  companyScaleName.value = label
}

const handleDashboardClick = () => {
  useRouter().push('/company-list')
}
</script>

<template>
  <div class="flex flex-col h-full p-4">
    <Header
      :breadcrumbs="breadcrumbs"
      @province-change="handleProvinceChange"
      @time-change="handleTimeChange"
      @scope-change="handleScopeChange"
    >
      <template #right-filter>
        <CompanyFilter v-model="companyId" @update:model-value="handleCompanyChange" />
      </template>
      <template #right-button>
        <DashboardButton text="单位列表" icon="icon-liebiao" @click="handleDashboardClick" />
      </template>
    </Header>
    <div class="w-full pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
      <CompanyTop :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyMiddle :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyDiffSituation :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyDivide :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyCareer :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyIndustry :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
      <CompanyBottom :province="province" :time="time" :scope="scope" :company-scale-name="companyScaleName" />
    </div>
  </div>
</template>
