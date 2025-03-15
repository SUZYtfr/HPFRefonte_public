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
        :fanfiction-filters="fanfictionFilters"
        :loading="listLoading"
        :is-fixed-height-card="true"
        :tooltip-position="'is-top'"
      />
    </b-modal>
    <br>
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div
        class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch"
      >
        <FanfictionFilters
          :fanfiction-filters="fanfictionFilters"
          :loading="listLoading"
        />
      </div>
      <!-- Liste des fictions -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <FanfictionList
          :fanfiction-filters="fanfictionFilters"
          :is-loading="listLoading"
          @loadingChange="(value: boolean) => (listLoading = value)"
        />
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
  </div>
</template>

<script setup lang="ts">
import { IFanfictionFilters } from "@/types/fanfictions";
import FanfictionList from "~/components/list/fanfictions/FanfictionList.vue";
import FanfictionFilters from "~/components/filters/fanfictions/FanfictionFilters.vue";
import { SortByEnum } from "~/types/basics";

const filtersOpened = ref<boolean>(false);

const fanfictionFilters = reactive<IFanfictionFilters>({
  searchTerm: null,
  searchAuthor: null,
  searchAuthorId: null,
  multipleAuthors: null,
  status: null,
  wordCount_min: null,
  wordCount_max: null,
  includedTags: [],
  excludedTags: [],
  customTags: [],
  featured: null,
  inclusive: false,
  fromDate: null,
  toDate: null,
  page: 1,
  pageSize: 10,
  totalPages: true,
  sortBy: SortByEnum.Descending,
  sortOn: "last_update_date"
});

const listLoading = ref<boolean>(false);
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
