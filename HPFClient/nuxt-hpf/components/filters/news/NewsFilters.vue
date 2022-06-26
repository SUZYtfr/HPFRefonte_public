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
          v-model="newsFilters.searchTerm"
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
          v-model="newsFilters.searchAuthor"
        >
        </b-input>
      </b-field>
      <b-field
        label="Publiée après le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="newsFilters.fromDate"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="newsFilters.fromDate ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="newsFilters.fromDate = null"
        >
        </b-datepicker>
      </b-field>
      <b-field
        label="Publiée avant le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="newsFilters.toDate"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="newsFilters.toDate ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="newsFilters.toDate = null"
        >
        </b-datepicker>
      </b-field>
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
import { Component, Vue, Prop } from "vue-property-decorator";
import { NewsFiltersData } from "~/types/news";

@Component({
  name: "NewsFilters",
})
export default class extends Vue {
  //#region Props
  @Prop() private newsFilters!: NewsFiltersData;
  @Prop({ default: false }) private loading!: boolean;
  //#endregion

  //#region Datas

  //#endregion

  //#region Hooks

  //#endregion

  //#region Methods

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


.z-index-zero {
  z-index: 0 !important;
}
</style>