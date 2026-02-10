<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FictionsThumbnailList
            :title="'Nouveautés ' + fandomData.fandoms[0]?.name"
            :is-loading="recentFanfictionsStatus == 'pending'"
            :list-type="FanfictionListType.Recent"
            :fanfictions="recentFanfictions"
        />
        <br />
        <!-- Sélections fanfictions -->
        <FictionsThumbnailList
            :title="'Sélections ' + fandomData.fandoms[0]?.name"
            :is-loading="recentFanfictionsStatus == 'pending'"
            :list-type="FanfictionListType.Selections"
            :fanfictions="recentFanfictions"
        />
        <br />
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList
            :is-loading="newsStatus === 'pending'"
            :news="paginatedRecentNews ?? undefined"
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

const route = useRoute();

const { data: fandomData } = await useAsyncGql('getFandomDetails', {
    filters: {
        slug: { exact: route.params.fandomSlug  as string}
    }
});

if (fandomData.value.fandoms.length == 0) {
    navigateTo('/');
}

const { data: recentFanfictions, status: recentFanfictionsStatus } = await useAsyncGql('getFandomFictions', {
    filters: {
        fandoms: {
            id: {
                exact: fandomData.value.fandoms[0]?.id
            }
        }
    }
}, {
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
