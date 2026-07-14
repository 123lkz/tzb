<script setup lang="ts">
import HorizontalBarChart from '../Echart/HorizontalBarChart.vue'
import SecondTitleHeader from '../SecondTitleHeader.vue'
import EchartChinaMap from '../Echart/EchartChinaMap.vue'
import RankList from '../RankList/RankList.vue'
import RightSvg from '~/assets/svg/right.svg'

interface ListItem {
  name: string
  value: number
}

interface ProvinceMapDataItem {
  name: string
  value: number
}

const props = defineProps<{
  provinceMapData: ProvinceMapDataItem[]
  schoolNumberRecruitmentData: ListItem[]
  majorStudentRecruitmentData: ListItem[]
}>()

const hoveredProvince = ref('')
const selectedProvince = ref('')
const showProvinceMap = ref(false)
const currentProvince = ref('')

function handleBarHover(name: string) {
  hoveredProvince.value = name
  // 当鼠标悬停在柱状图上时，暂停地图的自动高亮切换
  if (highlightTimer) {
    clearInterval(highlightTimer)
    highlightTimer = null
  }
}

function handleBarMouseout() {
  hoveredProvince.value = ''
  // 当鼠标移出柱状图时，恢复地图的自动高亮切换
  if (!isMapHovered.value) {
    startHighlightLoop()
  }
}
function handleBarClick(name: string) {
  selectedProvince.value = name
}
function handleProvinceClick(name: string) {
  currentProvince.value = name
  showProvinceMap.value = true
}
function handleBackToChinaMap() {
  showProvinceMap.value = false
  currentProvince.value = ''
}

// 当前高亮省份索引
const highlightIndex = ref(0)
const sortedProvinces = computed(() => [...props.provinceMapData].sort((a, b) => b.value - a.value))
const highlightProvince = computed(() => {
  // 如果有鼠标悬停的省份，优先显示该省份
  if (hoveredProvince.value) {
    return hoveredProvince.value
  }
  // 否则显示自动切换的省份
  return sortedProvinces.value[highlightIndex.value]?.name || ''
})

// 自动切换高亮省份
let highlightTimer: NodeJS.Timeout | null = null
function startHighlightLoop() {
  if (highlightTimer) clearInterval(highlightTimer)
  highlightTimer = setInterval(() => {
    highlightIndex.value = (highlightIndex.value + 1) % sortedProvinces.value.length
  }, 2000)
}
function stopHighlightLoop() {
  if (highlightTimer) clearInterval(highlightTimer)
  highlightTimer = null
}
onMounted(() => {
  startHighlightLoop()
})
onBeforeUnmount(() => {
  stopHighlightLoop()
})

// 控制HorizontalBarChart滚动状态
const isMapHovered = ref(false)

// 监听地图hover事件
function handleMapProvinceHover() {
  isMapHovered.value = true
  // 暂停HorizontalBarChart滚动
  if (highlightTimer) {
    clearInterval(highlightTimer)
    highlightTimer = null
  }
}

function handleMapProvinceMouseout() {
  isMapHovered.value = false
  // 恢复HorizontalBarChart滚动
  startHighlightLoop()
}
</script>

<template>
  <ClientOnly>
    <transition appear enter-from-class="opacity-0" enter-active-class="duration-300" name="fade">
      <div class="h-full relative">
        <div class="flex justify-between h-full">
          <div class="w-64 grid grid-rows-2 gap-4 z-10">
            <div
              class="relative text-center h-full flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.5)] border border-[#00ffff]/10 flex-1 min-h-0"
            >
              <SecondTitleHeader title="各省大专院校学生数排行" subtext="数据来源：2022年">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="20" height="20">
                    <path
                      d="M960.29696 809.18528a298.11712 298.11712 0 0 0-187.392-276.992 198.8608 198.8608 0 0 0-64.6656-358.66624 3.80928 3.80928 0 0 0-2.28352 0.18432c-1.024-0.09216-1.98656-0.27648-2.97984-0.27648a33.93536 33.93536 0 0 0-5.35552 67.44064 58.61376 58.61376 0 0 0 6.84032 2.12992 129.0752 129.0752 0 0 1-18.05312 248.99584c-0.1024 0-0.19456 0.18432-0.19456 0.18432a38.16448 38.16448 0 0 0 0.78848 76.22656c0.1024 0.09216 0.29696 0.27648 0.39936 0.27648 120.49408 12.288 205.88544 115.21024 205.88544 240.49664a33.4336 33.4336 0 0 0 66.84672 1.3824c0-0.18432 0.1024-0.27648 0.1024-0.4608v-0.9216M559.104 537.74336a237.03552 237.03552 0 1 0-263.41376 0A356.82304 356.82304 0 0 0 71.68 869.24288c0 8.4992 0.49152 16.81408 1.09568 25.12896h0.1024a33.024 33.024 0 1 0 66.048 0c0-1.024-0.19456-2.048-0.29696-3.072-0.59392-7.30112-1.18784-14.60224-1.18784-22.07744a289.9456 289.9456 0 1 1 579.88096 0c0 7.76192-0.59392 15.36-1.18784 22.91712 0 0.36864-0.1024 0.73728-0.1024 1.10592v1.024h0.1024a32.93184 32.93184 0 0 0 65.85344 0h0.1024c0.59392-8.31488 1.09568-16.62976 1.09568-25.0368A357.2736 357.2736 0 0 0 559.104 537.74336M427.32544 510.976A170.83392 170.83392 0 1 1 597.6064 340.1216 170.58816 170.58816 0 0 1 427.32544 510.976m0 0z"
                      fill="#00ffff"
                    ></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <HorizontalBarChart
                :data="props.provinceMapData"
                height="240px"
                unit="万"
                quantifier="人"
                tooltip-title="省大专职业院校学生数"
                is-show-province-data
                :scroll-step="10"
                @bar-hover="handleBarHover"
                @bar-click="handleBarClick"
                @bar-mouseout="handleBarMouseout"
              />
              <img
                :src="RightSvg"
                alt="right"
                class="w-6 h-6 opacity-30 absolute -right-[18.5px] top-[50%] -translate-y-[3]"
              />
            </div>
            <div
              class="text-center h-full flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-4 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/10 flex-1 min-h-0"
            >
              <SecondTitleHeader title="各省大专职业院校数排行" subtext="数据来源：2022年">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="18" height="18">
                    <path
                      d="M492 202.026l1.665-0.8 160.988-73.589-160.966-62.334-1.687-0.678z"
                      fill="#00ffff"
                    ></path>
                    <path
                      d="M856 631V464H166v167H63v327H390V715h244v243h325V631H856zM166 795H89v-79h77v79z m143 0h-78v-79h78v79z m1-164h-79v-79h79v79z m161 0h-78v-79h78v79z m162 0h-79v-79h79v79z m159 164h-78v-79h78v79z m3-164h-79v-79h79v79z m140 164h-78v-79h78v79z"
                      fill="#00ffff"
                    ></path>
                    <path
                      d="M925.911 464l-38.507-155H494V201.226l-2 0.8V64.625l2 0.678V62h-35v247H134.763L96.256 464h759.642z"
                      fill="#00ffff"
                    ></path>
                    <path d="M390 715h244v243H390z" fill="#00ffff"></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <HorizontalBarChart
                :data="props.schoolNumberRecruitmentData"
                height="240px"
                quantifier="所"
                tooltip-title="省大专职业院校数"
                is-show-province-data
                :scroll-step="10"
              />
            </div>
          </div>
          <div class="w-64 flex flex-col gap-4 z-10">
            <div
              class="overflow-hidden h-full text-center flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/10 flex flex-col min-h-0"
            >
              <SecondTitleHeader title="大专专业学生数排行" subtext="数据来源：2022年">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="24" height="24">
                    <path
                      d="M488.6 651.5c4.3 2 9.3 2 13.7 0l234.1-111v159c0 6.1-3.4 11.7-8.9 14.5L502.6 827.4c-4.5 2.3-9.8 2.3-14.4 0L203.5 714.1c-5.5-2.7-8.9-8.3-8.9-14.5V540.5l294 111zM836 359v440.1c0 16.5-13.4 29.9-29.9 29.9s-29.9-13.4-29.9-29.9V371.4l-39.7 9.3v110.4l-241 114.2-300.9-114.2V377l-78-25.2c-6.2-2.4-10.3-8.4-10.3-15s4.1-12.6 10.3-15l372.9-149c3.8-1.5 8-1.5 11.8 0l373 149c6.1 2.5 10.2 8.4 10.2 15s-4 12.6-10.2 15L836 359z"
                      fill="#00ffff"
                    ></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <div class="relative flex flex-col flex-1 min-h-0">
                <RankList
                  :data="props.majorStudentRecruitmentData"
                  tooltip-title="专业学生数"
                  unit="人"
                  :show-count="20"
                  period="5"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="h-full absolute left-0 top-0 w-full">
          <EchartChinaMap
            type="education"
            :data="props.provinceMapData"
            :circle-provinces="[highlightProvince]"
            :circle-size="48"
            :unit="'人'"
            :unit-of-account="'万'"
            quantifier="人"
            :highlight-province="highlightProvince"
            @province-click="handleProvinceClick"
            @province-hover="handleMapProvinceHover"
            @province-mouseout="handleMapProvinceMouseout"
          />
        </div>
      </div>
    </transition>
  </ClientOnly>
</template>
