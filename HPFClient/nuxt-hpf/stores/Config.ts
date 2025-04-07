import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { ThemeModel } from "~/models";
import {
    searchCharacteristics,
    searchCharacteristicsTypes
} from "@/api/characteristics";
import { searchThemes } from "@/api/themes";

export const Config = defineStore("Config", () => {
    const characteristics = ref<CharacteristicModel[]>();
    const characteristicTypes = ref<CharacteristicTypeModel[]>();
    const themes = ref<ThemeModel[]>();
    // Theme actuel de l'utilisateur courant
    const currentTheme = computed<ThemeModel | null>(() => {
        let currentTheme = null;
        // Theme évènementiel
        currentTheme = themes.value.find(theme => theme.use_default_from != null && theme.use_default_to != null && theme.use_default_from <= new Date() && theme.use_default_to >= new Date()) ?? null;
    
        if (import.meta.client) {
          // Cas utilisateur connecté
          if ($auth.loggedIn && $auth.user?.preferences != null) {
            // Theme utilisateur
            // (si le thème évènementiel est null ou si l'utilisateur a overridé son thème)
            if ((currentTheme == null) ||
              (($auth.user.preferences as any).theme_overriden_at != null &&
                currentTheme.use_default_to != null &&
                new Date(($auth.user.preferences as any).theme_overriden_at) > currentTheme.use_default_to))
              currentTheme = themes.value.find(theme => theme.id === ($auth.user?.preferences as any).theme) ?? null;
          }
        }
    
        // Theme par défaut si pas de thème évènementiel / pas de thème utilisateur
        if (currentTheme == null) currentTheme = themes.value.find(theme => theme.default) ?? null;
    
        return currentTheme;
    })

    function setCharacteristics(chars: CharacteristicModel[]) { characteristics.value = chars }
    function setCharacteristicTypes(charTypes: CharacteristicTypeModel[]) { characteristicTypes.value = charTypes }
    function setThemes(publicThemes: ThemeModel[]) { themes.value = publicThemes }

    // Bizarrement il faut séparer ces deux appels dans leur méthodes respectives
    // Sinon on a une erreur:
    // [nuxt] A composable that requires access to the Nuxt instance was called outside 
    // of a plugin, Nuxt hook, Nuxt middleware, or Vue setup function. This is probably 
    // not a Nuxt bug.
    // (Mais je pense que c'est un Nuxt bug)
    // Il faut aussi rendre une valeur quelconque pour éviter que useAsyncData se plaigne.
    async function fetchCharacteristics(): Promise<true> {
        const { data: characteristicTemp } = await searchCharacteristics(null);
        setCharacteristics(characteristicTemp.value);
        return true
    }

    async function fetchCharacteristicTypes(): Promise<true> {
        const { data: characteristicTypesTemp } = await searchCharacteristicsTypes();
        setCharacteristicTypes(characteristicTypesTemp.value);
        return true
    }

    async function fetchThemes(): Promise<true> {
        const { data: themesTemp } = await searchThemes(null);
        setThemes(themesTemp.value.results);
        return true
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
    }
});
