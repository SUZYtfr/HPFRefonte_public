<template>
  <div class="container px-5">
    <br>
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FanfictionThumbnailList :is-loading="recentFanfictionListLoading" :list-type="FanfictionListType.Recent" :fanfictions="recentFanfictions?.results" />
        <br>
        <!-- Sélections fanfictions -->
        <FanfictionThumbnailList :is-loading="selectionFanfictionListLoading" :list-type="FanfictionListType.Selections" :fanfictions="selectionFanfictions?.results" />
        <br>
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList :is-loading="newsListLoading" :news="paginatedRecentNews?.results" />
      </div>
    </div>
    <br>
  </div>
</template>

<script setup lang="ts">
import { searchNews } from "@/api/news";
import { searchFanfictions } from "@/api/fanfictions";
import { IBasicQuery, SortByEnum } from "@/types/basics";
import { IFanfictionFilters } from "@/types/fanfictions";
import FanfictionThumbnailList from "~/components/list/fanfictions/FanfictionThumbnailList.vue";
import NewsThumbnailList from "~/components/list/news/NewsThumbnailList.vue";
import { FanfictionListType } from "~/types/other";

let recentFanfictionFilters : IFanfictionFilters = {
  page: 1,
  pageSize: 20,
  totalPages: false,
  sortOn: "last_update_date",
  sortBy: SortByEnum.Descending,
  searchTerm: null,
  searchAuthor: null,
  searchAuthorId: null,
  multipleAuthors: null,
  status: null,
  wordCount_min: null,
  wordCount_max: null,
  includedTags: [],
  excludedTags: [],
  customTags: [],
  featured: null,
  inclusive: false,
  fromDate: null,
  toDate: null
};

let selectionsFanfictionFilters : IFanfictionFilters = {
  page: 1,
  pageSize: 20,
  totalPages: false,
  sortOn: "last_update_date",
  sortBy: SortByEnum.Descending,
  searchTerm: null,
  searchAuthor: null,
  searchAuthorId: null,
  multipleAuthors: null,
  status: null,
  wordCount_min: null,
  wordCount_max: null,
  includedTags: [],
  excludedTags: [],
  customTags: [],
  featured: true,
  inclusive: false,
  fromDate: null,
  toDate: null
};

let newsFilters : IBasicQuery = {
  page: 1,
  pageSize: 20,
  totalPages: true,
  sortOn: "post_date",
  sortBy: SortByEnum.Descending
};

const { data: paginatedRecentNews, status: newsStatus } = await searchNews(newsFilters);
const newsListLoading = newsStatus.value === "pending";

const { data: recentFanfictions, status: recentFanfictionStatus } = await searchFanfictions(recentFanfictionFilters);
const recentFanfictionListLoading = recentFanfictionStatus.value === "pending";

const { data: selectionFanfictions, status: selectionFanfictionStatus } = await searchFanfictions(selectionsFanfictionFilters);
const selectionFanfictionListLoading = selectionFanfictionStatus.value === "pending";

</script>

<style lang="scss">
@use "~/assets/scss/custom.scss";
.card-content {
  padding: 0px;
}

@media (max-width: var(--desktop-width)) {
  .columns.is-reversed-touch {
    flex-direction: column-reverse;
    display: flex;
  }
}

@media (max-width: var(--tablet-width)) {
  .columns.is-reversed-mobile {
    flex-direction: column-reverse;
    display: flex;
  }
}
</style>
