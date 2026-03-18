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
              <BInput v-model="chapter.title" type="text" required expanded />
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
  <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
    <BButton @click.prevent="$emit('clickPrevious')">Revenir à la fiction</BButton>
    <BButton v-show="activeTab" type="is-danger" :disabled="!unsavedChanges" @click.prevent="$emit('clickCancel')"
      >Annuler les modifications</BButton
    >
    <BField>
      <p class="control">
        <BButton
          type="is-warning"
          :disabled="!(isComplete && unsavedChanges && !isEditing)"
          @click.prevent="$emit('clickSave', true)"
          >Brouillon</BButton
        >
      </p>
      <p class="control">
        <BButton
          type="is-success"
          :disabled="!(isComplete && unsavedChanges)"
          @click.prevent="$emit('clickSave', false)"
        >
          {{ autoPublish ? "Publier" : "Envoyer à la modération" }}</BButton
        >
      </p>
    </BField>
  </div>
</template>

<script setup lang="ts">
import { BTabs, BTabItem, BField, BInput, BTaginput, BButton } from "buefy";
import type { ChapterModel } from "~/models";
import type { TriggerWarningData } from "~/types/characteristics";

interface Props {
  isEditing: boolean;
  chapterIds: string[];
}
interface Emits {
  (e: "clickPrevious" | "clickCancel"): void;
  (e: "clickSave", isDraft: boolean): void;
}

const unsavedChanges = defineModel<boolean>("unsavedChanges", { required: true });
const chapter = defineModel<ChapterModel>("chapter", { required: true });
watch(chapter, () => (unsavedChanges.value = true), { deep: true }); // si les champs changent
watch(chapter, () => (unsavedChanges.value = false)); // si le chapitre est rechargé

const activeTab = defineModel<string>("activeTab", { required: true });
const { chapterIds } = defineProps<Props>();
defineEmits<Emits>();
const isComplete = computed<boolean>(() => {
  return [chapter.value.title, chapter.value.text].every((field) => Boolean(field));
});
const autoPublish = true; // TODO depuis profileData ou payloadData

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
