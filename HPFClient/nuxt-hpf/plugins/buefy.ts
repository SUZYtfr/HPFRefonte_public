import Buefy, { DialogProgrammatic, ToastProgrammatic } from "buefy";
//import "buefy/dist/buefy.css";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default defineNuxtPlugin((nuxtApp: any) => {
  const appWithBuefy = nuxtApp.vueApp.use(Buefy, {
    //css: false,
    //materialDesignIcons: false,
    defaultIconPack: "fas",
    defaultIconComponent: "font-awesome-icon",
    defaultDialogCancelText: "Annuler",
  });

  const dialog = new DialogProgrammatic(appWithBuefy);
  nuxtApp.provide("dialog", dialog);

  const toast = new ToastProgrammatic(appWithBuefy);
  nuxtApp.provide("toast", toast);
});
