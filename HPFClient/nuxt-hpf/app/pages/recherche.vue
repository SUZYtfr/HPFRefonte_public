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
      <FictionsFilters
        :fanfiction-filters
        :initial-included-ids
        :initial-excluded-ids
        :is-loading="status === 'pending'"
        :execute="execute"
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
        <FictionsFilters
          :initial-included-ids
          :initial-excluded-ids
          :fanfiction-filters
          :is-loading="status === 'pending'"
          :execute="execute"
        />
      </div>
      <!-- Liste des fictions -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <FictionsList
          :paginated-fanfictions
          :fiction-order
          :fiction-pagination
          :is-loading="status === 'pending'"
          :execute="execute"
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
import type { FictionFilters, FictionOrder, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
import { plainToInstance } from "class-transformer";
import { FanfictionModel } from "~/models";

const route = useRoute();

const initialIncludedIds = (route.query['tags'] as string || '').split('.').map(t => Number(t)).filter(t => t > 0);
const initialExcludedIds = (route.query['tags'] as string || '').split('.').map(t => Number(t)).filter(t => t < 0).map(t => Math.abs(t));

const filtersOpened = ref<boolean>(false);
const fictionOrder = ref<FictionOrder>({
  lastUpdateDate: Ordering.DESC,
});
const fictionPagination = reactive<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});
const fanfictionFilters = ref<FictionFilters>({
  characteristics: {
    allIdsInList: initialIncludedIds.length > 0 ? initialIncludedIds.map(t => t.toString()) : null,
    AND: {
      NOT: {
        id: {
          inList: initialExcludedIds.length > 0 ? initialExcludedIds.map(t => t.toString()) : null
        }
      }
    }
  }
});

// Met à jour l'URL avec les paramètres de recherche actuels
watch(fanfictionFilters.value, () => {
  const newSearchParams = new URLSearchParams();
  const tagsParams = (fanfictionFilters.value.characteristics?.allIdsInList || [])
    .concat(fanfictionFilters.value.characteristics?.NOT?.id?.inList?.map(t => '-' + t) || [])
    .toSorted((a, b) => Math.abs(Number(a)) - Math.abs(Number(b)) )

  if (tagsParams.length > 0) {
    newSearchParams.append('tags', tagsParams.join('.'));
  }
  history.replaceState({}, '', '/recherche?' + newSearchParams.toString());
})

/* const fanfictionFilters = reactive<IFanfictionFilters>({
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
}); */

const { data: paginatedFanfictions, status, execute } = await useAsyncGql('searchFictions', {
    filters: fanfictionFilters,
    order: fictionOrder,
    pagination: fictionPagination,
}, {
    transform: (input) => {
        return {
            ...input.fictions,
            results: plainToInstance(FanfictionModel, input.fictions.results)
        }
    }
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