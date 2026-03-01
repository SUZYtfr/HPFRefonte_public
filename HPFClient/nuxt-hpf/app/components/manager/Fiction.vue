<template>
  <div class="card">
    <div class="card-content">
      <BField label="Titre">
        <BInput
          v-model="fiction.title"
          type="text"
          placeholder="Titre de la fiction"
          required
          @update:model-value="() => (unsavedChanges = true)"
        />
      </BField>
      <BField label="Statut">
        <BSelect v-model="fiction.status" required @update:model-value="() => (unsavedChanges = true)">
          <option v-for="[key, value] in Object.entries(FanfictionStatus)" :key="key" :value="key">
            {{ value }}
          </option>
        </BSelect>
      </BField>
      <BField label="Résumé">
        <CustomEditor
          v-model:text="fiction.summary"
          :config="{
            defaultValue: fiction.summary || '',
            showFooter: false,
            placeholder: '',
            fixedHeight: true,
            height: 200,
            canQuote: false,
            readOnly: false,
            quoteLimit: 0,
            fontSize: 100,
            oneLineToolbar: true,
            canUseImage: false,
          }"
          @update:text="() => (unsavedChanges = true)"
        />
      </BField>

      <BField label="Fandoms">
        <BTaginput
          v-model="selectedFandoms"
          field="name"
          ellipsis
          :allow-new="false"
          autocomplete
          :required="!selectedFandoms.length"
          keep-first
          placeholder="Ajouter au moins un fandom"
          :data="filteredFandoms"
          @typing="getFilteredFandoms"
        >
          <template #default="{ option }: { option: FandomData }">
            <strong>{{ option.id }}</strong
            >: {{ option.name }}
          </template>
        </BTaginput>
      </BField>

      <BField label="Genres">
        <BTaginput
          v-model="selectedGenres"
          field="name"
          ellipsis
          :allow-new="false"
          autocomplete
          :required="!selectedGenres.length"
          keep-first
          placeholder="Ajouter au moins un genre"
          :data="filteredGenres"
          @typing="getFilteredGenres"
        />
      </BField>

      <BField label="Rating">
        <BSelect v-model="selectedRating" label="Rating" placeholder="Sélectionner un rating" required>
          <option v-for="rating in ratings" :key="rating.characteristicId" :value="rating">
            {{ rating.name }}
          </option>
        </BSelect>
      </BField>

      <BField label="Caractéristiques">
        <BTaginput
          v-model="selectedCharacteristics"
          field="name"
          ellipsis
          :allow-new="false"
          autocomplete
          keep-first
          placeholder="Ajouter des caractéristiques"
          :data="filteredCharacteristics"
          @typing="getFilteredCharacteristics"
        >
          <template #default="{ option }: { option: CharacteristicModel }">
            <strong>{{
              characteristicTypes!.find(
                (ct) => ct.characteristicTypeId.toString() === option.characteristicTypeId.toString(),
              )!.name
            }}</strong
            >: {{ option.name }}
          </template>
          <template #tag="{ tag }: { tag: CharacteristicModel }">
            <span :class="[getCaracteristicTypeColor(Number(tag.characteristicTypeId))]">{{ tag.name }}</span>
          </template>
        </BTaginput>
      </BField>

      <BField label="Tags">
        <BTaginput
          v-model="selectedTags"
          field="name"
          ellipsis
          :allow-new="false"
          autocomplete
          keep-first
          placeholder="Ajouter des tags"
          :data="filteredTags"
          @typing="getFilteredTags"
        >
          <template #default="{ option }: { option: Tag }">
            <strong>{{ option.tagType }}</strong
            >: {{ option.name }}
          </template>
        </BTaginput>
      </BField>

      <BField label="Notes de fictions">
        <CustomEditor
          v-model:text="fiction.storynote"
          :config="{
            defaultValue: fiction.storynote || '',
            showFooter: false,
            placeholder: '',
            fixedHeight: false,
            height: 200,
            canQuote: false,
            readOnly: false,
            quoteLimit: 0,
            fontSize: 100,
            oneLineToolbar: true,
            canUseImage: false,
          }"
          @update:text="() => (unsavedChanges = true)"
        />
      </BField>
    </div>
  </div>
  <!-- Barre de navigation -->
  <slot></slot>
</template>

<script setup lang="ts">
import { BField, BInput, BTaginput, BSelect } from "buefy";
import type { CharacteristicModel, FanfictionModel } from "@/models";
import type { FandomData } from "@/types/fanfictions";
import { FanfictionStatus } from "@/models";
import { getCaracteristicTypeColor } from "#imports";

// NOTE J'aurais préféré watch(fiction, () => {}, { deep: true }) mais fiction est ref et pas reactive
// Quand la fiction vide par défaut est remplacée par la fiction chargée, on perd l'unité et donc la réactivité
const unsavedChanges = defineModel<boolean>("unsavedChanges", { required: true });
const fiction = defineModel<FanfictionModel>("fiction", { required: true });

const { characteristicTypes } = useConfigStore();
const { characteristics } = useConfigStore();
const { fandoms } = useConfigStore();

// FANDOM
const lastUsedFandom: FandomData = fandoms!.find((f) => f.name === "Harry Potter")!;
const selectedFandoms = ref<FandomData[]>([lastUsedFandom]);
const filteredFandoms = ref<FandomData[]>(fandoms!);

function getFilteredFandoms(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredFandoms.value = fandoms!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}

// GENRE
const genres = useConfigStore().characteristics!.filter((c) => c.characteristicTypeId.toString() === "2");
const filteredGenres = ref<CharacteristicModel[]>([]);
const selectedGenres = ref<CharacteristicModel[]>([]);
function getFilteredGenres(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredGenres.value = genres!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}

// RATINGS
const ratings = useConfigStore().characteristics!.filter((c) => c.characteristicTypeId.toString() === "5");
const selectedRating = ratings[0];

// CARACTÉRISTIQUES
const filteredCharacteristics = ref<CharacteristicModel[]>([]);
const selectedCharacteristics = ref<CharacteristicModel[]>([]);
function getFilteredCharacteristics(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredCharacteristics.value = characteristics!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}

// UNIFIÉ
interface Tag {
  name: string;
  tagType: string;
}
const characteristicsAsTags: Tag[] = useConfigStore().characteristics!.map((c) => {
  return {
    name: c.name,
    tagType: characteristicTypes!.find(
      (ct) => c.characteristicTypeId.toString() === ct.characteristicTypeId.toString(),
    )!.name,
  };
});
const fandomsAsTags: Tag[] = fandoms!.map((f) => {
  return { name: f.name, tagType: "Fandom" };
});

const tags: Tag[] = fandomsAsTags.concat(characteristicsAsTags);
const selectedTags = ref<Tag[]>([]);
const filteredTags = ref<Tag[]>([]);
function getFilteredTags(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredTags.value = tags.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}
</script>
