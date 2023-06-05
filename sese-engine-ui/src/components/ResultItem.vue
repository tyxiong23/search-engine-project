<script lang="ts" setup>
// import { routerKey } from 'vue-router';
import type { SearchResult } from '~/api/types'
import { useRouter } from 'vue-router';
import { emit } from 'process';


const props = defineProps<{
  keywords: string[]
  result: SearchResult
}>()

// const route = useRoute()
// const query = computed(() => {
//   const q = route.query.q?.toString()
//   if (q?.startsWith('site:'))
//     return q.split(' ').slice(1).join(' ')
//   else
//     return q
// })

/**
 * 高亮文本
 */
const highlightedText = (content: string, keywords: string[]) => {
  // to solve xss
  let result = content.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  keywords.forEach((item) => {
    const re = new RegExp(item, 'gi')
    result = result.replace(re, (val: string) => {
      return `<em class="highlight">${val}</em>`
    })
  })
  return result
}

const router = useRouter()
const emit = defineEmits(['childToParent', 'parentToChild'])
const goToDetail = (case_id: number) => {
  router.push({
    path: "/detail",
    query: {
      id: case_id
    }
  })
  emit("parentToChild", case_id)
}

const clickLabel = (str: string) => {
  emit('childToParent', str)
}






</script>

<template>
  <div class="result-item relative overflow-visible" flex="~ col" text="left" m="b-4">
    <!-- <span class="flex justify-between items-center">
    </span> -->
    <template v-if="result['title']">
      <!-- <h3 class="top-0 truncate" @click="push(result.id)" v-html="highlightedText(result.title, keywords)" color="#0000C6"/> -->
      <h3 class="top-0 truncate hover:underline"  v-html="highlightedText(result.title, keywords)" @click="goToDetail(result.id)" color="#0000C6"/>
      <p text="sm" v-html="highlightedText(result.content, keywords)"/>
    </template>
    
    
    <!-- <template v-if="result['信息']">
      <a
        :href="result['网址']" target="_blank"
        class="text-lg text-blue-900 hover:underline dark:text-blue-500"
      >
      <p
        text="sm"
        v-html="highlightedText(addString(result.fullText.substring(result.title.length, result.title.length + 97)), keywords)"
      />
        <h3 class="top-0 truncate">
          {{ result['信息']['标题'] }}
        </h3>
      </a> -->
      <!-- <p text="sm" v-html="highlightedText(result['content'], keywords)" />
    </template> -->
    <div v-else>
      <div class="inline-flex justify-start items-center border" p="1" m="1">
        <div i-ri-alert-line />
        <span m="l-1">我们的探测器对这个奇怪的网站没有效果！</span>
      </div>
    </div>

    <div class="tag-group">
      
      <el-tag
        :key='result.year'
        type='success'
        effect="dark" round
        style="margin:5px"
        @click="clickLabel(result.year.toString())">
        {{ result.year }}
      </el-tag>
      <el-tag
        :key='result.case_reason'
        :type="''"
        effect="dark" round
        style="margin:5px"
        @click="clickLabel(result.case_reason)">
        {{ result.case_reason }}
      </el-tag>
      <el-tag
        :key='result.judge_prop'
        :type="'warning'"
        effect="dark" round
        style="margin:5px"
        @click="clickLabel(result.judge_prop)">
        {{ result.judge_prop }}
      </el-tag>
      <el-tag
        :key='result.note_name'
        :type="'danger'"
        effect="dark" round
        style="margin:5px"
        @click="clickLabel(result.note_name)">
        {{ result.note_name }}
      </el-tag>
    </div>
    <!-- <div class="tag-group">
      <span class="tag-group__title">Plain</span>
      <el-tag
        v-for="item in items"
        :key="item.label"
        :type="item.type"
        effect="plain">
        {{ item.label }}
      </el-tag> -->
    <!-- </div> -->

    <!-- <Transition>
      <div
        class="reason-container absolute top-0 left-180 min-h-full justify-center hidden transition"
        w="64"
        opacity="0"
        flex="~ col"
      >
        <blockquote class="search-reason" p="l-2" text="xs">
          <span v-for="value, key in result['原因']" :key="key" class="block">
            {{ key }}：{{ value.toFixed(3) }}
          </span>
        </blockquote>
      </div>
    </Transition> -->
  </div>
</template>

<style lang="scss">
.result-item {
  .related-info {
    opacity: 0;
  }

  &:hover {
    .related-info {
      opacity: 1;
    }
    .reason-container {
      opacity: 1;
    }
  }
}

.search-reason {
  color: var(--se-c-text-light);
  border-left: 4px solid var(--se-c-text-light);
}
</style>
