<template>
  <div class="card">
    <div class="card-content">
      <BField label="Titre" grouped>
        <BInput
          v-model="collection.title"
          type="text"
          placeholder="Titre de la série"
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
          <BDropdownItem aria-role="listitem">Supprimer la série</BDropdownItem>
        </BDropdown>
      </BField>
      <BField label="Accès" expanded>
        <BSelect v-model="collection.access" required @update:model-value="() => (unsavedChanges = true)">
          <option v-for="[key, value] in Object.entries(Access)" :key="key" :value="key">
            {{ value }}
          </option>
        </BSelect>
      </BField>
      <BField label="Résumé">
        <RichtextEditor
          v-model:text="collection.summary"
          :config="{
            showFooter: false,
            placeholder: 'Résumé de la série',
            fixedHeight: true,
            height: 200,
            oneLineToolbar: true,
            canUseImage: false,
          }"
          @update:text="() => (unsavedChanges = true)"
        />
      </BField>
      <BField label="Fandoms" expanded>
        <ManagerFandomInput
          :fandom-field="collection.fandoms!"
          @update:fandom-field="
            (fandoms) => {
              collection.fandoms = fandoms;
              unsavedChanges = true;
            }
          "
        />
      </BField>
      <BField label="Caractéristiques">
        <ManagerCharacteristicInput
          :characteristic-field="collection.characteristics! as CharacteristicModel[]"
          @update:characteristic-field="
            (characteristics) => {
              collection.characteristics = characteristics;
              unsavedChanges = true;
            }
          "
        />
      </BField>
    </div>
  </div>
  <!-- Barre de navigation -->
  <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
    <div></div>
    <BButton v-if="isEditing" type="is-danger" :disabled="!unsavedChanges" @click.prevent="$emit('clickCancel')"
      >Annuler les modifications</BButton
    >
    <BButton
      type="is-primary"
      :disabled="!isComplete"
      @click.prevent="
        isEditing ? $emit('updateCollection') : $emit('createCollection');
        $emit('clickNext');
      "
    >
      {{ isEditing && unsavedChanges ? "Enregistrer et aller aux éléments" : "Aller aux éléments" }}
    </BButton>
  </div>
</template>

<script setup lang="ts">
import { BField, BInput, BDropdown, BDropdownItem, BSelect, BButton } from "buefy";
import type { CharacteristicModel, CollectionModel } from "~/models";
import { Access } from "~/types/fanfictions";

interface Props {
  isEditing: boolean;
}
interface Emits {
  (e: "clickCancel" | "clickNext" | "createCollection" | "updateCollection"): void;
}

defineProps<Props>();
defineEmits<Emits>();
const collection = defineModel<CollectionModel>("collection", { required: true });

const unsavedChanges = ref<boolean>(false);
const isComplete = computed<boolean>(() => {
  return [
    collection.value.title,
    collection.value.summary,
    collection.value.access,
    collection.value.fandoms?.length,
  ].every((field) => Boolean(field));
});
// si la série change, elle a été rechargée (enregistrement ou abandon des modifs)
watch(collection, () => (unsavedChanges.value = false));
</script>
