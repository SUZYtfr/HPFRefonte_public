<template>
  <div :class="[{ card: isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <BLoading v-model="isLoading" :is-full-page="false" />
    <header :class="[{ 'card-header': isCard }, 'p-2', 'is-flex', 'is-flex-direction-row', 'is-align-items-center']">
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <BButton v-if="showRefreshButton" type="is-primary" icon-left="redo-alt" @click="searchFictions">
          <span class="is-italic">
            {{ fanfictionResultLabel }}
          </span>
        </BButton>
      </div>
      <div class="is-flex-shrink-5">
        <BField label="Ordre de tri" label-position="on-border" custom-class="has-text-primary">
          <BSelect
            v-model="fictionsOrderChoice"
            placeholder="Trier par"
            icon="sort"
            expanded
            @update:model-value="(order: string) => (fictionsOrderChoice = order)"
          >
            <option value="alpha">Ordre alphabétique</option>
            <option value="most_recent">Plus récent au plus ancien</option>
            <option value="less_recent">Plus ancien au plus récent</option>
            <option value="most_reviews">Nombre de reviews - croissant</option>
            <option value="less_reviews">Nombre de reviews - décroissant</option>
            <option value="most_rating">Rating - croissant</option>
            <option value="less_rating">Rating - décroissant</option>
          </BSelect>
        </BField>
      </div>
    </header>
    <div :class="[{ 'card-content': isCard }, 'px-2', 'py-3', 'is-flex-grow-5']">
      <div v-if="!paginatedFanfictions.results.length" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <FictionsEntity
          v-for="(fanfiction, innerindex) of paginatedFanfictions.results"
          :key="'ff_' + fanfiction.fanfictionId.toString()"
          class="my-2"
          :fanfiction="fanfiction"
          :index="innerindex"
        />
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <BPagination
        v-model="pageFictionPagination.page"
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="paginatedFanfictions.totalCount"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="pageFictionPagination.pageSize"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
        @change="(page: number) => (pageFictionPagination.page = page)"
      />
    </footer>
  </div>
</template>

<script setup lang="ts">
import type { FanfictionModel } from "@/models";
import type { FictionOrder, FictionTypeOffsetPaginated, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";

interface Props {
  isCard?: boolean;
  showRefreshButton?: boolean;
  paginatedFanfictions: Omit<FictionTypeOffsetPaginated, "results"> & { results: FanfictionModel[] };
  searchFictions: () => Promise<void>;
}

const { isCard = true, showRefreshButton = true, paginatedFanfictions } = defineProps<Props>();

const pagination = defineModel<OffsetPaginationInput>("pagination", { required: true });
const order = defineModel<FictionOrder>("order", { required: true });
const isLoading = defineModel<boolean>("isLoading", { required: false, default: false });

// Transforme le système offset / limit en page / pageSize
const pageFictionPagination = reactive({
  pageSize: pagination.value.limit!,
  page: pagination.value.offset! / pagination.value.limit! + 1,
});
watch(pageFictionPagination, () => {
  pagination.value.limit = pageFictionPagination.pageSize;
  pagination.value.offset = (pageFictionPagination.page - 1) * pageFictionPagination.pageSize;
});

// TODO marche mais très moche, à la rigueur tenter un truc avec watch ?
const fictionsOrderChoice = computed<string>({
  get() {
    if (order.value.lastUpdateDate === Ordering.DESC) {
      return "most_recent";
    } else if (order.value.lastUpdateDate === Ordering.ASC) {
      return "less_recent";
    } else if (order.value.title === Ordering.DESC) {
      return "alpha";
    } else {
      return "";
    }
  },
  set(value: string) {
    if (value === "most_recent") {
      order.value.lastUpdateDate = Ordering.DESC;
      order.value.title = undefined;
    } else if (value === "less_recent") {
      order.value.lastUpdateDate = Ordering.ASC;
      order.value.title = undefined;
    } else if (value === "alpha") {
      order.value.title = Ordering.ASC;
      order.value.lastUpdateDate = undefined;
    }
  },
});

const fanfictionResultLabel = computed<string>(() => {
  let result = "Aucun résultat";
  if (paginatedFanfictions.totalCount === 0) return result;
  result = paginatedFanfictions.totalCount.toString() + " résultat";
  result += paginatedFanfictions.totalCount > 1 ? "s" : "";
  return result;
});

/*
let timerId: number = 0;
watch(() => fanfictionFilters, () => {
  clearTimeout(timerId);
  timerId = window.setTimeout(execute, 500);
}, {deep: true});

function SelectSortBy_OnInputChanged(event: any): void {
  if (fanfictionFilters == null) return;
  switch (event.target.value) {
    case "alpha":
      fanfictionFilters.sortBy = SortByEnum.Ascending;
      fanfictionFilters.sortOn = "title";
      break;
    case "most_recent":
      fanfictionFilters.sortBy = SortByEnum.Descending;
      fanfictionFilters.sortOn = "last_update_date";
      break;
    case "less_recent":
      fanfictionFilters.sortBy = SortByEnum.Ascending;
      fanfictionFilters.sortOn = "last_update_date";
      break;
    case "most_reviews":
      fanfictionFilters.sortBy = SortByEnum.Descending;
      fanfictionFilters.sortOn = "comments";
      break;
    case "less_reviews":
      fanfictionFilters.sortBy = SortByEnum.Ascending;
      fanfictionFilters.sortOn = "comments";
      break;
    case "most_rating":
      fanfictionFilters.sortBy = SortByEnum.Ascending;
      fanfictionFilters.sortOn = "rating";
      break;
    case "less_rating":
      fanfictionFilters.sortBy = SortByEnum.Ascending;
      fanfictionFilters.sortOn = "rating";
      break;
  }
} */
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
