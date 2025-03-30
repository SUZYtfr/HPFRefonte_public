export default defineNuxtPlugin(async () => {
  await useAsyncData("characteristics", () => Config().fetchCharacteristics());
  await useAsyncData("characteristicTypes", () => Config().fetchCharacteristics());
});
