import Buefy from "buefy";
import type { BuefyConfigOptions } from "buefy";
//import "buefy/dist/buefy.css";
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default defineNuxtPlugin((nuxtApp: any) => {
  const config: BuefyConfigOptions = {
    defaultIconPack: "fas",
    defaultIconComponent: "font-awesome-icon",
    defaultDialogCancelText: "Annuler",
  };
  nuxtApp.vueApp.use(Buefy, config);

  // Pas pratique finalement, les $dialog,$toast et $snackbar ne sont pas typés de cette façon
  // Utiliser le composable useBuefy
  // const dialog = new DialogProgrammatic(appWithBuefy);
  // nuxtApp.provide("dialog", dialog);

  // const toast = new ToastProgrammatic(appWithBuefy);
  // nuxtApp.provide("toast", toast);

  // const snackbar = new SnackbarProgrammatic(appWithBuefy);
  // nuxtApp.provide("snackbar", snackbar);
});
