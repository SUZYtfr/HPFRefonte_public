<template>
  <div class="card is-relative">
    <b-loading v-model="loading" :is-full-page="false" />
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">
        Filtres
      </p>
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
          v-model="fanfictionFilters.searchTerm"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
      </b-field>
      <b-field
        label="Rechercher un auteur"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-input
          v-model="fanfictionFilters.searchAuthor"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
      </b-field>
      <b-field
        label="Nombre de mots"
        label-position="on-border"
        custom-class="has-text-primary z-index-zero"
      >
        <b-slider
          v-model="sliderWords"
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
              :key="val.displayValue"
              :value="val.sliderValue"
              class="has-text-weight-semibold"
            >
              {{ val.displayValue }}
            </b-slider-tick>
          </template>
        </b-slider>
      </b-field>
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.status"
        :checked-value="4"
        :excluded-value="1"
        :unchecked-value="null"
        title="Histoires terminées"
        @change="fanfictionFilters.status = $event"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.multipleAuthors"
        title="Histoires co-écrites"
        @change="fanfictionFilters.multipleAuthors = $event"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.featured"
        title="Histoires médaillés"
        @change="fanfictionFilters.featured = $event"
      />
      <CharacteristicPanel
        v-for="(type, index) in characteristics_types"
        :key="'tag_' + index.toString()"
        class="my-2"
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
          class="mt-4"
          @typing="getFilteredTags"
        />
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
        />
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
        />
      </b-field>
      <b-switch
        v-model="fanfictionFilters.inclusive"
        class="ml-1"
        :rounded="false"
      >
        Recherche inclusive
      </b-switch>
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
        />
        <template #content>
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
import { SerialiseClass } from "@/serialiser-decorator";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";
import CharacteristicPanel from "@/components/CharacteristicPanel.vue";
import { IFanfictionFilters } from "~/types/fanfictions";
import { groupBy } from "@/utils/es6-utils";
import { ConfigModule } from "@/utils/store-accessor";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";

@Component({
  name: "FanfictionFilters",
  components: {
    ThreeStateCheckbox,
    CharacteristicPanel
  },
  fetchOnServer: true,
  fetchKey: "fanfiction-filter"
})
export default class extends Vue {
  // #region Props
  @Prop() public fanfictionFilters!: IFanfictionFilters;
  @Prop({ default: false }) public loading!: boolean;
  @Prop({ default: false }) public isFixedHeightCard!: boolean;
  @Prop({ default: "is-right" }) public tooltipPosition!: string;
  // #endregion

  // #region Datas
  public sliderTicks = [
    { sliderValue: 1, realValue: 500, displayValue: "<500" },
    { sliderValue: 2, realValue: 1000, displayValue: "1k" },
    { sliderValue: 3, realValue: 5000, displayValue: "5k" },
    { sliderValue: 4, realValue: 10000, displayValue: "10k" },
    { sliderValue: 5, realValue: 50000, displayValue: "50k" },
    { sliderValue: 6, realValue: 100000, displayValue: ">100k" }
  ];

  @SerialiseClass(CharacteristicModel)
  public filteredTags: CharacteristicModel[] = [];

  @SerialiseClass(CharacteristicModel)
  private characteristics: CharacteristicModel[] = [];

  @SerialiseClass(CharacteristicTypeModel)
  public characteristics_types: CharacteristicTypeModel[] = [];

  public sliderWords: number[] = [1, 6];
  // #endregion

  // #region Hooks
  async fetch(): Promise<void> {
    // Récupération des caractéristiques
    await this.getCharacteristics();
  }
  // #endregion

  // #region Watchers
  @Watch("sliderWords")
  public onSliderChanged(): void {
    this.fanfictionFilters.minWords = this.sliderTicks[this.sliderWords[0] - 1].realValue;
    this.fanfictionFilters.maxWords = this.sliderTicks[this.sliderWords[1] - 1].realValue;
    // Valeurs min et max -> null
    if (this.fanfictionFilters.minWords === 500) this.fanfictionFilters.minWords = null;
    if (this.fanfictionFilters.maxWords === 100000) this.fanfictionFilters.maxWords = null;
  }
  // #endregion

  // #region Methods
  private async getCharacteristics(): Promise<void> {
    // this.characteristics = (await getCharacteristics(null)).items;
    // this.characteristics_types = (await getCharacteristicsTypes()).items;
    if (
      ConfigModule.characteristicTypes.length === 0 ||
      ConfigModule.characteristics.length === 0
    ) {
      await ConfigModule.LoadConfig();
    }
    this.characteristics = ConfigModule.characteristics;
    console.log("CharacteristicModel: " + (this.characteristics[0] instanceof CharacteristicModel));
    this.characteristics_types = ConfigModule.characteristicTypes;
    console.log("CharacteristicTypeModel: " + (this.characteristics_types[0] instanceof CharacteristicTypeModel));
  }

  public sliderCustomFormatter(sliderValue: number): string {
    let result = "";
    if (sliderValue === 1) result += "< ";
    if (sliderValue === 6) result += "> ";
    result += this.sliderTicks[sliderValue - 1].realValue;
    return result + " mots";
  }

  public filteredCharacteristics(characteristic_type_id: number): CharacteristicModel[] {
    const itemsSorted: CharacteristicModel[] = this.characteristics
      .filter(
        (t: CharacteristicModel) =>
          t.characteristic_type_id === characteristic_type_id &&
          t.parent_id == null
      )
      .sort((a: CharacteristicModel, b: CharacteristicModel) => {
        return a.in_order - b.in_order;
      });
    groupBy(
      this.characteristics.filter(
        (t: CharacteristicModel) =>
          t.characteristic_type_id === characteristic_type_id
      ),
      (g: CharacteristicModel) => g.parent_id
    ).forEach((value: CharacteristicModel[], key: number) => {
      if (key != null) {
        const index = itemsSorted.findIndex(c => c.id === key);
        if (index === -1) itemsSorted.splice(0, 0, ...value);
        else itemsSorted.splice(index + 1, 0, ...value);
      }
    });
    return itemsSorted;
  }

  // Récupération des tags utilisateurs
  public async getFilteredTags(text: string): Promise<void> {
    // this.filteredTags =
  }

  // Mise à jour des filtres des caractéristiques incluses / excluses
  public characteristicsChanged(
    allIds: Set<number>,
    includedIds: number[],
    excludedIds: number[]
  ): void {
    this.fanfictionFilters.excludedTags =
      this.fanfictionFilters.excludedTags.filter(
        excludedId => !allIds.has(excludedId)
      );
    this.fanfictionFilters.excludedTags =
      this.fanfictionFilters.excludedTags.concat(excludedIds);
    this.fanfictionFilters.includedTags =
      this.fanfictionFilters.includedTags.filter(
        includedId => !allIds.has(includedId)
      );
    this.fanfictionFilters.includedTags =
      this.fanfictionFilters.includedTags.concat(includedIds);
  }

  // Déclencher le Watcher des filtres sur le clique recherche
  public toggleFilterChanged(): void {
    this.fanfictionFilters.searchTerm = this.fanfictionFilters.searchTerm + " ";
    this.fanfictionFilters.searchTerm = this.fanfictionFilters.searchTerm.slice(
      0,
      -1
    );
  }
  // #endregion
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
