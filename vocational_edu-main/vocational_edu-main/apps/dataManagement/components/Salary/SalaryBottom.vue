<script setup lang="ts">
import Icon from '../common/Icon.vue'
import SecondTitle from '../common/Title/SecondTitle.vue'
import RankList from '../common/RankList/RankList.vue'
import MultiBarChart from '../Echart/MultiBarChart.vue'

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

const handleClickCareer = () => {
  console.log('handleClick')
}

const handleClickIndustry = () => {
  console.log('handleClick')
}

const data = [
  {
    name: '农、林、牧、渔业',
    values: [
      {
        name: '城镇非私营单位',
        value: 62952,
      },
      {
        name: '城镇私营单位',
        value: 44465,
      },
    ],
  },
  {
    name: '采矿业',
    values: [
      {
        name: '城镇非私营单位',
        value: 135025,
      },
      {
        name: '城镇私营单位',
        value: 75648,
      },
    ],
  },
  {
    name: '制造业',
    values: [
      {
        name: '城镇非私营单位',
        value: 103932,
      },
      {
        name: '城镇私营单位',
        value: 71762,
      },
    ],
  },
  {
    name: '电力、燃气及水的生产和供应业',
    values: [
      {
        name: '城镇非私营单位',
        value: 143594,
      },
      {
        name: '城镇私营单位',
        value: 64826,
      },
    ],
  },
  {
    name: '建筑业',
    values: [
      {
        name: '城镇非私营单位',
        value: 85804,
      },
      {
        name: '城镇私营单位',
        value: 63857,
      },
    ],
  },
  {
    name: '交通运输、仓储和邮政业',
    values: [
      {
        name: '城镇非私营单位',
        value: 122705,
      },
      {
        name: '城镇私营单位',
        value: 68051,
      },
    ],
  },
  {
    name: '信息传输、计算机服务和软件业',
    values: [
      {
        name: '城镇非私营单位',
        value: 231810,
      },
      {
        name: '城镇私营单位',
        value: 129215,
      },
    ],
  },
  {
    name: '批发和零售业',
    values: [
      {
        name: '城镇非私营单位',
        value: 124362,
      },
      {
        name: '城镇私营单位',
        value: 63701,
      },
    ],
  },
  {
    name: '住宿和餐饮业',
    values: [
      {
        name: '城镇非私营单位',
        value: 58094,
      },
      {
        name: '城镇私营单位',
        value: 51583,
      },
    ],
  },
  {
    name: '金融业',
    values: [
      {
        name: '城镇非私营单位',
        value: 197663,
      },
      {
        name: '城镇私营单位',
        value: 124812,
      },
    ],
  },
  {
    name: '房地产业',
    values: [
      {
        name: '城镇非私营单位',
        value: 91932,
      },
      {
        name: '城镇私营单位',
        value: 56119,
      },
    ],
  },
  {
    name: '租赁和商务服务业',
    values: [
      {
        name: '城镇非私营单位',
        value: 109264,
      },
      {
        name: '城镇私营单位',
        value: 67107,
      },
    ],
  },
  {
    name: '科学研究、技术服务和地质勘查业',
    values: [
      {
        name: '城镇非私营单位',
        value: 171447,
      },
      {
        name: '城镇私营单位',
        value: 82277,
      },
    ],
  },
  {
    name: '水利、环境和公共设施管理业',
    values: [
      {
        name: '城镇非私营单位',
        value: 68656,
      },
      {
        name: '城镇私营单位',
        value: 47504,
      },
    ],
  },
  {
    name: '居民服务和其他服务业',
    values: [
      {
        name: '城镇非私营单位',
        value: 68919,
      },
      {
        name: '城镇私营单位',
        value: 49907,
      },
    ],
  },
  {
    name: '教育',
    values: [
      {
        name: '城镇非私营单位',
        value: 124067,
      },
      {
        name: '城镇私营单位',
        value: 55775,
      },
    ],
  },
  {
    name: '卫生、社会保障和社会福利业',
    values: [
      {
        name: '城镇非私营单位',
        value: 143818,
      },
      {
        name: '城镇私营单位',
        value: 74462,
      },
    ],
  },
  {
    name: '文化、体育和娱乐业',
    values: [
      {
        name: '城镇非私营单位',
        value: 127334,
      },
      {
        name: '城镇私营单位',
        value: 59407,
      },
    ],
  },
  {
    name: '公共管理和社会组织',
    values: [
      {
        name: '城镇非私营单位',
        value: 117108,
      },
      {
        name: '城镇私营单位',
        value: 0,
      },
    ],
  },
]
</script>

<template>
  <div class="w-full h-[440px] shadow-md mt-5 grid grid-cols-2 gap-4 flex-shrink-0 overflow-hidden">
    <div
      class="bg-white/5 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(255,255,255,0.1)] border border-white/10 w-full flex flex-col"
    >
      <div class="text-[#00ffff] flex justify-center gap-2 mb-4">
        <Icon name="icon-paihang" color="text-[#00ffff]" :size="20" />
        <span class="text-sm">薪资中位数排行</span>
      </div>
      <div class="grid grid-cols-2 gap-4 w-full">
        <div
          class="bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <SecondTitle
            title="薪资中位数排行"
            type="circle"
            icon="icon-gangwei"
            :icon-size="20"
            subtext="按标准职业分类第三级"
            show-text-button
            button-text="全部"
            @click="handleClickCareer"
          />
          <div class="relative flex flex-col flex-1 min-h-0">
            <RankList
              :data="industryRecruitmentData"
              tooltip-title="薪资中位数"
              unit="元"
              :show-count="10"
              period="5"
            />
          </div>
        </div>
        <div
          class="bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-2 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full"
        >
          <SecondTitle
            title="薪资中位数排行"
            type="circle"
            icon="icon-dianlihangye"
            :icon-size="20"
            subtext="按标准行业分类第三级"
            show-text-button
            button-text="全部"
            @click="handleClickIndustry"
          />
          <div class="relative flex flex-col flex-1 min-h-0">
            <RankList
              :data="industryRecruitmentData"
              tooltip-title="薪资中位数"
              unit="元"
              :show-count="10"
              period="5"
            />
          </div>
        </div>
      </div>
    </div>

    <div
      class="bg-[#00ffff]/5 backdrop-blur-sm rounded-lg p-4 text-white shadow-[inset_0_0_15px_rgba(0,255,255,0.1)] border border-[#00ffff]/20 w-full relative"
    >
      <SecondTitle
        title="按行业分城镇非私营单位和私营单位就业人员平均工资"
        icon="icon-a-zhuxingtu2"
        :icon-size="20"
        subtext="2023年年薪"
        @click="handleClickIndustry"
      />
      <MultiBarChart
        :data="data"
        height="350px"
        quantifier="元"
        tooltip-title="就业人员平均工资"
        :show-legend="true"
        :show-label="false"
        :grid="{ top: '25%', bottom: '5%', left: '0%', right: '0%' }"
        :x-axis-interval="1"
        :x-axis-max-length="3"
        :legend-style="{
          textStyle: { color: 'rgba(255,255,255,0.7)', fontSize: 12 },
        }"
      />
      <div class="absolute right-4 bottom-4 text-xs text-white/50">数据来源：国家统计局</div>
    </div>
  </div>
</template>

<style scoped></style>
