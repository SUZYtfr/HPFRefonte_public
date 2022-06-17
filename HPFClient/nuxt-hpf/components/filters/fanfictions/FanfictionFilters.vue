<template>
  <div class="card is-relative">
    <b-loading :is-full-page="false" v-model="loading"></b-loading>
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">Filtres</p>
    </header>
    <div
      :class="[
        'card-content',
        'px-2',
        'py-3',
        { 'fixed-height-card': isFixedHeightCard },
      ]"
    >
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
      <b-field
        label="Nombre de mots"
        label-position="on-border"
        custom-class="has-text-primary z-index-zero"
      >
        <b-slider
          v-model="fanfictionFilters.words"
          type="is-primary"
          class="px-4 pt-4 pb-3"
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
      </b-field>
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :externalValue="fanfictionFilters.status"
        :checkedValue="4"
        :excludedValue="1"
        :uncheckedValue="null"
        @change="fanfictionFilters.status = $event"
        title="Histoires terminées"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :externalValue="fanfictionFilters.multipleAuthors"
        @change="fanfictionFilters.multipleAuthors = $event"
        title="Histoires co-écrites"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :externalValue="fanfictionFilters.featured"
        @change="fanfictionFilters.featured = $event"
        title="Histoires médaillés"
      />
      <CharacteristicPanel
        class="my-2"
        v-for="(type, index) in characteristics_types"
        :key="'tag_' + index.toString()"
        :characteristic_type="type"
        :characteristics="filteredCharacteristics(type.characteristic_type_id)"
        @change="characteristicsChanged"
      />
      <b-field
        label="Tags personnalisés"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-taginput
          v-model="fanfictionFilters.customTags"
          :data="filteredTags"
          autocomplete
          :allow-new="false"
          :open-on-focus="true"
          icon="plus-square"
          placeholder="Inclure un tag personnalisé"
          @typing="getFilteredTags"
          class="mt-4"
        >
        </b-taginput>
      </b-field>
      <b-field
        label="Publiée après le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="fanfictionFilters.fromDate"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="fanfictionFilters.fromDate ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="fanfictionFilters.fromDate = null"
        >
        </b-datepicker>
      </b-field>
      <b-field
        label="Publiée avant le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="fanfictionFilters.toDate"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="fanfictionFilters.toDate ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="fanfictionFilters.toDate = null"
        >
        </b-datepicker>
      </b-field>
      <b-switch
        class="ml-1"
        :rounded="false"
        v-model="fanfictionFilters.inclusive"
        >Recherche inclusive</b-switch
      >
      <b-tooltip
        :position="tooltipPosition"
        type="is-primary"
        append-to-body
        multilined
      >
        <b-icon
          pack="fas"
          class="is-clickable"
          type="is-primary"
          icon="question-circle"
        >
        </b-icon>
        <template v-slot:content>
          <p>
            <strong class="has-text-white">Activé:</strong> Recherche les
            fictions Aventure/Action
            <strong class="has-text-white"><em>ET</em></strong>
            Comédie/Humour.
          </p>
          <p>
            <strong class="has-text-white">Désactivé:</strong> Recherche les
            fictions Aventure/Action
            <strong class="has-text-white"><em>OU</em></strong>
            Comédie/Humour.
          </p>
        </template>
      </b-tooltip>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <a @click.prevent.stop="toggleFilterChanged()">Rechercher</a>
        </span>
      </p>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "vue-property-decorator";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";
import CharacteristicPanel from "@/components/CharacteristicPanel.vue";
import { FanfictionFiltersData } from "~/types/fanfictions";
import { groupBy } from "@/utils/es6-utils";
import { ICharacteristic, ICharacteristicType } from "@/types/characteristics";
import { ConfigModule } from "@/utils/store-accessor";

@Component({
  name: "FanfictionFilters",
  components: {
    ThreeStateCheckbox,
    CharacteristicPanel,
  },
})
export default class extends Vue {
  //#region Props
  @Prop() private fanfictionFilters!: FanfictionFiltersData;
  @Prop({ default: false }) private loading!: boolean;
  @Prop({ default: false }) private isFixedHeightCard!: boolean;
  @Prop({ default: "is-right" }) private tooltipPosition!: string;
  //#endregion

  //#region Datas
  private sliderTicks = [
    { sliderValue: 1, realValue: 500, displayValue: "<500" },
    { sliderValue: 2, realValue: 1000, displayValue: "1k" },
    { sliderValue: 3, realValue: 5000, displayValue: "5k" },
    { sliderValue: 4, realValue: 10000, displayValue: "10k" },
    { sliderValue: 5, realValue: 50000, displayValue: "50k" },
    { sliderValue: 6, realValue: 100000, displayValue: ">100k" },
  ];

  private filteredTags: ICharacteristic[] = [];
  private characteristics: ICharacteristic[] = [];
  private characteristics_types: ICharacteristicType[] = [];
  //#endregion

  //#region Hooks
  async fetch() {
    // Récupération des caractéristiques
    await this.getCharacteristics();
  }
  //#endregion

  //#region Methods
  private async getCharacteristics() {
    if (
      ConfigModule.characteristicTypes.length == 0 ||
      ConfigModule.characteristics.length == 0
    ) {
      await ConfigModule.LoadConfig();
    }
    this.characteristics = ConfigModule.characteristics;
    this.characteristics_types = ConfigModule.characteristicTypes;
  }

  private sliderCustomFormatter(sliderValue: number) {
    let result = "";
    if (sliderValue == 1) result += "< ";
    if (sliderValue == 6) result += "> ";
    result += this.sliderTicks[sliderValue - 1].realValue;
    return result + " mots";
  }

  private filteredCharacteristics(characteristic_type_id: number) {
    let itemsSorted: ICharacteristic[] = this.characteristics
      .filter(
        (t: ICharacteristic) =>
          t.characteristic_type_id == characteristic_type_id &&
          t.parent_id == null
      )
      .sort((a: ICharacteristic, b: ICharacteristic) => {
        return a.in_order - b.in_order;
      });
    groupBy(
      this.characteristics.filter(
        (t: ICharacteristic) =>
          t.characteristic_type_id == characteristic_type_id
      ),
      (g: ICharacteristic) => g.parent_id
    ).forEach((value: ICharacteristic[], key: number) => {
      if (key != null) {
        let index = itemsSorted.findIndex((c) => c.characteristic_id === key);
        if (index == -1) itemsSorted.splice(0, 0, ...value);
        else itemsSorted.splice(index + 1, 0, ...value);
      }
    });
    return itemsSorted;
  }

  // Récupération des tags utilisateurs
  private async getFilteredTags(text: string) {
    //this.filteredTags =
  }

  // Mise à jour des filtres des caractéristiques incluses / excluses
  private characteristicsChanged(
    allIds: Set<number>,
    includedIds: number[],
    excludedIds: number[]
  ) {
    this.fanfictionFilters.excludedTags =
      this.fanfictionFilters.excludedTags.filter(
        (excludedId) => !allIds.has(excludedId)
      );
    this.fanfictionFilters.excludedTags =
      this.fanfictionFilters.excludedTags.concat(excludedIds);
    this.fanfictionFilters.includedTags =
      this.fanfictionFilters.includedTags.filter(
        (includedId) => !allIds.has(includedId)
      );
    this.fanfictionFilters.includedTags =
      this.fanfictionFilters.includedTags.concat(includedIds);
  }

  // Déclencher le Watcher des filtres sur le clique recherche
  private toggleFilterChanged() {
    this.fanfictionFilters.searchTerm = this.fanfictionFilters.searchTerm + " ";
    this.fanfictionFilters.searchTerm = this.fanfictionFilters.searchTerm.slice(
      0,
      -1
    );
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.card {
  overflow: hidden;
}

.card-header-title {
  color: white;
  text-transform: uppercase;
  background-color: $primary;
}

.card-content {
  padding: 0px;
}

.fixed-height-card {
  height: 70vh; 
  overflow-y: scroll
}

.z-index-zero {
  z-index: 0 !important;
}
</style>