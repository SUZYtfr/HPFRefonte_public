<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <!-- <FanfictionThumbnailList :is-loading="listLoading" :list-type="FanfictionListType.Recent" :fanfictions="recentFanfictions" /> -->
        <br />
        <!-- Sélections fanfictions -->
        <!-- <FanfictionThumbnailList :is-loading="listLoading" :list-type="FanfictionListType.Selections" :fanfictions="selectionsFanfictions" /> -->
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
import NewsThumbnailList from "@/components/list/news/NewsThumbnailList.vue";
import { plainToInstance } from "class-transformer";
import { NewsModel } from "~/models";
import type { NewsArticleOrder, NewsArticleTypeOffsetPaginated, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
//#endregion

// Metadata, SEO et droits d'accès à la page
definePageMeta({
  auth: false,
});

const newsPagination: OffsetPaginationInput = {
  limit: 20,
  offset: 0,
};
const newsOrder: NewsArticleOrder = {
  postDate: Ordering.DESC
};

const { data: paginatedRecentNews, status: newsStatus } = await useAsyncGql('getNews', {
  pagination: newsPagination,
  order: newsOrder,
}, {
  lazy: true,
  transform: (data: { news: NewsArticleTypeOffsetPaginated }) => {
    return {
      ...data.news,
      results: plainToInstance(NewsModel, data.news.results),
    };
  }
});
//#endregion
</script>

<style scoped></style>
