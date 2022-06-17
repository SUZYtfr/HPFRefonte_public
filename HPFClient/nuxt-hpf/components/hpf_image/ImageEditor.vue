<template>
  <node-view-wrapper
    :class="[{ 'image-editor-hover': editing }, 'image-editor']"
  >
    <div
      class="is-relative"
      @mouseover="hover = true"
      @mouseleave="hover = false"
    >
      <div
        v-if="image"
        class="
          is-flex
          is-flex-direction-row
          is-justify-content-center
          is-align-items-flex-start
          is-flex-wrap-wrap
        "
        style="gap: 5px"
      >
        <div
          class="
            is-flex-grow-2
            is-flex
            is-flex-direction-column
            is-justify-content-flex-start
            is-align-items-center
            is-align-self-center
          "
          style="gap: 2px;"
        >
          <img
            :src="image.url"
            :alt="image.alt"
            class="mx-3"
            :style="{
              height: currentHeight + 'px',
              width: currentWidth + 'px',
              maxHeight: editing ? 250 + 'px' : 1200 + 'px',
              maxWidth: editing ? 90 + '%' : 600 + 'px',
            }"
          />
          <p class="is-italic has-text-centered">Crédits: {{ image.credit }}</p>
        </div>
        <div
          v-if="editing"
          id="pnl-right-editor"
          class="
            is-flex
            is-flex-direction-column
            is-justify-content-flex-start
            is-align-items-center
            px-2
            pb-2
          "
          style="gap: 2px; min-width: 250px"
        >
          <b-field
            label="Url"
            label-position="on-border"
            custom-class="has-text-primary"
            style="width: 100%"
          >
            <b-input placeholder="Url" size="is-small" v-model="image.url">
            </b-input>
          </b-field>
          <div
            class="
              is-flex
              is-flex-direction-row
              is-justify-content-center
              is-align-items-baseline
            "
            style="gap: 5px"
          >
            <b-checkbox size="is-small" v-model="preserveRatio"
              >Préserver ratio</b-checkbox
            >
            <b-field
              label="Largeur"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model.number="currentWidth"
                type="number"
                size="is-small"
                placeholder="Largeur en pixel"
                pattern="^\d+$"
                @input="onWidthChanged"
              ></b-input>
            </b-field>
            <b-field
              label="Hauteur"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model.number="currentHeight"
                type="number"
                size="is-small"
                placeholder="Hauteur en pixel"
                pattern="^\d+$"
                @input="onHeightChanged"
              ></b-input>
            </b-field>
          </div>
          <div
            class="
              is-flex
              is-flex-direction-row
              is-justify-content-flex-start
              is-align-items-baseline
            "
            style="gap: 5px; width: 100%"
          >
            <div class="is-flex-grow-5">
              <b-field
                label="Description alternative"
                label-position="on-border"
                custom-class="has-text-primary"
              >
                <b-input
                  placeholder="Description de l'image pour les personnes en situation de handicap"
                  size="is-small"
                  v-model="image.alt"
                >
                </b-input>
              </b-field>
            </div>
            <b-checkbox size="is-small" v-model="image.age_restricted"
              >Contenu sensible</b-checkbox
            >
          </div>
          <div class="mt-3" style="width: 100%">
            <b-field
              label="Crédits"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                type="textarea"
                :has-counter="false"
                minlength="10"
                maxlength="100"
                placeholder="Crédits"
                size="is-small"
                v-model="image.credit"
              >
              </b-input>
            </b-field>
          </div>
        </div>
      </div>
      <div
        id="toolbar"
        class="is-flex is-flex-direction-row is-justify-content-flex-start"
        style="gap: 5px"
      >
        <!-- <font-awesome-icon class="is-danger" v-if="image.credit == null || image.credit.match(/\b\w+\b/) == null" id="warning" icon="exclamation-triangle" /> -->
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="edit"
          :class="{ 'is-hovered': editing }"
          @click="editing = !editing"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="trash-alt"
          @click="deleteImage()"
        ></b-button>
      </div>
      <font-awesome-icon
        v-if="hover"
        id="handle"
        icon="grip-vertical"
        contenteditable="false"
        draggable="true"
        data-drag-handle
      />
    </div>
  </node-view-wrapper>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from "nuxt-property-decorator";
import { ImageHPFData } from "@/types/images";
import { NodeViewWrapper, NodeViewContent } from "@tiptap/vue-2";

@Component({
  name: "ImageEditor",
  components: {
    NodeViewWrapper,
    NodeViewContent,
  },
})
export default class extends Vue {
  //#region Props
  @Prop() private deleteNode!: Function;
  @Prop() private editor!: any;
  @Prop() private node!: any;
  @Prop() private extension!: any;
  @Prop() private updateAttributes!: Function;
  //#endregion

  //#region Datas
  private image: ImageHPFData | null = null;
  private hover: boolean = false;
  private editing: boolean = true;
  private preserveRatio: boolean = true;
  private defaultWidth: number = 32;
  private defaultHeight: number = 32;
  private currentWidth: number = 32;
  private currentHeight: number = 32;
  //#endregion

  //#region Computed

  //#endregion

  //#region Hooks
  created() {
    if (this.extension.storage.images === undefined)
      this.extension.storage.images = new Array<ImageHPFData>();
    this.image = this.editor.extensionStorage.hpfImage.images.filter(
      (image: ImageHPFData) => image.id_in_text === this.node.attrs.id_in_text
    )[0];
    if (this.image === null || this.image === undefined) {
      this.image = new ImageHPFData(
        null,
        null,
        null,
        this.extension.storage.images.length + 1,
        this.node.attrs.url,
        null,
        null,
        false
      );
      // Mettre à jour l'attribut sans recharger le component
      this.node.attrs.id_in_text = this.image.id_in_text;
      // Ajouter l'image au storage
      this.extension.storage.images.push(this.image);
    }
    {
      // Restaurer les valeurs de tailles / les préférences
      this.editing = this.node.attrs.editing;
      this.preserveRatio = this.node.attrs.preserveRatio;
      this.defaultWidth = this.node.attrs.defaultWidth;
      this.defaultHeight = this.node.attrs.defaultHeight;
      this.currentWidth = this.node.attrs.currentWidth;
      this.currentHeight = this.node.attrs.currentHeight;
    }
  }

  updated() {
    // Fix bug draggable sur Firefox
    this.$el.setAttribute("draggable", "false");
  }

  beforeDestroy() {
    // Sauvegarder les choix actuels du component
    this.node.attrs.editing = this.editing;
    this.node.attrs.preserveRatio = this.preserveRatio;
    this.node.attrs.defaultWidth = this.defaultWidth;
    this.node.attrs.defaultHeight = this.defaultHeight;
    this.node.attrs.currentWidth = this.currentWidth;
    this.node.attrs.currentHeight = this.currentHeight;
  }
  //#endregion

  //#region Watchers
  @Watch("image.url")
  private async onUrlChanged() {
    const img = new Image();
    img.addEventListener("load", () => {
      if (this.node.attrs.url != this.image?.url) {
        this.defaultWidth = img.naturalWidth;
        this.currentWidth = this.defaultWidth;
        this.defaultHeight = img.naturalHeight;
        this.currentHeight = this.defaultHeight;
        this.node.attrs.url = this.image?.url;
      }
    });
    img.src =
      this.image?.url != null
        ? this.image?.url
        : "https://bulma.io/images/placeholders/32x32.png";
  }
  //#endregion

  //#region Methods
  private onWidthChanged() {
    if (this.preserveRatio) {
      this.currentHeight = Math.ceil(
        (this.defaultHeight * this.currentWidth) / this.defaultWidth
      );
    }
    this.node.attrs.currentWidth = this.currentWidth;
    this.node.attrs.currentHeight = this.currentHeight;
  }

  private onHeightChanged() {
    if (this.preserveRatio) {
      this.currentWidth = Math.ceil(
        (this.defaultWidth * this.currentHeight) / this.defaultHeight
      );
    }
    this.node.attrs.currentWidth = this.currentWidth;
    this.node.attrs.currentHeight = this.currentHeight;
  }

  private deleteImage() {
    this.editor.extensionStorage.hpfImage.images.splice(
      this.editor.extensionStorage.hpfImage.images.findIndex(
        (item: ImageHPFData) => item.id_in_text === this.image?.id_in_text
      ),
      1
    );
    this.deleteNode();
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
#warning {
  width: 1rem;
  height: 1rem;
  margin-top: 7px;
  //color: $primary;
}

#handle {
  color: $primary;
  display: block;
  position: absolute;
  z-index: 2;
  top: 0px;
  left: 0px;
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
  cursor: grab;
}

.image-editor {
  /*background: #FAF594;*/
  border: 2px solid #ffffff !important;
  border-radius: 0.75rem !important;
  margin: 0.25rem 0;
  position: relative;
  min-height: 50px;
  width: 100%;
  padding: 0.25rem 0.25rem;
}

.image-editor-hover {
  border: 2px solid $primary-light !important;
  border-radius: 0.75rem !important;
  background: #f6f6f6;
  /*margin: 1rem 0;
  position: relative;
  height: 200px;
  width: 200px;*/
}

img {
  display: block;
}

#pnl-right-editor {
  padding-top: 35px;
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
.vertical-line {
  border-radius: 0.75rem !important;
  border-left: 2px solid $primary-light;
  height: 100%;
}
#toolbar {
  display: block;
  position: absolute;
  z-index: 2;
  top: 0px;
  right: 0px;
  .button.is-primary {
    border-radius: 0.5rem !important;
  }
  .button.is-primary:not(.is-hovered) {
    border-color: transparent !important;
  }
}
</style>