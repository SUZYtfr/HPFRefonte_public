<template>
  <div class="card">
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">
        Actualités
      </p>
    </header>
    <div class="card-content is-relative">
      <b-loading v-model="isLoading" :is-full-page="false" />
      <div v-if="news?.length > 0">
        <News_2
          v-for="(item, innerindex) of news"
          :key="'news_' + (item.news_id?.toString() ?? '0')"
          :news="item"
          :active-color="innerindex % 2 != 0 ? '#e8d7e0' : '#f0f0f0'"
          :class="[{ 'is-hidden-mobile': innerindex > 0 }]"
          :index="innerindex"
        />
      </div>
      <p v-else class="has-text-centered">
        Aucune actualité trouvée
      </p>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <NuxtLink to="/news"> Plus d'actualités </NuxtLink>
        </span>
      </p>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import News_2 from "~/components/News_2.vue";
import { NewsModel } from "@/models/news";

  @Component({
    name: "NewsThumbnailList",
    components: {
      News_2
    },
    fetchOnServer: true,
    fetchKey: "news-thumbnail-list"
  })
export default class NewsList extends Vue {
    // #region Props
    @Prop({ default: false }) public isLoading!: boolean;
    @Prop({ default: [] }) public news!: NewsModel[];
    // #endregion
}
</script>

<style lang="scss" scoped>

</style>
