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
            <BField label="Titre">
              <BInput
                v-model="chapter.title"
                type="text"
                required
                @update:model-value="() => (unsavedChanges = true)"
              />
            </BField>
            <BField label="Note de début">
              <CustomEditor
                v-model:text="chapter.startNote"
                :config="{
                  defaultValue: chapter.startNote || '',
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
            <BField label="Texte">
              <CustomEditor
                v-model:text="chapter.text"
                :config="{
                  defaultValue: chapter.text || '',
                  showFooter: true,
                  placeholder: '',
                  fixedHeight: true,
                  height: 600,
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
            <BField label="Notes de fin">
              <CustomEditor
                v-model:text="chapter.endNote"
                :config="{
                  defaultValue: chapter.endNote || '',
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
            <BField label="Avertissements">
              <BTaginput
                v-model="selectedTriggerWarnings"
                field="name"
                ellipsis
                :allow-new="false"
                autocomplete
                keep-first
                placeholder="Ajouter des avertissements de contenu"
                :data="filteredTriggerWarnings"
                @typing="getFilteredTriggerWarnings"
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
import type { ChapterModel, CharacteristicModel } from "@/models";

interface Props {
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
const triggerWarnings = useConfigStore().characteristics!.filter((c) => c.characteristicTypeId.toString() === "4");
const filteredTriggerWarnings = ref<CharacteristicModel[]>([]);
const selectedTriggerWarnings = ref<CharacteristicModel[]>([]);
function getFilteredTriggerWarnings(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredTriggerWarnings.value = triggerWarnings!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}
</script>
