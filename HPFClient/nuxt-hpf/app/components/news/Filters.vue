<template>
  <div class="card is-relative">
    <b-loading v-model="listLoading" :is-full-page="false" />
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
          v-model="(newsFilters.title ??= {}).contains"
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
          v-model="((newsFilters.creationUser ??= {}).username! ??= {}).contains"
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
          v-model="(newsFilters.postDate ??= {}).gt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(newsFilters.postDate ??= {}).gt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(newsFilters.postDate ??= {}).gt = undefined"
        />
      </b-field>
      <b-field
        label="Publiée avant le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="(newsFilters.postDate ??= {}).lt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(newsFilters.postDate ??= {}).lt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(newsFilters.postDate ??= {}).lt = undefined"
        />
      </b-field>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <a @click.prevent.stop="execute">Rechercher</a>
        </span>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import type { NewsArticleFilters } from '#gql';

const { newsFilters, execute, isLoading } = defineProps<{
    newsFilters: NewsArticleFilters;
    isLoading: boolean,
    execute: () => {};
}>();

const listLoading = computed<boolean>(() => isLoading );

</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

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