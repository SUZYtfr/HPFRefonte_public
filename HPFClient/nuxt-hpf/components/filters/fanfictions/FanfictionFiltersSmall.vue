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
          :external-value="fanfictionFilters.status"
          :checked-value="4"
          :excluded-value="1"
          :unchecked-value="null"
          title="Histoires terminées"
          @change="fanfictionFilters.status = $event"
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

<script lang="ts">
import { Component, Vue, Watch, Prop } from "vue-property-decorator";
import { getModule } from "vuex-module-decorators";
import Config from "~/store/modules/Config";
import { IFanfictionFilters } from "@/types/fanfictions";
import { CharacteristicData, CharacteristicTypeData } from "@/types/characteristics";
import { groupBy } from "@/utils/es6-utils";
import { getClassTypeColor, getFullPath } from "@/utils/characteristics";
import ThreeStateCheckbox from "~/components/ThreeStateCheckbox.vue";

@Component({
  name: "FanfictionFiltersSmall",
  components: {
    ThreeStateCheckbox
  }
})
export default class extends Vue {
  // #region Props
  @Prop() private authorFieldVisible!: boolean;
  @Prop() public fanfictionFilters!: IFanfictionFilters;
  // #endregion

  // #region Data
  private characteristics: any[] = [];
  public filteredCharacteristics: any[] = [];
  public includedTagsFull: CharacteristicData[] = [];
  public excludedTagsFull: CharacteristicData[] = [];
  // #endregion

  // #region Hooks
  async fetch(): Promise<void> {
    // Récupération des caractéristiques
    await this.getCharacteristics();
  }
  // #endregion

  // #region Computed
  get ConfigModule(): Config {
    return getModule(Config, this.$store);
  }
  // #endregion

  // #region Watchers
  @Watch("fanfictionFilters", { deep: true })
  private onFiltersChanged(): void {
    this.$emit("change", this.fanfictionFilters);
  }

  @Watch("includedTagsFull")
  private onFiltersincludedTagsChanged(): void {
    if ((this.includedTagsFull?.length ?? 0) > 0)
      this.fanfictionFilters.includedTags = this.includedTagsFull.map((t: CharacteristicData) => t.characteristic_id);
    else
      this.fanfictionFilters.includedTags = [];
  }

  @Watch("excludedTagsFull")
  private onFiltersexcludedTagsChanged(): void {
    if ((this.excludedTagsFull?.length ?? 0) > 0)
      this.fanfictionFilters.excludedTags = this.excludedTagsFull.map((t: CharacteristicData) => t.characteristic_id);
    else
      this.fanfictionFilters.excludedTags = [];
  }
  // #endregion

  // #region Methods
  public getFilteredTags(text: string): void {
    this.filteredCharacteristics = [];
    this.characteristics.forEach((element) => {
      let items: CharacteristicData[] = [];
      if (element.type.toLowerCase().includes(text.toLowerCase())) {
        items = element.items;
      } else {
        items = element.items.filter(
          (item: CharacteristicData) =>
            (this.getFullPath(item) + item.name)
              .replace(/[\\\- ]/gi, "")
              .toLowerCase()
              .includes(text.replace(/[\\\- ]/gi, "").toLowerCase())
        );
      }
      items = items.filter(
        (item: CharacteristicData) =>
          !this.fanfictionFilters.includedTags.includes(
            item.id
          ) &&
          !this.fanfictionFilters.excludedTags.includes(item.id)
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
        this.filteredCharacteristics.push({
          type: element.type,
          items: itemsSorted
        });
      }
    });
  }

  public tagInput(tag: any): void {
    this.getFilteredTags("");
  }

  public async getCharacteristics(): Promise<void> {
    if (
      this.ConfigModule.characteristicTypes.length === 0 ||
      this.ConfigModule.characteristics.length === 0
    ) {
      await this.ConfigModule.LoadConfig();
    }

    const grouped = groupBy(
      this.ConfigModule.characteristics,
      (characteristic: CharacteristicData) => characteristic.characteristic_type_id
    );
    this.ConfigModule.characteristicTypes.forEach((element: CharacteristicTypeData) => {
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
      this.characteristics.push({
        type: element.name,
        items: itemsSorted
      });
    });
    this.filteredCharacteristics = this.characteristics;
  }

  public getClassTypeColor(characteristic: CharacteristicData): string {
    return getClassTypeColor(characteristic);
  }

  public getFullPath(characteristic: CharacteristicData): string {
    return getFullPath(characteristic, this.ConfigModule.characteristics);
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>
