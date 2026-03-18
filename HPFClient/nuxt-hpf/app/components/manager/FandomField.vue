<template>
  <BField :label :expanded>
    <BTaginput
      v-model="selectedFandoms"
      field="name"
      ellipsis
      :allow-new="false"
      autocomplete
      :required="!selectedFandoms.length"
      keep-first
      keep-open
      open-on-focus
      placeholder="Ajouter au moins un fandom"
      :data="filteredFandoms"
      @typing="getFilteredFandoms"
      @update:model-value="
        (value: FandomData[]) => {
          fandomField = value;
        }
      "
    />
  </BField>
</template>

<script setup lang="ts">
import { BField, BTaginput } from "buefy";
import type { FandomData } from "~/types/fanfictions";

interface Props {
  label?: string;
  expanded?: boolean;
}

const fandomField = defineModel<FandomData[]>("fandomField", { required: true });
defineProps<Props>();

const { fandoms } = useConfigStore();

// les fandoms et caractéristiques de la fiction sont "remplacés"
// par les fandoms stockés, pour garder une identité des objets
// BTagInput utilise l'identité des objets (===) et pas la similitude (==)
// pour comparer les tags entrés, ce qui potentiellement permet de choisir
// deux fois le même tag (un préselectionné, un sélectionné)
// TODO - effectuer ce "remplacement" en amont dans FictionModel?

const selectedFandoms = ref<FandomData[]>(
  fandoms!.filter((f) => fandomField.value.map((ff) => ff.id.toString()).includes(f.id.toString())),
);
const filteredFandoms = ref<FandomData[]>(fandoms!);
function getFilteredFandoms(text: number | string | undefined): string[] | undefined {
  if (text == null) {
    return;
  }
  filteredFandoms.value = fandoms!.filter((option) => {
    return option.name.toString().toLowerCase().indexOf(text.toString().toLowerCase()) >= 0;
  });
}
</script>
