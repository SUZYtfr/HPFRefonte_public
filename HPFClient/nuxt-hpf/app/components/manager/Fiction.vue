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
        <ManagerFandomField v-model:fandom-field="fiction.fandoms!" label="Fandoms" expanded />
        <ManagerCharacteristicField
          v-model:characteristic-field="fiction.characteristics!"
          :required="!fiction.characteristics!.filter((c) => c.characteristicTypeId.toString() === '2').length"
          :characteristic-type-ids="['2'] /* juste 2 - Genre */"
          label="Genres"
          expanded
        />
      </BField>

      <ManagerCharacteristicField
        v-model:characteristic-field="fiction.characteristics!"
        :select-addon="true"
        :characteristic-type-ids="'1345678'.split('') /* exclut 2 - Genre */"
        label="Autres caractéristiques"
      />

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
    <BButton v-show="isEditing" type="is-danger" :disabled="!unsavedChanges" @click.prevent="$emit('clickCancel')"
      >Annuler les modifications</BButton
    >
    <BButton type="is-primary" :disabled="!isComplete" @click.prevent="$emit('clickNext')">
      {{ isEditing && unsavedChanges ? "Enregistrer et aller aux chapitres" : "Aller aux chapitres" }}
    </BButton>
  </div>
</template>

<script setup lang="ts">
import { BField, BInput, BSelect, BDropdown, BDropdownItem, BButton } from "buefy";
import type { FanfictionModel } from "~/models";
import { FanfictionStatus, FanfictionRating } from "~/types/fanfictions";

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
</script>
