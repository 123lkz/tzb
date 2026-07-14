<template>
  <div class="dashboard-content w-full h-full p-6">
    <div class="grid-container">
      <!-- 顶部状态卡片 -->
      <div v-for="(stat, index) in stats" :key="index" class="stat-card">
        <div class="value">{{ stat.value }}</div>
        <div class="label">{{ stat.label }}</div>
      </div>

      <!-- 图表区域 -->
      <div class="grid-cell row-span-2">
        <h3>访问量趋势</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-4/5 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg flex items-center justify-center"
          >
            <span>折线图区域</span>
          </div>
        </div>
      </div>

      <div class="grid-cell">
        <h3>用户分布</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-3/4 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-lg flex items-center justify-center"
          >
            <span>饼图区域</span>
          </div>
        </div>
      </div>

      <div class="grid-cell">
        <h3>实时监控</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-3/4 bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-lg flex items-center justify-center"
          >
            <span>仪表盘</span>
          </div>
        </div>
      </div>

      <div class="grid-cell row-span-2">
        <h3>地域分布</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-4/5 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-lg flex items-center justify-center"
          >
            <span>地图区域</span>
          </div>
        </div>
      </div>

      <div class="grid-cell">
        <h3>设备占比</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-3/4 bg-gradient-to-r from-rose-500/20 to-pink-500/20 rounded-lg flex items-center justify-center"
          >
            <span>环形图</span>
          </div>
        </div>
      </div>

      <div class="grid-cell">
        <h3>流量来源</h3>
        <div class="chart">
          <div
            class="mock-chart w-full h-3/4 bg-gradient-to-r from-violet-500/20 to-fuchsia-500/20 rounded-lg flex items-center justify-center"
          >
            <span>漏斗图</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const stats = ref([
  { value: '1,248', label: '今日访问量' },
  { value: '86%', label: '转化率' },
  { value: '¥42,589', label: '今日销售额' },
  { value: '32', label: '新增用户' },
])
</script>

<style scoped>
.dashboard-content {
  @apply w-full h-full;
}

.grid-container {
  @apply grid grid-cols-4 grid-rows-[120px_1fr_1fr] gap-5 h-full;
}

.stat-card {
  @apply flex flex-col justify-center items-center rounded-lg bg-slate-800/50 p-4 shadow-md;
}

.stat-card .value {
  @apply text-3xl font-bold text-sky-500 my-1;
}

.stat-card .label {
  @apply text-sm text-slate-400;
}

.grid-cell {
  @apply bg-white/5 border border-white/10 rounded-lg p-4 shadow-md;
}

.grid-cell h3 {
  @apply mt-0 text-sky-400 font-semibold;
}

.chart {
  @apply h-full flex items-center justify-center text-slate-400 font-medium;
}

.mock-chart {
  @apply w-full rounded-lg flex items-center justify-center;
}
</style>
