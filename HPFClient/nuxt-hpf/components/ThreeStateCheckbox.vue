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

const {
  checkedValue,
  excludedValue,
  uncheckedValue,
  externalValue,
  title,
} = withDefaults(defineProps<threeStateCheckboxProps>(), {
  checkedValue: true,
  excludedValue: false,
  uncheckedValue: null
})

interface threeStateCheckboxEmits {
  (e: 'change', internalState: boolean | null): void
}

const emit = defineEmits<threeStateCheckboxEmits>()

const checkboxStatus: boolean = computed(() => externalValue === checkedValue).value
const indeterminate: boolean = computed(() => externalValue === excludedValue).value

const checkBoxClicked = (event: any) => {
  let internalState;
  if (indeterminate) {
    internalState = uncheckedValue;
  } else if (checkboxStatus) {
    internalState = excludedValue;
  } else {
    internalState = checkedValue;
  }
  emit("change", internalState)
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>
