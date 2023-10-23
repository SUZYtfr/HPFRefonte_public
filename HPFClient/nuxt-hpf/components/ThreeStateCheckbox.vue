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
interface threeStateCheckboxProps {
  externalValue?: any | undefined
  title: string | undefined
  checkedValue?: true
  excludedValue?: any
  uncheckedValue?: any
}

const props = withDefaults(defineProps<threeStateCheckboxProps>(), {
  checkedValue: true,
  excludedValue: false,
  uncheckedValue: null
})

interface threeStateCheckboxEmits {
  (e: 'change', internalState: boolean): void
}

const emit = defineEmits<threeStateCheckboxEmits>()

const checkboxStatus: boolean = props.externalValue === props.checkedValue
const indeterminate: boolean = props.externalValue === props.excludedValue
const checkBoxClicked = (event: any) => {
    let internalState;
    if (indeterminate) {
      internalState = props.uncheckedValue;
    } else if (checkboxStatus) {
      internalState = props.excludedValue;
    } else {
      internalState = props.checkedValue;
    }
    emit("change", internalState)
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
