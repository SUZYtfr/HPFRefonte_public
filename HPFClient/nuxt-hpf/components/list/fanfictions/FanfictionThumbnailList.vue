<template>
  <div>
    <div class="card">
      <header class="card-header sub-title">
        <p class="card-header-title is-centered">
          {{ title }}
        </p>
      </header>
      <div class="card-content is-relative p-2">
        <b-loading v-model="isLoading" :is-full-page="false" />
        <div
          v-if="fanfictions?.length > 0"
          class="
                columns
                is-variable
                is-1-mobile
                is-2-tablet
                is-3-desktop
                is-3-widescreen
                is-2-fullhd
                is-multiline
              "
        >
          <div

            v-for="(fanfiction, innerindex) of fanfictions"
            :key="'ff_recent_' + fanfiction.fanfiction_id.toString()"
            class="column is-half py-2"
          >
            <FanfictionThumbnail
              :key="fanfiction.fanfiction_id"
              :fanfiction="fanfiction"
              :index="innerindex"
            />
          </div>
        </div>
        <p v-else class="has-text-centered my-2">
          Aucune fanfiction trouvée
        </p>
      </div>
      <footer v-if="listType == FanfictionListType.Recent" class="card-footer">
        <p class="card-footer-item py-2">
          <span>
            <NuxtLink to="/search"> Plus de nouveautés </NuxtLink>
          </span>
        </p>
      </footer>
      <footer v-else-if="listType == FanfictionListType.Selections" class="card-footer">
        <p class="card-footer-item py-2">
          <span>
            <NuxtLink to="/search"> Plus de sélections </NuxtLink>
          </span>
        </p>
        <p class="card-footer-item py-2">
          <span>
            <a href="">Votez pour les sélections</a>
          </span>
        </p>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";
import { FanfictionModel } from "@/models/fanfictions";
import { FanfictionListType } from "@/types/other";

@Component({
  name: "FanfictionThumbnailList",
  components: {
    FanfictionThumbnail
  },
  fetchOnServer: true,
  fetchKey: "fanfiction-thumbnail-list"
})
export default class FanfictionThumbnailList extends Vue {
  // #region Props
  @Prop({ default: false }) public isLoading!: boolean;
  @Prop({ default: FanfictionListType.Recent }) public listType!: FanfictionListType;
  @Prop({ default: [] }) public fanfictions!: FanfictionModel[];
  // #endregion

  // #region Computed
  get title(): string {
    let result: string = "";
    switch (this.listType) {
      case FanfictionListType.Recent:
        result = "Nouveautés";
        break;
      case FanfictionListType.Selections:
        result = "Sélections du mois";
        break;
      default:
        result = "";
        break;
    }
    return result;
  }
  // #endregion
}
</script>

<style lang="scss" scoped>

</style>
