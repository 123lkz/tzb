<script setup lang="ts">
import PositionContent from '@/components/Position/PositionContent.vue'
import Header from '@/components/Layout/Header.vue'
import DashboardButton from '@/components/common/DashboardButton.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '职位信息', path: '/position' },
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
  useRouter().push('/position-list')
}
</script>

<template>
  <div class="flex flex-col h-full overflow-y-auto pl-4 pt-4">
    <div class="flex-shrink-0 mr-4">
      <Header
        :breadcrumbs="breadcrumbs"
        @province-change="handleProvinceChange"
        @time-change="handleTimeChange"
        @scope-change="handleScopeChange"
      >
        <template #right-button>
          <DashboardButton text="职位列表" icon="icon-liebiao" @click="handleDashboardClick" />
        </template>
      </Header>
    </div>
    <PositionContent :province="province" :time="time" :scope="scope" />
  </div>
</template>
