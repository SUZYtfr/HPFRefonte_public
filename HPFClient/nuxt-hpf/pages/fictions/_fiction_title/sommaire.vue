<template>
  <div style="background-color: blue;">
    <div class="is-flex-grow-5">
      <!-- Détail de la fiction -->
      <section v-if="fiction != null">
        <div class="card">
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
          aria-id="contentIdForA11y3"
        >
          <template #trigger="props">
            <div
              class="card-header"
              role="button"
              aria-controls="contentIdForA11y3"
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

      <!-- Sommaire -->
      <section>
        <b-collapse
          class="card"
          animation="slide"
          aria-id="contentIdForA11y3"
        >
          <template #trigger="props">
            <div
              class="card-header"
              role="button"
              aria-controls="contentIdForA11y3"
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

          <div class="card-content">
            <div class="content p-2">
              <div v-for="(chapter, index) in tableOfContent?.chapters" :key="index" class="has-text-centered">
                <NuxtLink

                  class="has-text-weight-normal"
                  :to="{ name: 'fictions-fiction_title-chapitres-chapter_title', params: { id: chapter.id.valueOf(), fiction_title: tableOfContent?.titleAsSlug, chapter_title: chapter.titleAsSlug ?? ''}}"
                >
                  {{ chapter.title }}
                </NuxtLink>
                <br>
              </div>
            </div>
          </div>
        </b-collapse>
        <br>
      </section>
    </div>
    <div><p>Liste des reviews</p></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import FanfictionEntity from "~/components/Fanfiction.vue";
import { getFanfictions } from "~/api/fanfictions";
import { FanfictionModel, FanfictionEntityConfig, TableOfContent } from "~/models/fanfictions";
import TipTapEditor from "~/components/TipTapEditor.vue";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";

@Component({
  name: "Fanfiction",
  components: {
    TipTapEditor, FanfictionEntity
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
  public editorContent: TipTapEditorContent | null = null;

  public tiptapReadOnlyConfig: TipTapEditorConfig = {
    showFooter: false,
    placeholder: "",
    readOnly: true,
    fixedHeight: false
  };

  public fanfictionEntityConfig: FanfictionEntityConfig = {
    inList: false
  };
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      // Charger la fiction
      this.fiction = (await getFanfictions(parseInt(this.$route.params.id)));
      this.$emit("change", this.fiction);
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
</style>
