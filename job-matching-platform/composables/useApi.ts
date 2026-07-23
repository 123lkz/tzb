import { ref, type Ref } from 'vue'
export function useApiData<T>(fetcher: () => Promise<T>) {
  const data = ref(null) as Ref<T | null>
  const pending = ref(true)
  const error = ref<string | null>(null)
  const reload = ref<() => void>(() => {})
  const load = async () => {
    pending.value = true; error.value = null
    try { data.value = await fetcher() }
    catch (e: any) { error.value = e?.message || '请求失败' }
    finally { pending.value = false }
  }
  reload.value = load
  load()
  return { data, pending, error, reload }
}
