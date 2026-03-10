<template>
  <div class="card">
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">Actualités</p>
    </header>
    <div class="card-content is-relative p-2">
      <BLoading :v-model="isLoading" :is-full-page="false" />
      <div v-if="(news?.totalCount ?? 0) > 0">
        <NewsEntity
          v-for="(item, innerindex) of news?.results"
          :key="'news_' + (item.newsId?.toString() ?? '0')"
          :news="item"
          :class="[
            { 'is-hidden-mobile': innerindex > 0 },
            'mb-2',
            { 'is-color-even': innerindex % 2 != 0 },
            { 'is-color-odd': innerindex % 2 == 0 },
          ]"
          :index="innerindex"
        />
      </div>
      <p v-else class="has-text-centered my-2">Aucune actualité trouvée</p>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <NuxtLink prefetch-on="interaction" to="/news"> Plus d'actualités </NuxtLink>
        </span>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import type { NewsModel } from "~/models";
import type { TransformedPaginated } from "~/types/other";

interface Props {
  news?: TransformedPaginated<NewsModel>;
}

defineProps<Props>();
const isLoading = defineModel<boolean>("isLoading", { required: false, default: false });
</script>

<style lang="scss" scoped></style>
