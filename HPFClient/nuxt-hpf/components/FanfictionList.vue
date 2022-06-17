<template>
  <div :class="[{'card': isCard }, 'is-flex', 'is-flex-direction-column', 'is-relative', 'fullheight']">
    <b-loading :is-full-page="false" v-model="listLoading"></b-loading>
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
    </header>
    <div :class="[{'card-content': isCard }, 'px-2', 'py-3', 'is-flex-grow-5']">
      <div
        v-if="fanfictions.length == 0"
        class="mx-auto my-auto has-text-centered"
      >
        <span class="is-italic mt-3"
          >Aucun résultat, essayer d'ajuster les filtres de recherche.</span
        >
      </div>
      <div v-else>
        <Fanfiction
          class="my-2"
          v-for="(fanfiction, innerindex) of fanfictions"
          :fanfiction="fanfiction"
          v-bind:index="innerindex"
          v-bind:key="'ff_' + fanfiction.fanfiction_id.toString()"
        ></Fanfiction>
      </div>
    </div>
    <footer :class="[{'card-footer':isCard}]">
      <b-pagination
        :class="[{'card-footer-item': isCard}, 'py-2']"
        :total="fanfictions.length"
        v-model="fanfictionFilters.currentPage"
        :range-before="rangeBefore"
        :range-after="rangeAfter"
        :rounded="false"
        :per-page="fanfictionFilters.perPage"
        icon-prev="chevron-left"
        icon-next="chevron-right"
        aria-next-label="Page suivante"
        aria-previous-label="Page précedente"
        aria-page-label="Page"
        aria-current-label="Page actuelle"
      >
      </b-pagination>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import Fanfiction from "~/components/Fanfiction.vue";
import { FanfictionFiltersData, FanfictionData } from "@/types/fanfictions";
import { getFanfictions } from "@/api/fanfictions";

@Component({
  name: "FanfictionList",
  components: {
    Fanfiction,
  },
})
export default class FanfictionList extends Vue {
  //#region Props
  @Prop({ default: true }) private isCard!: boolean;
  @Prop({ default: true }) private showRefreshButton!: boolean;
  @Prop({ default: false }) private listLoading!: boolean;
  @Prop() private fanfictionFilters!: FanfictionFiltersData;
  //#endregion

  //#region Data
  private fanfictions: FanfictionData[] = [];
  private timerId: number = 0;

  // Pagination
  private rangeBefore: number = 3;
  private rangeAfter: number = 1;
  //#endregion

  //#region Computed
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

  //#region Watchers
  @Watch("fanfictionFilters", { deep: true })
  private onFiltersChanged() {
    clearTimeout(this.timerId);
    this.timerId = window.setTimeout(this.getFanfictions, 500);
  }

  @Watch("listLoading", { deep: true })
  private onlistLoadingChanged() {
    this.$emit("isLoading", this.listLoading);
  }
  //#endregion

  //#region Methods
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
  //#endregion
}
</script>

<style lang="scss" scoped>
.fullheight {
  height: 100%;
}
</style>