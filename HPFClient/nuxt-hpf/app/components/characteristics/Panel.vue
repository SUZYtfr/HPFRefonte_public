<template>
  <div class="container-div">
    <div
      :class="[
        getCaracteristicTypeColor(characteristicType.characteristicTypeId),
        { 'header-expanded': expanded },
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
        'header',
      ]"
      @click="expanded = !expanded"
    >
      <span class="is-6 is-clickable py-1 pl-1 is-flex-grow-5">{{
        characteristicType.name
      }}</span>
      <span
        v-if="totalChecked > 0"
        class="is-size-6"
      ><strong> {{ "(" + totalChecked + ")" }} </strong></span>
      <b-icon class="is-clickable" :icon="expanded ? 'caret-up' : 'caret-down'" />
    </div>
    <div v-if="expanded">
      <simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
        <div class="is-flex is-flex-direction-column">
          <CharacteristicsThreeStateCheckbox
            v-for="(charac, index) in characteristics"
            :key="index"
            class="py-1 pl-1"
            :characteristic="charac"
            :external-state="stateForCheckbox(charac.characteristicId)"
            @change="(internalState: boolean | null) => threeStateChanged(charac.characteristicId, internalState)"
          />
        </div>
      </simplebar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getCaracteristicTypeColor } from "@/utils/characteristics";
import type { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";

interface Props {
  characteristicType: CharacteristicTypeModel;
  characteristics: CharacteristicModel[];
  initialIncludedIds: number[];
  initialExcludedIds: number[];
}

const { characteristicType, characteristics, initialIncludedIds, initialExcludedIds } = defineProps<Props>();

const includedValues = ref<number[]>(initialIncludedIds.filter(iii => characteristics.map(c => c.characteristicId).includes(iii)));
const excludedValues = ref<number[]>(initialExcludedIds.filter(iii => characteristics.map(c => c.characteristicId).includes(iii)));
const expanded = ref<boolean>(false);

const totalChecked = computed<number>(() => {
  return includedValues.value.length + excludedValues.value.length;
});

const $emit = defineEmits(["change"]);

function threeStateChanged(characteristicId: number, state: boolean | null): void {
  includedValues.value = includedValues.value.filter(
    iv => iv !== characteristicId
  );
  excludedValues.value = excludedValues.value.filter(
    iv => iv !== characteristicId
  );

  if (state === true) includedValues.value.push(characteristicId);
  else if (state === false) excludedValues.value.push(characteristicId);
  $emit("change", characteristicId, state);
}

function stateForCheckbox(value: number): boolean | null {
  if (includedValues.value.includes(value)) return true;
  else if (excludedValues.value.includes(value)) return false;
  else return null;
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
.container-div {
  border: 1px solid var(--primary);
  border-radius: 5px;
  max-height: 200px;
}

.header {
  border: 1px solid rgba(0, 0, 0, 0);
  border-radius: 0.27rem;
}

.header-expanded {
  border-bottom: 1px solid var(--primary);
  border-top-left-radius: 0.27rem;
  border-top-right-radius: 0.27rem;
  border-bottom-right-radius: 0px;
  border-bottom-left-radius: 0px;
}

.custom-scrollbar-bio {
  height: auto;
  max-height: 160px;
}
</style>