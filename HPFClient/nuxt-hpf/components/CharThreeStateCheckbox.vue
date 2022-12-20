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
      >{{ characteristic.name }}</span
    >
  </b-checkbox>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { ICharacteristic } from "@/types/characteristics";

@Component({
  name: "CharThreeStateCheckbox",
})
export default class extends Vue {
  //#region Props
  @Prop() private characteristic!: ICharacteristic | undefined;
  @Prop() private externalState!: number | undefined;
  //#endregion

  //#region Computed
  get checkboxStatus() {
    return this.externalState == 1;
  }
  get indeterminate() {
    return this.externalState == -1;
  }
  //#endregion

  //#region Methods
  private checkBoxClicked(event: any) {
    let internalState;
    if (this.indeterminate) {
      internalState = 0;
    } else if (this.checkboxStatus) {
      internalState = -1;
    } else {
      internalState = 1;
    }
    this.$emit("change", this.characteristic?.id, internalState);
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
.excluded {
  color: red;
}
</style>