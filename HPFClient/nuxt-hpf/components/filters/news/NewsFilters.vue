<template>
  <div class="card is-relative">
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
      ]"
    >
      <b-field
        label="Rechercher un titre, un mot-clé..."
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-input
          v-model="newsFilters.searchTerm"
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
          v-model="newsFilters.searchAuthor"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
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
        />
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
        />
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

<script setup lang="ts">
import { INewsFilters } from "~/types/news";

const { newsFilters } = defineProps<{
  newsFilters: INewsFilters
}>()

// Déclencher le Watcher des filtres sur le clique recherche
function toggleFilterChanged(): void {
  newsFilters.searchTerm = newsFilters.searchTerm + " ";
  newsFilters.searchTerm = newsFilters.searchTerm.slice(
    0,
    -1
  );
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.card {
  overflow: hidden;
}

.card-content {
  padding: 0px;
}

.z-index-zero {
  z-index: 0 !important;
}
</style>
