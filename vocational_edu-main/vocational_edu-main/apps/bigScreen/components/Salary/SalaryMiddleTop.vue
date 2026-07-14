<script setup lang="ts">
import HorizontalBarChart from '../Echart/HorizontalBarChart.vue'
import SecondTitleHeader from '../SecondTitleHeader.vue'
import EchartChinaMap from '../Echart/EchartChinaMap.vue'
import RankList from '../RankList/RankList.vue'
// import DataSource from '../DataSource.vue'
import { roundToThousand } from '~/utils/num'
import RightSvg from '~/assets/svg/right.svg'
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useApiData } from '@base/composables/CachedAxiosClient'
import { $occupationCategories, $industry } from '@base/api/Api'

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
  professionRecruitmentData: ListItem[]
  industryRecruitmentData: ListItem[]
}>()

const hoveredProvince = ref('')
const selectedProvince = ref('')
const showProvinceMap = ref(false)
const currentProvince = ref('')

// 追踪HorizontalBarChart当前显示的10个省份
const barCurrentStartIndex = ref(0)

// 监听HorizontalBarChart滚动事件（需在HorizontalBarChart中emit）
function handleBarScroll(startIndex: number) {
  barCurrentStartIndex.value = startIndex
}

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
let highlightTimer: ReturnType<typeof setInterval> | null = null

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

// 计算x轴最大值
const provinceMapDataMaxValue = computed(() => {
  return roundToThousand(Math.max(...props.provinceMapData.map((item) => item.value)))
})

// 职业与行业父级映射与缓存
const level3ParentsMap = ref<Record<string, { level1Name: string; level2Name: string }>>({})
const industryParentsMap = ref<Record<string, { level1Name: string; level2Name: string }>>({})

type OccupationNode = {
  level: number
  name: string
  code?: string
  children?: OccupationNode[]
}

type IndustryNode = {
  level: number
  name: string
  code?: string
  children?: IndustryNode[]
}

const { data: positionGradeList } = useApiData(() => $occupationCategories.GetGradeList())
const { data: industryGradeList } = useApiData(() => $industry.GetGradeList())

function buildParentsMapFromTree(tree: OccupationNode[]) {
  const result: Record<string, { level1Name: string; level2Name: string }> = {}

  function dfs(node: OccupationNode, context: { l1?: string; l2?: string }) {
    const level = Number(node.level)
    const name = node.name || ''

    let currentL1 = context.l1
    let currentL2 = context.l2

    if (level === 1) {
      currentL1 = name
    } else if (level === 2) {
      currentL2 = name
    } else if (level === 3) {
      if (name) {
        result[name] = {
          level1Name: currentL1 || '-',
          level2Name: currentL2 || '-'
        }
      }
    }

    const children = Array.isArray(node.children) ? node.children : []
    for (const child of children) {
      dfs(child, { l1: currentL1, l2: currentL2 })
    }
  }

  for (const root of Array.isArray(tree) ? tree : []) {
    dfs(root, {})
  }

  level3ParentsMap.value = result
}

function buildIndustryParentsMapFromTree(tree: IndustryNode[]) {
  const result: Record<string, { level1Name: string; level2Name: string }> = {}

  function dfs(node: IndustryNode, context: { l1?: string; l2?: string }) {
    const level = Number(node.level)
    const name = node.name || ''

    let currentL1 = context.l1
    let currentL2 = context.l2

    if (level === 2) {
      currentL1 = name
    } else if (level === 3) {
      currentL2 = name
    } else if (level === 4 || level === 5) {
      if (name) {
        result[name] = {
          level1Name: currentL1 || '-',
          level2Name: currentL2 || '-'
        }
      }
    }

    const children = Array.isArray(node.children) ? node.children : []
    for (const child of children) {
      dfs(child, { l1: currentL1, l2: currentL2 })
    }
  }

  for (const root of Array.isArray(tree) ? tree : []) {
    dfs(root, {})
  }

  industryParentsMap.value = result
}

watch(
  () => positionGradeList.value,
  (val) => {
    if (val) buildParentsMapFromTree(val as unknown as OccupationNode[])
  },
  { immediate: true, deep: true }
)

watch(
  () => industryGradeList.value,
  (val) => {
    if (val) buildIndustryParentsMapFromTree(val as unknown as IndustryNode[])
  },
  { immediate: true, deep: true }
)

const tooltipHtmlCache = ref<Record<string, string>>({})
const industryTooltipHtmlCache = ref<Record<string, string>>({})

watch(
  () => level3ParentsMap.value,
  () => {
    tooltipHtmlCache.value = {}
  },
  { deep: true }
)

watch(
  () => industryParentsMap.value,
  () => {
    industryTooltipHtmlCache.value = {}
  },
  { deep: true }
)

type TooltipDatum = { originalName?: string; name?: string }

function professionTooltipFormatter(params: Array<{ data?: TooltipDatum }>): string {
  const raw = params[0]?.data || {}
  const fullName = raw.originalName || raw.name || ''
  if (!fullName) return ''

  const cached = tooltipHtmlCache.value[fullName]
  if (cached !== undefined) return cached
  const parents = level3ParentsMap.value[fullName]
  if (!parents) {
    tooltipHtmlCache.value[fullName] = ''
    return ''
  }

  const level1Name = parents.level1Name || '-'
  const level2Name = parents.level2Name || '-'

  const html = `
      <div style="margin-top:8px;color:#666;text-align: left;">
        <div>一级标准职业：<b style="color:#333">${level1Name}</b></div>
        <div>二级标准职业：<b style="color:#333">${level2Name}</b></div>
      </div>
    `
  tooltipHtmlCache.value[fullName] = html
  return html
}

function industryTooltipFormatter(industryName: string): string {
  if (!industryName) return ''

  const cached = industryTooltipHtmlCache.value[industryName]
  if (cached !== undefined) return cached

  const parents = industryParentsMap.value[industryName]
  if (!parents) {
    industryTooltipHtmlCache.value[industryName] = ''
    return ''
  }

  const level1Name = parents.level1Name || '-'
  const level2Name = parents.level2Name || '-'

  const html = `一级标准行业：${level1Name}\n二级标准行业：${level2Name}`
  industryTooltipHtmlCache.value[industryName] = html
  return html
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
              <SecondTitleHeader title="薪资中位数" subtext="按省份排行">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="20" height="20">
                    <path
                      d="M952 511.648C952 268.848 755.008 72 512 72S72 268.848 72 511.648c0 224.32 168.08 409.376 385.264 436.304 12.24 2.576 27.152 4.064 44.912 4.064 4.992 0 9.792-0.256 14.432-0.72C757.488 948.816 952 752.944 952 511.648z m-62.912 6.224a432.272 432.272 0 0 0-8.576-64.288c0.368-7.456 0.48-14.512 0.304-21.072 5.456 25.52 8.336 52 8.336 79.12l-0.064 6.24z m-754.24-6.224c0-26.64 2.768-52.64 8.048-77.712 16.288 17.408 54.672 17.008 64.032-9.008 16.752 9.984 39.264 11.792 39.264 31.744 0 65.856 2.352 136.448 62.192 137.568 1.68 0 33.36 11.984 48.448 51.088 5.216 13.52 25.84 0 48.448 0 11.296 0 0 19.008 0 60.144 0 40.976 88.336 104.064 88.336 104.064-0.4 27.12 0.704 49.056 2.96 66.576-19.936-0.368-36.736 2.272-49.952 6.752C269.488 851.936 134.848 697.504 134.848 511.648z m470 365.344c-1.952-9.568-10.512-14.816-26.112-10.704 12.448-53.024 18.496-82.736 44.496-105.296 37.616-32.592 4.464-68.848-24.144-64.576-22.56 3.408-8.32-27.92-28.448-29.664-20.128-1.664-46.416-41.712-75.392-55.488-15.36-7.312-30.448-26.848-54.144-27.728-21.008-0.816-51.68 17.76-51.68 3.44 0-46.096-4.672-79.008-5.632-92.144-0.768-10.544-6.896-3.552 21.488-2.88 15.44 0.416 7.904-31.008 23.184-32.256 15.024-1.184 50.8 14.064 59.936 7.984 8.464-5.664 62.256 141.184 62.256 24.272 0-13.872-7.168-37.984 0-51.12 28.416-51.92 55.008-94.24 52.624-100.416-1.36-3.488-29.056-6.352-51.232 1.072-7.488 2.496 2.368 14.24-8.368 16.736-40.272 9.28-75.856-10.88-63.392-29.808 12.752-19.424 58.992-8.464 63.04-47.424 2.336-22.304 4.256-48.144 5.568-67.36 54.192 8.48 48.224-70.336-32.368-78.768 163.04 1.904 301.2 107.2 351.904 253.328a15.424 15.424 0 0 0-8.992-4.112c-24.368-60.864-83.52-16.816-63.456 36.864-107.488 82.64-79.984 140.288-44.656 173.296 18.576 17.328 36.304 43.424 47.84 62.16-12.56 36.608 46.272 21.936 75.28-40.176a377.776 377.776 0 0 1-269.6 260.768z"
                      fill="#00ffff"
                    ></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <HorizontalBarChart
                :data="props.provinceMapData"
                height="240px"
                tooltip-title="薪资中位数"
                is-show-province-data
                quantifier="元"
                :scroll-step="10"
                :x-axis-min="0"
                :x-axis-max="provinceMapDataMaxValue"
                @bar-hover="handleBarHover"
                @bar-click="handleBarClick"
                @bar-scroll="handleBarScroll"
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
              <SecondTitleHeader title="薪资中位数" subtext="按标准职业分类第三级排行">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="24" height="24">
                    <path
                      d="M511.636645 89.803699c11.109849 0 23.518968 0.831312 37.260387 2.48843l3.776688 0.473462 6.188043 0.842323 6.353205 0.946925 3.242666 0.512 6.606452 1.101075 3.36929 0.589075 3.413334 0.616602 8.720516 1.651613 8.984774 1.816774 3.672086 0.770753 3.716129 0.79828 7.558882 1.673634 3.842752 0.875355 7.817635 1.827785 3.980387 0.95243 8.081892 1.981936 8.258065 2.086537a33.032258 33.032258 0 0 1 24.724645 34.755441 728.179613 728.179613 0 0 1-3.523441 33.417634l-0.59458 4.404302-0.990968 6.859698c-3.083011 20.221247-6.947785 37.282409-11.693419 51.310108-1.018495 3.00043-2.174624 6.166022-3.479398 9.507785l-1.007484 2.532473-1.800258 4.376774-0.957936 2.251699-2.025978 4.641032-2.747183 6.055914-2.983914 6.336689-2.56 5.285161-2.714151 5.461333-2.868301 5.648516-3.798709 7.322151-4.046452 7.619441-3.407828 6.309161-3.561978 6.496344-4.051957 7.289118 6.077935 21.34985 9.199484 32.591828 9.672946 34.716903 5.587957 20.331355 6.243097 23.001462 6.644989 24.917334 5.147527 19.709247 2.383828 9.293075 4.39329 17.446538 3.396818 13.89557 2.290236 9.601376 3.127054 13.427613 2.405849 10.53729 4.123527 18.470538 3.396817 15.580215 3.484904 16.306925 5.395269 25.809204 3.716129 18.107183 4.76215 23.645591 4.90529 24.774194 6.072431 31.215484a33.032258 33.032258 0 0 1-5.241119 25.010924l-0.919398 1.266237-4.789677 6.259613-4.712602 6.083441-4.624516 5.907268-4.53643 5.725592-4.45385 5.56043-4.365763 5.378753-4.288688 5.20258-4.200603 5.026409-2.070021 2.449892-5.081463 5.929291-4.954838 5.659527-3.881291 4.332731-1.90486 2.103053-3.754666 4.073979-1.844302 1.965419-3.633548 3.815226-1.789247 1.844301-3.517936 3.550968-1.728688 1.712172-3.396817 3.303226-1.673634 1.580043-1.651613 1.541505-3.248172 2.956387c-1.596559 1.431398-3.176602 2.807742-4.723613 4.112516-22.561032 19.076129-55.092301 38.168774-97.913119 57.84499a33.032258 33.032258 0 0 1-27.725075-0.066065c-43.118108-20.061591-75.555785-39.104688-97.698408-57.718365l-1.497463-1.266237-1.508473-1.31028-3.088516-2.741677-3.171097-2.912344-3.248172-3.077505-4.184086-4.08499-4.305204-4.349247-3.545463-3.672086-3.622537-3.837247-1.849807-1.981936-3.754666-4.096-4.811699-5.356731-4.954839-5.626495-4.051957-4.696086-2.064516-2.405849-4.184086-4.954839-6.452301-7.746064-6.650495-8.142452-6.854193-8.527828-4.67957-5.901763-7.195527-9.182968a33.032258 33.032258 0 0 1-6.837678-23.177634l0.170667-1.552517 2.163613-15.717849 1.442409-10.251011 2.158107-15.046193 2.158108-14.638796 2.163613-14.236903 1.436903-9.260043 2.163613-13.565248 2.158107-13.157849 2.163613-12.750452 1.442409-8.27458 1.442408-8.103914 2.158108-11.809033 1.442408-7.652473 2.163613-11.142881 1.442409-7.206538 1.447914-7.02486 1.442409-6.848688 1.442408-6.667011 1.447914-6.496344 2.169118-9.397678 0.721205-3.044473 1.888344-7.740559 1.343312-5.362237 2.890322-11.208946 1.547011-5.846709 2.455398-9.067355 2.604043-9.43071 3.716129-13.141333 2.967398-10.284043 2.064516-7.052387 4.332731-14.594753 3.429849-11.374108 4.817205-15.72886 3.787699-12.221935 6.661505-21.179183 4.211613-13.196387 8.874667-27.488344 6.391742-19.538581-3.490409-5.92929-5.461333-9.408688-3.451871-6.050409-3.303226-5.874237-3.149075-5.692559-3.72714-6.876215-3.490409-6.595441-2.626064-5.086967-2.47742-4.910796-2.323268-4.734624-1.106581-2.312258-1.068043-2.257204-2.031484-4.404301-1.877333-4.228129-1.728689-4.062968c-0.550538-1.32129-1.084559-2.620559-1.585548-3.892301l-0.73772-1.882839-0.660645-1.734193c-6.380731-17.066667-11.654882-38.603699-15.965592-64.809291l-1.211183-7.613935-1.101075-7.542366a826.356989 826.356989 0 0 1-2.075527-15.778408 33.032258 33.032258 0 0 1 24.030968-35.84l1.24972-0.324817 8.021334-1.849807 7.850666-1.767226 7.68-1.69015 13.031226-2.758194 8.984774-1.816774 7.002839-1.359828 6.837677-1.282753 6.661506-1.194666 6.501849-1.117592 6.331183-1.029505 6.166022-0.95243 6.00086-0.86985 2.945376-0.401892 7.168-0.919398 6.909247-0.792774 2.69213-0.275269 2.653591-0.258753 5.175054-0.456946 2.532473-0.198193 4.938322-0.330323 4.778667-0.247742 2.328774-0.093591 4.530925-0.126624c1.486452-0.027527 2.945376-0.044043 4.376774-0.044043zM551.693763 357.849462H469.13514l-2.207656 6.733076-5.951312 18.332903-4.283183 13.323011-5.472344 17.19329-5.197075 16.53815-6.110968 19.753291-4.580473 15.068215-5.340215 17.914494-3.958366 13.592775-3.683096 12.937634-2.587527 9.271054-3.198624 11.781505-2.92886 11.131871-1.359828 5.318194-1.910366 7.668989-1.893849 7.867183-2.114065 9.166451-1.409376 6.353205-2.114065 9.88215-1.414881 6.826667-1.414882 7.013849-1.420387 7.206538-1.414882 7.39372-1.420387 7.586409-1.420387 7.773591-2.136086 12.018237-1.431398 8.247054-1.420387 8.439742-2.147097 13.009204-2.85729 18.008086-2.147097 14.005677-2.147097 14.424086-2.158107 14.853506-2.367312 16.818925 2.290237 2.879311 6.496344 8.092904 4.200602 5.164043 4.107011 4.987871 4.007914 4.806193 3.903311 4.624516 5.665033 6.595441 3.650064 4.16757 3.545463 3.985892 5.12 5.637506 3.292215 3.523441 3.182107 3.341763 1.552516 1.602065 3.022452 3.066494 2.917849 2.879312 2.807742 2.697635 1.365334 1.271741 2.64258 2.416861 2.543484 2.229677 1.16714 0.990968c6.07243 5.097978 13.532215 10.46572 22.373849 16.075699l2.692129 1.69015 4.745635 2.890323c1.618581 0.974452 3.281204 1.948903 4.982365 2.934365l2.576517 1.480947 5.334709 2.989419c3.407828 1.882839 6.947785 3.787699 10.630882 5.709075l3.72714 1.932387 6.15501 3.121549 5.984345 2.956387 2.64258-1.277247 3.253678-1.60757 3.193118-1.596559 6.204559-3.176603 3.011441-1.574537 2.945376-1.569032 5.720086-3.110538c15.734366-8.709505 28.572903-17.03914 38.477076-24.906323l1.937892-1.569032 1.596559-1.332301c0.875355-0.73772 1.76172-1.502968 2.670108-2.306753l1.376344-1.227699 2.824258-2.609548 2.939871-2.807742 1.508473-1.475441 1.541505-1.530494 3.149076-3.204129 1.61858-1.67914 1.646108-1.723183 4.228129-4.53643 4.39329-4.844731 4.552946-5.147527 4.718108-5.461334 1.932387-2.268215 3.947355-4.685075 4.046451-4.883269 4.145549-5.075957 4.25015-5.27415 4.349248-5.466839 6.105462-7.784602-2.240688-11.467699-4.982366-25.242151-4.83372-24.058494-3.760172-18.398968-4.563957-21.933419-3.545463-16.692301-3.446365-15.932559-3.352774-15.178323-2.449893-10.884129-2.394839-10.460215-3.116043-13.278968-2.879311-11.968688-2.653592-10.746495-4.398796-17.396989-3.215139-12.44215-2.56-9.783054-6.463312-24.306237-6.088946-22.489462-6.595441-24.008946-7.101936-25.539441-8.918709-31.710968-5.863226-20.562581z m-40.062623-201.975742c-1.690151 0-3.44086 0.027527-5.252129 0.082581l-2.769205 0.099097-4.332731 0.220215-2.246193 0.148645-4.646538 0.35785c-2.114065 0.181677-4.294194 0.385376-6.529376 0.616602l-3.402323 0.36886-5.285161 0.627613-2.714151 0.346839-5.593462 0.765247-5.802667 0.853333-2.978408 0.456946-6.116473 0.990968-6.320172 1.079054-3.237162 0.572559-6.633978 1.211183-8.571871 1.651613-8.896688 1.789247-6.243097 1.293763 0.401892 2.367312c3.138065 18.294366 6.716559 33.252473 10.647398 44.769721l0.737721 2.11957 0.638623 1.739699 1.057033 2.736172 0.572559 1.425892 1.24972 2.978409 1.370839 3.14357 1.497462 3.303225 1.629592 3.468387 1.750709 3.633549 1.871828 3.782193 2.009463 3.947355 2.125075 4.107011 2.257204 4.266667 3.617032 6.689032 2.565506 4.657548 2.692129 4.811699 4.266666 7.509334 4.552947 7.856172 1.800258 3.066494h94.499785l1.304774-2.350795 4.283183-7.850667 4.018924-7.503828 2.521463-4.806194 3.561978-6.909247 2.224172-4.415312 2.103054-4.25015 1.981936-4.090495 1.860817-3.930839 1.739699-3.771182 1.61858-3.606022 1.497463-3.446366 1.376344-3.281204 1.255226-3.116043 1.128602-2.950882 1.007484-2.78572 0.462451-1.332301c3.974882-11.748473 7.377204-27.840688 10.09686-48.083957l0.423914-3.231656 0.121119-0.968946-8.164473-1.82228-3.595011-0.781763-7.030366-1.469936c-2.312258-0.473462-4.585978-0.924903-6.826666-1.365333l-3.336258-0.638624-6.512861-1.194666-3.176602-0.556043-3.127054-0.534022-6.088946-0.974451-2.967398-0.445936-2.912344-0.423914-5.670537-0.754237-2.752689-0.341333-5.340215-0.589075a248.567742 248.567742 0 0 0-18.619182-1.266237l-2.791226-0.055053-1.915871-0.016517z"
                      fill="#00ffff"
                    ></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <HorizontalBarChart
                :data="props.professionRecruitmentData"
                height="240px"
                tooltip-title="薪资中位数"
                quantifier="元"
                :scroll-step="10"
                :tooltip-formatter="professionTooltipFormatter"
              />
            </div>
          </div>
          <div class="w-64 flex flex-col gap-4 z-10">
            <div
              class="overflow-hidden h-full text-center flex-shrink-0 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg px-3 py-2 text-white shadow-[inset_0_0_10px_rgba(0,255,255,0.1)] border border-[#00ffff]/10 flex flex-col min-h-0"
            >
              <SecondTitleHeader title="薪资中位数" subtext="按标准行业分类第三级排行">
                <template #second-svg>
                  <svg viewBox="0 0 1024 1024" width="28" height="28">
                    <path
                      d="M381.92 607.168l259.232 0 0-189.44-259.232 0L381.92 607.168zM419.2 455.52l37.632 0 0 113.888L419.2 569.408 419.2 455.52zM791.008 377.184l0-36.64-75.744 0L715.264 340.16c0-21.088-16.64-38.208-37.184-38.208l-0.192 0L677.888 224.544 642.24 224.544l0 77.408-38.752 0L603.488 224.544l-35.616 0 0 77.408-38.816 0L529.056 224.544 493.44 224.544l0 77.408-38.752 0L454.688 224.544l-35.584 0 0 77.408-38.752 0L380.352 224.544l-35.584 0 0 77.408-1.472 0c-20.544 0-37.184 17.12-37.184 38.208l0 0.416L232.992 340.576l0 36.64 73.088 0 0 39.84L232.992 417.056l0 36.64 73.088 0 0 39.84L232.992 493.536l0 36.608 73.088 0 0 39.872L232.992 570.016l0 36.64 73.088 0L306.08 646.4 232.992 646.4l0 36.64 73.088 0 0 3.488c0 21.12 16.672 38.24 37.184 38.24l1.472 0 0 74.688 35.584 0 0-74.688 38.752 0 0 74.688 35.584 0 0-74.688 38.752 0 0 74.688 35.616 0 0-74.688 38.816 0 0 74.688 35.616 0 0-74.688 38.752 0 0 74.688 35.616 0 0-74.688 0.192 0c20.576 0 37.184-17.12 37.184-38.24l0-3.488 75.744 0L790.944 646.4l-75.744 0 0-39.808 75.744 0 0-36.64-75.744 0 0-39.872 75.744 0 0-36.608-75.744 0 0-39.84 75.744 0 0-36.64-75.744 0 0-39.84L791.008 377.152zM680.064 655.648c0 17.376-13.696 31.424-30.56 31.424l-275.296 0c-16.896 0-30.56-14.048-30.56-31.424l0-284.736c0-17.344 13.664-31.392 30.56-31.392l275.296 0c16.864 0 30.56 14.048 30.56 31.392L680.064 655.648z"
                      fill="#00ffff"
                    ></path>
                  </svg>
                </template>
              </SecondTitleHeader>
              <div class="relative flex flex-col flex-1 min-h-0">
                <RankList
                  :data="props.industryRecruitmentData"
                  tooltip-title="薪资中位数"
                  unit="元"
                  :show-count="20"
                  period="5"
                  :tooltip-formatter="industryTooltipFormatter"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="h-full absolute left-0 top-0 w-full">
          <EchartChinaMap
            type="salary"
            :data="props.provinceMapData"
            :circle-provinces="[highlightProvince]"
            :circle-size="48"
            quantifier="元/月"
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
