// import { Nitro } from "nitropack";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Désactivé temporairement (?) - Voir composables/useCustomAuth.ts
  /*
  auth: {
    baseURL: "https://hpfrefonte.pythonanywhere.com/graphql/",
    isEnabled: true,
    disableServerSideAuth: false,
    provider: {
      type: "local",
      endpoints: {
        signIn: { path: "account/token/", method: "post" },
        signOut: false,
        // signUp: { path: "register", method: "post" },
        signUp: false,
        getSession: { path: "account/", method: "get" },
      },
      pages: {
        login: "/",
      },
      token: {
        signInResponseTokenPointer: "/access",
        type: "JWT",
        cookieName: "auth.token",
        headerName: "Authorization",
        maxAgeInSeconds: 60 * 30,
        sameSiteAttribute: "strict",
        secureCookieAttribute: false,
        httpOnlyCookieAttribute: false,
        //cookieDomain: "hpfanfiction.fr",
      },
      refresh: {
        isEnabled: false,
        endpoint: {
          path: "account/token/refresh/",
          method: "post",
        },
        refreshOnlyToken: false,
        token: {
          refreshResponseTokenPointer: "account/token/refresh/",
          refreshRequestTokenPointer: "/refresh",
          signInResponseRefreshTokenPointer: "/refresh",
          cookieName: "auth.refresh",
          maxAgeInSeconds: 60 * 60 * 24 * 30, // 30 jours
          sameSiteAttribute: "strict",
          secureCookieAttribute: false,
          httpOnlyCookieAttribute: false,
          //cookieDomain: "hpfanfiction.fr",
        },
      },
      session: {
        dataType: {
          id: "number",
          username: "string",
          email: "string",
          profile: {
            realname: "string | null",
            birthdate: "date | null",
            gender: "number",
            bio: "string | null",
            bioImages: "[]",
            externalProfiles: "[]",
            profilePicture: "string | null",
            ageConsent: "boolean",
          },
          preferences: {
            font: "string",
            fontSize: "number",
            lineSpacing: "number",
            colorScheme: "number",
            colorSchemeInReader: "boolean",
            theme: "number",
            themeOverridenAt: "date | null",
            showAnimations: "boolean",
            showProfilePictures: "boolean",
            memberReviewPolicy: "number",
            anonymousReviewPolicy: "number",
            letterSpacing: "number",
            paragraphSpacing: "number",
            redirectToSummary: "boolean",
            showTriggerWarnings: "boolean",
            showReviewEditor: "boolean",
            emailForReview: "boolean",
            emailForReply: "boolean",
            emailForNews: "boolean",
            emailForFavoriteActivity: "boolean",
            emailForFavorite: "boolean",
            emailForChapterStatus: "boolean",
            resultOrder: "number",
            displayContent: "number",
          },
        },
      },
    },
    sessionRefresh: {
      enablePeriodically: false,
      enableOnWindowFocus: true,
    },
    // Toutes les pages sont protégées par défaut on spécifie les pages publiques via definePageMeta
    globalAppMiddleware: true,
  },
  */

  compatibilityDate: "2024-11-01",

  build: {
    transpile: [
      "@fortawesome/vue-fontawesome", // https://stackoverflow.com/a/75735153/13038487
    ],
  },

  css: ["@fortawesome/fontawesome-svg-core/styles.css", "~/assets/scss/custom.scss"],

  debug: false,

  devtools: {
    enabled: true,
    //vueDevTools: true,
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

  modules: [
    '@nuxt/eslint',
    '@pinia/nuxt',
    // '@sidebase/nuxt-auth',
    'nuxt-graphql-client',
  ],
  'graphql-client': {
    codegen: {
      onlyOperationTypes: false,
    },
    // codegen: false,  // désactive codegen si le serveur n'est pas dispo pour le schéma
    clients: {
      default: {
        host: 'http://127.0.0.1:8000/graphql/',
        token: {
          type: 'JWT'
        },
      },
    }
  },

  runtimeConfig: {
    // The private keys which are only available within server-side
    baseApi: "http://127.0.0.1:8000/graphql/",
    // Keys within public, will be also exposed to the client-side
    public: {
      baseApi: "http://127.0.0.1:8000/graphql/",
    },
  },

  ssr: true,

  typescript: {
    typeCheck: true,
  },
});
