import { apiFetch } from './fetch'

interface SearchParams {
  q: string
  page: string
  lid: string // law_id
}

export async function search(params: Partial<SearchParams>) {
  const { useToast } = await import('vue-toastification')
  const toast = useToast()

  const searchParams: {
    q: string
    page : string
    lid: string
  } = {
    q: params.q || '',
    page: params.page || '1',
    lid: params.lid || ''
  }
  const data = await apiFetch('/search', {
    params: searchParams,
  }).catch((e) => {
    console.error(e)
    toast.error('坏了！服务器坏了！快去打莉沫酱！')
  })
  return data
}
