<template>
  <div
    :class="[
      { card: isCard },
      'is-flex',
      'is-flex-direction-column',
      'is-relative',
      'fullheight',
    ]"
  >
    <b-loading v-model="listLoading" :is-full-page="false" />
    <header
      :class="[
        { 'card-header': isCard },
        'p-2',
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
      ]"
    >
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <b-button
          v-if="showRefreshButton"
          type="is-primary"
          icon-left="redo-alt"
          @click="refreshNews"
        >
          <span class="is-italic">
            {{ newsResultLabel }}
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
            @input="(e: InputEvent) => newsFilters.sortOrder = e?.target?.value"
          >
            <option :value="SortOrderEnum.MostRecentFirst">
              Plus récent au plus ancien
            </option>
            <option :value="SortOrderEnum.MostRecentLast">
              Plus ancien au plus récent
            </option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div
      :class="[{ 'card-content': isCard }, 'p-2', 'is-flex-grow-5']"
    >
      <div v-if="(news?.length ?? 0) == 0" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <div>
          <News_2
            v-for="(item, innerindex) of news"
            :key="'news_' + item.news_id.toString()"
            class="mb-2"
            :news="item"
            :active-color="innerindex % 2 != 0 ? '#e8d7e0' : '#f0f0f0'"
            :index="innerindex"
          />
        </div>
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <b-pagination
        v-model="newsFilters.page"
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="totalNews"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="newsFilters.pageSize"
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
import News_2 from "~/components/News_2.vue";
import { INewsFilters } from "@/types/news";
import { NewsModel } from "@/models/news";
import { searchNews } from "@/api/news";
import { SortOrderEnum } from "~/types/basics";
import { UseFetchWrapperResponse } from "~/utils/api";
import { debounce } from '~/utils/es6-utils'
import { SnackbarProgrammatic as Snackbar } from 'buefy'

interface NewsListProps {
  isCard?: boolean
  showRefreshButton?: boolean
  // isLoading?: boolean  // on utilise la référence pending de useFetch directement
  newsFilters: INewsFilters
}
const { isCard, showRefreshButton, newsFilters } = withDefaults(defineProps<NewsListProps>(), {
  isCard: true,
  showRefreshButton: true,
  // isLoading: false,
})

const { data: news, pending: listLoading, refresh: refreshNews, error: newsError }: UseFetchWrapperResponse<NewsModel[]> = await searchNews(newsFilters)

watch(newsError, async (value) => {
  if (value && process.client) {
    console.error(value)
    Snackbar.open({
      duration: 5000,
      message: "Une erreur s'est produite lors de la récupération des actualités",
      type: "is-danger",
      position: "is-bottom-right",
      actionText: null,
      pauseOnHover: true,
      queue: true
    })
  }
})

interface NewsListEmits {
  (e: "loadingChange", value: boolean): void
}
const emit = defineEmits<NewsListEmits>()
watch(listLoading, async (value) => {
  emit("loadingChange", value)
})

const totalNews: number = 0; // TODO searchNews, ajouter ".meta" avec données de pagination ?

// FIXME - réparer ça quand on a les données méta de pagination
// const newsResultLabel = (): string => {
//   let result = "Aucun résultat";
//   if (totalNews === 0) return result;
//   result = totalNews.toString() + " résultat";
//   result += totalNews > 1 ? "s" : "";
//   return result;
// }
const newsResultLabel = "Rafraîchir"

const debouncedFilterChange = debounce(() => refreshNews(), 500)
watch(newsFilters, () => {
  debouncedFilterChange()
}, { deep: true })
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
