import { apiFetch } from "../fetch"

interface DetailParams {
    id: number
}

export async function detail(params: Partial<DetailParams>) {
    const { useToast } = await import('vue-toastification')
    const toast = useToast()

    console.log("in_detail", params.id)

    const detailParams: {
        id: number
      } = {
        id: params.id || 1
      }
    const data = await apiFetch('/detail/', {
      params: detailParams,
    }).catch((e) => {
      console.error(e)
      toast.error('服务器无法获取Case细节！')
    })
    return data
}