<template>
  <div class="container-div">
    <div
      :class="[
        getCaracteristicTypeColor(characteristic_type.characteristic_type_id),
        { 'header-expanded': expanded },
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
        'header',
      ]"
      @click="expanded = !expanded"
    >
      <span class="is-6 is-clickable py-1 pl-1 is-flex-grow-5">{{
        characteristic_type.name
      }}</span>
      <span
        v-if="totalIds > 0"
        class="is-size-6"
      ><strong> {{ "(" + totalIds + ")" }} </strong></span>
      <b-icon class="is-clickable" :icon="expanded ? 'caret-up' : 'caret-down'" />
    </div>
    <div v-if="expanded">
      <!-- <simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false"> -->
        <div class="is-flex is-flex-direction-column">
          <CharThreeStateCheckbox
            v-for="(charac, index) in characteristics"
            :key="index"
            class="py-1 pl-1"
            :characteristic="charac"
            :external-state="stateForCheckbox(charac.characteristic_id)"
            @change="threeStateChanged"
          />
        </div>
      <!-- </simplebar> -->
    </div>
  </div>
</template>

<script setup lang="ts">
// import simplebar from "simplebar-vue";
// import { CharacteristicData, CharacteristicTypeData } from "@/types/characteristics";
import { getCaracteristicTypeColor as gCaracteristicTypeColor} from "@/utils/characteristics";
import CharThreeStateCheckbox from "~/components/CharThreeStateCheckbox.vue";
// import "simplebar/dist/simplebar.min.css";
// import "simplebar/dist/simplebar.min.js";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
// import SimpleBar from "simplebar";

interface CharacteristicPanelProps {
  characteristic_type: CharacteristicTypeModel
  characteristics: CharacteristicModel[]
}
const { characteristic_type, characteristics } = defineProps<CharacteristicPanelProps>()

interface CharacteristicPanelEmits {
  (e: "change", allIds: Set<number>, includedIds: number[], excludedIds: number[]): void
}
const $emit = defineEmits<CharacteristicPanelEmits>()

let includedIds: number[] = [];
let excludedIds: number[] = [];
let expanded = ref<boolean>(false);

const totalIds = computed<number>(() => {
  return includedIds.length + excludedIds.length;
})

function getCaracteristicTypeColor(characteristic_type_id: number): string {
  return gCaracteristicTypeColor(characteristic_type_id);
}

function threeStateChanged(characteristic_id: number, state: number): void {
  includedIds = includedIds.filter(
    item => item !== characteristic_id
  );
  excludedIds = excludedIds.filter(
    item => item !== characteristic_id
  );

  if (state === -1) excludedIds.push(characteristic_id);
  else if (state === 1) includedIds.push(characteristic_id);
  $emit("change", new Set(characteristics.map(t => t.id)), includedIds, excludedIds);
}

// FIXME - pas réactif ! n'est appelé que lorque le panel est ouvert
function stateForCheckbox(characteristic_id: number): number {
  let state = 0;
  if (includedIds.includes(characteristic_id)) state = 1;
  else if (excludedIds.includes(characteristic_id)) state = -1;
  return state;
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
.container-div {
  border: 1px solid $primary;
  border-radius: 5px;
  max-height: 200px;
}

.header {
  border: 1px solid rgba(0, 0, 0, 0);
  border-radius: 0.27rem;
}

.header-expanded {
  border-bottom: 1px solid $primary;
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
