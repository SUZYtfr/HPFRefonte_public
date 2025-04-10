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
                  v-for="(theme) in paginatedThemes?.results || []"
                  :key="theme.id"
                  :ref="(el) => { instance.refs[`theme_row_${theme.id.toString()}`] = el }"
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
                  :ref="(el) => { instance.refs['txt-selected-theme-name'] = el }"
                  v-model="selectedTheme.name"
                  type="text"
                  placeholder="Libellé"
                  required
                  :expanded="true"
                />
              </b-field>
              <div class="is-flex is-flex-direction-row">
                <b-field>
                  <b-checkbox v-model="selectedTheme.default">
                    Theme par défaut
                  </b-checkbox>
                </b-field>
                <b-field>
                  <b-checkbox v-model="selectedTheme.enabled">
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
                    />
                  </b-field>
                </div>
              </client-only>
              <b-tabs v-if="selectedTheme.details != null && selectedTheme.details.length > 0" class="mt-3" type="is-toggle" expanded v-model=selectedDetailIndex>
                <template v-for="(detail, index) in selectedTheme.details" :key="index">
                  <b-tab-item
                    :value="index.toString()"
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
                        <b-colorpicker v-model="selectedDetail.primary" representation="square" class="mr-2">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="primaryColorInput"
                                v-model=selectedDetail.primary
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
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
                        <b-colorpicker v-model="selectedDetail.primary_light" representation="square" class="mr-2">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="lightColorInput"
                                v-model=selectedDetail.primary_light
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
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
                        <b-colorpicker v-model="selectedDetail.hpf_primary_lighter" representation="square" class="mr-2">
                          <template #footer>
                            <b-field type="is-primary">
                              <b-input
                                id="lightAlternativeColorInput"
                                v-model=selectedDetail.hpf_primary_lighter
                                type="text"
                                pattern="^#[a-fA-F0-9]{6}$"
                                validation-message="Veuillez saisir une couleur au format hexadecimal"
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

<script setup lang="ts">
import { searchThemes, postTheme, putTheme, deleteTheme } from '~/api/private/themes';
import { RecordStatusEnum } from "@/types/basics";
import { ThemeDetail, ColorSchemeEnum, ColorSchemeEnumMetadata } from "@/types/themes";
import { AuthorData } from "@/types/users";""
import { CharacteristicData } from "@/types/characteristics";
import { ThemeModel, NewsModel, FanfictionModel } from '@/models';
import { SnackbarProgrammatic as Snackbar } from 'buefy';
// import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";
// import FanfictionThumbnailList from "~/components/list/fanfictions/FanfictionThumbnailList.vue";
// import Fanfiction from "~/components/Fanfiction.vue";
// import { OpenToast } from "@/utils/formHelper";

const instance = getCurrentInstance();

const mockNews: NewsModel = new NewsModel({
  id: 1,
  title: "Nouveautés de la gazette",
  content: "Animer davantage morceau prétendre de vivant complet. Soirée pouvoir causer dix. Trou cou quel classe signifier. Droite appeler sentier neuf rencontrer trait année fond. Bête sous parfois cacher creuser ventre. L'Une cercle dernier million ce mourir.",
  post_date: new Date(),
  comment_count: 1,
  authors: [new AuthorData({ username: "L'équipe des news" })]
});

const mockFiction: FanfictionModel = new FanfictionModel({
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
  first_chapter: { id: 1, title: "Chapitre 1", order: 1 },
  chapter_count: 7,
  word_count: 105236,
  read_count: 892,
  review_count: 10,
  creation_date: new Date(),
  last_update_date: new Date(),
  modification_date: new Date()
});

const selectedTheme = ref<ThemeModel | null>(null);
const selectedDetail = ref<ThemeDetail | null>(null);

const { data: paginatedThemes, status: themeStatus } = await searchThemes(null);
const listLoading = computed(() => themeStatus.value === 'pending');
const loading = ref<boolean>(false);

// On sélectionne par défaut le thème par défaut au chargement initial du module
// TODO Peut-être plutôt le thème actuel?
watch(paginatedThemes, () => {
  selectedTheme.value = paginatedThemes.value?.results.find(_t => _t.default) || null;
  selectedDetail.value = selectedTheme.value?.details[0] || null;
});
watch(selectedTheme, () => {
  selectedDetail.value = selectedTheme.value.details[0] || null;
});
watch(selectedDetail, () => {
  changeTheme(selectedDetail.value);
}, {
  deep: true
});


// Timer de debounce sur le change thème
let timerThrottleChangeTheme: number = 0;

const ConfigModule = Config();

function formIsValid(): boolean {
  if (selectedTheme.value == null ||
  (selectedTheme.value.recordStatus === RecordStatusEnum.Deleted) ||
  (selectedTheme.value.recordStatus === RecordStatusEnum.Unchanged) ||
  (selectedTheme.value.name.length === 0)) return false;
  return true;
}

onBeforeUnmount(() => {
  changeTheme(Config().currentTheme?.details[0] ?? null);
});

// Idem qu'en dessous
// Changement de couleur depuis le footer
function colorInput(event: any): void {
  if (selectedDetail.value == null) return;

  const regex = /^#[a-fA-F0-9]{6}$/g;
  if (regex.test(event.target.value)) {
    if (event.target.id === "primaryColorInput") selectedDetail.value.primary = event.target.value;
    else if (event.target.id === "lightColorInput") selectedDetail.value.primary_light = event.target.value;
    else if (event.target.id === "lightAlternativeColorInput") selectedDetail.value.hpf_primary_lighter = event.target.value;
  }
}

// FIXME b-color-picker :value et @input ont l'air cassés, j'ai remplacé par v-model mais on perd le timeout
// Changement de couleur primaire
function primaryColorChanged(value: any): void {
  if (selectedDetail.value != null) {
    clearTimeout(timerThrottleChangeTheme);
    timerThrottleChangeTheme = window.setTimeout(
      () => {
        if (selectedDetail.value != null) {
          selectedDetail.value.primary = value.toString();
        }
      },
      150
    );
  }
}

// Changement de couleur light
function lightColorChanged(value: any): void {
  if (selectedDetail.value != null) {
    clearTimeout(timerThrottleChangeTheme);
    timerThrottleChangeTheme = window.setTimeout(
      () => {
        if (selectedDetail.value != null) {
          selectedDetail.value.primary_light = value.toString();
        }
      },
      150
    );
  }
}

// Changement de couleur light alternative
function lightAlternativeColorChanged(value: any): void {
  if (selectedDetail.value != null) {
    clearTimeout(timerThrottleChangeTheme);
    timerThrottleChangeTheme = window.setTimeout(
      () => {
        if (selectedDetail.value != null) {
          selectedDetail.value.hpf_primary_lighter = value.toString();
        }
      },
      150
    );
  }
}

// Détecter un changement sur l'éditeur
function editorChanged(sender: any): void {
  if (selectedTheme.value != null) {
    // Indiquer que l'item a subi des changements
    if (sender != null && selectedTheme.value.recordStatus !== RecordStatusEnum.Added) selectedTheme.value.recordStatus = RecordStatusEnum.Updated;
    if (selectedDetail.value != null) {
      changeTheme(selectedDetail.value);
    }
  }
}

// Commencer l'édition d'un élément
function beginEdit(theme: ThemeModel):void {
  // Confirmation de quitter sans sauvegarder
  if (selectedTheme.value != null && (selectedTheme.value.recordStatus === RecordStatusEnum.Added || selectedTheme.value.recordStatus === RecordStatusEnum.Updated)) {
    new Snackbar().open({
      indefinite: true,
      message: "Vous avez des modifications non enregistrées, êtes-vous sur de vouloir continuer ?",
      cancelText: "Annuler",
      actionText: "Confirmer",
      type: "is-warning",
      onAction: () => {
        // On ne tient pas compte des modifications et on passe à la suite
        paginatedThemes.value.results = paginatedThemes.value.results.filter((item: ThemeModel) => item.id !== 0);
        selectedTheme.value = structuredClone(toRaw(theme));
      }
    });
  } else {
    selectedTheme.value = structuredClone(toRaw(theme));
  }
  // Focus sur le libellé
  (instance.refs['txt-selected-theme-name'] as any).focus();
}

async function writeClipboardText(text: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(text);
  } catch (error) {
  }
}

// Insérer / Mettre à jour le thème
async function updateItem(): Promise<void> {
  try {
    if (selectedTheme.value == null) return;
    loading.value = true;
    let toastMessage = "";
    if (selectedTheme.value.recordStatus === RecordStatusEnum.Added) {
      const result = await postTheme(selectedTheme.value);
      selectedTheme.value = result.data.value;
      toastMessage = "Thème ajouté";
    } else if (selectedTheme.value.recordStatus === RecordStatusEnum.Updated) {
      const result = await putTheme(selectedTheme.value.id, selectedTheme.value);
      selectedTheme.value = result.data.value;
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
    loading.value = false;
  }
}

// Supprimer un thème
function deleteItem(): void {
  if (selectedTheme.value === null) return;

  // Confirmer l'action (seulement si ce n'est pas un nouvel item)
  if (selectedTheme.value.id > 0) {
    new Snackbar().open({
      indefinite: true,
      message: "Confirmer la suppression ? (action irréversible)",
      cancelText: "Annuler",
      actionText: "Confirmer",
      type: "is-danger",
      onAction: async () => {
        if (selectedTheme.value == null) return;
        try {
          loading.value = true;
          await deleteTheme(selectedTheme.value.id);
          // Suppression local
          paginatedThemes.value.results = paginatedThemes.value.results.filter((item: ThemeModel) => item.id !== selectedTheme.value?.id);
          selectedTheme.value = null;
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
          loading.value = false;
        }
      }
    });
  } else {
    // Supprimer l'item local par encore enregistré
    paginatedThemes.value.results = paginatedThemes.value.results.filter((item: ThemeModel) => item.id !== 0);
    selectedTheme.value = null;
  }
}

// Ajout d'un nouveau thème
function onNewTheme(): void {
  // Enlever les précédents nouveaux items non poussés
  paginatedThemes.value.results = paginatedThemes.value.results.filter((item: ThemeModel) => item.id !== 0);

  // Créer la nouvelle entrée
  const newItem = new ThemeModel({
    id: 0,
    recordStatus: RecordStatusEnum.Added,
    name: paginatedThemes.value.results.length === 0 ? "Défaut" : "Nouveau thème",
    default: paginatedThemes.value.results.length === 0,
    enabled: paginatedThemes.value.results.length === 0,
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
  paginatedThemes.value.results.push(newItem);

  // Après l'ajout dans le dom, l'afficher (en scrollant si nécessaire)
  nextTick(() => {
    const newThemeRow = (instance.refs[`theme_row_${newItem.id.toString()}`] as any);
    newThemeRow.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
  });

  // La sélectionner
  beginEdit(newItem);
}

// b-tabs @input ne semble plus fonctionner, @click event.detail donne toujours 1...
// On change de detail
// function detailsTabChanged(event: Event & { detail: number }): void {
//   console.log(event.detail)  // FIXME pourquoi toujours 1 ???
//   if (selectedTheme.value?.details == null || selectedTheme.value?.details.length < event.detail) return;
//   selectedDetail.value = selectedTheme.value.details[event.detail];
// }

// Ça marche, mais quelle horreur
const selectedDetailIndex = computed<number>({
  get: () => { return selectedTheme.value.details.indexOf(selectedDetail.value) },
  set: (tabIndex: number) => { selectedDetail.value = selectedTheme.value.details[tabIndex]; },
})
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