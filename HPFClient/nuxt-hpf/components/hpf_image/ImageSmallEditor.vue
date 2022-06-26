<template>
  <div
    :class="[{ 'image-editor-hover': hover }, 'is-relative']"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div
      id="image-editor"
      v-if="image"
      class="is-flex is-flex-direction-column is-justify-content-flex-start"
      style="gap: 10px"
    >
      <div
        class="is-flex is-flex-direction-row is-justify-content-flex-start"
        style="gap: 10px"
      >
        <img :src="image.url" />
        <div
          class="
            is-flex-grow-5
            is-flex
            is-flex-direction-column
            is-justify-content-flex-start
          "
          style="gap: 5px"
        >
          <b-input placeholder="Url" size="is-small" v-model="image.url">
          </b-input>
          <b-checkbox size="is-small" v-model="image.age_restricted"
            >Contenu sensible</b-checkbox
          >
        </div>
      </div>

      <b-input placeholder="Crédits" size="is-small" v-model="image.credit">
      </b-input>
      <b-input placeholder="Attribut alt" size="is-small" v-model="image.alt">
      </b-input>
    </div>
    <font-awesome-icon
      id="close-button"
      v-if="hover"
      icon="window-close"
      @click="$emit('remove', image.id_in_text)"
    />
    <!-- <b-button
      id="close-button"
      v-if="hover"
      type="is-primary"
      size="is-small"
      icon-pack="fas"
      icon-left="xmark"
      @click="$emit('remove', image.id_in_text)"
    ></b-button> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from "nuxt-property-decorator";
import { ImageHPFData } from "@/types/images";
@Component({
  name: "ImageSmallEditor",
})
export default class extends Vue {
  //#region Props
  @Prop() private image!: ImageHPFData;
  //#endregion

  //#region Datas
  private hover: boolean = false;
  //#endregion

  //#region Computed

  //#endregion

  //#region Watchers

  //#endregion

  //#region Methods

  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.image-editor-hover {
  // background-color: #e8d7e0 !important;
  // border: 1px solid $primary-light !important;
  // border-radius: 5px !important;
  // cursor: pointer;
}

img {
  display: block;
  max-width: 230px;
  max-height: 50px;
  width: auto;
  height: auto;
}

#close-button {
  display: block;
  position: absolute;
  z-index: 2;
  top: 0px;
  left: 0px;
}
#close-button:hover {
  color: $primary;
  cursor: pointer;
}
</style>