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
        { 'fixed-height-card': isFixedHeightCard },
      ]"
    >
      <b-field
        label="Rechercher un titre, un mot-clé..."
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-input
          v-model="(fanfictionFilters.title ??= {}).contains"
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
          v-model="((fanfictionFilters.creationUser ??= {}).username ??= {}).contains"
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
          :custom-formatter="(val: number) => sliderCustomFormatter(val)"
          append-to-body
          ticks
        >
        <template
          v-for="val in sliderTicks"
          :key="val.displayValue"
        >
            <b-slider-tick
              :value="val.sliderValue"
              class="has-text-weight-semibold"
            >
              {{ val.displayValue }}
            </b-slider-tick>
          </template>
        </b-slider>
      </b-field>
      <!-- <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.status"
        :checked-value="4"
        :excluded-value="1"
        :unchecked-value="null"
        title="Histoires terminées"
        @change="fanfictionFilters.status = $event"
      /> -->
<!--       <ThreeStateCheckbox
        class="py-1 pl-1"
        :external-value="fanfictionFilters.multipleAuthors"
        title="Histoires co-écrites"
        @change="fanfictionFilters.multipleAuthors = $event"
      /> -->
      <ThreeStateCheckbox
        class="py-1 pl-1"
        :externalState="(fanfictionFilters.featured ??= {})?.exact"
        title="Histoires médaillés"
        @change="(fanfictionFilters.featured ??= {}).exact = $event"
      />
      <Panel
        name="Fandoms"
        class="my-2"
        :options="ConfigModule.fandoms?.map(f => { return {name: f.name, value: f.id} }) || []"
        :initial-included-values="fanfictionFilters.fandoms?.allIdsInList || []"
        :initial-excluded-values="fanfictionFilters.fandoms?.NOT?.id?.inList || []"
        @change="fandomsChanged"
      />
      <CharacteristicsPanel
        v-for="(type, index) in ConfigModule.characteristicTypes"
        :initial-included-ids
        :initial-excluded-ids
        :key="'tag_' + index.toString()"
        class="my-2"
        :characteristicType="type"
        :characteristics="filteredCharacteristics(type.characteristicTypeId)"
        @change="characteristicsChanged"
      />
<!--       <b-field
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
      </b-field> -->
      <b-field
        label="Publiée après le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="(fanfictionFilters.lastUpdateDate ??= {}).gt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(fanfictionFilters.lastUpdateDate ??= {}).gt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(fanfictionFilters.lastUpdateDate ??= {}).gt = null"
        />
      </b-field>
      <b-field
        label="Publiée avant le"
        label-position="on-border"
        custom-class="has-text-primary"
      >
        <b-datepicker
          v-model="(fanfictionFilters.lastUpdateDate ??= {}).lt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(fanfictionFilters.lastUpdateDate ??= {}).lt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(fanfictionFilters.lastUpdateDate ??= {}).lt = null"
        />
      </b-field>
      <!-- <b-switch
        v-model="fanfictionFilters.inclusive"
        class="ml-1"
        :rounded="false"
      >
        Recherche inclusive
      </b-switch> -->
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
          <a @click.prevent.stop="execute">Rechercher</a>
        </span>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { groupBy } from "@/utils/es6-utils";
import type { FictionFilters } from "#gql";
import { CharacteristicModel, CharacteristicTypeModel } from "@/models";

interface Props {
  fanfictionFilters: FictionFilters;
  initialIncludedIds: number[];
  initialExcludedIds: number[];
  isLoading?: boolean;
  isFixedHeightCard?: boolean;
  tooltipPosition?: string;
  execute: () => {};
}

const {
  fanfictionFilters,
  isLoading = false,
  isFixedHeightCard = false,
  tooltipPosition = "is-right",
} = defineProps<Props>();

const listLoading = computed<boolean>(() => isLoading);

const sliderTicks = [
  { sliderValue: 1, realValue: 500, displayValue: "<500" },
  { sliderValue: 2, realValue: 1000, displayValue: "1k" },
  { sliderValue: 3, realValue: 5000, displayValue: "5k" },
  { sliderValue: 4, realValue: 10000, displayValue: "10k" },
  { sliderValue: 5, realValue: 50000, displayValue: "50k" },
  { sliderValue: 6, realValue: 100000, displayValue: ">100k" }
];

const sliderWords = ref<number[]>([1, 6]);

const ConfigModule = useConfigStore();

/* watch(sliderWords, () => {
  if (fanfictionFilters == null) return;
  fanfictionFilters.wordCount_min = sliderTicks[sliderWords.value[0] - 1]?.realValue ?? null;
  fanfictionFilters.wordCount_max = sliderTicks[sliderWords.value[1] - 1]?.realValue ?? null;
  // Valeurs min et max -> null
  if (fanfictionFilters.wordCount_min === 500) fanfictionFilters.wordCount_min = null;
  if (fanfictionFilters.wordCount_max === 100000) fanfictionFilters.wordCount_max = null;
}); */

function sliderCustomFormatter(sliderValue: number): string {
  let result = "";
  if (sliderValue === 1) result += "< ";
  if (sliderValue === 6) result += "> ";
  result += sliderTicks[sliderValue - 1]?.realValue;
  return result + " mots";
}

function filteredCharacteristics(characteristicTypeId: number): CharacteristicModel[] {
    const itemsSorted: CharacteristicModel[] = ConfigModule.characteristics!
        .filter(
            (t: CharacteristicModel) =>
                t.characteristicTypeId.toString() === characteristicTypeId.toString() &&
                t.parentId == null
        )
        .sort((a: CharacteristicModel, b: CharacteristicModel) => {
            return a.order - b.order;
        });
    groupBy(
        ConfigModule.characteristics!.filter(
            (t: CharacteristicModel) =>
                t.characteristicTypeId.toString() === characteristicTypeId.toString()
        ),
        (g: CharacteristicModel) => g.parentId
    ).forEach((value: CharacteristicModel[], key: number) => {
        if (key != null) {
            const index = itemsSorted.findIndex(c => c.characteristicId.toString() === key.toString());
        if (index === -1) itemsSorted.splice(0, 0, ...value);
            else itemsSorted.splice(index + 1, 0, ...value);
        }
    });
    return itemsSorted;
}

function fandomsChanged(fandomId: string, action: boolean | null) {
  let newIncluded = ((fanfictionFilters.fandoms ??= {}).allIdsInList || []).filter(t => t !== fandomId.toString());
  let newExcluded = ((((fanfictionFilters.fandoms ??= {}).NOT ??= {}).id ??= {}).inList || []).filter(t => t !== fandomId.toString());

  switch (action) {
    case true:
      newIncluded = newIncluded.concat(fandomId.toString());
      break;
    case false:
      newExcluded = newExcluded.concat(fandomId.toString());
      break;
    default:
      break;
  }
  
  fanfictionFilters.fandoms = {
    allIdsInList: newIncluded.length > 0 ? newIncluded : null,
    NOT: {
      id: {
        inList: newExcluded.length > 0 ? newExcluded : null
      }
    }
  }
}

function characteristicsChanged(characteristicId: number, action: boolean | null) {
  let newIncluded = ((fanfictionFilters.characteristics ??= {}).allIdsInList || []).filter(t => t !== characteristicId.toString());
  let newExcluded = ((((fanfictionFilters.characteristics ??= {}).NOT ??= {}).id ??= {}).inList || []).filter(t => t !== characteristicId.toString());

  switch (action) {
    case true:
      newIncluded = newIncluded.concat(characteristicId.toString());
      break;
    case false:
      newExcluded = newExcluded.concat(characteristicId.toString());
      break;
    default:
      break;
  }
  
  fanfictionFilters.characteristics = {
    allIdsInList: newIncluded.length > 0 ? newIncluded : null,
    NOT: {
      id: {
        inList: newExcluded.length > 0 ? newExcluded : null
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

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