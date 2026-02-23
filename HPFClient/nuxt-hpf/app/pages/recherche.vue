<template>
  <div class="container px-5">
    <!-- Modal filtres -->
    <BModal v-model="filtersOpened" scroll="clip" width="70vw" class="is-hidden-desktop" has-modal-card>
      <FictionsFilters
        :fanfiction-filters
        :initial-included-ids="initialIncludedTagIds"
        :initial-excluded-ids="initialExcludedTagIds"
        :is-loading="status === 'pending'"
        :execute="execute"
        :is-fixed-height-card="true"
        :tooltip-position="'is-top'"
        @filters-change="(filters: FictionFilters) => (fanfictionFilters = filters)"
      />
    </BModal>
    <br />
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch">
        <FictionsFilters
          :initial-included-ids="initialIncludedTagIds"
          :initial-excluded-ids="initialExcludedTagIds"
          :fanfiction-filters
          :is-loading="status === 'pending'"
          :execute="execute"
          @filters-change="(filters: FictionFilters) => (fanfictionFilters = filters)"
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
          @pagination-change="(pagination: OffsetPaginationInput) => (fictionPagination = pagination)"
          @order-change="(order: FictionOrder) => (fictionOrder = order)"
        />
      </div>
      <!-- Bouton filtres (seulement en tablet et inférieur) -->
      <div class="stick-bottom is-hidden-desktop">
        <BButton
          v-if="!filtersOpened"
          type="is-primary"
          icon-right="filter"
          class="btn-filters mb-2"
          @click="filtersOpened = true"
        >
          Afficher les filtres
        </BButton>
      </div>
      <br />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FictionFilters, FictionOrder, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
import { plainToInstance } from "class-transformer";
import { FanfictionModel } from "@/models";

const route = useRoute();

const initialIncludedFandomIds = ((route.query["fandoms"] as string) || "")
  .split(".")
  .map((t) => Number(t))
  .filter((t) => t > 0);
const initialExcludedFandomIds = ((route.query["fandoms"] as string) || "")
  .split(".")
  .map((t) => Number(t))
  .filter((t) => t < 0)
  .map((t) => Math.abs(t));
const initialIncludedTagIds = ((route.query["tags"] as string) || "")
  .split(".")
  .map((t) => Number(t))
  .filter((t) => t > 0);
const initialExcludedTagIds = ((route.query["tags"] as string) || "")
  .split(".")
  .map((t) => Number(t))
  .filter((t) => t < 0)
  .map((t) => Math.abs(t));

const filtersOpened = ref<boolean>(false);
const fictionOrder = ref<FictionOrder>({
  lastUpdateDate: Ordering.DESC,
});
const fictionPagination = ref<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});

const fanfictionFilters = ref<FictionFilters>({
  fandoms: {
    allIdsInList: initialIncludedFandomIds.length > 0 ? initialIncludedFandomIds.map((t) => t.toString()) : null,
    NOT: {
      id: {
        inList: initialExcludedFandomIds.length > 0 ? initialExcludedFandomIds.map((t) => t.toString()) : null,
      },
    },
  },
  characteristics: {
    allIdsInList: initialIncludedTagIds.length > 0 ? initialIncludedTagIds.map((t) => t.toString()) : null,
    NOT: {
      id: {
        inList: initialExcludedTagIds.length > 0 ? initialExcludedTagIds.map((t) => t.toString()) : null,
      },
    },
  },
});

// Met à jour l'URL avec les paramètres de recherche actuels
watch(fanfictionFilters.value, () => {
  const newSearchParams = new URLSearchParams();
  const fandomsParams = (fanfictionFilters.value.fandoms?.allIdsInList || [])
    .concat(fanfictionFilters.value.fandoms?.NOT?.id?.inList?.map((t) => "-" + t) || [])
    .toSorted((a, b) => Math.abs(Number(a)) - Math.abs(Number(b)));
  const tagsParams = (fanfictionFilters.value.characteristics?.allIdsInList || [])
    .concat(fanfictionFilters.value.characteristics?.NOT?.id?.inList?.map((t) => "-" + t) || [])
    .toSorted((a, b) => Math.abs(Number(a)) - Math.abs(Number(b)));

  if (fandomsParams.length > 0) {
    newSearchParams.append("fandoms", fandomsParams.join("."));
  }
  if (tagsParams.length > 0) {
    newSearchParams.append("tags", tagsParams.join("."));
  }
  history.replaceState({}, "", "/recherche?" + newSearchParams.toString());
});

const {
  data: paginatedFanfictions,
  status,
  execute,
} = await useAsyncGql(
  "searchFictions",
  {
    filters: fanfictionFilters,
    order: fictionOrder,
    pagination: fictionPagination,
  },
  {
    transform: (input) => {
      return {
        ...input.fictions,
        results: plainToInstance(FanfictionModel, input.fictions.results),
      };
    },
  },
);

useHead({
  title: "HPF - Recherche de fanfictions",
});
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
