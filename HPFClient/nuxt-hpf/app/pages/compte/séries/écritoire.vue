<template>
  <div class="container px-5">
    <BSteps ref="steps" v-model="currentStep" :has-navigation="false">
      <BLoading v-model="pending" :is-full-page="false" />
      <BStepItem label="Série" step="collection" value="collection" icon-pack="fas" icon="book-open-reader">
        <LazyManagerCollection
          v-model:collection="collection"
          v-model:unsaved-changes="unsavedChanges"
          :is-editing
          @click-cancel="
            async () => {
              fetchCollection(collection.collectionId.toString());
              unsavedChanges = false;
            }
          "
          @click-next="steps?.next()"
          @create-collection="createCollection"
          @update-collection="updateCollection"
        />
      </BStepItem>
      <BStepItem
        label="Éléments"
        step="items"
        value="items"
        icon-pack="fas"
        :icon="itemsComplete ? 'square-check' : 'square'"
      >
        <LazyManagerItems
          :items="collection.items!"
          :search-item-filters
          :searched-items
          :search-user-filters
          :searched-users
          @click-previous="steps?.prev()"
          @create-collection-item="createCollectionItem"
          @accept-collection-item="acceptCollectionItem"
          @move-collection-item="moveCollectionItem"
          @delete-collection-item="deleteCollectionItem"
        />
      </BStepItem>
    </BSteps>
  </div>
</template>

<script setup lang="ts">
import { CollectionModel } from "~/models";
import { CollectionItemData, ItemType } from "~/types/fanfictions";
import { RecordStatusEnum } from "~/types/basics";
import { BSteps, BStepItem, BLoading } from "buefy";
import { plainToInstance } from "class-transformer";
import type { CollectionItemInput, SearchItemTypeFilter, UserFilters } from "#gql";
import { UserData } from "~/types/users";

definePageMeta({
  auth: true,
});

const route = useRoute();

const initialCollectionId = route.query["série"] as string | undefined;

const steps = useTemplateRef("steps");
const currentStep = ref<"collection" | "items">("collection");
const pending = ref<boolean>(false);
const isEditing = ref<boolean>(Boolean(initialCollectionId));
const itemsComplete = computed(() => true);
const unsavedChanges = ref<boolean>(false);

const collection = ref<CollectionModel>(
  new CollectionModel({
    recordStatus: RecordStatusEnum.New,
    items: [],
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

const searchedItems = ref<CollectionItemData[]>([]);
const searchItemFilters = reactive<SearchItemTypeFilter>({
  creationUsername: "Loutre", // TODO depuis profileData
  collectionId: collection.value.collectionId.toString(),
  title: null,
  types: Object.values(ItemType),
});
async function searchItems(): Promise<CollectionItemData[]> {
  const searchItems = await GqlSearchItems({
    filters: searchItemFilters,
  });
  searchedItems.value = plainToInstance(CollectionItemData, searchItems.itemtypeSearch);
  return searchedItems.value;
}
watch(searchItemFilters, () => searchItems());

async function createCollection(): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlCreateCollection({
      collectionData: {
        title: collection.value.title,
        summary: collection.value.summary!,
        access: collection.value.access!,
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
        access: collection.value.access!,
        fandoms: { set: collection.value.fandoms!.map((f) => f.id) },
        characteristics: { set: collection.value.characteristics!.map((c) => c.characteristicId.toString()) },
      },
    });
  } finally {
    pending.value = false;
  }
  return true;
}

async function createCollectionItem(collectionItemData: CollectionItemInput): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlCreateCollectionItem({
      collectionId: collection.value.collectionId.toString(),
      collectionItemData: collectionItemData,
    });
    collection.value.items = plainToInstance(CollectionItemData, data.createCollectionItem);
    searchItems(); // force la mise-à-jour de la recherche pour faire disparaître l'élément ajouté
  } finally {
    pending.value = false;
  }
  return true;
}

async function acceptCollectionItem(collectionItemId: string): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlAcceptCollectionItem({ collectionItemId: collectionItemId });
    collection.value.items = plainToInstance(CollectionItemData, data.acceptCollectionItem);
  } finally {
    pending.value = false;
  }
  return true;
}

async function moveCollectionItem(collectionItemId: string, position: number): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlMoveCollectionItem({ collectionItemId: collectionItemId, position: position });
    collection.value.items = plainToInstance(CollectionItemData, data.moveCollectionItem);
  } finally {
    pending.value = false;
  }
  return true;
}

async function deleteCollectionItem(collectionItemId: string): Promise<true> {
  pending.value = true;
  try {
    const data = await GqlDeleteCollectionItem({ collectionItemId: collectionItemId });
    collection.value.items = plainToInstance(CollectionItemData, data.deleteCollectionItem);
    searchItems(); // force la mise-à-jour de la recherche pour faire réapparaître l'élément ajouté
  } finally {
    pending.value = false;
  }
  return true;
}

useHead({
  title: "HPF - " + (isEditing.value ? "Modification de la série" : "Nouvelle série"),
});
</script>
