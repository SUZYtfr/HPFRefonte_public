<template>
  <div
    :class="[{ 'fanfiction-hover': hover }, 'fanfiction', 'mx-1 px-1 pb-1']"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div class="columns is-mobile my-0 mx-0">
      <div class="column py-0 pl-0">
        <h3 class="h3 has-text-weight-semibold text-ellipsis-one-line">
          <NuxtLink
            :key="'fiction_' + fanfiction.fanfiction_id.toString()"
            :to="{ name: 'fictions-id', params: { id: fanfiction.fanfiction_id } }"
          >
            {{ fanfiction.title }}
          </NuxtLink>
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
        <template v-for="(author, index) in fanfiction?.authors">
          <template v-if="index > 0">
            ,
          </template>
          <NuxtLink
            :key="'author_' + author.user_id.toString()"
            class="is-size-6-5 has-text-weight-normal"
            :to="{ name: 'auteurs-id', params: { id: author.user_id } }"
          >
            {{ author.username }}
          </NuxtLink>
        </template>
      </div>
      <div class="">
        <NuxtLink
          class="is-size-6 has-text-weight-normal"
            :to="{ name: 'patience', params: { title: 'Reviews pour « ' + fanfiction.title + ' »' } }"
        >
          {{
            (fanfiction?.review_count != null ? (fanfiction?.review_count +
              " review" +
              (fanfiction?.review_count > 1 ? "s" : "")) : "aucune review")
          }}<font-awesome-icon class="ml-1" icon="comments" />
        </NuxtLink>
      </div>
    </div>
    <div
      v-if="(fanfiction?.collection_count ?? 0) > 0"
      class="is-flex is-flex-direction-row"
    >
      <div class="is-flex-grow-5">
        <span><strong>{{
          "Série" + ((fanfiction?.collection_count ?? 0) > 1 ? "s" : "") + " : "
        }}</strong></span>
        <template v-for="(serie, index) in fanfiction?.series">
          <template v-if="index > 0">
            ,
          </template>
          <a
            :key="'serie_' + serie.serie_id.toString()"
            class="is-size-6-5 has-text-weight-normal"
            :href="'series/' + serie.serie_id"
          >{{ serie.title }}
          </a>
        </template>
      </div>
    </div>
    <b-taglist class="mb-0">
      <NuxtLink
        v-for="characteristic in fanfiction?.characteristics"
        :key="'tag_' + characteristic.id.toString()"
        :to="{ name: 'patience', params: { title: 'Page de la caractéristique « ' + characteristic.name + ' »' } }"
      >
        <b-tag
          :class="[getClassType(characteristic), 'mt-0  mb-1 mr-2 is-size-8']"
          type="is-info"
        >
          {{ characteristic.name }}
        </b-tag>
      </NuxtLink>
    </b-taglist>
    <div class="columns mb-0 mx-0 mt-0">
      <div class="column py-0 pl-0">
        <p v-html="fanfiction?.summary" />
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-justify-content-space-evenly">
      <span><strong>{{ fanfiction?.chapter_count }}</strong>
        {{ " chapitre" + ((fanfiction?.chapter_count ?? 0) > 1 ? "s" : "") }}</span>
      <span><strong>{{ fanfiction?.word_count }}</strong>
        {{ " mot" + ((fanfiction?.word_count ?? 0)> 1 ? "s" : "") }}</span>
      <span><strong>{{ fanfiction?.read_count }}</strong>
        {{ " lecture" + ((fanfiction?.read_count ?? 0) > 1 ? "s" : "") }}</span>
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
        <span v-if="(fanfiction?.last_update_date instanceof Date)" class="is-size-6"><strong>{{ (fanfiction?.last_update_date ?? new Date()).toLocaleDateString() }}</strong></span>
        <span class="is-size-6-5 is-hidden-mobile">(publiée depuis le </span>
        <span v-if="(fanfiction?.creation_date instanceof Date)" class="is-size-6-5 is-hidden-mobile"><strong>{{ (fanfiction?.creation_date ?? new Date()).toLocaleDateString() }}</strong></span><span class="is-size-6-5 is-hidden-mobile">)</span>
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

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FanfictionModel } from "@/models/fanfictions";
import { getClassTypeColor } from "@/utils/characteristics";
import { CharacteristicData } from "@/types/characteristics";

@Component({
  name: "Fanfiction"
})
export default class Fanfiction extends Vue {
  // #region Props
  @Prop() public fanfiction!: FanfictionModel;
  // #endregion

  // #region Datas
  // public ratinga = 10;
  public hover: boolean = false;
  // #endregion

  public mounted(): void {
    // console.log("Fanfiction type: " + (this.fanfiction instanceof FanfictionModel));
    // console.log("Date type: " + ((new Date()) instanceof Date));
    // console.log("Creation date type: " + (this.fanfiction?.creation_date instanceof Date));
    // console.log("Last update date type: " + (this.fanfiction?.last_update_date instanceof Date));
    // console.log("Characteristic type: " + (this.fanfiction.characteristics[0] instanceof CharacteristicData));
    // console.log(this.fanfiction?.creation_date);
    // console.log(this.fanfiction?.creation_date?.toLocaleDateString());
  }

  // #region Methods
  public getClassType(characteristic: CharacteristicData): string {
    return getClassTypeColor(characteristic);
  }
  // #endregion
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

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
  background-color: #f6f6f6 !important;
  //border: 1px solid #f6f6f6 !important;
  border-radius: 10px 10px 0px 0px !important;
}

.fanfiction {
  background-color: #ffffff;
  border-bottom: 2px solid $primary;
}

hr {
  background-color: $primary;
}
</style>
