import type { NuxtConfig } from '@nuxt/types'

const config: NuxtConfig = {
  build: {
    parallel: true,
    cache: true,
    extractCSS: process.env.NODE_ENV === 'production',
    optimizeCSS: process.env.NODE_ENV === 'production',
  },
  buildModules: [
    '@nuxt/typescript-build',
  ],
  components: false,
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css',
    '~/assets/scss/custom.scss',
    '@/node_modules/animate.css/animate.css',
  ],
  env: {},
  head: {
    title: 'nuxt-community/typescript-template',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'A boilerplate to start a Nuxt+TS project quickly' }
    ],
    link: []
  },
  loading: { color: '#0c64c1' },
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    ['nuxt-buefy', {
      css: false,
      materialDesignIcons: false,
      defaultIconPack: 'fas',
      defaultIconComponent: 'font-awesome-icon'
    }],
    ['nuxt-facebook-pixel-module', {
      /* module options */
      track: 'PageView',
      pixelId: 'FACEBOOK_PIXEL_ID',
      autoPageView: true,
      disabled: false
    }],
    'nuxt-ssr-class-serialiser',
  ],
  plugins: [
    '~/plugins/truncate',
    '~/plugins/axios',
    '~/plugins/fontawesome',
  ],
  axios: {
    baseURL: process.env.VUE_APP_BASE_API, // Used as fallback if no runtime config is provided,
    credentials: true
  },
  auth: {
    strategies: {
      local: undefined,
      cookie: {
        scheme: 'refresh',
        token: {
          property: 'access',
          maxAge: 30,
          global: true,
          type: 'Bearer'
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24 * 30
        },
        endpoints: {
          login: { url: '/account/token/', method: 'post' },
          refresh: { url: '/account/refresh/', method: 'post' },
          logout: false,
          user: { url: '/account/', method: 'get' }
        },
        user: {
          property: false,
        },
        options: {
//           à activer en production
//           secure: true
        }
      }
    },
    redirect: {
      login: undefined,
      logout: undefined,
      callback: undefined,
      home: undefined
    },
  }
}

export default config
