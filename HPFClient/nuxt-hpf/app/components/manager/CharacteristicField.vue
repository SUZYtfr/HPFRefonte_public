<template>
  <BField :label :expanded>
    <BSelect v-if="selectAddon" v-model="selectedCharacteristicType">
      <option
        v-for="characteristicType in characteristicTypeSet"
        :key="characteristicType.characteristicTypeId"
        :value="characteristicType"
      >
        {{ characteristicType.name }}
      </option>
    </BSelect>
    <BTaginput
      v-model="selectedCharacteristics"
      field="name"
      expanded
      ellipsis
      :allow-new="false"
      autocomplete
      :required
      keep-first
      keep-open
      open-on-focus
      :placeholder="
        'Ajouter des ' +
        selectedCharacteristicType.name.toLowerCase() +
        's parmi ' +
        characteristics
          ?.filter(
            (c) => c.characteristicTypeId.toString() === selectedCharacteristicType.characteristicTypeId.toString(),
          )!
          .length.toString() +
        ' choix'
      "
      :data="filteredCharacteristics"
      @typing="getFilteredCharacteristics"
      @add="addCharacteristic"
      @remove="removeCharacteristic"
    />
  </BField>
</template>

<script setup lang="ts">
import { BField, BSelect, BTaginput } from "buefy";
import type { CharacteristicModel, CharacteristicTypeModel } from "~/models";

interface Props {
  label?: string;
  expanded?: boolean;
  selectAddon?: boolean;
  required?: boolean;
  characteristicTypeIds?: string[];
}

const characteristicField = defineModel<CharacteristicModel[]>("characteristicField", { required: true });
const { characteristicTypeIds } = defineProps<Props>();

function addCharacteristic(characteristic: CharacteristicModel): void {
  characteristicField.value = characteristicField.value.concat(characteristic);
}
function removeCharacteristic(characteristic: CharacteristicModel): void {
  characteristicField.value = characteristicField.value.slice(characteristicField.value.indexOf(characteristic));
}

const { characteristics, characteristicTypes } = useConfigStore();

const characteristicTypeSet = characteristicTypeIds
  ? characteristicTypes.filter((ct) => characteristicTypeIds.includes(ct.characteristicTypeId.toString()))
  : characteristicTypes;

// les fandoms et caractéristiques de la fiction sont "remplacés"
// par les fandoms stockés, pour garder une identité des objets
// BTagInput utilise l'identité des objets (===) et pas la similitude (==)
// pour comparer les tags entrés, ce qui potentiellement permet de choisir
// deux fois le même tag (un préselectionné, un sélectionné)
// TODO - effectuer ce "remplacement" en amont dans FictionModel?

const selectedCharacteristicType = ref<CharacteristicTypeModel>(characteristicTypeSet[0]!);
const selectedCharacteristics = ref<CharacteristicModel[]>(
  characteristics!.filter((ct) =>
    characteristicField
      .value!.filter((c) =>
        characteristicTypeSet
          .map((ct) => ct.characteristicTypeId.toString())
          .includes(c.characteristicTypeId.toString()),
      )
      .map((c) => c.characteristicId.toString())
      .includes(ct.characteristicId.toString()),
  ),
);
const filteredCharacteristics = ref<CharacteristicModel[]>(
  characteristics!.filter(
    (option) =>
      option.characteristicTypeId.toString() === selectedCharacteristicType.value.characteristicTypeId.toString(),
  ),
);
function getFilteredCharacteristics(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredCharacteristics.value = characteristics!
    .filter(
      (option) =>
        option.characteristicTypeId.toString() === selectedCharacteristicType.value.characteristicTypeId.toString(),
    )
    .filter((option) => {
      return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
    });
}
watch(selectedCharacteristicType, () => getFilteredCharacteristics(""));
</script>
