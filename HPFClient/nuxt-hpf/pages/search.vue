<template>
  <div class="container px-5">
    <!-- Modal filtres -->
    <b-modal
      v-model="filtersOpened"
      scroll="clip"
      width="70vw"
      class="is-hidden-desktop"
      has-modal-card
    >
      <div class="card">
        <header class="card-header sub-title">
          <p class="card-header-title is-centered">Filtres</p>
        </header>
        <div
          class="card-content px-2 py-3"
          style="height: 70vh; overflow-y: scroll"
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
            :key="index"
            :characteristic_type="type"
            :characteristics="
              filteredCharacteristics(type.characteristic_type_id)
            "
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
          <b-tooltip position="is-right" type="is-primary" multilined>
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
                <strong class="has-text-white"><i>ET</i></strong>
                Comédie/Humour.
              </p>
              <p>
                <strong class="has-text-white">Désactivé:</strong> Recherche les
                fictions Aventure/Action
                <strong class="has-text-white"><i>OU</i></strong>
                Comédie/Humour.
              </p>
            </template>
          </b-tooltip>
        </div>
        <footer class="card-footer">
          <p class="card-footer-item py-2">
            <span>
              <a @click.prevent.stop="onFiltersChanged">Rechercher</a>
            </span>
          </p>
        </footer>
      </div>
    </b-modal>
    <br />
    <div class="columns is-desktop">
      <!-- Panel filtres (seulement en desktop et supérieur) -->
      <div
        class="column is-4-desktop is-3-widescreen is-3-fullhd is-hidden-touch"
      >
        <div class="card is-relative">
          <b-loading :is-full-page="false" v-model="listLoading"></b-loading>
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Filtres</p>
          </header>
          <div class="card-content px-2 py-3">
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
              :key="index"
              :characteristic_type="type"
              :characteristics="
                filteredCharacteristics(type.characteristic_type_id)
              "
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
              position="is-right"
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
                  <strong class="has-text-white"><i>ET</i></strong>
                  Comédie/Humour.
                </p>
                <p>
                  <strong class="has-text-white">Désactivé:</strong> Recherche
                  les fictions Aventure/Action
                  <strong class="has-text-white"><i>OU</i></strong>
                  Comédie/Humour.
                </p>
              </template>
            </b-tooltip>
          </div>
          <footer class="card-footer">
            <p class="card-footer-item py-2">
              <span>
                <a @click.prevent.stop="onFiltersChanged">Rechercher</a>
              </span>
            </p>
          </footer>
        </div>
      </div>
      <!-- Liste des fictions -->
      <div class="column is-12-tablet is-8-desktop is-9-widescreen is-9-fullhd">
        <div class="card is-flex is-flex-direction-column is-relative" style="height: 100%">
          <b-loading :is-full-page="false" v-model="listLoading"></b-loading>
          <header
            class="
              card-header
              p-2
              is-flex is-flex-direction-row is-align-items-center
            "
          >
            <div class="is-flex-grow-5 p-0 m-0 mr-2">
              <b-button
                type="is-primary"
                icon-left="redo-alt"
                @click="onFiltersChanged"
              >
                <span class="is-italic">
                  {{ fanfictionResultLabel }}
                </span>
              </b-button>
            </div>
            <div class="is-flex-shrink-5">
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
                  <option value="most_recent">
                    Plus récent au plus ancien
                  </option>
                  <option value="less_recent">
                    Plus ancien au plus récent
                  </option>
                  <option value="most_reviews">
                    Nombre de reviews - croissant
                  </option>
                  <option value="less_reviews">
                    Nombre de reviews - décroissant
                  </option>
                  <option value="most_rating">Rating - croissant</option>
                  <option value="less_rating">Rating - décroissant</option>
                </b-select>
              </b-field>
            </div>
          </header>
          <div class="card-content px-2 py-3 is-flex-grow-5">
            <div
              v-if="fanfictions.length == 0"
              class="mx-auto my-auto has-text-centered"
            >
              <span class="is-italic mt-3"
                >Aucun résultat, essayer d'ajuster les filtres de
                recherche.</span
              >
            </div>
            <div v-else>
              <Fanfiction
                class="my-2"
                v-for="(fanfiction, innerindex) of fanfictions"
                :fanfiction="fanfiction"
                v-bind:index="innerindex"
                v-bind:key="fanfiction.id"
              ></Fanfiction>
            </div>
          </div>
          <footer class="card-footer">
            <b-pagination
              class="py-2 card-footer-item"
              :total="fanfictions.length"
              v-model="currentPage"
              :range-before="rangeBefore"
              :range-after="rangeAfter"
              :order="order"
              :size="size"
              :simple="isSimple"
              :rounded="isRounded"
              :per-page="perPage"
              :icon-prev="prevIcon"
              :icon-next="nextIcon"
              aria-next-label="Page suivante"
              aria-previous-label="Page précedente"
              aria-page-label="Page"
              aria-current-label="Page actuelle"
            >
            </b-pagination>
          </footer>
        </div>
      </div>
    </div>
    <!-- Bouton filtres (seulement en tablet et inférieur) -->
    <div class="stick-bottom is-hidden-desktop">
      <b-button
        v-if="!filtersOpened"
        type="is-primary"
        icon-right="filter"
        class="btn-filters mb-2"
        @click="filtersOpened = true"
        >Afficher les filtres</b-button
      >
    </div>
    <br />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { FanfictionFiltersData, FanfictionData } from "@/types/fanfictions";
import CharacteristicPanel from "@/components/CharacteristicPanel.vue";
import { ConfigModule } from "@/utils/store-accessor";
import { ICharacteristic, ICharacteristicType } from "@/types/characteristics";
import { groupBy } from "@/utils/es6-utils";
import { getFanfictions } from "@/api/fanfictions";
import Fanfiction from "~/components/Fanfiction.vue";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";

@Component({
  name: "Recherche",
  components: {
    CharacteristicPanel,
    Fanfiction,
    ThreeStateCheckbox,
  },
})
export default class extends Vue {
  //#region Data
  //public windowWidth: number = 0;
  public filtersOpened: boolean = false;

  private fanfictionFilters: FanfictionFiltersData = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: 0,
    sortBy: "most_recent",
    multipleAuthors: null,
    status: null,
    words: [1, 6],
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: null,
    inclusive: false,
    fromDate: null,
    toDate: null,
  };

  private displayMinWords: string = "";
  private displayMaxWords: string = "";

  private sliderTicks = [
    { sliderValue: 1, realValue: 500, displayValue: "<500" },
    { sliderValue: 2, realValue: 1000, displayValue: "1k" },
    { sliderValue: 3, realValue: 5000, displayValue: "5k" },
    { sliderValue: 4, realValue: 10000, displayValue: "10k" },
    { sliderValue: 5, realValue: 50000, displayValue: "50k" },
    { sliderValue: 6, realValue: 100000, displayValue: ">100k" },
  ];

  private characteristics: ICharacteristic[] = [];
  private characteristics_types: ICharacteristicType[] = [];

  private fanfictions: FanfictionData[] = [];

  // Pagination
  private currentPage: number = 1;
  private perPage: number = 10;
  private rangeBefore: number = 3;
  private rangeAfter: number = 1;
  private order: string = "";
  private size: string = "";
  private isSimple: boolean = false;
  private isRounded: boolean = false;
  private prevIcon: string = "chevron-left";
  private nextIcon: string = "chevron-right";

  private filteredTags: ICharacteristic[] = [];

  private listLoading: boolean = false;
  private timerId: number = 0;

  //#endregion

  //#region Computed
  // get isSizeTouch() {
  //   return this.windowWidth < 1024;
  // }

  get fanfictionResultLabel() {
    let result = "";
    result +=
      this.fanfictions.length > 0
        ? this.fanfictions.length.toString()
        : "Aucun";
    result += " résultat";
    result += this.fanfictions.length > 1 ? "s" : "";
    return result;
  }
  //#endregion

  //#region Hooks
  async fetch() {
    // Récupération des caractéristiques
    await this.getCharacteristics();
  }

  // mounted() {
  //   window.addEventListener("resize", this.handleResize);
  // }
  // beforeDestroy() {
  //   window.removeEventListener("resize", this.handleResize);
  // }
  //#endregion

  //#region Watchers
  @Watch("fanfictionFilters", { deep: true })
  private onFiltersChanged() {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.getFanfictions, 500);
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

  private filteredCharacteristics(characteristic_type_id: number) {
    // return this.characteristics
    //   .filter(
    //     (t: ICharacteristic) =>
    //       t.characteristic_type_id == characteristic_type_id
    //   )
    //   .sort((a: ICharacteristic, b: ICharacteristic) => {
    //     return a.in_order - b.in_order;
    //   });

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
  
  // Mise à jour des filtres des caractéristiques incluses / excluses
  private characteristicsChanged(allIds: Set<number>, includedIds: number[], excludedIds: number[]) {
    this.fanfictionFilters.excludedTags = this.fanfictionFilters.excludedTags.filter(
      (excludedId) => !allIds.has(excludedId)
    );
    this.fanfictionFilters.excludedTags = this.fanfictionFilters.excludedTags.concat(excludedIds);
    this.fanfictionFilters.includedTags = this.fanfictionFilters.includedTags.filter(
      (includedId) => !allIds.has(includedId)
    );
    this.fanfictionFilters.includedTags = this.fanfictionFilters.includedTags.concat(includedIds);
  }

  //#endregion

  private async getFanfictions() {
    this.listLoading = true;
    try {
      const { data } = await getFanfictions(this.fanfictionFilters);
      this.fanfictions = data.items;
    } catch {
    } finally {
      this.listLoading = false;
    }
  }

  private async getFilteredTags(text: string) {
    //this.filteredTags =
  }
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.sub-title {
  background-color: $primary;
}

.sub-title .card-header-title {
  color: white;
  text-transform: uppercase;
}

.card-content {
  padding: 0px;
}

.z-index-zero {
  z-index: 0 !important;
}

.btn-filters {
  left: 50%;
  transform: translate(-50%, 0);
}

.stick-bottom {
  position: sticky;
  bottom: 0;
}
</style>