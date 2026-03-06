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
          <BSelect
            v-model="fiction.rating"
            placeholder="Sélectionner un rating"
            required
            @update:model-value="() => (unsavedChanges = true)"
          >
            <option v-for="[key, value] in Object.entries(FanfictionRating)" :key="key" :value="key">
              {{ value }}
            </option>
          </BSelect>
        </BField>
      </BField>
      <BField label="Résumé">
        <RichtextEditor
          v-model:text="fiction.summary"
          :config="{
            showFooter: false,
            placeholder: 'Résumé de la fiction',
            fixedHeight: true,
            height: 200,
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
            keep-open
            open-on-focus
            placeholder="Ajouter au moins un fandom"
            :data="filteredFandoms"
            @typing="getFilteredFandoms"
            @update:model-value="
              (value: FandomData[]) => {
                fiction.fandoms = value;
                unsavedChanges = true;
              }
            "
          />
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
            keep-open
            open-on-focus
            placeholder="Ajouter au moins un genre"
            :data="filteredGenres"
            @typing="getFilteredGenres"
            @add="(value: CharacteristicModel) => (fiction.characteristics = fiction.characteristics!.concat(value))"
            @remove="
              (value: CharacteristicModel) =>
                (fiction.characteristics = fiction.characteristics!.slice(fiction.characteristics!.indexOf(value)))
            "
            @update:model-value="() => (unsavedChanges = true)"
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
            'Ajouter des ' +
            selectedCharacteristicType.name.toLowerCase() +
            's parmi ' +
            characteristics
              ?.filter(
                (c) => c.characteristicTypeId.toString() === selectedCharacteristicType.characteristicTypeId.toString(),
              )!
              .length.toString() +
            ' choix'
          "
          :data="filteredCharacteristics"
          @typing="getFilteredCharacteristics"
          @add="(value: CharacteristicModel) => (fiction.characteristics = fiction.characteristics!.concat(value))"
          @remove="
            (value: CharacteristicModel) =>
              (fiction.characteristics = fiction.characteristics!.slice(fiction.characteristics!.indexOf(value)))
          "
          @update:model-value="() => (unsavedChanges = true)"
        />
      </BField>

      <BField label="Notes de fictions">
        <RichtextEditor
          v-model:text="fiction.storynote"
          :config="{
            showFooter: false,
            placeholder: 'Notes de la fiction',
            fixedHeight: false,
            height: 200,
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
import type { CharacteristicModel, CharacteristicTypeModel, FanfictionModel } from "~/models";
import type { FandomData } from "~/types/fanfictions";
import { FanfictionStatus, FanfictionRating } from "~/models";

interface Props {
  isEditing: boolean;
}

defineProps<Props>();
// NOTE J'aurais préféré watch(fiction, () => {}, { deep: true }) mais fiction est ref et pas reactive
// Quand la fiction vide par défaut est remplacée par la fiction chargée, on perd l'unité et donc la réactivité
const unsavedChanges = defineModel<boolean>("unsavedChanges", { required: true });
const fiction = defineModel<FanfictionModel>("fiction", { required: true });

const { fandoms } = useConfigStore();
const { characteristicTypes } = useConfigStore();
const { characteristics } = useConfigStore();

// les fandoms et caractéristiques de la fiction sont "remplacés"
// par les fandoms stockés, pour garder une identité des objets
// BTagInput utilise l'identité des objets (===) et pas la similitude (==)
// pour comparer les tags entrés, ce qui potentiellement permet de choisir
// deux fois le même tag (un préselectionné, un sélectionné)
// TODO - effectuer ce "remplacement" en amont dans FictionModel?

// FANDOM
const selectedFandoms = ref<FandomData[]>(
  fandoms!.filter((f) => fiction.value.fandoms!.map((ff) => ff.id.toString()).includes(f.id.toString())),
);
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
const genres = characteristics!.filter((c) => c.characteristicTypeId.toString() === "2");
const selectedGenres = ref<CharacteristicModel[]>(
  genres!.filter((ct) =>
    fiction.value.characteristics!.map((c) => c.characteristicId.toString()).includes(ct.characteristicId.toString()),
  ),
);
const filteredGenres = ref<CharacteristicModel[]>(genres);
function getFilteredGenres(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredGenres.value = genres!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}

// AUTRES CARACTÉRISTIQUES
const otherCharacteristicTypes = characteristicTypes!.filter((ct) => ct.characteristicTypeId.toString() !== "2");
const selectedCharacteristicType = ref<CharacteristicTypeModel>(otherCharacteristicTypes[0]!);
const otherCharacteristics = characteristics!.filter((c) => c.characteristicTypeId.toString() !== "2");
const selectedCharacteristics = ref<CharacteristicModel[]>(
  otherCharacteristics!.filter((ct) =>
    fiction.value.characteristics!.map((c) => c.characteristicId.toString()).includes(ct.characteristicId.toString()),
  ),
);
const filteredCharacteristics = ref<CharacteristicModel[]>(
  otherCharacteristics!.filter(
    (option) =>
      option.characteristicTypeId.toString() === selectedCharacteristicType.value.characteristicTypeId.toString(),
  ),
);
function getFilteredCharacteristics(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredCharacteristics.value = otherCharacteristics!
    .filter(
      (option) =>
        option.characteristicTypeId.toString() === selectedCharacteristicType.value.characteristicTypeId.toString(),
    )
    .filter((option) => {
      return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
    });
}
watch(selectedCharacteristicType, () => getFilteredCharacteristics(""));
</script>
