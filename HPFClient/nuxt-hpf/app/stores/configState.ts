import { CharacteristicModel, CharacteristicTypeModel, ThemeModel } from "~/models";
import type { FandomData } from "~/types/fanfictions";
import { InvalidationReasonData } from "~/types/config";
import { plainToInstance } from "class-transformer";
import type { CharacteristicType, CharacteristicTypeType, ThemeType } from "#gql";


export const useConfigStore = defineStore("config", () => {
  //#region State
  const characteristics = ref<CharacteristicModel[]>();
  const characteristicTypes = ref<CharacteristicTypeModel[]>();
  const themes = ref<ThemeModel[]>();
  const fandoms = ref<FandomData[]>();
  // TODO appel à l'api, pour l'instant en dur.
  const invalidationReasons = ref<InvalidationReasonData[]>([
    new InvalidationReasonData({ id: 1, reason: "Taille trop courte" }),
    new InvalidationReasonData({ id: 2, reason: "Orthographe" }),
    new InvalidationReasonData({ id: 3, reason: "Grammaire" }),
    new InvalidationReasonData({ id: 4, reason: "Conjugaison" }),
    new InvalidationReasonData({ id: 5, reason: "Non-respect du réglement" }),
    new InvalidationReasonData({ id: 6, reason: "Mise en forme" }),
    new InvalidationReasonData({ id: 7, reason: "Autre" }),
  ]);
  //#endregion

  //#region Getter
  const currentTheme = computed(() => {
    if (themes.value == null || themes.value.length === 0) return null;

    const { data, isAuthenticated } = useCustomAuth();

    let currentTheme = null;
    // Theme évènementiel
    currentTheme =
      themes.value.find(
        (theme) =>
          theme.useDefaultFrom != null &&
          theme.useDefaultTo != null &&
          theme.useDefaultFrom <= new Date() &&
          theme.useDefaultTo >= new Date(),
      ) ?? null;

    // Cas utilisateur connecté
    if (isAuthenticated.value && data.value?.preferences != null) {
      // Theme utilisateur
      // (si le thème évènementiel est null ou si l'utilisateur a overridé son thème)
      if (
        currentTheme == null ||
        (data.value.preferences.themeOverridenAt != null &&
          currentTheme.useDefaultTo != null &&
          new Date(data.value.preferences.themeOverridenAt) > currentTheme.useDefaultTo)
      )
        currentTheme = themes.value.find((theme) => theme.id === data?.value?.preferences.theme) ?? null;
    }

    // Theme par défaut si pas de thème évènementiel / pas de thème utilisateur
    if (currentTheme == null) currentTheme = themes.value.find((theme) => theme.default) ?? null;

    return currentTheme;
  });
  //#endregion

  //#region Action
  function setCharacteristics(chars: CharacteristicModel[]): void {
    characteristics.value = chars;
  }
  function setCharacteristicTypes(charTypes: CharacteristicTypeModel[]): void {
    characteristicTypes.value = charTypes;
  }
  function setThemes(thms: ThemeModel[]): void {
    themes.value = thms;
  }
  function setFandoms(fdoms: FandomData[]): void {
    fandoms.value = fdoms;
  }
  //#endregion

  // Bizarrement il faut séparer ces deux appels dans leur méthodes respectives
  // Sinon on a une erreur:
  // [nuxt] A composable that requires access to the Nuxt instance was called outside
  // of a plugin, Nuxt hook, Nuxt middleware, or Vue setup function. This is probably
  // not a Nuxt bug.
  // (Mais je pense que c'est un Nuxt bug)
  // Il faut aussi rendre une valeur quelconque pour éviter que useAsyncData se plaigne.
  async function fetchCharacteristics(): Promise<true> {
    const { data: characteristicTemp } = await useAsyncGql('getCharacteristics', {}, {
      transform: (data: { characteristics: CharacteristicType[] }) => {
        return plainToInstance(CharacteristicModel, data.characteristics)
      }
    });
    setCharacteristics(characteristicTemp.value ?? []);
    return true;
  }

  async function fetchCharacteristicTypes(): Promise<true> {
    const { data: characteristicTypesTemp } = await useAsyncGql('getCharacteristicTypes', {}, {
      transform: (data: { characteristicTypes: CharacteristicTypeType[] }) => {
        return plainToInstance(CharacteristicTypeModel, data.characteristicTypes)
      }
    });
    setCharacteristicTypes(characteristicTypesTemp.value ?? []);
    return true;
  }

  async function fetchThemes(): Promise<true> {
    const { data: themesTemp } = await useAsyncGql('getThemes', {}, {
      transform: (data: { themes: ThemeType[] }) => {
        return plainToInstance(ThemeModel, data.themes)
      }
    })
    setThemes(themesTemp.value ?? []);
    return true;
  }

  async function fetchFandoms(): Promise<true> {
    const { data: fdoms } = await useAsyncGql('getFandoms', {}, {
      transform: (data: { fandoms: FandomData[] }) => {
        return data.fandoms
      }
    });
    setFandoms(fdoms.value ?? []);
    return true;
  }

  return {
    characteristics,
    characteristicTypes,
    themes,
    currentTheme,
    fandoms,
    invalidationReasons,
    // setCharacteristics,
    // setCharacteristicTypes,
    fetchCharacteristicTypes,
    fetchCharacteristics,
    fetchThemes,
    fetchFandoms,
  };
});
