<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    cdata: any[]
    limit: number
    height?: number
    keyField?: string
  }>(),
  {
    cdata: [],
    height: 1.7,
    limit: 10,
  }
)
</script>

<template>
  <div class="overflow-hidden" :style="{ height: props.height * props.limit + 'rem' }">
    <TransitionGroup name="list" tag="div">
      <div
        v-for="(row, i) in props.cdata.slice(0, props.limit)"
        :key="props.keyField ? row[props.keyField] : i"
        :style="{ height: props.height + 'rem' }"
        class="flex items-center leading-4 text-xs"
      >
        <slot :row="row" :index="i" />
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.list-move,
.list-leave-active,
.list-enter-active {
  transition: all 1s;
}

.list-enter-from {
  opacity: 0;
  height: 0 !important;
}

.list-leave-to {
  opacity: 0;
  height: 0 !important;
}
</style>
