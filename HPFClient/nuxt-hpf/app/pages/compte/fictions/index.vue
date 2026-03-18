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
                const ordering = order.toUpperCase() as Ordering;
                fictionOrder.title = field === 'title' ? ordering : undefined;
                fictionOrder.lastUpdateDate =
                  field === 'lastUpdateDate'
                    ? includeUnpublished
                      ? ((ordering + '_NULLS_FIRST') as Ordering)
                      : ordering
                    : undefined;
                fictionOrder.reviewCount = field === 'reviewCount' ? ordering : undefined;
                fictionOrder.readCount = field === 'readCount' ? ordering : undefined;
                fictionOrder.average = field === 'average' ? ordering : undefined;
              }
            "
          >
            <BTableColumn v-slot="{ row: fiction }: { row: FanfictionModel }" field="title" label="Titre" sortable>
              {{ fiction.title }}
            </BTableColumn>
            <BTableColumn
              v-slot="{ row: fiction }: { row: FanfictionModel }"
              field="lastUpdateDate"
              label="Dernière publication"
              sortable
            >
              {{ fiction.lastUpdateDate?.toLocaleDateString("fr-fr") || "Non publiée" }}
              <BTag class="is-pulled-right">{{ fiction.statusAsText }}</BTag>
            </BTableColumn>
            <!-- TODO dont ràr -->
            <BTableColumn
              v-slot="{ row: fiction }: { row: FanfictionModel }"
              field="reviewCount"
              label="Reviews"
              sortable
            >
              {{ fiction.reviewCount }}
            </BTableColumn>
            <BTableColumn v-slot="{ row: fiction }: { row: FanfictionModel }" field="average" label="Notation" sortable>
              <BRate v-if="fiction.average" v-model="fiction.average" disabled :max="1" rtl show-score />
            </BTableColumn>
            <BTableColumn
              v-slot="{ row: fiction }: { row: FanfictionModel }"
              field="readCount"
              label="Lectures"
              sortable
            >
              {{ fiction.readCount }}
            </BTableColumn>
            <BTableColumn>
              <template #default="{ row: fiction }: { row: FanfictionModel }">
                <NuxtLink
                  :to="{
                    name: 'compte-fictions-écritoire',
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
                    name: 'compte-fictions-écritoire',
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
                <td>
                  {{ chapter.publicationDate?.toLocaleDateString("fr-fr") || "Brouillon" }}
                  <!-- TODO statut de la dernière version (brouillon, publiée, non validée, etc.)-->
                  <!-- <BTag class="is-pulled-right">{{ chapter.validationStatus }}</BTag> -->
                </td>
                <td>
                  {{ chapter.reviewCount }}
                </td>
                <td>
                  <BRate v-if="chapter.average" v-model="chapter.average" disabled :max="1" rtl show-score />
                </td>
                <td>{{ chapter.readCount }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      name: 'compte-fictions-écritoire',
                      query: {
                        fiction: fiction.fanfictionId,
                        chapitre: chapter.chapterId,
                      },
                    }"
                    no-prefetch
                    ><BButton size="is-small is-light">Modifier</BButton></NuxtLink
                  >
                </td>
              </tr>
              <tr>
                <td></td>
                <td colspan="5" class="has-text-centered">
                  <NuxtLink
                    :to="{
                      name: 'compte-fictions-écritoire',
                      query: {
                        fiction: fiction.fanfictionId,
                        chapitre: '',
                      },
                    }"
                    no-prefetch
                  >
                    <BButton size="is-small" expanded>Nouveau chapitre</BButton>
                  </NuxtLink>
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
import { BTable, BTableColumn, BButton, BTabs, BTabItem, BSwitch, BRate, BTag } from "buefy";
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
// TODO filtres plus précis: fics à chapitres avec status nouvelle version
const includeUnpublished = ref<boolean>(true);

const fictionFilters = reactive<FictionFilters>({
  fandoms: { id: undefined },
  lastUpdateDate: undefined,
});

const pagination = reactive<OffsetPaginationInput>({
  limit: 20,
  offset: 0,
});

const fictionOrder = reactive<FictionOrder>({
  lastUpdateDate: Ordering.DESC_NULLS_FIRST,
  title: undefined,
  reviewCount: undefined,
  readCount: undefined,
  average: undefined,
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
