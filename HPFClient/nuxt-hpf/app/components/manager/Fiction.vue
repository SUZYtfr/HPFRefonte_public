<template>
  <div class="card">
    <div class="card-content">
      <BField label="Titre" grouped>
        <BInput v-model="fiction.title" type="text" placeholder="Titre de la fiction" required expanded />
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
          <BSelect v-model="fiction.status" required>
            <option v-for="[key, value] in Object.entries(FanfictionStatus)" :key="key" :value="key">
              {{ value }}
            </option>
          </BSelect>
        </BField>
        <BField label="Rating" expanded>
          <BSelect v-model="fiction.rating" placeholder="Sélectionner un rating" required>
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
        />
      </BField>

      <BField grouped>
        <BField label="Fandoms" expanded>
          <ManagerFandomInput v-model:fandom-field="fiction.fandoms!" />
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
        />
      </BField>
    </div>
  </div>
  <!-- Barre de navigation -->
  <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
    <BButton @click.prevent="$emit('clickPrevious')">Relire le réglement</BButton>
    <BButton v-if="isEditing" type="is-danger" :disabled="!unsavedChanges" @click.prevent="$emit('clickCancel')"
      >Annuler les modifications</BButton
    >
    <BButton type="is-primary" :disabled="!isComplete" @click.prevent="$emit('clickNext')">
      {{ isEditing && unsavedChanges ? "Enregistrer et aller aux chapitres" : "Aller aux chapitres" }}
    </BButton>
  </div>
</template>

<script setup lang="ts">
import { BField, BInput, BTaginput, BSelect, BDropdown, BDropdownItem, BButton } from "buefy";
import type { CharacteristicModel, CharacteristicTypeModel, FanfictionModel } from "~/models";
import { FanfictionStatus, FanfictionRating } from "~/models";

interface Props {
  isEditing: boolean;
}
interface Emits {
  (e: "clickPrevious" | "clickCancel" | "clickNext"): void;
}

defineProps<Props>();
defineEmits<Emits>();

const unsavedChanges = defineModel<boolean>("unsavedChanges", { required: true });
const fiction = defineModel<FanfictionModel>("fiction", { required: true });
watch(fiction, () => (unsavedChanges.value = true), { deep: true }); // si les champs changent
watch(fiction, () => (unsavedChanges.value = false)); // si la fiction est rechargée

const isComplete = computed<boolean>(() => {
  return [
    fiction.value.title,
    fiction.value.summary,
    fiction.value.status,
    fiction.value.rating,
    fiction.value.fandoms?.length,
    fiction.value.characteristics?.filter((c) => c.characteristicTypeId.toString() === "2").length,
  ].every((field) => Boolean(field));
});

const { characteristicTypes } = useConfigStore();
const { characteristics } = useConfigStore();

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
