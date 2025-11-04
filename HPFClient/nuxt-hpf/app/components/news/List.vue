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
        'is-white'
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
            v-model="newsOrderChoice"
          >
            <option value="most_recent">
              Plus récent au plus ancien
            </option>
            <option value="less_recent">
              Plus ancien au plus récent
            </option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div
      :class="[{ 'card-content': isCard }, 'p-2', 'is-flex-grow-5']"
    >
      <div v-if="(paginatedNews.results?.length ?? 0) == 0" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <div>
          <NewsEntity2
            v-for="(item, innerindex) of paginatedNews.results"
            :key="'news_' + item.newsId.toString()"
            :class="['mb-2', {'is-color-even': (innerindex % 2 != 0) }, {'is-color-odd': (innerindex % 2 == 0) }]"
            :news="item"
            :index="innerindex"
          />
        </div>
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <b-pagination
        v-model="page"
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="paginatedNews.totalCount"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="newsPagination.limit"
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
import type { NewsArticleFilters, NewsArticleOrder, NewsArticleTypeOffsetPaginated, OffsetPaginationInput } from '#gql';
import { Ordering } from '#gql/default';
import type { NewsModel } from '~/models';

const {
  isCard = true,
  paginatedNews,
  showRefreshButton = true,
  isLoading = false,
  newsPagination,
  newsOrder,
  execute,
} = defineProps<{
  isCard?: boolean,
  showRefreshButton?: boolean,
  isLoading?: boolean,
  paginatedNews: Omit<NewsArticleTypeOffsetPaginated, 'results'> & { results: NewsModel[]},
  newsFilters?: NewsArticleFilters,
  newsPagination: OffsetPaginationInput,
  newsOrder: NewsArticleOrder,
  execute: () => {},
}>();

const listLoading = computed<boolean>(() => isLoading );

const timerId: number = 0;

const newsResultLabel = computed<string>(() => {
    let result = "Aucun résultat";
    if (paginatedNews.totalCount === 0) return result;
    result = paginatedNews.totalCount.toString() + " résultat";
    result += paginatedNews.totalCount > 1 ? "s" : "";
    return result;
});

// Transforme le système offset / limit en page / pageSize et vice versa
const page = computed<number>(
  {
    get() { return (newsPagination.offset! / newsPagination.limit!) + 1 },
    set(page: number) { newsPagination.offset = (page - 1) * newsPagination.limit! },
  },
);

const newsOrderChoice = computed<string>(
  {
    get() { return newsOrder.postDate === Ordering.DESC ? 'most_recent' : 'less_recent' },
    set(value: string) { newsOrder.postDate = value == 'most_recent' ? Ordering.DESC : Ordering.ASC },
  },
);

// TODO à la place, tenter un debounce sur useAsyncData.execut ou .watch
const onFiltersChanged = () => {};

</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
.card-header {
  background-color: var(--scheme-main);
}
</style>