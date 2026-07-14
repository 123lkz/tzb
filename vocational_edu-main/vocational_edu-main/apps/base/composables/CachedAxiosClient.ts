import { useNuxtApp, useState } from '#imports'
import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, ResponseType } from 'axios'
import axios from 'axios'
import type { ShallowReactive, ToRefs } from 'vue'
import { getCurrentScope, reactive, ref, shallowReactive, toRefs, watchEffect } from 'vue'

export function isPromise(obj: any): obj is Promise<any> {
  return !!obj && (typeof obj === 'object' || typeof obj === 'function') && typeof obj.then === 'function'
}

export function isLoadingOrNull(obj: any): obj is Promise<any> {
  return isPromise(obj) || !obj
}

export type _Transform<Input, Output> = (input: Input) => Output

export type QueryParamsType = Record<string | number, any>

interface ApiDataOptions<DataT, Transform extends _Transform<DataT, any> = _Transform<DataT, DataT>> {
  parser?: Transform
  onLoaded?: (data: ReturnType<Transform> | null) => void
  onError?: (e: any) => void
  clearBeforeReload?: boolean
  resolvePendingDelay?: number
  initData?: any
}

export type ApiDataResult<DataT, Transform extends _Transform<DataT, any> = _Transform<DataT, DataT>> = {
  data: ReturnType<Transform> | null
  pending: boolean
  error: boolean
  reload: () => void
}

// 类似 nuxt 的 useAsyncData
export function useApiData<DataT, Transform extends _Transform<DataT, any> = _Transform<DataT, DataT>>(
  getter: (isReload?: boolean) => Promise<DataT> | null,
  setting?: ApiDataOptions<DataT, Transform>
) {
  const self = shallowReactive<ApiDataResult<DataT, Transform>>({
    data: null,
    pending: false,
    error: false,
    reload: () => {
      self.data = null
      getterId.value++
    }
  })

  if (!getCurrentScope()) {
    console.error('请在 setup 函数内使用 useApiData')
    return toRefs(self)
  }

  const cache = ref<any>(null)
  let lastGetterId = 1
  const getterId = ref(1)
  let pendingTimer: any = null

  function resolveData(d: any, isError = false) {
    clearTimeout(pendingTimer)
    pendingTimer = setTimeout(() => {
      self.pending = false
    }, setting?.resolvePendingDelay || 100)
    if (isError || (d && '_status' in d && d._status === 'ERR')) {
      self.error = true
      self.data = null
      if (setting?.onError) {
        setTimeout(() => setting?.onError!(d || new Error('Unknown error')))
      }
      return
    }
    if (d) {
      if (setting?.parser) {
        self.data = setting.parser(d)
      } else {
        self.data = d
      }
    } else {
      self.data = null
    }
    if (setting?.onLoaded) {
      setTimeout(() => setting?.onLoaded!(self.data))
    }
  }

  let dataResolved = false

  if (import.meta.client) {
    watchEffect(() => {
      if (setting?.clearBeforeReload) {
        self.data = null
      }
      if (setting?.initData) {
        cache.value = setting.initData
        self.data = setting.parser ? setting.parser(setting.initData) : setting.initData
        self.pending = false
        if (setting.onLoaded) {
          setting.onLoaded(self.data)
        }
        delete setting.initData
        return
      }
      cache.value = getter(getterId.value !== lastGetterId)

      lastGetterId = getterId.value

      if (isPromise(cache.value)) {
        // 如果 getter 返回的是 promise，可能有两种结果：
        // 返回的是 promise-like 的响应式数据，会先被 watch 监听到一次，然后被 resolve
        // 返回的是 promise，只会被 resolve 一次
        // 在第一种情况下，使用 dataResolved 进行标记
        // 如果 getter 返回的是数据，直接 resolve
        dataResolved = false // 确保一个 promise 只被 resolve 一次
        self.pending = true
        clearTimeout(pendingTimer)
        cache.value.then((d: any) => {
          if (!dataResolved) {
            dataResolved = true
            resolveData(d)
          }
        })
        cache.value.catch((e) => {
          if (!dataResolved) {
            dataResolved = true
            resolveData(e, true)
          } else {
            clearTimeout(pendingTimer)
            pendingTimer = setTimeout(() => {
              self.pending = false
            }, setting?.resolvePendingDelay || 100)
          }
        })
      } else {
        dataResolved = true
        resolveData(cache.value)
      }
    })
  }

  return toRefs(self)
}

export async function useAsyncApiData<DataT, Transform extends _Transform<DataT, any> = _Transform<DataT, DataT>>(
  getter: (isReload?: boolean) => Promise<DataT> | null,
  setting?: ApiDataOptions<DataT, Transform>
): Promise<ToRefs<ShallowReactive<ApiDataResult<DataT, Transform>>>> {
  if (import.meta.client) {
    return new Promise((resolve, reject) => {
      const ret = useApiData(getter, {
        ...setting,
        onLoaded(data) {
          setting?.onLoaded?.(data)
          resolve(ret)
        },
        onError(e) {
          reject(e)
        }
      }) as ToRefs<ShallowReactive<ApiDataResult<DataT, Transform>>>
    })
  }
  const self = shallowReactive<ApiDataResult<DataT, Transform>>({
    data: null,
    pending: false,
    error: false,
    reload: () => {
      self.data = null
    }
  })

  const nuxtApp = useNuxtApp()

  try {
    const ret = await nuxtApp.runWithContext(getter)
    if (ret) {
      self.data = setting?.parser ? setting.parser(ret) : ret
    }
    if (setting?.onLoaded) {
      setting.onLoaded(self.data)
    }
  } catch (e) {
    self.data = null
    self.error = true
  } finally {
    self.pending = false
  }

  return toRefs(self)
}

export type RemoveCacheMode = 'single' | 'prefix' | 'none'

export enum ContentType {
  Json = 'application/json',
  FormData = 'multipart/form-data',
  UrlEncoded = 'application/x-www-form-urlencoded'
}

export interface FullRequestParams extends Omit<AxiosRequestConfig, 'data' | 'params' | 'url' | 'responseType'> {
  /** request path */
  path: string
  /** content type of request body */
  type?: ContentType
  /** query params */
  query?: QueryParamsType
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseType
  /** request body */
  body?: unknown

  removeRelativeCache?: RemoveCacheMode // mutate 操作中，移除缓存，默认为 'prefix' 模式

  forceReload?: boolean // GET 操作中，是否重新加载数据

  disableCache?: boolean // GET 操作，是否禁用缓存

  ignoreError?: boolean
}

export type RequestParams = Omit<FullRequestParams, 'body' | 'method' | 'query' | 'path'>

export type ApiStore = {
  readonly requestCache: Record<string, any>
  readonly objectCache: Record<string, any>
  clearStore: () => void
  prepare: (...args: any[]) => void
}

export type ApiConfig = {
  baseUrl: () => string
  responseHandler: (response: AxiosResponse) => any
  extractItems: (data: any, url: string) => null | { id: string; data?: any }[]
  errorHandler: (error: AxiosError, api: CachedApi) => Error

  store?: ApiStore
}

class TwoWayMap {
  map: Record<string, number> = {}
  reverseMap: Record<number, string> = {}

  get(key: string) {
    return this.map[key]
  }

  revGet(key: number) {
    return this.reverseMap[key]
  }

  set(key: string, value: number) {
    this.map[key] = value
    this.reverseMap[value] = key
  }

  unset(key: string) {
    const val = this.get(key)
    delete this.reverseMap[val]
    delete this.map[key]
  }
}

// 存储 url 和 urlId（主要为了节省空间）
class UrlStore extends TwoWayMap {
  private counter = 1

  store(url: string) {
    const val = this.get(url)
    if (val) return val
    this.set(url, this.counter++)
    return this.counter - 1
  }
}

class ItemStore {
  // 存储 每个 item 对应的 urls（item 发生变化时，所有 urls 都需要更新）
  private store: Record<string, Set<number>> = {}

  private urlStore = new UrlStore()

  storeItem(id: string, fromPath: string) {
    const urlId = this.urlStore.store(fromPath)
    this.store[id] = this.store[id] ? this.store[id].add(urlId) : new Set([urlId])
  }

  getItemUrls(id: string) {
    const set = this.store[id]
    if (set) {
      return Array.from(set).map((urlId) => this.urlStore.revGet(urlId))
    }
    return []
  }

  popItemUrls(id: string): string[] {
    const ret = this.getItemUrls(id)
    delete this.store[id]
    return ret
  }
}

function createFormData(input: Record<string, unknown>): FormData {
  return Object.keys(input || {}).reduce((formData, key) => {
    const property = input[key]
    formData.append(
      key,
      property instanceof Blob
        ? property
        : typeof property === 'object' && property !== null
        ? JSON.stringify(property)
        : `${property}`
    )
    return formData
  }, new FormData())
}

function createDefaultStore(): ApiStore {
  const cache: Record<string, any> = reactive({
    request: {},
    object: {}
  })
  return {
    get requestCache() {
      return cache.request
    },
    get objectCache() {
      return cache.object
    },
    clearStore() {
      cache.request = {}
      cache.object = {}
    },
    prepare() {}
  }
}

export function createNuxtStore(): ApiStore {
  function getNuxtApiStore(checkContext = true) {
    try {
      return useState('api-store', () => {
        return {
          requestCache: {},
          objectCache: {}
        }
      })
    } catch (e) {
      if (checkContext) {
        throw new Error(
          '未能获取 NuxtApp，请在 Nuxt 环境下使用该函数，或参考：https://nuxt.com/docs/api/composables/use-nuxt-app#runwithcontext'
        )
      }
    }
  }

  return {
    get requestCache() {
      return getNuxtApiStore()?.value.requestCache || {}
    },
    get objectCache() {
      return getNuxtApiStore()?.value.requestCache || {}
    },
    prepare() {
      return getNuxtApiStore()
    },
    clearStore() {
      const store = getNuxtApiStore(false)
      if (store) {
        store.value.requestCache = {}
        store.value.objectCache = {}
      }
    }
  }
}

export class CachedApi {
  public $axios!: AxiosInstance
  public baseUrl: () => string
  public format?: ResponseType = 'json'
  public token: string = ''

  private readonly isNuxt = true

  // 为了能在服务端使用，store 中的数据需要存储到 vueApp 中
  private readonly store!: ApiStore

  private itemStore = new ItemStore()

  private responseHandler!: ApiConfig['responseHandler']
  private readonly errorHandler!: ApiConfig['errorHandler']
  private readonly extractItems!: ApiConfig['extractItems']

  constructor({ baseUrl, responseHandler, errorHandler, extractItems }: ApiConfig) {
    this.$axios = axios.create()

    if (!this.isNuxt) {
      this.store = createDefaultStore()
    } else {
      this.store = createNuxtStore()
    }

    this.baseUrl = baseUrl
    this.responseHandler = responseHandler
    this.errorHandler = errorHandler
    this.extractItems = extractItems
  }

  initStore() {
    this.store.clearStore()
  }

  public get(
    path: string,
    query?: QueryParamsType,
    requestParams?: Omit<FullRequestParams, 'path' | 'method' | 'query'>
  ) {
    return this.request({
      method: 'GET',
      path,
      query,
      ...requestParams
    })
  }

  public post(path: string, body: any, requestParams?: Omit<FullRequestParams, 'path' | 'method' | 'body'>) {
    return this.mutateRequest({ method: 'POST', path, body, ...requestParams })
  }

  public patch(path: string, body: any, requestParams?: Omit<FullRequestParams, 'path' | 'method' | 'body'>) {
    return this.mutateRequest({ method: 'PATCH', path, body, ...requestParams })
  }

  public put(path: string, body: any, requestParams?: Omit<FullRequestParams, 'path' | 'method' | 'body'>) {
    return this.mutateRequest({ method: 'PUT', path, body, ...requestParams })
  }

  public delete(path: string, requestParams?: Omit<FullRequestParams, 'path' | 'method'>) {
    return this.mutateRequest({ method: 'DELETE', path, ...requestParams })
  }

  public async request<T>(requestParams: FullRequestParams): Promise<T> {
    const { path, method, type, format, forceReload, disableCache, query, headers, ...params } = requestParams
    const contentType = type && type !== ContentType.FormData ? { 'Content-Type': type } : undefined

    let app: any = {
      runWithContext: (f: any) => {
        return f()
      }
    }
    if (this.isNuxt) {
      try {
        app = useNuxtApp()
        this.store.prepare()
      } catch (e) {
        throw new Error('Nuxt 上下文丢失，请在异步函数中使用 runWithContext')
      }
    }

    if (method !== 'GET') {
      return this.mutateRequest(requestParams)
    }

    const config: AxiosRequestConfig = {
      params: query,
      headers: {
        ...contentType,
        ...(headers || {})
      },
      ...params,
      responseType: format || this.format
    }

    if (import.meta.server) {
      try {
        const response = await this.$axios.get(this.getPath(path), config)
        return app.runWithContext(() => {
          let data = this.responseHandler(response)
          if (!disableCache) {
            data = this.storeToCache(path, query, data)
          }
          return data
        })
      } catch (e: any) {
        throw this.errorHandler(e, this)
      }
    }

    let cachedData = this.getFromCache(path, query)
    if (cachedData.state === 'ok') {
      // 命中缓存
      if (isPromise(cachedData.data)) {
        // 正在请求中
        return cachedData.data
      } else if (!forceReload) {
        return cachedData.data
      }
    }

    const promise = new Promise((resolve, reject) => {
      let data
      this.$axios
        .get(this.getPath(path), config)
        .then((response) => {
          data = this.responseHandler(response)
          if (!disableCache) {
            data = this.storeToCache(path, query, data)
          }
          resolve(data)
        })
        .catch((e) => {
          reject(this.errorHandler(e, this))
        })
    })
    this.storeToCache(path, query, promise)

    cachedData = this.getFromCache(path, query)
    if (cachedData.state === 'ok') {
      // 命中缓存
      if (isPromise(cachedData.data)) {
        // 正在请求中
        return cachedData.data
      } else if (!forceReload) {
        return cachedData.data
      }
    }
    return cachedData.data
  }

  setToken(token: string) {
    if (!token) {
      this.initStore()
      this.$axios.defaults.headers.common.Authorization = ''
      this.token = ''
      return
    }
    this.$axios.defaults.headers.common.Authorization = 'Bearer ' + token
    this.token = token
  }

  public removeCache(...parts: string[]) {
    this.removeCacheItem(parts.join('/'))
  }

  private storeToCache(path: string, query: any, data: any) {
    const compiledPath = this.compilePath(path, query, true)
    this.store.requestCache[compiledPath] = data

    const items = this.extractItems(data, compiledPath)

    if (items) {
      items.forEach((item) => {
        if (import.meta.client) {
          // 仅在 client 进行 item url 双向缓存
          this.itemStore.storeItem(item.id, compiledPath)
        }
        if (item.data) {
          this.store.objectCache[item.id] = item.data
        }
      })
    }

    return this.store.requestCache[compiledPath]
  }

  private getFromCache(path: string, query: any) {
    const cacheName = this.compilePath(path, query, true)

    if (Object.hasOwnProperty.call(this.store.requestCache, cacheName)) {
      return {
        state: 'ok',
        data: this.store.requestCache[cacheName]
      }
    }
    return { state: 'none' }
  }

  private compilePath(path: string, query?: QueryParamsType, insertQuery = false) {
    if (!query) {
      return path
    }
    const setParams: any = {}
    if (insertQuery) {
      const requestParams = new URLSearchParams({})
      Object.keys(query)
        .filter((param) => !setParams[param])
        .forEach((param) => {
          if (query[param] !== undefined) {
            requestParams.append(param, query[param].toString())
          }
        }, '')
      if (requestParams.toString()) {
        path += '?' + requestParams.toString()
      }
    }
    return path
  }

  private removeCacheItem(
    path: string,
    query?: Record<string, any>,
    headers?: Record<string, string | number | boolean>,
    mode: RemoveCacheMode = 'prefix'
  ) {
    if (import.meta.server) {
      // 服务端都是一次性数据，不需要主动删除
      return
    }
    const cacheName = this.compilePath(path, query)
    delete this.store.requestCache[cacheName]

    // 如果这个 item 还是其它 urls 的请求结果，则全部删除
    const items = this.extractItems(null, cacheName)

    if (items) {
      items.forEach((item) => {
        const urls = this.itemStore.popItemUrls(item.id)
        urls.forEach((url) => {
          delete this.store.requestCache[url]
        })
        delete this.store.objectCache[item.id]
      })
    } else if (mode === 'single') {
      for (const name in this.store.requestCache) {
        if (name === path) {
          delete this.store.requestCache[name]
          break
        }
      }
    } else {
      // 如果不是针对 item 的操作，级联删除
      Object.keys(this.store.requestCache).forEach((name) => {
        if (name.startsWith(path)) {
          delete this.store.requestCache[name]
        }
      })
    }
  }

  private getPath(path: string) {
    if (path.startsWith('http')) {
      return path
    }
    return this.baseUrl() + path
  }

  private mutateRequest<T>(requestParams: FullRequestParams): Promise<T> {
    const { path, method, type, format, removeRelativeCache, query, headers, ...params } = requestParams
    let { body } = requestParams
    const contentType = type && type !== ContentType.FormData ? { 'Content-Type': type } : undefined

    // try to get _etag from cache
    const url = this.compilePath(path, query, true)
    const items = this.extractItems(null, url)
    let etag = ''
    if (items) {
      const id = items[0].id
      const cache = this.store.objectCache[id]
      if (cache && typeof cache === 'object' && cache._etag) {
        etag = cache._etag
      }
    }

    const config: AxiosRequestConfig = {
      params: query,
      headers: {
        ...contentType,
        ...(etag ? { 'If-Match': etag } : {}),
        ...(headers || {})
      },
      ...params,
      responseType: format || this.format
    }

    if (method === 'DELETE') {
      return this.$axios
        .delete(this.getPath(this.compilePath(path, config.params)), config)
        .then((response: any) => {
          if (removeRelativeCache !== 'none') {
            this.removeCacheItem(path, query, headers as Record<string, any>, removeRelativeCache)
          }
          return response && response.data
        })
        .catch((e) => {
          throw this.errorHandler(e, this)
        })
    }

    // POST/PATCH/PUT
    if (type === ContentType.FormData && body && typeof body === 'object') {
      body = createFormData(body as Record<string, unknown>)
    }

    // @ts-expect-error method 已知
    return this.$axios[method.toLowerCase()](this.getPath(this.compilePath(path, params)), body, config)
      .then((response: any) => {
        if (removeRelativeCache !== 'none') {
          this.removeCacheItem(path, query, headers as Record<string, any>, removeRelativeCache)
        }
        return this.responseHandler(response)
      })
      .catch((e: any) => {
        throw this.errorHandler(e, this)
      })
  }
}
