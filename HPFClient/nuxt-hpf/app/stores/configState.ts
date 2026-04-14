import { CharacteristicModel, CharacteristicTypeModel, ThemeModel } from "~/models";
import type { FandomData } from "~/types/fanfictions";
import { InvalidationReasonData } from "~/types/config";
import { plainToInstance } from "class-transformer";
import type { CharacteristicType, CharacteristicTypeType, ThemeType, TriggerWarningType } from "#gql";
import { TriggerWarningData } from "~/types/characteristics";

export const useConfigStore = defineStore("config", () => {
  //#region State
  const characteristics = ref<CharacteristicModel[]>([]);
  const characteristicTypes = ref<CharacteristicTypeModel[]>([]);
  const triggerWarnings = ref<TriggerWarningData[]>([]);
  const themes = ref<ThemeModel[]>([]);
  const fandoms = ref<FandomData[]>([]);
  // TODO appel à l'api, pour l'instant en dur.
  const invalidationReasons = ref<InvalidationReasonData[]>([
    new InvalidationReasonData({ id: "1", reason: "Taille trop courte" }),
    new InvalidationReasonData({ id: "2", reason: "Orthographe" }),
    new InvalidationReasonData({ id: "3", reason: "Grammaire" }),
    new InvalidationReasonData({ id: "4", reason: "Conjugaison" }),
    new InvalidationReasonData({ id: "5", reason: "Non-respect du réglement" }),
    new InvalidationReasonData({ id: "6", reason: "Mise en forme" }),
    new InvalidationReasonData({ id: "7", reason: "Autre" }),
  ]);
  //#endregion

  // Bizarrement il faut séparer ces deux appels dans leur méthodes respectives
  // Sinon on a une erreur:
  // [nuxt] A composable that requires access to the Nuxt instance was called outside
  // of a plugin, Nuxt hook, Nuxt middleware, or Vue setup function. This is probably
  // not a Nuxt bug.
  // (Mais je pense que c'est un Nuxt bug)
  // Il faut aussi rendre une valeur quelconque pour éviter que useAsyncData se plaigne.
  async function fetchCharacteristics(): Promise<true> {
    const { data } = await useAsyncGql(
      "getCharacteristics",
      {},
      {
        transform: (input: { characteristics: CharacteristicType[] }) => {
          return plainToInstance(CharacteristicModel, input.characteristics);
        },
      },
    );
    characteristics.value = data.value;
    return true;
  }

  async function fetchCharacteristicTypes(): Promise<true> {
    const { data } = await useAsyncGql(
      "getCharacteristicTypes",
      {},
      {
        transform: (input: { characteristicTypes: CharacteristicTypeType[] }) => {
          return plainToInstance(CharacteristicTypeModel, input.characteristicTypes);
        },
      },
    );
    characteristicTypes.value = data.value;
    return true;
  }

  async function fetchTriggerWarnings(): Promise<true> {
    const { data } = await useAsyncGql(
      "getTriggerWarnings",
      {},
      {
        transform: (input: { triggerWarnings: TriggerWarningType[] }) => {
          return plainToInstance(TriggerWarningData, input.triggerWarnings);
        },
      },
    );
    triggerWarnings.value = data.value;
    return true;
  }

  async function fetchThemes(): Promise<true> {
    const { data } = await useAsyncGql(
      "getThemes",
      {},
      {
        transform: (input: { themes: ThemeType[] }) => {
          return plainToInstance(ThemeModel, input.themes);
        },
      },
    );
    themes.value = data.value;
    return true;
  }

  async function fetchFandoms(): Promise<true> {
    const { data } = await useAsyncGql(
      "getFandoms",
      {},
      {
        transform: (input: { fandoms: FandomData[] }) => {
          return input.fandoms;
        },
      },
    );
    fandoms.value = data.value;
    return true;
  }

  return {
    characteristics,
    characteristicTypes,
    triggerWarnings,
    themes,
    fandoms,
    invalidationReasons,
    fetchCharacteristicTypes,
    fetchCharacteristics,
    fetchTriggerWarnings,
    fetchThemes,
    fetchFandoms,
  };
});
