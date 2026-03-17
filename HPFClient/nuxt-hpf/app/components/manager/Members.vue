<template>
  <div class="card">
    <div class="card-content">
      <div class="panel">
        <div class="panel-heading">Éléments</div>
        <ManagerMemberTable
          :table-type="'accepted'"
          :members="members.filter((m) => m.isAccepted)"
          @move-collection-member="
            (collectionMemberId, newPosition) => $emit('moveCollectionMember', collectionMemberId, newPosition)
          "
          @delete-collection-member="(collectionMemberId) => $emit('deleteCollectionMember', collectionMemberId)"
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
          searchMemberFilters.title = ''; /* déclenche le watcher pour faire le premier appel*/
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
        <ManagerMemberTable
          :table-type="'searched'"
          :members="searchedMembers"
          :searched-users
          :search-member-filters
          :search-user-filters
          @create-collection-member="(collectionMemberData) => $emit('createCollectionMember', collectionMemberData)"
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
              <BTag type="is-info is-light">{{ members.filter((m) => !m.isAccepted).length }}</BTag>
            </p>
          </div>
        </template>
        <ManagerMemberTable
          :table-type="'suggested'"
          :members="members.filter((m) => !m.isAccepted)"
          @accept-collection-member="(collectionMemberId) => $emit('acceptCollectionMember', collectionMemberId)"
          @delete-collection-member="(collectionMemberId) => $emit('deleteCollectionMember', collectionMemberId)"
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
import type { CollectionMemberData } from "~/types/fanfictions";
import type { SearchMemberTypeFilter, UserFilters, CollectionMemberInput } from "#gql";
import type { UserData } from "~/types/users";

interface Props {
  searchedMembers: CollectionMemberData[];
  searchedUsers: UserData[];
  members: CollectionMemberData[];
}
interface Emits {
  (e: "clickPrevious"): void;
  (e: "createCollectionMember", collectionMemberData: CollectionMemberInput): void;
  (e: "acceptCollectionMember" | "deleteCollectionMember", collectionMemberId: string): void;
  (e: "moveCollectionMember", collectionMemberId: string, newPosition: number): void;
}

const { searchedMembers, searchedUsers, members } = defineProps<Props>();
defineEmits<Emits>();

const openPanel = ref<"search" | "suggestions" | null>(null);

const searchMemberFilters = defineModel<SearchMemberTypeFilter>("searchMemberFilters", { required: true });
const searchUserFilters = defineModel<UserFilters>("searchUserFilters", { required: true });
</script>
