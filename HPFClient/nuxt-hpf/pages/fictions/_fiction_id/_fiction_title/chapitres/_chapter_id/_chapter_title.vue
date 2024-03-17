<template>
  <div>
    <b-loading v-model="chapterLoading" :is-full-page="false" />
    <div class="columns">
      <!-- Colonne gauche - Toolbar -->
      <div v-if="chapter != null" class="column is-narrow pr-0">
        <div class="card" style="position: sticky; top: 60px; width: 40px;">
          <div class="card-content" style="padding: 5px;">
            <div class="content is-flex is-flex-direction-column" style="gap: 5px;">
              <b-tooltip
                label="Afficher / masquer le panel de review"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="feather-alt"
                  @click="reviewEditorVisible = !reviewEditorVisible"
                />
              </b-tooltip>
              <b-tooltip
                label="Augmenter la taille de la police"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-up"
                  @click="upSizeFont()"
                />
              </b-tooltip>
              <b-tooltip
                label="Taille de police par défaut"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="compress-alt"
                  @click="defaultSizeFont()"
                />
              </b-tooltip>
              <b-tooltip
                label="Réduire la taille de la police"
                position="is-right"
                append-to-body
              >
                <b-button
                  type="is-primary"
                  size="is-small"
                  icon-pack="fas"
                  icon-left="sort-alpha-down-alt"
                  @click="downSizeFont()"
                />
              </b-tooltip>
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne centrale - Contenu -->
      <div :class="['column', 'is-flex', 'is-flex-direction-column']">
        <div class="is-flex-grow-5">
          <!-- Notes de fiction (seulement sur le chapitre 1)-->
          <section v-if="((chapter?.order ?? 0) == 1) && (tableOfContent?.storynote?.length ?? 0 > 0)">
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

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="tableOfContent.storynote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Note de début de chapitre -->
          <section v-if="(chapter?.startnote?.length ?? 0) > 0">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="chapterStartNote"
            >
              <template #trigger="props">
                <div
                  class="card-header"
                  role="button"
                  aria-controls="chapterStartNote"
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

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="chapter?.startnote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Trigger warning -->
          <article v-if="(chapter?.trigger_warnings_loaded?.length ?? 0) > 0" class="message is-danger">
            <div class="message-body py-3 px-2 is-flex is-flex-direction-row">
              <b-icon icon="exclamation-triangle" /><span><strong class="mr-1"> TW / CW </strong></span>
              <div v-for="(trigger_warning, index) in chapter?.trigger_warnings_loaded" :key="index">
                <span v-if="index > 0">
                  ,
                </span>
                <span class="has-text-danger">{{ trigger_warning.caption }}</span>
              </div>
            </div>
          </article>

          <!-- Contenu du chapitre -->
          <section v-if="chapter != null">
            <b-collapse
              class="card"
              animation="slide"
              aria-id="chapterContent"
            >
              <template #trigger="props">
                <div
                  class="card-header sub-title"
                  role="button"
                  aria-controls="chapterContent"
                  :aria-expanded="props.open"
                >
                  <p class="card-header-title is-centered">
                    {{ chapter?.title }}
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" type="is-light" />
                  </a>
                </div>
              </template>
              <div class="card-content p-0">
                <!-- DEBUT: Sticky FontSize -->
                <div class="has-text-right" style="position: sticky; top: 80px; height: 50px;">
                  <span v-show="fontSizeVisible" class="mr-2 p-1 is-primary is-size-7 has-text-weight-semibold" style="background-color: whitesmoke; opacity: 1; border: solid; border-radius: 0.50rem;">
                    {{ tiptapReadOnlyConfig.fontSize + '%' }}
                  </span>
                </div>
                <!-- FIN: Sticky FontSize -->
                <div class="content p-2" style="display: block; overflow: auto; margin-top: -55px;">
                  <client-only>
                    <TipTapEditor ref="chapterContentEditor" :config="tiptapReadOnlyConfig" @quote="quoteFromText" />
                  </client-only>
                </div>
              </div>
              <footer v-if="false" class="card-footer">
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
              aria-id="chapterEndNote"
            >
              <template #trigger="props">
                <div
                  class="card-header"
                  role="button"
                  aria-controls="chapterEndNote"
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

              <div class="card-content p-0">
                <div class="content p-2">
                  <p v-html="chapter?.endnote" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>

          <!-- Reviews -->
          <section v-if="chapter != null">
            <b-collapse
              v-model="reviewPaneExpanded"
              class="card"
              animation="slide"
              aria-id="chapterReviews"
            >
              <template #trigger>
                <div
                  class="card-header  sub-title"
                  role="button"
                  aria-controls="chapterReviews"
                  :aria-expanded="reviewPaneExpanded"
                >
                  <p class="card-header-title is-unselectable">
                    {{ 'Reviews (' + chapter?.review_count?.toString() + ")" }}
                  </p>
                  <a class="card-header-icon">
                    <b-icon class="is-clickable" :icon="reviewPaneExpanded ? 'caret-up' : 'caret-down'" type="is-light" />
                  </a>
                </div>
              </template>

              <div class="card-content pb-0">
                <div class="content p-2">
                  <ReviewList ref="reviewList" :item_id="reviewListItemId" :review-list-type="reviewListType" @reviewContentChanged="(value) => (editorContentReview = value)" />
                </div>
              </div>
            </b-collapse>
            <br>
          </section>
        </div>
      </div>

      <!-- Colonne droite - Editeur review -->
      <div v-if="$auth.loggedIn" v-show="reviewEditorVisible" class="column is-4">
        <div class="card" style="position: sticky; top: 60px;">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              Editeur de review
            </p>
            <button class="delete mr-1 mt-1" @click="reviewEditorVisible = false" />
          </header>
          <div class="card-content p-3">
            <div v-if="reviewHeaderMessageVisible" class="notification is-info is-light is-size-6 py-2 pl-2 pr-5">
              <button class="delete is-small" @click="reviewHeaderMessageVisible = false" />
              <p>Vous avez aimé ce texte ? <strong>Dites-le !</strong> Vous pensez que ce texte peut être amélioré ? <strong>Ecrivez-le !</strong></p><p>Avec gentillesse et bienveillance, faites part de votre avis.</p>
            </div>
            <client-only>
              <TipTapEditor ref="reviewEditorSmall" :config="tiptapReviewConfig" :show-footer="false" :placeholder="'Ecrire une review'" @change="(value) => (editorContentReview = value)" />
            </client-only>
            <div class="mt-1 is-flex is-flex-direction-row is-flex-wrap-wrap">
              <b-checkbox v-model="canRate">
                Ajouter une note
              </b-checkbox>
              <b-rate
                v-model="reviewRating"
                icon-pack="fas"
                :max="10"
                size="default"
                :show-score="canRate"
                :rtl="false"
                :spaced="false"
                :disabled="!canRate"
              />
            </div>
          </div>
          <footer class="card-footer py-2">
            <b-button
              :disabled="(editorContentReview?.wordcount ?? 0) < 3"
              :expanded="false"
              label="Poster une review"
              type="is-primary"
              class="mx-auto"
            />
          </footer>
        </div>
      </div>
      <div v-else-if="reviewEditorVisible" class="buttons column is-narrow">
        <b-button
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser une review"
          type="is-primary"
          style="position: sticky; top: 60px;"
          @click="ModalsStatesModule.setLoginModalActive(true)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "nuxt-property-decorator";
import { getModule } from "vuex-module-decorators";
import { SerialiseClass } from "@/serialiser-decorator";
import { getChapters } from "@/api/chapters";
import { ChapterModel, TableOfContent } from "@/models/fanfictions";
import TipTapEditor from "@/components/TipTapEditor.vue";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";
import ModalsStates from "~/store/modules/ModalsStates";
import ReviewList from "@/components/list/reviews/ReviewList.vue";
import { ReviewItemTypeEnum } from "@/types/fanfictions";

@Component({
  name: "Chapter",
  components: {
    TipTapEditor,
    ReviewList
  },
  fetchOnServer: true,
  fetchKey: "chapter-page"
})

export default class extends Vue {
  // #region Props
  @SerialiseClass(TableOfContent)
  @Prop() public tableOfContent!: TableOfContent;
  // #endregion

  // #region Data
  @SerialiseClass(ChapterModel)
  public chapter: ChapterModel | null = null;

  public reviewEditorVisible = false;
  public editorContentReview: TipTapEditorContent | null = null;

  public tiptapReadOnlyConfig: TipTapEditorConfig = {
    showFooter: false,
    placeholder: "",
    readOnly: true,
    fixedHeight: false,
    height: 125,
    defaultValue: "",
    canQuote: false,
    quoteLimit: 250,
    fontSize: 100,
    oneLineToolbar: false,
    canUseImage: true
  };

  public tiptapReviewConfig: TipTapEditorConfig = {
    showFooter: false,
    placeholder: "Votre review ici",
    readOnly: false,
    fixedHeight: true,
    height: 250,
    defaultValue: "",
    canQuote: false,
    quoteLimit: 0,
    fontSize: 100,
    oneLineToolbar: true,
    canUseImage: false
  };

  public chapterLoading: boolean = true;

  public reviewHeaderMessageVisible: boolean = true;

  public fontSizeVisible: boolean = false;

  public timerThrottleFontsize: number = 0;

  public reviewPaneExpanded: boolean = false;

  // Reviews
  public reviewListType : ReviewItemTypeEnum = ReviewItemTypeEnum.Chapter;
  public reviewListItemId : number = 0;

  public canRate: boolean = false;
  public reviewRating: number | null = null;
  // #endregion

  public mounted(): any {
    console.log(this.tableOfContent);
  }

  // #region Computed
  get ModalsStatesModule(): ModalsStates {
    return getModule(ModalsStates, this.$store);
  }
  // #endregion

  // #region Watchers
  @Watch("$route.query", { deep: true })
  private onRouteChanged(): void {
    this.$fetch();
  }

  @Watch("$auth.loggedIn", { immediate: true })
  private onAuthChanged(): void {
    this.tiptapReadOnlyConfig.canQuote = this.$auth.loggedIn;
  }

  @Watch("reviewPaneExpanded", { deep: true })
  private onreviewPaneExpanded(): void {
    if (this.reviewPaneExpanded && this.reviewEditorVisible) {
      if (process.client) {
        (this.$refs.reviewList as ReviewList)?.setContent(this.editorContentReview);
      }
      this.reviewEditorVisible = false;
    }
  }

  @Watch("canRate")
  public onCanRateChanged(): void {
    this.reviewRating = (this.canRate ? 10 : null);
  }

  @Watch("reviewEditorVisible")
  public onreviewEditorVisibleChanged(): void {
    if (this.reviewEditorVisible && this.reviewPaneExpanded) {
      if (process.client) {
        (this.$refs.reviewEditorSmall as TipTapEditor)?.setContent(this.editorContentReview);
      }
      this.reviewPaneExpanded = false;
    }
  }
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.chapterLoading = true;
    try {
      // Charger le chapitre
      this.chapter = (await getChapters(parseInt(this.$route.params.chapter_id)));
      this.tiptapReadOnlyConfig.defaultValue = (this.chapter?.text ?? "");
      if (this.chapter != null) {
        this.reviewListItemId = this.chapter?.chapter_id;
        this.reviewListType = ReviewItemTypeEnum.Chapter;
      }
      if (process.client) {
        (this.$refs.chapterContentEditor as TipTapEditor)?.setContent(new TipTapEditorContent({ content: (this.chapter?.text ?? "") }));
      }
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
      this.chapterLoading = false;
    }
  }
  // #endregion

  // #region Methods
  public quoteFromText(quote: string): void {
    if (process.client) {
      if (this.reviewPaneExpanded === false) {
        if (this.reviewEditorVisible === false) this.reviewEditorVisible = true;
        (this.$refs.reviewEditorSmall as TipTapEditor)?.setQuote(quote);
      } else if (this.reviewPaneExpanded) (this.$refs.reviewList as ReviewList)?.setQuote(quote);
    }
  }

  // Augmenter la taille du texte
  public upSizeFont(): void {
    if (process.client) {
      this.tiptapReadOnlyConfig.fontSize += 10;
      this.displayFontSize();
    }
  }

  // Réduire la taille du texte
  public defaultSizeFont(): void {
    if (process.client) {
      this.tiptapReadOnlyConfig.fontSize = 100;
      this.displayFontSize();
    }
  }

  // Réduire la taille du texte
  public downSizeFont(): void {
    if (process.client) {
      this.tiptapReadOnlyConfig.fontSize -= 10;
      this.displayFontSize();
    }
  }

  // Afficher / masquer l'indicateur de fontSize
  private displayFontSize(): void {
    this.fontSizeVisible = true;
    clearTimeout(this.timerThrottleFontsize);
    this.timerThrottleFontsize = window.setTimeout(
      () => { this.fontSizeVisible = false; },
      3000
    );
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
*{
  // border: 1px solid green;
}
</style>
