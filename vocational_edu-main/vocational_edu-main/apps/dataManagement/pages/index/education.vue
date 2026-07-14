<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import DashboardButton from '@/components/common/DashboardButton.vue'
import EducationRecruit from '~/components/Education/EducationRecruit.vue'
import EducationSupply from '~/components/Education/EducationSupply.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '薪酬信息', path: '/education' },
]

const province = ref('全国')
const time = ref('month')
const scope = ref('all')

const handleProvinceChange = (value: string) => {
  province.value = value
}

const handleTimeChange = (value: string) => {
  time.value = value
}
const handleScopeChange = (value: string) => {
  scope.value = value
}

const handleDashboardClick = () => {
  useRouter().push('/education-major-list')
}
</script>

<template>
  <div class="flex flex-col h-full overflow-y-auto overflow-x-hidden pl-4 pt-4">
    <div class="flex-shrink-0 mr-4">
      <Header
        :breadcrumbs="breadcrumbs"
        @province-change="handleProvinceChange"
        @time-change="handleTimeChange"
        @scope-change="handleScopeChange"
      >
        <template #right-button>
          <DashboardButton text="专业列表" icon="icon-liebiao" @click="handleDashboardClick" />
        </template>
      </Header>
    </div>
    <div class="w-full my-4 pr-4 flex flex-col overflow-y-auto overflow-x-hidden custom-scrollbar">
      <EducationRecruit :province="province" :time="time" :scope="scope" />
      <EducationSupply />
    </div>
  </div>
</template>

s
