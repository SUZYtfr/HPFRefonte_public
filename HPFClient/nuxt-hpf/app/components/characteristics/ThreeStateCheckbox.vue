<template>
  <BCheckbox
    v-model="checkboxStatus"
    :indeterminate="externalState === false"
    :type="externalState === false ? 'is-danger' : ''"
    :class="[{ excluded: externalState === false }]"
    @click.prevent="checkBoxClicked"
  >
    <FontAwesomeIcon v-if="characteristic?.parentId != null" icon="level-up-alt" rotation="90" class="mr-1 ml-2" />
    <span :class="[characteristic?.parentId != null ? 'is-italic has-text-weight-light' : 'has-text-weight-medium']">{{
      characteristic?.name
    }}</span>
  </BCheckbox>
</template>

<script setup lang="ts">
import type { CharacteristicData } from "@/types/characteristics";

interface Props {
  externalState?: boolean | null;
  characteristic?: CharacteristicData | undefined;
}

const { characteristic, externalState = null } = defineProps<Props>();

const checkboxStatus = computed<boolean>(() => {
  return externalState === true;
});

const $emit = defineEmits(["change"]);

// alterne au clic : true (inclus) => false (exclu) => null (vide)
// Note : "indeterminate" = false (exclu)
function checkBoxClicked(): void {
  if (externalState === true) {
    $emit("change", false);
  } else if (externalState === false) {
    $emit("change", null);
  } else {
    $emit("change", true);
  }
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
