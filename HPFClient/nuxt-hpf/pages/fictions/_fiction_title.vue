<template>
  <div id="main-container" class="container pt-3 is-flex is-flex-direction-column" style="background-color: red; height: 100%; ">
    <div class="is-flex-grow-5">
      <!-- Sous page fiction / chapitre -->
      <NuxtChild :table-of-content="tableOfContent" @change="(value) => (currentItem = value)" />
    </div>

    <!-- Navigation -->
    <div class="is-flex is-flex-direction-row is-justify-content-space-between">
      <!-- Previous -->
      <b-button
        v-if="previousItem != null"
        type="is-primary"
        outlined
        icon-left="angle-left"
        tag="router-link"
        :to="PreviousToRouterLink"
      >
        <span class="is-hidden-mobile">{{ ((previousItem?.title ?? "").length > 25 ? (previousItem?.title ?? "").substring(0,25) + "..." : previousItem?.title) }}</span>
      </b-button>
      <!-- Sommaire -->
      <b-dropdown v-if="(currentItem instanceof ChapterModel)" aria-role="list" position="is-top-right" :class="[{'mr-auto': nextItem == null }, {'ml-auto': nextItem == null }]">
        <template #trigger="{ active }">
          <b-button
            label="Sommaire"
            type="is-primary"
            outlined
            :icon-right="active ? 'angle-up' : 'angle-down'"
          />
        </template>
        <b-dropdown-item aria-role="listitem">
          <b-icon icon="book-open" />
          <NuxtLink
            class="has-text-weight-normal"
            :to="{ name: 'fictions-fiction_title-sommaire', params: { id: tableOfContent?.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug }}"
          >
            {{ tableOfContent?.title }}
          </NuxtLink>
        </b-dropdown-item>
        <b-dropdown-item v-for="(chapter, index) in tableOfContent?.chapters" :key="index" aria-role="listitem">
          <NuxtLink
            class="has-text-weight-normal"
            :to="{ name: 'fictions-fiction_title-chapitres-chapter_title', params: { id: chapter.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug, chapter_title: chapter.titleAsSlug ?? ''}}"
          >
            {{ chapter.title }}
          </NuxtLink>
        </b-dropdown-item>
      </b-dropdown>
      <!-- Next -->
      <b-button
        v-if="nextItem != null"
        type="is-primary"
        outlined
        icon-right="angle-right"
        tag="router-link"
        :to="NextToRouterLink"
        :class="[{'ml-auto': (currentItem instanceof FanfictionModel) }]"
      >
        <span class="is-hidden-mobile">{{ ((nextItem?.title ?? "").length > 25 ? (nextItem?.title ?? "").substring(0,25) + "..." : nextItem?.title) }}</span>
      </b-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { getTableOfContent } from "~/api/fanfictions";
import { TableOfContent, ChapterModelLight, FanfictionModel, ChapterModel } from "~/models/fanfictions";

  @Component({
    name: "TableOfContent",
    fetchOnServer: true,
    fetchKey: "table-of-content-page"
  })

export default class extends Vue {
  // #region  Data
  @SerialiseClass(TableOfContent)
  public tableOfContent: TableOfContent | null = null;

  public previousItem: TableOfContent | ChapterModelLight | null = null;
  public currentItem: FanfictionModel | ChapterModel | null = null;
  public nextItem: TableOfContent | ChapterModelLight | null = null;

  public loading = false;
  // #endregion

  // #region Computed
  public get NextToRouterLink(): any {
    if (this.nextItem == null) return "";
    return { name: "fictions-fiction_title-chapitres-chapter_title", params: { id: this.nextItem?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug, chapter_title: this.nextItem?.titleAsSlug ?? "" } };
  }

  public get PreviousToRouterLink(): any {
    if (this.previousItem == null) return "";
    else if (this.currentItem instanceof ChapterModel) {
      if (((this.currentItem as ChapterModel).order ?? -1) === 1) {
        return { name: "fictions-fiction_title-sommaire", params: { id: this.tableOfContent?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug } };
      } else {
        return { name: "fictions-fiction_title-chapitres-chapter_title", params: { id: this.previousItem?.id.valueOf(), fiction_title: this.tableOfContent?.titleAsSlug, chapter_title: this.previousItem?.titleAsSlug ?? "" } };
      }
    }
  }
  // #endregion

  // #region Watchers
  @Watch("currentItem")
  public onItemChanged(): void {
    if (this.currentItem instanceof FanfictionModel) {
      this.previousItem = null;
      this.nextItem = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
    } else if (this.currentItem instanceof ChapterModel) {
      if ((this.currentItem as ChapterModel).order === 1)
        this.previousItem = this.tableOfContent;
      else
        this.previousItem = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === (((this.currentItem as ChapterModel).order ?? -1) - 1)) ?? null;
      this.nextItem = this.tableOfContent?.chapters?.find((chapter: ChapterModelLight) => chapter.order === (((this.currentItem as ChapterModel).order ?? -1) + 1)) ?? null;
    }
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.loading = true;
    try {
      this.tableOfContent = (await getTableOfContent(parseInt(this.$route.params.id)));
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
      this.loading = false;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
*{
  // border: 1px solid green;
}
</style>
