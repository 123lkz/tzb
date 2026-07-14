<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: number
    color?: string
  }>(),
  {
    size: 80,
    color: '#00ffff',
  }
)
</script>

<template>
  <div class="h-screen w-full flex flex-col items-center justify-center">
    <svg class="animate-spin" viewBox="0 0 1024 1024" :width="size" :height="size">
      <path
        d="M512 0c219.428571 0 73.142857 292.571429 0 292.571429S292.571429 0 512 0z"
        :fill="color"
      ></path>
      <path
        d="M512 1024c219.428571 0 73.142857-292.571429 0-292.571429s-219.428571 292.571429 0 292.571429z"
        :fill="color"
        opacity=".3"
      ></path>
      <path
        d="M149.942857 149.942857C305.152-5.12 408.576 305.152 356.937143 356.937143c-51.712 51.712-362.057143-51.712-206.921143-206.921143z"
        :fill="color"
        opacity=".8"
      ></path>
      <path
        d="M874.057143 874.057143C1029.12 718.848 718.848 615.424 667.062857 667.062857c-51.712 51.712 51.712 362.057143 206.921143 206.921143z"
        :fill="color"
        opacity=".2"
      ></path>
      <path
        d="M0 512c0-219.428571 292.571429-73.142857 292.571429 0s-292.571429 219.428571-292.571429 0z"
        :fill="color"
        opacity=".6"
      ></path>
      <path
        d="M1024 512c0-219.428571-292.571429-73.142857-292.571429 0s292.571429 219.428571 292.571429 0z"
        :fill="color"
        opacity=".1"
      ></path>
      <path
        d="M149.942857 874.057143C-5.12 718.848 305.152 615.424 356.937143 667.062857c51.712 51.712-51.712 362.057143-206.921143 206.921143z"
        :fill="color"
        opacity=".4"
      ></path>
      <path
        d="M874.057143 149.942857C718.848-5.12 615.424 305.152 667.062857 356.937143c51.712 51.712 362.057143-51.712 206.921143-206.921143z"
        :fill="color"
        opacity=".05"
      ></path>
    </svg>
    <div class="mt-10 gradient-3d-text">国家职业教育人才供需平台</div>
  </div>
</template>

<style scoped>
.gradient-3d-text {
  color: #00ffff;
  font-size: 4rem;
  font-weight: bold;
  position: relative;
  text-shadow: 0 1px 0 #0088ff, 0 2px 0 #0088ff, 0 3px 0 #0066cc, 0 4px 0 #0066cc, 0 5px 0 #004488,
    0 6px 1px rgba(0, 0, 0, 0.1), 0 0 5px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.3),
    0 3px 5px rgba(0, 0, 0, 0.2), 0 5px 10px rgba(0, 0, 0, 0.25);
  transform: perspective(250px) rotateX(30deg);
}

.gradient-3d-text::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  color: transparent;
  background: linear-gradient(to bottom, #00ffff 0%, #0088ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  transform: rotateX(180deg) translateY(15px);
  filter: blur(2px);
  opacity: 0.7;
}
</style>
