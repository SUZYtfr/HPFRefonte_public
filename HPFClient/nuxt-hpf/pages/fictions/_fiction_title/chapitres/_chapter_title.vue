<template>
  <div>
    <!-- Note de début de chapitre -->
    <section v-if="(chapter?.startnote?.length ?? 0) > 0">
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
            <p class="card-header-title">
              Notes de chapitre
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

    <!-- Contenu du chapitre -->
    <section v-if="chapter != null">
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
            <p class="card-header-title">
              {{ chapter?.title }}
            </p>
            <a class="card-header-icon">
              <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content">
          <div class="content p-2" style="display: block; overflow: auto;">
            <client-only>
              <TipTapEditor ref="readOnlyEditor" :config="tiptapReadOnlyConfig" />
            </client-only>
          </div>
        </div>
        <footer class="card-footer">
          <a class="card-footer-item">Save</a>
          <a class="card-footer-item">Edit</a>
          <a class="card-footer-item">Delete</a>
        </footer>
      </b-collapse>
      <br>
    </section>

    <!-- Note de fin de chapitre -->
    <section v-if="(chapter?.endnote?.length ?? 0) > 0">
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
            <p class="card-header-title">
              Notes de fin de chapitre
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { getChapters } from "@/api/chapters";
import { ChapterModel } from "@/models/fanfictions";
import TipTapEditor from "@/components/TipTapEditor.vue";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";

@Component({
  name: "Chapter",
  components: {
    TipTapEditor
  },
  fetchOnServer: true,
  fetchKey: "chapter-page"
})

export default class extends Vue {
  // #region Props
  @SerialiseClass(ChapterModel)
  @Prop() public chapterProp: ChapterModel | null = null;

  @Prop() public testProp!: string;
  // #endregion

  // #region  Data
  // @SerialiseClass(ChapterModel)
  // public chapter: ChapterModel | null = null;

  public fictionLoading = false;
  public reviewEditorVisible = false;
  public editorContent: TipTapEditorContent | null = null;

  public tiptapReadOnlyConfig: TipTapEditorConfig = {
    showFooter: false,
    placeholder: "",
    readOnly: true,
    fixedHeight: false
  };
  // #endregion

  // @Watch("chapter", { deep: true })
  // private onFChapterChanged(): void {
  //   this.$emit("change", this.chapter);
  // }

  get chapter(): ChapterModel | null {
    return this.chapterProp;
  }

  set chapter(value: ChapterModel | null) {
    this.$emit("change", value);
  }

  // #region Hooks
  mounted():void {
    console.log(this.testProp);
  }

  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      // Charger le chapitre
      this.chapter = (await getChapters(parseInt(this.$route.params.id)));
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération du chapitre",
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
