<template>
  <div style="height: 500px; width: 70%;">
    <p v-if="$fetchState.pending">
      Loading....
    </p>
    <p v-else-if="$fetchState.error">
      Error while fetching
    </p>
    <div Fv-else>
      <!-- <p>
        {{ characteristics_types[0].name }}
        {{ ( characteristics_types[0] instanceof CharacteristicTypeModel) }}
      </p>
      <p>
        {{ characteristics[0].name }}
        {{ ( characteristics[0] instanceof CharacteristicModel) }}
      </p> -->
      <p v-if="fanfictions[0] != null">
        {{ fanfictions[0].title }}
        {{ ( fanfictions[0] instanceof FanfictionModel) }}
        {{ ( fanfictions[0].creation_date instanceof Date) }}
        {{ ( fanfictions[0].last_update_date instanceof Date) }}
        {{ (new Date()).toLocaleDateString() }}
      </p>
      <p v-if="(fanfictions[0]?.last_update_date instanceof Date)">
        {{ fanfictions[0].last_update_date?.toLocaleDateString() }}
      </p>
      <p v-if="(fanfictions[0]?.creation_date instanceof Date)">
        {{ fanfictions[0].creation_date?.toLocaleDateString() }}
      </p>
      <p>
        {{ new Date("2020-11-01T19:25:43.511Z") }}
      </p>
    </div>
    <!-- <client-only>
      <TipTapEditor class="m-5" />
    </client-only> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";

// import { plainToInstance, Type } from "class-transformer";
// import { ConfigModule } from "@/utils/store-accessor";
import { SerialiseClass } from "@/serialiser-decorator";
// import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { FanfictionModel } from "@/models/fanfictions";
import { searchFanfictions } from "@/api/fanfictions";

// import TipTapEditor from "~/components/TipTapEditor.vue";

@Component({
  // components: {
  //   TipTapEditor
  // }
  fetchOnServer: true,
  fetchKey: "test-key"
})
export default class Test extends Vue {
  // @SerialiseClass(CharacteristicModel)
  // public characteristics: CharacteristicModel[] = [];

  // @SerialiseClass(CharacteristicTypeModel)
  // public characteristics_types: CharacteristicTypeModel[] = [];

  @SerialiseClass(FanfictionModel)
  public fanfictions: FanfictionModel[] = [];

  asyncData(): void {
    console.log("asyncData");
  }

  created(): void {
    console.log("created");
  }

  async fetch(): Promise<void> {
    console.log("fetch");
    await this.getFanfictions();
  }

  mounted(): void {
    console.log("mounted");
  }

  beforeCreate(): void {
    console.log("beforeCreate");
  }

  beforeMount(): void {
    console.log("beforeMount");
  }

  beforeUpdate(): void {
    console.log("beforeUpdate");
  }

  updated(): void {
    console.log("updated");
  }

  beforeUnmount(): void {
    console.log("beforeUnmount");
  }

  unmounted(): void {
    console.log("unmounted");
  }

  // @Watch("$fetchState.pending", { immediate: true, deep: false })
  // private onFetchChanged(): void {
  //   console.log("fetchstate:");
  //   if (this.$fetchState !== undefined) {
  //     console.log(this.$fetchState.pending);
  //     // console.log(this.characteristics);
  //     // console.log(this.characteristics_types);
  //     // Création des CharacteristicData instanciées
  //     this.characteristics = plainToInstance(
  //       CharacteristicModel,
  //       this.characteristics
  //     );
  //     this.characteristics_types = plainToInstance(
  //       CharacteristicTypeModel,
  //       this.characteristics_types
  //     );
  //   }
  // }

  // private async getCharacteristics(): Promise<void> {
  //   if (
  //     ConfigModule.characteristicTypes.length === 0 ||
  //     ConfigModule.characteristics.length === 0
  //   ) {
  //     await ConfigModule.LoadConfig();
  //   }
  //   this.characteristics = ConfigModule.characteristics;
  //   this.characteristics_types = ConfigModule.characteristicTypes;
  //   console.log(this.characteristics);
  //   console.log(this.characteristics_types);
  // }

  private async getFanfictions(): Promise<void> {
    // this.listLoading = true;
    try {
      this.fanfictions = (await searchFanfictions(null)).items;
      // console.log(this.fanfictions);
      console.log("Fanfiction type: " + (this.fanfictions[0] instanceof FanfictionModel));
      console.log("Date type: " + ((new Date()) instanceof Date));
      console.log("Creation date type: " + (this.fanfictions[0].creation_date instanceof Date));
      console.log("Last update date type: " + (this.fanfictions[0].last_update_date instanceof Date));
      console.log(this.fanfictions[0].creation_date?.toLocaleDateString());
      // console.log(this.fanfictions[0] instanceof FanfictionModel);
    } catch (error) {
      console.log(error);
    } finally {
      // this.listLoading = false;
    }
  }
}

</script>

<style lang="scss">
//@import "~/assets/scss/custom.scss";
</style>
