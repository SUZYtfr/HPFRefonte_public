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
import { SortByEnum, type IBasicQuery } from "~/types/basics";
import { searchNews } from "@/api/news";
import NewsThumbnailList from "@/components/list/news/NewsThumbnailList.vue";
//#endregion

//#region Datas
const newsFilters: IBasicQuery = {
  page: 1,
  pageSize: 20,
  totalPages: true,
  sortOn: "post_date",
  sortBy: SortByEnum.Descending,
};

const { data: paginatedRecentNews, status: newsStatus } = await searchNews(newsFilters, {
  lazy: true,
});
//#endregion
</script>

<style scoped></style>
