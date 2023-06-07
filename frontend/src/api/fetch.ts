import { $fetch } from 'ohmyfetch'

export const apiFetch = $fetch.create({
  baseURL: import.meta.env.VITE_API_URL,
  retry: 0,
  async onResponse({ response }) {
    const { useToast } = await import('vue-toastification')
    const toast = useToast()
    if (typeof response._data === 'string')
      toast.error('服务器出现了bug，请稍后重试')
  },
  async onResponseError({ response }) {
    const { useToast } = await import('vue-toastification')
    const toast = useToast()
    toast.error(`${response.status} ${response.statusText}`)
    if (response._data)
      toast.error(response._data['信息'])
  },
})
