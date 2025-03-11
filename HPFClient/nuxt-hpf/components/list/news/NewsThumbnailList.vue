<template>
  <div class="card">
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">
        Actualités
      </p>
    </header>
    <div class="card-content is-relative p-2">
      <b-loading v-if="isLoading" :is-full-page="false" />
      <div v-if="news?.length > 0">
        <News_2
          v-for="(item, innerindex) of news"
          :key="'news_' + (item.news_id?.toString() ?? '0')"
          :news="item"
          :class="[{ 'is-hidden-mobile': innerindex > 0 }, 'mb-2', {'is-color-even': (innerindex % 2 != 0) }, {'is-color-odd': (innerindex % 2 == 0) }]"
          :index="innerindex"
        />
      </div>
      <p v-else class="has-text-centered my-2">
        Aucune actualité trouvée
      </p>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <NuxtLink
            to="/news"
            no-prefetch
          > Plus d'actualités </NuxtLink>
        </span>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import News_2 from "~/components/News_2.vue";
import { NewsModel } from "@/models/news";

const { isLoading = false, news = [] } = defineProps<{
  isLoading: boolean;
  news: NewsModel[];
}>()

</script>

<style lang="scss" scoped>

</style>
