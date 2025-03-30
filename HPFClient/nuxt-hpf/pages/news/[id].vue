<template>
  <div id="main-container" class="container px-5">
    <News v-if="news != null" class="mt-2 is-color-odd" :news="news" />
    <br />
    <div>
      <!-- <CommentList v-if="news != null" :news_id="news?.id" :comments="news?.comments" /> -->
    </div>
    <br />
  </div>
</template>

<script setup lang="ts">
//#region Imports
import { getNews } from "~/api/news";
import News from "~/components/entities/news/News.vue";
//#endregion

//#region Usings
const route = useRoute();
//#endregion

//#region Datas
const { data: news } = await getNews(parseInt(route.params.id as string));
//#endregion
</script>

<style lang="scss" scoped></style>
