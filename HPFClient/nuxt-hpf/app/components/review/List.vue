<template>
  <!-- Editeur de review -->
  <div v-if="isAuthenticated">
    <!-- TODO - le conditionnement de l'apparence selon captureEditor est moche,
        trouver un meilleur moyen de rendre l'éditeur responsif -->
    <ClientOnly>
      <Teleport :to="captureEditorTarget" :disabled="!captureEditor" defer>
        <RichtextEditor
          ref="review-editor"
          v-model:text="reviewText"
          v-model:word-count="wordCount"
          :config="tiptapConfig"
        />
        <div :class="[captureEditor ? 'mt-1' : 'm-2', 'is-flex', 'is-flex-direction-row', 'is-flex-wrap-wrap']">
          <BCheckbox v-model="canGrade"> Ajouter une note </BCheckbox>
          <BRate
            v-model="grading"
            icon-pack="fas"
            :max="10"
            :size="captureEditor ? 'default' : 'is-medium'"
            :show-score="canGrade"
            :rtl="false"
            :spaced="true"
            :disabled="!canGrade"
          />
        </div>
        <component
          :is="captureEditor ? 'footer' : 'div'"
          :class="[captureEditor ? 'card-footer py-2' : 'buttons mt-1']"
        >
          <BButton
            :disabled="wordCount < 3"
            :expanded="false"
            label="Poster une review"
            type="is-primary"
            class="mx-auto"
            @click="() => postReview({ text: reviewText, grading: grading })"
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
        <ReviewEntity
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
</template>

<script setup lang="ts" generic="ReviewTypeOffsetPaginated extends ChapterReviewTypeOffsetPaginated">
// le schéma GQL ne contient pas de ReviewTypeOffsetPaginated générique par défaut, mais il est peut-être possible de le faire tout de même
import type { ChapterReviewTypeOffsetPaginated, OffsetPaginationInput, ReviewInput } from "#gql";
import type { ReviewItemTypeEnum } from "~/types/fanfictions";
import type { TipTapEditorConfig, TransformedPaginated } from "~/types/other";
import type { ReviewModel } from "~/models";
import type { TiptapEditor } from "#imports";

interface Props {
  reviewListType: ReviewItemTypeEnum;
  paginatedReviews?: TransformedPaginated<ReviewModel>;
  postReview: (reviewData: ReviewInput) => Promise<void>;
  captureEditorTarget?: string;
  captureEditor?: boolean;
}

defineProps<Props>();

const pagination = defineModel<OffsetPaginationInput>("pagination", { required: true });
const isLoading = defineModel<boolean>("isLoading", { required: false, default: false });

// On fait passer l'éditeur à un potentiel parent qui en voudrait
// Un peu hacky mais ça fonctionne bien
const editorComponent = useTemplateRef("review-editor");
const editor = computed<TiptapEditor | undefined>(() => editorComponent.value?.editor);
defineExpose({ editor: editor });

const reviewText = ref<string>("");
const wordCount = ref<number>(0);
const canGrade = ref<boolean>(false);
const grading = ref<number>();
watch(canGrade, (newValue) => (grading.value = newValue ? 10 : undefined));

const { isAuthenticated } = useCustomAuth();

// Transforme le système offset / limit en page / pageSize
const pageReviewPagination = reactive({
  pageSize: pagination.value.limit!,
  page: pagination.value.offset! / pagination.value.limit! + 1,
});
watch(pageReviewPagination, () => {
  pagination.value.limit = pageReviewPagination.pageSize;
  pagination.value.offset = (pageReviewPagination.page - 1) * pageReviewPagination.pageSize;
});

const tiptapConfig = reactive<TipTapEditorConfig>({
  showFooter: false,
  placeholder: "Écrivez votre review ici",
  fixedHeight: true,
  height: 250,
  oneLineToolbar: true,
  canUseImage: false,
});

const listLoading = computed(() => isLoading.value);
</script>
