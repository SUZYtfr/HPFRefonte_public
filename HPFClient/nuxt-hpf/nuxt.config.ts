export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      // apiBase: process.env.VUE_APP_BASE_API
      apiBase: ""
    }
  },
  // devtools: { enabled: true },  // marche pas
  // experimental: {
  //   renderJsonPayloads: true  // active plugin/serialize.ts
  // },
  builder: "vite",
  // nitro: {
  //   // moduleSideEffects: ["reflect-metadata"],  // ça ne marche pas
  //   esbuild: {
  //     options: {
  //       target: "esnext",
  //       tsconfigRaw: {
  //         compilerOptions: {
  //           experimentalDecorators: true,
  //           // emitDecoratorMetadata: true,  // ça n'existe pas
  //         }
  //       }
  //     }
  //   }
  // },
  vite: {
    esbuild: {
      tsconfigRaw: {
        compilerOptions: {
          experimentalDecorators: true
        }
      }
    },
    // build: {
    //   target: "esnext",
    // },
    // optimizeDeps: {
    //   esbuildOptions: {
    //     target: "esnext",
    //   }
    // }
  },
  alias: {
    "~/*": "./*",
    "@/*": "./*"
  },
  app: {
    head: {
      title: "Harry Potter Fanfiction : Harry Potter selon ses fans",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "description", content: "Harry Potter Fanfiction : Harry Potter selon ses fans" }
      ],
    },
  },
  css: [
    "@fortawesome/fontawesome-svg-core/styles.css",
    "~/assets/scss/custom.scss",
    "@/node_modules/animate.css/animate.css"
  ],
  modules: [
    "nuxt3-vuex-module"
  ],
  ssr: true
  /*
  auth: {
    localStorage: false,
    strategies: {
      local: undefined,
      cookie: {
        scheme: "refresh",
        token: {
          property: "access",
          global: true,
          required: true,
          type: "Bearer",
          name: "Authorization",
          maxAge: 60 * 30 // 30 minutes
        },
        refreshToken: {
          property: "refresh",
          required: true,
          data: "refresh",
          maxAge: 60 * 60 * 24 * 30 // 30 jours
        },
        user: {
          property: false,
          autoFetch: true
        },
        endpoints: {
          login: { url: "/account/token/", method: "post" },
          refresh: { url: "/account/token/refresh/", method: "post" },
          logout: false,
          user: { url: "/account/", method: "get" }
        },
        options: {
          secure: (process.env.NODE_ENV === "production")
        }
      }
    },
    // @ts-ignore
    redirect: false,
    resetOnError: true
  },
  */
});

/*
export default defineNuxtConfig({
  build: {
    transpile: ["defu"],
    loaders: {
      vue: {
        compiler: require("vue-template-babel-compiler")
      }
    },
    parallel: true,
    cache: true,
    extractCSS: process.env.NODE_ENV === "production",
    optimizeCSS: process.env.NODE_ENV === "production",
    extend(config2, ctx) {
      if (ctx.isServer === false) {
        config2.node = {
          fs: "empty"
        };
      }
      if (ctx.isDev) {
        config2.devtool = ctx.isClient ? "source-map" : "inline-source-map";
      }
    }
  },
});
*/