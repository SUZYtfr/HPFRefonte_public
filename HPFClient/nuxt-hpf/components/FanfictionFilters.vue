<template>
  <div :value="fanfictionFilters">
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
            v-model="fanfictionFilters.searchTerm"
          >
          </b-input>
        </b-field>
      </div>
      <div class="column is-3 pt-0" v-if="authorFieldVisible">
        <b-field
          label="Rechercher un auteur"
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-input
            placeholder="Rechercher..."
            type="search"
            icon="search"
            v-model="fanfictionFilters.searchAuthor"
          >
          </b-input>
        </b-field>
      </div>
      <div class="column is-3 pt-0">
        <b-field
          label="Ordre de tri"
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-select
            placeholder="Trier par"
            icon="sort"
            expanded
            v-model="fanfictionFilters.sortBy"
          >
            <option value="alpha">Ordre alphabétique</option>
            <option value="most_recent">Plus récent au plus ancien</option>
            <option value="less_recent">Plus ancien au plus récent</option>
            <option value="most_reviews">Nombre de reviews - croissant</option>
            <option value="less_reviews">
              Nombre de reviews - décroissant
            </option>
            <option value="most_rating">Rating - croissant</option>
            <option value="less_rating">Rating - décroissant</option>
          </b-select>
        </b-field>
      </div>
    </div>
    <div class="columns mt-0 is-vcentered">
      <div class="column is-6 pt-0">
        <b-switch :rounded="false" v-model="fanfictionFilters.completed"
          >Terminées</b-switch
        >
        <b-switch :rounded="false" v-model="fanfictionFilters.coauthor"
          >Co-écrites</b-switch
        >
      </div>
      <div class="column is-3 pt-0">
        <b-field
          label="Mots minimums"
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-input
            v-model="displayMinWords"
            type="text"
            placeholder="Mots minimums"
            icon-right="close-circle"
            icon-right-clickable
            @icon-right-click="clearFieldMinWord($event)"
            @keydown.native="restrictNumber($event)"
          >
          </b-input>
        </b-field>
      </div>
      <div class="column is-3 pt-0">
        <b-field
          label="Mots maximums"
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-input
            v-model="displayMaxWords"
            type="text"
            placeholder="Mots maximums"
            icon-right="close-circle"
            icon-right-clickable
            @icon-right-click="clearFieldMaxWord($event)"
            @keydown.native="restrictNumber($event)"
          >
          </b-input>
        </b-field>
      </div>
      <!-- <div class="column pt-0 pb-1">
        <b-slider
          v-model="fanfictionFilters.words"
          type="is-primary"
          :min="1"
          :max="6"
          :step="1"
          lazy
          :custom-formatter="(val) => sliderCustomFormatter(val)"
          append-to-body
          ticks
        >
          <template v-for="val in sliderTicks">
            <b-slider-tick
              :value="val.sliderValue"
              :key="val.displayValue"
              class="has-text-weight-semibold"
              >{{ val.displayValue }}</b-slider-tick
            >
          </template>
        </b-slider>
      </div> -->
    </div>
    <div class="columns mt-0">
      <div class="column is-6 pt-0">
        <b-field
          label="Inclure des personnages, catégories, genres, époques..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-taginput
            v-model="fanfictionFilters.includedTags"
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
            v-model="fanfictionFilters.excludedTags"
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
import { FanfictionFiltersData } from "@/types/fanfictions";
import { ICharacteristic, ICharacteristicType } from "@/types/characteristics";
import { ConfigModule } from "@/utils/store-accessor";
import { groupBy } from "@/utils/es6-utils";
import { getClassTypeColor, getFullPath } from "@/utils/characteristics";

@Component({
  name: "FanfictionFilters",
})
export default class extends Vue {
  //#region Props
  @Prop() private authorFieldVisible!: boolean;
  //#endregion

  //#region Data
  private fanfictionFilters: FanfictionFiltersData = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: 0,
    sortBy: "most_recent",
    multipleAuthors: null,
    status: null,
    minWord: null,
    maxWord: null,
    words: [1, 6],
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: false,
    inclusive: false,
    fromDate: null,
    toDate: null,
  };

  private displayMinWords: string = "";
  private displayMaxWords: string = "";

  private sliderTicks = [
    { sliderValue: 1, realValue: 500, displayValue: "<500" },
    { sliderValue: 2, realValue: 1000, displayValue: "1000" },
    { sliderValue: 3, realValue: 5000, displayValue: "5000" },
    { sliderValue: 4, realValue: 10000, displayValue: "10000" },
    { sliderValue: 5, realValue: 50000, displayValue: "50000" },
    { sliderValue: 6, realValue: 100000, displayValue: ">100000" },
  ];

  private characteristics: any[] = [];
  private filteredCharacteristics: any[] = [];
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
    this.$emit("change", this.fanfictionFilters);
  }

  @Watch("displayMinWords")
  private minWordsChanged() {
    console.log(this.displayMinWords);
    this.fanfictionFilters.minWord = isNaN(parseInt(this.displayMinWords))
      ? null
      : parseInt(this.displayMinWords);
  }

  @Watch("displayMaxWords")
  private maxWordsChanged() {
    this.fanfictionFilters.maxWord = isNaN(parseInt(this.displayMaxWords))
      ? null
      : parseInt(this.displayMaxWords);
  }
  //#endregion

  //#region Methods
  private sliderCustomFormatter(sliderValue: number) {
    let result = "";
    if (sliderValue == 1) result += "< ";
    if (sliderValue == 6) result += "> ";
    result += this.sliderTicks[sliderValue - 1].realValue;
    return result + " mots";
  }

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
          !this.fanfictionFilters.includedTags.includes(item) &&
          !this.fanfictionFilters.excludedTags.includes(item)
      );

      let itemsSorted: ICharacteristic[] = items
        .filter((t) => t.parent_id == null)
        .sort((a: ICharacteristic, b: ICharacteristic) => {
          return a.in_order - b.in_order;
        });
      groupBy(items, (g: ICharacteristic) => g.parent_id).forEach(
        (value: ICharacteristic[], key: number) => {
          if (key != null) {
            let index = itemsSorted.findIndex(
              (c) => c.characteristic_id === key
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
      (characteristic: ICharacteristic) => characteristic.characteristic_type_id
    );
    ConfigModule.characteristicTypes.forEach((element: ICharacteristicType) => {
      const items = grouped
        .get(element.characteristic_type_id)
        .map((groupedCharacteristic: ICharacteristic) => {
          return groupedCharacteristic;
        });

      let itemsSorted: ICharacteristic[] = items
        .filter((t: ICharacteristic) => t.parent_id == null)
        .sort((a: ICharacteristic, b: ICharacteristic) => {
          return a.in_order - b.in_order;
        });
      groupBy(items, (g: ICharacteristic) => g.parent_id).forEach(
        (value: ICharacteristic[], key: number) => {
          if (key != null) {
            let index = itemsSorted.findIndex(
              (c) => c.characteristic_id === key
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

  private clearFieldMinWord(event: any) {
    this.displayMinWords = "";
  }

  private clearFieldMaxWord(event: any) {
    this.displayMaxWords = "";
  }

  private restrictNumber(event: any) {
    if (
      (event.keyCode < 8 || event.keyCode > 13) &&
      (event.keyCode < 35 || event.keyCode > 46) &&
      (event.keyCode < 96 || event.keyCode > 105)
    ) {
      event.preventDefault();
      event.stopPropagation();
    }
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