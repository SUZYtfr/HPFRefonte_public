<template>
  <b-checkbox
    v-model="checkboxStatus"
    :indeterminate="indeterminate"
    :type="indeterminate ? 'is-danger' : ''"
    :class="[{ excluded: indeterminate }]"
    @click.native.prevent="checkBoxClicked($event)"
  >
    <font-awesome-icon v-if="characteristic.parent_id != null" icon="level-up-alt" rotation="90" class="mr-1 ml-2" />
    <span
      :class="[
        characteristic.parent_id != null
          ? 'is-italic has-text-weight-light'
          : 'has-text-weight-medium',
      ]"
    >{{ characteristic.name }}</span>
  </b-checkbox>
</template>

<script setup lang="ts">
import { CharacteristicData } from "@/types/characteristics";

interface CharThreeStateCheckboxProps {
  characteristic: CharacteristicData
  externalState: number
}
const { characteristic, externalState } = defineProps<CharThreeStateCheckboxProps>()

interface CharThreeStateCheckboxEmits {
  (e: "change", characteristic_id: number, state: number): void
}
const $emit = defineEmits<CharThreeStateCheckboxEmits>()

const checkboxStatus = computed(() => externalState === 1).value
const indeterminate = computed(() => externalState === -1 ).value

function checkBoxClicked(event: any): void {
  let internalState;
  if (indeterminate) {
    internalState = 0;
  } else if (checkboxStatus) {
    internalState = -1;
  } else {
    internalState = 1;
  }
  $emit("change", characteristic.id, internalState);
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
