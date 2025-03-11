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
        v-if="nextChapter != null"
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

const currentChapter = computed(() => {
  if (route.params.chapter_id == null) {
      return null;
    } else {
      return tableOfContent.value.chapters?.find((chapter: ChapterModelLight) => chapter.id === parseInt(route.params.chapter_id[0])) ?? null;
    }
});

const previousChapter = computed(() => {
  if (currentChapter.value == null) {
    return null
  }
  else if (currentChapter.value.order === 1) {
    return null
  }
  else {
    return tableOfContent.value.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((currentChapter.value.order ?? -1) - 1)) ?? null;
  }
});

const nextChapter = computed(() => {
  if (currentChapter.value == null) {
    return tableOfContent.value.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
  } else {
    return tableOfContent.value.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((currentChapter.value.order ?? -1) + 1)) ?? null;
  }
});


const NextToRouterLink = computed(() => {
  if (!nextChapter) return "";
    return { name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title", params: { fiction_id: tableOfContent.value.id.valueOf(), fiction_title: tableOfContent.value.titleAsSlug, chapter_id: nextChapter.value.id.valueOf(), chapter_title: nextChapter.value.titleAsSlug ?? "" } };
});

const PreviousToRouterLink = computed(() => {
  console.log("toto")
  if (!currentChapter) return "";
  else if (currentChapter != null) {
    if ((currentChapter.value.order ?? -1) === 1) {
      return { name: "fictions-fiction_id-fiction_title-sommaire", params: { fiction_id: tableOfContent.value.id.valueOf(), fiction_title: tableOfContent.value.titleAsSlug } };
    } else {
      return { name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title", params: { fiction_id: tableOfContent.value.id.valueOf(), fiction_title: tableOfContent.value.titleAsSlug, chapter_id: previousChapter.value.id.valueOf(), chapter_title: previousChapter.value.titleAsSlug ?? "" } };
    }
  }
});

  // #region Watchers
  // public onItemChanged(): void {
  //   console.log("currentChapterChanged");
  //   if (this.currentChapter == null) {
  //     this.previousChapter = null;
  //     this.nextChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
  //   } else {
  //     if (this.currentChapter.order === 1)
  //       this.previousChapter = null;
  //     else
  //       this.previousChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.currentChapter?.order ?? -1) - 1)) ?? null;
  //     this.nextChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.currentChapter?.order ?? -1) + 1)) ?? null;
  //   }
  // }




// private async fetch(): Promise<void> {
//   this.fictionLoading = true;
//   try {
//     this.tableOfContent = (await getTableOfContent(parseInt(this.$route.params.fiction_id)));
//     this.onRouteChanged();
//   } catch (error) {
//     if (process.client) {
//       this.$buefy.snackbar.open({
//         duration: 5000,
//         message: "Une erreur s'est produite lors de la récupération du sommaire",
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
//     this.fictionLoading = false;
//   }
// }
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
