<template>
  <BCheckbox
    v-model="checkboxStatus"
    :indeterminate="externalState === false"
    :type="externalState === false ? 'is-danger' : ''"
    :class="[{ excluded: externalState === false }]"
    @click.prevent="checkBoxClicked"
  >
    <span>{{ title }}</span>
  </BCheckbox>
</template>

<script setup lang="ts">
interface Props {
  externalState?: boolean | null;
  title: string;
}

interface Emits {
  (e: "change", internalState: boolean | null): void;
}

const { externalState = null } = defineProps<Props>();

const checkboxStatus = computed<boolean>(() => {
  return externalState === true;
});

const emit = defineEmits<Emits>();

// alterne au clic : true (inclus) => false (exclu) => null (vide)
// Note : "indeterminate" = false (exclu)
function checkBoxClicked(): void {
  if (externalState === true) {
    emit("change", false);
  } else if (externalState === false) {
    emit("change", null);
  } else {
    emit("change", true);
  }
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
