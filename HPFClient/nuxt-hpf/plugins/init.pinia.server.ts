// https://krutiepatel.com/blog/nuxt-server-init-where-is-it-in-nuxt-3/

export default defineNuxtPlugin(async (nuxtApp) => {
    await useAsyncData('characteristics', () => Config().fetchCharacteristics());
    await useAsyncData('characteristicTypes', () => Config().fetchCharacteristicTypes());
    await useAsyncData('themes', () => Config().fetchThemes());
})
