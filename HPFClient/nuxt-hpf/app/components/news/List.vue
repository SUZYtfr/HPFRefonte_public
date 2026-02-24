<template>
  <div :class="[{ card: isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <BLoading v-model="listLoading" :is-full-page="false" />
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
        <BButton v-if="showRefreshButton" type="is-primary" icon-left="redo-alt" @click="execute">
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
import type { NewsModel } from "@/models";

const {
  isCard = true,
  paginatedNews,
  showRefreshButton = true,
  isLoading = false,
  newsPagination,
  newsOrder,
  execute,
} = defineProps<{
  isCard?: boolean;
  showRefreshButton?: boolean;
  isLoading?: boolean;
  paginatedNews: Omit<NewsArticleTypeOffsetPaginated, "results"> & { results: NewsModel[] };
  newsPagination: OffsetPaginationInput;
  newsOrder: NewsArticleOrder;
  execute: () => Promise<void>;
}>();

const listLoading = computed<boolean>(() => isLoading);

const emit = defineEmits(["paginationChange", "orderChange"]);

const newsResultLabel = computed<string>(() => {
  let result = "Aucun résultat";
  if (!paginatedNews || paginatedNews?.totalCount === 0) return result;
  result = paginatedNews.totalCount.toString() + " résultat";
  result += paginatedNews.totalCount > 1 ? "s" : "";
  return result;
});

// Transforme le système offset / limit en page / pageSize
const pageNewsPagination = reactive({
  pageSize: newsPagination.limit!,
  page: newsPagination.offset! / newsPagination.limit! + 1,
});
watch(pageNewsPagination, () => {
  const pagination: OffsetPaginationInput = {
    limit: pageNewsPagination.pageSize,
    offset: (pageNewsPagination.page - 1) * pageNewsPagination.pageSize,
  };
  emit("paginationChange", pagination);
});

// TODO très moche
const newsOrderChoice = computed<string>({
  get() {
    if (newsOrder.postDate === Ordering.DESC) {
      return "most_recent";
    } else {
      return "less_recent";
    }
  },
  set(value: string) {
    const order: NewsArticleOrder = {};
    if (value === "most_recent") {
      order.postDate = Ordering.DESC;
    } else {
      order.postDate = Ordering.ASC;
    }
    emit("orderChange", order);
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
