<template>
  <BTable
    :data="members"
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
    <BTableColumn v-slot="{ row: member }: { row: CollectionMemberData; index: number }">
      <template v-if="tableType === 'accepted'">
        {{ member.position }} <BIcon icon="grip" class="is-pulled-right" />
      </template>
      <template v-else-if="tableType === 'searched'">
        <BButton
          type="is-success is-light"
          size="is-small"
          @click.prevent="
            $emit('createCollectionMember', {
              chapterId: member.chapter?.chapterId.toString(),
              fictionId: member.fiction?.fanfictionId.toString(),
              collectionId: member.collection?.collectionId.toString(),
            })
          "
          ><BIcon icon="plus" icon-pack="fas"
        /></BButton>
      </template>
      <template v-else-if="tableType === 'suggested'">
        <BButton
          type="is-success is-light"
          size="is-small"
          @click.prevent="$emit('acceptCollectionMember', member.memberId.toString())"
          ><BIcon icon="plus" icon-pack="fas"
        /></BButton>
      </template>
    </BTableColumn>
    <BTableColumn label="Titre" :searchable="tableType === 'searched'">
      <template #default="{ row: member }: { row: CollectionMemberData }">
        {{ member.title }}
      </template>
      <template #searchable>
        <BInput v-model="searchMemberFilters!.title" :lazy="true" type="search" placeholder="Filtrer par titre"
      /></template>
    </BTableColumn>
    <BTableColumn label="Type" :searchable="tableType === 'searched'">
      <template #default="{ row: member }: { row: CollectionMemberData }">
        {{ member.memberType }}
      </template>
      <template #searchable>
        <BSelect v-model="searchMemberFilters!.types">
          <option :value="Object.values(MemberType)">Tous</option>
          <option v-for="[key, value] in Object.entries(MemberType)" :key="key" :value="[value]">
            {{ value }}
          </option>
        </BSelect>
      </template>
    </BTableColumn>
    <BTableColumn label="Auteur•ice" :searchable="tableType === 'searched'">
      <template #default="{ row: member }: { row: CollectionMemberData }">
        {{ (member.chapter || member.fiction || member.collection)?.authors?.map((a) => a.username).join(", ") }}
      </template>
      <template #searchable>
        <BAutocomplete
          v-model="searchMemberFilters!.creationUsername"
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
    <template #detail="{ row: member }: { row: CollectionMemberData }">
      <article>
        <template v-if="member.chapter">
          <div>
            Chapitre {{ member.chapter.order! + 1 }} de la fiction {{ member.chapter.fiction!.title }} par
            {{ member.chapter.authors?.map((a) => a.username).join(",") }}
            <NuxtLink
              :to="{
                name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
                params: {
                  fictionId: member.chapter.fiction!.fanfictionId,
                  fictionTitle: member.chapter.fiction!.titleAsSlug,
                  chapterId: member.chapter.chapterId,
                  chapterTitle: member.chapter.titleAsSlug,
                },
              }"
              no-prefetch
              target="_blank"
            >
              <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
            </NuxtLink>
          </div>
        </template>
        <template v-else-if="member.fiction">
          <div>
            Fiction de {{ member.fiction.chapterCount }} chapitre{{ member.fiction.chapterCount! > 1 ? "s" : "" }} par
            {{ member.fiction.authors?.map((a) => a.username).join(",") }}
            <NuxtLink
              :to="{
                name: 'fictions-fictionId-fictionTitle-sommaire',
                params: {
                  fictionId: member.fiction.fanfictionId,
                  fictionTitle: member.fiction.titleAsSlug,
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
        <template v-else-if="member.collection">
          <div>
            Série par {{ member.collection.authors?.map((a) => a.username).join(",") }} contenant
            {{ member.collection.memberCount }} élément{{ member.collection.memberCount! > 1 ? "s" : "" }}
          </div>
          <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
          <div>Caractéristiques: --, --, --, -- Fandoms: --, --, --, --</div>
        </template>
        <template v-if="tableType === 'accepted'">
          <div>Ajouté par {{ member.additionUser?.username }} le {{ member.additionDate?.toLocaleDateString() }}</div>
          <div>
            <BButton
              size="is-small"
              type="is-danger is-light"
              @click.prevent="$emit('deleteCollectionMember', member.memberId)"
              >Retirer</BButton
            >
          </div>
        </template>
        <template v-else-if="tableType === 'suggested'">
          <div>Suggéré par {{ member.additionUser?.username }} le {{ member.additionDate?.toLocaleDateString() }}</div>
          <div>
            <BButton
              size="is-small"
              type="is-danger is-light"
              @click.prevent="$emit('deleteCollectionMember', member.memberId)"
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
import { type CollectionMemberData, MemberType } from "~/types/fanfictions";
import type { UserFilters, SearchMemberTypeFilter, CollectionMemberInput } from "#gql";
import type { UserData } from "~/types/users";

interface Props {
  tableType: "accepted" | "searched" | "suggested";
  members: CollectionMemberData[];
  searchedUsers?: UserData[];
}
interface Emits {
  (e: "createCollectionMember", collectionMemberData: CollectionMemberInput): void;
  (e: "acceptCollectionMember" | "deleteCollectionMember", collectionMemberId: string): void;
  (e: "moveCollectionMember", collectionMemberId: string, newPosition: number): void;
}

const { tableType, members } = defineProps<Props>();
const emit = defineEmits<Emits>();
const searchMemberFilters = defineModel<SearchMemberTypeFilter>("searchMemberFilters");
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
    const collectionMemberId = members.find((m) => m.order === draggingRowIndex.value);
    if (collectionMemberId) {
      emit("moveCollectionMember", collectionMemberId.memberId, payload.index);
    }
    draggingRowIndex.value = null;
  }
}
</script>
