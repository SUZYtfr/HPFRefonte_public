<template>
  <div class="container px-5">
    <br>
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FanfictionThumbnailList :is-loading="recentFanfictionsLoading" :list-type="FanfictionListType.Recent" :fanfictions="recentFanfictions" />
        <br>
        <!-- Sélections fanfictions -->
        <FanfictionThumbnailList :is-loading="selectionsFanfictionsLoading" :list-type="FanfictionListType.Selections" :fanfictions="selectionsFanfictions" />
        <br>
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList :is-loading="newsLoading" :news="recentNews" />
      </div>
    </div>
    <br>
  </div>
</template>

<script setup lang="ts">
import { searchNews } from "@/api/news";
import { NewsModel } from "@/models/news";
import { searchFanfictions } from "@/api/fanfictions";
import { FanfictionModel } from "@/models/fanfictions";
import { IBasicQuery, SortByEnum } from "@/types/basics";
import { IFanfictionFilters } from "@/types/fanfictions";
import FanfictionThumbnailList from "~/components/list/fanfictions/FanfictionThumbnailList.vue";
import NewsThumbnailList from "~/components/list/news/NewsThumbnailList.vue";
import { FanfictionListType } from "~/types/other";
import type { UseFetchWrapperResponse } from "~/utils/api"

const recentFanfictionFilters: IFanfictionFilters = {
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

const selectionsFanfictionFilters : IFanfictionFilters = {
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

const newsFilters : IBasicQuery = {
  page: 1,
  pageSize: 20,
  totalPages: true,
  sortOn: "post_date",
  sortBy: SortByEnum.Descending
};

// TODO - rétablir la snackbar d'erreur (useFetch fournit error)
const { data: recentNews, pending: newsLoading } : UseFetchWrapperResponse<NewsModel[]> = await searchNews(newsFilters)
const { data: recentFanfictions, pending: recentFanfictionsLoading} : UseFetchWrapperResponse<FanfictionModel[]> = await searchFanfictions(recentFanfictionFilters)
const { data: selectionsFanfictions, pending: selectionsFanfictionsLoading} : UseFetchWrapperResponse<FanfictionModel[]> = await searchFanfictions(selectionsFanfictionFilters)

</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";

.card-content {
  padding: 0px;
}

@media (max-width: $desktop) {
  .columns.is-reversed-touch {
    flex-direction: column-reverse;
    display: flex;
  }
}

@media (max-width: $tablet) {
  .columns.is-reversed-mobile {
    flex-direction: column-reverse;
    display: flex;
  }
}
</style>
