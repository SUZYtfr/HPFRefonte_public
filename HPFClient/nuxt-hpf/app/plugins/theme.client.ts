import { ColorSchemeEnum } from "~/types/themes";

export default defineNuxtPlugin(() => {
  const { themes } = useConfigStore();
  const { accountData } = useCustomAuth();

  async function updateThemeDetails(): Promise<void> {
    const { theme: userThemeId, colorScheme: userColorScheme, themeOverridenAt } = accountData.value?.preferences || { theme: undefined, colorScheme: undefined, themeOverridenAt: undefined };

    // Thème événementiel ou thème par défaut en fallback
    let currentTheme = themes.find((theme) => theme.isCurrent) || themes.find(theme => theme.default)!;

    // Si le thème préféré est défini, et imposé sur le thème événementiel le cas échéant, on l'utilise
    if (userThemeId) {
      const userTheme = themes.find(theme => theme.themeId == userThemeId);
      if (userTheme) {
        if (currentTheme.isCurrent && ((themeOverridenAt || new Date(0)) < currentTheme.useDefaultFrom!)) {
          // rien
        }
        else {
          currentTheme = userTheme;
        }
      }
    }

    // variante préférée, ou variante par défaut en fallback  
    const themeDetail = currentTheme.details.find(d => d.colorScheme == userColorScheme || ColorSchemeEnum.Light)!;
    useChangeTheme(themeDetail);
  }

  watch(accountData, () => updateThemeDetails(), { immediate: true });
});
