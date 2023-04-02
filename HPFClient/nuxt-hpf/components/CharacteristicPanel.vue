<template>
  <div class="container-div">
    <div
      :class="[
        getCaracteristicTypeColor(characteristic_type.characteristic_type_id),
        { 'header-expanded': expanded },
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
        'header',
      ]"
      @click="expanded = !expanded"
    >
      <span class="is-6 is-clickable py-1 pl-1 is-flex-grow-5">{{
        characteristic_type.name
      }}</span>
      <span
        v-if="totalIds > 0"
        class="is-size-6"
      ><strong> {{ "(" + totalIds + ")" }} </strong></span>
      <b-icon class="is-clickable" :icon="expanded ? 'caret-up' : 'caret-down'" />
    </div>
    <div v-if="expanded">
      <simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
        <div class="is-flex is-flex-direction-column">
          <CharThreeStateCheckbox
            v-for="(charac, index) in characteristics"
            :key="index"
            class="py-1 pl-1"
            :characteristic="charac"
            :external-state="stateForCheckbox(charac.characteristic_id)"
            @change="threeStateChanged"
          />
        </div>
      </simplebar>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import simplebar from "simplebar-vue";
// import { CharacteristicData, CharacteristicTypeData } from "@/types/characteristics";
import { getCaracteristicTypeColor } from "@/utils/characteristics";
import CharThreeStateCheckbox from "~/components/CharThreeStateCheckbox.vue";
import "simplebar/dist/simplebar.min.css";
import "simplebar/dist/simplebar.min.js";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
// import SimpleBar from "simplebar";

@Component({
  name: "CharacteristicPanel",
  components: {
    CharThreeStateCheckbox,
    simplebar
  }
})
export default class extends Vue {
  // #region Props
  @Prop() public characteristic_type!: CharacteristicTypeModel;
  @Prop() public characteristics!: CharacteristicModel[];
  // #endregion

  mounted(): void {
    // console.log(this.characteristic_type);
    // console.log(this.characteristic_type instanceof CharacteristicTypeModel);
    // console.log(this.characteristics);
    // console.log(this.characteristics[0] instanceof CharacteristicModel);
  }

  // #region Datas
  private includedIds: number[] = [];
  private excludedIds: number[] = [];
  public expanded: boolean = false;
  // #endregion

  // #region Computed
  get totalIds(): number {
    return this.includedIds.length + this.excludedIds.length;
  }
  // #endregion

  // #region Methods
  public getCaracteristicTypeColor(characteristic_type_id: number): string {
    return getCaracteristicTypeColor(characteristic_type_id);
  }

  public threeStateChanged(caracteristic_id: number, state: number): void {
    this.includedIds = this.includedIds.filter(
      item => item !== caracteristic_id
    );
    this.excludedIds = this.excludedIds.filter(
      item => item !== caracteristic_id
    );

    if (state === -1) this.excludedIds.push(caracteristic_id);
    else if (state === 1) this.includedIds.push(caracteristic_id);
    this.$emit("change", new Set(this.characteristics.map(t => t.id)), this.includedIds, this.excludedIds);
  }

  public stateForCheckbox(caracteristic_id: number): number {
    let state = 0;
    if (this.includedIds.includes(caracteristic_id)) state = 1;
    else if (this.excludedIds.includes(caracteristic_id)) state = -1;
    return state;
  }
  // #region
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
.container-div {
  border: 1px solid $primary;
  border-radius: 5px;
  max-height: 200px;
}

.header {
  border: 1px solid rgba(0, 0, 0, 0);
  border-radius: 0.27rem;
}

.header-expanded {
  border-bottom: 1px solid $primary;
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
