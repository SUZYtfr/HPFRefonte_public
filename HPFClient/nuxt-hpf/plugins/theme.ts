// import { ColorSchemeEnum, ThemeDetail } from "@/types/themes";
// import { hexToHsl, hexToRgb, invertHex, rgbToHsl } from "@/utils/color";

// function assignCssVar(cssVar: string, hexColor: string): void {
//   // color
//   document.documentElement.style.setProperty(cssVar, hexColor);
//   // rgb
//   const rgbPrimary = hexToRgb(hexColor);
//   document.documentElement.style.setProperty(cssVar + "-rgb", Math.round(rgbPrimary[0]).toString() + "," + Math.round(rgbPrimary[1]).toString() + "," + Math.round(rgbPrimary[2]).toString());
//   // h, s, l
//   const hslPrimary = rgbToHsl(rgbPrimary[0], rgbPrimary[1], rgbPrimary[2]);
//   document.documentElement.style.setProperty(cssVar + "-h", Math.round(hslPrimary[0]).toString() + "deg");
//   document.documentElement.style.setProperty(cssVar + "-s", Math.round(hslPrimary[1]).toString() + "%");
//   document.documentElement.style.setProperty(cssVar + "-l", Math.round(hslPrimary[2]).toString() + "%");
// }

// export default defineNuxtPlugin(() => {
//   return {
//     provide: {
//       changeTheme: (theme: ThemeDetail | null) => {
//         if (theme === null) return;
//         assignCssVar("--primary", theme.primary);
//         assignCssVar("--primary-light", theme.primary_light);
//         assignCssVar("--hpf-primary-lighter", theme.hpf_primary_lighter);
//         if (theme.colorScheme === ColorSchemeEnum.Dark) {
//           assignCssVar("--scheme-main", "#14161A");
//           assignCssVar("--scheme-main-bis", "#181B20");
//           assignCssVar("--scheme-main-ter", "#1D1F26");
//           assignCssVar("--background", "#1F2229");
//           assignCssVar("--border-weak", "#2E333D");
//           assignCssVar("--border", "#353A46");
//           assignCssVar("--text-weak", "#6A7489");
//           assignCssVar("--text", "#ABB1BF");
//           assignCssVar("--text-strong", "#EBECF0");
//           assignCssVar("--text-title", "#FFFFFF");
//           document.documentElement.style.setProperty("--hover-background-l-delta", "5%");
//           document.documentElement.style.setProperty("--active-background-l-delta", "10%");
//           document.documentElement.style.setProperty("--hover-border-l-delta", "10%");
//           document.documentElement.style.setProperty("--active-border-l-delta", "20%");
//           document.documentElement.style.setProperty("--hover-color-l-delta", "5%");
//           document.documentElement.style.setProperty("--active-color-l-delta", "10%");
//         } else {
//           assignCssVar("--scheme-main", "#FFFFFF");
//           assignCssVar("--scheme-main-bis", "#F9FAFB");
//           assignCssVar("--scheme-main-ter", "#F3F4F6");
//           assignCssVar("--background", "#F3F4F6");
//           assignCssVar("--border-weak", "#EBECF0");
//           assignCssVar("--border", "#D6D9E0");
//           assignCssVar("--text-weak", "#69748C");
//           assignCssVar("--text", "#404654");
//           assignCssVar("--text-strong", "#2E333D");
//           assignCssVar("--text-title", "#1F2229");
//           document.documentElement.style.setProperty("--hover-background-l-delta", "5%");
//           document.documentElement.style.setProperty("--active-background-l-delta", "10%");
//           document.documentElement.style.setProperty("--hover-border-l-delta", "10%");
//           document.documentElement.style.setProperty("--active-border-l-delta", "20%");
//           document.documentElement.style.setProperty("--hover-color-l-delta", "5%");
//           document.documentElement.style.setProperty("--active-color-l-delta", "10%");
//         }
//         document.documentElement.style.setProperty("--hpf-banner", "url(" + theme.banner_url + ")");
//       }
//     }
//   }
// });
