<template>
  <div class="container px-5">
    <br>
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
            <b-loading v-model="listLoading" :is-full-page="false" />
            <!-- Breadcrumb -->
            <b-breadcrumb align="is-left" class="mb-0">
              <b-breadcrumb-item @click.native="MoveToBreadCrumb(undefined)">
                Accueil
              </b-breadcrumb-item>
              <b-breadcrumb-item
                v-for="(charac, innerindex) of breadcrumbStack"
                :key="innerindex"
                :index="innerindex"
                @click.native="MoveToBreadCrumb(innerindex)"
              >
                {{ charac.name }}
              </b-breadcrumb-item>
            </b-breadcrumb>
            <hr class="mt-1 mb-3">
            <!-- Liste -->
            <div
              v-if="currentCharacs.length > 0"
              class="columns is-multiline is-centered is-variable is-8"
            >
              <div
                v-for="(charac, innerindex) of currentCharacs"
                :key="innerindex"
                :index="innerindex"
                class="column is-4 is-4-desktop is-4-widescreen is-3-fullhd"
              >
                <TagPanel
                  :characteristic_type_id="
                    charac instanceof CharacteristicModel
                      ? charac.characteristic_type_id
                      : charac.characteristic_type_id
                  "
                  :characteristic_id="
                    charac instanceof CharacteristicModel ? charac.characteristic_id : null
                  "
                  :characteristic_name="charac.name"
                  :characteristic_description="charac.description"
                  :characteristic_count="charac.storiesCount"
                  @click="AddBreadCrumbLevel"
                />
              </div>
            </div>
            <div v-if="currentCharacs.length == 0">
              <FanfictionList
                :is-card="false"
                :fanfiction-filters="fanfictionFilters"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import TagPanel from "~/components/TagPanel.vue";
import { ConfigModule } from "@/utils/store-accessor";
import { ICharacteristicFilters } from "@/types/characteristics";
import {
  CharacteristicModel,
  CharacteristicTypeModel
} from "@/models/characteristics";
import { getCharacteristics } from "@/api/characteristics";
import { IFanfictionFilters } from "@/types/fanfictions";
import FanfictionList from "~/components/list/fanfictions/FanfictionList.vue";
import { SortByEnum } from "~/types/basics";

@Component({
  name: "Category",
  components: {
    TagPanel,
    FanfictionList
  },
  fetchOnServer: true
})
export default class extends Vue {
  // #region Data
  public breadcrumbStack: any[] = [];

  // Caractérisitiques affichés
  public currentCharacs: any[] = [];

  // Filtres des charactéristiques
  public caracteristicFilters: ICharacteristicFilters = {
    characteristic_type_id: null,
    parent_id: null,
    options: {
      with_stats: true
    },
    limit: 10
  };

  // Filtres
  public fanfictionFilters: IFanfictionFilters = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: 0,
    multipleAuthors: null,
    status: null,
    minWords: null,
    maxWords: null,
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: null,
    inclusive: false,
    fromDate: null,
    toDate: null,
    page: 1,
    pageSize: 10,
    totalPages: false,
    sortBy: SortByEnum.Descending,
    sortOn: "last_update_date"
  };

  public listLoading: boolean = false;
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des caractéristiques types
    await this.getCharacteristicsTypes();
    this.listLoading = false;
  }
  // #endregion

  // #region Watchers
  // @Watch("$fetchState.pending", { immediate: true, deep: false })
  // private onFetchChanged(): void {
  //   console.log("fetchstate:");
  //   console.log(this.$fetchState);
  //   if (this.$fetchState?.pending === false) {
  //   // Création des CharacteristicData instanciées
  //     this.currentCharacs = plainToInstance(
  //       CharacteristicTypeModel,
  //       this.currentCharacs
  //     );
  //     console.log(this.currentCharacs[0]);
  //     console.log(this.currentCharacs[0] instanceof CharacteristicTypeModel);
  //   }
  // }

  // Actualisation des résultats
  @Watch("breadcrumbStack")
  private async onPileChanged(): Promise<void> {
    this.listLoading = true;
    if (this.breadcrumbStack.length > 0) {
      const current = this.breadcrumbStack[this.breadcrumbStack.length - 1];
      if (current instanceof CharacteristicModel) {
        this.caracteristicFilters.characteristic_type_id =
          current.characteristic_type_id;
        this.caracteristicFilters.parent_id = current.characteristic_id;
      } else if (current instanceof CharacteristicTypeModel) {
        this.caracteristicFilters.characteristic_type_id = current.characteristic_type_id;
        this.caracteristicFilters.parent_id = null;
      }
      await this.getCharacteristics();
      // Si pas de nouvelle caractéristique, on est en bas de la pile on déclenche recherche les fictions
      if (this.currentCharacs.length === 0)
        this.fanfictionFilters.includedTags = [current.characteristic_id];
    } else {
      await this.getCharacteristicsTypes();
    }
    this.listLoading = false;
  }
  // #endregion

  // #region Methods
  // Récupération des caractéristiques types, depuis la config
  private async getCharacteristicsTypes(): Promise<void> {
    if (ConfigModule.characteristicTypes.length === 0)
      await ConfigModule.LoadConfig();
    this.currentCharacs = ConfigModule.characteristicTypes;
  }

  // Récupération des caractéristiques et de leurs stats
  private async getCharacteristics(): Promise<void> {
    this.currentCharacs = (
      await getCharacteristics(this.caracteristicFilters)
    ).items;
  }

  // Descendre dans l'arborescence
  public AddBreadCrumbLevel(
    caracteristic_type_id: number | undefined,
    caracteristic_id: number | undefined
  ): void {
    if (caracteristic_id !== null) {
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: CharacteristicModel) => t.characteristic_id === caracteristic_id
        )[0]
      );
    } else if (caracteristic_type_id !== null) {
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: CharacteristicTypeModel) => t.characteristic_type_id === caracteristic_type_id
        )[0]
      );
    }
  }

  //  Remonter dans l'arborescence
  public MoveToBreadCrumb(index: number | undefined): void {
    if (index === undefined) this.breadcrumbStack = [];
    else this.breadcrumbStack.splice(index + 1);
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.card-content {
  padding: 0px;
}
</style>
