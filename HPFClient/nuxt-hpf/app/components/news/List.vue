<template>
  <div :class="[{ card: isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <BLoading v-model="isLoading" :is-full-page="false" />
    <header
      :class="[
        { 'card-header': isCard },
        'p-2',
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
        'is-white',
      ]"
    >
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <BButton v-if="showRefreshButton" type="is-primary" icon-left="redo-alt" @click="searchNews">
          <span class="is-italic">
            {{ newsResultLabel }}
          </span>
        </BButton>
      </div>
      <div class="is-flex-shrink-5">
        <BField label="Ordre de tri" label-position="on-border" custom-class="has-text-primary">
          <BSelect
            v-model="newsOrderChoice"
            placeholder="Trier par"
            icon="sort"
            expanded
            @update:model-value="(order: string) => (newsOrderChoice = order)"
          >
            <option value="most_recent">Plus récent au plus ancien</option>
            <option value="less_recent">Plus ancien au plus récent</option>
          </BSelect>
        </BField>
      </div>
    </header>
    <div :class="[{ 'card-content': isCard }, 'p-2', 'is-flex-grow-5']">
      <div v-if="(paginatedNews?.results?.length ?? 0) == 0" class="mx-auto my-auto has-text-centered">
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <div>
          <NewsEntity2
            v-for="(item, innerindex) of paginatedNews?.results"
            :key="'news_' + item.newsId.toString()"
            :class="['mb-2', { 'is-color-even': innerindex % 2 != 0 }, { 'is-color-odd': innerindex % 2 == 0 }]"
            :news="item"
            :index="innerindex"
          />
        </div>
      </div>
    </div>
    <footer :class="[{ 'card-footer': isCard }]">
      <BPagination
        v-model="pageNewsPagination.page"
        :class="[{ 'card-footer-item': isCard }, 'py-2']"
        :total="paginatedNews.totalCount"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="pageNewsPagination.pageSize"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
        @change="(page: number) => (pageNewsPagination.page = page)"
      />
    </footer>
  </div>
</template>

<script setup lang="ts">
import type { NewsArticleOrder, NewsArticleTypeOffsetPaginated, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
import type { NewsModel } from "~/models";

interface Props {
  isCard?: boolean;
  showRefreshButton?: boolean;
  paginatedNews: Omit<NewsArticleTypeOffsetPaginated, "results"> & { results: NewsModel[] };
  searchNews: () => Promise<void>;
}

const { isCard = true, paginatedNews, showRefreshButton = true, searchNews } = defineProps<Props>();

const pagination = defineModel<OffsetPaginationInput>("pagination", { required: true });
const order = defineModel<NewsArticleOrder>("order", { required: true });
const isLoading = defineModel<boolean>("isLoading", { required: false, default: false });

const newsResultLabel = computed<string>(() => {
  let result = "Aucun résultat";
  if (!paginatedNews || paginatedNews?.totalCount === 0) return result;
  result = paginatedNews.totalCount.toString() + " résultat";
  result += paginatedNews.totalCount > 1 ? "s" : "";
  return result;
});

// Transforme le système offset / limit en page / pageSize
const pageNewsPagination = reactive({
  pageSize: pagination.value.limit!,
  page: pagination.value.offset! / pagination.value.limit! + 1,
});
watch(pageNewsPagination, () => {
  pagination.value.limit = pageNewsPagination.pageSize;
  pagination.value.offset = (pageNewsPagination.page - 1) * pageNewsPagination.pageSize;
});

// TODO très moche
const newsOrderChoice = computed<string>({
  get() {
    if (order.value.postDate === Ordering.DESC) {
      return "most_recent";
    } else {
      return "less_recent";
    }
  },
  set(value: string) {
    if (value === "most_recent") {
      order.value.postDate = Ordering.DESC;
    } else {
      order.value.postDate = Ordering.ASC;
    }
  },
});
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
.card-header {
  background-color: var(--scheme-main);
}
</style>
