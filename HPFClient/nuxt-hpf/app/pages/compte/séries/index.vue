<template>
  <div class="container">
    <div class="card">
      <BTable
        :loading="collectionStatus === 'pending'"
        :data="collections.results"
        :backend-sorting="true"
        :default-sort="Object.keys(collectionOrder).find((fo) => fo)"
        :default-sort-direction="Object.entries(collectionOrder).find((fo) => fo[1])![1]!"
        :backend-pagination="true"
        :paginated="true"
        :pagination-simple="true"
        :per-page="pagination.limit!"
        :total="collections.totalCount"
        custom-detail-row
        detailed
        detail-key="collectionId"
        @details-open="async (row: CollectionModel) => (row.items = await getItems(row.collectionId.toString()))"
        @page-change="(page: number | string) => (pagination.offset = (Number(page) - 1) * pagination.limit!)"
        @sort="
          (field: string | undefined, order: 'asc' | 'desc') => {
            const ordering = order.toUpperCase() as Ordering;
            collectionOrder.title = field === 'title' ? ordering : undefined;
            collectionOrder.reviewCount = field === 'reviewCount' ? ordering : undefined;
            collectionOrder.average = field === 'average' ? ordering : undefined;
          }
        "
      >
        <BTableColumn v-slot="{ row: collection }: { row: CollectionModel }" field="title" label="Titre" sortable>
          {{ collection.title }} <BTag class="is-pulled-right">{{ Object.fromEntries(Object.entries(CollectionAccess))[collection.access!] }}</BTag>
        </BTableColumn>
        <!-- TODO dont ràr -->
        <BTableColumn
          v-slot="{ row: collection }: { row: CollectionModel }"
          field="reviewCount"
          label="Reviews"
          sortable
        >
          {{ collection.reviewCount }}
        </BTableColumn>
        <BTableColumn v-slot="{ row: collection }: { row: CollectionModel }" field="average" label="Notation" sortable>
          <BRate v-if="collection.average" v-model="collection.average" disabled :max="1" rtl show-score />
        </BTableColumn>
        <BTableColumn>
          <template #default="{ row: collection }: { row: CollectionModel }">
            <NuxtLink
              :to="{
                name: 'compte-séries-écritoire',
                query: {
                  série: collection.collectionId,
                },
              }"
              no-prefetch
            >
              <BButton size="is-small is-light">Modifier</BButton>
            </NuxtLink>
          </template>
          <template #header>
            <NuxtLink
              :to="{
                name: 'compte-séries-écritoire',
              }"
              no-prefetch
            >
              <BButton size="is-small is-success">Ajouter</BButton>
            </NuxtLink>
          </template>
        </BTableColumn>
        <template #detail="{ row: collection }: { row: CollectionModel }">
          <tr v-for="item in collection.items" :key="item.id">
            <td class="has-text-centered">{{ item.position }}</td>
            <td>
              {{ item.title }}<BTag class="is-pulled-right">{{ item.itemType }}</BTag>
            </td>
            <td>
              {{ item.reviewCount }}
            </td>
            <td>
              <BRate v-if="item.average" v-model="item.average" disabled :max="1" rtl show-score />
            </td>
            <td></td>
          </tr>
          <tr>
            <td></td>
            <td colspan="3" class="has-text-centered">
              <!-- <NuxtLink
                :to="{
                  name: 'écritoire',
                  query: {
                    fiction: fiction.fanfictionId,
                    chapitre: '',
                  },
                }"
                no-prefetch
              > -->
              <BButton size="is-small" expanded>Ajouter un élément</BButton>
              <!-- </NuxtLink> -->
            </td>
          </tr>
        </template>
      </BTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BTable, BTableColumn, BButton, BRate, BTag } from "buefy";
import { CollectionModel } from "~/models";
import { CollectionAccess, CollectionItemData } from "~/types/fanfictions";
import { plainToInstance } from "class-transformer";
import { Ordering, type CollectionOrder, type OffsetPaginationInput /* CollectionFilters */ } from "#gql/default";

definePageMeta({
  auth: true,
});

const pagination = reactive<OffsetPaginationInput>({
  limit: 20,
  offset: 0,
});

const collectionOrder = reactive<CollectionOrder>({
  title: Ordering.ASC,
  reviewCount: undefined,
  average: undefined,
});

const { data: collections, status: collectionStatus } = await useAsyncGql(
  "getPrivateCollections",
  {
    // filters: fictionFilters,
    pagination: pagination,
    order: collectionOrder,
  },
  {
    transform: (input) => {
      return {
        ...input.privateCollections,
        results: plainToInstance(CollectionModel, input.privateCollections.results),
      };
    },
  },
);

async function getItems(collectionId: string): Promise<CollectionItemData[]> {
  const collection = await GqlGetPrivateCollectionItems({
    collectionId: collectionId,
  });
  return plainToInstance(CollectionItemData, collection.privateCollection.items);
}
</script>
