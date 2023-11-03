<template>
  <div id="main-container" class="container px-5">
    <News_2 v-if="news != null" class="mt-2" :news="news" :active-color="'#f0f0f0'" />
    <br>
    <div>
      <CommentList v-if="news != null" :news_id="news?.news_id" :comments="news?.comments" />
    </div>
    <br>
  </div>
</template>

<script setup lang="ts">
import { getNews } from "~/api/news";
import { NewsModel } from "~/models/news";
import type { UseFetchWrapperResponse } from "~/utils/api";
import News_2 from "~/components/News_2.vue";
import CommentList from "~/components/list/comments/CommentList.vue";

const route = useRoute()
const { data: news }: UseFetchWrapperResponse<NewsModel> = await getNews(Number(route.params.id))
</script>

<style lang="scss" scoped>

</style>
