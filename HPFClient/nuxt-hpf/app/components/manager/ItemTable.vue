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
          <option :value="Object.values(itemType)">Tous</option>
          <option v-for="[key, value] in Object.entries(itemType)" :key="key" :value="[value]">
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
        <template v-if="item.chapter">
          <div>
            Chapitre {{ item.chapter.order! + 1 }} de la fiction {{ item.chapter.fiction!.title }} par
            {{ item.chapter.authors?.map((a) => a.username).join(",") }}
            <NuxtLink
              :to="{
                name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
                params: {
                  fictionId: item.chapter.fiction!.fanfictionId,
                  fictionTitle: item.chapter.fiction!.titleAsSlug,
                  chapterId: item.chapter.chapterId,
                  chapterTitle: item.chapter.titleAsSlug,
                },
              }"
              no-prefetch
              target="_blank"
            >
              <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
            </NuxtLink>
          </div>
        </template>
        <template v-else-if="item.fiction">
          <div>
            Fiction de {{ item.fiction.chapterCount }} chapitre{{ item.fiction.chapterCount! > 1 ? "s" : "" }} par
            {{ item.fiction.authors?.map((a) => a.username).join(",") }}
            <NuxtLink
              :to="{
                name: 'fictions-fictionId-fictionTitle-sommaire',
                params: {
                  fictionId: item.fiction.fanfictionId,
                  fictionTitle: item.fiction.titleAsSlug,
                },
              }"
              no-prefetch
              target="_blank"
            >
              <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
            </NuxtLink>
          </div>
          <div>Caractéristiques: --, --, --, -- Fandoms: --, --, --, --</div>
        </template>
        <template v-else-if="item.collection">
          <div>
            Série par {{ item.collection.authors?.map((a) => a.username).join(",") }} contenant
            {{ item.collection.itemCount }} élément{{ item.collection.itemCount! > 1 ? "s" : "" }}
          </div>
          <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
          <div>Caractéristiques: --, --, --, -- Fandoms: --, --, --, --</div>
        </template>
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
import { type CollectionItemData, itemType } from "~/types/fanfictions";
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
