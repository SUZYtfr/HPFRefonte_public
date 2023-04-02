<template>
  <!-- <b-tooltip
    :label="link.link_url"
    position="is-bottom"
    :delay="250"
    append-to-body
  > -->
  <div
    id="user-link-content"
    class="is-flex"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div id="user-link-image" class="" style="z-index: 9999">
      <figure class="image is-32x32 is-clickable">
        <img
          :class="[{ 'img-hover': hover }, 'is-rounded']"
          :src="linkIdImg"
          :alt="link.display_name"
        >
      </figure>
    </div>
    <div v-if="hover" class="">
      <p :class="[{ 'link-hover': hover }, { 'animate__fadeInLeft': hover}, 'animate__animated']">
        {{ link.display_name }}
      </p>
    </div>
  </div>
  <!-- </b-tooltip> -->
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { UserLinkData } from "@/types/users";

@Component({
  name: "UserLink"
})
export default class extends Vue {
  // #region Props
  @Prop() public link!: UserLinkData;
  @Prop() private fullLength!: boolean;
  // #endregion

  // #region Datas
  public hover: boolean = false;
  // #endregion

  // #region Computed
  get linkIdImg(): string {
    const imgDir = require.context("@/assets/img/");
    let s = "placeholders/32x32.png";
    switch (this.link.link_type_id) {
      case 1:
        s = "logo_forum_centre.png";
        break;
      case 2:
        s = "logo_heron_centre.png";
        break;
      case 3:
        s = "facebook.svg";
        break;
      case 4:
        s = "twitter.svg";
        break;
      case 5:
        s = "instagram.svg";
        break;
      case 6:
        s = "deviantart.svg";
        break;
    }
    return imgDir("./" + s);
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

#user-link-content:hover {
  cursor: pointer;
}

img {
  background-color: #f0f0f0;
  /*border: 1px solid $primary;*/
  /*border: 1px solid #707070;*/
}

.img-hover {
  border: 2px solid $primary;
  /*border: 2px solid #707070;*/
}

.link-hover {
  /*font-weight: bold;*/
  text-decoration: underline;
  font-style: italic;
}

figure {
  margin: 0rem !important;
}

p {
  margin-left: 0.5rem;
  color: $primary;
}

#user-link-image {
  z-index: 111;
}
</style>
