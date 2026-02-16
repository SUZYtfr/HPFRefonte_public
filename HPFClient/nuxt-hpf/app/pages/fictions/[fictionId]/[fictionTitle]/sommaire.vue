<template>
  <div>
    <!-- Détail de la fiction -->
    <section v-if="fiction != null">
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
            :config="fanfictionEntityConfig"
          />
        </div>
      </div>
      <br />
    </section>

    <!-- Notes de fiction -->
    <section>
      <b-collapse class="card" animation="slide" aria-id="fictionNotes">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionNotes" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Notes de fiction</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content">
          <div class="content p-2">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nec iaculis mauris.
          </div>
        </div>
      </b-collapse>
      <br />
    </section>

    <!-- Trigger warning -->
    <article v-if="fictionTriggerWarnings().length > 0" class="message is-danger">
      <div class="message-body py-1 px-2">
        <div class="is-flex is-flex-direction-row">
          <b-icon icon="exclamation-triangle" /><span><strong> TW / CW </strong></span>
        </div>
        <p>
          <template v-for="(tw, index) in fictionTriggerWarnings()" :key="index">
            <ul>
              <li>{{ tw.caption }}</li>
            </ul>
          </template>
        </p>
      </div>
    </article>

    <!-- Sommaire -->
    <section>
      <b-collapse class="card" animation="slide" aria-id="fictionTableOfContent">
        <template #trigger="props">
          <div class="card-header" role="button" aria-controls="fictionTableOfContent" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">Sommaire</p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-2">
          <div class="content p-2">
            <div
              v-for="(chapter, index) in tableOfContent?.chapters"
              :key="index"
              class="is-flex is-flex-direction-row is-justify-content-center"
            >
              <NuxtLink
                no-prefetch
                class="has-text-weight-normal"
                :to="{
                  name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
                  params: {
                    fictionId: tableOfContent?.id.valueOf(),
                    fictionTitle: tableOfContent?.titleAsSlug,
                    chapterId: chapter.id.valueOf(),
                    chapterTitle: chapter.titleAsSlug ?? '',
                  },
                }"
              >
                {{ chapter.title }}
              </NuxtLink>
              <div
                v-if="(chapter?.triggerWarningsLoaded?.length ?? 0) > 0"
                class="is-danger ml-2 is-flex is-flex-direction-row is-align-items-baseline"
              >
                <b-icon icon="exclamation-triangle" size="is-small" type="is-danger" class="mr-1" />
                <div v-for="(triggerWarning, index) in chapter.triggerWarningsLoaded" :key="index">
                  <span v-if="index > 0"> , </span>
                  <span class="has-text-danger">{{ triggerWarning.caption }}</span>
                </div>
              </div>
              <br />
            </div>
          </div>
        </div>
      </b-collapse>
      <br />
    </section>

    <!-- Reviews -->
    <section v-if="fiction != null">
      <b-collapse class="card" animation="slide" aria-id="fictionReviews">
        <template #trigger="props">
          <div class="card-header sub-title" role="button" aria-controls="fictionReviews" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">
              {{ "Reviews (" + fiction?.reviewCount?.toString() + ")" }}
            </p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
            </a>
          </div>
        </template>

        <div class="card-content pb-0">
          <div class="content p-2">
            <!-- <ReviewList ref="reviewList" :item_id="reviewListItemId" :review-list-type="reviewListType" /> -->
          </div>
        </div>
      </b-collapse>
      <br />
    </section>
  </div>
</template>

<script setup lang="ts">
import type { FanfictionEntityConfig, TableOfContent, ChapterModelLight } from "~/models";
import { FanfictionModel } from "~/models";
import { ReviewItemTypeEnum } from "~/types/fanfictions";
// import ReviewList from "~/components/list/reviews/ReviewList.vue";
import { plainToInstance } from "class-transformer";

// FIXME - Fonctionne mais avec mismatch d'hydration, pourquoi ?

const { tableOfContent } = defineProps<{
  tableOfContent?: TableOfContent;
}>();

const route = useRoute();

const { data: fiction } = await useAsyncGql(
  "getFictions",
  {
    filters: {
      id: {
        exact: route.params.fictionId as string,
      },
    },
    pagination: {
      limit: 1,
    },
    withAuthors: true,
  },
  {
    transform: (input) => {
      return plainToInstance(FanfictionModel, input.fictions.results[0]);
    },
  },
);

const reviewListItemId = computed(() => {
  return fiction.value.fanfictionId;
});
const reviewListType = computed(() => {
  return fiction.value ? ReviewItemTypeEnum.Fanfiction : ReviewItemTypeEnum.Chapter;
});

// Pas utilisé ?
// const fictionLoading = ref<boolean>(false);
// const reviewEditorVisible = ref<boolean>(false);

// TODO potentielle reactif?
const fanfictionEntityConfig: FanfictionEntityConfig = {
  inList: false,
};

function fictionTriggerWarnings(): { id: number; caption: string }[] {
  let triggerWarningsGrouped: { id: number; caption: string }[] = [];
  tableOfContent?.chapters
    ?.filter((t: ChapterModelLight) => (t.triggerWarnings?.length ?? 0) > 0)
    .forEach((t: ChapterModelLight) => triggerWarningsGrouped.push(...t.triggerWarningsLoaded));
  triggerWarningsGrouped = triggerWarningsGrouped.filter(
    (value, index, self) => index === self.findIndex((t) => t.id === value.id),
  );
  return triggerWarningsGrouped;
}
</script>

<style lang="scss" scoped>
* {
  // border: 1px solid green;
}

ul {
  list-style: inside;
}
</style>
