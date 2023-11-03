<template>
  <div>
    <div class="columns my-0">
      <div class="column pt-0">
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
      </div>
      <div class="column is-6 pt-0">
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
      </div>
    </div>
    <div class="columns mt-0">
      <div class="column is-6 pt-0">
        <b-field
          label="Inclure des personnages, catégories, genres, époques..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-taginput
            ref="includedTags"
            v-model="includedTagsFull"
            :data="filteredCharacteristics"
            autocomplete
            :open-on-focus="true"
            field="name"
            icon="plus-square"
            placeholder="Inclure des personnages, catégories, genres, époques..."
            group-field="type"
            group-options="items"
            @typing="getFilteredTags"
            @input="tagInput"
          >
            <template #default="props">
              <span class="is-italic has-text-weight-light">{{
                getFullPath(props.option)
              }}</span><span class="has-text-weight-semibold">{{
                props.option.name
              }}</span>
            </template>
            <template #empty>
              Aucun résultat
            </template>
            <template #selected="props">
              <b-tag
                v-for="(tag, index) in props.tags"
                :key="index"
                :class="getClassTypeColor(tag)"
                :tabstop="false"
                closable
                @close="$refs.includedTags?.removeTag(index, $event)"
              >
                {{ tag.name }}
              </b-tag>
            </template>
          </b-taginput>
        </b-field>
      </div>
      <div class="column is-6 pt-0">
        <b-field
          label="Exclure des personnages, catégories, genres, époques..."
          label-position="on-border"
          custom-class="has-text-primary"
        >
          <b-taginput
            ref="excludedTags"
            v-model="excludedTagsFull"
            :data="filteredCharacteristics"
            autocomplete
            :open-on-focus="true"
            field="name"
            icon="minus-square"
            placeholder="Exclure des personnages, catégories, genres, époques..."
            group-field="type"
            group-options="items"
            @typing="getFilteredTags"
            @input="tagInput"
          >
            <template #default="props">
              <span class="is-italic has-text-weight-light">{{
                getFullPath(props.option)
              }}</span><span class="has-text-weight-semibold">{{
                props.option.name
              }}</span>
            </template>
            <template #empty>
              Aucun résultat
            </template>
            <template #selected="props">
              <b-tag
                v-for="(tag, index) in props.tags"
                :key="index"
                class="characteristic-bg-excluded"
                :tabstop="false"
                ellipsis
                closable
                @close="$refs.excludedTags?.removeTag(index, $event)"
              >
                {{ tag.name }}
              </b-tag>
            </template>
          </b-taginput>
        </b-field>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IFanfictionFilters } from "@/types/fanfictions";
import { CharacteristicData, CharacteristicTypeData } from "@/types/characteristics";
import { groupBy } from "@/utils/es6-utils";
import { getClassTypeColor as gClassTypeColor, getFullPath as gFullPath } from "@/utils/characteristics";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";
import { getCharacteristics, getCharacteristicsTypes } from "~/api/characteristics";

interface FanfictionFiltersSmallProps {
  authorFieldVisible?: boolean
  fanfictionFilters: IFanfictionFilters
}

let { authorFieldVisible, fanfictionFilters } = defineProps<FanfictionFiltersSmallProps>()

const { data: characteristics } = await getCharacteristics(null)
const { data: characteristicTypes } = await getCharacteristicsTypes()
const filteredTags: CharacteristicData[] = []
let filteredCharacteristics: any[] = []
console.log(characteristics.value)


const grouped = groupBy(
    characteristics.value,
    (characteristic: CharacteristicData) => characteristic.characteristic_type_id
);
characteristicTypes.value.forEach((element: CharacteristicTypeData) => {
    const items = grouped
    .get(element.id)
    .map((groupedCharacteristic: CharacteristicData) => {
        return groupedCharacteristic;
    });

    const itemsSorted: CharacteristicData[] = items
    .filter((t: CharacteristicData) => t.parent_id == null)
    .sort((a: CharacteristicData, b: CharacteristicData) => {
        return a.order - b.order;
    });
    groupBy(items, (g: CharacteristicData) => g.parent_id).forEach(
    (value: CharacteristicData[], key: number) => {
        if (key != null) {
        const index = itemsSorted.findIndex(
            c => c.id === key
        );
        if (index === -1) itemsSorted.splice(0, 0, ...value);
        else itemsSorted.splice(index + 1, 0, ...value);
        }
    }
    );
    filteredCharacteristics.push({
    type: element.name,
    items: itemsSorted
    });
});

let includedTagsFull: CharacteristicData[] = [];
let excludedTagsFull: CharacteristicData[] = [];


// interface FanfictionFiltersSmallEmits {
//   (e: "change", value: IFanfictionFilters): void
// }
// const emit = defineEmits<FanfictionFiltersSmallEmits>()
// watch(fanfictionFilters, () => {
//   emit("change", fanfictionFilters)
// }, { deep: true })

watch(includedTagsFull, (value) => {
  if ((value.length ?? 0) > 0)
    fanfictionFilters.includedTags = value.map((t: CharacteristicData) => t.characteristic_id);
  else
    fanfictionFilters.includedTags = [];
})


watch(excludedTagsFull, (value) => {
  if ((value.length ?? 0) > 0)
    fanfictionFilters.excludedTags = value.map((t: CharacteristicData) => t.characteristic_id);
  else
    fanfictionFilters.excludedTags = [];
})

function getFilteredTags(text: string): void {
  filteredCharacteristics = [];
  characteristics.value.forEach((element: CharacteristicData) => {
    let items: CharacteristicData[] = [];
    if (element.type.toLowerCase().includes(text.toLowerCase())) {
      items = element.items;
    } else {
      items = element.items.filter(
        (item: CharacteristicData) =>
          (getFullPath(item) + item.name)
            .replace(/[\\\- ]/gi, "")
            .toLowerCase()
            .includes(text.replace(/[\\\- ]/gi, "").toLowerCase())
      );
    }
    items = items.filter(
      (item: CharacteristicData) =>
        fanfictionFilters.includedTags.includes(
          item.id
        ) &&
        fanfictionFilters.excludedTags.includes(item.id)
    );

    const itemsSorted: CharacteristicData[] = items
      .filter(t => t.parent_id == null)
      .sort((a: CharacteristicData, b: CharacteristicData) => {
        return a.order - b.order;
      });
    groupBy(items, (g: CharacteristicData) => g.parent_id).forEach(
      (value: CharacteristicData[], key: number) => {
        if (key != null) {
          const index = itemsSorted.findIndex(
            c => c.id === key
          );
          if (index === -1) itemsSorted.splice(0, 0, ...value);
          else itemsSorted.splice(index + 1, 0, ...value);
        }
      }
    );
    if (itemsSorted.length) {
      filteredCharacteristics.push({
        type: element.type,
        items: itemsSorted
      });
    }
  });
}

function tagInput(tag: any): void {
  getFilteredTags("");
}

function getClassTypeColor(characteristic: CharacteristicData): string {
  return gClassTypeColor(characteristic);
}

function getFullPath(characteristic: CharacteristicData): string {
  return gFullPath(characteristic, characteristics.value);
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>
