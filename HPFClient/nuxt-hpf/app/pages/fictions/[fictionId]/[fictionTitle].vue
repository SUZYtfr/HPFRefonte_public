<template>
  <div
    id="main-container"
    class="container pt-3 is-flex is-flex-direction-column is-flex-grow-5"
    style="/*background-color: red; */"
  >
    <BLoading v-if="status === 'pending'" :is-full-page="false" />
    <div class="is-flex-grow-5">
      <!-- Sous page fiction / chapitre -->
      <NuxtPage :table-of-content="tableOfContent" class="px-3" />
    </div>

    <!-- Navigation -->
    <!-- <div class="card">
      <div class="card-content p-2"> -->
    <div class="p-2 is-flex is-flex-direction-row is-justify-content-space-between">
      <!-- Previous -->
      <BButton
        v-if="previousChapter !== undefined"
        type="is-primary"
        icon-left="angle-left"
        tag="router-link"
        :to="{
          name: previousChapter
            ? 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle'
            : 'fictions-fictionId-fictionTitle-sommaire',
          params: {
            fictionId: tableOfContent.id,
            fictionTitle: tableOfContent.titleAsSlug,
            chapterId: previousChapter?.chapterId.toString(),
            chapterTitle: previousChapter?.titleAsSlug,
          },
        }"
      >
        <span class="is-hidden-mobile">{{
          previousChapter
            ? (previousChapter.title || "").length > 25
              ? (previousChapter.title || "").substring(0, 25) + "..."
              : previousChapter.title
            : (tableOfContent.title || "").length > 25
              ? (tableOfContent.title || "").substring(0, 25) + "..."
              : tableOfContent.title
        }}</span>
      </BButton>
      <!-- Sommaire -->
      <BDropdown
        v-if="currentChapter"
        aria-role="list"
        position="is-top-right"
        :class="[{ 'mr-auto': nextChapter == null }, { 'ml-auto': nextChapter == null }]"
      >
        <template #trigger="{ active }">
          <BButton label="Sommaire" type="is-primary" :icon-right="active ? 'angle-up' : 'angle-down'" />
        </template>
        <BDropdownItem aria-role="listitem" has-link>
          <NuxtLink
            no-prefetch
            class="has-text-weight-normal dropdown-item"
            :to="{
              name: 'fictions-fictionId-fictionTitle-sommaire',
              params: { fictionId: tableOfContent.fanfictionId.toString(), fictionTitle: tableOfContent.titleAsSlug },
            }"
          >
            <BIcon icon="book-open" /> {{ tableOfContent.title }}
          </NuxtLink>
        </BDropdownItem>
        <BDropdownItem v-for="(chapter, index) in tableOfContent.chapters" :key="index" aria-role="listitem" has-link>
          <NuxtLink
            no-prefetch
            class="has-text-weight-normal dropdown-item"
            :to="{
              name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
              params: {
                fictionId: tableOfContent.fanfictionId.toString(),
                fictionTitle: tableOfContent.titleAsSlug,
                chapterId: chapter.chapterId.toString(),
                chapterTitle: chapter.titleAsSlug,
              },
            }"
          >
            {{ chapter.title }}
          </NuxtLink>
        </BDropdownItem>
      </BDropdown>
      <!-- Next -->
      <BButton
        v-if="nextChapter"
        type="is-primary"
        icon-right="angle-right"
        tag="router-link"
        :to="{
          name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
          params: {
            fictionId: tableOfContent.id,
            fictionTitle: tableOfContent.titleAsSlug,
            chapterId: nextChapter.chapterId.toString(),
            chapterTitle: nextChapter.titleAsSlug,
          },
        }"
        :class="[{ 'ml-auto': currentChapter == null }]"
      >
        <span class="is-hidden-mobile">{{
          (nextChapter.title || "").length > 25 ? (nextChapter.title || "").substring(0, 25) + "..." : nextChapter.title
        }}</span>
      </BButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FictionType } from "#gql";
import { plainToInstance } from "class-transformer";
import { TableOfContent, type ChapterModelLight } from "@/models";

const route = useRoute();

const { data: tableOfContent, status } = await useAsyncGql(
  "getTableOfContents",
  {
    fictionId: route.params.fictionId as string,
  },
  {
    transform: (input: { fiction: FictionType }) => {
      // @ts-ignore
      input.fiction.chapters = input.fiction.chapters.results;
      return plainToInstance(TableOfContent, input.fiction);
    },
  },
);

const currentChapter = computed<ChapterModelLight | null>(() => {
  return route.params.chapterId
    ? tableOfContent.value.chapters!.find((c) => c.id === route.params.chapterId) || null
    : null;
});

// si premier chapitre => null (sommaire)
// si chapitre subséquent => ChapterModelLight (chapitre précédent)
// si sommaire => undefined (rien avant le sommaire)
const previousChapter = computed<ChapterModelLight | null | undefined>(() => {
  if (currentChapter.value) {
    const chapterPosition = tableOfContent.value.chapters!.indexOf(currentChapter.value);
    if (chapterPosition > 0) {
      return tableOfContent.value.chapters![chapterPosition - 1]!;
    } else {
      return null;
    }
  } else {
    return undefined;
  }
});

// si chapitre => chapitre suivant ou undefined
// si sommaire => premier chapitre
const nextChapter = computed<ChapterModelLight | undefined>(() => {
  if (currentChapter.value) {
    const chapterPosition = tableOfContent.value.chapters!.indexOf(currentChapter.value);
    if (chapterPosition > tableOfContent.value.chapters!.length) {
      return undefined;
    } else {
      return tableOfContent.value.chapters![chapterPosition + 1]!;
    }
  } else {
    return tableOfContent.value.chapters![0]!;
  }
});
</script>

<style lang="scss" scoped>
@use "@/assets/scss/custom_bulma_core.scss";
#main-container {
  background-color: var(--hpf-primary-lighter);
}
</style>
