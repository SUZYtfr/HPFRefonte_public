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
        <div class="card-content" style="padding: 5px; padding-top: 2px; padding-bottom: 0px;">
          <FanfictionEntity
            :key="'ff_' + fiction.fanfiction_id.toString()"
            class="my-2"
            :fanfiction="fiction"
            :config="fanfictionEntityConfig"
          />
        </div>
      </div>
      <br>
    </section>

    <!-- Notes de fiction -->
    <section>
      <b-collapse
        class="card"
        animation="slide"
        aria-id="fictionNotes"
      >
        <template #trigger="props">
          <div
            class="card-header"
            role="button"
            aria-controls="fictionNotes"
            :aria-expanded="props.open"
          >
            <p class="card-header-title is-unselectable">
              Notes de fiction
            </p>
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
      <br>
    </section>

    <!-- Trigger warning -->
    <article v-if="fictionTriggerWarnings.length > 0" class="message is-danger">
      <div class="message-body py-1 px-2">
        <div class="is-flex is-flex-direction-row">
          <b-icon icon="exclamation-triangle" /><span><strong> TW / CW </strong></span>
        </div>
        <p>
          <ul v-for="(tw, index) in fictionTriggerWarnings" :key="index">
            <li>{{ tw.caption }}</li>
          </ul>
        </p>
      </div>
    </article>

    <!-- Sommaire -->
    <section>
      <b-collapse
        class="card"
        animation="slide"
        aria-id="fictionTableOfContent"
      >
        <template #trigger="props">
          <div
            class="card-header"
            role="button"
            aria-controls="fictionTableOfContent"
            :aria-expanded="props.open"
          >
            <p class="card-header-title is-unselectable">
              Sommaire
            </p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content p-2">
          <div class="content p-2">
            <div v-for="(chapter, index) in tableOfContent?.chapters" :key="index" class="is-flex is-flex-direction-row is-justify-content-center">
              <NuxtLink

                class="has-text-weight-normal"
                :to="{ name: 'fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title', params: { fiction_id: tableOfContent?.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug, chapter_id: chapter.id.valueOf(), chapter_title: chapter.titleAsSlug ?? ''}}"
              >
                {{ chapter.title }}
              </NuxtLink>
              <div v-if="(chapter?.trigger_warnings_loaded?.length ?? 0) > 0" class="is-danger ml-2 is-flex is-flex-direction-row is-align-items-baseline">
                <b-icon icon="exclamation-triangle" size="is-small" type="is-danger" class="mr-1" />
                <div v-for="(trigger_warning, index) in chapter.trigger_warnings_loaded" :key="index">
                  <span v-if="index > 0">
                    ,
                  </span>
                  <span class="has-text-danger">{{ trigger_warning.caption }}</span>
                </div>
              </div>
              <br>
            </div>
          </div>
        </div>
      </b-collapse>
      <br>
    </section>

    <!-- Reviews -->
    <section v-if="fiction != null">
      <b-collapse
        class="card"
        animation="slide"
        aria-id="fictionReviews"
      >
        <template #trigger="props">
          <div
            class="card-header  sub-title"
            role="button"
            aria-controls="fictionReviews"
            :aria-expanded="props.open"
          >
            <p class="card-header-title is-unselectable">
              {{ 'Reviews (' + fiction?.review_count?.toString() + ")" }}
            </p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
            </a>
          </div>
        </template>

        <div class="card-content pb-0">
          <div class="content p-2">
            <ReviewList ref="reviewList" :item_id="reviewListItemId" :review-list-type="reviewListType" />
          </div>
        </div>
      </b-collapse>
      <br>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import FanfictionEntity from "~/components/Fanfiction.vue";
import { getFanfictions } from "~/api/fanfictions";
import { FanfictionModel, FanfictionEntityConfig, TableOfContent, ChapterModelLight } from "~/models/fanfictions";
import ReviewList from "@/components/list/reviews/ReviewList.vue";
import { ReviewItemTypeEnum } from "@/types/fanfictions";

@Component({
  name: "Fanfiction",
  components: {
    FanfictionEntity,
    ReviewList
  },
  fetchOnServer: true,
  fetchKey: "fanfiction-page"
})

export default class extends Vue {
  // #region Props
  @SerialiseClass(TableOfContent)
  @Prop() public tableOfContent!: TableOfContent;
  // #endregion

  // #region Data
  @SerialiseClass(FanfictionModel)
  public fiction: FanfictionModel | null = null;

  public fictionLoading = false;
  public reviewEditorVisible = false;

  public fanfictionEntityConfig: FanfictionEntityConfig = {
    inList: false
  };

  // Reviews
  public reviewListType : ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;
  public reviewListItemId : number = 0;
  // #endregion

  // #region Computed
  public get fictionTriggerWarnings() : {id: number, caption: string }[] {
    let triggerWarningsGrouped: {id: number, caption: string }[] = [];
    this.tableOfContent.chapters?.filter(
      (t: ChapterModelLight) =>
        ((t.trigger_warnings?.length ?? 0) > 0)
    ).forEach((t: ChapterModelLight) => triggerWarningsGrouped.push(...t.trigger_warnings_loaded));
    triggerWarningsGrouped = triggerWarningsGrouped.filter((value, index, self) =>
      index === self.findIndex(t => (
        t.id === value.id
      ))
    );
    return triggerWarningsGrouped;
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      // Charger la fiction
      this.fiction = (await getFanfictions(parseInt(this.$route.params.fiction_id)));
      if (this.fiction != null) {
        this.reviewListItemId = this.fiction?.fanfiction_id;
        this.reviewListType = ReviewItemTypeEnum.Fanfiction;
      }
      console.log(this.fiction instanceof FanfictionModel);
      // this.$emit("change", this.fiction);
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

ul {
  list-style: inside;
}
</style>
