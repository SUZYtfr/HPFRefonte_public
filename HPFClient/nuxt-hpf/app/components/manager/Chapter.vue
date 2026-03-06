<template>
  <div class="card">
    <div class="card-content">
      <BTabs v-model="activeTab" type="is-boxed" :animated="false" vertical>
        <BTabItem v-for="(value, index) in chapterIds.concat([''])" :key="index" :value="value" destroy-on-hide>
          <!-- Items vides sauf celui du chapitre en question -->
          <template #header>
            <span :title="value === '' ? 'Nouveau chapitre' : 'Chapitre ' + (index + 1)">
              {{ value === "" ? "+" : index + 1 }}
            </span>
          </template>
          <template v-if="value === (chapter.chapterId || '').toString()">
            <BField label="Titre" grouped>
              <BInput
                v-model="chapter.title"
                type="text"
                required
                expanded
                @update:model-value="() => (unsavedChanges = true)"
              />
              <BDropdown aria-role="list" :disabled="!isEditing || activeTab === ''">
                <template #trigger="{ active }">
                  <BButton label="Plus d'actions" type="is-warning" :icon-right="active ? 'caret-up' : 'caret-down'" />
                </template>
                <BDropdownItem aria-role="listitem">Voir les statistiques</BDropdownItem>
                <BDropdownItem aria-role="listitem">Ajouter à une série</BDropdownItem>
                <BDropdownItem aria-role="listitem">Supprimer le chapitre</BDropdownItem>
              </BDropdown>
            </BField>
            <BField label="Note de début">
              <RichtextEditor
                v-model:text="chapter.startNote"
                :config="{
                  showFooter: false,
                  placeholder: 'Notes de début de fiction',
                  fixedHeight: false,
                  height: 200,
                  oneLineToolbar: true,
                  canUseImage: false,
                }"
                @update:text="() => (unsavedChanges = true)"
              />
            </BField>
            <BField label="Texte">
              <RichtextEditor
                v-model:text="chapter.text"
                :config="{
                  showFooter: true,
                  placeholder: 'Texte du chapitre',
                  fixedHeight: true,
                  height: 600,
                  oneLineToolbar: true,
                  canUseImage: false,
                }"
                @update:text="() => (unsavedChanges = true)"
              />
            </BField>
            <BField label="Notes de fin">
              <RichtextEditor
                v-model:text="chapter.endNote"
                :config="{
                  showFooter: false,
                  placeholder: 'Notes de fin de fiction',
                  fixedHeight: false,
                  height: 200,
                  oneLineToolbar: true,
                  canUseImage: false,
                }"
                @update:text="() => (unsavedChanges = true)"
              />
            </BField>
            <BField label="Avertissements">
              <BTaginput
                v-model="selectedTriggerWarnings"
                field="name"
                type="is-danger"
                ellipsis
                :allow-new="false"
                autocomplete
                keep-first
                keep-open
                open-on-focus
                placeholder="Ajouter des avertissements de contenu"
                :data="filteredTriggerWarnings"
                @typing="getFilteredTriggerWarnings"
                @update:model-value="
                  (value: TriggerWarningData[]) => {
                    chapter.triggerWarnings = value;
                    unsavedChanges = true;
                  }
                "
              />
            </BField>
          </template>
        </BTabItem>
      </BTabs>
    </div>
  </div>
  <!-- Barre de navigation -->
  <slot></slot>
</template>

<script setup lang="ts">
import { BTabs, BTabItem, BField, BInput, BTaginput } from "buefy";
import type { ChapterModel } from "~/models";
import type { TriggerWarningData } from "~/types/characteristics";

interface Props {
  isEditing: boolean;
  chapterIds: string[];
}

// NOTE J'aurais préféré watch(fiction, () => {}, { deep: true }) mais fiction est ref et pas reactive
// Quand la fiction vide par défaut est remplacée par la fiction chargée, on perd l'unité et donc la réactivité
const unsavedChanges = defineModel<boolean>("unsavedChanges", { required: true });
const chapter = defineModel<ChapterModel>("chapter", { required: true });
const activeTab = defineModel<string>("activeTab", { required: true });
const { chapterIds } = defineProps<Props>();

// Préremplit le titre du nouveau chapitre
watch(
  activeTab,
  (newTab) => {
    if (newTab === "") {
      chapter.value.title = "Chapitre " + (chapterIds.length + 1);
    }
  },
  {
    immediate: true,
  },
);

// Avertissements
const { triggerWarnings } = useConfigStore();
const selectedTriggerWarnings = ref<TriggerWarningData[]>(
  triggerWarnings!.filter((tw) =>
    chapter.value.triggerWarnings!.map((tw) => tw.id.toString()).includes(tw.id.toString()),
  ),
);
const filteredTriggerWarnings = ref<TriggerWarningData[]>(triggerWarnings!);
function getFilteredTriggerWarnings(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredTriggerWarnings.value = triggerWarnings!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}
</script>
