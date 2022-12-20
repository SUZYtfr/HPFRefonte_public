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
      <FanfictionFilters
        :fanfictionQueryParams="fanfictionQueryParams"
        :loading="listLoading"
        :isFixedHeightCard="true"
        :tooltipPosition="'is-top'"
      />
    </b-modal>
    <br />
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div
        class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch"
      >
        <FanfictionFilters
          :fanfictionQueryParams="fanfictionQueryParams"
          :loading="listLoading"
        />
      </div>
      <!-- Liste des fictions -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <FanfictionList
          :fanfictionQueryParams="fanfictionQueryParams"
          :isLoading="listLoading"
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
        >Afficher les filtres</b-button
      >
    </div>
    <br />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { FanfictionQueryParams } from "@/types/fanfictions";
import FanfictionList from "~/components/list/fanfictions/FanfictionList.vue";
import FanfictionFilters from "~/components/filters/fanfictions/FanfictionFilters.vue";

@Component({
  name: "Recherche",
  components: {
    FanfictionList,
    FanfictionFilters,
  },
})
export default class extends Vue {
  //#region Data
  public filtersOpened: boolean = false;

  private fanfictionQueryParams: FanfictionQueryParams = {
    title: undefined,
    author: undefined,
    searchAuthorId: undefined,
    sortBy: "most_recent",
    multipleAuthors: undefined,
    status: undefined,
    minWords: undefined,
    maxWords: undefined,
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: undefined,
    inclusive: false,
    fromDate: undefined,
    toDate: undefined,
    page_size: 20,
    page: 1,
  };

  private listLoading: boolean = false;

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