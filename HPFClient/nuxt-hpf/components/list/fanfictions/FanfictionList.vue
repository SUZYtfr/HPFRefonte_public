<template>
  <div :class="[{'card': isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <b-loading v-model="listLoading" :is-full-page="false" />
    <header
      :class="[
        {'card-header': isCard },
        'p-2',
        'is-flex', 'is-flex-direction-row', 'is-align-items-center'
      ]"
    >
      <div class="is-flex-grow-5 p-0 m-0 mr-2">
        <b-button
          v-if="showRefreshButton"
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
            @input="SelectSortBy_OnInputChanged"
          >
            <option value="alpha">
              Ordre alphabétique
            </option>
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
            <option value="most_rating">
              Rating - croissant
            </option>
            <option value="less_rating">
              Rating - décroissant
            </option>
          </b-select>
        </b-field>
      </div>
    </header>
    <div :class="[{'card-content': isCard }, 'px-2', 'py-3', 'is-flex-grow-5']">
      <div
        v-if="(fanfictions?.length ?? 0) == 0"
        class="mx-auto my-auto has-text-centered"
      >
        <span class="is-italic mt-3">Aucun résultat, essayer d'ajuster les filtres de recherche.</span>
      </div>
      <div v-else>
        <Fanfiction
          v-for="(fanfiction, innerindex) of fanfictions"
          :key="'ff_' + fanfiction.fanfiction_id.toString()"
          class="my-2"
          :fanfiction="fanfiction"
          :index="innerindex"
        />
      </div>
    </div>
    <footer :class="[{'card-footer':isCard}]">
      <b-pagination
        v-model="fanfictionFilters.page"
        :class="[{'card-footer-item': isCard}, 'py-2']"
        :total="fanfictions?.length ?? 1"
        :range-before="3"
        :range-after="1"
        :rounded="false"
        :per-page="fanfictionFilters.pageSize"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
      />
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import Fanfiction from "~/components/Fanfiction.vue";
import { IFanfictionFilters } from "@/types/fanfictions";
import { FanfictionModel } from "@/models/fanfictions";
import { searchFanfictions } from "@/api/fanfictions";
import { SortByEnum } from "~/types/basics";

@Component({
  name: "FanfictionList",
  components: {
    Fanfiction
  },
  fetchOnServer: true,
  fetchKey: "fanfiction-list"
})
export default class FanfictionList extends Vue {
  // #region Props
  @Prop({ default: true }) public isCard!: boolean;
  @Prop({ default: true }) public showRefreshButton!: boolean;
  @Prop({ default: false }) private isLoading!: boolean;
  @Prop() public fanfictionFilters!: IFanfictionFilters;
  // #endregion

  // #region Data
  @SerialiseClass(FanfictionModel)
  public fanfictions: FanfictionModel[] = [];

  private timerId: number = 0;
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.listLoading = true;
    // Récupération des fictions
    await this.getFanfictions();
    this.listLoading = false;
  }
  // #endregion

  // #region Computed
  get fanfictionResultLabel(): string {
    let result = "Aucun résultat";
    if (this.fanfictions == null || this.fanfictions.length === 0) return result;
    result = this.fanfictions.length.toString() + " résultat";
    result += this.fanfictions.length > 1 ? "s" : "";
    return result;
  }

  get listLoading(): boolean {
    return this.isLoading;
  }

  set listLoading(value) {
    this.$emit("loadingChange", value);
  }
  // #endregion

  // #region Watchers
  @Watch("fanfictionFilters", { deep: true })
  public onFiltersChanged(): void {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.$fetch, 500);
  }
  // #endregion

  // #region Hooks
  mounted(): void {
    // Déclenche une recherche à l'affichage
    // clearTimeout(this.timerId);
    // this.timerId = window.setTimeout(this.$fetch, 500);
  }
  // #endregion

  // #region Methods
  private async getFanfictions(): Promise<void> {
    // this.listLoading = true;
    try {
      this.fanfictions = (await searchFanfictions(this.fanfictionFilters)).items;
      // console.log("Fanfiction type: " + (this.fanfictions[0] instanceof FanfictionModel));
      // console.log("Date type: " + ((new Date()) instanceof Date));
      // console.log("Creation date type: " + (this.fanfictions[0].creation_date instanceof Date));
      // console.log("Last update date type: " + (this.fanfictions[0].last_update_date instanceof Date));
      // console.log("Characteristic type: " + (this.fanfictions[0].characteristics[0] instanceof CharacteristicData));
      // console.log(this.fanfictions[0]?.creation_date);
      // console.log(new Date(this.fanfictions[0]?.creation_date));
      // console.log(new Date(this.fanfictions[0]?.creation_date).toLocaleDateString());
      // console.log(this.fanfictions[0].creation_date?.toLocaleDateString());
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération des fictions",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    } finally {
      // this.listLoading = false;
    }
  }

  public SelectSortBy_OnInputChanged(value: string): void {
    switch (value) {
      case "alpha":
        this.fanfictionFilters.sortBy = SortByEnum.Ascending;
        this.fanfictionFilters.sortOn = "title";
        break;
      case "most_recent":
        this.fanfictionFilters.sortBy = SortByEnum.Descending;
        this.fanfictionFilters.sortOn = "last_update_date";
        break;
      case "less_recent":
        this.fanfictionFilters.sortBy = SortByEnum.Ascending;
        this.fanfictionFilters.sortOn = "last_update_date";
        break;
      case "most_reviews":
        this.fanfictionFilters.sortBy = SortByEnum.Descending;
        this.fanfictionFilters.sortOn = "comments";
        break;
      case "less_reviews":
        this.fanfictionFilters.sortBy = SortByEnum.Ascending;
        this.fanfictionFilters.sortOn = "comments";
        break;
      case "most_rating":
        this.fanfictionFilters.sortBy = SortByEnum.Ascending;
        this.fanfictionFilters.sortOn = "rating";
        break;
      case "less_rating":
        this.fanfictionFilters.sortBy = SortByEnum.Ascending;
        this.fanfictionFilters.sortOn = "rating";
        break;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>
