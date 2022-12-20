<template>
  <div>
    <div class="columns my-0">
      <div class="column pt-0">
        <b-field
          label="Rechercher un titre, un mot-clé..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-input
            placeholder="Rechercher..."
            type="search"
            icon="search"
            v-model="fanfictionQueryParams.title"
          >
          </b-input>
        </b-field>
      </div>
      <div class="column is-6 pt-0">
        <ThreeStateCheckbox
            class="py-1 pl-1"
            :externalValue="fanfictionQueryParams.status"
            :checkedValue="4"
            :excludedValue="1"
            :uncheckedValue="null"
            @change="fanfictionQueryParams.status = $event"
            title="Histoires terminées"
          />
          <ThreeStateCheckbox
            class="py-1 pl-1"
            :externalValue="fanfictionQueryParams.multipleAuthors"
            @change="fanfictionQueryParams.multipleAuthors = $event"
            title="Histoires co-écrites"
          />
          <ThreeStateCheckbox
            class="py-1 pl-1"
            :externalValue="fanfictionQueryParams.featured"
            @change="fanfictionQueryParams.featured = $event"
            title="Histoires médaillés"
          />
      </div>
    </div>
    <div class="columns mt-0">
      <div class="column is-6 pt-0">
        <b-field
          label="Inclure des personnages, catégories, genres, époques..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-taginput
            v-model="fanfictionQueryParams.includedTags"
            :data="filteredCharacteristics"
            autocomplete
            :open-on-focus="true"
            ref="includedTags"
            field="name"
            icon="plus-square"
            placeholder="Inclure des personnages, catégories, genres, époques..."
            group-field="type"
            group-options="items"
            @typing="getFilteredTags"
            @input="tagInput"
          >
            <template v-slot="props">
              <span class="is-italic has-text-weight-light">{{
                getFullPath(props.option)
              }}</span
              ><span class="has-text-weight-semibold">{{
                props.option.name
              }}</span>
            </template>
            <template #empty> Aucun résultat </template>
            <template #selected="props">
              <b-tag
                v-for="(tag, index) in props.tags"
                :key="index"
                :class="getClassTypeColor(tag)"
                :tabstop="false"
                closable
                @close="$refs.includedTags.removeTag(index, $event)"
              >
                {{ tag.name }}
              </b-tag>
            </template>
          </b-taginput>
        </b-field>
      </div>
      <div class="column is-6 pt-0">
        <b-field
          label="Exclure des personnages, catégories, genres, époques..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-taginput
            v-model="fanfictionQueryParams.excludedTags"
            :data="filteredCharacteristics"
            autocomplete
            :open-on-focus="true"
            ref="excludedTags"
            field="name"
            icon="minus-square"
            placeholder="Exclure des personnages, catégories, genres, époques..."
            group-field="type"
            group-options="items"
            @typing="getFilteredTags"
            @input="tagInput"
          >
            <template v-slot="props">
              <span class="is-italic has-text-weight-light">{{
                getFullPath(props.option)
              }}</span
              ><span class="has-text-weight-semibold">{{
                props.option.name
              }}</span>
            </template>
            <template #empty> Aucun résultat </template>
            <template #selected="props">
              <b-tag
                v-for="(tag, index) in props.tags"
                :key="index"
                class="characteristic-bg-excluded"
                :tabstop="false"
                ellipsis
                closable
                @close="$refs.excludedTags.removeTag(index, $event)"
              >
                {{ tag.name }}
              </b-tag>
            </template>
          </b-taginput>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "vue-property-decorator";
import { FanfictionQueryParams } from "@/types/fanfictions";
import { ICharacteristic, ICharacteristicType } from "@/types/characteristics";
import { ConfigModule } from "@/utils/store-accessor";
import { groupBy } from "@/utils/es6-utils";
import { getClassTypeColor, getFullPath } from "@/utils/characteristics";
import { getCharacteristics, getCharacteristicTypes } from "@/api/characteristics";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";

@Component({
  name: "FanfictionFiltersSmall",
  components:{
    ThreeStateCheckbox,
  }
})
export default class extends Vue {
  //#region Props
  @Prop() private authorFieldVisible!: boolean;
  @Prop() private fanfictionQueryParams!: FanfictionQueryParams;
  //#endregion

  //#region Data
  private characteristics: any[] = [];
  private filteredCharacteristics: any[] = [];
  private characteristic_types: ICharacteristicType[] = [];
  //#endregion

  //#region Hooks
  async fetch() {
    // Récupération des caractéristiques
    await this.getCharacteristics();
  }
  //#endregion

  //#region Computed
  //#endregion

  //#region Watchers
  @Watch("fanfictionFilters", { deep: true })
  private onFiltersChanged() {
    this.$emit("change", this.fanfictionQueryParams);
  }
  //#endregion

  //#region Methods
  private getFilteredTags(text: string) {
    this.filteredCharacteristics = [];
    this.characteristics.forEach((element) => {
      let items: ICharacteristic[] = [];
      if (element.type.toLowerCase().indexOf(text.toLowerCase()) >= 0) {
        items = element.items;
      } else {
        items = element.items.filter(
          (item: ICharacteristic) =>
            (this.getFullPath(item) + item.name)
              .replace(/[\\\- ]/gi, "")
              .toLowerCase()
              .indexOf(text.replace(/[\\\- ]/gi, "").toLowerCase()) >= 0
        );
      }
      items = items.filter(
        (item: ICharacteristic) =>
          // @ts-ignore
          this.fanfictionQueryParams.includedTags!.includes(item.id) &&
          // @ts-ignore
          this.fanfictionQueryParams.excludedTags!.includes(item.id)
      );

      let itemsSorted: ICharacteristic[] = items
        .filter((t) => t.parent_id == null)
        .sort((a: ICharacteristic, b: ICharacteristic) => {
          return a.order! - b.order!;
        });
      groupBy(items, (g: ICharacteristic) => g.parent_id).forEach(
        (value: ICharacteristic[], key: number) => {
          if (key != null) {
            let index = itemsSorted.findIndex(
              (c) => c.id === key
            );
            if (index == -1) itemsSorted.splice(0, 0, ...value);
            else itemsSorted.splice(index + 1, 0, ...value);
          }
        }
      );
      if (itemsSorted.length) {
        this.filteredCharacteristics.push({
          type: element.type,
          items: itemsSorted,
        });
      }
    });
  }

  private tagInput(tag: any) {
    this.getFilteredTags("");
  }

  private async getCharacteristics() {
    if (
      ConfigModule.characteristicTypes.length == 0 ||
      ConfigModule.characteristics.length == 0
    ) {
      await ConfigModule.LoadConfig();
    }

    const grouped = groupBy(
      ConfigModule.characteristics,
      (characteristic: ICharacteristic) => characteristic.category_id
    );
    ConfigModule.characteristicTypes.forEach((element: ICharacteristicType) => {
      const items = grouped
        .get(element.id)
        .map((groupedCharacteristic: ICharacteristic) => {
          return groupedCharacteristic;
        });

      let itemsSorted: ICharacteristic[] = items
        .filter((t: ICharacteristic) => t.parent_id == null)
        .sort((a: ICharacteristic, b: ICharacteristic) => {
          return a.order! - b.order!;
        });
      groupBy(items, (g: ICharacteristic) => g.parent_id).forEach(
        (value: ICharacteristic[], key: number) => {
          if (key != null) {
            let index = itemsSorted.findIndex(
              (c) => c.id === key
            );
            if (index == -1) itemsSorted.splice(0, 0, ...value);
            else itemsSorted.splice(index + 1, 0, ...value);
          }
        }
      );
      this.characteristics.push({
        type: element.name,
        items: itemsSorted,
      });
    });
    this.filteredCharacteristics = this.characteristics;
  }

  private getClassTypeColor(characteristic: ICharacteristic) {
    return getClassTypeColor(characteristic);
  }

  private getFullPath(characteristic: ICharacteristic) {
    return getFullPath(characteristic, ConfigModule.characteristics);
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>