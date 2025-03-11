<template>
  <div>
    <div>
      <!-- Editeur de review -->
      <div v-if="$auth.loggedIn">
        <client-only>
          <TipTapEditor ref="reviewEditor" :config="tiptapConfig" @change="(value) => (editorContent = value)" />
        </client-only>
        <div class="m-2 is-flex is-flex-direction-row is-flex-wrap-wrap">
          <b-checkbox v-model="canRate">
            Ajouter une note à votre review
          </b-checkbox>
          <b-rate
            v-model="reviewRating"
            icon-pack="fas"
            :max="10"
            size="is-medium"
            :show-score="canRate"
            :rtl="false"
            :spaced="true"
            :disabled="!canRate"
          />
        </div>
        <div class="buttons mt-1">
          <b-button
            :disabled="(editorContent?.wordcount ?? 0) < 3"
            :expanded="false"
            label="Poster une review"
            type="is-primary"
            class=" mx-auto"
            @click="PostReview"
          />
        </div>
      </div>
      <div v-else class="buttons mt-1 is-centered">
        <b-button
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser une review"
          type="is-primary"
          @click="ModalsStatesModule.setLoginModalActive(true)"
        />
      </div>

      <!-- Liste paginée des reviews -->
      <div>
        <b-loading v-model="listLoading" :is-full-page="false" />
        <div class="px-2 py-3 is-flex-grow-5">
          <div
            v-if="(reviews?.count ?? 0) == 0"
            class="mx-auto my-auto has-text-centered"
          >
            <span class="is-italic mt-3">Aucune review, soyez le premier !</span>
          </div>
          <div v-else>
            <Review
              v-for="(review, innerindex) of reviews.results"
              :key="'rv_' + review.review_id.toString()"
              class="my-2"
              :review="review"
              :index="innerindex"
            />
          </div>
        </div>
        <footer>
          <b-pagination
            v-model="reviewFilters.page"
            class="py-2"
            :total="totalReviews"
            :range-before="3"
            :range-after="1"
            :rounded="false"
            :per-page="reviewFilters.pageSize"
            icon-prev="chevron-left"
            icon-next="chevron-right"
            aria-next-label="Page suivante"
            aria-previous-label="Page précedente"
            aria-page-label="Page"
            aria-current-label="Page actuelle"
          />
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { searchChapterReviews, searchCollectionReviews, searchFictionReviews, postChapterReview, postChapterReviewReply, postCollectionReview, postCollectionReviewReply, postFictionReview, postFictionReviewReply } from "~/api/reviews";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";
import { ReviewModel } from "~/models/fanfictions";
import { ReviewItemTypeEnum } from "@/types/fanfictions";
import { SortByEnum } from "~/types/basics";
import Review from "~/components/entities/review.vue";

interface Props {
  item_id?: number;
  totalReviews?: number;
  isLoading?: boolean;
  reviewListType?: ReviewItemTypeEnum;
}
const { item_id, totalReviews, isLoading, reviewListType } = defineProps<Props>();

// TODO Un truc qui fait pas pleurer
let searchReviews: typeof searchChapterReviews | typeof searchFictionReviews | typeof searchCollectionReviews
switch (reviewListType) {
  case ReviewItemTypeEnum.Chapter:
    searchReviews = searchChapterReviews;
    break;
  case ReviewItemTypeEnum.Fanfiction:
    searchReviews = searchFictionReviews;
    break;
  case ReviewItemTypeEnum.Serie:
    searchReviews = searchCollectionReviews;
    break;
}

const { data: reviews, status } = await searchReviews(item_id, null)
// const reviews = searchReviews(item_id, reviewFilters)
const listLoading = computed(() => status.value === 'pending')

const ModalsStatesModule = ModalsStates();

  // public editorContent: TipTapEditorContent | null = null;
  // public canRate: boolean = false;
  // public reviewRating: number | null = null;

// TODO faire réactif
const reviewFilters = {
  page: 1,
  pageSize: 10,
  totalPages: false,
  sortBy: SortByEnum.Descending,
  sortOn: "post_date"
};

  // public tiptapConfig: TipTapEditorConfig = {
  //   showFooter: false,
  //   placeholder: "Ecrire un commentaire",
  //   readOnly: false,
  //   fixedHeight: true,
  //   defaultValue: "",
  //   canQuote: false,
  //   quoteLimit: 0,
  //   fontSize: 100,
  //   height: 300,
  //   oneLineToolbar: false,
  //   canUseImage: false
  // };

  // private timerId: number = 0;
  // // #endregion

  // get listLoading(): boolean {
  //   return this.isLoading ?? false;
  // }

  // set listLoading(value) {
  //   this.$emit("loadingChange", value);
  // }

  // // #endregion

  // // #region Watchers
  // @Watch("reviewFilters", { deep: true })
  // public onFiltersChanged(): void {
  //   clearTimeout(this.timerId);
  //   this.timerId = window.setTimeout(this.$fetch, 500);
  // }

  // @Watch("canRate")
  // public onCanRateChanged(): void {
  //   this.reviewRating = (this.canRate ? 10 : null);
  // }

  // // @Watch("propEditorContent")
  // // public onpropEditorContentChanged(): void {
  // //   if (process.client) {
  // //     (this.$refs.reviewEditor as TipTapEditor)?.setContent(this.propEditorContent);
  // //   }
  // // }

  // @Watch("editorContent")
  // public oneditorContentChanged(): void {
  //   this.$emit("reviewContentChanged", this.editorContent);
  // }

  // // #endregion

  // // #region Methods
  // private async getReviews(): Promise<void> {
  //   if (this.item_id == null) return;
  //   try {
  //     // if (this.reviewFilters == null || this.reviewFilters.item_id <= 0) return;
  //     let response;
  //     switch (this.reviewListType) {
  //       case ReviewItemTypeEnum.Chapter:
  //         response = (await searchChapterReviews(this.item_id, this.reviewFilters));
  //         break;
  //       case ReviewItemTypeEnum.Fanfiction:
  //         response = (await searchFictionReviews(this.item_id, this.reviewFilters));
  //         break;
  //       case ReviewItemTypeEnum.Serie:
  //         response = (await searchCollectionReviews(this.item_id, this.reviewFilters));
  //         break;
  //     }
  //     this.reviews = response.results;
  //     this.reviewFilters.page = response.current;
  //   } catch (error) {
  //     if (process.client) {
  //       this.$buefy.snackbar.open({
  //         duration: 5000,
  //         message: "Une erreur s'est produite lors de la récupération des reviews",
  //         type: "is-danger",
  //         position: "is-bottom-right",
  //         actionText: null,
  //         pauseOnHover: true,
  //         queue: true
  //       });
  //     } else {
  //       console.log(error);
  //     }
  //   } finally {
  //     // Rien
  //   }
  // }

  // public async PostReview(): Promise<void> {
  //   if (this.item_id == null) return;
  //   if (this.reviewListType == null) return;
  //   if ((this.editorContent?.wordcount ?? 0) < 3) return;
  //   if (this.editorContent?.content == null) return;
  //   try {
  //     let review: ReviewModel = new ReviewModel();
  //     review.text = this.editorContent?.content;
  //     review.grading = this.reviewRating;
  //     review.review_item_type_id = this.reviewListType;
  //     review.item_id = this.item_id;
  //     review.is_draft = false;
  //     switch (this.reviewListType) {
  //       case ReviewItemTypeEnum.Chapter:
  //         review = (await postChapterReview(this.item_id, review)).items;
  //         break;
  //       case ReviewItemTypeEnum.Fanfiction:
  //         review = (await postFictionReview(this.item_id, review)).items;
  //         break;
  //       case ReviewItemTypeEnum.Serie:
  //         review = (await postCollectionReview(this.item_id, review)).items;
  //         break;
  //     }
  //     if (review != null) this.reviews?.push(review);
  //   } catch (error) {
  //     console.log(error);
  //   }
  // }

  // // Changer le contenu de l'éditeur
  // public setContent(tiptapContent: TipTapEditorContent | null): void {
  //   if (process.client) {
  //     (this.$refs.reviewEditor as TipTapEditor)?.setContent(tiptapContent);
  //   }
  // }

  // // Quoter dans l'éditeur
  // public setQuote(quote: string): void {
  //   if (process.client) {
  //     (this.$refs.reviewEditor as TipTapEditor)?.setQuote(quote);
  //   }
  // }
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

</style>
