<template>
  <div
    :class="[{ 'fanfiction-hover': ((config?.inList ?? true) ? hover : false) }, 'fanfiction', 'mx-1 px-1 pb-1', {'fanfiction-with-border': (config?.inList ?? true)}]"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div class="columns is-mobile my-0 mx-0">
      <div class="column py-0 pl-0">
        <h3 :class="['h3', 'has-text-weight-semibold', 'text-ellipsis-one-line', {'has-text-centered': ((config?.inList ?? true) == false)}]">
          <!-- <NuxtLink
            v-if="(config?.inList ?? true)"
            :key="'fiction_' + fanfiction.fanfictionId.toString()"
            :to="{ name: 'fictions-fiction_id-fiction_title-chapitres-chapter_id-chapter_title', params: { fiction_id: fanfiction.fanfictionId, fiction_title: fanfiction.titleAsSlug, chapter_id: fanfiction.firstChapter?.id, chapter_title: fanfiction.firstChapter?.title } }"
          > -->
            {{ fanfiction.title }}
          <!-- </NuxtLink> -->
        </h3>
      </div>
      <div class="column is-narrow py-0 px-0 is-flex is-flex-direction-row">
        <b-icon
          v-if="fanfiction?.featured"
          pack="fas"
          type="is-primary"
          icon="award"
        />
        <span class="has-text-weight-bold">{{ fanfiction.average }}</span>
        <b-rate
          v-if="fanfiction.average"
          class="is-align-items-start"
          icon-pack="fas"
          :value="fanfiction.average / 10"
          :disabled="true"
          :max="1"
          :rtl="true"
        />
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-align-items-center">
      <div class="is-flex-grow-5">
        <span class="is-size-6"><strong>{{
          "Auteur" + ((fanfiction?.authors?.length ?? 0) > 1 ? "s" : "") + " : "
        }}</strong></span>
        <template v-for="(author, index) in fanfiction?.authors" :key="'author_' + author.userId.toString()">
          <template v-if="index > 0">
            ,
          </template>
          <a
            class="is-size-6-5 has-text-weight-normal"
            :href="'auteurs/' + author.userId"
          >{{ author.username }}
          </a>
        </template>
      </div>
      <div class="">
        <a class="is-size-6 has-text-weight-normal">{{
          (fanfiction?.reviewCount != null ? (fanfiction?.reviewCount +
            " review" +
            (fanfiction?.reviewCount > 1 ? "s" : "")) : "aucune review")
        }}<font-awesome-icon class="ml-1" icon="comments" />
        </a>
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-align-items-center">
      <div class="is-flex-grow-5">
        <span class="is-size-6"><strong>{{
          "Fandom" + ((fanfiction?.fandoms?.length ?? 0) > 1 ? "s" : "") + " : "
        }}</strong></span>
        <template v-for="(fandom, index) in fanfiction?.fandoms" :key="'author_' + fandom.id.toString()">
          <template v-if="index > 0">, </template>
          <NuxtLink
            class="is-size-6-5 has-text-weight-normal"
            :to="{name: 'fandomSlug', params: {fandomSlug: fandom.slug}}"
          >{{ fandom.name }}</NuxtLink>
        </template>
      </div>
    </div>
    <div
      v-if="(fanfiction?.collectionCount ?? 0) > 0"
      class="is-flex is-flex-direction-row"
    >
      <div class="is-flex-grow-5">
        <span><strong>{{
          "Série" + ((fanfiction?.collectionCount ?? 0) > 1 ? "s" : "") + " : "
        }}</strong></span>
        <template v-for="(serie, index) in fanfiction?.series" :key="'serie_' + serie.serieId.toString()">
          <template v-if="index > 0">
            ,
          </template>
          <a
            class="is-size-6-5 has-text-weight-normal"
            :href="'series/' + serie.serieId"
          >{{ serie.title }}
          </a>
        </template>
      </div>
    </div>
    <b-taglist class="mb-0">
      <span
        v-for="characteristic in fanfiction?.characteristics"
        :key="'tag_' + characteristic.characteristicId.toString()"
      ><b-tag
        :class="[getClassType(characteristic), 'mt-0  mb-1 mr-2 is-size-8']"
        type="is-info"
      >{{ characteristic.name }}</b-tag></span>
    </b-taglist>
    <div class="columns mb-0 mx-0 mt-0">
      <div class="column py-0 pl-0">
        <p v-html="fanfiction?.summary" ></p>
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-justify-content-space-evenly">
      <span><strong>{{ fanfiction?.chapterCount }}</strong>
        {{ " chapitre" + ((fanfiction?.chapterCount ?? 0) > 1 ? "s" : "") }}</span>
      <span><strong>{{ fanfiction?.wordCount }}</strong>
        {{ " mot" + ((fanfiction?.wordCount ?? 0)> 1 ? "s" : "") }}</span>
      <span><strong>{{ fanfiction?.readCount }}</strong>
        {{ " lecture" + ((fanfiction?.readCount ?? 0) > 1 ? "s" : "") }}</span>
    </div>
    <div
      class="
        is-flex
        is-flex-direction-row
        is-flex-wrap-nowrap
        is-justify-content-space-between
        is-align-items-center
      "
    >
      <div>
        <span class="has-text-weight-semibold has-text-primary">{{
          fanfiction?.statusAsText
        }}</span>
        <span class="is-size-6">le </span>
        <span v-if="(fanfiction?.lastUpdateDate instanceof Date)" class="is-size-6"><strong>{{ (fanfiction?.lastUpdateDate ?? new Date()).toLocaleDateString("fr-FR") }}</strong></span>
        <span class="is-size-6-5 is-hidden-mobile">(publiée depuis le </span>
        <span v-if="(fanfiction?.creationDate instanceof Date)" class="is-size-6-5 is-hidden-mobile"><strong>{{ (fanfiction?.creationDate ?? new Date()).toLocaleDateString("fr-FR") }}</strong></span><span class="is-size-6-5 is-hidden-mobile">)</span>
      </div>
      <div class="is-block">
        <b-tooltip label="Ajouter à la pile à lire" type="is-primary">
          <b-button
            type="is-primary"
            icon-left="bookmark"
            size="is-small"
            outlined
            class="is-inline"
          />
        </b-tooltip>
        <b-tooltip label="Signaler" type="is-danger">
          <b-button
            type="is-danger"
            icon-left="exclamation-triangle"
            size="is-small"
            outlined
            class="is-inline"
          />
        </b-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FanfictionModel, FanfictionEntityConfig } from "~/models";
import { getClassTypeColor } from "~/utils/characteristics";
import type { CharacteristicData } from "~/types/characteristics";

interface Props {
  fanfiction: FanfictionModel;
  config?: FanfictionEntityConfig;
}

const { fanfiction, config } = defineProps<Props>();

const hover = ref<boolean>(false);

function getClassType(characteristic: CharacteristicData): string {
  return getClassTypeColor(characteristic);
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

.rating-float-right {
  display: block;
  position: absolute;
  width: 20px;
  height: 25px;
  z-index: 2;
  text-align: center;
  font-size: 13px !important;
  padding-right: 5px;
  padding-top: 2px;
}

.is-size-8 {
  font-size: 0.7rem;
}

.is-size-6-5 {
  font-size: 0.87rem;
}

.fanfiction-hover {
  background-color: var(--whitesmoke) !important;
  //border: 1px solid #f6f6f6 !important;
  border-radius: 10px 10px 0px 0px !important;
}

.fanfiction {
  background-color: var(--scheme-main);
}
.fanfiction-with-border {
  border-bottom: 2px solid var(--primary);
}

hr {
  background-color: var(--primary);
}
</style>