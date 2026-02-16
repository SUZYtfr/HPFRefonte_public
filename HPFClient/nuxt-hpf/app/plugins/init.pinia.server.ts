export default defineNuxtPlugin(async () => {
  await useAsyncData("getCharacteristics", () => useConfigStore().fetchCharacteristics());
  await useAsyncData("getCharacteristicTypes", () => useConfigStore().fetchCharacteristicTypes());
  await useAsyncData("getThemes", () => useConfigStore().fetchThemes());
  await useAsyncData("getFandoms", () => useConfigStore().fetchFandoms());
});
