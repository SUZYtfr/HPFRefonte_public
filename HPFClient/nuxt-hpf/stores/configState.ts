import type { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics.ts";
import type { ThemeModel } from "~/models/themes";
import { searchCharacteristics, searchCharacteristicsTypes } from "@/api/characteristics.ts";
import { getPublicThemes } from "@/api/themes.ts";

export const useConfigStore = defineStore("config", () => {
  //#region State
  const characteristics = ref<CharacteristicModel[]>();
  const characteristicTypes = ref<CharacteristicTypeModel[]>();
  const themes = ref<ThemeModel[]>();
  //#endregion

  //#region Getter
  const currentTheme = computed(() => {
    if (themes.value == null || themes.value.length === 0) return null;

    const { data, status } = useAuth();

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
    if (status.value === "authenticated" && data.value?.preferences != null) {
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
  //#endregion

  // Bizarrement il faut séparer ces deux appels dans leur méthodes respectives
  // Sinon on a une erreur:
  // [nuxt] A composable that requires access to the Nuxt instance was called outside
  // of a plugin, Nuxt hook, Nuxt middleware, or Vue setup function. This is probably
  // not a Nuxt bug.
  // (Mais je pense que c'est un Nuxt bug)
  // Il faut aussi rendre une valeur quelconque pour éviter que useAsyncData se plaigne.
  async function fetchCharacteristics(): Promise<true> {
    const { data: characteristicTemp } = await searchCharacteristics(null);
    setCharacteristics(characteristicTemp.value ?? []);
    return true;
  }

  async function fetchCharacteristicTypes(): Promise<true> {
    const { data: characteristicTypesTemp } = await searchCharacteristicsTypes();
    setCharacteristicTypes(characteristicTypesTemp.value ?? []);
    return true;
  }

  async function fetchThemes(): Promise<true> {
    const { data: themesTemp } = await getPublicThemes(null);
    setThemes(themesTemp.value?.results ?? []);
    return true;
  }

  return {
    characteristics,
    characteristicTypes,
    themes,
    currentTheme,
    // setCharacteristics,
    // setCharacteristicTypes,
    fetchCharacteristicTypes,
    fetchCharacteristics,
    fetchThemes,
  };
});
