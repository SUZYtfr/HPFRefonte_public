<template>
  <div class="columns" style="height: 100%;">
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
    <div :class="['column', 'is-flex', 'is-flex-direction-column']" style="background-color: blue;">
      <div class="is-flex-grow-5">
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
                <p class="card-header-title is-unselectable">
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
                <p class="card-header-title is-unselectable">
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
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
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
  // #region Data
  @SerialiseClass(ChapterModel)
  public chapter: ChapterModel | null = null;

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

  // #region Watchers
  @Watch("$route.query", { deep: true })
  private onRouteChanged(): void {
    this.$fetch();
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.fictionLoading = true;
    try {
      // Charger le chapitre
      this.chapter = (await getChapters(parseInt(this.$route.params.id)));
      this.$emit("change", this.chapter);
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
