<template>
  <div class="container-div">
    <div
      :class="[{ 'header-expanded': expanded }, 'is-flex', 'is-flex-direction-row', 'is-align-items-center', 'header']"
      @click="expanded = !expanded"
    >
      <span class="is-6 is-clickable py-1 pl-1 is-flex-grow-5">{{ name }}</span>
      <span v-if="totalChecked > 0" class="is-size-6"
        ><strong> {{ "(" + totalChecked + ")" }} </strong></span
      >
      <BIcon class="is-clickable" :icon="expanded ? 'caret-up' : 'caret-down'" />
    </div>
    <div v-if="expanded">
      <Simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
        <div class="is-flex is-flex-direction-column">
          <ThreeStateCheckbox
            v-for="(option, index) in options"
            :key="index"
            :title="option.name"
            class="py-1 pl-1"
            :external-state="stateForCheckbox(option.value)"
            @change="(internalState: boolean | null) => threeStateChanged(option.value, internalState)"
          />
        </div>
      </Simplebar>
    </div>
  </div>
</template>

<script setup lang="ts" generic="T extends { name: string; value: string }">
interface Props {
  name: string;
  options: T[];
  initialIncludedValues: string[];
  initialExcludedValues: string[];
}

interface Emits {
  (e: "change", value: string, state: boolean | null): void;
}

const { initialIncludedValues, initialExcludedValues } = defineProps<Props>();

const includedValues = ref<string[]>(initialIncludedValues);
const excludedValues = ref<string[]>(initialExcludedValues);
const expanded = ref<boolean>(false);

const totalChecked = computed<number>(() => {
  return includedValues.value.length + excludedValues.value.length;
});

const emit = defineEmits<Emits>();

function threeStateChanged(value: string, state: boolean | null): void {
  includedValues.value = includedValues.value.filter((iv) => iv !== value);
  excludedValues.value = excludedValues.value.filter((iv) => iv !== value);
  if (state === true) includedValues.value.push(value);
  else if (state === false) excludedValues.value.push(value);
  emit("change", value, state);
}

function stateForCheckbox(value: string): boolean | null {
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
