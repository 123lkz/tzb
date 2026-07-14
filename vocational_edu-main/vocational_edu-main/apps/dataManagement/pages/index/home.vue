<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import HomeTop from '~/components/Home/HomeTop.vue'
import HomeBottom from '~/components/Home/HomeBottom.vue'
import DashboardButton from '~/components/common/DashboardButton.vue'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '数据总览', path: '/home' },
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
  window.open('https://tte.smartedu.work/zjscreen', '_blank')
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
      <template #right-button>
        <DashboardButton text="数据大屏" icon="icon-gaikuang" @click="handleDashboardClick" />
      </template>
    </Header>
    <HomeTop :province="province" :time="time" :scope="scope" />
    <HomeBottom :province="province" :time="time" :scope="scope" />
  </div>
</template>
