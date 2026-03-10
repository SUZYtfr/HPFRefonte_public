export default defineNuxtPlugin(async () => {
  useConfigStore().fetchCharacteristics();
  useConfigStore().fetchCharacteristicTypes();
  useConfigStore().fetchTriggerWarnings();
  useConfigStore().fetchThemes();
  useConfigStore().fetchFandoms();
});
