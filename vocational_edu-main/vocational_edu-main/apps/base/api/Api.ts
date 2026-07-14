/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface ListUserLoginLogsItem {
  /** IP */
  ip?: string;
  /**
   * 时间
   * @format date-time
   */
  time?: string;
}

export interface ListUserPasswordLogsItem {
  /** IP */
  ip?: string;
  /**
   * 时间
   * @format date-time
   */
  time?: string;
}

export interface ListUserPhoneLogsItem {
  /** IP */
  ip?: string;
  /**
   * 时间
   * @format date-time
   */
  time?: string;
}

export interface ListUserUsernameLogsItem {
  /** IP */
  ip?: string;
  /** 曾用名 */
  name?: string;
  /**
   * 时间
   * @format date-time
   */
  time?: string;
}

export interface ListUserItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 邮箱 */
  email?: string;
  /** 头像 */
  headImage?: string;
  /**
   * 上次登录时间
   * @format date-time
   */
  lastLogin?: string;
  /** 登录日志 */
  loginLogs?: ListUserLoginLogsItem[];
  /**
   * 注销时间
   * @format date-time
   */
  logoffAt?: string;
  /** 姓名 */
  name?: string;
  /** 密码修改日志 */
  passwordLogs?: ListUserPasswordLogsItem[];
  /** 手机号 */
  phone: string;
  /** 手机号修改日志 */
  phoneLogs?: ListUserPhoneLogsItem[];
  /**
   * 注册时间
   * @format date-time
   */
  registerAt?: string;
  /** 注册 IP */
  registerIp?: string;
  /** 角色 */
  roles?: string[];
  /** 联系电话 */
  telephone?: string;
  /**
   * Token 失效时间
   * @format date-time
   */
  tokenExp?: string;
  /** 用户名（昵称） */
  username?: string;
  /** 用户名修改日志 */
  usernameLogs?: ListUserUsernameLogsItem[];
}

export interface ListResultPageInfo {
  total: number;
  hasNextPage: boolean;
  hasPrevPage: boolean;
}

export interface ListUserResult {
  _status: string;
  _items: ListUserItem[];
  _pageInfo: ListResultPageInfo;
}

export interface MutateResult {
  _id: string;
  /** @format date-time */
  _updated: string;
  _etag: string;
}

export interface PositionScreenTrendResult {
  /** 月份/年份 */
  months: string[];
  /** 职位数 */
  positions: string[];
  /** 招聘人数 */
  recruitment: string[];
  /** 招聘单位数 */
  companies: string[];
  /** 职位数变化率 */
  positionChangeRate: string[];
  /** 招聘人数变化率 */
  recruitmentChangeRate: string[];
  /** 招聘单位数变化率 */
  companyChangeRate: string[];
}

export interface PositionScreenTotalResult {
  /** 总职位数 */
  totalPositions: number;
  /** 总招聘人数 */
  totalRecruitment: number;
  /** 总招聘单位数 */
  totalCompanies: number;
}

export interface PositionScreenProvinceResult {
  /** 省份分布数据 */
  provinceData: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface PositionDistributionResult {
  /** 学历要求分布 */
  educationRequirement: string[];
  /** 经验要求分布 */
  workingExpRequirement: string[];
  /** 公司规模分布 */
  companySizeDistribution: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface PositionScreenIndustryResult {
  /** 标准行业排行前100（招聘人数） */
  industryMediumByRecruitNumber: string[];
  /** 三大产业 */
  threeIndustryByRecruitNumber: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface PositionListItem {
  /** 职位ID */
  _id: string;
  /** 职位名称 */
  jobName: string;
  /** 省份 */
  province: string;
  /** 城市 */
  jobClassify: string;
  /** 公司名称 */
  companyName: string;
  /** 学历要求 */
  education: string;
  /** 工作经验要求 */
  workingExp: string;
  /** 发布时间 */
  publishTime: string;
  /** 招聘人数 */
  recruitNumber: number;
  /** 原始薪资区间和薪资倍数字符串 */
  salary60: string;
  /** 薪资区间和薪资字符串 */
  salaryReal: string;
  /** 职位URL */
  positionUrl: string;
}

export interface PositionListResult {
  /** 职位列表 */
  items: PositionListItem[];
  /** 总数量 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
  /** 总页数 */
  totalPages: number;
  /** 是否有下一页 */
  hasNext: boolean;
  /** 是否有上一页 */
  hasPrev: boolean;
}

export interface SalaryScreenTotalResult {
  /** 薪资25分位数 */
  p25Salary: number;
  /** 薪资50分位数 */
  p50Salary: number;
  /** 薪资75分位数 */
  p75Salary: number;
  /** 数据更新时间 */
  updateTime: string;
}

export interface SalaryScreenProvinceResult {
  /** 省份薪资中位数排行 */
  provinceData: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface SalaryScreenCareerResult {
  /** 小类职业薪资中位数排行 */
  standardXiaoleiRanking: string[];
  /** 细类职业薪资中位数排行 */
  standardXileiRanking: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface SalaryScreenIndustryResult {
  /** 标准行业薪资中位数排行前100 */
  industryRankBySalary: string[];
  /** 三大产业薪资中位数排行 */
  threeIndustriesBySalary: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface SalaryScreenDistributionResult {
  /** 公司规模分布 */
  companySizeDistribution: string[];
  /** 学历要求分布 */
  educationDistribution: string[];
  /** 经验要求分布 */
  workingExpDistribution: string[];
  /** 数据更新时间 */
  updateTime: string;
}

export interface CompanyResultItem {
  /** 名称 */
  name: string;
  /** 数量 */
  value: number;
  /** 排名 */
  rank: number;
}

export interface CompanyTrendResult {
  /** 月度/年度公司数量统计 */
  trend: CompanyResultItem[];
}

export interface CompanyProvinceResult {
  /** 省份公司分布 */
  provinceDistribution: CompanyResultItem[];
}

export interface CompanySizeResult {
  /** 公司规模分布 */
  sizeDistribution: CompanyResultItem[];
}

export interface CompanyPositionStatsResult {
  /** 发布职位最多的公司前100 */
  topCompaniesByPositionCount: CompanyResultItem[];
  /** 按招聘人数最多的公司前100 */
  topCompaniesByHiringCount: CompanyResultItem[];
  /** 按薪资中位数最高的公司前100 */
  topCompaniesBySalaryMedian: CompanyResultItem[];
}

export interface ListCompanyItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 备用电话列表 */
  additional_phones?: string[];
  /**
   * 最近核准日期
   * @format date-time
   */
  approval_date?: string;
  /** 主要联系电话 */
  business_phone?: string;
  /** 经营范围 */
  business_scope?: string;
  /** 经营状态 */
  business_status?: string;
  /** 营业期限 */
  business_term?: string;
  /** 城市 */
  city?: string;
  /** 唯一公司ID */
  company_id?: string;
  /** 公司全称 */
  company_name?: string;
  /** 公司规模 */
  company_size?: string;
  /** 公司类型 */
  company_type?: string;
  /**
   * 发布时间
   * @format date-time
   */
  create_time?: string;
  /** 统一社会信用代码 */
  credit_code?: string;
  /** 实际经营地址 */
  current_address?: string;
  /** 数据来源 */
  data_source?: string;
  /** 区县 */
  district?: string;
  /** 公司英文名称 */
  english_name?: string;
  /**
   * 成立日期
   * @format date-time
   */
  establishment_date?: string;
  /** 曾用名列表 */
  former_names?: string[];
  /** 失信记录 */
  has_dishonest_record?: boolean;
  /** 被执行记录 */
  has_execution_record?: boolean;
  /**
   * 导入日期
   * @format date-time
   */
  import_date?: string;
  /** 行业大类 */
  industry_category?: string;
  /** 行业编码 */
  industry_code?: string;
  /** 行业中类 */
  industry_major?: string;
  /** 行业小类 */
  industry_medium?: string;
  /** 行业细类 */
  industry_minor?: string;
  /** 法定代表人 */
  legal_representative?: string;
  /** 组织机构代码 */
  organization_code?: string;
  /** 实缴资本(万元) */
  paid_capital?: number;
  /** 母公司/集团 */
  parent_group?: string;
  /** 省份 */
  province?: string;
  /** 注册地址 */
  registered_address?: string;
  /** 注册资本(万元) */
  registered_capital?: number;
  /** 注册邮箱 */
  registered_email?: string;
  /** 登记机关 */
  registration_authority?: string;
  /** 工商注册号 */
  registration_number?: string;
  /** 股东列表 */
  shareholders?: string[];
  /** 社保缴纳人数 */
  social_security_count?: number;
  /** 验证邮箱 */
  verified_email?: string;
}

export interface ListCompanyResult {
  _status: string;
  _items: ListCompanyItem[];
  _pageInfo: ListResultPageInfo;
}

export interface ResultItem {
  /** 名称 */
  name: string;
  /** 数量 */
  value: number;
  /** 排名 */
  rank: number;
}

export interface ProvinceSchoolResult {
  /** 省份分布数据 */
  provinceData: ResultItem[];
}

export interface SchoolNumResult {
  /** 全部院校数量 */
  allSchoolNum: number;
  /** 双高院校数量 */
  doubleHighNum: number;
  /** 本科院校数量 */
  undergraduateNum: number;
  /** 专科院校数量 */
  specialtyNum: number;
}

export interface ListSchoolItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 是否为211 */
  is211?: number;
  /** 是否为985 */
  is985?: number;
  /** 是否为中央高校 */
  isCenter?: number;
  /** 是否为双高院校 */
  isDoubleHigh?: number;
  /** 是否为双一流 */
  isDoubleTop?: number;
  /** 是否为地方高校 */
  isLocal?: number;
  /** 办学层次 */
  level?: string;
  /** 城市 */
  location?: string;
  /** 主管部门 */
  manager?: string;
  /** 学校性质 */
  note?: string;
  /** 状态 */
  openState?: number;
  /** 省份 */
  province?: string;
  /** 学校名称 */
  school: string;
  /** 学校代码 */
  schoolCode?: number;
  /** 类型 */
  type?: string;
  /**
   * 更新时间
   * @format date-time
   */
  updateDate?: string;
}

export interface ListSchoolResult {
  _status: string;
  _items: ListSchoolItem[];
  _pageInfo: ListResultPageInfo;
}

export interface GraduateYearItem {
  /** 年份 */
  year: number;
  /** 招生人数 */
  enrollmentNum: number;
  /** 毕业生人数 */
  graduateNum: number;
  /** 在校学生数 */
  inSchoolNum: number;
  /** 双高院校招生人数 */
  dhEnrollmentNum: number;
  /** 非双高院校招生人数 */
  ndhEnrollmentNum: number;
  /** 双高院校毕业生人数 */
  dhGraduateNum: number;
  /** 非双高院校毕业生人数 */
  ndhGraduateNum: number;
  /** 双高院校在校学生数 */
  dhInSchoolNum: number;
  /** 非双高院校在校学生数 */
  ndhInSchoolNum: number;
}

export interface GraduateNumResult {
  /** 2016-2022年各年学生数量 */
  list: GraduateYearItem[];
}

export interface MajorByPositionResult {
  /** 专业名称列表 */
  major_name: string[];
  /** 专业代码列表 */
  major_code: string[];
  /** 学历层次列表 */
  education_level: string[];
  /** 对应职业名称 */
  job_name: string;
  /** 对应职业编码 */
  job_code: string;
  /** 匹配数量 */
  count: number;
}

export interface ListJobMajorMappingItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 学历层次 */
  education_level: string;
  /** 职业编码 */
  job_code: string;
  /** 职业名称 */
  job_name: string;
  /** 专业代码 */
  major_code: string;
  /** 专业名称 */
  major_name: string;
}

export interface ListJobMajorMappingResult {
  _status: string;
  _items: ListJobMajorMappingItem[];
  _pageInfo: ListResultPageInfo;
}

export interface ListJobOccupationMappingSourceOriginalHierarchyItem {
  /** 一级类目 */
  level_1?: string;
  /** 二级类目 */
  level_2?: string;
}

export interface ListJobOccupationMappingSourceItem {
  /** 来源名称 */
  name?: string;
  /** 来源原始层级 */
  original_hierarchy?: ListJobOccupationMappingSourceOriginalHierarchyItem;
}

export interface ListJobOccupationMappingStandardClassificationDaleiPrimaryItem {
  /** 编码 */
  code?: string;
  /** 名称 */
  name?: string;
}

export interface ListJobOccupationMappingStandardClassificationDaleiItem {
  /** 主匹配 */
  primary?: ListJobOccupationMappingStandardClassificationDaleiPrimaryItem;
}

export interface ListJobOccupationMappingStandardClassificationXiaoliPrimaryItem {
  /** 编码 */
  code?: string;
  /** 名称 */
  name?: string;
}

export interface ListJobOccupationMappingStandardClassificationXiaoliItem {
  /** 主匹配 */
  primary?: ListJobOccupationMappingStandardClassificationXiaoliPrimaryItem;
}

export interface ListJobOccupationMappingStandardClassificationXileiPrimaryItem {
  /** 编码 */
  code?: string;
  /** 名称 */
  name?: string;
}

export interface ListJobOccupationMappingStandardClassificationXileiItem {
  /** 主匹配 */
  primary?: ListJobOccupationMappingStandardClassificationXileiPrimaryItem;
}

export interface ListJobOccupationMappingStandardClassificationZhongleiPrimaryItem {
  /** 编码 */
  code?: string;
  /** 名称 */
  name?: string;
}

export interface ListJobOccupationMappingStandardClassificationZhongleiItem {
  /** 主匹配 */
  primary?: ListJobOccupationMappingStandardClassificationZhongleiPrimaryItem;
}

export interface ListJobOccupationMappingStandardClassificationItem {
  /** 大类（第一级） */
  dalei?: ListJobOccupationMappingStandardClassificationDaleiItem;
  /** 小类（第三级） */
  xiaoli?: ListJobOccupationMappingStandardClassificationXiaoliItem;
  /** 细类（第四级） */
  xilei?: ListJobOccupationMappingStandardClassificationXileiItem;
  /** 中类（第二级） */
  zhonglei?: ListJobOccupationMappingStandardClassificationZhongleiItem;
}

export interface ListJobOccupationMappingItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 职位名称 */
  position_name: string;
  /** 来源信息 */
  source?: ListJobOccupationMappingSourceItem;
  /** 标准职业分类映射 */
  standard_classification?: ListJobOccupationMappingStandardClassificationItem;
  /** 状态 */
  status?: string;
  /** 版本 */
  version?: string;
}

export interface ListJobOccupationMappingResult {
  _status: string;
  _items: ListJobOccupationMappingItem[];
  _pageInfo: ListResultPageInfo;
}

export interface GradeTreeItem {
  /** 级别(2/3/4/5) */
  level: number;
  /** 名称 */
  name: string;
  /** 编码 */
  code: string;
  /** 子级列表 */
  children?: any;
}

export interface SimpleItem {
  /** 名称 */
  name: string;
  /** 编码 */
  code: string;
}

export interface OccupationUpResult {
  /** 大类(1级) */
  dalei: SimpleItem[];
  /** 中类(2级) */
  zhonglei: SimpleItem[];
  /** 小类(3级) */
  xiaoli: SimpleItem[];
  /** 细类(4级，若请求level=4则返回) */
  xilei: SimpleItem[];
}

export interface OccupationDownResult {
  /** 大类(1级)列表 */
  dalei: SimpleItem[];
  /** 中类(2级)列表 */
  zhonglei: SimpleItem[];
  /** 小类(3级)列表 */
  xiaoli: SimpleItem[];
  /** 细类(4级)列表 */
  xilei: SimpleItem[];
}

export interface ListOccupationCategoriesItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 标准职业编码 */
  code: string;
  /** 职责描述 */
  description?: string;
  /** 国标码 */
  gbm_code?: string;
  /** 级别 */
  level: number;
  /** 名称 */
  name: string;
  /** 父级编码 */
  parent_code?: string;
  /** 父级国标码（可选） */
  parent_gbm_code?: string;
  /** 自顶向下编码路径 */
  path: string[];
  /** 后缀 */
  suffix?: string;
  /** 主要任务 */
  tasks?: string;
}

export interface ListOccupationCategoriesResult {
  _status: string;
  _items: ListOccupationCategoriesItem[];
  _pageInfo: ListResultPageInfo;
}

export interface ListIndustryItem {
  /** @format date-time */
  _created?: string;
  _etag: string;
  /**
   * ID
   * @format objectId
   */
  _id: string;
  /** @format date-time */
  _updated: string;
  /** 编码 */
  code: string;
  /** 职责描述 */
  description?: string;
  /** 级别 */
  level: number;
  /** 名称 */
  name: string;
  /** 父级编码 */
  parent_code?: string;
  /** 自顶向下编码路径 */
  path?: string;
}

export interface ListIndustryResult {
  _status: string;
  _items: ListIndustryItem[];
  _pageInfo: ListResultPageInfo;
}

import {
  CachedApi,
  ContentType,
  RequestParams,
} from "../composables/CachedAxiosClient";

import { ApiConfig } from "../composables/CachedAxiosClient";

let API: CachedApi;

export function initApi(config: ApiConfig) {
  API = new CachedApi(config);
  return API;
}

export const $user = {
  /**
   * No description
   *
   * @tags 用户账户
   * @name List
   * @summary 监管：获取用户列表
   * @request GET:/zjapi/User
   * @secure
   * @response `default` `ListUserResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListUserResult>({
      path: `/User`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 用户账户
   * @name Update
   * @summary 用户：更新信息
   * @request PATCH:/zjapi/User/{combinedId}
   * @secure
   * @response `default` `MutateResult`
   */
  Update: (
    combinedId: string,
    data: {
      /**
       * @format text
       * @maxLength 100
       */
      email?: string;
      /**
       * @format text
       * @maxLength 100
       */
      telephone?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<MutateResult>({
      path: `/User/${combinedId}`,
      method: "PATCH",
      body: data,
      type: ContentType.Json,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/User", ...parts);
  },
};

export const $base = {
  /**
 * No description
 * 
 * @tags 基础数据缓存管理
 * @name CacheAllCombinations
 * @summary 手动缓存所有4种组合的基础数据（异步执行）
 * @request GET:/zjapi/base/cache/all
 * @response `default` `{
  \** 是否成功启动 *\
    success?: boolean,
  \** 提示信息 *\
    message?: string,
  \** 任务ID *\
    taskId?: string,
  \** 总任务数 *\
    totalTasks?: number,

}` 批量缓存任务启动结果
 */
  CacheAllCombinations: (params: RequestParams = {}) =>
    API.request<{
      /** 是否成功启动 */
      success?: boolean;
      /** 提示信息 */
      message?: string;
      /** 任务ID */
      taskId?: string;
      /** 总任务数 */
      totalTasks?: number;
    }>({
      path: `/base/cache/all`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
 * No description
 * 
 * @tags 基础数据缓存管理
 * @name CacheSingleCombination
 * @summary 手动触发单个查询条件的基础数据缓存（异步执行）
 * @request GET:/zjapi/base/cache/single
 * @response `default` `{
  \** 是否成功启动 *\
    success?: boolean,
  \** 提示信息 *\
    message?: string,
  \** 任务ID *\
    taskId?: string,
  \** 缓存键 *\
    cacheKey?: string,

}` 缓存任务启动结果
 */
  CacheSingleCombination: (params: RequestParams = {}) =>
    API.request<{
      /** 是否成功启动 */
      success?: boolean;
      /** 提示信息 */
      message?: string;
      /** 任务ID */
      taskId?: string;
      /** 缓存键 */
      cacheKey?: string;
    }>({
      path: `/base/cache/single`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
 * No description
 * 
 * @tags 基础数据缓存管理
 * @name ClearYesterdayCache
 * @summary 清理昨天的缓存（保留今天的缓存）
 * @request POST:/zjapi/base/cache/clear-yesterday
 * @response `default` `{
  \** 是否全部成功 *\
    success?: boolean,
    clearedKeys?: (string)[],
    errors?: (string)[],

}` 清理操作结果
 */
  ClearYesterdayCache: (params: RequestParams = {}) =>
    API.request<{
      /** 是否全部成功 */
      success?: boolean;
      clearedKeys?: string[];
      errors?: string[];
    }>({
      path: `/base/cache/clear-yesterday`,
      method: "POST",
      format: "json",
      ...params,
    }),

  /**
 * No description
 * 
 * @tags 基础数据缓存管理
 * @name GetCacheStatus
 * @summary 获取缓存状态信息
 * @request GET:/zjapi/base/cache/status
 * @response `default` `{
    combinations?: ({
    params?: {
    dateType?: "month" | "year",
    caliberType?: "all" | "college",

},
    cacheKey?: string,
    exists?: boolean,
    ttl?: number,

})[],
    summary?: {
    total?: number,
    cached?: number,
    missing?: number,

},

}` 缓存状态信息
 */
  GetCacheStatus: (params: RequestParams = {}) =>
    API.request<{
      combinations?: {
        params?: {
          dateType?: "month" | "year";
          caliberType?: "all" | "college";
        };
        cacheKey?: string;
        exists?: boolean;
        ttl?: number;
      }[];
      summary?: {
        total?: number;
        cached?: number;
        missing?: number;
      };
    }>({
      path: `/base/cache/status`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
 * No description
 * 
 * @tags 基础数据缓存管理
 * @name CheckRedisMemory
 * @summary 检查Redis内存使用情况
 * @request GET:/zjapi/base/cache/redis-memory
 * @response `200` `{
    usedMemory?: string,
    maxMemory?: string,
    usagePercent?: number,
    evictionPolicy?: string,

}` Redis内存信息
 */
  CheckRedisMemory: (params: RequestParams = {}) =>
    API.request<{
      usedMemory?: string;
      maxMemory?: string;
      usagePercent?: number;
      evictionPolicy?: string;
    }>({
      path: `/base/cache/redis-memory`,
      method: "GET",
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/base", ...parts);
  },
};

export const $position = {
  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenTrendData
   * @summary 数据大屏：获取左侧职位趋势
   * @request GET:/zjapi/position/screen/trend/data
   * @response `default` `PositionScreenTrendResult`
   */
  GetScreenTrendData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionScreenTrendResult>({
      path: `/position/screen/trend/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenTotalData
   * @summary 数据大屏：获取总数量统计
   * @request GET:/zjapi/position/screen/total/data
   * @response `default` `PositionScreenTotalResult`
   */
  GetScreenTotalData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionScreenTotalResult>({
      path: `/position/screen/total/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenDataByProvince
   * @summary 数据大屏：获取各省份的招聘数量统计
   * @request GET:/zjapi/position/screen/province/data
   * @response `default` `PositionScreenProvinceResult`
   */
  GetScreenDataByProvince: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionScreenProvinceResult>({
      path: `/position/screen/province/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenDistributionData
   * @summary 数据大屏：获取学历要求分布、经验要求分布和公司规模分布
   * @request GET:/zjapi/position/screen/distribution/data
   * @response `default` `PositionDistributionResult`
   */
  GetScreenDistributionData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionDistributionResult>({
      path: `/position/screen/distribution/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenCareerRank
   * @summary 数据大屏：获取标准职业排行前40
   * @request GET:/zjapi/position/screen/career/rank
   * @response `default` `PositionDistributionResult`
   */
  GetScreenCareerRank: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionDistributionResult>({
      path: `/position/screen/career/rank`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetScreenIndustryData
   * @summary 数据大屏：获取标准行业前100名和三大产业数据
   * @request GET:/zjapi/position/screen/industry/data
   * @response `default` `PositionScreenIndustryResult`
   */
  GetScreenIndustryData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionScreenIndustryResult>({
      path: `/position/screen/industry/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetPositionList
   * @summary 获取职位列表（支持分页和排序）
   * @request GET:/zjapi/position/list
   * @response `default` `PositionListResult`
   */
  GetPositionList: (
    query?: {
      /**
       * 页码
       * @format float
       * @min 1
       * @default 1
       */
      page?: number;
      /**
       * 每页数量
       * @format float
       * @min 1
       * @max 100
       * @default 20
       */
      pageSize?: number;
      /**
       * 排序字段
       * @default "publishTime"
       */
      sortField?: "recruitNumber" | "publishTime";
      /**
       * 排序方向
       * @default "desc"
       */
      sortOrder?: "asc" | "desc";
      /** 职位名称 */
      name?: string;
      /** 公司名称 */
      companyName?: string;
      /** 省份 */
      province?: string;
      /** 学历要求 */
      education?: string;
      /** 工作经验要求 */
      workingExp?: string;
      /** 职位分类 */
      classify?: string;
      /** 月份过滤 (格式: YYYY-MM) */
      date?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<PositionListResult>({
      path: `/position/list`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name ExportPositionList
   * @summary 导出职位列表为Excel文件
   * @request GET:/zjapi/position/export
   * @response `default` `File` Excel文件下载
   */
  ExportPositionList: (
    query?: {
      /**
       * 页码
       * @format float
       * @min 1
       * @default 1
       */
      page?: number;
      /**
       * 每页数量
       * @format float
       * @min 1
       * @max 100
       * @default 20
       */
      pageSize?: number;
      /**
       * 排序字段
       * @default "publishTime"
       */
      sortField?: "recruitNumber" | "publishTime";
      /**
       * 排序方向
       * @default "desc"
       */
      sortOrder?: "asc" | "desc";
      /** 职位名称 */
      name?: string;
      /** 公司名称 */
      companyName?: string;
      /** 省份 */
      province?: string;
      /** 学历要求 */
      education?: string;
      /** 工作经验要求 */
      workingExp?: string;
      /** 职位分类 */
      classify?: string;
      /** 月份过滤 (格式: YYYY-MM) */
      date?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<File>({
      path: `/position/export`,
      method: "GET",
      query: query,
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetPositionLog
   * @summary 获取职教服务端项目日志
   * @request GET:/zjapi/position/log
   * @response `default` `string` PM2应用日志内容
   */
  GetPositionLog: (
    query: {
      lines: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<string>({
      path: `/position/log`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 职位
   * @name GetPositionErrorLog
   * @summary 获取职教服务端项目错误日志
   * @request GET:/zjapi/position/error-log
   * @response `default` `string` PM2应用错误日志内容
   */
  GetPositionErrorLog: (
    query: {
      lines: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<string>({
      path: `/position/error-log`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/position", ...parts);
  },
};

export const $salary = {
  /**
   * No description
   *
   * @tags 薪酬
   * @name GetScreenTotalData
   * @summary 数据大屏：获取薪资总数据概览
   * @request GET:/zjapi/salary/screen/total/data
   * @response `default` `SalaryScreenTotalResult`
   */
  GetScreenTotalData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<SalaryScreenTotalResult>({
      path: `/salary/screen/total/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 薪酬
   * @name GetScreenProvinceData
   * @summary 数据大屏：获取薪资省份排行数据
   * @request GET:/zjapi/salary/screen/province/data
   * @response `default` `SalaryScreenProvinceResult`
   */
  GetScreenProvinceData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<SalaryScreenProvinceResult>({
      path: `/salary/screen/province/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 薪酬
   * @name GetScreenCareerData
   * @summary 数据大屏：获取薪资职业排行数据
   * @request GET:/zjapi/salary/screen/career/data
   * @response `default` `SalaryScreenCareerResult`
   */
  GetScreenCareerData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<SalaryScreenCareerResult>({
      path: `/salary/screen/career/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 薪酬
   * @name GetScreenIndustryData
   * @summary 数据大屏：获取薪资行业排行数据
   * @request GET:/zjapi/salary/screen/industry/data
   * @response `default` `SalaryScreenIndustryResult`
   */
  GetScreenIndustryData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<SalaryScreenIndustryResult>({
      path: `/salary/screen/industry/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 薪酬
   * @name GetScreenDistributionData
   * @summary 数据大屏：获取薪资分布数据
   * @request GET:/zjapi/salary/screen/distribution/data
   * @response `default` `SalaryScreenDistributionResult`
   */
  GetScreenDistributionData: (
    query?: {
      /**
       * 年度/月度
       * @format text
       * @maxLength 50
       */
      dateType?: string;
      /**
       * 全口径/应届大专生
       * @format text
       * @maxLength 50
       */
      caliberType?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<SalaryScreenDistributionResult>({
      path: `/salary/screen/distribution/data`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/salary", ...parts);
  },
};

export const $company = {
  /**
   * No description
   *
   * @tags 公司
   * @name GetTrendStats
   * @summary 数据中台：按时间获取公司数量趋势统计
   * @request GET:/zjapi/Company/trends
   * @response `default` `CompanyTrendResult`
   */
  GetTrendStats: (
    query?: {
      /**
       * 省份名称
       * @format text
       * @maxLength 50
       */
      province?: string;
      /**
       * 城市名称
       * @format text
       * @maxLength 50
       */
      city?: string;
      /**
       * 时间类型
       * @format text
       * @maxLength 50
       */
      trendType?: string;
      /**
       * 公司规模
       * @format text
       * @maxLength 50
       */
      companySize?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<CompanyTrendResult>({
      path: `/Company/trends`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 公司
   * @name GetProvinceStats
   * @summary 数据中台：按省份获取公司数量统计
   * @request GET:/zjapi/Company/province
   * @response `default` `CompanyProvinceResult`
   */
  GetProvinceStats: (
    query?: {
      /**
       * 省份名称
       * @format text
       * @maxLength 50
       */
      province?: string;
      /**
       * 城市名称
       * @format text
       * @maxLength 50
       */
      city?: string;
      /**
       * 时间类型
       * @format text
       * @maxLength 50
       */
      trendType?: string;
      /**
       * 公司规模
       * @format text
       * @maxLength 50
       */
      companySize?: string;
      /**
       * 日期
       * @format text
       * @maxLength 50
       */
      selectedDate?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<CompanyProvinceResult>({
      path: `/Company/province`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 公司
   * @name GetSizeStats
   * @summary 数据中台：按规模获取公司数量统计
   * @request GET:/zjapi/Company/size
   * @response `default` `CompanySizeResult`
   */
  GetSizeStats: (
    query?: {
      /**
       * 省份名称
       * @format text
       * @maxLength 50
       */
      province?: string;
      /**
       * 城市名称
       * @format text
       * @maxLength 50
       */
      city?: string;
      /**
       * 时间类型
       * @format text
       * @maxLength 50
       */
      trendType?: string;
      /**
       * 公司规模
       * @format text
       * @maxLength 50
       */
      companySize?: string;
      /**
       * 日期
       * @format text
       * @maxLength 50
       */
      selectedDate?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<CompanySizeResult>({
      path: `/Company/size`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 公司
   * @name GetPositionStats
   * @summary 数据中台：获取公司职位统计排行
   * @request GET:/zjapi/Company/position-stats
   * @response `default` `CompanyPositionStatsResult`
   */
  GetPositionStats: (
    query?: {
      /**
       * 省份名称
       * @format text
       * @maxLength 50
       */
      province?: string;
      /**
       * 城市名称
       * @format text
       * @maxLength 50
       */
      city?: string;
      /**
       * 时间类型
       * @format text
       * @maxLength 50
       */
      trendType?: string;
      /**
       * 公司规模
       * @format text
       * @maxLength 50
       */
      companySize?: string;
      /**
       * 日期
       * @format text
       * @maxLength 50
       */
      selectedDate?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<CompanyPositionStatsResult>({
      path: `/Company/position-stats`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 公司
   * @name List
   * @summary 获取公司列表
   * @request GET:/zjapi/Company
   * @response `default` `ListCompanyResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListCompanyResult>({
      path: `/Company`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/Company", ...parts);
  },
};

export const $schools = {
  /**
   * No description
   *
   * @tags 学校
   * @name GetSchoolNumByProvince
   * @summary 获取各省学校数量
   * @request GET:/zjapi/Schools/getByProvince
   * @response `default` `ProvinceSchoolResult`
   */
  GetSchoolNumByProvince: (
    query?: {
      /**
       * 办学层次
       * @format text
       * @maxLength 50
       */
      level?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<ProvinceSchoolResult>({
      path: `/Schools/getByProvince`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校
   * @name GetSchoolNum
   * @summary 查询院校数量
   * @request GET:/zjapi/Schools/getSchoolNum
   * @response `default` `SchoolNumResult`
   */
  GetSchoolNum: (params: RequestParams = {}) =>
    API.request<SchoolNumResult>({
      path: `/Schools/getSchoolNum`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
 * No description
 * 
 * @tags 学校
 * @name UpdateDoubleHighStatus
 * @summary 更新双高院校标识
 * @request GET:/zjapi/Schools/updateDoubleHighStatus
 * @response `default` `{
    updated?: number,
    total?: number,

}` 更新结果
 */
  UpdateDoubleHighStatus: (params: RequestParams = {}) =>
    API.request<{
      updated?: number;
      total?: number;
    }>({
      path: `/Schools/updateDoubleHighStatus`,
      method: "GET",
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/Schools", ...parts);
  },
};

export const $school = {
  /**
   * No description
   *
   * @tags 学校
   * @name List
   * @summary 获取学校列表
   * @request GET:/zjapi/School
   * @response `default` `ListSchoolResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
      /**
       * 分页(从1开始)
       * @format float
       * @min 1
       */
      page?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListSchoolResult>({
      path: `/School`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/School", ...parts);
  },
};

export const $schoolEnrollment = {
  /**
   * No description
   *
   * @tags 学校招生
   * @name GetStudentNumByProvince
   * @summary 获取各省份在校生人数2020-2022年
   * @request GET:/zjapi/SchoolEnrollment/getStudentNumByProvince
   * @response `default` `ProvinceSchoolResult`
   */
  GetStudentNumByProvince: (
    query?: {
      /**
       * 办学层次
       * @format text
       * @maxLength 50
       */
      category?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<ProvinceSchoolResult>({
      path: `/SchoolEnrollment/getStudentNumByProvince`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校招生
   * @name GetSchoolNumByProvince
   * @summary 获取各省份学校数量（含双高院校数量）
   * @request GET:/zjapi/SchoolEnrollment/getSchoolNumByProvince
   * @response `default` `ProvinceSchoolResult`
   */
  GetSchoolNumByProvince: (
    query?: {
      /**
       * 办学层次
       * @format text
       * @maxLength 50
       */
      category?: string;
      /** 年份 */
      year?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ProvinceSchoolResult>({
      path: `/SchoolEnrollment/getSchoolNumByProvince`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校招生
   * @name GetStudentNumByMajor
   * @summary 统计各专业学生数量2020-2022年
   * @request GET:/zjapi/SchoolEnrollment/getStudentNumByMajor
   * @response `default` `ProvinceSchoolResult`
   */
  GetStudentNumByMajor: (
    query?: {
      /**
       * 办学层次
       * @format text
       * @maxLength 50
       */
      category?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<ProvinceSchoolResult>({
      path: `/SchoolEnrollment/getStudentNumByMajor`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校招生
   * @name GetStudentNumByYear
   * @summary 统计2017-2022年各年的招生、毕业、在校人数
   * @request GET:/zjapi/SchoolEnrollment/getStudentNumByYear
   * @response `default` `GraduateNumResult`
   */
  GetStudentNumByYear: (
    query?: {
      /**
       * 办学层次
       * @format text
       * @maxLength 50
       */
      category?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<GraduateNumResult>({
      path: `/SchoolEnrollment/getStudentNumByYear`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校招生
   * @name GetSchoolNum
   * @summary 统计专科双高/非双高院校数量
   * @request GET:/zjapi/SchoolEnrollment/getSchoolNum
   * @response `default` `ProvinceSchoolResult`
   */
  GetSchoolNum: (params: RequestParams = {}) =>
    API.request<ProvinceSchoolResult>({
      path: `/SchoolEnrollment/getSchoolNum`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 学校招生
   * @name GetMajorByPosition
   * @summary 统计标准职业对应专业词云
   * @request GET:/zjapi/SchoolEnrollment/getMajorByPosition
   * @response `default` `(MajorByPositionResult)[]`
   */
  GetMajorByPosition: (params: RequestParams = {}) =>
    API.request<MajorByPositionResult[]>({
      path: `/SchoolEnrollment/getMajorByPosition`,
      method: "GET",
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/SchoolEnrollment", ...parts);
  },
};

export const $jobMajorMapping = {
  /**
   * No description
   *
   * @tags 职业-专业对应表
   * @name List
   * @summary 获取职业对应专业列表
   * @request GET:/zjapi/JobMajorMapping
   * @response `default` `ListJobMajorMappingResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
      /**
       * 分页(从1开始)
       * @format float
       * @min 1
       */
      page?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListJobMajorMappingResult>({
      path: `/JobMajorMapping`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/JobMajorMapping", ...parts);
  },
};

export const $jobOccupationMapping = {
  /**
   * No description
   *
   * @tags 职位到标准职业分类映射表
   * @name List
   * @summary 获取职位到标准职业映射列表
   * @request GET:/zjapi/JobOccupationMapping
   * @response `default` `ListJobOccupationMappingResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
      /**
       * 分页(从1开始)
       * @format float
       * @min 1
       */
      page?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListJobOccupationMappingResult>({
      path: `/JobOccupationMapping`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/JobOccupationMapping", ...parts);
  },
};

export const $occupationCategories = {
  /**
   * No description
   *
   * @tags 标准职业分类
   * @name GetGradeList
   * @summary 返回分级数据
   * @request GET:/zjapi/occupationCategories/standard/all
   * @response `default` `(GradeTreeItem)[]`
   */
  GetGradeList: (params: RequestParams = {}) =>
    API.request<GradeTreeItem[]>({
      path: `/occupationCategories/standard/all`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 标准职业分类
   * @name GetUpByLevel
   * @summary 返回当前级别及其上层的数据
   * @request GET:/zjapi/occupationCategories/standard/up
   * @response `default` `OccupationUpResult`
   */
  GetUpByLevel: (
    query: {
      /**
       * 级别(1/2/3/4)
       * @min 1
       * @max 4
       */
      level: number;
      /**
       * 名称
       * @format text
       * @maxLength 200
       */
      name?: string;
      /**
       * 编码
       * @format text
       * @maxLength 50
       */
      code?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<OccupationUpResult>({
      path: `/occupationCategories/standard/up`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 标准职业分类
   * @name GetDownByLevel
   * @summary 返回当前级别及其下属数据
   * @request GET:/zjapi/occupationCategories/standard/down
   * @response `default` `OccupationDownResult`
   */
  GetDownByLevel: (
    query?: {
      /**
       * 父级小类编码(3级)
       * @format text
       * @maxLength 50
       */
      code?: string;
      /**
       * 父级小类名称(3级)
       * @format text
       * @maxLength 200
       */
      name?: string;
    },
    params: RequestParams = {},
  ) =>
    API.request<OccupationDownResult>({
      path: `/occupationCategories/standard/down`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 标准职业分类
   * @name List
   * @summary 获取职业分类列表
   * @request GET:/zjapi/OccupationCategories
   * @response `default` `ListOccupationCategoriesResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
      /**
       * 分页(从1开始)
       * @format float
       * @min 1
       */
      page?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListOccupationCategoriesResult>({
      path: `/OccupationCategories`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/OccupationCategories", ...parts);
  },
};

export const $industry = {
  /**
   * No description
   *
   * @tags 标准行业
   * @name GetGradeList
   * @summary 返回分级数据（从2级开始，支持到5级）
   * @request GET:/zjapi/industry/standard/all
   * @response `default` `(GradeTreeItem)[]`
   */
  GetGradeList: (params: RequestParams = {}) =>
    API.request<GradeTreeItem[]>({
      path: `/industry/standard/all`,
      method: "GET",
      format: "json",
      ...params,
    }),

  /**
   * No description
   *
   * @tags 标准行业
   * @name List
   * @summary 获取职业分类列表
   * @request GET:/zjapi/Industry
   * @response `default` `ListIndustryResult`
   */
  List: (
    query?: {
      /**
       * 游标分页：之后
       * @format cursor
       * @maxLength 200
       */
      after?: string;
      /**
       * 游标分页：之前
       * @format cursor
       * @maxLength 200
       */
      before?: string;
      /**
       * 数量限制
       * @format float
       * @min 1
       * @max 200
       */
      limit?: number;
      /**
       * 查询条件
       * @format query-string
       * @maxLength 200
       */
      query?: string;
      /**
       * 排序字段
       * @format sort-string
       * @maxLength 200
       */
      sort?: string;
      /**
       * 字段过滤
       * @format field-filter-string
       * @maxLength 200
       */
      fields?: string;
      /**
       * 分页(从1开始)
       * @format float
       * @min 1
       */
      page?: number;
    },
    params: RequestParams = {},
  ) =>
    API.request<ListIndustryResult>({
      path: `/Industry`,
      method: "GET",
      query: query,
      format: "json",
      ...params,
    }),

  Reload: (...parts: string[]) => {
    return API.removeCache("/Industry", ...parts);
  },
};
