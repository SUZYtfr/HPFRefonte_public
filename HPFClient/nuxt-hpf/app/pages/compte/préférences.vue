<template>
  <div>
    <div class="columns">
      <div class="column card">
        <header class="card-header">
          <p class="card-header-title">Apparence</p>
        </header>
        <div class="card-content">
          <BField label="Thème">
            <BCarouselList v-model="selectedCarouselTheme" :data="themes" :items-to-show="4">
              <template #item="item: ThemeModel">
                <div class="card">
                  <header class="card-header">
                    <p
                      class="card-header-title"
                      :style="[
                        'background-color: ' + item.details[0]!.primary,
                        'color: ' + item.details[0]!.primaryLight,
                      ]"
                    >
                      {{ item.name }}
                    </p>
                  </header>
                  <div>
                    <BRadioButton
                      key="system"
                      v-model="dummySelectedRadioButton"
                      :native-value="item.id + '_system'"
                      @update:model-value="handleThemeRadioButtonChange(Number(item.id), 0)"
                    >
                      Paramètre système
                    </BRadioButton>
                    <BRadioButton
                      v-for="(detail, index) in item.details"
                      :key="index"
                      v-model="dummySelectedRadioButton"
                      :native-value="item.id + '_' + detail.colorScheme"
                      @update:model-value="handleThemeRadioButtonChange(Number(item.id), detail.colorScheme)"
                    >
                      {{ ColorSchemeEnumMetadata.get(detail.colorScheme)!.description }}
                    </BRadioButton>
                  </div>
                </div>
              </template>
            </BCarouselList>
          </BField>
          <BField label="Animations activées" horizontal>
            <BSwitch v-model="preferences.showAnimations" />
          </BField>
          <BField label="Afficher les avatars" horizontal>
            <BSwitch v-model="preferences.showProfilePictures" />
          </BField>
        </div>
      </div>
      <div class="column card">
        <header class="card-header">
          <p class="card-header-title">Lecture</p>
        </header>
        <div class="card-content">
          <BField label="Police d'écriture" horizontal>
            <BSelect v-model="preferences.font">
              <option v-for="[value, display] in fonts" :key="value">{{ display }}</option>
            </BSelect>
          </BField>
          <BField label="Taille de police" horizontal>
            <BNumberinput v-model="preferences.fontSize" min="7" max="32" />
          </BField>
          <BField label="Espace intercaractère" horizontal>
            <BNumberinput v-model="preferences.letterSpacing" min="0.2" max="2" step="0.1" />
          </BField>
          <BField label="Espace interligne" horizontal>
            <BNumberinput v-model="preferences.lineSpacing" min="0.2" max="2" step="0.1" />
          </BField>
          <BField label="Espace interparagraphe" horizontal>
            <BNumberinput v-model="preferences.paragraphSpacing" min="0.2" max="2" step="0.1" />
          </BField>
          <BField label="Afficher l'éditeur de review" horizontal>
            <BSwitch v-model="preferences.showReviewEditor" />
          </BField>
          <BField label="Lecteur toujours en mode diurne" horizontal>
            <BSwitch v-model="preferences.colorSchemeInReader" />
          </BField>
          <!-- <BField label="Afficher les réactions dans le texte" horizontal>
          <BSwitch v-model="" />
        </BField> -->
          <BField label="Rediriger sur le sommaire de la fiction" horizontal>
            <BSwitch v-model="preferences.redirectToSummary" />
          </BField>
          <BField label="Afficher les avertissements de contenu" horizontal>
            <BSwitch v-model="preferences.showTriggerWarnings" />
          </BField>
        </div>
      </div>
      <div class="column card">
        <header class="card-header">
          <p class="card-header-title">Recherche</p>
        </header>
        <div class="card-content">
          <BField label="Ordre de tri par défaut" horizontal>
            <BSelect v-model="preferences.resultOrder">
              <option v-for="(order, index) in resultOrders" :key="index" :value="index">{{ order }}</option>
            </BSelect>
          </BField>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column card">
        <header class="card-header">
          <p class="card-header-title">Notifications par courriel</p>
        </header>
        <div class="card-content">
          <BField label="Nouvelle review" horizontal>
            <BSwitch v-model="preferences.emailForReview" />
          </BField>
          <BField label="Nouvelle réponse à review" horizontal>
            <BSwitch v-model="preferences.emailForReply" />
          </BField>
          <BField label="Nouvelle actualité" horizontal>
            <BSwitch v-model="preferences.emailForNews" />
          </BField>
          <BField label="Nouvelle activité de favoris" horizontal>
            <BSwitch v-model="preferences.emailForFavoriteActivity" />
          </BField>
          <BField label="Nouvelle mise en favoris" horizontal>
            <BSwitch v-model="preferences.emailForFavorite" />
          </BField>
          <BField label="Changement de statut de publication" horizontal>
            <BSwitch v-model="preferences.emailForChapterStatus" />
          </BField>
          <BField label="Modération de contenu" horizontal>
            <BSwitch v-model="moderationEmails" disabled />
          </BField>
        </div>
      </div>
      <div class="column card">
        <header class="card-header">
          <p class="card-header-title">Droits de reviews</p>
        </header>
        <div class="card-content">
          <BField label="Droits des membres">
            <BSlider
              v-model="preferences.memberReviewPolicy"
              :min="0"
              :max="4"
              aria-label="memberReviewRights"
              :tooltip="false"
            >
              <BSliderTick v-for="(display, index) in ReviewPolicy" :key="index" :value="index">{{
                display
              }}</BSliderTick>
            </BSlider>
          </BField>
          <BField label="Droits des visiteurs">
            <BSlider
              v-model="preferences.anonymousReviewPolicy"
              :min="0"
              :max="4"
              aria-label="AnonymousReviewRights"
              :tooltip="false"
            >
              <BSliderTick v-for="(display, index) in ReviewPolicy" :key="index" :value="index">{{
                display
              }}</BSliderTick>
            </BSlider>
          </BField>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { UserPreferencesInput } from "#gql";
import { BField, BNumberinput, BSelect, BSwitch, BSlider, BSliderTick, BCarouselList, BRadioButton } from "buefy";
import type { ThemeModel } from "~/models";
import { ColorSchemeEnum, ColorSchemeEnumMetadata } from "~/types/themes";

const { accountData } = useCustomAuth();
const { preferences } = accountData.value!;
const { themes } = useConfigStore();

// Apparence

const selectedCarouselTheme = ref(0);
const dummySelectedRadioButton = ref();

function handleThemeRadioButtonChange(themeId: number, colorScheme: ColorSchemeEnum | 0): void {
  preferences.theme = themeId;
  preferences.colorScheme = colorScheme;
  // si colorscheme undefined: déterminer le paramètre navigateur
  const currentColorScheme =
    colorScheme ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches ? ColorSchemeEnum.Dark : ColorSchemeEnum.Light);

  useChangeTheme(themes.find((t) => t.themeId == themeId)!.details.find((d) => d.colorScheme == currentColorScheme)!);
}

const fonts = [
  ["Default", "Police par défaut"],
  ["Tahoma", "Tahoma"],
  ["Times New Roman", "Times New Roman"],
];

const resultOrders = [
  "Ordre alphabétique",
  "Ordre alphabétique inversé",
  "Ordre chronologique",
  "Ordre chronologique inversé",
];

const moderationEmails = ref<true>(true);

// Reviews
// const reviewWriteRights = ["Reviews désactivées", "Reviews par les inscrits", "Reviews anonymes autorisées"];
// const reviewGradingRights = ["Notation désactivées", "Notation par les inscrits", "Notation anonymes autorisées"];
// const reviewReadRights = ["Reviews masquées", "Reviews visibles aux inscrits", "Reviews visibles à tous"];
const ReviewPolicy = [
  "Désactivé",
  "Peuvent écrire des reviews",
  "Peuvent voir les reviews",
  "Peuvent ajouter une note aux reviews",
  "Peuvent voir les notes des reviews",
];

function updatePreferences(preferences: UserPreferencesInput): void {
  GqlUpdateUserPreferences({
    userPreferencesData: preferences,
  });
}
watch(preferences, () => updatePreferences(preferences));
</script>
