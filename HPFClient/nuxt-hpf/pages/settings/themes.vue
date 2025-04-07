<template>
  <div class="container is-fluid">
    <div class="columns">
      <div class="column">
        <!-- <span class="is-size-5">
          Aperçus
        </span> -->
        <!-- Bannière -->
        <div id="banner" class="hero mb-2">
          <div class="hero-body">
            <div class="container">
              <h1>Harry Potter Fanfiction</h1>
            </div>
          </div>
        </div>
        <!-- Aperçu d'une actualité -->
        <News_2
          :key="'news_mock_' + (mockNews.news_id?.toString() ?? '0')"
          :news="mockNews"
          class="mt-2 is-color-even"
        />
        <!-- Aperçus d'une fiction -->
        <FanfictionThumbnail
          :fanfiction="mockFiction"
          class="mt-2"
        />
        <!-- <div class="columns mb-0">
            <div class="column is-half">
              <FanfictionThumbnail
                :fanfiction="mockFiction"
              />
            </div>
        <div class="column is-half">
              <FanfictionThumbnail
                :fanfiction="mockFiction"
              />
            </div>
        </div> -->
        <Fanfiction
          class="mt-2"
          :fanfiction="mockFiction"
        />
      </div>
      <div class="column is-narrow">
        <div style="width: 355px;">
          <!-- Liste des thèmes existants + nouveau thème-->
          <div class="card">
            <div class="card-content px-3 py-3">
              <simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
                <div
                  v-for="(theme) in themes"
                  :key="theme.id"
                  :ref="'theme_row_' + theme.id.toString()"
                  :class="['is-flex', 'is-flex-direction-row', 'is-align-items-center', 'is-clickable', 'py-1', 'px-2', 'mt-1', 'theme-list-item-wrapper' ]"
                  :style="{ backgroundColor: (((selectedTheme?.id ?? -1) == theme.id) ? theme.details?.find(t=>t.colorScheme == ColorSchemeEnum.Light)?.hpf_primary_lighter : 'transparent')}"
                  @click="beginEdit(theme)"
                >
                  <div class="rounded-square mr-2" :style="{ backgroundColor: theme.details?.find(t=>t.colorScheme == ColorSchemeEnum.Light)?.primary}" />
                  <span :class="['has-text-weight-medium', 'theme-list', { 'has-text-weight-bold': ((selectedTheme?.id ?? -1) == theme.id)}]">{{ theme.name }}</span>
                </div>
              </simplebar>
              <div id="add-new-theme" class="has-text-centered is-clickable mt-1" @click="onNewTheme">
                <p class="is-flex is-flex-direction-row is-align-items-center is-justify-content-center">
                  <b-icon icon="plus-square" size="is-medium" />
                  Créer un nouveau thème
                </p>
              </div>
            </div>
          </div>
          <br>
          <!-- Edition d'un thème -->
          <div v-if="selectedTheme != null" class="card">
            <header class="card-header sub-title">
              <p class="card-header-title is-centered">
                {{ selectedTheme.name + ((selectedTheme.recordStatus == RecordStatusEnum.Added || selectedTheme.recordStatus == RecordStatusEnum.Updated) ? "*" : "") }}
              </p>
            </header>
            <div class="card-content px-3 py-3">
              <b-field
                label="Libellé"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  ref="TxtSelectedTheme_Name"
                  v-model="selectedTheme.name"
                  type="text"
                  placeholder="Libellé"
                  required
                  :expanded="true"
                  @input="editorChanged"
                />
              </b-field>
              <div class="is-flex is-flex-direction-row">
                <b-field>
                  <b-checkbox v-model="selectedTheme.default" @input="editorChanged">
                    Theme par défaut
                  </b-checkbox>
                </b-field>
                <b-field>
                  <b-checkbox v-model="selectedTheme.enabled" @input="editorChanged">
                    Theme actif
                  </b-checkbox>
                </b-field>
              </div>
              <client-only>
                <div v-show="selectedTheme.default == false">
                  <b-field
                    label="Par défaut à partir du"
                    label-position="on-border"
                    custom-class="has-text-primary"
                  >
                    <b-datepicker
                      v-model="selectedTheme.use_default_from"
                      locale="fr-FR"
                      placeholder="Sélectionner une date"
                      append-to-body
                      icon="calendar-alt"
                      :first-day-of-week="1"
                      :icon-right="selectedTheme.use_default_from ? 'times-circle' : ''"
                      :icon-right-clickable="true"
                      @icon-right-click="selectedTheme.use_default_from = null"
                      @input="editorChanged"
                    />
                  </b-field>
                  <b-field
                    label="Par défaut jusqu'au"
                    label-position="on-border"
                    custom-class="has-text-primary"
                  >
                    <b-datepicker
                      v-model="selectedTheme.use_default_to"
                      locale="fr-FR"
                      placeholder="Sélectionner une date"
                      append-to-body
                      icon="calendar-alt"
                      :first-day-of-week="1"
                      :icon-right="selectedTheme.use_default_to ? 'times-circle' : ''"
                      :icon-right-clickable="true"
                      @icon-right-click="selectedTheme.use_default_to = null"
                      @input="editorChanged"
                    />
                  </b-field>
                </div>
              </client-only>
              <b-tabs v-if="selectedTheme.details != null && selectedTheme.details.length > 0" class="mt-3" type="is-toggle" expanded @input="detailsTabChanged">
                <template v-for="(detail, index) in selectedTheme.details" :key="index"
                >
                  <b-tab-item
                    :value="index | numberToString"
                    label=""
                    :icon="ColorSchemeEnumMetadata.get(detail.colorScheme).icon"
                  >
                    <div v-if="selectedDetail != null">
                      <div
                        class="
                  is-flex
                  is-flex-direction-row
                  is-align-items-center
                  mb-2"
                      >
                        <b-colorpicker :value="selectedDetail.primary" representation="square" class="mr-2" @input="primaryColorChanged">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="primaryColorInput"
                                :value="selectedDetail.primary"
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
                                @input.native="colorInput($event)"
                              />
                            </b-field>
                          </template>
                        </b-colorpicker>
                        <b-tooltip label="Copier" type="is-white" class="mr-2">
                          <b-button
                            type="is-light"
                            icon-left="copy"
                            @click="writeClipboardText(selectedDetail.primary)"
                          />
                        </b-tooltip>
                        <span class="has-text-primary">Couleur principale</span>
                      </div>
                      <div class="is-flex is-flex-direction-row is-align-items-center mb-2">
                        <b-colorpicker :value="selectedDetail.primary_light" representation="square" class="mr-2" @input="lightColorChanged">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="lightColorInput"
                                :value="selectedDetail.primary_light"
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
                                @input.native="colorInput($event)"
                              />
                            </b-field>
                          </template>
                        </b-colorpicker>
                        <b-tooltip label="Copier" type="is-white" class="mr-2">
                          <b-button
                            type="is-light"
                            icon-left="copy"
                            @click="writeClipboardText(selectedDetail.primary_light)"
                          />
                        </b-tooltip>
                        <span class="has-text-primary">Couleur light</span>
                      </div>
                      <div class="is-flex is-flex-direction-row is-align-items-center mb-3">
                        <b-colorpicker :value="selectedDetail.hpf_primary_lighter" representation="square" class="mr-2" @input="lightAlternativeColorChanged">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="lightAlternativeColorInput"
                                :value="selectedDetail.hpf_primary_lighter"
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
                                @input.native="colorInput($event)"
                              />
                            </b-field>
                          </template>
                        </b-colorpicker>
                        <b-tooltip label="Copier" type="is-white" class="mr-2">
                          <b-button
                            type="is-light"
                            icon-left="copy"
                            @click="writeClipboardText(selectedDetail.hpf_primary_lighter)"
                          />
                        </b-tooltip>
                        <span class="has-text-primary">Couleur light (alternative)</span>
                      </div>
                      <b-field
                        label="Url de la bannière"
                        label-position="on-border"
                        custom-class="has-text-primary"
                      >
                        <b-input
                          v-model="selectedDetail.banner_url"
                          type="text"
                          placeholder="Libellé"
                          required
                          :expanded="true"
                          @input="editorChanged"
                        />
                      </b-field>
                    </div>
                  </b-tab-item>
                </template>
              </b-tabs>
            </div>
            <footer class="modal-card-foot p-3">
              <b-button
                :disabled="!formIsValid"
                label="Enregistrer"
                type="is-primary"
                :loading="loading"
                class="mr-auto"
                @click="updateItem"
              />
              <b-button
                label="Supprimer"
                type="is-danger"
                :loading="loading"
                class="ml-auto"
                @click="deleteItem"
              />
            </footer>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, getModule, Vue, Watch } from "nuxt-property-decorator";
import simplebar from "simplebar-vue";
import { RecordStatusEnum } from "@/types/basics";
import { ThemeDetail, ColorSchemeEnum, ColorSchemeEnumMetadata } from "@/types/themes";
import { ThemeModel } from "@/models/themes";
import { SerialiseClass } from "@/serialiser-decorator";
import News_2 from "~/components/News_2.vue";
import { NewsModel } from "@/models/news";
import { AuthorData } from "@/types/users";
import { FanfictionModel } from "@/models/fanfictions";
import { CharacteristicData } from "~/types/characteristics";
import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";
import FanfictionThumbnailList from "~/components/list/fanfictions/FanfictionThumbnailList.vue";
import Fanfiction from "~/components/Fanfiction.vue";
import { OpenToast } from "@/utils/formHelper";
import { getPrivateThemes, deleteTheme, postTheme, putTheme } from "@/api/themes";
import "simplebar/dist/simplebar.min.css";
import "simplebar/dist/simplebar.min.js";
import Config from "~/store/modules/Config";

@Component({
  name: "SettingsThemes",
  components: {
    News_2,
    FanfictionThumbnail,
    FanfictionThumbnailList,
    Fanfiction,
    simplebar
  },
  fetchOnServer: true,
  fetchKey: "settings-themes",
  setup() {
    return {
      ColorSchemeEnum,
      ColorSchemeEnumMetadata
    };
  },
  filters: {
    numberToString: (number: number) => {
      return number.toString();
    }
  }
})
export default class ThemeSettings extends Vue {
  // #region Data
  public listLoading: boolean = false;
  public loading: boolean = false;

  @SerialiseClass(NewsModel)
  public mockNews: NewsModel = new NewsModel({
      id: 1,
      title: "Nouveautés de la gazette",
      content: "Animer davantage morceau prétendre de vivant complet. Soirée pouvoir causer dix. Trou cou quel classe signifier. Droite appeler sentier neuf rencontrer trait année fond. Bête sous parfois cacher creuser ventre. L'Une cercle dernier million ce mourir.",
      post_date: new Date(),
      comment_count: 1,
      authors: [new AuthorData({ username: "L'équipe des news" })]
    });

  @SerialiseClass(FanfictionModel)
  public mockFiction: FanfictionModel = new FanfictionModel({
      id: 1,
      authors: [new AuthorData({ username: "L'auteur de la fiction" })],
      title: "Mon histoire favorite",
      average: 8.5,
      summary: "Drame mal branche demi. Exprimer occasion secours étude autrement grandir trop témoin. Chaque toi inspirer cacher but fumer. Contraire bande charge jambe essayer habiter puis. Histoire couper intérêt compter impossible. Mot revoir place parole rouge fois. Éprouver passion résoudre abattre tôt avoir pointe. Ignorer cou bas dame ailleurs français. Franchir d'autres allumer réfléchir peser.",
      characteristics: [
        new CharacteristicData({ id: 1, characteristic_type_id: 5, name: "Tous" }),
        new CharacteristicData({ id: 2, characteristic_type_id: 4, name: "Lime" }),
        new CharacteristicData({ id: 3, characteristic_type_id: 8, name: "Quidditch" }),
        new CharacteristicData({ id: 4, characteristic_type_id: 4, name: "Lemon soft" }),
        new CharacteristicData({ id: 5, characteristic_type_id: 3, name: "Breton" }),
        new CharacteristicData({ id: 6, characteristic_type_id: 2, name: "Autres fics HP" }),
        new CharacteristicData({ id: 7, characteristic_type_id: 1, name: "Roman" }),
        new CharacteristicData({ id: 8, characteristic_type_id: 2, name: "Polar/enquête" }),
        new CharacteristicData({ id: 9, characteristic_type_id: 2, name: "Slash/Yaoi" }),
        new CharacteristicData({ id: 10, characteristic_type_id: 7, name: "Lily L. Potter" })
      ],
      chapter_count: 7,
      word_count: 105236,
      read_count: 892,
      review_count: 10,
      creation_date: new Date(),
      last_update_date: new Date(),
      modification_date: new Date()
    });

  @SerialiseClass(ThemeModel)
  public themes: ThemeModel [] = [];

  @SerialiseClass(ThemeModel)
  public selectedTheme: ThemeModel | null = null;

  public selectedDetail: ThemeDetail | null = null;

  // Timer de debounce sur le change thème
  private timerThrottleChangeTheme: number = 0;
  // #endregion

  // #region Computed
  get ConfigModule(): Config {
    return getModule(Config, this.$store);
  }

  get mockFanfictionsList(): FanfictionModel[] {
    return [this.mockFiction, this.mockFiction];
  }

  get formIsValid(): boolean {
    if (this.selectedTheme == null ||
    (this.selectedTheme.recordStatus === RecordStatusEnum.Deleted) ||
    (this.selectedTheme.recordStatus === RecordStatusEnum.Unchanged) ||
    (this.selectedTheme.name.length === 0)) return false;
    return true;
  }
  // #endregion

  // #region Watchers
  @Watch("selectedTheme")
  public onselectedThemeChanged(): void {
    if (this.selectedTheme == null) {
      this.selectedDetail = null;
      return;
    }
    if (this.selectedTheme?.details == null || this.selectedTheme.details.length === 0) {
      // Détail par défaut
      this.selectedTheme.details = [
        new ThemeDetail({
          primary: "#42162b",
          primary_light: "#8f5a74",
          hpf_primary_lighter: "#E8D7E0",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Light
        }),
        new ThemeDetail({
          primary: "#2A2346",
          primary_light: "#3A3F4C",
          hpf_primary_lighter: "#24292E",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Dark
        }),
        new ThemeDetail({
          primary: "#2A2346",
          primary_light: "#3A3F4C",
          hpf_primary_lighter: "#24292E",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Contrast
        })
      ];
    }
    this.selectedDetail = this.selectedTheme.details[0];
    // Actualisation de l'UI
    this.$changeTheme(this.selectedDetail);
  }
  // #endregion

  // #region Hooks
  // Récupérer les données
  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des themes
    await this.getThemes();
    // Sélection du premier item disponible
    if ((this.themes?.length ?? 0) > 0) this.selectedTheme = this.themes[0];
    this.listLoading = false;
  }

  // Hook de destruction
  destroyed(): void {
    // Remettre le theme défaut actuel
    this.$changeTheme(this.ConfigModule.currentTheme?.details[0] ?? null);
  }
  // #endregion

  // #region Methods
  // Changement de couleur depuis le footer
  public colorInput(event:any): void {
    if (this.selectedDetail == null) return;

    const regex = /^#[a-fA-F0-9]{6}$/g;
    if (regex.test(event.target.value)) {
      if (event.target.id === "primaryColorInput") this.selectedDetail.primary = event.target.value;
      else if (event.target.id === "lightColorInput") this.selectedDetail.primary_light = event.target.value;
      else if (event.target.id === "lightAlternativeColorInput") this.selectedDetail.hpf_primary_lighter = event.target.value;
      else if (event.target.id === "lightAlternativeColorInput") this.selectedDetail.hpf_primary_lighter = event.target.value;
      this.editorChanged(event.target);
    }
  }

  // Changement de couleur primaire
  public primaryColorChanged(value: any): void {
    if (this.selectedDetail != null) {
      clearTimeout(this.timerThrottleChangeTheme);
      this.timerThrottleChangeTheme = window.setTimeout(
        () => {
          if (this.selectedDetail != null) {
            this.selectedDetail.primary = value.toString(); this.editorChanged(value);
          }
        },
        150
      );
    }
  }

  // Changement de couleur light
  public lightColorChanged(value: any): void {
    if (this.selectedDetail != null) {
      clearTimeout(this.timerThrottleChangeTheme);
      this.timerThrottleChangeTheme = window.setTimeout(
        () => {
          if (this.selectedDetail != null) {
            this.selectedDetail.primary_light = value.toString(); this.editorChanged(value);
          }
        },
        150
      );
    }
  }

  // Changement de couleur light alternative
  public lightAlternativeColorChanged(value: any): void {
    if (this.selectedDetail != null) {
      clearTimeout(this.timerThrottleChangeTheme);
      this.timerThrottleChangeTheme = window.setTimeout(
        () => {
          if (this.selectedDetail != null) {
            this.selectedDetail.hpf_primary_lighter = value.toString();
            this.editorChanged(value);
          }
        },
        150
      );
    }
  }

  // Détecter un changement sur l'éditeur
  public editorChanged(sender: any): void {
    if (this.selectedTheme != null) {
      // Indiquer que l'item a subi des changements
      if (sender != null && this.selectedTheme.recordStatus !== RecordStatusEnum.Added) this.selectedTheme.recordStatus = RecordStatusEnum.Updated;
      if (this.selectedDetail != null) {
        this.$changeTheme(this.selectedDetail);
      }
    }
  }

  // Commencer l'édition d'un élément
  public beginEdit(theme: ThemeModel):void {
    // Confirmation de quitter sans sauvegarder
    if (this.selectedTheme != null && (this.selectedTheme.recordStatus === RecordStatusEnum.Added || this.selectedTheme.recordStatus === RecordStatusEnum.Updated)) {
      this.$buefy.snackbar.open({
        indefinite: true,
        message: "Vous avez des modifications non enregistrées, êtes-vous sur de vouloir continuer ?",
        cancelText: "Annuler",
        actionText: "Confirmer",
        type: "is-warning",
        onAction: () => {
          // On ne tient pas compte des modifications et on passe à la suite
          this.themes = this.themes.filter((item: ThemeModel) => item.id !== 0);
          this.selectedTheme = structuredClone(theme);
        }
      });
    } else {
      this.selectedTheme = structuredClone(theme);
    }
    // Focus sur le libellé
    (this.$refs.TxtSelectedTheme_Name as any).focus();
  }

  // Copier dans le presse papier
  public async writeClipboardText(text: string): Promise<void> {
    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
    }
  }

  // Appel à l'API pour récupérer les items
  private async getThemes(): Promise<void> {
    try {
      const response = (await getPrivateThemes(null));
      this.themes = response.results;
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des thèmes",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    }
  }

  // Insérer / Mettre à jour le thème
  public async updateItem(): Promise<void> {
    try {
      if (this.selectedTheme == null) return;
      this.loading = true;
      let toastMessage = "";
      if (this.selectedTheme.recordStatus === RecordStatusEnum.Added) {
        const result = await postTheme(this.selectedTheme);
        this.selectedTheme = result;
        toastMessage = "Thème ajouté";
      } else if (this.selectedTheme.recordStatus === RecordStatusEnum.Updated) {
        const result = await putTheme(this.selectedTheme.id, this.selectedTheme);
        this.selectedTheme = result;
        toastMessage = "Thème mis à jour";
      }

      OpenToast(
        toastMessage,
        "is-primary",
        5000,
        false,
        true,
        "is-bottom"
      );
    } catch (exception) {
      OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
    } finally {
      this.loading = false;
    }
  }

  // Supprimer un thème
  public deleteItem(): void {
    if (this.selectedTheme === null) return;

    // Confirmer l'action (seulement si ce n'est pas un nouvel item)
    if (this.selectedTheme.id > 0) {
      this.$buefy.snackbar.open({
        indefinite: true,
        message: "Confirmer la suppression ? (action irréversible)",
        cancelText: "Annuler",
        actionText: "Confirmer",
        type: "is-danger",
        onAction: async () => {
          if (this.selectedTheme == null) return;
          try {
            this.loading = true;
            await deleteTheme(this.selectedTheme.id);
            // Suppression local
            this.themes = this.themes.filter((item: ThemeModel) => item.id !== this.selectedTheme?.id);
            this.selectedTheme = null;
            OpenToast(
              "Thème supprimé",
              "is-primary",
              5000,
              false,
              true,
              "is-bottom"
            );
          } catch (exception) {
            OpenToast("Erreur : " + (exception as Error).message, "is-danger", 5000, false, true, "is-bottom");
          } finally {
            this.loading = false;
          }
        }
      });
    } else {
      // Supprimer l'item local par encore enregistré
      this.themes = this.themes.filter((item: ThemeModel) => item.id !== 0);
      this.selectedTheme = null;
    }
  }

  // Ajout d'un nouveau thème
  public onNewTheme(): void {
    // Enlever les précédents nouveaux items non poussés
    this.themes = this.themes.filter((item: ThemeModel) => item.id !== 0);

    // Créer la nouvelle entrée
    const newItem = new ThemeModel({
      id: 0,
      recordStatus: RecordStatusEnum.Added,
      name: this.themes.length === 0 ? "Défaut" : "Nouveau thème",
      default: this.themes.length === 0,
      enabled: this.themes.length === 0,
      use_default_from: null,
      use_default_to: null,
      details: [
        new ThemeDetail({
          primary: "#42162b",
          primary_light: "#8f5a74",
          hpf_primary_lighter: "#E8D7E0",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Light
        }),
        new ThemeDetail({
          primary: "#2A2346",
          primary_light: "#3A3F4C",
          hpf_primary_lighter: "#24292E",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Dark
        }),
        new ThemeDetail({
          primary: "#2A2346",
          primary_light: "#3A3F4C",
          hpf_primary_lighter: "#24292E",
          banner_url: "https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg",
          colorScheme: ColorSchemeEnum.Contrast
        })
      ]
    });

    // L'ajouter aux entrées existantes
    this.themes.push(newItem);

    // Après l'ajout dans le dom, l'afficher (en scrollant si nécessaire)
    this.$nextTick(() => {
      const newThemeRow = (this.$refs["theme_row_" + newItem.id.toString()] as any);
      newThemeRow[0].scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    });

    // La sélectionner
    this.beginEdit(newItem);
  }

  // On change de detail
  public detailsTabChanged(value: number): void {
    if (this.selectedTheme?.details == null || this.selectedTheme?.details.length < value) return;
    this.selectedDetail = this.selectedTheme.details[value];
    this.$changeTheme(this.selectedDetail);
  }
  // #endregion
}

</script>

<style lang="scss" scoped>
// *{
//   border: 1px solid green;
// }

.custom-scrollbar-bio {
  height: auto;
  max-height: 110px;
}

.theme-list-item-wrapper{
  border-radius: 4px;
}

.theme-list:hover{
  font-weight: var(--weight-bold) !important;
}

.rounded-square {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.hero-body {
  background-image: var(--hpf-banner);
  background-size: 100% 100%;
}

#banner h1 {
  font-size: 25px;
  background-color: rgba(255, 255, 255, 0.6);
  font-family: "Amiri", serif;
  text-transform: uppercase;
  text-align: center;
  padding: 0px 10px;
}

#add-new-theme{
  border: 1px dashed var(--primary);
  border-radius: 4px;
  // height: 30px;
  // width: 100%;
}

#add-new-theme:hover{
  background-color: var(--hpf-primary-lighter);
}
</style>
