<template>
  <div class="card is-relative">
    <BLoading v-model="isLoading" :is-full-page="false" />
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">Filtres</p>
    </header>
    <div :class="['card-content', 'px-2', 'py-3', { 'fixed-height-card': isFixedHeightCard }]">
      <BField label="Rechercher un titre, un mot-clé..." label-position="on-border" custom-class="has-text-primary">
        <BInput v-model="(filters.title ??= {}).contains" placeholder="Rechercher..." type="search" icon="search" />
      </BField>
      <BField label="Rechercher un auteur" label-position="on-border" custom-class="has-text-primary">
        <BInput
          v-model="((filters.creationUser ??= {}).username ??= {}).contains"
          placeholder="Rechercher..."
          type="search"
          icon="search"
        />
      </BField>
      <BField label="Nombre de mots" label-position="on-border" custom-class="has-text-primary z-index-zero">
        <BSlider
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
          <template v-for="val in sliderTicks" :key="val.displayValue">
            <BSliderTick :value="val.sliderValue" class="has-text-weight-semibold">
              {{ val.displayValue }}
            </BSliderTick>
          </template>
        </BSlider>
      </BField>
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
        :external-state="(filters.featured ??= {})?.exact"
        title="Histoires médaillés"
        @change="(filters.featured ??= {}).exact = $event"
      />
      <Panel
        name="Fandoms"
        class="my-2"
        :options="
          ConfigModule.fandoms?.map((f) => {
            return { name: f.name, value: f.id };
          }) || []
        "
        :initial-included-values="filters.fandoms?.allIdsInList || []"
        :initial-excluded-values="filters.fandoms?.NOT?.id?.inList || []"
        @change="fandomsChanged"
      />
      <CharacteristicPanel
        v-for="(type, index) in ConfigModule.characteristicTypes"
        :key="'tag_' + index.toString()"
        :initial-included-ids
        :initial-excluded-ids
        class="my-2"
        :characteristic-type="type"
        :characteristics="filteredCharacteristics(type.characteristicTypeId)"
        @change="characteristicsChanged"
      />
      <!--       <BField
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
      </BField> -->
      <BField label="Publiée après le" label-position="on-border" custom-class="has-text-primary">
        <BDatepicker
          v-model="(filters.lastUpdateDate ??= {}).gt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(filters.lastUpdateDate ??= {}).gt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(filters.lastUpdateDate ??= {}).gt = null"
        />
      </BField>
      <BField label="Publiée avant le" label-position="on-border" custom-class="has-text-primary">
        <BDatepicker
          v-model="(filters.lastUpdateDate ??= {}).lt"
          locale="fr-FR"
          placeholder="Sélectionner une date"
          append-to-body
          icon="calendar-alt"
          :first-day-of-week="1"
          :icon-right="(filters.lastUpdateDate ??= {}).lt ? 'times-circle' : ''"
          :icon-right-clickable="true"
          @icon-right-click="(filters.lastUpdateDate ??= {}).lt = null"
        />
      </BField>
      <!-- <b-switch
        v-model="fanfictionFilters.inclusive"
        class="ml-1"
        :rounded="false"
      >
        Recherche inclusive
      </b-switch> -->
      <BTooltip :position="tooltipPosition" type="is-primary" append-to-body multilined>
        <BIcon pack="fas" class="is-clickable" type="is-primary" icon="question-circle" />
        <template #content>
          <p>
            <strong class="has-text-white">Activé:</strong> Recherche les fictions Aventure/Action
            <strong class="has-text-white"><em>ET</em></strong>
            Comédie/Humour.
          </p>
          <p>
            <strong class="has-text-white">Désactivé:</strong> Recherche les fictions Aventure/Action
            <strong class="has-text-white"><em>OU</em></strong>
            Comédie/Humour.
          </p>
        </template>
      </BTooltip>
    </div>
    <footer class="card-footer">
      <p class="card-footer-item py-2">
        <span>
          <a @click.prevent.stop="searchFictions">Rechercher</a>
        </span>
      </p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { groupBy } from "~/utils/es6-utils";
import type { FictionFilters } from "#gql";
import type { CharacteristicModel } from "~/models";

// NOTE - C'est quand même fou qu'on puisse pas extraire le type de prop d'un composant Buefy...
type TooltipPosition = "is-left" | "is-right" | "is-top" | "is-bottom" | "is-auto" | undefined;

interface Props {
  initialIncludedIds?: number[];
  initialExcludedIds?: number[];
  isFixedHeightCard?: boolean;
  tooltipPosition?: TooltipPosition;
  searchFictions: () => Promise<void>;
}

const { isFixedHeightCard = false, tooltipPosition = "is-right" } = defineProps<Props>();

const filters = defineModel<FictionFilters>("filters", { required: true });
const isLoading = defineModel<boolean>("isLoading", { required: false, default: false });

const sliderTicks = [
  { sliderValue: 1, realValue: 500, displayValue: "<500" },
  { sliderValue: 2, realValue: 1000, displayValue: "1k" },
  { sliderValue: 3, realValue: 5000, displayValue: "5k" },
  { sliderValue: 4, realValue: 10000, displayValue: "10k" },
  { sliderValue: 5, realValue: 50000, displayValue: "50k" },
  { sliderValue: 6, realValue: 100000, displayValue: ">100k" },
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
  const itemsSorted: CharacteristicModel[] = ConfigModule.characteristics!.filter(
    (t: CharacteristicModel) =>
      t.characteristicTypeId.toString() === characteristicTypeId.toString() && t.parentId == null,
  ).sort((a: CharacteristicModel, b: CharacteristicModel) => {
    return a.order - b.order;
  });
  groupBy(
    ConfigModule.characteristics!.filter(
      (t: CharacteristicModel) => t.characteristicTypeId.toString() === characteristicTypeId.toString(),
    ),
    (g: CharacteristicModel) => g.parentId,
  ).forEach((value: CharacteristicModel[], key: number) => {
    if (key != null) {
      const index = itemsSorted.findIndex((c) => c.characteristicId.toString() === key.toString());
      if (index === -1) itemsSorted.splice(0, 0, ...value);
      else itemsSorted.splice(index + 1, 0, ...value);
    }
  });
  return itemsSorted;
}

function fandomsChanged(fandomId: string, action: boolean | null): void {
  let newIncluded = ((filters.value.fandoms ??= {}).allIdsInList || []).filter((t) => t !== fandomId.toString());
  let newExcluded = ((((filters.value.fandoms ??= {}).NOT ??= {}).id ??= {}).inList || []).filter(
    (t) => t !== fandomId.toString(),
  );

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

  filters.value.fandoms = {
    allIdsInList: newIncluded.length > 0 ? newIncluded : null,
    NOT: {
      id: {
        inList: newExcluded.length > 0 ? newExcluded : null,
      },
    },
  };
}

function characteristicsChanged(characteristicId: number, action: boolean | null): void {
  let newIncluded = ((filters.value.characteristics ??= {}).allIdsInList || []).filter(
    (t) => t !== characteristicId.toString(),
  );
  let newExcluded = ((((filters.value.characteristics ??= {}).NOT ??= {}).id ??= {}).inList || []).filter(
    (t) => t !== characteristicId.toString(),
  );

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

  filters.value.characteristics = {
    allIdsInList: newIncluded.length > 0 ? newIncluded : null,
    NOT: {
      id: {
        inList: newExcluded.length > 0 ? newExcluded : null,
      },
    },
  };
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
  overflow-y: scroll;
}

.z-index-zero {
  z-index: 0 !important;
}
</style>
