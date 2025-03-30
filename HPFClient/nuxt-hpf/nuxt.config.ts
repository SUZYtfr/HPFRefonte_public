// import { Nitro } from "nitropack";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",

  build: {
    transpile: [
      "@fortawesome/vue-fontawesome", // https://stackoverflow.com/a/75735153/13038487
    ],
  },

  css: ["@fortawesome/fontawesome-svg-core/styles.css", "@/assets/scss/custom.scss"],

  debug: true,

  devtools: {
    enabled: true,
    vueDevTools: true,
    timeline: {
      enabled: true,
    },
  },

  // Marche pas
  // hooks: {
  //   "nitro:build:before": (nitro: Nitro) => {
  //     nitro.options.moduleSideEffects.push("reflect-metadata");
  //   },
  // },

  // Marche à moitié
  // nitro: {
  //   hooks: {
  //     "rollup:before": (nitro: Nitro) => {
  //       nitro.options.moduleSideEffects.push("reflect-metadata");
  //     },
  //   },
  //   rollupConfig: {
  //     output: {
  //       banner: 'import "reflect-metadata";',
  //     },
  //   },
  // },

  modules: ["@nuxt/eslint", "@pinia/nuxt"],

  runtimeConfig: {
    // The private keys which are only available within server-side
    baseApi: "https://hpfrefonte.pythonanywhere.com/api/",
    // Keys within public, will be also exposed to the client-side
    public: {
      baseApi: "https://hpfrefonte.pythonanywhere.com/api/",
    },
  },

  ssr: true,

  typescript: {
    typeCheck: true,
  },
});
