<script setup lang="ts">
import { useEnter } from '~/composables/search'
import { useSearchStore } from '~/stores/search'

import { bannerUrl } from '~/config'

const { enter } = useEnter()
const search = useSearchStore()
const keyword = ref(search.savedKeyword)

const router = useRouter()

const advanceDialogVisible = ref(false)

const handleUploadSuccess = () => {
  router.push("/search?upload=1")
}

const advanceSearch = () => {
  let total_str = form.query + form.year + form.judge_prop + form.court + form.note_name + form.case_reason;
  if (total_str.trim().length == 0){
    return;
  }
  router.push({
    path: '/search',
    query: {
      q: form.query,
      year: form.year,
      judge_prop: form.judge_prop,
      court: form.court,
      note_name: form.note_name,
      case_reason: form.case_reason
    },
  })
  advanceDialogVisible.value = false
}

const form = reactive({
  query: '',
  year: '',
  judge_prop: '',
  court: '',
  note_name: '',
  case_reason: '',
})

const UPLOAD_URL = import.meta.env.VITE_API_URL + "/upload/"

const { t } = useI18n()
</script>

<template>
  <div class="flex flex-col justify-center items-center" h="full">
    <img width="280" height="156" class="w-70 filter drop-shadow" m="-b-4" :src="bannerUrl" alt="Rimo And XiaoYun">

    <InputBox v-model="keyword" m="t-0 b-4" :enter="() => { enter(keyword) }" />

    <div m="b-18" class="flex" style="flex-direction: row;">
      <button class="sese-btn m-3 text-sm btn " bg="gradient-to-r" @click="enter(keyword)">
        {{ t('button.search') }}
      </button>
      <button class="sese-btn m-3 text-sm btn " bg="gradient-to-r" @click="advanceDialogVisible = true">
        {{ t('button.advance_search') }}
      </button>
      <el-upload :action="UPLOAD_URL" :on-success="handleUploadSuccess">
        <button class="sese-btn m-3 text-sm btn " bg="gradient-to-r" style="width: 60px; align-self: center;">
          类案检索
        </button>
        <!-- <el-button size="small" type="danger" class="sese-btn m-3 text-sm btn " bg="gradient-to-r"></el-button> -->
      </el-upload>
    </div>
</div>
  <el-dialog v-model="advanceDialogVisible" title="高级检索" width="30%" class="advance-dialog">
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
    <el-button @click="advanceSearch" style="margin-top: 15px;">
      {{ t("button.advance_search") }}
    </el-button>
    <!-- <el-button type="primary" @click="advanceDialogVisible = false">
            Confirm
          </el-button> -->
  </el-dialog>
  <Footer />
</template>

<route lang="yaml">
meta:
  layout: home
</route>

<style lang="scss">
.advance-dialog {
  // --el-dialog-padding-primary: 10px;
}
</style>
