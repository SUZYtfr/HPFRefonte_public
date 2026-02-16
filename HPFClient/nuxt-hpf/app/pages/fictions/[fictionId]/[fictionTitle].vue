<template>
  <div
    id="main-container"
    class="container pt-3 is-flex is-flex-direction-column is-flex-grow-5"
    style="/*background-color: red; */"
  >
    <b-loading v-if="status === 'pending'" :is-full-page="false" />
    <div class="is-flex-grow-5">
      <!-- Sous page fiction / chapitre -->
      <NuxtPage :table-of-content="tableOfContent" class="px-3" />
    </div>

    <!-- Navigation -->
    <!-- <div class="card">
      <div class="card-content p-2"> -->
    <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
      <!-- Previous -->
      <b-button
        v-if="currentChapter != null"
        type="is-primary"
        icon-left="angle-left"
        tag="router-link"
        :to="PreviousToRouterLink"
      >
        <span class="is-hidden-mobile">{{
          previousChapter != null
            ? (previousChapter?.title ?? "").length > 25
              ? (previousChapter?.title ?? "").substring(0, 25) + "..."
              : previousChapter?.title
            : (tableOfContent?.title ?? "").length > 25
              ? (tableOfContent?.title ?? "").substring(0, 25) + "..."
              : tableOfContent?.title
        }}</span>
      </b-button>
      <!-- Sommaire -->
      <b-dropdown
        v-if="currentChapter != null"
        aria-role="list"
        position="is-top-right"
        :class="[{ 'mr-auto': nextChapter == null }, { 'ml-auto': nextChapter == null }]"
      >
        <template #trigger="{ active }">
          <b-button label="Sommaire" type="is-primary" :icon-right="active ? 'angle-up' : 'angle-down'" />
        </template>
        <b-dropdown-item aria-role="listitem">
          <b-icon icon="book-open" />
          <NuxtLink
            no-prefetch
            class="has-text-weight-normal"
            :to="{
              name: 'fictions-fictionId-fictionTitle-sommaire',
              params: { fictionId: tableOfContent?.id.valueOf(), fictionTitle: tableOfContent?.titleAsSlug },
            }"
          >
            {{ tableOfContent?.title }}
          </NuxtLink>
        </b-dropdown-item>
        <b-dropdown-item v-for="(chapter, index) in tableOfContent?.chapters" :key="index" aria-role="listitem">
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
        </b-dropdown-item>
      </b-dropdown>
      <!-- Next -->
      <b-button
        v-if="nextChapter"
        type="is-primary"
        icon-right="angle-right"
        tag="router-link"
        :to="NextToRouterLink"
        :class="[{ 'ml-auto': currentChapter == null }]"
      >
        <span class="is-hidden-mobile">{{
          (nextChapter?.title ?? "").length > 25
            ? (nextChapter?.title ?? "").substring(0, 25) + "..."
            : nextChapter?.title
        }}</span>
      </b-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FictionTypeOffsetPaginated } from "#gql";
import { plainToInstance } from "class-transformer";
import type { ChapterModelLight } from "~/models";
import { TableOfContent } from "~/models";

const route = useRoute();

const { data: tableOfContent, status } = await useAsyncGql(
  "getTableOfContents",
  {
    fictionId: route.params.fictionId as string,
  },
  {
    transform: (data: { fictions: FictionTypeOffsetPaginated }) => {
      // Pas très beau tout ça, mais ça fonctionne
      const tableOfContent = data.fictions.results[0];
      //@ts-ignore
      tableOfContent.chapters = tableOfContent?.chapters.results;
      return plainToInstance(TableOfContent, data.fictions.results[0]);
    },
  },
);

// const { data: tableOfContent, status } = await getTableOfContent(parseInt(route.params.fictionId as string));

const previousChapter = ref<ChapterModelLight | null>(null);
const currentChapter = ref<ChapterModelLight | null>(null);
const nextChapter = ref<ChapterModelLight | null>(null);

interface RouterLink {
  name: string;
  params: {
    fictionId: string;
    fictionTitle: string;
    chapterId: string | null;
    chapterTitle: string | null;
  };
}

const PreviousToRouterLink = reactive<RouterLink>({
  name: "fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle",
  params: {
    fictionId: tableOfContent.value.fanfictionId.toString(),
    fictionTitle: tableOfContent.value.titleAsSlug,
    chapterId: null,
    chapterTitle: null,
  },
});

const NextToRouterLink = reactive<RouterLink>({
  name: "fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle",
  params: {
    fictionId: tableOfContent.value.fanfictionId.toString(),
    fictionTitle: tableOfContent.value.titleAsSlug,
    chapterId: null,
    chapterTitle: null,
  },
});

effect(() => {
  const currentChapterIndex =
    tableOfContent.value.chapters?.findIndex((c) => c.chapterId.toString() === (route.params.chapterId as string)) ||
    -1;
  if (currentChapterIndex === -1) {
    currentChapter.value = null;

    previousChapter.value = null;
    PreviousToRouterLink.params.chapterId = null;
    PreviousToRouterLink.params.chapterTitle = null;

    nextChapter.value = tableOfContent.value.chapters![currentChapterIndex + 1] ?? null;
    NextToRouterLink.params.chapterId = tableOfContent.value.chapters![0]?.chapterId.toString() ?? null;
    NextToRouterLink.params.chapterTitle = tableOfContent.value.chapters![0]?.titleAsSlug ?? null;
  } else {
    currentChapter.value = tableOfContent.value.chapters![currentChapterIndex]!;

    previousChapter.value = tableOfContent.value.chapters![currentChapterIndex - 1] ?? null;
    PreviousToRouterLink.name = previousChapter.value
      ? "fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle"
      : "fictions-fictionId-fictionTitle-sommaire";
    PreviousToRouterLink.params.chapterId = previousChapter.value?.chapterId.toString() ?? null;
    PreviousToRouterLink.params.chapterTitle = previousChapter.value?.titleAsSlug ?? null;

    nextChapter.value = tableOfContent.value.chapters![currentChapterIndex + 1] ?? null;
    NextToRouterLink.params.chapterId = nextChapter.value?.chapterId.toString() ?? null;
    NextToRouterLink.params.chapterTitle = nextChapter.value?.titleAsSlug ?? null;
  }
});
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom_bulma_core.scss";
* {
  // border: 1px solid green;
}
#main-container {
  background-color: var(--hpf-primary-lighter);
}
</style>
