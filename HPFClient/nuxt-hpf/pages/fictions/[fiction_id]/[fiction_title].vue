<template>
  <div id="main-container" class="container pt-3 is-flex is-flex-direction-column is-flex-grow-5" style="/*background-color: red; */">
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
        <span class="is-hidden-mobile">{{ (previousChapter != null ? ((previousChapter?.title ?? "").length > 25 ? (previousChapter?.title ?? "").substring(0,25) + "..." : previousChapter?.title) : ((tableOfContent?.title ?? "").length > 25 ? (tableOfContent?.title ?? "").substring(0,25) + "..." : tableOfContent?.title)) }}</span>
      </b-button>
      <!-- Sommaire -->
      <b-dropdown v-if="currentChapter != null" aria-role="list" position="is-top-right" :class="[{'mr-auto': nextChapter == null }, {'ml-auto': nextChapter == null }]">
        <template #trigger="{ active }">
          <b-button
            label="Sommaire"
            type="is-primary"
            :icon-right="active ? 'angle-up' : 'angle-down'"
          />
        </template>
        <b-dropdown-item aria-role="listitem">
          <b-icon icon="book-open" />
          <NuxtLink
            no-prefetch
            class="has-text-weight-normal"
            :to="{ name: 'fictions-fiction_id-fiction_title-sommaire', params: { fiction_id: tableOfContent?.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug }}"
          >
            {{ tableOfContent?.title }}
          </NuxtLink>
        </b-dropdown-item>
        <b-dropdown-item v-for="(chapter, index) in tableOfContent?.chapters" :key="index" aria-role="listitem">
          <NuxtLink
            no-prefetch
            class="has-text-weight-normal"
            :to="{ name: 'fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title', params: { fiction_id: tableOfContent?.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug, chapter_id: chapter.id.valueOf(), chapter_title: chapter.titleAsSlug ?? ''}}"
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
        :class="[{'ml-auto': (currentChapter == null) }]"
      >
        <span class="is-hidden-mobile">{{ ((nextChapter?.title ?? "").length > 25 ? (nextChapter?.title ?? "").substring(0,25) + "..." : nextChapter?.title) }}</span>
      </b-button>
    </div>
    <!-- </div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { getTableOfContent } from "~/api/fanfictions";
import { TableOfContent, ChapterModelLight } from "~/models/fanfictions";

const route = useRoute();

const { data: tableOfContent, status } = await getTableOfContent(parseInt(route.params.fiction_id as string));

const previousChapter = ref<ChapterModelLight>(null);
const currentChapter = ref<ChapterModelLight>(null);
const nextChapter = ref<ChapterModelLight>(null);

const PreviousToRouterLink = reactive({
  name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title",
  params: {
    fiction_id: tableOfContent.value.fanfiction_id.toString(),
    fiction_title: tableOfContent.value.titleAsSlug,
    chapter_id: null,
    chapter_title: null,
  }
})

const NextToRouterLink = reactive({
  name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title",
  params: {
    fiction_id: tableOfContent.value.fanfiction_id.toString(),
    fiction_title: tableOfContent.value.titleAsSlug,
    chapter_id: null,
    chapter_title: null,
  }
})

effect(() => {
  const currentChapterIndex = tableOfContent.value.chapters.findIndex((c) => c.chapter_id.toString() === route.params.chapter_id as string);
  if(currentChapterIndex === -1) {
    currentChapter.value = null;

    previousChapter.value = null;
    PreviousToRouterLink.params.chapter_id = null;
    PreviousToRouterLink.params.chapter_title = null;
   
    nextChapter.value = tableOfContent.value.chapters[currentChapterIndex + 1] ?? null;
    NextToRouterLink.params.chapter_id = tableOfContent.value.chapters[0]?.chapter_id.toString() ?? null;
    NextToRouterLink.params.chapter_title = tableOfContent.value.chapters[0]?.titleAsSlug ?? null;
  }
  else {
    currentChapter.value = tableOfContent.value.chapters[currentChapterIndex];

    previousChapter.value = tableOfContent.value.chapters[currentChapterIndex - 1] ?? null;
    PreviousToRouterLink.name = previousChapter.value ? "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title": "fictions-fiction_id-fiction_title-sommaire";
    PreviousToRouterLink.params.chapter_id = previousChapter.value?.chapter_id.toString() ?? null;
    PreviousToRouterLink.params.chapter_title = previousChapter.value?.titleAsSlug ?? null;
    
    nextChapter.value = tableOfContent.value.chapters[currentChapterIndex + 1] ?? null;
    NextToRouterLink.params.chapter_id = nextChapter.value?.chapter_id.toString() ?? null;
    NextToRouterLink.params.chapter_title = nextChapter.value?.titleAsSlug ?? null;
  }
})
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom_bulma_core.scss";
*{
  // border: 1px solid green;
}
#main-container{
  background-color: var(--hpf-primary-lighter);
}
</style>
