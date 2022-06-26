<template>
  <div
    :class="[
      { card: isCard },
      'is-flex',
      'is-flex-direction-column',
      'is-relative',
      'fullheight',
    ]"
  >
    <b-loading :is-full-page="false" v-model="listLoading"></b-loading>
    <header
      :class="[
        { 'card-header': isCard },
        'p-2',
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
      ]"
    >
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <b-button
          v-if="showRefreshButton"
          type="is-primary"
          icon-left="redo-alt"
          @click="onFiltersChanged"
        >
          <span class="is-italic">
            {{ newsResultLabel }}
          </span>
        </b-button>
      </div>
      <div class="is-flex-shrink-5">
        <b-field
          label="Ordre de tri"
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-select
            placeholder="Trier par"
            icon="sort"
            expanded
            v-model="newsFilters.sortBy"
          >
            <option value="alpha">Ordre alphabétique</option>
            <option value="most_recent">Plus récent au plus ancien</option>
            <option value="less_recent">Plus ancien au plus récent</option>
            <option value="most_reviews">Nombre de reviews - croissant</option>
            <option value="less_reviews">
              Nombre de reviews - décroissant
            </option>
            <option value="most_rating">Rating - croissant</option>
            <option value="less_rating">Rating - décroissant</option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div
      :class="[{ 'card-content': isCard }, 'px-0', 'py-3', 'is-flex-grow-5']"
    >
      <div v-if="news.length == 0" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3"
          >Aucun résultat, essayer d'ajuster les filtres de recherche.</span
        >
      </div>
      <div v-else>
        <div>
          <News_2
              v-for="(item, innerindex) of news"
              :key="'news_' + item.news_id.toString()"
              :news="item"
              :activeColor="innerindex % 2 != 0 ? '#e8d7e0' : '#f0f0f0'"
              :class="[{ 'is-hidden-mobile': innerindex > 0 }]"
              v-bind:index="innerindex"
            ></News_2>
        </div>
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <b-pagination
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="news.length"
        v-model="newsFilters.currentPage"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="newsFilters.perPage"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
      >
      </b-pagination>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import News_2 from "~/components/News_2.vue";
import { NewsData, NewsFiltersData } from "@/types/news";
import { getNews } from "@/api/news";

@Component({
  name: "NewsList",
  components: {
    News_2,
  },
})
export default class NewsList extends Vue {
  //#region Props
  @Prop({ default: true }) private isCard!: boolean;
  @Prop({ default: true }) private showRefreshButton!: boolean;
  @Prop({ default: false }) private isLoading!: boolean;
  @Prop() private newsFilters!: NewsFiltersData;
  //#endregion

  //#region Data
  private news: NewsData[] = [];
  private timerId: number = 0;

  // Pagination

  //#endregion

  //#region Computed
  get newsResultLabel() {
    let result = "";
    result += this.news.length > 0 ? this.news.length.toString() : "Aucun";
    result += " résultat";
    result += this.news.length > 1 ? "s" : "";
    return result;
  }

  get listLoading() {
    return this.isLoading;
  }

  set listLoading(value) {
    this.$emit("loadingChange", value);
  }
  //#endregion

  //#region Watchers
  @Watch("newsFilters", { deep: true })
  private onFiltersChanged() {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.getNews, 500);
  }
  //#endregion

  //#region Hooks
  mounted(){
    // Déclenche une recherche à l'affichage
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.getNews, 500);
  }
  //#endregion

  //#region Methods
  private async getNews() {
    this.listLoading = true;
    try {
      const { data } = await getNews(this.newsFilters);
      this.news = data.items;
    } catch {
    } finally {
      this.listLoading = false;
    }
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>