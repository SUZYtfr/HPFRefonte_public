import type { NuxtConfig } from "@nuxt/types";
import { instanceToPlain } from "class-transformer";

const config: NuxtConfig = {
  build: {
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
      if (ctx.isDev) {
        config2.devtool = ctx.isClient ? "source-map" : "inline-source-map";
      }
    }
  },
  buildModules: [
    "@nuxt/typescript-build"
  ],
  components: false,
  css: [
    "@fortawesome/fontawesome-svg-core/styles.css",
    "~/assets/scss/custom.scss",
    "@/node_modules/animate.css/animate.css"
  ],
  env: {},
  head: {
    title: "Harry Potter Fanfiction: Harry Potter selon ses fans",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "Harry Potter Fanfiction: Harry Potter selon ses fans" }
    ],
    link: []
  },
  loading: { color: "#0c64c1" },
  modules: [
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
    ["nuxt-buefy", {
      css: false,
      materialDesignIcons: false,
      defaultIconPack: "fas",
      defaultIconComponent: "font-awesome-icon"
    }],
    ["nuxt-facebook-pixel-module", {
      /* module options */
      track: "PageView",
      pixelId: "FACEBOOK_PIXEL_ID",
      autoPageView: true,
      disabled: false
    }]
    // "nuxt-ssr-class-serialiser"
  ],
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
        },
        redirect: false,
        resetOnError: true
      }
    }
  },
  plugins: [
    "~/plugins/truncate",
    "~/plugins/axios",
    "~/plugins/fontawesome",
    "~/plugins/classes"
  ],
  axios: {
    baseURL: process.env.VUE_APP_BASE_API, // Used as fallback if no runtime config is provided,
    credentials: (process.env.NODE_ENV === "production")
  },
  ssr: true,
  target: "server",
  hooks: {
    render: {
      routeContext(context) {
        // console.log("Data: ");
        // console.log(context.data);
        // console.log("Fetch: ");
        // console.log(context.fetch);
        const { fetch } = context || {};
        // const { fetch } = context.nuxtState || {};
        if (fetch) {
          Object.keys(fetch).forEach((fetchkey) => {
            // console.log("FetchKey: ");
            // console.log(fetchkey);

            Object.keys(fetch[fetchkey]).forEach((key) => {
              const asyncFetch = fetch[fetchkey];
              // console.log("AsyncFetch: ");
              // console.log(key);
              // console.log("Instance:");
              // console.log(asyncFetch[key]);
              asyncFetch[key] = instanceToPlain(asyncFetch[key]);
              // console.log("Plain:");
              // console.log(asyncFetch[key]);
            });
          });
        }

        //   const asyncFetch = fetch[Object.keys(fetch)[0]];
        //   // const asyncFetch = fetch[0];
        //   // console.log("AsyncFetch: ");
        //   // console.log(asyncFetch);
        //   Object.keys(asyncFetch).forEach((key) => {
        //     // Converts the class instance to POJO
        //     console.log("Route Render AsyncFetch: ");
        //     console.log(key);
        //     console.log(asyncFetch[key]);
        //     asyncFetch[key] = instanceToPlain(asyncFetch[key]);
        //     console.log("Plain: ");
        //     console.log(asyncFetch[key]);
        //   });
        // }

        // const { fetch } = this.$nuxt.context.nuxtState || {};
        // console.log(context);
        // console.log(context.data);
        // console.log(context.fetch);
        // if (Array.isArray(context?.nuxt?.data)) {
        //   console.log(context.nuxt.data);
        //   // This object contain the data fetched in asyncData
        //   const asyncData = context.nuxt.data[0] || {};
        //   // For every asyncData, we serialise it
        //   Object.keys(asyncData).forEach((key) => {
        //     // Converts the class instance to POJO
        //     asyncData[key] = instanceToPlain(asyncData[key]);
        //   });
        // }
      }
    }
  }
};

export default config;
