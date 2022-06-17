<template>
  <div
    :class="[{ 'fanfiction-hover': hover }, 'fanfiction', 'mx-1 px-1 pb-1']"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div class="columns is-mobile my-0 mx-0">
      <div class="column py-0 pl-0">
        <h3 class="h3 has-text-weight-semibold text-ellipsis-one-line">
          <a href="viewstory.php?sid=37709">{{ fanfiction.title }}</a>
        </h3>
      </div>
      <div class="column is-narrow py-0 px-0 is-flex is-flex-direction-row">
        <b-icon
          v-if="fanfiction.featured"
          pack="fas"
          type="is-primary"
          icon="award"
        />
        <span class="has-text-weight-bold">{{ ratinga }}</span>
        <b-rate
          class="is-align-items-start"
          icon-pack="fas"
          :value="1"
          :disabled="true"
          :max="1"
          :rtl="true"
        ></b-rate>
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-align-items-center">
      <div class="is-flex-grow-5">
        <span class="is-size-6"
          ><strong>{{
            "Auteur" + (fanfiction.authors.length > 1 ? "s" : "") + " : "
          }}</strong></span
        >
        <template v-for="(author, index) in fanfiction.authors">
          <template v-if="index > 0">,</template>
          <a
            class="is-size-6-5 has-text-weight-normal"
            v-bind:key="'author_' + author.author_id.toString()"
            v-bind:href="'auteurs/' + author.author_id"
            >{{ author.nickname }}
          </a>
        </template>
      </div>
      <div class="">
        <a class="is-size-6 has-text-weight-normal"
          >{{
            fanfiction.comments.length +
            " review" +
            (fanfiction.comments.length > 1 ? "s" : "")
          }}<font-awesome-icon class="ml-1" icon="comments" />
        </a>
      </div>
    </div>
    <div
      v-if="fanfiction.series != null && fanfiction.series.length > 0"
      class="is-flex is-flex-direction-row"
    >
      <div class="is-flex-grow-5">
        <span
          ><strong>{{
            "Série" + (fanfiction.series.length > 1 ? "s" : "") + " : "
          }}</strong></span
        >
        <template v-for="(serie, index) in fanfiction.series">
          <template v-if="index > 0">,</template>
          <a
            class="is-size-6-5 has-text-weight-normal"
            v-bind:key="'serie_' + serie.serie_id.toString()"
            v-bind:href="'series/' + serie.serie_id"
            >{{ serie.title }}
          </a>
        </template>
      </div>
    </div>
    <b-taglist class="mb-0">
      <a
        v-for="characteristic in fanfiction.characteristics"
        v-bind:key="'tag_' + characteristic.characteristic_id.toString()"
        v-bind:href="'auteurs/' + characteristic.characteristic_id"
        ><b-tag
          :class="[getClassType(characteristic), 'mt-0  mb-1 mr-2 is-size-8']"
          type="is-info"
          >{{ characteristic.name }}</b-tag
        ></a
      >
    </b-taglist>
    <div class="columns mb-0 mx-0 mt-0">
      <div class="column py-0 pl-0">
        <p v-html="fanfiction.summary"></p>
      </div>
    </div>
    <div class="is-flex is-flex-direction-row is-justify-content-space-evenly">
      <span
        ><strong>{{ fanfiction.chapter_count }}</strong>
        {{ " chapitre" + (fanfiction.chapter_count > 1 ? "s" : "") }}</span
      >
      <span
        ><strong>{{ fanfiction.word_count }}</strong>
        {{ " mot" + (fanfiction.word_count > 1 ? "s" : "") }}</span
      >
      <span
        ><strong>{{ fanfiction.read_count }}</strong>
        {{ " lecture" + (fanfiction.read_count > 1 ? "s" : "") }}</span
      >
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
          fanfiction.status | fanfictionStatus
        }}</span>
        <span class="is-size-6">le </span>
        <span class="is-size-6"
          ><strong>{{ fanfiction.last_update_date | parseTime }}</strong></span
        >
        <span class="is-size-6-5 is-hidden-mobile">(publiée depuis le </span>
        <span class="is-size-6-5 is-hidden-mobile"
          ><strong>{{ fanfiction.creation_date | parseTime }}</strong></span
        ><span class="is-size-6-5 is-hidden-mobile">)</span>
      </div>
      <div class="is-block">
        <b-tooltip label="Ajouter à la pile à lire" type="is-primary">
          <b-button
            type="is-primary"
            icon-left="bookmark"
            size="is-small"
            outlined
            class="is-inline"
          >
          </b-button>
        </b-tooltip>
        <b-tooltip label="Signaler" type="is-danger">
          <b-button
            type="is-danger"
            icon-left="exclamation-triangle"
            size="is-small"
            outlined
            class="is-inline"
          >
          </b-button>
        </b-tooltip>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FanfictionData } from "@/types/fanfictions";
import { getClassTypeColor } from "@/utils/characteristics";
import { ICharacteristic } from "@/types/characteristics";

@Component({
  name: "Fanfiction",
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    },
    fanfictionStatus: (status: number) => {
      switch (status) {
        case 1:
          return "Mise à jour";
        case 2:
          return "Arrêtée";
        case 3:
          return "Abandonnée";
        case 4:
          return "Terminée";
      }
    },
  },
})
export default class Fanfiction extends Vue {
  //#region Props
  @Prop() private fanfiction!: FanfictionData;
  //#endregion

  //#region Datas
  private ratinga = 10;
  private hover: boolean = false;
  //#endregion

  //#region Methods
  private getClassType(characteristic: ICharacteristic) {
    return getClassTypeColor(characteristic);
  }
  //#endregion
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
