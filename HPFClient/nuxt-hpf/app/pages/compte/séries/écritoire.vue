<template>
  <div class="container px-5">
    <BSteps ref="steps" v-model="currentStep" :has-navigation="false">
      <BLoading v-model="pending" :is-full-page="false" />
      <BStepItem label="Série" step="collection" value="collection" icon-pack="fas" icon="book-open-reader">
        <LazyManagerCollection
          :is-editing
          :collection
          @click-cancel="fetchCollection(collection.collectionId.toString())"
          @click-next="steps?.next()"
          @create-collection="createCollection"
          @update-collection="updateCollection"
        />
      </BStepItem>
      <BStepItem
        label="Éléments"
        step="members"
        value="members"
        icon-pack="fas"
        :icon="membersComplete ? 'square-check' : 'square'"
      >
        <LazyManagerMembers
          :members="collection.members!"
          :search-member-filters
          :searched-members
          :search-user-filters
          :searched-users
          @click-previous="steps?.prev()"
          @create-collection-member="createCollectionMember"
          @accept-collection-member="acceptCollectionMember"
          @move-collection-member="moveCollectionMember"
          @delete-collection-member="deleteCollectionMember"
        />
      </BStepItem>
    </BSteps>
  </div>
</template>

<script setup lang="ts">
import { CollectionModel } from "~/models";
import { CollectionMemberData, MemberType } from "~/types/fanfictions";
import { RecordStatusEnum } from "~/types/basics";
import { BSteps, BStepItem, BLoading } from "buefy";
import { plainToInstance } from "class-transformer";
import type { CollectionMemberInput, SearchMemberTypeFilter, UserFilters } from "#gql";
import { UserData } from "~/types/users";

definePageMeta({
  auth: true,
});

const route = useRoute();

const initialCollectionId = route.query["série"] as string | undefined;

const steps = useTemplateRef("steps");
const currentStep = ref<"collection" | "members">("collection");
const pending = ref<boolean>(false);
const isEditing = ref<boolean>(Boolean(initialCollectionId));
const membersComplete = computed(() => true);

const collection = ref<CollectionModel>(
  new CollectionModel({
    recordStatus: RecordStatusEnum.New,
    members: [],
    fandoms: [],
    characteristics: [],
  }),
);
async function fetchCollection(collectionId: string): Promise<CollectionModel> {
  pending.value = true;
  try {
    const data = await GqlGetPrivateCollection({ collectionId: collectionId });
    collection.value = plainToInstance(CollectionModel, data.privateCollection);
  } finally {
    pending.value = false;
  }
  return collection.value;
}

// Fetch initial si le contexte initial est la modification
if (initialCollectionId) {
  await fetchCollection(initialCollectionId);
}

const searchedUsers = ref<UserData[]>([]);
const searchUserFilters = reactive<UserFilters>({
  username: { iContains: "" },
});
async function searchUsers(): Promise<UserData[]> {
  const searchUsers = await GqlSearchUsers({ filters: searchUserFilters });
  searchedUsers.value = plainToInstance(UserData, searchUsers.users.results);
  return searchedUsers.value;
}
watch(searchUserFilters, () => searchUsers());

const searchedMembers = ref<CollectionMemberData[]>([]);
const searchMemberFilters = reactive<SearchMemberTypeFilter>({
  creationUsername: "Loutre", // TODO depuis profileData
  collectionId: collection.value.collectionId.toString(),
  title: null,
  types: Object.values(MemberType),
});
async function searchMembers(): Promise<CollectionMemberData[]> {
  const searchMembers = await GqlSearchMembers({
    filters: searchMemberFilters,
  });
  searchedMembers.value = plainToInstance(CollectionMemberData, searchMembers.membertypeSearch);
  return searchedMembers.value;
}
watch(searchMemberFilters, () => searchMembers());

async function createCollection(): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlCreateCollection({
      collectionData: {
        title: collection.value.title,
        summary: collection.value.summary!,
        access: Number(collection.value.access!),
        fandoms: { set: collection.value.fandoms!.map((f) => f.id) },
        characteristics: { set: collection.value.characteristics!.map((c) => c.characteristicId.toString()) },
      },
    });
    collection.value.id = data.createCollection.id;
    isEditing.value = true;
  } finally {
    pending.value = false;
  }
  return true;
}

async function updateCollection(): Promise<true> {
  pending.value = true;
  try {
    await GqlUpdateCollection({
      collectionId: collection.value.collectionId.toString(),
      collectionData: {
        title: collection.value.title,
        summary: collection.value.summary!,
        access: Number(collection.value.access!),
        fandoms: { set: collection.value.fandoms!.map((f) => f.id) },
        characteristics: { set: collection.value.characteristics!.map((c) => c.characteristicId.toString()) },
      },
    });
  } finally {
    pending.value = false;
  }
  return true;
}

async function createCollectionMember(collectionMemberData: CollectionMemberInput): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlCreateCollectionMember({
      collectionId: collection.value.collectionId.toString(),
      collectionMemberData: collectionMemberData,
    });
    collection.value.members = plainToInstance(CollectionMemberData, data.createCollectionMember);
    searchMembers(); // force la mise-à-jour de la recherche pour faire disparaître l'élément ajouté
  } finally {
    pending.value = false;
  }
  return true;
}

async function acceptCollectionMember(collectionMemberId: string): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlAcceptCollectionMember({ collectionMemberId: collectionMemberId });
    collection.value.members = plainToInstance(CollectionMemberData, data.acceptCollectionMember);
  } finally {
    pending.value = false;
  }
  return true;
}

async function moveCollectionMember(collectionMemberId: string, position: number): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlMoveCollectionMember({ collectionMemberId: collectionMemberId, position: position });
    collection.value.members = plainToInstance(CollectionMemberData, data.moveCollectionMember);
  } finally {
    pending.value = false;
  }
  return true;
}

async function deleteCollectionMember(collectionMemberId: string): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlDeleteCollectionMember({ collectionMemberId: collectionMemberId });
    collection.value.members = plainToInstance(CollectionMemberData, data.deleteCollectionMember);
    searchMembers(); // force la mise-à-jour de la recherche pour faire réapparaître l'élément ajouté
  } finally {
    pending.value = false;
  }
  return true;
}

useHead({
  title: "HPF - " + (isEditing.value ? "Modification de la série" : "Nouvelle série"),
});
</script>
