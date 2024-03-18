<template>
  <div id="main-container" class="container pt-3 is-flex is-flex-direction-column is-flex-grow-5" style="/*background-color: red; */">
    <b-loading v-model="fictionLoading" :is-full-page="false" />
    <div class="is-flex-grow-5">
      <!-- Sous page fiction / chapitre -->
      <NuxtChild :table-of-content="tableOfContent" class="px-3" />
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
            class="has-text-weight-normal"
            :to="{ name: 'fictions-fiction_id-fiction_title-sommaire', params: { fiction_id: tableOfContent?.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug }}"
          >
            {{ tableOfContent?.title }}
          </NuxtLink>
        </b-dropdown-item>
        <b-dropdown-item v-for="(chapter, index) in tableOfContent?.chapters" :key="index" aria-role="listitem">
          <NuxtLink
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

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { getTableOfContent } from "~/api/fanfictions";
import { TableOfContent, ChapterModelLight } from "~/models/fanfictions";

  @Component({
    name: "TableOfContent",
    fetchOnServer: true,
    fetchKey: "table-of-content-page"
  })

export default class extends Vue {
  // #region  Data
  @SerialiseClass(TableOfContent)
  public tableOfContent: TableOfContent | null = null;

  @SerialiseClass(ChapterModelLight)
  public previousChapter: ChapterModelLight | null = null;

  @SerialiseClass(ChapterModelLight)
  public nextChapter: ChapterModelLight | null = null;

  public currentChapter: ChapterModelLight | null = null;

  public fictionLoading: boolean = false;
  // #endregion

  // #region Computed
  public get NextToRouterLink(): any {
    if (this.nextChapter == null) return "";
    return { name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title", params: { fiction_id: this.tableOfContent?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug, chapter_id: this.nextChapter?.id.valueOf(), chapter_title: this.nextChapter?.titleAsSlug ?? "" } };
  }

  public get PreviousToRouterLink(): any {
    if (this.currentChapter == null) return "";
    else if (this.currentChapter != null) {
      if ((this.currentChapter.order ?? -1) === 1) {
        return { name: "fictions-fiction_id-fiction_title-sommaire", params: { fiction_id: this.tableOfContent?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug } };
      } else {
        return { name: "fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title", params: { fiction_id: this.tableOfContent?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug, chapter_id: this.previousChapter?.id.valueOf(), chapter_title: this.previousChapter?.titleAsSlug ?? "" } };
      }
    }
  }
  // #endregion

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

  @Watch("$route.query")
  private onRouteChanged(): void {
    if (this.$route.params.chapter_id == null) {
      this.currentChapter = null;
    } else {
      this.currentChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.id === parseInt(this.$route.params.chapter_id)) ?? null;
    }

    // Mise à jour des previous et next chapter
    if (this.currentChapter == null) {
      this.previousChapter = null;
      this.nextChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
    } else {
      if (this.currentChapter.order === 1)
        this.previousChapter = null;
      else
        this.previousChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.currentChapter?.order ?? -1) - 1)) ?? null;
      this.nextChapter = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.currentChapter?.order ?? -1) + 1)) ?? null;
    }
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      this.tableOfContent = (await getTableOfContent(parseInt(this.$route.params.fiction_id)));
      this.onRouteChanged();
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération du sommaire",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    } finally {
      this.fictionLoading = false;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
*{
  // border: 1px solid green;
}
@import "~/assets/scss/custom_bulma_core.scss";
#main-container{
  background-color: $primary-lighter;
}
</style>
