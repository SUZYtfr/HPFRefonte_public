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
              v-if="(currentCharacs?.length ?? 0) > 0"
              class="columns is-multiline is-centered is-variable is-8"
            >
              <div
                v-for="(charac, innerindex) of currentCharacs"
                :key="innerindex"
                :index="innerindex"
                class="column is-4 is-4-desktop is-4-widescreen is-3-fullhd"
              >
                <TagPanel
                  :characteristicTypeId="
                    charac instanceof CharacteristicModel
                      ? charac.characteristicTypeId
                      : charac.characteristicTypeId
                  "
                  :characteristicId="
                    charac instanceof CharacteristicModel ? charac.characteristicId : null
                  "
                  :characteristic_name="charac.name"
                  :characteristic_description="charac.description"
                  :characteristic_count="charac.fictionCount"
                  @click="AddBreadCrumbLevel"
                />
              </div>
            </div>
            <div v-if="(currentCharacs?.length ?? 0) == 0">
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
import { getModule } from "vuex-module-decorators";
import Config from "~/store/modules/Config";
import TagPanel from "~/components/TagPanel.vue";
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
    characteristicTypeId: null,
    parentId: null
  };

  // Filtres
  public fanfictionFilters: IFanfictionFilters = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: null,
    multipleAuthors: null,
    status: null,
    wordCount_min: null,
    wordCount_max: null,
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
    sortOn: "lastUpdateDate"
  };

  public listLoading: boolean = false;
  // #endregion

  // #region Computed
  get ConfigModule(): Config {
    return getModule(Config, this.$store);
  }
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
        this.caracteristicFilters.characteristicTypeId =
          current.characteristicTypeId;
        this.caracteristicFilters.parentId = current.characteristicId;
      } else if (current instanceof CharacteristicTypeModel) {
        this.caracteristicFilters.characteristicTypeId = current.characteristicTypeId;
        this.caracteristicFilters.parentId = null;
      }
      await this.getCharacteristics();
      // Si pas de nouvelle caractéristique, on est en bas de la pile on déclenche recherche les fictions
      if ((this.currentCharacs?.length ?? 0) === 0)
        this.fanfictionFilters.includedTags = [current.characteristicId];
      console.log(this.fanfictionFilters);
    } else {
      await this.getCharacteristicsTypes();
    }
    this.listLoading = false;
  }
  // #endregion

  // #region Methods
  // Récupération des caractéristiques types, depuis la config
  private async getCharacteristicsTypes(): Promise<void> {
    if (this.ConfigModule.characteristicTypes.length === 0)
      await this.ConfigModule.LoadConfig();
    this.currentCharacs = this.ConfigModule.characteristicTypes;
    if (this.currentCharacs == null || this.currentCharacs.length === 0) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des catégories",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log("Une erreur s'est produite lors de la récupération des catégories");
      }
    }
  }

  // Récupération des caractéristiques et de leurs stats
  private async getCharacteristics(): Promise<void> {
    try {
      this.currentCharacs = (
        await getCharacteristics(this.caracteristicFilters)
      );
      console.log(this.currentCharacs);
    } catch (error) {
      this.currentCharacs = [];

      // if (process.client) {
      //   this.$buefy.snackbar.open({
      //     duration: 5000,
      //     message: "Une erreur s'est produite lors de la récupération des catégories",
      //     type: "is-danger",
      //     position: "is-bottom-right",
      //     actionText: null,
      //     pauseOnHover: true,
      //     queue: true
      //   });
      // } else {
      //   console.log(error);
      // }
    }
  }

  // Descendre dans l'arborescence
  public AddBreadCrumbLevel(
    caracteristic_type_id: number | undefined,
    caracteristic_id: number | undefined
  ): void {
    if (caracteristic_id !== null) {
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: CharacteristicModel) => t.characteristicId === caracteristic_id
        )[0]
      );
    } else if (caracteristic_type_id !== null) {
      this.breadcrumbStack.push(
        this.currentCharacs.filter(
          (t: CharacteristicTypeModel) => t.characteristicTypeId === caracteristic_type_id
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
