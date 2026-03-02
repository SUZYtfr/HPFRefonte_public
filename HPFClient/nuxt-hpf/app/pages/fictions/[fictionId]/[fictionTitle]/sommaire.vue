<template>
  <div>
    <!-- Détail de la fiction -->
    <section>
      <div class="card">
        <header class="card-header sub-title">
          <p class="card-header-title is-centered has-text-centered">
            {{ fiction.title }}
          </p>
        </header>
        <div class="card-content" style="padding: 5px; padding-top: 2px; padding-bottom: 0px">
          <FictionsEntity
            :key="'ff_' + fiction.fanfictionId.toString()"
            class="my-2"
            :fanfiction="fiction"
            :config="{ inList: false }"
          />
        </div>
      </div>
      <br />
    </section>

    <!-- Notes de fiction -->
    <section>
      <BCollapse class="card" animation="slide" aria-id="fictionNotes">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionNotes" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Notes de fiction</p>
            <a class="card-header-icon">
              <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content">
          <div class="content p-2">
            <!-- FIXME erreur d'hydration -->
            {{ fiction.storynote }}
          </div>
        </div>
      </BCollapse>
      <br />
    </section>

    <!-- Trigger warning -->
    <article v-if="fiction.triggerWarnings?.length ?? 0 > 0" class="message is-danger">
      <div class="message-body py-1 px-2">
        <div class="is-flex is-flex-direction-row">
          <BIcon icon="exclamation-triangle" /><span><strong> TW / CW </strong></span>
        </div>
        <p>
          <template v-for="(tw, index) in fiction.triggerWarnings" :key="index">
            <ul>
              <li>{{ tw.name }}</li>
            </ul>
          </template>
        </p>
      </div>
    </article>

    <!-- Sommaire -->
    <section>
      <BCollapse class="card" animation="slide" aria-id="fictionTableOfContent">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionTableOfContent" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Sommaire</p>
            <a class="card-header-icon">
              <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-2">
          <div class="content p-2">
            <div
              v-for="(chapter, index) in tableOfContent.chapters"
              :key="index"
              class="is-flex is-flex-direction-row is-justify-content-center"
            >
              <NuxtLink
                no-prefetch
                class="has-text-weight-normal"
                :to="{
                  name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
                  params: {
                    fictionId: tableOfContent.id,
                    fictionTitle: tableOfContent.titleAsSlug,
                    chapterId: chapter.chapterId,
                    chapterTitle: chapter.titleAsSlug,
                  },
                }"
              >
                {{ chapter.title }}
              </NuxtLink>
              <div v-if="chapter.triggerWarnings?.length || 0 > 0" class="b-tooltips ml-2">
                <BTooltip type="is-danger" position="is-right">
                  <BIcon icon="exclamation-triangle" size="is-small" type="is-danger" class="mr-1" />
                  <template #content>
                    {{ chapter.triggerWarnings?.map((tw) => tw.name).join(", ") }}
                  </template>
                </BTooltip>
              </div>
              <br />
            </div>
          </div>
        </div>
      </BCollapse>
      <br />
    </section>

    <!-- Reviews -->
    <section v-if="fiction">
      <BCollapse class="card" animation="slide" aria-id="fictionReviews">
        <template #trigger="props">
          <div class="card-header sub-title" role="button" aria-controls="fictionReviews" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">
              {{ "Reviews (" + (fiction.reviewCount || 0).toString() + ")" }}
            </p>
            <a class="card-header-icon">
              <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
            </a>
          </div>
        </template>

        <div class="card-content pb-0">
          <div class="content p-2">
            <ReviewsList
              ref="review-list"
              :review-list-type="ReviewItemTypeEnum.Fanfiction"
              :paginated-reviews
              :review-pagination
              :is-loading="reviewsStatus === 'pending'"
              :post-review
              @pagination-change="(pagination: OffsetPaginationInput) => (reviewPagination = pagination)"
            />
          </div>
        </div>
      </BCollapse>
      <br />
    </section>
  </div>
</template>

<script setup lang="ts">
import type { FictionReviewTypeOffsetPaginated, FictionType, OffsetPaginationInput } from "#gql";
import { FanfictionModel, ReviewModel, type TableOfContent } from "@/models";
import { ReviewItemTypeEnum } from "@/types/fanfictions";
import type { ReviewState } from "@/types/other";
import { plainToInstance } from "class-transformer";

const { tableOfContent } = defineProps<{
  tableOfContent: TableOfContent;
}>();

const route = useRoute();

const reviewState = useState<ReviewState>("reviewState");

const { data: fiction } = await useAsyncGql(
  "getFictionDetail",
  {
    fictionId: route.params.fictionId as string,
    // withAuthors: true,
  },
  {
    transform: (input: { fiction: FictionType }) => {
      return plainToInstance(FanfictionModel, input.fiction);
    },
  },
);

const reviewPagination = ref<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});

// FIXME - les reviews avec de l'html ne passent pas l'hydration !
const { data: paginatedReviews, status: reviewsStatus } = await useAsyncGql(
  "getFictionReviews",
  {
    filters: {
      fiction: {
        id: {
          exact: route.params.fictionId as string,
        },
      },
    },
    pagination: reviewPagination,
  },
  {
    lazy: true,
    transform: (input: { fictionReviews: FictionReviewTypeOffsetPaginated }) => {
      return {
        ...input.fictionReviews,
        results: plainToInstance(ReviewModel, input.fictionReviews.results),
      };
    },
  },
);

async function postReview(): Promise<void> {
  await GqlCreateFictionReview({
    fictionId: route.params.fictionId as string,
    fictionReviewData: {
      text: reviewState.value.content,
      grading: reviewState.value.grading,
    },
  });
}

useHead({
  title: "HPF - " + fiction.value.title,
});
</script>

<style lang="scss" scoped>
ul {
  list-style: inside;
}
</style>
