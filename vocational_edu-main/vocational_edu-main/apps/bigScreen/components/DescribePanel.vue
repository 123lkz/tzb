<template>
  <div
    class="describe-panel bg-white bg-opacity-10 rounded-lg p-6 w-full max-w-xl mx-auto flex flex-col items-center"
  >
    <div class="flex items-center mb-4">
      <button :disabled="currentIndex === 0" class="px-2 py-1 text-lg" title="上一项" @click="prev">
        ←
      </button>
      <div class="text-2xl font-bold mx-4">{{ industries[currentIndex].title }}</div>
      <button
        :disabled="currentIndex === industries.length - 1"
        class="px-2 py-1 text-lg"
        title="下一项"
        @click="next"
      >
        →
      </button>
    </div>
    <div class="text-base text-center whitespace-pre-line leading-relaxed">
      {{ industries[currentIndex].content }}
    </div>
    <div class="flex mt-4 space-x-2">
      <span
        v-for="(item, idx) in industries"
        :key="item.title"
        class="w-2 h-2 rounded-full"
        :class="currentIndex === idx ? 'bg-blue-500' : 'bg-gray-400'"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const industries = [
  {
    title: '第一产业',
    content:
      '第一产业主要包括：\n农业、林业、牧业、渔业等。\n主要从事自然资源的开发和初级产品的生产。',
  },
  {
    title: '第二产业',
    content:
      '第二产业主要包括：\n工业、建筑业等。\n主要从事对初级产品的加工、制造和建筑施工等活动。',
  },
  {
    title: '第三产业',
    content:
      '第三产业主要包括：\n服务业、金融、教育、医疗、交通运输、信息技术等。\n主要为社会和生产提供服务。',
  },
]

const currentIndex = ref(0)

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}
function next() {
  if (currentIndex.value < industries.length - 1) {
    currentIndex.value++
  }
}
</script>

<style scoped>
.describe-panel {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
