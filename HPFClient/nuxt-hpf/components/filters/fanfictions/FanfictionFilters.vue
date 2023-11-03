<template>
  <div class="card is-relative">
    <b-loading v-model="loading" :is-full-page="false" />
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
        { 'fixed-height-card': isFixedHeightCard },
      ]"
    >
      <b-field
        label="Rechercher un titre, un mot-clé..."
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-input
          v-model="fanfictionFilters.searchTerm"
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
          v-model="fanfictionFilters.searchAuthor"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
      </b-field>
      <b-field
        label="Nombre de mots"
        label-position="on-border"
        custom-class="has-text-primary z-index-zero"
      >
        <b-slider
          v-model="sliderWords"
          type="is-primary"
          class="px-4 pt-4 pb-3"
          :min="1"
          :max="6"
          :step="1"
          lazy
          :custom-formatter="(val: number | null) => sliderCustomFormatter(val)"
          append-to-body
          ticks
        >
          <template v-for="val in sliderTicks" :key="val.displayValue">
            <b-slider-tick
              :value="val.sliderValue"
              class="has-text-weight-semibold"
            >
              {{ val.displayValue }}
            </b-slider-tick>
          </template>
        </b-slider>
      </b-field>
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.finished"
        title="Histoires terminées"
        @change="fanfictionFilters.finished = $event"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.multipleAuthors"
        title="Histoires co-écrites"
        @change="fanfictionFilters.multipleAuthors = $event"
      />
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.featured"
        title="Histoires médaillés"
        @change="fanfictionFilters.featured = $event"
      />
      <CharacteristicPanel
        v-for="(type, index) in characteristics_types"
        :key="'tag_' + index.toString()"
        class="my-2"
        :characteristic_type="type"
        :characteristics="filteredCharacteristics(type.characteristic_type_id)"
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
          class="mt-4"
          @typing="getFilteredTags"
        />
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
        />
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
        />
      </b-field>
      <b-switch
        v-model="fanfictionFilters.inclusive"
        class="ml-1"
        :rounded="false"
      >
        Recherche inclusive
      </b-switch>
      <b-tooltip
        :position="tooltipPosition"
        type="is-primary"
        append-to-body
        multilined
      >
        <b-icon
          pack="fas"
          class="is-clickable"
          type="is-primary"
          icon="question-circle"
        />
        <template #content>
          <p>
            <strong class="has-text-white">Activé:</strong> Recherche les
            fictions Aventure/Action
            <strong class="has-text-white"><em>ET</em></strong>
            Comédie/Humour.
          </p>
          <p>
            <strong class="has-text-white">Désactivé:</strong> Recherche les
            fictions Aventure/Action
            <strong class="has-text-white"><em>OU</em></strong>
            Comédie/Humour.
          </p>
        </template>
      </b-tooltip>
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
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";
import CharacteristicPanel from "@/components/CharacteristicPanel.vue";
import { IFanfictionFilters } from "~/types/fanfictions";
import { groupBy } from "@/utils/es6-utils";
import { CharacteristicModel, CharacteristicTypeModel } from "~/models/characteristics";
import { getCharacteristics, getCharacteristicsTypes } from "~/api/characteristics";

interface FanfictionFiltersProps {
  fanfictionFilters: IFanfictionFilters
  loading?: boolean
  isFixedHeightCard?: boolean
  tooltipPosition?: string
}
const { fanfictionFilters, loading, isFixedHeightCard, tooltipPosition } = withDefaults(defineProps<FanfictionFiltersProps>(), {
  loading: false,
  isFixedHeightCard: false,
  tooltipPosition: "is-right"
})

const sliderTicks = [
  { sliderValue: 1, realValue: 500, displayValue: "<500" },
  { sliderValue: 2, realValue: 1000, displayValue: "1k" },
  { sliderValue: 3, realValue: 5000, displayValue: "5k" },
  { sliderValue: 4, realValue: 10000, displayValue: "10k" },
  { sliderValue: 5, realValue: 50000, displayValue: "50k" },
  { sliderValue: 6, realValue: 100000, displayValue: ">100k" }
];

const sliderWords: Ref<number[]> = ref([1, 6])

watch(sliderWords, (value) => {
  fanfictionFilters.wordCount_min = sliderTicks[value[0] - 1].realValue;
  fanfictionFilters.wordCount_max = sliderTicks[value[1] - 1].realValue;
  // Valeurs min et max -> null
  if (fanfictionFilters.wordCount_min === 500) fanfictionFilters.wordCount_min = null;
  if (fanfictionFilters.wordCount_max === 100000) fanfictionFilters.wordCount_max = null;
})

function sliderCustomFormatter(sliderValue: number | null): string {
  let result = "";
  if (sliderValue) {
    if (sliderValue === 1) result += "< ";
    if (sliderValue === 6) result += "> ";
    result += sliderTicks[sliderValue - 1].realValue;
    return result + " mots";
  } else {
    return result
  }
}

// TODO - remettre dans un store / plugin
const { data: characteristics } = await getCharacteristics(null)
const { data: characteristics_types } = await getCharacteristicsTypes()
const filteredTags: CharacteristicModel[] = []

function filteredCharacteristics(characteristic_type_id: number): CharacteristicModel[] {
  const itemsSorted: CharacteristicModel[] = characteristics.value
    .filter(
      (t: CharacteristicModel) =>
        t.characteristic_type_id === characteristic_type_id &&
        t.parent_id == null
    )
    .sort((a: CharacteristicModel, b: CharacteristicModel) => {
      return a.order - b.order;
    });
  groupBy(
    characteristics.value.filter(
      (t: CharacteristicModel) =>
        t.characteristic_type_id === characteristic_type_id
    ),
    (g: CharacteristicModel) => g.parent_id
  ).forEach((value: CharacteristicModel[], key: number) => {
    if (key != null) {
      const index = itemsSorted.findIndex(c => c.id === key);
      if (index === -1) itemsSorted.splice(0, 0, ...value);
      else itemsSorted.splice(index + 1, 0, ...value);
    }
  });
  return itemsSorted;
}

// Récupération des tags utilisateurs
async function getFilteredTags(text: string): Promise<void> {
  // this.filteredTags =
}

// Mise à jour des filtres des caractéristiques incluses / excluses
function characteristicsChanged(
  allIds: Set<number>,
  includedIds: number[],
  excludedIds: number[]
): void {
  fanfictionFilters.excludedTags = fanfictionFilters.excludedTags.filter(excludedId => !allIds.has(excludedId));
  fanfictionFilters.excludedTags = fanfictionFilters.excludedTags.concat(excludedIds);
  fanfictionFilters.includedTags = fanfictionFilters.includedTags.filter(includedId => !allIds.has(includedId));
  fanfictionFilters.includedTags = fanfictionFilters.includedTags.concat(includedIds);
}

// Déclencher le Watcher des filtres sur le clique recherche
function toggleFilterChanged(): void {
  fanfictionFilters.searchTerm = fanfictionFilters.searchTerm + " ";
  fanfictionFilters.searchTerm = fanfictionFilters.searchTerm.slice(0, -1);
}
// #endregion
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.card {
  overflow: hidden;
}

.card-content {
  padding: 0px;
}

.fixed-height-card {
  height: 70vh;
  overflow-y: scroll
}

.z-index-zero {
  z-index: 0 !important;
}
</style>
