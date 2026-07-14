<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const currentDateTime = ref('')
let timer: number | null = null

const updateDateTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const weekday = weekdays[now.getDay()]
  currentDateTime.value = `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds} ${weekday}`
}

onMounted(() => {
  updateDateTime()
  // 每秒更新一次时间
  timer = window.setInterval(updateDateTime, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<template>
  <div class="header-container">
    <div class="title-wrapper">
      <div class="line-decoration">
        <svg width="100%" height="70" viewBox="0 0 1000 70" preserveAspectRatio="none">
          <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color: #00ffff; stop-opacity: 0" />
              <stop offset="5%" style="stop-color: #00ffff; stop-opacity: 0.5" />
              <stop offset="10%" style="stop-color: #00ffff; stop-opacity: 1" />
              <stop offset="25%" style="stop-color: #00ffff; stop-opacity: 0.8" />
              <stop offset="50%" style="stop-color: #00bfff; stop-opacity: 0.9" />
              <stop offset="75%" style="stop-color: #00ffff; stop-opacity: 0.8" />
              <stop offset="90%" style="stop-color: #00ffff; stop-opacity: 1" />
              <stop offset="95%" style="stop-color: #00ffff; stop-opacity: 0.5" />
              <stop offset="100%" style="stop-color: #00ffff; stop-opacity: 0" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <path
            class="animated-line"
            d="M0,15 Q5,15 10,15 L300,15 Q310,15 315,15 Q320,15 325,35 Q330,55 335,55 L665,55 Q670,55 675,55 Q680,55 685,35 Q690,15 695,15 L990,15 Q995,15 1000,15"
          />
        </svg>
      </div>
      <h1 class="glowing-title">国家职业教育人才供需动态匹配平台</h1>
      <div class="date-info">
        <svg class="clock-icon" viewBox="0 0 24 24" width="20" height="20">
          <path
            fill="currentColor"
            d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"
          />
        </svg>
        <span class="date-time">{{ currentDateTime }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-container {
  height: 5rem;
  backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 0 10px;
  position: relative;
  overflow: hidden;
}

.title-wrapper {
  position: relative;
  text-align: center;
  padding-top: 20px;
}

.glowing-title {
  color: #fff;
  font-size: clamp(1.2rem, 4vw, 2.2rem);
  font-weight: bold;
  margin: 0;
  position: absolute;
  left: 50%;
  top: 45%;
  transform: translate(-50%, -50%);
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5), 0 0 20px rgba(255, 255, 255, 0.3),
    0 0 30px rgba(255, 255, 255, 0.2);
  animation: glow 2s ease-in infinite alternate;
  white-space: nowrap;
  width: 100%;
  text-align: center;
  padding: 0 20px;
  box-sizing: border-box;
}

.line-decoration {
  position: relative;
  width: 100%;
  height: 70px;
}

.animated-line {
  stroke: url(#lineGradient);
  stroke-width: 4;
  fill: none;
  filter: url(#glow);
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5), 0 0 20px rgba(255, 255, 255, 0.3),
      0 0 30px rgba(255, 255, 255, 0.2);
  }
  to {
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 30px rgba(255, 255, 255, 0.5),
      0 0 40px rgba(255, 255, 255, 0.3);
  }
}

.date-info {
  position: absolute;
  right: 20px;
  bottom: 10px;
  text-align: right;
  color: #00ffff;
  font-size: 1rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  display: flex;
  align-items: center;
  gap: 8px;
}

.clock-icon {
  color: #00ffff;
  filter: drop-shadow(0 0 5px rgba(0, 255, 255, 0.5));
}

.date-time {
  font-weight: 500;
  letter-spacing: 1px;
}
</style>
