<template>
  <div class="container px-5">
    <!-- Modal filtres -->
    <b-modal
      v-model="filtersOpened"
      scroll="clip"
      width="70vw"
      class="is-hidden-desktop"
      has-modal-card
    >
      <NewsFilters
        :news-filters
        :is-loading="newsStatus == 'pending'"
        :execute
      />
    </b-modal>
    <br/>
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div
        class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch"
      >
        <NewsFilters
          :news-filters
          :is-loading="newsStatus == 'pending'"
          :execute
        />
      </div>
      <!-- Liste des news -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <NewsList
          :paginated-news
          :news-pagination
          :news-order
          :is-loading="newsStatus == 'pending'"
          :execute
        />
      </div>
    </div>
    <!-- Bouton filtres (seulement en tablet et inférieur) -->
    <div class="stick-bottom is-hidden-desktop">
      <b-button
        v-if="!filtersOpened"
        type="is-primary"
        icon-right="filter"
        class="btn-filters mb-2"
        @click="filtersOpened = true"
      >
        Afficher les filtres
      </b-button>
    </div>
    <br/>
  </div>
</template>

<script setup lang="ts">
import type { NewsArticleFilters, NewsArticleOrder, NewsArticleTypeOffsetPaginated, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
import { plainToInstance } from "class-transformer";
import { NewsModel } from "~/models";

const filtersOpened = ref<boolean>(false);

const newsFilters = ref<NewsArticleFilters>({});
const newsOrder = ref<NewsArticleOrder>({
  postDate: Ordering.DESC,
});
const newsPagination = reactive<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});

const { data: paginatedNews, status: newsStatus, execute } = await useAsyncGql("getNews", {
  pagination: newsPagination,
  order: newsOrder,
  filters: newsFilters,
}, {
  lazy: true,
  transform: (input: { news: NewsArticleTypeOffsetPaginated }) => {
    return {
      ...input.news,
      results: plainToInstance(NewsModel, input.news.results),
    };
  }
});

useHead({
  title: "HPF - Recherche d'actualités",
});

</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

.btn-filters {
  left: 50%;
  transform: translate(-50%, 0);
}

.stick-bottom {
  position: sticky;
  bottom: 0;
}
</style>