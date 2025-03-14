<template>
  <div>
    <b-loading v-if="status === 'pending'" :is-full-page="false" />
    <div class="columns">
      <!-- Colonne gauche - Toolbar -->
      <div v-if="chapter != null" class="column is-narrow pr-0">
        <div class="card" style="position: sticky; top: 60px; width: 40px;">
          <div class="card-content" style="padding: 5px;">
            <div class="content is-flex is-flex-direction-column" style="gap: 5px;">
              <b-tooltip
                label="Afficher / masquer le panel de review"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="feather-alt"
                  @click="reviewEditorVisible = !reviewEditorVisible"
                />
              </b-tooltip>
              <b-tooltip
                label="Augmenter la taille de la police"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-up"
                  @click="upSizeFont()"
                />
              </b-tooltip>
              <b-tooltip
                label="Taille de police par défaut"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="compress-alt"
                  @click="defaultSizeFont()"
                />
              </b-tooltip>
              <b-tooltip
                label="Réduire la taille de la police"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-down-alt"
                  @click="downSizeFont()"
                />
              </b-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne centrale - Contenu -->
      <div :class="['column', 'is-flex', 'is-flex-direction-column']">
        <div class="is-flex-grow-5">
          <!-- Notes de fiction (seulement sur le chapitre 1)-->
          <section v-if="((chapter?.order ?? 0) == 1) && (tableOfContent?.storynote?.length ?? 0 > 0)">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="fictionNotes"
            >
              <template #trigger="props">
                <div
                  class="card-header"
                  role="button"
                  aria-controls="fictionNotes"
                  :aria-expanded="props.open"
                >
                  <p class="card-header-title is-unselectable">
                    Notes de fiction
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                  </a>
                </div>
              </template>

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="tableOfContent.storynote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Note de début de chapitre -->
          <section v-if="(chapter?.startnote?.length ?? 0) > 0">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="chapterStartNote"
            >
              <template #trigger="props">
                <div
                  class="card-header"
                  role="button"
                  aria-controls="chapterStartNote"
                  :aria-expanded="props.open"
                >
                  <p class="card-header-title is-unselectable">
                    Notes de chapitre
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                  </a>
                </div>
              </template>

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="chapter?.startnote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Trigger warning -->
          <article v-if="(chapter?.trigger_warnings_loaded?.length ?? 0) > 0" class="message is-danger">
            <div class="message-body py-3 px-2 is-flex is-flex-direction-row">
              <b-icon icon="exclamation-triangle" /><span><strong class="mr-1"> TW / CW </strong></span>
              <div v-for="(trigger_warning, index) in chapter?.trigger_warnings_loaded" :key="index">
                <span v-if="index > 0">
                  ,
                </span>
                <span class="has-text-danger">{{ trigger_warning.caption }}</span>
              </div>
            </div>
          </article>

          <!-- Contenu du chapitre -->
          <section v-if="chapter != null">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="chapterContent"
            >
              <template #trigger="props">
                <div
                  class="card-header sub-title"
                  role="button"
                  aria-controls="chapterContent"
                  :aria-expanded="props.open"
                >
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
                <div class="has-text-right" style="position: sticky; top: 80px; height: 50px;">
                  <span v-show="fontSizeVisible" class="mr-2 p-1 is-primary is-size-7 has-text-weight-semibold" style="background-color: whitesmoke; opacity: 1; border: solid; border-radius: 0.50rem;">
                    {{ tiptapReadOnlyConfig.fontSize + '%' }}
                  </span>
                </div>
                <!-- FIN: Sticky FontSize -->
                <div class="content p-2" style="display: block; overflow: auto; margin-top: -55px;">
                  <client-only>
                    <TipTapEditor ref="chapter-content-editor" :config="tiptapReadOnlyConfig" @quote="quoteFromText" />
                  </client-only>
                </div>
              </div>
              <footer v-if="false" class="card-footer">
                <a class="card-footer-item">Save</a>
                <a class="card-footer-item">Edit</a>
                <a class="card-footer-item">Delete</a>
              </footer>
            </b-collapse>
            <br>
          </section>

          <!-- Note de fin de chapitre -->
          <section v-if="(chapter?.endnote?.length ?? 0) > 0">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="chapterEndNote"
            >
              <template #trigger="props">
                <div
                  class="card-header"
                  role="button"
                  aria-controls="chapterEndNote"
                  :aria-expanded="props.open"
                >
                  <p class="card-header-title is-unselectable">
                    Notes de fin de chapitre
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                  </a>
                </div>
              </template>

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="chapter?.endnote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Reviews -->
          <section v-if="chapter != null">
            <b-collapse
              v-model="reviewPaneExpanded"
              class="card"
              animation="slide"
              aria-id="chapterReviews"
            >
              <template #trigger>
                <div
                  class="card-header  sub-title"
                  role="button"
                  aria-controls="chapterReviews"
                  :aria-expanded="reviewPaneExpanded"
                >
                  <p class="card-header-title is-unselectable">
                    {{ 'Reviews (' + chapter?.review_count?.toString() + ")" }}
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="reviewPaneExpanded ? 'caret-up' : 'caret-down'" type="is-light" />
                  </a>
                </div>
              </template>

              <div class="card-content pb-0">
                <div class="content p-2">
                  <ReviewList ref="review-list" :item_id="reviewListItemId" :review-list-type="reviewListType" @reviewContentChanged="(value) => (editorContentReview = value)" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>
        </div>
      </div>

      <!-- Colonne droite - Editeur review -->
      <div v-if="$auth.loggedIn" v-show="reviewEditorVisible" class="column is-4">
        <div class="card" style="position: sticky; top: 60px;">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              Editeur de review
            </p>
            <button class="delete mr-1 mt-1" @click="reviewEditorVisible = false" />
          </header>
          <div class="card-content p-3">
            <div v-if="reviewHeaderMessageVisible" class="notification is-info is-light is-size-6 py-2 pl-2 pr-5">
              <button class="delete is-small" @click="reviewHeaderMessageVisible = false" />
              <p>Vous avez aimé ce texte ? <strong>Dites-le !</strong> Vous pensez que ce texte peut être amélioré ? <strong>Ecrivez-le !</strong></p><p>Avec gentillesse et bienveillance, faites part de votre avis.</p>
            </div>
            <client-only>
              <TipTapEditor ref="review-editor-small" :config="tiptapReviewConfig" :show-footer="false" :placeholder="'Ecrire une review'" @change="(value) => (editorContentReview = value)" />
            </client-only>
            <div class="mt-1 is-flex is-flex-direction-row is-flex-wrap-wrap">
              <b-checkbox v-model="canRate">
                Ajouter une note
              </b-checkbox>
              <b-rate
                v-model="reviewRating"
                icon-pack="fas"
                :max="10"
                size="default"
                :show-score="canRate"
                :rtl="false"
                :spaced="false"
                :disabled="!canRate"
              />
            </div>
          </div>
          <footer class="card-footer py-2">
            <b-button
              :disabled="(editorContentReview?.wordcount ?? 0) < 3"
              :expanded="false"
              label="Poster une review"
              type="is-primary"
              class="mx-auto"
            />
          </footer>
        </div>
      </div>
      <div v-else-if="reviewEditorVisible" class="buttons column is-narrow">
        <b-button
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser une review"
          type="is-primary"
          style="position: sticky; top: 60px;"
          @click="ModalStatesModule.setLoginModalActive(true)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getChapter } from "@/api/chapters";
import { ChapterModel, TableOfContent } from "@/models/fanfictions";
import TipTapEditor from "@/components/TipTapEditor.vue";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";
import ReviewList from "@/components/list/reviews/ReviewList.vue";
import { ReviewItemTypeEnum } from "@/types/fanfictions";
import { TiptapEditor } from "~/.nuxt/imports";

const { tableOfContent } = defineProps<{
  tableOfContent: TableOfContent;
}>();

const route = useRoute();

const ModalStatesModule = ModalsStates();

const { data: chapter, status } = await getChapter(parseInt(route.params.chapter_id as string));
const reviewListItemId = computed(() => chapter.value.chapter_id)

const tiptapReadOnlyConfig = reactive<TipTapEditorConfig>({
  showFooter: false,
  placeholder: "",
  readOnly: true,
  fixedHeight: false,
  height: 125,
  defaultValue: chapter.value.text ?? "",
  canQuote: false,
  quoteLimit: 250,
  fontSize: 100,
  oneLineToolbar: false,
  canUseImage: true
});

// FIXME - mais en a-t-on besoin ?
// const chapterContentEditor = useTemplateRef("chapter-content-editor");
// effect(() => {
//   (chapterContentEditor.value as unknown as TiptapEditor).commands.setContent(
//     new TipTapEditorContent({ content: (chapter.value.text ?? "") }).content
//   )
// })

let reviewEditorVisible = ref<boolean>(true);
let editorContentReview: TipTapEditorContent | null = null;

let tiptapReviewConfig: TipTapEditorConfig = {
  showFooter: false,
  placeholder: "Votre review ici",
  readOnly: false,
  fixedHeight: true,
  height: 250,
  defaultValue: "",
  canQuote: false,
  quoteLimit: 0,
  fontSize: 100,
  oneLineToolbar: true,
  canUseImage: false
};

let reviewHeaderMessageVisible = ref<boolean>(true);

let fontSizeVisible = ref<boolean>(false);

let timerThrottleFontsize: number = 0;

let reviewPaneExpanded = ref<boolean>(false);

// Reviews
let reviewListType : ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;

let canRate: boolean = false;
let reviewRating: number | null = null;

// FIXME
// function onAuthChanged(): void {
//   this.tiptapReadOnlyConfig.canQuote = this.$auth.loggedIn;
// }

// function onreviewPaneExpanded(): void {
//   if (this.reviewPaneExpanded && this.reviewEditorVisible) {
//     if (process.client) {
//       (this.$refs.reviewList as ReviewList)?.setContent(this.editorContentReview);
//     }
//     this.reviewEditorVisible = false;
//   }
// }

// function onCanRateChanged(): void {
//   this.reviewRating = (this.canRate ? 10 : null);
// }

// function onreviewEditorVisibleChanged(): void {
//   if (this.reviewEditorVisible && this.reviewPaneExpanded) {
//     if (process.client) {
//       (this.$refs.reviewEditorSmall as TipTapEditor)?.setContent(this.editorContentReview);
//     }
//     this.reviewPaneExpanded = false;
//   }
// }

function quoteFromText() {}
// FIXME
// const reviewEditorSmall = useTemplateRef("review-editor-small");
// const reviewList = useTemplateRef("review-list");
// function quoteFromText(quote: string): void {
//   if (import.meta.client) {
//     if (reviewPaneExpanded.value === false) {
//       if (reviewEditorVisible.value === false) reviewEditorVisible.value = true;
//       (reviewEditorSmall.value as unknown as typeof TipTapEditor).commands.setQuote(quote);
//     } else if (reviewPaneExpanded.value) (reviewList.value as unknown as typeof ReviewList).setQuote(quote);
//   }
// }

// Augmenter la taille du texte
function upSizeFont(): void {
  if (import.meta.client) {
    tiptapReadOnlyConfig.fontSize += 10;
    displayFontSize();
  }
}

// Réduire la taille du texte
function defaultSizeFont(): void {
  if (import.meta.client) {
    tiptapReadOnlyConfig.fontSize = 100;
    displayFontSize();
  }
}

// Réduire la taille du texte
function downSizeFont(): void {
  if (import.meta.client) {
    tiptapReadOnlyConfig.fontSize -= 10;
    displayFontSize();
  }
}

// Afficher / masquer l'indicateur de fontSize
function displayFontSize(): void {
  fontSizeVisible.value = true;
  clearTimeout(timerThrottleFontsize);
  timerThrottleFontsize = window.setTimeout(
    () => { fontSizeVisible.value = false; },
    3000
  );
}
</script>

<style lang="scss" scoped>
*{
  // border: 1px solid green;
}
</style>
