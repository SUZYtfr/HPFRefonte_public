<template>
  <BTable
    :data="items"
    detailed
    detail-key="position"
    :draggable="tableType === 'accepted'"
    :paginated="tableType === 'accepted'"
    backend-filtering
    @dragstart="dragstart"
    @dragover="dragover"
    @dragleave="dragleave"
    @drop="drop"
  >
    <BTableColumn v-slot="{ row: item }: { row: CollectionItemData; index: number }">
      <template v-if="tableType === 'accepted'">
        {{ item.position }} <BIcon icon="grip" class="is-pulled-right" />
      </template>
      <template v-else-if="tableType === 'searched'">
        <BButton
          type="is-success is-light"
          size="is-small"
          @click.prevent="
            $emit('createCollectionItem', {
              chapterId: item.chapter?.chapterId.toString(),
              fictionId: item.fiction?.fanfictionId.toString(),
              collectionId: item.collection?.collectionId.toString(),
            })
          "
          ><BIcon icon="plus" icon-pack="fas"
        /></BButton>
      </template>
      <template v-else-if="tableType === 'suggested'">
        <BButton
          type="is-success is-light"
          size="is-small"
          @click.prevent="$emit('acceptCollectionItem', item.itemId.toString())"
          ><BIcon icon="plus" icon-pack="fas"
        /></BButton>
      </template>
    </BTableColumn>
    <BTableColumn label="Titre" :searchable="tableType === 'searched'">
      <template #default="{ row: item }: { row: CollectionItemData }">
        {{ item.title }}
      </template>
      <template #searchable>
        <BInput v-model="searchItemFilters!.title" :lazy="true" type="search" placeholder="Filtrer par titre"
      /></template>
    </BTableColumn>
    <BTableColumn label="Type" :searchable="tableType === 'searched'">
      <template #default="{ row: item }: { row: CollectionItemData }">
        {{ item.itemType }}
      </template>
      <template #searchable>
        <BSelect v-model="searchItemFilters!.types">
          <option :value="Object.values(ItemType)">Tous</option>
          <option v-for="[key, value] in Object.entries(ItemType)" :key="key" :value="[value]">
            {{ value }}
          </option>
        </BSelect>
      </template>
    </BTableColumn>
    <BTableColumn label="Auteur•ice" :searchable="tableType === 'searched'">
      <template #default="{ row: item }: { row: CollectionItemData }">
        {{ (item.chapter || item.fiction || item.collection)?.authors?.map((a) => a.username).join(", ") }}
      </template>
      <template #searchable>
        <BAutocomplete
          v-model="searchItemFilters!.creationUsername"
          type="search"
          :data="searchedUsers"
          field="username"
          keep-first
          placeholder="Rechercher par auteur•ices"
          @typing="
            (value) => {
              searchUserFilters!.username!.iContains = value as string;
            }
          "
        >
          <template #empty>Aucun résultat</template>
        </BAutocomplete>
      </template>
    </BTableColumn>
    <template #detail="{ row: item }: { row: CollectionItemData }">
      <article>
        <ChapterItem v-if="item.chapter" :chapter="item.chapter" />
        <FictionItem v-else-if="item.fiction" :fiction="item.fiction" />
        <CollectionItem v-else-if="item.collection" :collection="item.collection" />
        <template v-if="tableType === 'accepted'">
          <div>Ajouté par {{ item.additionUser?.username }} le {{ item.additionDate?.toLocaleDateString() }}</div>
          <div>
            <BButton
              size="is-small"
              type="is-danger is-light"
              @click.prevent="$emit('deleteCollectionItem', item.itemId)"
              >Retirer</BButton
            >
          </div>
        </template>
        <template v-else-if="tableType === 'suggested'">
          <div>Suggéré par {{ item.additionUser?.username }} le {{ item.additionDate?.toLocaleDateString() }}</div>
          <div>
            <BButton
              size="is-small"
              type="is-danger is-light"
              @click.prevent="$emit('deleteCollectionItem', item.itemId)"
              >Rejeter</BButton
            >
          </div>
        </template>
      </article>
    </template>
    <template #empty>
      <div class="has-text-centered">
        <template v-if="tableType === 'accepted'">Aucun élément n'a encore été ajouté</template>
        <template v-else-if="tableType === 'searched'">Aucun résultat</template>
        <template v-else-if="tableType === 'suggested'">Aucune suggestion</template>
      </div>
    </template>
  </BTable>
</template>

<script setup lang="ts">
import { BTable, BTableColumn, BButton, BAutocomplete, BIcon, type TableRowDragEvent } from "buefy";
import { type CollectionItemData, ItemType } from "~/types/fanfictions";
import type { UserFilters, SearchItemTypeFilter, CollectionItemInput } from "#gql";
import type { UserData } from "~/types/users";

interface Props {
  tableType: "accepted" | "searched" | "suggested";
  items: CollectionItemData[];
  searchedUsers?: UserData[];
}
interface Emits {
  (e: "createCollectionItem", collectionItemData: CollectionItemInput): void;
  (e: "acceptCollectionItem" | "deleteCollectionItem", collectionItemId: string): void;
  (e: "moveCollectionItem", collectionItemId: string, newPosition: number): void;
}

const { tableType, items } = defineProps<Props>();
const emit = defineEmits<Emits>();
const searchItemFilters = defineModel<SearchItemTypeFilter>("searchItemFilters");
const searchUserFilters = defineModel<UserFilters>("searchUserFilters");

const draggingRowIndex = ref<number | null>(null);

function dragstart(payload: TableRowDragEvent): void {
  if (tableType === "accepted") {
    draggingRowIndex.value = payload.index;
    payload.event.dataTransfer!.effectAllowed = "move";
  }
}
function dragover(payload: TableRowDragEvent): void {
  if (tableType === "accepted") {
    payload.event.dataTransfer!.dropEffect = "move";
    (payload.event.target as Element).closest("tr")!.classList.add("is-selected");
    payload.event.preventDefault();
  }
}
function dragleave(payload: TableRowDragEvent): void {
  if (tableType === "accepted") {
    (payload.event.target as Element).closest("tr")!.classList.remove("is-selected");
    payload.event.preventDefault();
  }
}
function drop(payload: TableRowDragEvent): void {
  if (tableType === "accepted") {
    (payload.event.target as Element).closest("tr")!.classList.remove("is-selected");
    const collectionItemId = items.find((m) => m.order === draggingRowIndex.value);
    if (collectionItemId) {
      emit("moveCollectionItem", collectionItemId.itemId, payload.index);
    }
    draggingRowIndex.value = null;
  }
}
</script>
