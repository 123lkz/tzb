<script lang="ts" setup>
import ThirdTitleSvg from '~/assets/svg/thirdTitle.svg'

const props = withDefaults(
  defineProps<{
    title: string
    size?: 'xs' | 'sm' | 'md'
  }>(),
  {
    size: 'sm',
  }
)
</script>
<template>
  <div class="flex items-center relative h-7 w-full rounded overflow-hidden">
    <img
      :src="ThirdTitleSvg"
      alt="thirdTitle"
      class="absolute top-0 left-0 right-0 bottom-0 w-full h-full object-cover"
    />
    <span
      class="text-white font-bold relative z-10 pl-2"
      :class="props.size === 'xs' ? 'text-xs' : props.size === 'sm' ? 'text-sm' : 'text-md'"
      >{{ props.title }}</span
    >
  </div>
</template>
