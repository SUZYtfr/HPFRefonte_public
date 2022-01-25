<template>
  <div class="container-div">
    <div
      @click="expanded = !expanded"
      :class="[
        getCaracteristicTypeColor(characteristic_type.characteristic_type_id),
        { 'header-expanded': expanded },
        'is-flex',
        'is-flex-direction-row',
        'is-align-items-center',
        'header',
      ]"
    >
      <span class="is-6 is-clickable py-1 pl-1 is-flex-grow-5">{{
        characteristic_type.name
      }}</span>
      <span v-if="totalIds > 0" class="is-size-6"
        ><b> {{ "(" + totalIds + ")" }} </b></span
      >
      <b-icon class="is-clickable" :icon="expanded ? 'caret-up' : 'caret-down'">
      </b-icon>
    </div>
    <div v-if="expanded">
      <simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
        <div class="is-flex is-flex-direction-column">
          <CharThreeStateCheckbox
            class="py-1 pl-1"
            v-for="(carac, index) in characteristics"
            :key="index"
            :caracteristic="carac"
            :externalState="stateForCheckbox(carac.characteristic_id)"
            @change="threeStateChanged"
          />
        </div>
      </simplebar>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { ICharacteristic, ICharacteristicType } from "@/types/characteristics";
import { getCaracteristicTypeColor } from "@/utils/characteristics";
import CharThreeStateCheckbox from "~/components/CharThreeStateCheckbox.vue";
import simplebar from "simplebar-vue";
import "simplebar/dist/simplebar.min.css";
import "simplebar/dist/simplebar.min.js";
import SimpleBar from "simplebar";

@Component({
  name: "CharacteristicPanel",
  components: {
    CharThreeStateCheckbox,
    simplebar,
  },
})
export default class extends Vue {
  //#region Props
  @Prop() private characteristic_type!: ICharacteristicType;
  @Prop() private characteristics!: ICharacteristic[];
  //#endregion

  //#region Datas
  private includedIds: number[] = [];
  private excludedIds: number[] = [];
  private expanded: boolean = false;
  //#endregion

  //#region Computed
  get totalIds() {
    return this.includedIds.length + this.excludedIds.length;
  }
  //#endregion

  //#region Methods
  private getCaracteristicTypeColor(characteristic_type_id: number) {
    return getCaracteristicTypeColor(characteristic_type_id);
  }

  private threeStateChanged(caracteristic_id: number, state: number) {
    this.includedIds = this.includedIds.filter(
      (item) => item !== caracteristic_id
    );
    this.excludedIds = this.excludedIds.filter(
      (item) => item !== caracteristic_id
    );

    if (state == -1) this.excludedIds.push(caracteristic_id);
    else if (state == 1) this.includedIds.push(caracteristic_id);
    this.$emit("change", new Set(this.characteristics.map(t=>t.characteristic_id)), this.includedIds, this.excludedIds);
  }

  private stateForCheckbox(caracteristic_id: number) {
    let state = 0;
    if (this.includedIds.indexOf(caracteristic_id) !== -1) state = 1;
    else if (this.excludedIds.indexOf(caracteristic_id) !== -1) state = -1;
    return state;
  }
  //#region
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
  border-radius: 5px;
}

.header-expanded {
  border-bottom: 1px solid $primary;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 0px;
  border-bottom-left-radius: 0px;
}

.custom-scrollbar-bio {
  height: auto;
  max-height: 160px;
}
</style>