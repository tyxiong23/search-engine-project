<script setup lang="ts">
import { useEnter } from '~/composables/search'
import { useDetailStore} from '~/stores/detail'

import { detail } from "~/api/detail"

import { useRouter} from "vue-router"

import {
  Search,
} from '@element-plus/icons-vue'

import { bannerUrl } from '~/config'
import { CaseDetail } from '~/api/types/detail'

const { enter } = useEnter()
const detailStore = useDetailStore()


const router = useRouter()
const route = useRoute()
const BackToSearch = () => {
  router.back()
}


const case_query = computed(() => parseInt(route.query.id?.toString() || '-1'))
const case_id = ref(case_query.value)
watch(() => case_query.value, () => {
  console.log("case", case_id.value, "query", case_query.value)
  case_id.value = case_query.value
  console.log("update casd_id", case_id.value)
  if (case_id.value > 0) {
    getDetail()
  }
  
  
})

// console.log("case_id" ,case_id)
const detailData = ref<CaseDetail>()

const getDetail = async () => {
  detailStore.isLoading = true
  detailStore.isLoading = true
  console.log("getDetail", case_id.value)
  const data = await detail({
    id: case_id.value
  }) 
  detailData.value = data.data
  console.log(detailData.value?.head, case_id.value, detailData.value?.id, detailData.value?.head)
  detailStore.isLoading = false
}

onBeforeMount(async () => {
  getDetail()
})

const searchFromLaw = (law_id: string) => {
  router.push(`/search?lid=${law_id}`)
}

// onBeforeRouteUpdate(async () => {
  
  
// })


const { t } = useI18n()
</script>

<template>

  <div p="2" h="screen">
    <Transition>
      <Loading v-if="detailStore.isLoading" />
    </Transition>

    <div p="l-2 lt-sm:l-0" class="relative flex justify-start items-center lt-sm:mt-6" style="float:center; margin: 4px; margin-left: 20px">
      <a class="cursor-pointer inline-flex justify-center lt-sm:absolute -top-5 left-5" m="r-3 b-1" @click="() => { router.push('/') }" style="margin-left: ;">
        <img class="w-16 filter drop-shadow" :src="bannerUrl" alt="Rimo And XiaoYun" style="margin:0px">
      </a>
      <button
          class="sese-btn m-3 text-sm btn "
          bg="gradient-to-r"
          @click="BackToSearch()"
          style="float: left; margin-left: 60px;"
        >
        {{ t('button.back') }}
        </button>
    </div>
    
    <div class="flex flex-col" h="full" style="flex-direction: row;">
      
      <div m="l-6 r-8 t-3" style="width:60%">
        
      
      <div v-if="detailData" style="text-align: left; background-color: #dddddd; padding: 5px;">
        <div style="text-align:center">
        <h2 style="font-size:larger">{{ detailData.head }}</h2>
        </div>
        <div class="flex flex-row" style=" justify-content: center; align-content: center;">
          <div style="width:50%; background-color: #EEDDFF; float:center; margin: 10px;">
            <p> <b>年份：</b>{{ detailData.year }}</p>
            <p> <b>经办法院：</b>{{ detailData.court }}</p>
            <p> <b>审判程序：</b>{{ detailData.judge_prop }}</p>
            <p> <b>文书名称：</b>{{ detailData.note_name }}</p>
            <p> <b>案由：</b>{{ detailData.case_reason }}</p>
          </div>
         
        </div>
        <p class="case-content"> <b>当事人：</b>{{ detailData.related_people }}</p>
        <p class="case-content"> <b>诉讼记录：</b>{{ detailData.judicial_record}}</p>
        <p class="case-content"> <b>案件基本情况：</b>{{ detailData.basic_info }}</p>
        <p class="case-content"> <b>判决分析过程：</b>{{ detailData.judgement_process }}</p>
        <p class="case-content"> <b>判决结果：</b>{{ detailData.result}}</p>
        <p style="text-align: center;"> {{ detailData.tail }}</p>
      </div>

        
      </div>
      <div style="width: 40%; height: 85%;" overflow-y="auto">
      <div v-if="detailData" style="margin-top: 10px;">
        <p style="margin: 8px; font-size: large;">相关法律条文</p>
          <template v-for="(item_law) in detailData.laws" sm>
            <el-tag
              :type="''"
              effect="dark" round
              style="margin:5px" @click="searchFromLaw(item_law.id.toString())">
              {{ item_law.name }}
            </el-tag>
          </template>
      </div>
      <div style="margin-top: 25px;">
          <p style="margin: 8px; font-size: large;">案例推荐</p>
          <template v-if="detailData">
            <ResultItem v-for="(item, i) in detailData.related_cases" :key="i" :keywords="[]" se :result="item"/>
          </template>
        </div>
      </div>
      <!-- <img width="280" height="156" class="w-70 filter drop-shadow" m="-b-4" :src="bannerUrl" alt="Rimo And XiaoYun">

      <InputBox v-model="keyword" m="t-0 b-4" :enter="() => { enter(keyword) }" />

      <div m="b-18">
        <button
          class="sese-btn m-3 text-sm btn "
          bg="gradient-to-r"
          @click="enter(keyword)"
        >
          {{ t('button.search') }}
        </button> -->
        
      <!-- </div> -->
    </div>
    <!-- <Footer/> -->
  </div>
</template>

<route lang="yaml">
meta:
  layout: default
</route>

<style lang="scss">
.case-content {
  margin: 6px;
}
</style>
