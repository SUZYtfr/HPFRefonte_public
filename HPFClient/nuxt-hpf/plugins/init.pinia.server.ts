export default defineNuxtPlugin(async () => {
  await useAsyncData("characteristics", () => useConfigStore().fetchCharacteristics());
  await useAsyncData("characteristicTypes", () => useConfigStore().fetchCharacteristicTypes());
  await useAsyncData("themes", () => useConfigStore().fetchThemes());
});
