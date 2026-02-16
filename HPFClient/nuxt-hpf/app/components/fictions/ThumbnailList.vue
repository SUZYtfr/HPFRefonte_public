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
          v-if="fanfictions?.totalCount || 0 > 0"
          class="columns is-variable is-1-mobile is-2-tablet is-3-desktop is-3-widescreen is-2-fullhd is-multiline"
        >
          <div
            v-for="(fanfiction, innerindex) of fanfictions?.results"
            :key="
              'ff_' +
              (listType == FanfictionListType.Recent ? 'recent' : 'selection') +
              '_' +
              fanfiction.fanfictionId.toString()
            "
            class="column is-half py-2"
          >
            <FictionsThumbnail :key="fanfiction.fanfictionId" :fanfiction="fanfiction" :index="innerindex" :fandom />
          </div>
        </div>
        <p v-else class="has-text-centered my-2">Aucune fanfiction trouvée</p>
      </div>
      <footer v-if="listType == FanfictionListType.Recent" class="card-footer">
        <p class="card-footer-item py-2">
          <span>
            <NuxtLink
              :to="{
                name: 'recherche',
                query: {
                  fandoms: fandom?.id,
                },
              }"
              no-prefetch
            >
              Plus de nouveautés
            </NuxtLink>
          </span>
        </p>
      </footer>
      <footer v-else-if="listType == FanfictionListType.Selections" class="card-footer">
        <p class="card-footer-item py-2">
          <span>
            <NuxtLink
              :to="{
                name: 'recherche',
                query: {
                  fandoms: fandom?.id,
                },
              }"
              no-prefetch
            >
              Plus de sélections
            </NuxtLink>
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
import type { FanfictionModel } from "@/models/fanfictions";
import { FanfictionListType } from "@/types/other";
import type { FandomData } from "@/types/fanfictions";
import type { FictionTypeOffsetPaginated } from "#gql";

// TODO probablement un meilleur moyen de faire ça
type FictionTypeModelOffsetPaginated = Omit<FictionTypeOffsetPaginated, "results"> & {
  results: FanfictionModel[];
};

defineProps<{
  isLoading: boolean;
  title?: string;
  fandom?: FandomData;
  fanfictions?: FictionTypeModelOffsetPaginated;
  listType: FanfictionListType;
}>();
</script>

<style lang="scss" scoped></style>
