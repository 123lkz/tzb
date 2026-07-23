<template>
  <div class="p-2">
    <div v-for="(item,i) in data" :key="i" class="flex items-center justify-between py-2 border-b border-[rgba(0,255,255,0.06)] last:border-0">
      <div class="flex items-center gap-2">
        <span class="w-5 h-5 flex-center rounded text-[10px] font-bold" :class="rankClass(i)">{{ i+1 }}</span>
        <span class="text-xs text-[rgba(176,196,222,0.8)] truncate max-w-[120px]">{{ item.name }}</span>
      </div>
      <div class="text-right">
        <div class="text-xs text-[#00ffff]">{{ item.positions }}{{ item.avgSalary ? "个岗位" : "" }}</div>
        <div v-if="item.avgSalary" class="text-[10px] text-[rgba(176,196,222,0.4)]">{{ item.avgSalary }}K</div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{ data: {name:string;positions:number;avgSalary?:number}[] }>()
function rankClass(i: number): string {
  if (i === 0) return "bg-[rgba(255,217,61,0.2)] text-[#ffd93d]"
  if (i === 1) return "bg-[rgba(176,196,222,0.15)] text-[rgba(176,196,222,0.7)]"
  if (i === 2) return "bg-[rgba(107,203,119,0.15)] text-[#6bcb77]"
  return "bg-[rgba(0,255,255,0.06)] text-[rgba(176,196,222,0.4)]"
}
</script>