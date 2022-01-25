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

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";

@Component({
  name: "ThreeStateCheckbox",
})
export default class extends Vue {
  //#region Props
  @Prop() private externalValue!: any | undefined;
  @Prop() private title: string | undefined;
  @Prop({ default: true }) private checkedValue: any;
  @Prop({ default: false }) private excludedValue: any;
  @Prop({ default: null }) private uncheckedValue: any;
  //#endregion

  //#region Computed
  get checkboxStatus() {
    return this.externalValue == this.checkedValue;
  }
  get indeterminate() {
    return this.externalValue == this.excludedValue;
  }
  //#endregion

  //#region Methods
  private checkBoxClicked(event: any) {
    let internalState;
    if (this.indeterminate) {
      internalState = this.uncheckedValue;
    } else if (this.checkboxStatus) {
      internalState = this.excludedValue;
    } else {
      internalState = this.checkedValue;
    }
    this.$emit("change", internalState);
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>