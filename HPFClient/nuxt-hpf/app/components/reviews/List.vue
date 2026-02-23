<template>
  <div>
    <div>
      <!-- Editeur de review -->
      <div v-if="isAuthenticated">
        <!-- TODO - le conditionnement de l'apparence selon captureEditor est moche,
        trouver un meilleur moyen de rendre l'éditeur responsif -->
        <ClientOnly>
          <Teleport :to="captureEditorTarget" :disabled="!captureEditor" defer>
            <CustomEditor ref="review-editor" :config="tiptapConfig" />
            <div :class="[captureEditor ? 'mt-1' : 'm-2', 'is-flex', 'is-flex-direction-row', 'is-flex-wrap-wrap']">
              <BCheckbox v-model="reviewState.canGrade"> Ajouter une note </BCheckbox>
              <BRate
                v-model="reviewState.grading"
                icon-pack="fas"
                :max="10"
                :size="captureEditor ? 'default' : 'is-medium'"
                :show-score="reviewState.canGrade"
                :rtl="false"
                :spaced="true"
                :disabled="!reviewState.canGrade"
              />
            </div>
            <component
              :is="captureEditor ? 'footer' : 'div'"
              :class="[captureEditor ? 'card-footer py-2' : 'buttons mt-1']"
            >
              <BButton
                :disabled="reviewState.wordCount < 3"
                :expanded="false"
                label="Poster une review"
                type="is-primary"
                class="mx-auto"
                @click="postReview"
              />
            </component>
          </Teleport>
        </ClientOnly>
      </div>
      <div v-else class="buttons mt-1 is-centered">
        <BButton
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser une review"
          type="is-primary"
          @click="useModalsStateStore().setLoginModalActive(true)"
        />
      </div>

      <!-- Liste paginée des reviews -->
      <div>
        <BLoading v-model="listLoading" :is-full-page="false" />
        <div class="px-2 py-3 is-flex-grow-5">
          <div v-if="!paginatedReviews?.totalCount" class="mx-auto my-auto has-text-centered">
            <span class="is-italic mt-3">Aucune review, soyez le premier !</span>
          </div>
          <div v-else>
            <ReviewsEntity
              v-for="(review, innerindex) of paginatedReviews?.results"
              :key="'rv_' + review.reviewId.toString()"
              class="my-2"
              :review="review"
              :index="innerindex"
            />
          </div>
        </div>
        <footer>
          <BPagination
            v-model="pageReviewPagination.page"
            class="py-2"
            :total="paginatedReviews?.totalCount"
            :range-before="3"
            :range-after="1"
            :rounded="false"
            :per-page="pageReviewPagination.pageSize"
            icon-prev="chevron-left"
            icon-next="chevron-right"
            aria-next-label="Page suivante"
            aria-previous-label="Page précedente"
            aria-page-label="Page"
            aria-current-label="Page actuelle"
            @change="(page: number) => (pageReviewPagination.page = page)"
          />
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" generic="ReviewTypeOffsetPaginated extends ChapterReviewTypeOffsetPaginated">
// le schéma GQL ne contient pas de ReviewTypeOffsetPaginated générique par défaut, mais il est peut-être possible de le faire tout de même
import type { ChapterReviewTypeOffsetPaginated, OffsetPaginationInput, ReviewInput } from "#gql";
import type { ReviewItemTypeEnum } from "@/types/fanfictions";
import type { TipTapEditorConfig, ReviewState } from "@/types/other";
import type { ReviewModel } from "@/models";
import type { TiptapEditor } from "#imports";

interface Props {
  isLoading: boolean;
  reviewListType: ReviewItemTypeEnum;
  paginatedReviews?: Omit<ReviewTypeOffsetPaginated, "results"> & { results: ReviewModel[] };
  reviewPagination: OffsetPaginationInput;
  postReview: (reviewData: ReviewInput) => Promise<void>;
  captureEditorTarget?: string;
  captureEditor?: boolean;
}

const { isLoading, reviewPagination } = defineProps<Props>();

// On fait passer l'éditeur à un potentiel parent qui en voudrait
// Un peu hacky mais ça fonctionne bien
const editorComponent = useTemplateRef("review-editor");
const editor = computed<TiptapEditor | undefined>(() => editorComponent.value?.editor);
defineExpose({ editor: editor });

// Cet état permet de partager en temps réel le contenu de l'éditeur de review
// (en bas et sur le côté) avec les composants qui en dépendent, en y
// ajoutant les informations de notation également
// FIXME - l'état persiste à la navigation entre les éditeurs de review de fiction / chapitres
// trouver comment 1) alerter de la perte du contenu, 2) remettre l'état à zéro
const reviewState = useState<ReviewState>("reviewState", () => {
  return {
    content: "",
    wordCount: 0,
    canGrade: false,
    grading: undefined,
  };
});
watch(
  () => reviewState.value.canGrade,
  () => (reviewState.value.grading = reviewState.value.canGrade ? 10 : undefined),
);
watch(
  () => editor.value?.getHTML(),
  () => {
    reviewState.value.content = editor.value?.getHTML() || "";
    reviewState.value.wordCount = editor.value?.extensionStorage.characterCount.words() || 0;
  },
);

// const { isAuthenticated } = useCustomAuth();
const isAuthenticated = true;

const emit = defineEmits(["pagination-change"]);

// Transforme le système offset / limit en page / pageSize
const pageReviewPagination = reactive({
  pageSize: reviewPagination.limit!,
  page: reviewPagination.offset! / reviewPagination.limit! + 1,
});
watch(pageReviewPagination, () => {
  const pagination: OffsetPaginationInput = {
    limit: pageReviewPagination.pageSize,
    offset: (pageReviewPagination.page - 1) * pageReviewPagination.pageSize,
  };
  emit("pagination-change", pagination);
});

const tiptapConfig = reactive<TipTapEditorConfig>({
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
  canUseImage: false,
});

const listLoading = computed(() => isLoading);
</script>
