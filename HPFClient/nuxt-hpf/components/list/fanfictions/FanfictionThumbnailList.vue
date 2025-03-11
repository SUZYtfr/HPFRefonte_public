<template>
  <div>
    <div class="card">
      <header class="card-header sub-title">
        <p class="card-header-title is-centered">
          {{ title }}
        </p>
      </header>
      <div class="card-content is-relative p-2">
        <b-loading v-if="isLoading" :is-full-page="false" />
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
            :key="'ff_' + (listType == FanfictionListType.Recent ? 'recent' : 'selection' )+'_' + fanfiction.fanfiction_id.toString()"
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
            <NuxtLink
              to="/search"
              no-prefetch
            > Plus de nouveautés </NuxtLink>
          </span>
        </p>
      </footer>
      <footer v-else-if="listType == FanfictionListType.Selections" class="card-footer">
        <p class="card-footer-item py-2">
          <span>
            <NuxtLink
              to="/search"
              no-prefetch
            > Plus de sélections </NuxtLink>
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

<script setup lang="ts">
import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";
import { FanfictionModel } from "@/models/fanfictions";
import { FanfictionListType } from "@/types/other";

const { isLoading = false, fanfictions = [], listType } = defineProps<{
  isLoading: boolean;
  fanfictions: FanfictionModel[];
  listType: FanfictionListType;
}>();

let title: string = "";
switch (listType) {
  case FanfictionListType.Recent:
    title = "Nouveautés";
    break;
  case FanfictionListType.Selections:
    title = "Sélections du mois";
    break;
  default:
    title = "";
    break;
}
</script>

<style lang="scss" scoped>

</style>
