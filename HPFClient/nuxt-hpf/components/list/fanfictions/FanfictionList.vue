<template>
  <div :class="[{'card': isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <b-loading v-model="listLoading" :is-full-page="false" />
    <header
      :class="[
        {'card-header': isCard },
        'p-2',
        'is-flex', 'is-flex-direction-row', 'is-align-items-center'
      ]"
    >
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <b-button
          v-if="showRefreshButton"
          type="is-primary"
          icon-left="redo-alt"
          @click="execute"
        >
          <span class="is-italic">
            {{ fanfictionResultLabel }}
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
            <option value="alpha">
              Ordre alphabétique
            </option>
            <option value="most_recent">
              Plus récent au plus ancien
            </option>
            <option value="less_recent">
              Plus ancien au plus récent
            </option>
            <option value="most_reviews">
              Nombre de reviews - croissant
            </option>
            <option value="less_reviews">
              Nombre de reviews - décroissant
            </option>
            <option value="most_rating">
              Rating - croissant
            </option>
            <option value="less_rating">
              Rating - décroissant
            </option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div :class="[{'card-content': isCard }, 'px-2', 'py-3', 'is-flex-grow-5']">
      <div
        v-if="(fanfictions?.length ?? 0) == 0"
        class="mx-auto my-auto has-text-centered"
      >
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <Fanfiction
          v-for="(fanfiction, innerindex) of fanfictions"
          :key="'ff_' + fanfiction.fanfiction_id.toString()"
          class="my-2"
          :fanfiction="fanfiction"
          :index="innerindex"
        />
      </div>
    </div>
    <footer :class="[{'card-footer':isCard}]">
      <b-pagination
        v-model="fanfictionFilters.page"
        :class="[{'card-footer-item': isCard}, 'py-2']"
        :total="totalFanfictions"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="fanfictionFilters.pageSize"
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

<script setup lang="ts">
import Fanfiction from "~/components/Fanfiction.vue";
import { IFanfictionFilters } from "@/types/fanfictions";
import { FanfictionModel } from "@/models/fanfictions";
import { searchFanfictions } from "@/api/fanfictions";
import { SortByEnum } from "~/types/basics";

interface Props {
  isCard?: boolean;
  showRefreshButton?: boolean;
  isLoading?: boolean;
  fanfictionFilters?: IFanfictionFilters;
}

const { isCard = true, showRefreshButton = true, isLoading = false, fanfictionFilters } = defineProps<Props>();

const { data: paginatedFanfictions, status, execute } = await searchFanfictions(fanfictionFilters);
const listLoading = computed<boolean>(() => status.value === 'pending');
const fanfictions = computed<FanfictionModel[]>(() => paginatedFanfictions.value.results);
const totalFanfictions = computed<number>(() => paginatedFanfictions.value.count);

const fanfictionResultLabel = computed<string>(() => {
  let result = "Aucun résultat";
  if (totalFanfictions.value === 0) return result;
  result = totalFanfictions.value.toString() + " résultat";
  result += totalFanfictions.value > 1 ? "s" : "";
  return result;
});

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
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
