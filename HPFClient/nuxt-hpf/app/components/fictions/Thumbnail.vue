<template>
  <div
    :class="[{ 'fanfiction-hover': hover }, 'fanfiction']"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div
      class="
        is-flex
        is-flex-direction-row
        is-flex-wrap-nowrap
        is-justify-content-start
        is-align-items-center
      "
    >
      <div class="is-flex-grow-5">
        <h3 class="h3 has-text-weight-semibold text-ellipsis-one-line">
          <!-- <NuxtLink
            v-if="fanfiction.chapters?.length || 0 > 0"
            :key="'fiction_' + fanfiction.fanfictionId.toString()"
            :to="{ name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle', params: { fictionId: fanfiction.fanfictionId, fictionTitle: fanfiction.titleAsSlug, chapterId: fanfiction.chapters![0]!.id, chapterTitle: fanfiction.chapters![0]!.title } }"
            no-prefetch
          > -->
            {{ fanfiction.title }}
          <!-- </NuxtLink> -->
        </h3>
      </div>
      <span class="has-text-weight-bold">{{ fanfiction.average }}</span>
      <b-rate
        v-if="fanfiction.average"
        icon-pack="fas"
        :value="fanfiction.average / 10"
        :disabled="true"
        :max="1"
        :rtl="true"
      />
    </div>
    <div
      class="
        is-flex
        is-flex-direction-row
        is-flex-wrap-nowrap
        is-justify-content-start
        is-align-items-center
      "
    >
      <div class="mr-3 white-space-nowrap">
        <template
          v-for="(author, index) in fanfiction.authors"
          :key="'author_' + author.userId.toString()"
        >
          <template v-if="index > 0">
            ,
          </template>
          <!-- <NuxtLink
            class="is-size-7 has-text-weight-normal"
            :to="{ name: 'auteurs-id', params: { id: author.userId } }"
            no-prefetch
          > -->
            {{ author.username }}
          <!-- </NuxtLink> -->
        </template>
      </div>
      <div class="overflow-hidden white-space-nowrap">
        <NuxtLink
          v-for="characteristic in fanfiction.characteristics"
          :key="
            'ff_' +
              fanfiction.fanfictionId +
              '_characteristic_' +
              characteristic.characteristicId.toString()
          "
          :to="{
            name: 'recherche',
            query: {
              fandoms: fandom?.id,
              tags: characteristic.characteristicId
            }
          }"
        ><b-tag
          :class="[getClassType(characteristic), 'my-0 mr-1 is-size-8']"
          type="is-info"
        >{{ characteristic.name }}</b-tag></NuxtLink>
      </div>
    </div>
    <p
      v-plaintext
      class="text-ellipsis-three-line"
      v-html="fanfiction.summary"
    ></p>
  </div>
</template>

<script setup lang="ts">
import type { FanfictionModel } from "~/models";
import { getClassTypeColor } from "~/utils/characteristics";
import type { CharacteristicData } from "~/types/characteristics";
import type { FandomData } from "~/types/fanfictions";

const { fanfiction } = defineProps<{
  fanfiction: FanfictionModel;
  fandom?: FandomData;
}>();

// https://vuejs.org/guide/reusability/custom-directives.html#when-to-use
const vPlaintext = {
    //@ts-ignore
    mounted: el => el.innerHTML = el.innerText.trimStart(),
};

const hover = ref<boolean>(false);

function getClassType(characteristic: CharacteristicData): string {
  return getClassTypeColor(characteristic);
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

.text-ellipsis-three-line {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.text-ellipsis-one-line {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.rating-float-right {
  display: block;
  position: absolute;
  width: 20px;
  height: 25px;
  z-index: 2;
  /*background: blue;*/
  text-align: center;
  font-size: 13px !important;
  padding-right: 5px;
  padding-top: 2px;
}

.fanfiction-hover {
  background-color: var(--hpf-primary-lighter) !important;
  border: 1px solid var(--primary-light) !important;
  border-radius: 5px !important;
}

.fanfiction {
  background-color: var(--scheme-main);
  /*height: 118px;*/
  border: 1px solid transparent;
  padding-bottom: 5px;
  padding-right: 5px;
  padding-left: 5px;
  padding-top: 2px;
}

.overflow-hidden {
  overflow: hidden;
}

.white-space-nowrap {
  white-space: nowrap;
}
</style>