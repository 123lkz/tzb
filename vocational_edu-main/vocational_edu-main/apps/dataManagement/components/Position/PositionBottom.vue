<script setup lang="ts">
import { computed } from 'vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import FirstTitle from '../common/Title/FirstTitle.vue'
import HorizontalRank from '../common/HorizontalRank.vue'
import RankList from '../common/RankList/RankList.vue'
import GradientBarChart from '../Echart/GradientBarChart.vue'
import Icon from '../common/Icon.vue'

const industryRecruitmentData = [
  {
    name: '人力资源服务',
    value: 16043,
  },
  {
    name: '技术推广服务',
    value: 9440,
  },
  {
    name: '软件开发',
    value: 7295,
  },
  {
    name: '组织管理服务',
    value: 7225,
  },
  {
    name: '其他科技推广服务业',
    value: 7012,
  },
  {
    name: '道路货物运输',
    value: 6967,
  },
  {
    name: '其他商务服务业',
    value: 6936,
  },
  {
    name: '其他信息技术服务业',
    value: 6932,
  },
  {
    name: '咨询与调查',
    value: 6157,
  },
  {
    name: '软件和信息技术服务业',
    value: 5309,
  },
  {
    name: '机械设备经营租赁',
    value: 4959,
  },
  {
    name: '信息技术咨询服务',
    value: 4943,
  },
  {
    name: '综合管理服务',
    value: 3776,
  },
  {
    name: '商务服务业',
    value: 3608,
  },
  {
    name: '其他批发业',
    value: 3343,
  },
  {
    name: '机械设备、五金产品及电子产品批发',
    value: 3084,
  },
  {
    name: '工业与专业设计及其他专业技术服务',
    value: 2960,
  },
  {
    name: '食品、饮料及烟草制品批发',
    value: 2732,
  },
  {
    name: '综合零售',
    value: 2423,
  },
  {
    name: '信息系统集成和物联网技术服务',
    value: 2309,
  },
  {
    name: '运输代理业',
    value: 1897,
  },
  {
    name: '餐饮配送及外卖送餐服务',
    value: 1703,
  },
  {
    name: '财产保险',
    value: 1680,
  },
  {
    name: '零售业',
    value: 1677,
  },
  {
    name: '矿产品、建材及化工产品批发',
    value: 1586,
  },
  {
    name: '汽车、摩托车、零配件和燃料及其他动力销售',
    value: 1505,
  },
  {
    name: '批发业',
    value: 1467,
  },
  {
    name: '货摊、无店铺及其他零售业',
    value: 1366,
  },
  {
    name: '工程和技术研究和试验发展',
    value: 1338,
  },
  {
    name: '纺织、服装及家庭用品批发',
    value: 1223,
  },
  {
    name: '食品、饮料及烟草制品专门零售',
    value: 1214,
  },
  {
    name: '其他未列明制造业',
    value: 1184,
  },
  {
    name: '研究和试验发展',
    value: 1067,
  },
  {
    name: '人身保险',
    value: 1014,
  },
  {
    name: '其他居民服务业',
    value: 942,
  },
  {
    name: '法律服务',
    value: 929,
  },
  {
    name: '互联网信息服务',
    value: 840,
  },
  {
    name: '其他文化艺术业',
    value: 805,
  },
  {
    name: '房地产开发经营',
    value: 794,
  },
  {
    name: '广告业',
    value: 768,
  },
  {
    name: '工程技术与设计服务',
    value: 732,
  },
  {
    name: '医药及医疗器材批发',
    value: 731,
  },
  {
    name: '汽车、摩托车等修理与维护',
    value: 724,
  },
  {
    name: '科技推广和应用服务业',
    value: 707,
  },
  {
    name: '输配电及控制设备制造',
    value: 681,
  },
  {
    name: '其他通用设备制造业',
    value: 679,
  },
  {
    name: '汽车零部件及配件制造',
    value: 671,
  },
  {
    name: '其他食品制造',
    value: 660,
  },
  {
    name: '贸易经纪与代理',
    value: 633,
  },
  {
    name: '城市公共交通运输',
    value: 627,
  },
  {
    name: '医院',
    value: 620,
  },
  {
    name: '纺织、服装及日用品专门零售',
    value: 612,
  },
  {
    name: '物业管理',
    value: 601,
  },
  {
    name: '其他未列明建筑业',
    value: 580,
  },
  {
    name: '邮政业',
    value: 574,
  },
  {
    name: '房地产中介服务',
    value: 572,
  },
  {
    name: '塑料制品业',
    value: 571,
  },
  {
    name: '建筑装饰和装修业',
    value: 559,
  },
  {
    name: '土木工程建筑业',
    value: 542,
  },
  {
    name: '保险业',
    value: 528,
  },
  {
    name: '计算机、通信和其他电子设备制造业',
    value: 525,
  },
  {
    name: '饮料制造',
    value: 507,
  },
  {
    name: '电子器件制造',
    value: 488,
  },
  {
    name: '专用设备制造业',
    value: 481,
  },
  {
    name: '道路运输辅助活动',
    value: 477,
  },
  {
    name: '专业技术服务业',
    value: 464,
  },
  {
    name: '家用电器及电子产品专门零售',
    value: 462,
  },
  {
    name: '通用仪器仪表制造',
    value: 462,
  },
  {
    name: '其他仪器仪表制造业',
    value: 456,
  },
  {
    name: '信息处理和存储支持服务',
    value: 448,
  },
  {
    name: '道路运输业',
    value: 444,
  },
  {
    name: '五金、家具及室内装饰材料专门零售',
    value: 443,
  },
  {
    name: '公路旅客运输',
    value: 432,
  },
  {
    name: '文化体育娱乐活动与经纪代理服务',
    value: 413,
  },
  {
    name: '其他互联网服务',
    value: 398,
  },
  {
    name: '其他房屋建筑业',
    value: 386,
  },
  {
    name: '其他电子设备制造',
    value: 381,
  },
  {
    name: '互联网接入及相关服务',
    value: 369,
  },
  {
    name: '医学研究和试验发展',
    value: 368,
  },
  {
    name: '互联网平台',
    value: 364,
  },
  {
    name: '环保、邮政、社会公共服务及其他专用设备制造',
    value: 353,
  },
  {
    name: '电子元件及电子专用材料制造',
    value: 333,
  },
  {
    name: '电子和电工机械专用设备制造',
    value: 332,
  },
  {
    name: '互联网和相关服务',
    value: 329,
  },
  {
    name: '其他仓储业',
    value: 329,
  },
  {
    name: '金属加工机械制造',
    value: 328,
  },
  {
    name: '水上运输辅助活动',
    value: 328,
  },
  {
    name: '医药及医疗器材专门零售',
    value: 312,
  },
  {
    name: '通信设备制造',
    value: 309,
  },
  {
    name: '质检技术服务',
    value: 304,
  },
  {
    name: '通用设备制造业',
    value: 303,
  },
  {
    name: '农副食品加工业',
    value: 302,
  },
  {
    name: '电气机械和器材制造业',
    value: 301,
  },
  {
    name: '仪器仪表制造业',
    value: 299,
  },
  {
    name: '文艺创作与表演',
    value: 298,
  },
  {
    name: '医疗仪器设备及器械制造',
    value: 295,
  },
  {
    name: '方便食品制造',
    value: 291,
  },
  {
    name: '调味品、发酵制品制造',
    value: 290,
  },
  {
    name: '铁路、道路、隧道和桥梁工程建筑',
    value: 289,
  },
  {
    name: '居民服务业',
    value: 287,
  },
]

const platformData = [
  { name: 'BOSS直聘', value: '750', rate: 10 },
  { name: '58同城', value: '300', rate: 20 },
  { name: '智联招聘', value: '600', rate: 0 },
  { name: '前程无忧', value: '450', rate: -15 },
  { name: '拉勾网', value: '200', rate: -25 },
]

const platformChartData = [
  { name: 'BOSS直聘', value: 750 },
  { name: '58同城', value: 300 },
  { name: '智联招聘', value: 600 },
  { name: '前程无忧', value: 450 },
  { name: '拉勾网', value: 200 },
]

// 计算总数量和变化率
const totalCount = computed(() => {
  return platformChartData.reduce((sum, item) => sum + item.value, 0)
})

const changeRate = computed(() => {
  // 模拟变化率计算，实际应该从父组件传入
  return -15
})

// 获取变化率图标
const getRateIcon = (rate: number): string => {
  if (rate > 0) {
    return 'icon-shangsheng'
  } else if (rate < 0) {
    return 'icon-xiajiang'
  } else {
    return ''
  }
}

// 获取变化率颜色
const getRateColor = (rate: number): string => {
  if (rate > 0) {
    return 'text-green-400'
  } else if (rate < 0) {
    return 'text-red-400'
  } else {
    return 'text-gray-400'
  }
}

// 获取变化率显示文本
const getRateText = (rate: number): string => {
  if (rate > 0) {
    return '+' + rate + '%'
  } else if (rate < 0) {
    return rate + '%'
  } else {
    return '0%'
  }
}
</script>

<template>
  <div class="w-full grid grid-cols-4 h-[360px] gap-4 mt-5">
    <div
      class="col-span-1 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
    >
      <SecondTitle
        title="热门职位TOP100"
        subtext="按招聘人数排行"
        icon="icon-remen"
        icon-size="18"
      />
      <div class="relative flex flex-col flex-1 min-h-0">
        <RankList
          :data="industryRecruitmentData"
          tooltip-title="招聘总人数"
          unit="人"
          :show-count="10"
          period="5"
        />
      </div>
    </div>

    <div class="col-span-3 bg-white/5 rounded-lg p-4">
      <SecondTitle
        title="各招聘平台爬取职位相关数据量"
        subtext="用于分析各平台爬取数量"
        icon="icon-pachong"
        icon-size="18"
      />
      <div class="grid grid-cols-10 gap-4 flex-1 mt-4 min-h-0">
        <!-- 第一个子区域 -->
        <div
          class="col-span-4 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <FirstTitle title="各招聘平台职位总个数" />
          <div class="mt-4">
            <HorizontalRank :data="platformData" rate-title="较上周" />
          </div>
        </div>

        <!-- 第二个子区域 -->
        <div
          class="col-span-3 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <FirstTitle title="招聘平台职位列表数量" />
          <div class="mt-2">
            <!-- 顶部统计信息 -->
            <div class="flex items-center justify-between mb-4">
              <!-- 左侧总数量 -->
              <div class="flex flex-col">
                <span class="text-2xl font-DIN-Medium text-[#00ffff]"
                  >{{ totalCount.toLocaleString() }}
                  <span class="text-sm text-gray-400">个</span>
                </span>
                <span class="text-xs text-gray-400">总数量</span>
              </div>
              <!-- 右侧变化率 -->
              <div class="flex items-center gap-2">
                <Icon
                  v-if="changeRate !== 0"
                  :name="getRateIcon(changeRate)"
                  :color="getRateColor(changeRate)"
                  :size="16"
                />
                <div class="flex flex-col items-end">
                  <span class="text-sm font-DIN-Medium" :class="getRateColor(changeRate)">
                    {{ getRateText(changeRate) }}
                  </span>
                  <span class="text-xs text-gray-400">较上周</span>
                </div>
              </div>
            </div>

            <!-- 渐变柱状图 -->
            <GradientBarChart
              height="150px"
              :data="platformChartData"
              :x-axis-rotate="0"
              :bar-gradient="{
                startColor: '#ffd9a0',
                endColor: '#ffb86c',
              }"
              :grid="{
                top: '15%',
                bottom: '0%',
                left: '1%',
                right: '1%',
              }"
              :label-style="{
                fontSize: 9,
                color: '#ffd9a0',
              }"
              tooltip-title="平台职位列表爬取数量"
              quantifier="个"
            />
          </div>
        </div>

        <!-- 第三个子区域 -->
        <div
          class="col-span-3 bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <FirstTitle title="招聘平台职位详情数量" />
          <div class="mt-2">
            <!-- 顶部统计信息 -->
            <div class="flex items-center justify-between mb-4">
              <!-- 左侧总数量 -->
              <div class="flex flex-col">
                <span class="text-2xl font-DIN-Medium text-[#00ffff]"
                  >{{ totalCount.toLocaleString() }}
                  <span class="text-sm text-gray-400">个</span>
                </span>
                <span class="text-xs text-gray-400">总数量</span>
              </div>
              <!-- 右侧变化率 -->
              <div class="flex items-center gap-2">
                <Icon
                  v-if="changeRate !== 0"
                  :name="getRateIcon(changeRate)"
                  :color="getRateColor(changeRate)"
                  :size="16"
                />
                <div class="flex flex-col items-end">
                  <span class="text-sm font-DIN-Medium" :class="getRateColor(changeRate)">
                    {{ getRateText(changeRate) }}
                  </span>
                  <span class="text-xs text-gray-400">较上周</span>
                </div>
              </div>
            </div>

            <!-- 渐变柱状图 -->
            <GradientBarChart
              height="150px"
              :data="platformChartData"
              :x-axis-rotate="0"
              :bar-gradient="{
                startColor: '#a8ffce',
                endColor: '#faffd1',
              }"
              :grid="{
                top: '15%',
                bottom: '0%',
                left: '1%',
                right: '1%',
              }"
              :label-style="{
                fontSize: 9,
                color: '#a8ffce',
              }"
              tooltip-title="平台职位列表爬取数量"
              quantifier="个"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
