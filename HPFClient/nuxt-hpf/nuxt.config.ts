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
  }
}

export default config
