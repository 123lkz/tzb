<script setup lang="ts">
import { ref, computed } from 'vue'
import Header from '~/components/Layout/Header.vue'
import VTable from '~/components/common/VTable.vue'
import { $position } from '@base/api/Api'
import { useApiData } from '@base/composables/CachedAxiosClient'

const breadcrumbs = [
  { label: '首页', path: '/' },
  { label: '职位信息', path: '/position' },
  { label: '职位列表', path: '/position-list' }
]

const columns = [
  {
    title: '职位名称',
    key: 'name',
    width: 250,
    search: true
  },
  {
    title: '发布日期',
    key: 'publishTime',
    width: 130,
    sortable: true,
    formatter: (value: string) => {
      return value.split(' ')[0]
    }
  },
  {
    title: '月份过滤',
    key: 'date',
    hidden: true,
    search: {
      type: 'select' as const,
      options: [
        { label: '2025-01', value: '2025-01' },
        { label: '2025-02', value: '2025-02' },
        { label: '2025-03', value: '2025-03' },
        { label: '2025-04', value: '2025-04' },
        { label: '2025-05', value: '2025-05' },
        { label: '2025-06', value: '2025-06' },
        { label: '2025-07', value: '2025-07' },
        { label: '2025-08', value: '2025-08' },
        { label: '2025-09', value: '2025-09' },
        { label: '2025-10', value: '2025-10' },
        { label: '2025-11', value: '2025-11' },
        { label: '2025-12', value: '2025-12' },
        { label: '2026-01', value: '2026-01' },
        { label: '2026-02', value: '2026-02' },
        { label: '2026-03', value: '2026-03' },
        { label: '2026-04', value: '2026-04' },
        { label: '2026-05', value: '2026-05' },
        { label: '2026-06', value: '2026-06' },
        { label: '2026-07', value: '2026-07' },
        { label: '2026-08', value: '2026-08' },
        { label: '2026-09', value: '2026-09' },
        { label: '2026-10', value: '2026-10' },
        { label: '2026-11', value: '2026-11' },
        { label: '2026-12', value: '2026-12' }
      ]
    }
  },
  {
    title: '薪资区间',
    key: 'salaryReal'
  },
  {
    title: '月薪倍数',
    key: 'salary60',
    formatter: (value: string) => {
      return value ? value.split('·')[1] : '12薪'
    }
  },
  {
    title: '招聘人数',
    key: 'recruitNumber',
    sortable: true
  },
  {
    title: '学历要求',
    key: 'education',
    search: {
      type: 'select' as const,
      options: [
        { label: '学历不限', value: '学历不限' },
        { label: '高中及以下', value: '高中' },
        { label: '大专', value: '大专' },
        { label: '本科', value: '本科' },
        { label: '研究生及以上', value: '研究生及以上' }
      ]
    }
  },
  {
    title: '工作年限',
    key: 'workingExp',
    search: {
      type: 'select' as const,
      options: [
        { label: '1年以下', value: '1年以下' },
        { label: '1-3年', value: '1-3年' },
        { label: '3-5年', value: '3-5年' },
        { label: '5-10年', value: '5-10年' },
        { label: '10年以上', value: '10年以上' }
      ]
    }
  },
  {
    title: '所属单位',
    key: 'companyName',
    width: 240,
    search: true
  },
  {
    title: '工作省份',
    key: 'province',
    search: {
      type: 'select' as const,
      options: [
        // 直辖市
        { label: '北京市', value: '北京' },
        { label: '上海市', value: '上海' },
        { label: '天津市', value: '天津' },
        { label: '重庆市', value: '重庆' },

        // 省份
        { label: '河北省', value: '河北' },
        { label: '山西省', value: '山西' },
        { label: '辽宁省', value: '辽宁' },
        { label: '吉林省', value: '吉林' },
        { label: '黑龙江省', value: '黑龙江' },
        { label: '江苏省', value: '江苏' },
        { label: '浙江省', value: '浙江' },
        { label: '安徽省', value: '安徽' },
        { label: '福建省', value: '福建' },
        { label: '江西省', value: '江西' },
        { label: '山东省', value: '山东' },
        { label: '河南省', value: '河南' },
        { label: '湖北省', value: '湖北' },
        { label: '湖南省', value: '湖南' },
        { label: '广东省', value: '广东' },
        { label: '海南省', value: '海南' },
        { label: '四川省', value: '四川' },
        { label: '贵州省', value: '贵州' },
        { label: '云南省', value: '云南' },
        { label: '陕西省', value: '陕西' },
        { label: '甘肃省', value: '甘肃' },
        { label: '青海省', value: '青海' },

        // 自治区
        { label: '内蒙古自治区', value: '内蒙古' },
        { label: '广西壮族自治区', value: '广西' },
        { label: '西藏自治区', value: '西藏' },
        { label: '宁夏回族自治区', value: '宁夏' },
        { label: '新疆维吾尔自治区', value: '新疆' },

        // 特别行政区
        { label: '香港特别行政区', value: '香港' },
        { label: '澳门特别行政区', value: '澳门' },

        // 台湾省
        { label: '台湾省', value: '台湾' }
      ],
      placeholder: '选择省份'
    }
  },
  {
    title: '智联职位分类',
    key: 'classify',
    width: 180,
    search: true
  },
  {
    title: '职位链接',
    key: 'positionUrl'
  }
]

// 搜索和排序状态
const searchParams = ref({})
const sortParams = ref({
  sortField: 'publishTime' as 'publishTime' | 'recruitNumber',
  sortOrder: 'desc' as 'asc' | 'desc'
})

// 分页状态
const currentPage = ref(1)

// 导出状态
const exportLoading = ref(false)

const { data, pending, error, reload } = useApiData((isReload) =>
  $position.GetPositionList(
    {
      page: currentPage.value,
      pageSize: 20,
      ...searchParams.value,
      ...sortParams.value
    },
    {
      forceReload: isReload
    }
  )
)

// 确保 data 始终有默认值
const safeData = computed(() => {
  return data.value || { items: [], total: 0, totalPages: 0, page: 1, hasNext: false, hasPrev: false }
})

// 处理搜索
const handleSearch = (searchData: Record<string, string | number>) => {
  // 过滤掉空值，只保留有值的搜索参数
  const filteredSearchData: Record<string, string | number> = {}
  Object.entries(searchData).forEach(([key, value]) => {
    // 判断值是否为空：null、undefined、空字符串、只包含空格的字符串
    if (value !== null && value !== undefined && String(value).trim() !== '') {
      filteredSearchData[key] = value
    }
  })

  searchParams.value = filteredSearchData
  currentPage.value = 1 // 重置到第一页
  // 触发重新加载
  reload.value()
}

// 处理重置搜索
const handleReset = () => {
  searchParams.value = {}
  currentPage.value = 1 // 重置到第一页
  // 触发重新加载
  reload.value()
}

// 处理排序
const handleSort = (field: string, order: 'asc' | 'desc') => {
  sortParams.value = { sortField: field as 'publishTime' | 'recruitNumber', sortOrder: order }
  currentPage.value = 1 // 重置到第一页
  // 触发重新加载
  reload.value()
}

// 处理分页变化
const handlePageChange = (page: number) => {
  currentPage.value = page
  // 触发重新加载
  reload.value()
}

// 处理新增职位
const handleAddPosition = () => {
  // 这里可以添加新增职位的逻辑，比如打开弹窗或跳转页面
  // 例如：router.push('/position/add')
  alert('新增职位功能')
}

// 处理导出职位数据
const handleExportPositions = async () => {
  try {
    exportLoading.value = true

    // 构建查询参数
    const queryParams = new URLSearchParams({
      ...searchParams.value,
      ...sortParams.value
    }).toString()

    // 使用 fetch 直接请求文件
    const response = await fetch(`https://tte-api.smartedu.work/zjapi/position/export?${queryParams}`, {
      method: 'GET',
      headers: {
        Accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    // 获取 Blob 数据
    const blob = await response.blob()

    // 创建下载链接
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `职位列表_${new Date().toISOString().split('T')[0]}.xlsx`
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败，请稍后重试')
  } finally {
    exportLoading.value = false
  }
}

// 处理重新加载
const handleReload = () => {
  reload.value()
}
</script>

<template>
  <div class="flex flex-col h-full mt-4 px-4" :style="{ boxSizing: 'border-box', width: 'calc(100vw - 200px - 1rem)' }">
    <div class="flex-shrink-0 pr-4 mb-4">
      <Header :breadcrumbs="breadcrumbs" :show-scope="false" :show-province="false" :show-time="false"></Header>
    </div>
    <div class="w-full pr-4 pb-4 overflow-hidden" :style="`height: calc(100vh - 1rem - 48px`">
      <VTable
        :columns="columns"
        :data="safeData.items"
        :loading="pending"
        :error="error"
        :on-reload="handleReload"
        :total="safeData.total"
        :total-pages="safeData.totalPages"
        :current-page="safeData.page"
        :has-next="safeData.hasNext"
        :has-prev="safeData.hasPrev"
        :exportable="true"
        :export-loading="exportLoading"
        title="职位列表"
        @add="handleAddPosition"
        @export="handleExportPositions"
        @search="handleSearch"
        @reset="handleReset"
        @sort="handleSort"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>
