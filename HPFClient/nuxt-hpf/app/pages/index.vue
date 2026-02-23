<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FictionsThumbnailList
          title="Nouveautés tous fandoms"
          :is-loading="recentFanfictionsStatus == 'pending'"
          :list-type="FanfictionListType.Recent"
          :fanfictions="recentFanfictions"
        />
        <br />
        <!-- Sélections fanfictions -->
        <FictionsThumbnailList
          title="Sélections tous fandoms"
          :is-loading="recentFanfictionsStatus == 'pending'"
          :list-type="FanfictionListType.Selections"
          :fanfictions="recentFanfictions"
        />
        <br />
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList
          v-if="paginatedRecentNews"
          :is-loading="newsStatus === 'pending'"
          :news="paginatedRecentNews"
        />
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
//#endregion

// Metadata, SEO et droits d'accès à la page
definePageMeta({
  auth: false,
});

const { data: recentFanfictions, status: recentFanfictionsStatus } = await useAsyncGql(
  "getIndexFictions",
  {},
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
  "getIndexNews",
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
  title: "HPF - Hameau Pour Fanfiction",
});
</script>

<style scoped></style>
