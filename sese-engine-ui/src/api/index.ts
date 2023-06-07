import { apiFetch } from './fetch'

interface SearchParams {
  q: string
  page: string
  lid: string // law_id
  year: string
  note_name: string
  judge_prop: string
  case_reason: string
  court: string
  upload: string
}

export async function search(params: Partial<SearchParams>) {
  const { useToast } = await import('vue-toastification')
  const toast = useToast()

  const searchParams: {
    q: string
    page : string
    lid: string
    year: string
    note_name: string
    judge_prop: string
    case_reason: string
    court: string
    upload: string
  } = {
    q: params.q || '',
    page: params.page || '1',
    lid: params.lid || '',
    year: params.year || '',
    note_name: params.note_name || '',
    judge_prop: params.judge_prop || '',
    case_reason: params.case_reason || '',
    court: params.court || '',  
    upload: params.upload || '',  
  }
  const data = await apiFetch('/search', {
    params: searchParams,
  }).catch((e) => {
    console.error(e)
    toast.error('服务器出现故障！！/search/')
  })
  return data
}
