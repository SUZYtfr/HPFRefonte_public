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
        :news-filters="newsFilters"
        :loading="listLoading"
      />
    </b-modal>
    <br>
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div
        class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch"
      >
        <NewsFilters
          :news-filters="newsFilters"
          :loading="listLoading"
        />
      </div>
      <!-- Liste des news -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <NewsList
          :news-filters="newsFilters"
          :is-loading="listLoading"
          @loadingChange="(value) => (listLoading = value)"
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
    <br>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { INewsFilters } from "@/types/news";
import NewsList from "~/components/list/news/NewsList.vue";
import NewsFilters from "~/components/filters/news/NewsFilters.vue";
import { SortByEnum } from "~/types/basics";

@Component({
  name: "Nouveautés",
  components: {
    NewsList,
    NewsFilters
  }
})
export default class extends Vue {
  // #region Data
  public filtersOpened: boolean = false;

  public newsFilters: INewsFilters = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: 0,
    status: null,
    fromDate: null,
    toDate: null,
    page: 1,
    pageSize: 10,
    totalPages: false,
    sortBy: SortByEnum.Descending,
    sortOn: "post_date"
  };

  public listLoading: boolean = false;

  // #endregion

  // #region Hooks
  mounted(): void {
    console.log("mounted");
  }
  // #endregion

  // #region Methods

  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.btn-filters {
  left: 50%;
  transform: translate(-50%, 0);
}

.stick-bottom {
  position: sticky;
  bottom: 0;
}
</style>
