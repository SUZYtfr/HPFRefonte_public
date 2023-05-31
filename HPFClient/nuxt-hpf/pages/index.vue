<template>
  <div class="container px-5">
    <br>
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <FanfictionThumbnailList :is-loading="listLoading" :list-type="FanfictionListType.Recent" :fanfictions="recentFanfictions" />
        <br>
        <!-- Sélections fanfictions -->
        <FanfictionThumbnailList :is-loading="listLoading" :list-type="FanfictionListType.Selections" :fanfictions="selectionsFanfictions" />
        <br>
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <NewsThumbnailList :is-loading="listLoading" :news="recentNews" />
      </div>
    </div>
    <br>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { searchNews } from "@/api/news";
import { NewsModel } from "@/models/news";
import { searchFanfictions } from "@/api/fanfictions";
import { FanfictionModel } from "@/models/fanfictions";
import { IBasicQuery, SortByEnum } from "@/types/basics";
import { IFanfictionFilters } from "@/types/fanfictions";
import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";
import FanfictionThumbnailList from "~/components/list/fanfictions/FanfictionThumbnailList.vue";
import NewsThumbnailList from "~/components/list/news/NewsThumbnailList.vue";

@Component({
  components: {
    FanfictionThumbnail,
    FanfictionThumbnailList,
    NewsThumbnailList
  },
  fetchOnServer: true,
  fetchKey: "index"
})
export default class extends Vue {
  // #region  Datas

  @SerialiseClass(NewsModel)
  public recentNews: NewsModel[] = [];

  @SerialiseClass(FanfictionModel)
  public recentFanfictions: FanfictionModel[] = [];

  @SerialiseClass(FanfictionModel)
  public selectionsFanfictions: FanfictionModel[] = [];

  public listLoading = false;
  private recentFanfictionFilters : IFanfictionFilters = {
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
    minWords: null,
    maxWords: null,
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: null,
    inclusive: false,
    fromDate: null,
    toDate: null
  };

  private selectionsFanfictionFilters : IFanfictionFilters = {
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
    minWords: null,
    maxWords: null,
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: true,
    inclusive: false,
    fromDate: null,
    toDate: null
  };

  private newsFilters : IBasicQuery = {
    page: 1,
    pageSize: 20,
    totalPages: true,
    sortOn: "post_date",
    sortBy: SortByEnum.Descending
  };
  // #endregion

  // #region Hooks
  created(): void {}

  async fetch(): Promise<void> {
    this.listLoading = true;
    try {
      this.recentNews = (await searchNews(this.newsFilters)).results;
      this.recentFanfictions = (await searchFanfictions(this.recentFanfictionFilters)).results;
      this.selectionsFanfictions = (await searchFanfictions(this.selectionsFanfictionFilters)).results;
    // console.log("Fanfiction type: " + (this.fanfictions[0] instanceof FanfictionModel));
    // console.log("Date type: " + ((new Date()) instanceof Date));
    // console.log("Creation date type: " + (this.fanfictions[0]?.creation_date instanceof Date));
    // console.log("Last update date type: " + (this.fanfictions[0]?.last_update_date instanceof Date));
    // console.log(this.fanfictions[0]?.creation_date?.toLocaleDateString());
    // console.log(this.fanfictions[0]?.creation_date?.toLocaleDateString());
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des données",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    } finally {
      this.listLoading = false;
    }
  }

  beforeMount(): void {}

  mouted(): void {}
  // #endregion

  // #region Methods
  // private async searchNews(): Promise<void> {
  //   this.listLoading = true;
  //   try {
  //     const { data } = await searchNews(this.newsFilters);
  //     this.news = data.items;
  //   } catch {
  //   } finally {
  //     this.listLoading = false;
  //   }
  // }

  // private async getFanfictions(): Promise<void> {
  //   this.listLoading = true;
  //   try {
  //     const { data } = await getFanfictions(this.fanfictionFilters);
  //     this.fanfictions = data.items;
  //   } catch {
  //   } finally {
  //     this.listLoading = false;
  //   }
  // }
  // #endregion
}
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
