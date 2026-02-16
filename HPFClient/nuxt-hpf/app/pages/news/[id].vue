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
import type { NewsArticleTypeOffsetPaginated } from "#gql";
import { plainToInstance } from "class-transformer";
import { NewsModel } from "~/models";
//#endregion

definePageMeta({
  auth: false,
});

//#region Usings
const route = useRoute();
//#endregion

//#region Datas
// On peut aussi faire une route dédiée pour chercher un élément sur le serveur
// TODO - regarder s'il existe une directive / override pour utiliser getNews (liste) pour un seul élément
// TODO - erreur si l'élément n'est pas récupéré
const { data: news } = await useAsyncGql(
  "getNewsDetails",
  {
    filters: {
      id: {
        exact: route.params.id as string,
      },
    },
  },
  {
    transform: (data: { news: NewsArticleTypeOffsetPaginated }) => {
      return plainToInstance(NewsModel, data.news.results[0]);
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
