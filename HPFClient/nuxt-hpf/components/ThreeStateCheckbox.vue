<template>
  <b-checkbox
    v-model="checkboxStatus"
    :indeterminate="indeterminate"
    :type="indeterminate ? 'is-danger' : ''"
    :class="[{ excluded: indeterminate }]"
    @click.native.prevent="checkBoxClicked($event)"
  >
    <span>{{ title }}</span>
  </b-checkbox>
</template>

<script setup lang="ts">

interface Props {
  externalValue?: any;
  title?: string;
  checkedValue?: any;
  excludedValue?: any;
  uncheckedValue?: any;
} 

const { 
  externalValue,
  title,
  checkedValue = true,
  excludedValue = false,
  uncheckedValue = null
} = defineProps<Props>();

const checkboxStatus = computed<boolean>(() => {
    return externalValue === checkedValue;
});

const indeterminate = computed<boolean>(() => {
    return externalValue === excludedValue;
});

const $emit = defineEmits(["change"]);

function checkBoxClicked(event: any): void {
  let internalState: number;
  if (indeterminate.value) {
    internalState = uncheckedValue;
  } else if (checkboxStatus.value) {
    internalState = excludedValue;
  } else {
    internalState = checkedValue;
  }
  $emit("change", internalState);
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
