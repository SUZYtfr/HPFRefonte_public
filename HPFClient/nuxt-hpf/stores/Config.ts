import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import {
    searchCharacteristics,
    searchCharacteristicsTypes
} from "@/api/characteristics";

export const Config = defineStore("Config", () => {
    const characteristics = ref<CharacteristicModel[]>();
    const characteristicTypes = ref<CharacteristicTypeModel[]>();

    function setCharacteristics(chars: CharacteristicModel[]) { characteristics.value = chars }
    function setCharacteristicTypes(charTypes: CharacteristicTypeModel[]) { characteristicTypes.value = charTypes}

    // Bizarrement il faut séparer ces deux appels dans leur méthodes respectives
    // Sinon on a une erreur:
    // [nuxt] A composable that requires access to the Nuxt instance was called outside 
    // of a plugin, Nuxt hook, Nuxt middleware, or Vue setup function. This is probably 
    // not a Nuxt bug.
    // (Mais je pense que c'est un Nuxt bug)
    // Il faut aussi rendre une valeur quelconque pour éviter que useAsyncData se plaigne.
    async function fetchCharacteristics(): Promise<true> {
        const { data: characteristicTemp } = await searchCharacteristics(null);
        setCharacteristics(characteristicTemp.value);
        return true
    }

    async function fetchCharacteristicTypes(): Promise<true> {
        const { data: characteristicTypesTemp } = await searchCharacteristicsTypes();
        setCharacteristicTypes(characteristicTypesTemp.value);
        return true
    }

    return {
        characteristics,
        characteristicTypes,
        // setCharacteristics,
        // setCharacteristicTypes,
        fetchCharacteristicTypes,
        fetchCharacteristics
    }
});
