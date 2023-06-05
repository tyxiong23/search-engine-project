<script setup lang="ts">
import { search } from '~/api'
import type { SearchData } from '~/api/types'
import { useEnter } from '~/composables/search'
import { useSearchStore } from '~/stores/search'
import { reactive } from 'vue'

import { bannerUrl } from '~/config'

import {
  Search,
} from '@element-plus/icons-vue'

const { t } = useI18n()
const { enter } = useEnter()
const route = useRoute()
const router = useRouter()

const searchStore = useSearchStore()
const query = computed(() => route.query.q?.toString() || '')

const law_id = computed(() => route.query.lid?.toString() || '')

const keyword = ref(query.value)
watch(() => query.value, () => {
  searchStore.setNewKeyword(query.value)
  keyword.value = query.value
})

// const slice = ref(route.query.slice?.toString())
const pageNumber = ref(10)

const searchData = ref<SearchData>()
const keywords = computed(() => (searchData.value && searchData.value['split_words']) || [keyword.value])
// const keywords = computed(() => [keyword.value])
useHead({
  title: computed(() => `${query.value} - ${t('sese.title')}`),
})

const searchByParams = async () => {
  searchStore.isLoading = true
  const data = await search({
    q: keyword.value,
    page: String(curPage.value),
    lid: law_id.value,
  })
  searchStore.isLoading = false
  searchData.value = data
}

onBeforeMount(async () => {
  console.log("onBeforeMount")
  searchByParams()
})

onBeforeRouteLeave(
  async () => {
    console.log("onBeforeMountLeave")
    searchStore.isLoading = true
  }
)

const curPage = ref(1)

const goToPage = (page: number) => {
  curPage.value = page
  // slice.value = `${(curPage.value - 1) * pageNumber.value}:${curPage.value * pageNumber.value}`

  router.push({
    path: '/search',
    query: {
      q: keyword.value,
      page: curPage.value,
    },
  })
  searchByParams()
}

watch(() => searchStore.savedKeyword, () => {
  searchByParams()
})

/**
 * 显示的页数
 */
const displayedPages = computed(() => {
  if (searchData.value && searchData.value['total_objects']) {
    const pages = Math.ceil(searchData.value['total_objects'] / pageNumber.value)
    return pages <= 10 ? pages : 10
  }
  else { return 0 }
})

const searchKeyword = () => {
  // reset
  curPage.value = 1
  // slice.value = `0:${pageNumber.value}`
  enter(keyword.value)
}


// 高亮文本
// do not use same name with ref
const form = reactive({
  year: null,
  judge_prop: '',
  court: '',
  note_name: '',
  case_reason: false,
  type: [],
  resource: '',
  desc: '',
})

const onSubmit = () => {
  console.log('submit!')
}

const pushLabel = (msg: string) => {
  keyword.value = msg
  searchByParams()
}

</script>

<template>
  <div p="2" h="screen">
    <Transition>
      <Loading v-if="searchStore.isLoading" />
    </Transition>

    <div p="l-2 lt-sm:l-0" class="relative flex justify-start items-center lt-sm:mt-6">
      <a class="cursor-pointer inline-flex justify-center lt-sm:absolute -top-5 left-5" m="r-3 b-1"
        @click="() => { router.push('/') }">
        <img class="w-16 filter drop-shadow" :src="bannerUrl" alt="Rimo And XiaoYun">
      </a>
      <InputBox v-model="keyword" class="inline-flex" :enter="() => { searchKeyword() }" />
      <el-button type="" :icon="Search" @click="searchKeyword()" circle style="margin: 10px" />
      <!-- <button
                    m="l-2" p="2" class="search-btn icon-btn flex justify-center items-center border rounded rounded-full !outline-none"
                    hover="border-red"
                    @click="searchKeyword()"
                  >
                    <div class="line" i-ri-heart-line/>
                    <div class="fill" i-ri-heart-fill text="red" />
                  </button> -->
    </div>
    <div style="display: flex; float: left; " w="screen">
      <div>
        <div v-if="searchData" m="l-24 lt-sm:l-0" p="2" class="max-w-2xl">
          <div text="left sm gray-500" m="b-2">
            找到 {{ searchData['total_objects'] }} 个结果，共花费{{ searchData.time }} 秒。
          </div>
          <template v-if="searchData['total_objects']">
            <ResultItem v-for="(item, i) in searchData['results']" :key="i" :keywords="keywords" se :result="item" @child-to-parent="pushLabel"/>
          </template>

          <div v-else text="left" m="t-8">
            找不到和您查询的「<strong text="red-500">{{ keyword }}</strong>」相符的内容或信息！

            <p class="cursor-pointer hover:underline" text="sm" m="t-4" @click="router.go(-1)">
              返回上一页
            </p>

            <p m="t-8" text="left">
              建议：
            <ul p="4">
              <li class="list-circle">
                <a class="hover:underline" :href="`https://www.google.com/search?q=${keyword}`" target="_blank"
                  :title="keyword">
                  使用 Google 搜索
                </a>
              </li>
            </ul>
            <img src="/rimo-touch-fish.png" alt="摸鱼">
            </p>
          </div>

          <div v-if="displayedPages" m="t-6 b-4" class="pagination-container flex justify-center items-center">
            <span v-if="curPage > 1" class="page-link" text="sm" p="r-1" m="r-1" @click="goToPage(curPage - 1)">
              <div i-ri-arrow-left-line />
            </span>
            <span v-for="i in displayedPages" :key="i" p="1" m="1" class="pagination-page"
              :class="curPage === i ? 'text-black dark:text-white' : 'text-blue-600 dark:text-blue-500 cursor-pointer hover:underline'"
              text="sm" @click="curPage === i ? null : goToPage(i)">
              {{ i }}
            </span>
            <span v-if="curPage < displayedPages" class="page-link" text="sm" p="l-1" m="l-1"
              @click="goToPage(curPage + 1)">
              <div i-ri-arrow-right-line />
            </span>
          </div>
        </div>
        <div v-else-if="!searchStore.isLoading" m="t-10">
          服务器出现问题！！
        </div>
      </div>
      <div style="width:500px; margin-left: 50px;">
        <div style="height:screen; background-color: burlywood;">
        </div>
        <div style="background-color: #eeeeee; padding: 20px;">
          <el-container>
            <el-header>
              高级检索
            </el-header>
            <el-form :model="form" label-width="120px">
              <el-form-item label="年份">
                <el-input v-model="form.name" />
              </el-form-item>
              <el-form-item label="Activity name">
                <el-input v-model="form.name" />
              </el-form-item>
              <el-form-item label="Activity name">
                <el-input v-model="form.name" />
              </el-form-item>
              <el-form-item label="Activity name">
                <el-input v-model="form.name" />
              </el-form-item>
              <el-form-item label="Activity name">
                <el-input v-model="form.name" />
              </el-form-item>
              

                <button
                  class="sese-btn m-3 text-sm btn "
                  bg="gradient-to-r"
                  @click="enter(keyword)"
                >
                  {{ t('button.search') }}
                </button>
                <!-- <el-button type="" @click="onSubmit">Create</el-button>
                <el-button>Cancel</el-button> -->
              <!-- </el-main> -->
            </el-form>
          </el-container>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.search-btn {
  .line {
    display: block;
  }

  .fill {
    display: none;
  }

  &:hover {
    .line {
      display: none;
    }

    .fill {
      display: block;
    }
  }
}
</style>
