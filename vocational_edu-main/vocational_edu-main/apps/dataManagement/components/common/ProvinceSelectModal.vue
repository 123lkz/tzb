<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-start justify-center bg-black/40"
    @click.self="emit('close')"
  >
    <div
      class="bg-gradient-to-br from-[#e0f7faee] to-[#b2ebf2cc] rounded-xl shadow-2xl p-8 min-w-[480px] mt-32"
    >
      <div class="grid grid-cols-4 gap-3">
        <button
          v-for="item in provinceList"
          :key="item"
          @click="select(item)"
          :class="[
            'px-4 py-2 m-1 rounded-lg font-bold transition',
            item === selected
              ? 'bg-cyan-600 text-white ring-2 ring-cyan-400'
              : 'bg-cyan-500/80 text-white hover:bg-cyan-400/90',
          ]"
        >
          {{ item }}
        </button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ show: boolean; selected?: string }>()
const emit = defineEmits(['select', 'close'])
function select(name: string) {
  emit('select', name)
}

const provinceList = [
  '全国',
  '北京市',
  '天津市',
  '河北省',
  '山西省',
  '内蒙古自治区',
  '辽宁省',
  '吉林省',
  '黑龙江省',
  '上海市',
  '江苏省',
  '浙江省',
  '安徽省',
  '福建省',
  '江西省',
  '山东省',
  '河南省',
  '湖北省',
  '湖南省',
  '广东省',
  '广西壮族自治区',
  '海南省',
  '重庆市',
  '四川省',
  '贵州省',
  '云南省',
  '西藏自治区',
  '陕西省',
  '甘肃省',
  '青海省',
  '宁夏回族自治区',
  '新疆维吾尔自治区',
  '香港特别行政区',
  '澳门特别行政区',
  '台湾省',
]
</script>
