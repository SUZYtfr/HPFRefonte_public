<template>
  <div id="main-container" class="container px-5">
    <NewsEntity v-if="news" class="mt-2 is-color-odd" :news="news" />
    <br />
    <div>
      <CommentsList v-if="news" :news-id="news.newsId" :comments="news.comments" />
    </div>
    <br />
  </div>
</template>

<script setup lang="ts">
//#region Imports
import type { NewsArticleType } from "#gql";
import { plainToInstance } from "class-transformer";
import { NewsModel } from "~/models";
//#endregion

definePageMeta({
  auth: false,
});

//#region Usings
const route = useRoute();
//#endregion

// TODO - erreur si l'élément n'est pas récupéré
const { data: news } = await useAsyncGql(
  "getNewsDetails",
  {
    newsId: route.params.id as string,
  },
  {
    transform: (input: { newsArticle: NewsArticleType }) => {
      return plainToInstance(NewsModel, input.newsArticle);
    },
  },
);

if (!news.value) {
  navigateTo("/");
}

useHead({
  title: "HPF - " + news.value.title,
});

//#endregion
</script>

<style lang="scss" scoped></style>
