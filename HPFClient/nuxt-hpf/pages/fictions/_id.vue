<template>
  <div id="main-container" class="container px-1" style="background-color: red;">
    <div class="columns">
      <!-- Colonne gauche - Toolbar -->
      <div v-if="chapter != null" class="column is-narrow" style="background-color: green;">
        <div class="card" style="position: sticky; top: 60px; width: 40px;">
          <div class="card-content" style="padding: 5px;">
            <div class="content is-flex is-flex-direction-column" style="gap: 5px;">
              <b-button
                class="news_comment_button"
                type="is-primary"
                size="is-small"
                icon-pack="fas"
                icon-left="comment-alt"
                @click="reviewEditorVisible = !reviewEditorVisible"
              />
              <b-button
                class="news_comment_button"
                type="is-primary"
                size="is-small"
                icon-pack="fas"
                icon-left="comment-alt"
                @click="reviewEditorVisible = !reviewEditorVisible"
              />
              <b-button
                class="news_comment_button"
                type="is-primary"
                size="is-small"
                icon-pack="fas"
                icon-left="comment-alt"
                @click="reviewEditorVisible = !reviewEditorVisible"
              />
            </div>
          </div>
        </div>
      </div>
      <!-- Colonne centrale - Contenu -->
      <div :class="['column']" style="background-color: blue;">
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
        <section v-if="fiction != null">
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

        <!-- Note de début de chapitre -->
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
                  Titre du chapitre
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

        <!-- Navigation -->
        <div class="is-flex is-flex-direction-row is-justify-content-space-between">
          <!-- Previous -->
          <b-button v-if="previousItem != null" type="is-primary" outlined icon-left="angle-left">
            <span class="is-hidden-mobile">{{ previousItem?.title }}</span>
          </b-button>
          <!-- Sommaire -->
          <b-dropdown aria-role="list" position="is-top-right" style="margin-left: auto; margin-right: auto;">
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
              {{ summary?.title }}
            </b-dropdown-item>
            <b-dropdown-item v-for="(chapter, index) in summary?.chapters" :key="index" aria-role="listitem">
              {{ chapter.title }}
            </b-dropdown-item>
          </b-dropdown>
          <!-- Next -->
          <b-button v-if="nextItem != null" type="is-primary" outlined icon-right="angle-right">
            <span class="is-hidden-mobile">{{ nextItem?.title }}</span>
          </b-button>
        </div>
        <div><p>Liste des reviews</p></div>
      </div>
      <!-- Colonne droite - Editeur review -->
      <div v-if="$auth.loggedIn && reviewEditorVisible" class="column is-4" style="background-color: yellow;">
        <div class="card" style="position: sticky; top: 60px;">
          <header class="card-header">
            <p class="card-header-title">
              Laisser une review
            </p>
          </header>
          <div class="card-content p-3">
            <div class="notification is-info is-light is-size-6 p-2">
              <p>Vous avez aimé ce texte ? Dites-le !</p><p>Vous pensez que ce texte peut être amélioré ? Ecrivez-le !</p><p>Avec gentillesse et bienveillance, faites part de votre avis.</p>
            </div>
            <client-only>
              <TipTapEditor ref="commentEditor" :show-footer="false" :placeholder="'Ecrire un commentaire'" @change="(value) => (editorContent = value)" />
            </client-only>
          </div>
          <footer class="card-footer">
            <div class="buttons mt-1">
              <b-button
                :disabled="(editorContent?.wordcount ?? 0) < 3"
                :expanded="false"
                label="Laisser une review"
                type="is-primary"
              />
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import FanfictionEntity from "~/components/Fanfiction.vue";
import { getFanfictions } from "~/api/fanfictions";
import { FanfictionModel, FanfictionEntityConfig, ChapterModel, FanfictionModelLight, ChapterModelLight } from "~/models/fanfictions";
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
  // #region  Data
  @SerialiseClass(FanfictionModel)
  public fiction: FanfictionModel | null = null;

  @SerialiseClass(ChapterModel)
  public chapter: ChapterModel | null = null;

  @SerialiseClass(FanfictionModelLight)
  public summary: FanfictionModelLight | null = null;

  public previousItem: FanfictionModelLight | ChapterModelLight | null = null;
  public nextItem: FanfictionModelLight | ChapterModelLight | null = null;

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

  // #region Watchers
  // @Watch("currentItem")
  // public onChapterChanged(): void {
  //   if (this.currentItem == null) {
  //     // On verra
  //     this.previousItem = null;
  //     this.nextItem = null;
  //   } else if (this.currentItem instanceof FanfictionModel) {
  //     this.previousItem = null;
  //     this.nextItem = this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
  //   } else if (this.currentItem instanceof ChapterModel) {
  //     if (this.currentItem.order === 1)
  //       this.previousItem = this.summary;
  //     else
  //       this.previousItem = this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === (this.currentItem.order - 1)) ?? null;
  //     this.nextItem = this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === (this.currentItem.order + 1)) ?? null;
  //   }
  // }
  // #endregion

  // #region Hooks

  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      if (this.summary == null) {
        this.summary = new FanfictionModelLight();
        this.summary.id = 240;
        this.summary.creation_date = new Date();
        this.summary.creation_user_id = null;
        this.summary.modification_date = new Date();
        this.summary.modification_user_id = null;
        this.summary.title = "Le titre de la fiction";
        this.summary.chapters = [];
        let chapter = new ChapterModelLight();
        chapter.id = 1;
        chapter.title = "Chapitre 1: Le début";
        chapter.order = 1;
        this.summary.chapters.push(chapter);
        chapter = new ChapterModelLight();
        chapter.id = 2;
        chapter.title = "Chapitre 2: La suite";
        chapter.order = 2;
        this.summary.chapters.push(chapter);
      }
      this.fiction = (await getFanfictions(parseInt(this.$route.params.id)));
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération de la fiction",
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
      console.log(this.fiction instanceof FanfictionModel);
      if (this.fiction != null) {
        this.previousItem = null;
        this.nextItem = this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === 1) ?? null;
      } else if (this.chapter != null) {
        this.previousItem = (this.chapter.order === 1) ? this.summary : (this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.chapter?.order ?? 0) - 1)) ?? null);
        this.nextItem = this.summary?.chapters?.find((chapter: ChapterModelLight) => chapter.order === ((this.chapter?.order ?? 0) + 1)) ?? null;
      } else {
        // On verra
        this.previousItem = null;
        this.nextItem = null;
      }
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
