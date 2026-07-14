<script lang="ts" setup>
import Icon from '../Icon.vue'

const props = withDefaults(
  defineProps<{
    icon?: string
    iconSize?: number
    suffixIcon?: string
    title: string
    subtext?: string
    size?: 'sm' | 'md'
    showBtmLine?: boolean
  }>(),
  {
    icon: '',
    iconSize: 20,
    suffixIcon: '',
    size: 'sm',
    subtext: '',
    showBtmLine: true,
  }
)
</script>

<template>
  <div class="flex items-center relative">
    <div
      class="absolute left-0 top-0 w-full h-full bg-gradient-to-l rounded-md"
      :class="[
        props.showBtmLine ? 'from-[#00ffff]/0 to-[#00ffff]/10' : 'from-[#00ffff]/5 to-[#00ffff]/10',
      ]"
    />
    <div
      class="flex items-center"
      :class="props.size === 'sm' ? 'gap-1 px-2 pt-1 pb-1.5' : 'gap-2 px-4 pt-2 pb-3'"
    >
      <Icon v-if="props.icon" :name="props.icon" color="rgba(255, 255, 255, 0.9)" size="20" />
      <span class="text-white/90" :class="props.size === 'sm' ? 'text-sm' : 'text-md'">{{
        props.title
      }}</span>
      <span v-if="props.subtext" class="text-white/70 text-xs">{{ props.subtext }}</span>
    </div>
    <div
      class="absolute bottom-0 w-full h-1 bg-gradient-to-l from-[#00ffff]/40 to-[#00ffff]/0 rounded-full"
      :class="[props.showBtmLine ? 'block' : 'hidden']"
    ></div>
    <div class="absolute right-0 top-0 w-full h-full flex items-center justify-end">
      <Icon
        v-if="props.suffixIcon"
        :name="props.suffixIcon"
        color="#00ffff"
        size="20"
        class="opacity-50 rotate-45 mr-2"
      />
      <Icon v-else name="icon-title" color="#00ffff" size="28" class="opacity-30" />
    </div>
  </div>
</template>
