<template>
  <div class="container">
    <div class="card">
      <BTabs
        v-model="activeTab"
        :animated="false"
        @update:model-value="
          (value?: string | number | null) =>
            (fictionFilters.fandoms = value ? { id: { exact: value.toString() } } : undefined)
        "
      >
        <BTabItem v-for="{ id, name } of fandomTabs" :key="id" :value="id" :label="name">
          <BTable
            :loading="fictionStatus === 'pending'"
            :data="fictions.results"
            :backend-sorting="true"
            :default-sort="Object.keys(fictionOrder).find((fo) => fo)"
            :default-sort-direction="Object.entries(fictionOrder).find((fo) => fo[1])![1]!"
            :backend-pagination="true"
            :paginated="true"
            :pagination-simple="true"
            :per-page="pagination.limit!"
            :total="fictions.totalCount"
            custom-detail-row
            detailed
            detail-key="fanfictionId"
            @details-open="
              async (row: FanfictionModel) => (row.chapters = await getChapters(row.fanfictionId.toString()))
            "
            @page-change="(page: number | string) => (pagination.offset = (Number(page) - 1) * pagination.limit!)"
            @sort="
              (field: string | undefined, order: 'asc' | 'desc') => {
                const ordering = (order.toUpperCase() + (includeUnpublished ? '_NULLS_FIRST' : '')) as Ordering;
                fictionOrder.title = field === 'title' ? ordering : undefined;
                fictionOrder.lastUpdateDate = field === 'lastUpdateDate' ? ordering : undefined;
                fictionOrder.reviewCount = field === 'reviewCount' ? ordering : undefined;
                fictionOrder.readCount = field === 'readCount' ? ordering : undefined;
              }
            "
          >
            <BTableColumn v-slot="{ row: fiction }: { row: FanfictionModel }" field="title" label="Titre" sortable>
              {{ fiction.title }}
            </BTableColumn>
            <BTableColumn
              v-slot="{ row: fiction }: { row: FanfictionModel }"
              field="lastUpdateDate"
              label="Dernière mise-à-jour"
              sortable
            >
              {{ fiction.lastUpdateDate?.toLocaleDateString("fr-fr") || "Non publiée" }}
            </BTableColumn>
            <BTableColumn v-slot="{ row: fiction }: { row: FanfictionModel }" field="reviewCount" label="Reviews" sortable>
              {{ fiction.reviewCount }}{{ fiction.average ? " (" + fiction.average?.toFixed(1).toString() + "/10)" : "" }}
            </BTableColumn>
            <BTableColumn v-slot="{ row: fiction }: { row: FanfictionModel }" field="readCount" label="Lectures" sortable>
              {{ fiction.readCount }}
            </BTableColumn>
            <BTableColumn>
              <template #default="{ row: fiction }: { row: FanfictionModel }">
                <NuxtLink
                  :to="{
                    name: 'écritoire',
                    query: {
                      fiction: fiction.fanfictionId,
                    },
                  }"
                  no-prefetch
                  ><BButton size="is-small is-light">Modifier</BButton></NuxtLink
                >
              </template>
              <template #header>
                <NuxtLink
                  :to="{
                    name: 'écritoire',
                    query: activeTab
                      ? {
                          fandom: activeTab,
                        }
                      : undefined,
                  }"
                  no-prefetch
                  ><BButton size="is-small is-success">Nouveau</BButton></NuxtLink
                >
              </template>
            </BTableColumn>
            <template #detail="{ row: fiction }: { row: FanfictionModel }">
              <tr v-for="chapter in fiction.chapters" :key="chapter.chapterId">
                <td class="has-text-centered">{{ chapter.order }}</td>
                <td>{{ chapter.title }}</td>
                <td>{{ chapter.publicationDate?.toLocaleDateString("fr-fr") || "Brouillon" }}</td>
                <td>
                  {{ chapter.reviewCount
                  }}{{ chapter.average ? " (" + chapter.average?.toFixed(1).toString() + "/10)" : "" }}
                </td>
                <td>{{ chapter.readCount }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      name: 'écritoire',
                      query: {
                        chapitre: chapter.chapterId,
                      },
                    }"
                    no-prefetch
                    ><BButton size="is-small is-light">Modifier</BButton></NuxtLink
                  >
                </td>
              </tr>
            </template>
            <template #bottom-left>
              <BSwitch
                v-model="includeUnpublished"
                @update:model-value="
                  (value: boolean) => (fictionFilters.lastUpdateDate = value ? undefined : { isNull: false })
                "
              >
                Inclure les fictions non publiées
              </BSwitch>
            </template>
          </BTable>
        </BTabItem>
      </BTabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BTable, BTableColumn, BButton, BTabs, BTabItem, BSwitch } from "buefy";
import { ChapterModel, FanfictionModel } from "@/models";
import { plainToInstance } from "class-transformer";
import { Ordering, type FictionOrder, type OffsetPaginationInput, type FictionFilters } from "#gql/default";

definePageMeta({
  auth: true,
});

const { payloadData } = useCustomAuth();

// TODO - en faire un paramètre de profileData
const { fandoms } = useConfigStore();
const preferredFandoms = fandoms!.filter((f) => payloadData.value?.preferred5Fandoms?.includes(Number(f.id)));

interface FandomTab {
  id: string;
  name: string;
}

const fandomTabs: FandomTab[] = [
  {
    id: "",
    name: "Tous fandoms",
  },
].concat(preferredFandoms);

const activeTab = ref<string>(fandomTabs[0]!.id);
const includeUnpublished = ref<boolean>(true);

const fictionFilters = reactive<FictionFilters>({
  fandoms: { id: undefined },
  lastUpdateDate: undefined,
});

const pagination = reactive<OffsetPaginationInput>({
  limit: 20,
  offset: 0,
});

// TODO option pour cacher les fictions non publiées ?
const fictionOrder = reactive<FictionOrder>({
  lastUpdateDate: Ordering.DESC_NULLS_FIRST,
  title: undefined,
  reviewCount: undefined,
  readCount: undefined,
});

const { data: fictions, status: fictionStatus } = await useAsyncGql(
  "getPrivateFictions",
  {
    filters: fictionFilters,
    pagination: pagination,
    order: fictionOrder,
  },
  {
    transform: (input) => {
      return {
        ...input.privateFictions,
        results: plainToInstance(FanfictionModel, input.privateFictions.results),
      };
    },
  },
);

async function getChapters(fictionId: string): Promise<ChapterModel[]> {
  const chapters = await GqlGetPrivateChapters({
    filters: {
      fiction: {
        id: { exact: fictionId },
      },
    },
  });
  return plainToInstance(ChapterModel, chapters.privateChapters.results);
}
</script>
