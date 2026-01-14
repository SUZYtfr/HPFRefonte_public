import { type ThemeDetail, ColorSchemeEnum } from "@/types/themes.ts";
import { hexToRgb, rgbToHsl } from "@/utils/color.ts";

export const useChangeTheme = (theme: ThemeDetail | null): void => {
  if (theme === null) return;
  assignCssVar("--primary", theme.primary);
  assignCssVar("--primary-light", theme.primaryLight);
  assignCssVar("--hpf-primary-lighter", theme.hpfPrimaryLighter);
  if (theme.colorScheme === ColorSchemeEnum.Dark) {
    assignCssVar("--scheme-main", "#14161A");
    assignCssVar("--scheme-main-bis", "#181B20");
    assignCssVar("--scheme-main-ter", "#1D1F26");
    assignCssVar("--background", "#1F2229");
    assignCssVar("--border-weak", "#2E333D");
    assignCssVar("--border", "#353A46");
    assignCssVar("--text-weak", "#6A7489");
    assignCssVar("--text", "#ABB1BF");
    assignCssVar("--text-strong", "#EBECF0");
    assignCssVar("--text-title", "#FFFFFF");
    document.documentElement.style.setProperty("--hover-background-l-delta", "5%");
    document.documentElement.style.setProperty("--active-background-l-delta", "10%");
    document.documentElement.style.setProperty("--hover-border-l-delta", "10%");
    document.documentElement.style.setProperty("--active-border-l-delta", "20%");
    document.documentElement.style.setProperty("--hover-color-l-delta", "5%");
    document.documentElement.style.setProperty("--active-color-l-delta", "10%");
  } else {
    assignCssVar("--scheme-main", "#FFFFFF");
    assignCssVar("--scheme-main-bis", "#F9FAFB");
    assignCssVar("--scheme-main-ter", "#F3F4F6");
    assignCssVar("--background", "#F3F4F6");
    assignCssVar("--border-weak", "#EBECF0");
    assignCssVar("--border", "#D6D9E0");
    assignCssVar("--text-weak", "#69748C");
    assignCssVar("--text", "#404654");
    assignCssVar("--text-strong", "#2E333D");
    assignCssVar("--text-title", "#1F2229");
    document.documentElement.style.setProperty("--hover-background-l-delta", "5%");
    document.documentElement.style.setProperty("--active-background-l-delta", "10%");
    document.documentElement.style.setProperty("--hover-border-l-delta", "10%");
    document.documentElement.style.setProperty("--active-border-l-delta", "20%");
    document.documentElement.style.setProperty("--hover-color-l-delta", "5%");
    document.documentElement.style.setProperty("--active-color-l-delta", "10%");
  }
  document.documentElement.style.setProperty("--hpf-banner", "url(" + theme.bannerUrl + ")");
};

function assignCssVar(cssVar: string, hexColor: string): void {
  // color
  document.documentElement.style.setProperty(cssVar, hexColor);
  // rgb
  const rgbPrimary = hexToRgb(hexColor);
  document.documentElement.style.setProperty(
    cssVar + "-rgb",
    Math.round(rgbPrimary?.[0] ?? 255).toString() +
      "," +
      Math.round(rgbPrimary?.[1] ?? 255).toString() +
      "," +
      Math.round(rgbPrimary?.[2] ?? 255).toString(),
  );
  // h, s, l
  const hslPrimary = rgbToHsl(rgbPrimary?.[0] ?? 255, rgbPrimary?.[1] ?? 255, rgbPrimary?.[2] ?? 255);
  document.documentElement.style.setProperty(cssVar + "-h", Math.round(hslPrimary[0]).toString() + "deg");
  document.documentElement.style.setProperty(cssVar + "-s", Math.round(hslPrimary[1]).toString() + "%");
  document.documentElement.style.setProperty(cssVar + "-l", Math.round(hslPrimary[2]).toString() + "%");
}
