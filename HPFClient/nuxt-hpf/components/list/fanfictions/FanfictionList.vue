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
          @click="refresh"
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
            @input="(e: InputEvent) => fanfictionFilters.sortOrder = e?.target?.value"
          >
            <option :value="SortOrderEnum.TitleAlphabetic">
              Ordre alphabétique
            </option>
            <option :value="SortOrderEnum.MostRecentFirst">
              Plus récent au plus ancien
            </option>
            <option :value="SortOrderEnum.MostRecentLast">
              Plus ancien au plus récent
            </option>
            <option :value="SortOrderEnum.MostReviewsFirst">
              Nombre de reviews - croissant
            </option>
            <option :value="SortOrderEnum.MostReviewsLast">
              Nombre de reviews - décroissant
            </option>
            <option :value="SortOrderEnum.GreatestAverageFirst">
              Rating - croissant
            </option>
            <option :value="SortOrderEnum.GreatestAverageLast">
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
import { SortOrderEnum } from "~/types/basics";
import { UseFetchWrapperResponse } from "~/utils/api"
import { SnackbarProgrammatic as Snackbar } from "buefy";
import { debounce } from "~/utils/es6-utils";

interface fanfictionListProps {
  isCard?: boolean
  showRefreshButton?: boolean
  isLoading?: boolean
  fanfictionFilters: IFanfictionFilters
}

const { isCard, showRefreshButton, isLoading, fanfictionFilters } = withDefaults(defineProps<fanfictionListProps>(), {
  isCard: true,
  showRefreshButton: true,
  isLoading: false
})

// TODO - rétablir ça quand on aura les données méta d'une réponse paginée
// get fanfictionResultLabel(): string {
  //   let result = "Aucun résultat";
  //   if (this.totalFanfictions === 0) return result;
  //   result = this.totalFanfictions.toString() + " résultat";
  //   result += this.totalFanfictions > 1 ? "s" : "";
  //   return result;
  // }
const totalFanfictions: number = 0;
const fanfictionResultLabel = "Rafraîchir"

const { data: fanfictions, refresh, pending: listLoading, error: fanfictionError }: UseFetchWrapperResponse<FanfictionModel[]> = await searchFanfictions(fanfictionFilters)

watch(fanfictionError, async (value) => {
  if (value && process.client) {
    console.error(value)
    Snackbar.open({
      duration: 5000,
      message: "Une erreur s'est produite lors de la récupération des fanfictions",
      type: "is-danger",
      position: "is-bottom-right",
      actionText: null,
      pauseOnHover: true,
      queue: true
    })
  }
})

const debouncedRefresh = debounce(() => refresh(), 500)
watch(fanfictionFilters, () => {
  debouncedRefresh()
})
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
