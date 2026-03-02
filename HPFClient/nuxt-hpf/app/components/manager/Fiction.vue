<template>
  <div class="card">
    <div class="card-content">
      <BField label="Titre" grouped>
        <BInput
          v-model="fiction.title"
          type="text"
          placeholder="Titre de la fiction"
          required
          expanded
          @update:model-value="() => (unsavedChanges = true)"
        />
        <BDropdown aria-role="list" :disabled="!isEditing">
          <template #trigger="{ active }">
            <BButton label="Plus d'actions" type="is-warning" :icon-right="active ? 'caret-up' : 'caret-down'" />
          </template>
          <BDropdownItem aria-role="listitem">Voir les statistiques</BDropdownItem>
          <BDropdownItem aria-role="listitem">Ajouter à une série</BDropdownItem>
          <BDropdownItem aria-role="listitem">Supprimer la fiction</BDropdownItem>
        </BDropdown>
      </BField>
      <BField grouped>
        <BField label="Statut" expanded>
          <BSelect v-model="fiction.status" required @update:model-value="() => (unsavedChanges = true)">
            <option v-for="[key, value] in Object.entries(FanfictionStatus)" :key="key" :value="key">
              {{ value }}
            </option>
          </BSelect>
        </BField>
        <BField label="Rating" expanded>
          <BSelect v-model="selectedRating" label="Rating" placeholder="Sélectionner un rating" required>
            <option v-for="rating in ratings" :key="rating.characteristicId" :value="rating">
              {{ rating.name }}
            </option>
          </BSelect>
        </BField>
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

      <BField grouped>
        <BField label="Fandoms" expanded>
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
        <BField label="Genres" expanded>
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
      </BField>

      <BField label="Autres caractéristiques">
        <BSelect v-model="selectedCharacteristicType">
          <option
            v-for="characteristicType in otherCharacteristicTypes"
            :key="characteristicType.characteristicTypeId"
            :value="characteristicType"
          >
            {{ characteristicType.name }}
          </option>
        </BSelect>
        <BTaginput
          v-model="selectedCharacteristics"
          field="name"
          expanded
          ellipsis
          :allow-new="false"
          autocomplete
          keep-first
          keep-open
          open-on-focus
          :placeholder="
            'Ajouter des caractéristiques parmi ' +
            characteristics
              ?.filter(
                (c) => c.characteristicTypeId.toString() === selectedCharacteristicType.characteristicTypeId.toString(),
              )!
              .length.toString() +
            ' choix'
          "
          :data="filteredCharacteristics"
          @typing="getFilteredCharacteristics"
        />
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
import { BField, BInput, BTaginput, BSelect, BDropdown, BDropdownItem, BButton } from "buefy";
import type { CharacteristicModel, CharacteristicTypeModel, FanfictionModel } from "@/models";
import type { FandomData } from "@/types/fanfictions";
import { FanfictionStatus } from "@/models";

interface Props {
  isEditing: boolean;
}

defineProps<Props>();
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
const selectedRating = ref<CharacteristicModel>();

// AUTRES CARACTÉRISTIQUES
const otherCharacteristicTypes = characteristicTypes!.filter(
  (ct) => !["2", "4", "5"].includes(ct.characteristicTypeId.toString()),
);
const selectedCharacteristicType = ref<CharacteristicTypeModel>(otherCharacteristicTypes[0]!);
const filteredCharacteristics = ref<CharacteristicModel[]>([]);
const selectedCharacteristics = ref<CharacteristicModel[]>([]);
function getFilteredCharacteristics(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredCharacteristics.value = characteristics!
    .filter(
      (option) =>
        option.characteristicTypeId.toString() === selectedCharacteristicType.value.characteristicTypeId.toString(),
    )
    .filter((option) => {
      return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
    });
}
</script>
