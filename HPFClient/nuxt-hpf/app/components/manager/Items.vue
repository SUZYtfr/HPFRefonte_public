<template>
  <div class="card">
    <div class="card-content">
      <div class="panel">
        <div class="panel-heading">Éléments</div>
        <ManagerItemTable
          :table-type="'accepted'"
          :items="items.filter((m) => m.isAccepted)"
          @move-collection-item="
            (collectionItemId, newPosition) => $emit('moveCollectionItem', collectionItemId, newPosition)
          "
          @delete-collection-item="(collectionItemId) => $emit('deleteCollectionItem', collectionItemId)"
        />
      </div>
    </div>
    <div class="card-content">
      <!-- Recherche -->
      <BCollapse
        :model-value="openPanel === 'search'"
        class="panel"
        @open="
          openPanel = 'search';
          searchItemFilters.title = ''; /* déclenche le watcher pour faire le premier appel*/
        "
      >
        <template #trigger>
          <div
            class="panel-heading"
            role="button"
            aria-controls="contentIdForA11y2"
            :aria-expanded="openPanel === 'search'"
          >
            <p>Ajouter de nouveaux éléments</p>
          </div>
        </template>
        <ManagerItemTable
          :table-type="'searched'"
          :items="searchedItems"
          :searched-users
          :search-item-filters="searchItemFilters"
          :search-user-filters
          @create-collection-item="(collectionItemData) => $emit('createCollectionItem', collectionItemData)"
        />
      </BCollapse>
      <!-- Propositions -->
      <BCollapse :model-value="openPanel === 'suggestions'" class="panel" @open="openPanel = 'suggestions'">
        <template #trigger>
          <div
            class="panel-heading"
            role="button"
            aria-controls="contentIdForA11y2"
            :aria-expanded="openPanel === 'suggestions'"
          >
            <p>
              Voir les propositions
              <BTag type="is-info is-light">{{ items.filter((m) => !m.isAccepted).length }}</BTag>
            </p>
          </div>
        </template>
        <ManagerItemTable
          :table-type="'suggested'"
          :items="items.filter((m) => !m.isAccepted)"
          @accept-collection-item="(collectionItemId) => $emit('acceptCollectionItem', collectionItemId)"
          @delete-collection-item="(collectionItemId) => $emit('deleteCollectionItem', collectionItemId)"
        />
      </BCollapse>
    </div>
  </div>
  <!-- Barre de navigation -->
  <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
    <BButton @click.prevent="$emit('clickPrevious')">Revenir à la série</BButton>
  </div>
</template>

<script setup lang="ts">
import { BButton, BTag, BCollapse } from "buefy";
import type { CollectionItemData } from "~/types/fanfictions";
import type { SearchItemTypeFilter, UserFilters, CollectionItemInput } from "#gql";
import type { UserData } from "~/types/users";

interface Props {
  searchedItems: CollectionItemData[];
  searchedUsers: UserData[];
  items: CollectionItemData[];
}
interface Emits {
  (e: "clickPrevious"): void;
  (e: "createCollectionItem", collectionItemData: CollectionItemInput): void;
  (e: "acceptCollectionItem" | "deleteCollectionItem", collectionItemId: string): void;
  (e: "moveCollectionItem", collectionItemId: string, newPosition: number): void;
}

const { searchedItems: searchedItems, searchedUsers, items } = defineProps<Props>();
defineEmits<Emits>();

const openPanel = ref<"search" | "suggestions" | null>(null);

const searchItemFilters = defineModel<SearchItemTypeFilter>("searchItemFilters", { required: true });
const searchUserFilters = defineModel<UserFilters>("searchUserFilters", { required: true });
</script>
