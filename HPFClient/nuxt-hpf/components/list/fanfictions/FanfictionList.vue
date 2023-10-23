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
          @click="onFiltersChanged"
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
import type { IFanfictionFilters } from "@/types/fanfictions";
import { FanfictionModel } from "@/models/fanfictions";
import { searchFanfictions } from "@/api/fanfictions";
import { SortByEnum } from "~/types/basics";
import { UseFetchWrapperResponse } from "~/utils/api"

interface fanfictionListProps {
  isCard?: boolean
  showRefreshButton?: boolean
  isLoading?: boolean
  fanfictionFilters: IFanfictionFilters
}

const props = withDefaults(defineProps<fanfictionListProps>(), {
  isCard: true,
  showRefreshButton: true,
  isLoading: false
})

let fanfictionFilters: IFanfictionFilters = ref(props.fanfictionFilters).value

interface fanfictionListEmits {
  (e: 'changeSortBy', sortBy: SortByEnum): void
  (e: 'changeSortOn', sortOn: string): void
}

const emit = defineEmits<fanfictionListEmits>()


// TODO - rétablir ça
// get fanfictionResultLabel(): string {
  //   let result = "Aucun résultat";
  //   if (this.totalFanfictions === 0) return result;
  //   result = this.totalFanfictions.toString() + " résultat";
  //   result += this.totalFanfictions > 1 ? "s" : "";
  //   return result;
  // }
const totalFanfictions: number = 0;
const fanfictionResultLabel = "Aucun résultat"

// TODO - rétablir la snackbar d'erreur (useFetch fournit error)
const { data: fanfictions, refresh, pending: listLoading }: UseFetchWrapperResponse<FanfictionModel[]> = await searchFanfictions(props.fanfictionFilters || null)

const SelectSortBy_OnInputChanged = (value: string): void => {
  switch (value) {
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
  emit("changeSortBy", fanfictionFilters.sortBy)
  emit("changeSortOn", fanfictionFilters.sortOn)
}

// TODO - rétablir le watch
// @Watch("fanfictionFilters", { deep: true })
let timerId: number = 0;
const onFiltersChanged = (): void => {
  clearTimeout(timerId);
  timerId = window.setTimeout(() => refresh, 500);
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
