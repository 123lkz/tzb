<script setup lang="ts">
import SalaryContent from '~/components/Salary/SalaryContent.vue'
import Header from '@/components/Layout/Header.vue'
import DashboardButton from '@/components/common/DashboardButton.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '薪酬信息', path: '/salary' },
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
  useRouter().push('/salary-list')
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
          <DashboardButton text="薪酬列表" icon="icon-liebiao" @click="handleDashboardClick" />
        </template>
      </Header>
    </div>
    <SalaryContent :province="province" :time="time" :scope="scope" />
  </div>
</template>
