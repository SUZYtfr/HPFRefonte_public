<template>
  <b-checkbox
    v-model="checkboxStatus"
    :indeterminate="externalState === false"
    :type="externalState === false ? 'is-danger' : ''"
    :class="[{ excluded: externalState === false }]"
    @click.native.prevent="checkBoxClicked"
  >
    <span>{{ title }}</span>
  </b-checkbox>
</template>

<script setup lang="ts">

interface Props {
  externalState?: boolean | null;
  title: string;
} 

const { externalState = null } = defineProps<Props>();

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