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
          <a href="viewstory.php?sid=37709">{{ fanfiction.title }}</a>
        </h3>
      </div>
      <span class="has-text-weight-bold">{{ ratinga }}</span>
      <b-rate
        icon-pack="fas"
        :value="1"
        :disabled="true"
        :max="1"
        :rtl="true"
      ></b-rate>
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
        <template v-for="(author, index) in fanfiction.authors">
          <template v-if="index > 0">,</template>
          <a
            class="is-size-7 has-text-weight-normal"
            v-bind:key="author.author_id"
            v-bind:href="'auteurs/' + author.author_id"
            >{{ author.nickname }}
          </a>
        </template>
      </div>
      <div class="overflow-hidden white-space-nowrap">
        <a
          v-for="characteristic in fanfiction.characteristics"
          v-bind:key="characteristic.characteristic_id"
          v-bind:href="'auteurs/' + characteristic.characteristic_id"
          ><b-tag
            :class="[getClassType(characteristic), 'my-0 mr-1 is-size-8']"
            type="is-info"
            >{{ characteristic.name }}</b-tag
          ></a
        >
      </div>
    </div>
    <p
      v-html="fanfiction.summary"
      v-plaintext
      class="text-ellipsis-three-line"
    ></p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FanfictionData } from "@/types/fanfictions";
import { getClassTypeColor } from "@/utils/characteristics";
import { ICharacteristic } from "@/types/characteristics";

@Component({
  name: "FanfictionThumbnail",
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    },
  },
  directives: {
    plaintext: {
      bind: function (el, binding, vnode) {
        el.innerHTML = el.innerText.trimStart();
      },
    },
  },
})
export default class FanfictionThumbnail extends Vue {
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
  background-color: #e8d7e0 !important;
  border: 1px solid $primary-light !important;
  border-radius: 5px !important;
}

.fanfiction {
  background-color: #ffffff;
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
