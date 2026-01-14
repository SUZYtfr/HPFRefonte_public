<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FictionsThumbnailList :is-loading="recentFanfictionsStatus == 'pending'" :list-type="FanfictionListType.Recent" :fanfictions="recentFanfictions" />
        <br />
        <!-- Sélections fanfictions -->
        <FictionsThumbnailList :is-loading="recentFanfictionsStatus == 'pending'" :list-type="FanfictionListType.Selections" :fanfictions="recentFanfictions" />
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
import type { NewsArticleOrder, NewsArticleTypeOffsetPaginated, OffsetPaginationInput, FictionOrder, FictionTypeOffsetPaginated } from "#gql";
import { Ordering } from "#gql/default";
import { FanfictionListType } from "~/types/other";
//#endregion

// Metadata, SEO et droits d'accès à la page
definePageMeta({
  auth: false,
});

const { data: recentFanfictions, status: recentFanfictionsStatus } = await useAsyncGql('getIndexFictions', {}, {
  lazy: true,
  transform: (input: { fictions: FictionTypeOffsetPaginated }) => {
    return {
      ...input.fictions,
      results: plainToInstance(FanfictionModel, input.fictions.results),
    };
  }
});

const { data: paginatedRecentNews, status: newsStatus } = await useAsyncGql('getIndexNews', {}, {
  lazy: true,
  transform: (input: { news: NewsArticleTypeOffsetPaginated }) => {
    return {
      ...input.news,
      results: plainToInstance(NewsModel, input.news.results),
    };
  }
});
//#endregion
</script>

<style scoped></style>
