<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FictionsThumbnailList
          :title="'Nouveautés ' + fandom?.name"
          :fandom
          :is-loading="recentFanfictionsStatus == 'pending'"
          :list-type="FanfictionListType.Recent"
          :fanfictions="recentFanfictions"
        />
        <br />
        <!-- Sélections fanfictions -->
        <FictionsThumbnailList
          :title="'Sélections ' + fandom?.name"
          :fandom
          :is-loading="recentFanfictionsStatus == 'pending'"
          :list-type="FanfictionListType.Selections"
          :fanfictions="recentFanfictions"
        />
        <br />
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList :is-loading="newsStatus === 'pending'" :news="paginatedRecentNews ?? undefined" />
      </div>
    </div>
    <br />
  </div>
</template>

<script setup lang="ts">
//#region Imports
import { plainToInstance } from "class-transformer";
import { FanfictionModel, NewsModel } from "~/models";
import type { NewsArticleTypeOffsetPaginated, FictionTypeOffsetPaginated } from "#gql";
import { FanfictionListType } from "~/types/other";
import type { FandomData } from "~/types/fanfictions";
//#endregion

// Metadata, SEO et droits d'accès à la page
definePageMeta({
  auth: false,
});

const route = useRoute();

const { data: fandom } = await useAsyncGql(
  "getFandomDetails",
  {
    fandomSlug: route.params.fandomSlug as string,
  },
  {
    transform: (input: { fandom: FandomData }) => {
      return input.fandom;
    },
  },
);

if (!fandom.value) {
  navigateTo("/");
}

const { data: recentFanfictions, status: recentFanfictionsStatus } = await useAsyncGql(
  "getFandomFictions",
  {
    filters: {
      fandoms: {
        id: {
          exact: fandom.value?.id,
        },
      },
    },
  },
  {
    lazy: true,
    transform: (input: { fictions: FictionTypeOffsetPaginated }) => {
      return {
        ...input.fictions,
        results: plainToInstance(FanfictionModel, input.fictions.results),
      };
    },
  },
);

const { data: paginatedRecentNews, status: newsStatus } = await useAsyncGql(
  "getFandomNews",
  {},
  {
    lazy: true,
    transform: (input: { newsArticles: NewsArticleTypeOffsetPaginated }) => {
      return {
        ...input.newsArticles,
        results: plainToInstance(NewsModel, input.newsArticles.results),
      };
    },
  },
);

useHead({
  title: "HPF - Fanfictions " + fandom.value?.name,
});
//#endregion
</script>

<style scoped></style>
