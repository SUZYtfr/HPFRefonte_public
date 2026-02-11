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
        v-if="totalIds > 0"
        class="is-size-6"
      ><strong> {{ "(" + totalIds + ")" }} </strong></span>
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
            @change="threeStateChanged"
          />
        </div>
      </simplebar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getCaracteristicTypeColor } from "@/utils/characteristics";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";

interface Props {
  characteristicType: CharacteristicTypeModel;
  characteristics: CharacteristicModel[];
  initialIncludedIds: number[];
  initialExcludedIds: number[];
}

const { characteristicType, characteristics, initialIncludedIds, initialExcludedIds } = defineProps<Props>();

const includedIds = ref<number[]>(initialIncludedIds.filter(iii => characteristics.map(c => Number(c.characteristicId)).includes(iii)));
const excludedIds = ref<number[]>(initialExcludedIds.filter(iii => characteristics.map(c => Number(c.characteristicId)).includes(iii)));
const expanded = ref<boolean>(false);

const totalIds = computed<number>(() => {
  return includedIds.value.length + excludedIds.value.length;
})

const $emit = defineEmits(["change"])

function threeStateChanged(characteristicId: number, state: number): void {
  includedIds.value = includedIds.value.filter(
    item => item !== Number(characteristicId)
  );
  excludedIds.value = excludedIds.value.filter(
    item => item !== Number(characteristicId)
  );

  if (state === -1) excludedIds.value.push(Number(characteristicId));
  else if (state === 1) includedIds.value.push(Number(characteristicId));
  $emit("change", characteristicId, state === -1 ? 'exclude' : state === 1 ? 'include' : null);
}

function stateForCheckbox(caracteristic_id: number): number {
  let state = 0;
  if (includedIds.value.includes(Number(caracteristic_id))) state = 1;
  else if (excludedIds.value.includes(Number(caracteristic_id))) state = -1;
  return state;
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