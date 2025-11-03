<template>
  <div id="main-container" class="container px-5">
    <NewsEntity v-if="news[0]" class="mt-2 is-color-odd" :news="news[0]" />
    <br />
    <div>
      <CommentsList v-if="news[0]" :newsId="news[0]?.newsId" :comments="news[0]?.comments" />
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
  auth: false
})

//#region Usings
const route = useRoute();
//#endregion

//#region Datas
// On peut aussi faire une route dédiée pour chercher un élément sur le serveur
// TODO - regarder s'il existe une directive / override pour utiliser getNews (liste) pour un seul élément
// TODO - erreur si l'élément n'est pas récupéré
const { data: news } = await useAsyncGql('getNews', {
  pagination: { limit: 1 },
  filters: {
    id: {
      'exact': route.params.id as string
    }
  },
  withComments: true,
},
{
    transform: (data: { news: NewsArticleTypeOffsetPaginated }) => {
      return plainToInstance(NewsModel, data.news.results)
    }
});

//#endregion
</script>

<style lang="scss" scoped></style>
