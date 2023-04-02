<template>
  <div
    :class="[{ 'image-editor-hover': hover }, 'is-relative']"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div
      v-if="image"
      id="image-editor"
      class="is-flex is-flex-direction-column is-justify-content-flex-start"
      style="gap: 10px"
    >
      <div
        class="is-flex is-flex-direction-row is-justify-content-flex-start"
        style="gap: 10px"
      >
        <img :src="image.url">
        <div
          class="
            is-flex-grow-5
            is-flex
            is-flex-direction-column
            is-justify-content-flex-start
          "
          style="gap: 5px"
        >
          <b-input v-model="image.url" placeholder="Url" size="is-small" />
          <b-checkbox v-model="image.age_restricted" size="is-small">
            Contenu sensible
          </b-checkbox>
        </div>
      </div>

      <b-input v-model="image.credit" placeholder="Crédits" size="is-small" />
      <b-input v-model="image.alt" placeholder="Attribut alt" size="is-small" />
    </div>
    <font-awesome-icon
      v-if="hover"
      id="close-button"
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
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { ImageHPFData } from "@/types/images";
@Component({
  name: "ImageSmallEditor"
})
export default class extends Vue {
  // #region Props
  @Prop() public image!: ImageHPFData;
  // #endregion

  // #region Datas
  public hover: boolean = false;
  // #endregion

  // #region Computed

  // #endregion

  // #region Watchers

  // #endregion

  // #region Methods

  // #endregion
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
