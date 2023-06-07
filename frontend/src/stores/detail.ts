import { acceptHMRUpdate, defineStore } from 'pinia'

export const useDetailStore = defineStore('search', () => {

  const [isLoading, toggleLoading] = useToggle(false)

  return {
    isLoading,
    toggleLoading,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDetailStore, import.meta.hot))
