<template>
  <div class="container px-5">
    <br />
    <div class="columns">
      <div class="column">
        <div class="card">
          <!-- Breadcrumb -->
          <header class="card-header sub-title">
            <p class="is-centered card-header-title">
              Parcourir les catégories
            </p>
          </header>
          <!-- Contenu -->
          <div class="card-content px-4 pt-2 pb-4">
            <b-loading :is-full-page="false" v-model="listLoading"></b-loading>
            <!-- Breadcrumb -->
            <b-breadcrumb align="is-left" class="mb-0">
              <b-breadcrumb-item @click.native="MoveToBreadCrumb(undefined)"
                >Accueil</b-breadcrumb-item
              >
              <b-breadcrumb-item
                v-for="(charac, innerindex) of breadcrumbStack"
                v-bind:index="innerindex"
                v-bind:key="innerindex"
                @click.native="MoveToBreadCrumb(innerindex)"
                >{{ charac.name }}</b-breadcrumb-item
              >
            </b-breadcrumb>
            <hr class="mt-1 mb-3" />
            <!-- Liste -->
            <div
              v-if="currentCharacs.length > 0"
              class="columns is-multiline is-centered is-variable is-8"
            >
              <div
                v-for="(charac, innerindex) of currentCharacs"
                v-bind:index="innerindex"
                v-bind:key="innerindex"
                class="column is-4 is-4-desktop is-4-widescreen is-3-fullhd"
              >
                <TagPanel
                  :characteristic_type_id="charac.characteristic_type_id"
                  :characteristic_id="charac.characteristic_id"
                  :characteristic_name="charac.name"
                  :characteristic_description="charac.description"
                  :characteristic_count="charac.count"
                  @click="AddBreadCrumbLevel"
                />
              </div>
            </div>
            <div v-if="currentCharacs.length == 0">
              <FanfictionList
                :isCard="false"
                :fanfictionFilters="fanfictionFilters"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <br />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import TagPanel from "~/components/TagPanel.vue";
import { ConfigModule } from "@/utils/store-accessor";
import {
  ICharacteristic,
  ICharacteristicType,
  ICharacteristicFilters,
} from "@/types/characteristics";
import { getCharacteristics } from "@/api/characteristics";
import { FanfictionFiltersData } from "@/types/fanfictions";
import FanfictionList from "~/components/FanfictionList.vue";

@Component({
  name: "Category",
  components: {
    TagPanel,
    FanfictionList,
  },
})
export default class extends Vue {
  //#region Data
  private breadcrumbStack: any[] = [];

  // Caractérisitiques affichés
  private currentCharacs: any[] = [];

  // Filtres des charactéristiques
  private caracteristicFilters: ICharacteristicFilters = {
    characteristic_type_id: null,
    parent_id: null,
    options: {
      with_stats: true,
    },
    limit: 10,
  };

  // Filtres
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
    currentPage: 1,
    perPage: 10,
  };

  private listLoading: boolean = false;
  //#endregion

  //#region Hooks
  async fetch() {
    this.listLoading = true;
    // Récupération des caractéristiques types
    await this.getCharacteristicsTypes();
    this.listLoading = false;
  }
  //#endregion

  //#region Watchers
  // Actualisation des résultats
  @Watch("breadcrumbStack")
  private async onPileChanged() {
    this.listLoading = true;
    if (this.breadcrumbStack.length > 0) {
      let current = this.breadcrumbStack[this.breadcrumbStack.length - 1];
      this.caracteristicFilters.characteristic_type_id =
        current.characteristic_type_id;
      this.caracteristicFilters.parent_id = current.characteristic_id;
      await this.getCharacteristics();
      // Si pas de nouvelle caractéristique, on est en bas de la pile on déclenche recherche les fictions
      if (this.currentCharacs.length == 0)
        this.fanfictionFilters.includedTags = [current.characteristic_id];
    } else {
      await this.getCharacteristicsTypes();
    }
    this.listLoading = false;
  }
  //#endregion

  //#region Methods
  // Récupération des caractéristiques types, depuis la config
  private async getCharacteristicsTypes() {
    if (ConfigModule.characteristicTypes.length == 0)
      await ConfigModule.LoadConfig();
    this.currentCharacs = ConfigModule.characteristicTypes;
  }

  // Récupération des caractéristiques et de leurs stats
  private async getCharacteristics() {
    this.currentCharacs = (
      await getCharacteristics(this.caracteristicFilters)
    ).data.items;
  }

  // Descendre dans l'arborescence
  private AddBreadCrumbLevel(
    caracteristic_type_id: number | undefined,
    caracteristic_id: number | undefined
  ) {
    if (caracteristic_id !== undefined)
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: ICharacteristic) => t.characteristic_id == caracteristic_id
        )[0]
      );
    else if (caracteristic_type_id !== undefined)
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: ICharacteristicType) =>
            t.characteristic_type_id == caracteristic_type_id
        )[0]
      );
  }

  //  Remonter dans l'arborescence
  private MoveToBreadCrumb(index: number | undefined) {
    if (index === undefined) this.breadcrumbStack = [];
    else this.breadcrumbStack.splice(index + 1);
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.card-content {
  padding: 0px;
}

.sub-title {
  background-color: $primary;
}
.sub-title .card-header-title {
  color: white;
  text-transform: uppercase;
}
</style>