<template>
  <div>
    <BLoading v-model="chapterLoading" :is-full-page="false" />
    <div class="columns">
      <!-- Colonne gauche - Toolbar -->
      <div v-if="chapter" class="column is-narrow pr-0">
        <div class="card" style="position: sticky; top: 60px; width: 40px">
          <div class="card-content" style="padding: 5px">
            <div class="content is-flex is-flex-direction-column" style="gap: 5px">
              <BTooltip label="Afficher / masquer le panel de review" position="is-right" append-to-body>
                <BButton
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="feather-alt"
                  @click="reviewEditorVisible = !reviewEditorVisible"
                />
              </BTooltip>
              <BTooltip label="Augmenter la taille de la police" position="is-right" append-to-body>
                <BButton
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-up"
                  @click="upSizeFont()"
                />
              </BTooltip>
              <BTooltip label="Taille de police par défaut" position="is-right" append-to-body>
                <BButton
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="compress-alt"
                  @click="defaultSizeFont()"
                />
              </BTooltip>
              <BTooltip label="Réduire la taille de la police" position="is-right" append-to-body>
                <BButton
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-down-alt"
                  @click="downSizeFont()"
                />
              </BTooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne centrale - Contenu -->
      <div :class="['column', 'is-flex', 'is-flex-direction-column']">
        <div class="is-flex-grow-5">
          <!-- Notes de fiction (seulement sur le chapitre 1)-->
          <section v-if="chapter.order == 1 && (tableOfContent.storynote?.length ?? 0 > 0)">
            <BCollapse class="card" animation="slide" aria-id="fictionNotes">
              <template #trigger="props">
                <div class="card-header" role="button" aria-controls="fictionNotes" :aria-expanded="props.open">
                  <p class="card-header-title is-unselectable">Notes de fiction</p>
                  <a class="card-header-icon">
                    <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                  </a>
                </div>
              </template>

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="tableOfContent.storynote"></p>
                </div>
              </div>
            </BCollapse>
            <br />
          </section>

          <!-- Note de début de chapitre -->
          <section v-if="chapter.startNote.length > 0">
            <BCollapse class="card" animation="slide" aria-id="chapterStartNote">
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
                  <p v-html="chapter.startNote"></p>
                </div>
              </div>
            </BCollapse>
            <br />
          </section>

          <!-- Trigger warning -->
          <article v-if="chapter.triggerWarningsLoaded?.length || 0 > 0" class="message is-danger">
            <div class="message-body py-3 px-2 is-flex is-flex-direction-row">
              <BIcon icon="exclamation-triangle" /><span><strong class="mr-1"> TW / CW </strong></span>
              <div v-for="(tw, index) in chapter.triggerWarningsLoaded" :key="index">
                <span v-if="index > 0"> , </span>
                <span class="has-text-danger">{{ tw.caption }}</span>
              </div>
            </div>
          </article>

          <!-- Contenu du chapitre -->
          <section v-if="chapter != null">
            <BCollapse class="card" animation="slide" aria-id="chapterContent">
              <template #trigger="props">
                <div
                  class="card-header sub-title"
                  role="button"
                  aria-controls="chapterContent"
                  :aria-expanded="props.open"
                >
                  <p class="card-header-title is-centered">
                    {{ chapter.title }}
                  </p>
                  <a class="card-header-icon">
                    <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
                  </a>
                </div>
              </template>
              <div class="card-content p-0">
                <!-- DEBUT: Sticky FontSize -->
                <div class="has-text-right" style="position: sticky; top: 80px; height: 50px">
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
                  <CustomEditor
                    ref="chapter-content-editor"
                    :config="tiptapReadOnlyConfig"
                    @quote="(quote: string) => (reviewState.content = reviewState.content.concat(quote))"
                  />
                </div>
              </div>
              <footer v-if="false" class="card-footer">
                <a class="card-footer-item">Save</a>
                <a class="card-footer-item">Edit</a>
                <a class="card-footer-item">Delete</a>
              </footer>
            </BCollapse>
            <br />
          </section>

          <!-- Note de fin de chapitre -->
          <section v-if="chapter.endNote.length > 0">
            <BCollapse class="card" animation="slide" aria-id="chapterEndNote">
              <template #trigger="props">
                <div class="card-header" role="button" aria-controls="chapterEndNote" :aria-expanded="props.open">
                  <p class="card-header-title is-unselectable">Notes de fin de chapitre</p>
                  <a class="card-header-icon">
                    <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
                  </a>
                </div>
              </template>

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="chapter.endNote"></p>
                </div>
              </div>
            </BCollapse>
            <br />
          </section>
          <!-- Reviews -->
          <section v-if="chapter">
            <BCollapse v-model="reviewPaneExpanded" class="card" animation="slide" aria-id="chapterReviews">
              <template #trigger>
                <div
                  class="card-header sub-title"
                  role="button"
                  aria-controls="chapterReviews"
                  :aria-expanded="reviewPaneExpanded"
                >
                  <p class="card-header-title is-unselectable">
                    {{ "Reviews (" + (chapter.reviewCount || 0).toString() + ")" }}
                  </p>
                  <a class="card-header-icon">
                    <BIcon
                      class="is-clickable"
                      :icon="reviewPaneExpanded ? 'caret-up' : 'caret-down'"
                      type="is-light"
                    />
                  </a>
                </div>
              </template>

              <div class="card-content pb-0">
                <div class="content p-2">
                  <ReviewsList
                    ref="review-list"
                    :review-list-type="ReviewItemTypeEnum.Chapter"
                    :paginated-reviews
                    :review-pagination
                    :is-loading="reviewsStatus === 'pending'"
                    :post-review="postChapterReview"
                    :capture-editor-target="'#sidebar-editor'"
                    :capture-editor="reviewEditorVisible"
                    @page-change="handleReviewPageChange"
                  />
                </div>
              </div>
            </BCollapse>
            <br />
          </section>
        </div>
      </div>

      <!-- Colonne droite - Editeur review -->
      <div v-if="isAuthenticated" v-show="reviewEditorVisible" class="column is-4">
        <div class="card" style="position: sticky; top: 60px">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Editeur de review</p>
            <button class="delete mr-1 mt-1" @click="reviewEditorVisible = false"></button>
          </header>
          <div class="card-content p-3">
            <div v-if="reviewHeaderMessageVisible" class="notification is-info is-light is-size-6 py-2 pl-2 pr-5">
              <button class="delete is-small" @click="reviewHeaderMessageVisible = false"></button>
              <p>
                Vous avez aimé ce texte ? <strong>Dites-le !</strong> Vous pensez que ce texte peut être amélioré ?
                <strong>Ecrivez-le !</strong>
              </p>
              <p>Avec gentillesse et bienveillance, faites part de votre avis.</p>
            </div>
            <!-- L'éditeur de ReviewList peut se monter là
            TODO - existe-t-il un throwaway tag qui "disparaitrait" quand l'éditeur est monté ici ? -->
            <div id="sidebar-editor"></div>
          </div>
        </div>
      </div>
      <div v-else-if="reviewEditorVisible" class="buttons column is-narrow">
        <BButton
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser une review"
          type="is-primary"
          style="position: sticky; top: 60px"
          @click="modalsStateStore.setLoginModalActive(true)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChapterReviewTypeOffsetPaginated, ChapterTypeOffsetPaginated, OffsetPaginationInput } from "#gql";
import { plainToInstance } from "class-transformer";
import { ChapterModel, ReviewModel, type TableOfContent } from "@/models";
import { ReviewItemTypeEnum } from "@/types/fanfictions";
import type { TipTapEditorConfig, ReviewState } from "@/types/other";

interface Props {
  tableOfContent: TableOfContent;
}

defineProps<Props>();

const route = useRoute();
// const { isAuthenticated } = useCustomAuth();
const isAuthenticated = true;

const modalsStateStore = useModalsStateStore();

const reviewPaneExpanded = ref<boolean>(false);
const reviewEditorVisible = ref<boolean>(false);
const reviewHeaderMessageVisible = ref<boolean>(true);
const fontSizeVisible = ref<boolean>(false);
const reviewState = useState<ReviewState>("reviewState", () => {
  return {
    content: "",
    wordCount: 0,
    canGrade: false,
    grading: undefined,
  };
});

const { data: chapter, status: chapterStatus } = await useAsyncGql(
  "getChapterDetail",
  {
    filters: {
      id: {
        // TODO s'assurer que chapterId ET fictionID sont corrects
        // et que le chapitre appartient bien à la fiction
        // Je ne sais pas quelles répercussions aurait une erreur ou un acte volontaire
        // mais autant éviter de se retrouver dans cette situation
        exact: route.params.chapterId as string,
      },
    },
  },
  {
    transform: (data: { chapters: ChapterTypeOffsetPaginated }) => {
      return plainToInstance(ChapterModel, data.chapters.results[0]);
    },
  },
);

const chapterLoading = computed(() => chapterStatus.value === "pending");

const reviewPagination = reactive<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});
function handleReviewPageChange(page: number): void {
  reviewPagination.offset = (page - 1) * reviewPagination.limit!;
}

// FIXME - les reviews avec de l'html ne passent pas l'hydration !
const { data: paginatedReviews, status: reviewsStatus } = await useAsyncGql(
  "getChapterReviews",
  {
    filters: {
      chapter: {
        id: {
          exact: route.params.chapterId as string,
        },
      },
    },
    pagination: reviewPagination,
  },
  {
    transform: (input: { chapterReviews: ChapterReviewTypeOffsetPaginated }) => {
      return {
        ...input.chapterReviews,
        results: plainToInstance(ReviewModel, input.chapterReviews.results),
      };
    },
  },
);

const tiptapReadOnlyConfig = reactive<TipTapEditorConfig>({
  showFooter: false,
  placeholder: "",
  readOnly: true,
  fixedHeight: false,
  height: 125,
  defaultValue: chapter.value.text || "",
  canQuote: true,
  quoteLimit: 250,
  fontSize: 100,
  oneLineToolbar: false,
  canUseImage: true,
});

async function postChapterReview(): Promise<void> {
  await GqlCreateChapterReview({
    chapterId: Number(route.params.chapterId as string),
    chapterReviewData: {
      text: reviewState.value.content,
      grading: reviewState.value.grading,
    },
  });
}

//   @Watch("$auth.loggedIn", { immediate: true })
//   private onAuthChanged(): void {
//     this.tiptapReadOnlyConfig.canQuote = this.$auth.loggedIn;
//   }

//   @Watch("reviewPaneExpanded", { deep: true })
//   private onreviewPaneExpanded(): void {
//     if (this.reviewPaneExpanded && this.reviewEditorVisible) {
//       if (process.client) {
//         (this.$refs.reviewList as ReviewList)?.setContent(this.editorContentReview);
//       }
//       this.reviewEditorVisible = false;
//     }
//   }

//   @Watch("reviewEditorVisible")
//   public onreviewEditorVisibleChanged(): void {
//     if (this.reviewEditorVisible && this.reviewPaneExpanded) {
//       if (process.client) {
//         (this.$refs.reviewEditorSmall as TipTapEditor)?.setContent(this.editorContentReview);
//       }
//       this.reviewPaneExpanded = false;
//     }
//   }
//   // #endregion

const timerThrottleFontsize = ref<number>(0);

// Augmenter la taille du texte
function upSizeFont(): void {
  if (import.meta.client) {
    tiptapReadOnlyConfig.fontSize += 10;
    displayFontSize();
  }
}

// Restaurer la taille du texte
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
  clearTimeout(timerThrottleFontsize.value);
  timerThrottleFontsize.value = window.setTimeout(() => {
    fontSizeVisible.value = false;
  }, 3000);
}
</script>

<style lang="scss" scoped>
* {
  // border: 1px solid green;
}
</style>
