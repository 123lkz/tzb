<script lang="ts" setup>
import TitleSvg from '~/assets/svg/title.svg'
const props = defineProps<{
  title: string
}>()
</script>
<template>
  <div class="flex flex-col">
    <div class="flex items-center relative">
      <div
        class="absolute left-0 top-0 w-full h-full bg-gradient-to-l from-[#00ffff]/0 to-[#00ffff]/30 rounded-md"
      />
      <div class="flex items-center gap-2 px-2 py-1 pb-1.5">
        <span class="text-white font-bold text-[#00ffff] text-sm">{{ props.title }}</span>
      </div>
      <div
        class="absolute bottom-0 w-full h-1 bg-gradient-to-l from-[#00ffff]/40 to-[#00ffff]/0 rounded-full"
      ></div>
      <img :src="TitleSvg" alt="title" class="w-auto h-full absolute right-0 top-0 opacity-10" />
    </div>
  </div>
</template>
