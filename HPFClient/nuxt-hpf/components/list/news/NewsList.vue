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
    <b-loading v-model="listLoading" :is-full-page="false" />
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
            @input="SelectSortBy_OnInputChanged"
          >
            <option value="most_recent">
              Plus récent au plus ancien
            </option>
            <option value="less_recent">
              Plus ancien au plus récent
            </option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div
      :class="[{ 'card-content': isCard }, 'p-2', 'is-flex-grow-5']"
    >
      <div v-if="(news?.length ?? 0) == 0" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <div>
          <News_2
            v-for="(item, innerindex) of news"
            :key="'news_' + item.news_id.toString()"
            class="mb-2"
            :news="item"
            :active-color="innerindex % 2 != 0 ? '#e8d7e0' : '#f0f0f0'"
            :index="innerindex"
          />
        </div>
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <b-pagination
        v-model="newsFilters.page"
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="totalNews"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="newsFilters.pageSize"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
      />
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import News_2 from "~/components/News_2.vue";
import { INewsFilters } from "@/types/news";
import { NewsModel } from "@/models/news";
import { searchNews } from "@/api/news";
import { SortByEnum } from "~/types/basics";

@Component({
  name: "NewsList",
  components: {
    News_2
  },
  fetchOnServer: true,
  fetchKey: "news-list"
})
export default class NewsList extends Vue {
  // #region Props
  @Prop({ default: true }) public isCard!: boolean;
  @Prop({ default: true }) public showRefreshButton!: boolean;
  @Prop({ default: false }) private isLoading!: boolean;
  @Prop() public newsFilters!: INewsFilters;
  // #endregion

  // #region Data
  @SerialiseClass(NewsModel)
  public news: NewsModel[] = [];

  public totalNews: number = 0;
  private timerId: number = 0;
  // #endregion

  // #region Computed
  get newsResultLabel(): string {
    let result = "Aucun résultat";
    if (this.totalNews === 0) return result;
    result = this.totalNews.toString() + " résultat";
    result += this.totalNews > 1 ? "s" : "";
    return result;
  }

  get listLoading(): boolean {
    return this.isLoading;
  }

  set listLoading(value) {
    this.$emit("loadingChange", value);
  }
  // #endregion

  // #region Watchers
  @Watch("newsFilters", { deep: true })
  public onFiltersChanged(): void {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.$fetch, 500);
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des fictions
    await this.searchNews();
    this.listLoading = false;
  }
  // #endregion

  // #region Methods
  private async searchNews(): Promise<void> {
    try {
      const response = (await searchNews(this.newsFilters));
      this.news = response.results;
      this.newsFilters.page = response.current;
      this.totalNews = response.count;
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des actualités",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    }
  }

  public SelectSortBy_OnInputChanged(value: string): void {
    switch (value) {
      case "most_recent":
        // this.newsFilters.sortBy = SortByEnum.Descending;
        // this.newsFilters.sortOn = "last_update_date";
        this.newsFilters.orderBy = "-post_date";
        break;
      case "less_recent":
        // this.newsFilters.sortBy = SortByEnum.Ascending;
        // this.newsFilters.sortOn = "last_update_date";
        this.newsFilters.orderBy = "post_date";
        break;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
