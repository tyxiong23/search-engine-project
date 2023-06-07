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
const case_reason = computed(() => route.query.case_reason?.toString() || '')
const court = computed(() => route.query.court?.toString() || '')
const note_name = computed(() => route.query.note_name?.toString() || '')
const judge_prop = computed(() => route.query.judge_prop?.toString() || '')
const year = computed(() => route.query.year?.toString() || '')
const upload = computed(() => route.query.upload?.toString() || '')

const keyword = ref(query.value)
const ref_law_id = ref(law_id.value)
const ref_case_reason = ref(case_reason.value)
const ref_court = ref(court.value)
const ref_note_name = ref(note_name.value)
const ref_judge_prop = ref(judge_prop.value)
const ref_year = ref(year.value)
const ref_upload = ref(upload.value)

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
    lid: ref_law_id.value,
    case_reason: ref_case_reason.value,
    judge_prop: ref_judge_prop.value,
    court: court.value,
    note_name: ref_note_name.value,
    year: ref_year.value,
    upload: ref_upload.value
  })
  searchStore.isLoading = false
  searchData.value = data
}

onBeforeMount(async () => {
  console.log("onBeforeMount")
  searchByParams()
})

onBeforeRouteUpdate(
  async () => {
    console.log("onBeforeRouteUpdate")
    searchByParams()
  }
)

// onBeforeRouteLeave(
//   async () => {
//     console.log("onBeforeMountLeave")
//     searchStore.isLoading = true
//   }
// )

const curPage = ref(1)

const goToPage = (page: number) => {
  curPage.value = page
  // slice.value = `${(curPage.value - 1) * pageNumber.value}:${curPage.value * pageNumber.value}`

  router.push({
    path: '/search',
    query: {
      q: keyword.value,
      page: curPage.value,
      lid: ref_law_id.value,
      case_reason: ref_case_reason.value,
      judge_prop: ref_judge_prop.value,
      court: ref_court.value,
      note_name: ref_note_name.value,
      year: ref_year.value
    },
  })
  searchByParams()
}

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
  ref_case_reason.value = ""
  ref_note_name.value = ""
  ref_year.value = ''
  ref_judge_prop.value = ""
  ref_law_id.value = ''
  ref_upload.value = ''
  curPage.value = 1
  // slice.value = `0:${pageNumber.value}`
  enter(keyword.value)
}


// 高亮文本
// do not use same name with ref
const form = reactive({
  query: '',
  year: '',
  judge_prop: '',
  court: '',
  note_name: '',
  case_reason: '',
})

const resetSearchField = () => {
  keyword.value = ""
  ref_case_reason.value = ""
  ref_note_name.value = ""
  ref_year.value = ''
  ref_judge_prop.value = ""
  ref_court.value = ''
  ref_law_id.value = ''
  ref_upload.value = ''
}

const AdvanceSearch = () => {
  resetSearchField()
  keyword.value = form.query.trim()
  ref_case_reason.value = form.case_reason.trim()
  ref_note_name.value = form.note_name.trim()
  ref_judge_prop.value = form.judge_prop.trim()
  ref_court.value = form.court.trim()
  ref_year.value = form.year.trim()

  form.query = ''
  form.case_reason = ''
  form.court = ''
  form.judge_prop = ''
  form.note_name = ''
  form.year = ''

  router.push({
    path: '/search',
    query: {
      q: keyword.value,
      page: curPage.value,
      case_reason: ref_case_reason.value,
      judge_prop: ref_judge_prop.value,
      court: ref_court.value,
      note_name: ref_note_name.value,
      year: ref_year.value
    },
  })
  // searchByParams()
}

const handleUploadSuccess = () => {
  console.log("upload success!!!")
  resetSearchField()
  ref_upload.value = "1"
  router.push({
    path: '/search',
    query: {
      upload: ref_upload.value
    },
  })
  searchByParams()
}

const searchLabel = (msg: string, cls: number) => {
  resetSearchField()
  if (cls == 1) {
    ref_year.value = msg
  } else if (cls == 2) {
    ref_note_name.value = msg
  } else if (cls == 3) {
    ref_judge_prop.value = msg
  } else if (cls == 4) {
    ref_case_reason.value = msg
  }
  router.push({
    path: '/search',
    query: {
      q: keyword.value,
      page: curPage.value,
      lid: ref_law_id.value,
      case_reason: ref_case_reason.value,
      judge_prop: ref_judge_prop.value,
      court: ref_court.value,
      note_name: ref_note_name.value,
      year: ref_year.value
    },
  })
  searchByParams()
}

const UPLOAD_URL = import.meta.env.VITE_API_URL + "/upload/"

</script>

<template>
  <div p="2" h="screen">
    <Transition>
      <Loading v-if="searchStore.isLoading" />
    </Transition>

    <div p="l-2 lt-sm:l-0" class="relative flex justify-start items-center lt-sm:mt-6" >
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
      <div style="">
        <div v-if="searchData" m="l-24 lt-sm:l-0" p="2" class="max-w-2xl">
          <div text="left sm gray-500" m="b-2">
            找到 {{ searchData['total_objects'] }} 个结果，共花费{{ searchData.time }} 秒。
          </div>
          <template v-if="searchData['total_objects']">
            <ResultItem v-for="(item, i) in searchData['results']" :key="i" :keywords="keywords" se :result="item"
              @item-to-search="searchLabel" />
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
      <div style="width: 30%; margin: 50px; margin-top: 10px;">
        <div style="">
          <el-container style="background-color: #eeeeee;  padding: 20px; border-radius: 10px;">
            <el-header style="font-size: larger; font-weight: bolder; height: 45px">
              高级检索
            </el-header>
            <el-form :model="form" label-width="120px" label-position="left" style="font-weight: bolder;">
              <el-form-item label="关键词" style="height: 28px;">
                <el-input v-model="form.query" />
              </el-form-item>
              <el-form-item label="年份" style="height: 28px;">
                <el-input v-model="form.year" style="height: 28px;" />
              </el-form-item>
              <el-form-item label="经办法院" style="height: 28px;">
                <el-input v-model="form.court" />
              </el-form-item>
              <el-form-item label="审判程序" style="height: 28px;">
                <el-input v-model="form.judge_prop" />
              </el-form-item>
              <el-form-item label="案由" style="height: 28px;">
                <el-input v-model="form.case_reason" />
              </el-form-item>
              <el-form-item label="文书名称" style="height: 28px;">
                <el-input v-model="form.note_name" />
              </el-form-item>
              <!-- <el-button type="" @click="onSubmit">Create</el-button>
                  <el-button>Cancel</el-button> -->
              <!-- </el-main> -->
            </el-form>
            <button class="sese-btn m-3 text-sm btn " bg="gradient-to-r" @click="AdvanceSearch"
              style="width: 60px; align-self: center; margin: 3px;">
              {{ t('button.advance_search') }}
            </button>
          </el-container>

          <el-container style="background-color: #eeeeee;  padding: 20px; border-radius: 10px; margin-top: 30px; padding-bottom: 10px;">
            <el-header style="font-size: larger; font-weight: bolder; height: 35px ">
              类案检索
            </el-header>
            <!-- <el-upload :action="UPLOAD_URL" :on-success="handleUploadSuccess">
            <button class="sese-btn m-3 text-sm btn " bg="gradient-to-r" style="width: 60px; align-self: center;">
                类案检索
              </button>
              <el-button size="small" type="danger" class="sese-btn m-3 text-sm btn " bg="gradient-to-r"></el-button>
            </el-upload> -->
            <el-upload
              class="upload-demo"
              drag
              :action="UPLOAD_URL"
              :on-success="handleUploadSuccess"
              multiple
            >
              <el-icon class="el-icon--upload" style="background-color;:burlywood"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖拽文件至此或<em>点击进行上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip" style="font-size: 12px;">
                  支持txt和xml文件的解析
                </div>
              </template>
            </el-upload>
          </el-container>


          <div>

          </div>
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
