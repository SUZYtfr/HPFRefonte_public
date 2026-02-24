<template>
  <div class="card is-relative">
    <BLoading v-model="listLoading" :is-full-page="false" />
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">Filtres</p>
    </header>
    <div :class="['card-content', 'px-2', 'py-3']">
      <BField label="Rechercher un titre, un mot-clé..." label-position="on-border" custom-class="has-text-primary">
        <BInput v-model="(filters.title ??= {}).contains" placeholder="Rechercher..." type="search" icon="search" />
      </BField>
      <BField label="Rechercher un auteur" label-position="on-border" custom-class="has-text-primary">
        <BInput
          v-model="((filters.creationUser ??= {}).username! ??= {}).contains"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
      </BField>
      <BField label="Publiée après le" label-position="on-border" custom-class="has-text-primary">
        <BDatepicker
          v-model="(filters.postDate ??= {}).gt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(filters.postDate ??= {}).gt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(filters.postDate ??= {}).gt = undefined"
        />
      </BField>
      <BField label="Publiée avant le" label-position="on-border" custom-class="has-text-primary">
        <BDatepicker
          v-model="(filters.postDate ??= {}).lt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(filters.postDate ??= {}).lt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(filters.postDate ??= {}).lt = undefined"
        />
      </BField>
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
import type { NewsArticleFilters } from "#gql";

const { newsFilters, execute, isLoading } = defineProps<{
  newsFilters: NewsArticleFilters;
  isLoading: boolean;
  execute: () => void;
}>();

const filters = ref<NewsArticleFilters>(Object.assign({}, newsFilters));
const emit = defineEmits(["filtersChange"]);

watch(filters, () => emit("filtersChange", filters.value), { deep: true });

const listLoading = computed<boolean>(() => isLoading);
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
