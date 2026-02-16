<template>
  <div class="is-flex-grow-5">
    <!-- Résumé de la fiction, par défaut fermé, sauf si chapter.order == 1-->
    <section v-if="(summary?.length ?? 0) > 0">
      <b-collapse class="card" animation="slide" aria-id="fictionSummary" :open="false">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionSummary" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Résumé de la fiction</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-0">
          <div class="content p-2">
            <p v-html="summary"></p>
          </div>
        </div>
      </b-collapse>
    </section>

    <!-- Notes de fiction (seulement sur le chapitre 1)-->
    <section v-if="storynotes?.length ?? 0 > 0">
      <b-collapse class="card" animation="slide" aria-id="fictionNotes">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionNotes" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Notes de fiction</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-0">
          <div class="content p-2">
            <p v-html="storynotes"></p>
          </div>
        </div>
      </b-collapse>
      <br />
    </section>

    <!-- Note de début de chapitre -->
    <section v-if="(chapter?.startnote?.length ?? 0) > 0">
      <b-collapse class="card" animation="slide" aria-id="chapterStartNote">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="chapterStartNote" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Notes de chapitre</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-0">
          <div class="content p-2">
            <p v-html="chapter?.startnote"></p>
          </div>
        </div>
      </b-collapse>
      <br />
    </section>

    <!-- Trigger warning -->
    <article v-if="(chapter?.triggerWarningsLoaded?.length ?? 0) > 0" class="message is-danger">
      <div class="message-body py-3 px-2 is-flex is-flex-direction-row">
        <b-icon icon="exclamation-triangle" /><span><strong class="mr-1"> TW / CW </strong></span>
        <div v-for="(trigger_warning, index) in chapter?.triggerWarningsLoaded" :key="index">
          <span v-if="index > 0"> , </span>
          <span class="has-text-danger">{{ trigger_warning.caption }}</span>
        </div>
      </div>
    </article>

    <!-- Contenu du chapitre -->
    <section v-if="chapter != null">
      <b-collapse class="card" animation="slide" aria-id="chapterContent">
        <template #trigger="props">
          <div class="card-header sub-title" role="button" aria-controls="chapterContent" :aria-expanded="props.open">
            <p class="card-header-title is-centered">
              {{ chapter?.title }}
            </p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
            </a>
          </div>
        </template>
        <div class="card-content p-0">
          <!-- DEBUT: Sticky FontSize -->
          <div
            v-if="tiptapReadOnlyConfig != null"
            class="has-text-right"
            style="position: sticky; top: 80px; height: 50px"
          >
            <span
              v-show="fontSizeVisible"
              class="mr-2 p-1 is-primary is-size-7 has-text-weight-semibold"
              style="background-color: whitesmoke; opacity: 1; border: solid; border-radius: 0.5rem"
            >
              {{ tiptapReadOnlyConfig.fontSize + "%" }}
            </span>
          </div>
          <!-- FIN: Sticky FontSize -->
          <div class="content p-2" style="display: block; overflow: auto; margin-top: -55px">
            <client-only>
              <!-- <TipTapEditor
                ref="chapterContentEditor"
                :config="tiptapReadOnlyConfig"
                @quote="(value: string) => emit('quote', value)"
              /> -->
            </client-only>
          </div>
        </div>
        <footer v-if="false" class="card-footer">
          <a class="card-footer-item">Save</a>
          <a class="card-footer-item">Edit</a>
          <a class="card-footer-item">Delete</a>
        </footer>
      </b-collapse>
      <br />
    </section>

    <!-- Note de fin de chapitre -->
    <section v-if="(chapter?.endnote?.length ?? 0) > 0">
      <b-collapse class="card" animation="slide" aria-id="chapterEndNote">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="chapterEndNote" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Notes de fin de chapitre</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-0">
          <div class="content p-2">
            <p v-html="chapter?.endnote"></p>
          </div>
        </div>
      </b-collapse>
      <br />
    </section>
  </div>
</template>

<script setup lang="ts">
//#region Import
import type { ChapterModel } from "~/models";
// import type { TipTapEditorConfig } from "~/types/tiptap";
//#endregion

//#region Props
defineProps<{
  chapter: ChapterModel | null;
  summary: string | null | undefined;
  storynotes: string | null | undefined;
  fontSizeVisible: boolean;
  tiptapReadOnlyConfig: { fontSize: number } | null;
  // tiptapReadOnlyConfig: TipTapEditorConfig | null;
}>();
//#endregion

//#region Emits
// const emit = defineEmits<{ (e: "quote", quote: string): void }>();
//#endregion
</script>

<style lang="scss" scoped></style>
