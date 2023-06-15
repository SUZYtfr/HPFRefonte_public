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
          <NuxtLink
            :key="'fiction_' + fanfiction.fanfiction_id.toString()"
            :to="{ name: 'fictions-id', params: { id: fanfiction.fanfiction_id } }"
          >
            {{ fanfiction.title }}
          </NuxtLink>
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
        <template v-for="(author, index) in fanfiction.authors">
          <template v-if="index > 0">
            ,
          </template>
          <NuxtLink
            :key="'author_' + author.user_id.toString()"
            class="is-size-7 has-text-weight-normal"
            :to="{ name: 'auteurs-id', params: { id: author.user_id } }"
          >
            {{ author.username }}
          </NuxtLink>
        </template>
      </div>
      <div class="overflow-hidden white-space-nowrap">
        <NuxtLink
          v-for="characteristic in fanfiction.characteristics"
          :to="{ name: 'patience', params: { title: 'Page de la caractéristique « ' + characteristic.name + ' »' } }"
          :key="
            'ff_' +
              fanfiction.fanfiction_id +
              '_characteristic_' +
              characteristic.id.toString()
          "
        >
          <b-tag
            :class="[getClassType(characteristic), 'my-0 mr-1 is-size-8']"
            type="is-info"
          >{{ characteristic.name }}</b-tag>
        </NuxtLink>
      </div>
    </div>
    <p
      v-plaintext
      class="text-ellipsis-three-line"
      v-html="fanfiction.summary"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FanfictionModel } from "@/models/fanfictions";
import { getClassTypeColor } from "@/utils/characteristics";
import { CharacteristicData } from "@/types/characteristics";

@Component({
  name: "FanfictionThumbnail",
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    }
  },
  directives: {
    plaintext: {
      bind: function (el, binding, vnode) {
        el.innerHTML = el.innerText.trimStart();
      }
    }
  }
})
export default class FanfictionThumbnail extends Vue {
  // #region Props
  @Prop() public fanfiction!: FanfictionModel;
  // #endregion

  // #region Datas
  // public ratinga = 10;
  public hover: boolean = false;
  // #endregion

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
