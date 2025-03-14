<template>
  <NodeViewWrapper
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
          >
          <p class="is-italic has-text-centered">
            Crédits: {{ image.credits }}
          </p>
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
            <b-input v-model="image.url" placeholder="Url" size="is-small" />
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
            <b-checkbox v-model="preserveRatio" size="is-small">
              Préserver ratio
            </b-checkbox>
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
              />
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
              />
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
                  v-model="image.alt"
                  placeholder="Description de l'image pour les personnes en situation de handicap"
                  size="is-small"
                />
              </b-field>
            </div>
            <!-- <b-checkbox v-model="image.is_adult_only" size="is-small">
              Contenu sensible
            </b-checkbox> -->
          </div>
          <div class="mt-3" style="width: 100%">
            <b-field
              label="Crédits"
              label-position="on-border"
              custom-class="has-text-primary"
            >
              <b-input
                v-model="image.credits"
                type="textarea"
                :has-counter="false"
                minlength="10"
                maxlength="100"
                placeholder="Crédits"
                size="is-small"
              />
            </b-field>
          </div>
        </div>
      </div>
      <div
        id="toolbar"
        class="is-flex is-flex-direction-row is-justify-content-flex-start"
        style="gap: 5px"
      >
        <!-- <font-awesome-icon class="is-danger" v-if="image.credits == null || image.credits.match(/\b\w+\b/) == null" id="warning" icon="exclamation-triangle" /> -->
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="edit"
          :class="{ 'is-hovered': editing }"
          @click="editing = !editing"
        />
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="trash-alt"
          @click="deleteImage()"
        />
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
  </NodeViewWrapper>
</template>

<script setup lang="ts">
import { NodeViewWrapper, NodeViewContent } from "@tiptap/vue-3";
import { ExplicitContentEnum, ImageHPFData } from "@/types/images";

const { deleteNode, editor, node, extension, updateAttributes } = defineProps<{
  deleteNode?: Function;
  editor?: any;
  node?: any;
  extension?: any;
  updateAttributes?: Function;
}>();

let image: ImageHPFData | null = null;
const hover = ref(false);
let editing: boolean = true;
let preserveRatio: boolean = true;
let defaultWidth: number = 32;
let defaultHeight: number = 32;
let currentWidth: number = 32;
let currentHeight: number = 32;

if (extension.storage.images === undefined) extension.storage.images = new Array<ImageHPFData>();
image = editor.extensionStorage.hpfImage.images.filter((image: ImageHPFData) => image.index === node.attrs.index)[0];
if (image === null || image === undefined) {
  image = new ImageHPFData(
    null,
    null,
    null,
    extension.storage.images.length + 1,
    node.attrs.url,
    null,
    null,
    ExplicitContentEnum.Safe,
    null,
    null
  );
  // Mettre à jour l'attribut sans recharger le component
  node.attrs.index = image.index;
  // Ajouter l'image au storage
  extension.storage.images.push(image);
} else {
  // Restaurer les valeurs de tailles / les préférences
  editing = node.attrs.editing;
  preserveRatio = node.attrs.preserveRatio;
  defaultWidth = node.attrs.defaultWidth;
  defaultHeight = node.attrs.defaultHeight;
  currentWidth = node.attrs.currentWidth;
  currentHeight = node.attrs.currentHeight;
}

// TODO régler ça
const toto = useTemplateRef("???")
onUpdated(() => {
  // Fix bug draggable sur Firefox
  toto.value.setAttribute("draggable", "false");
})

onBeforeUnmount(() => {
  // Sauvegarder les choix actuels du component
  node.attrs.editing = editing;
  node.attrs.preserveRatio = preserveRatio;
  node.attrs.defaultWidth = defaultWidth;
  node.attrs.defaultHeight = defaultHeight;
  node.attrs.currentWidth = currentWidth;
  node.attrs.currentHeight = currentHeight;
})

watch(image, () => {
  const img = new Image();
  img.addEventListener("load", () => {
      if (node.attrs.url !== image?.url) {
        defaultWidth = img.naturalWidth;
        currentWidth = defaultWidth;
        defaultHeight = img.naturalHeight;
        currentHeight = defaultHeight;
        node.attrs.url = image?.url;
      }
    });
    img.src = image?.url != null ? image?.url : "https://bulma.io/assets/images/placeholders/32x32.png";
})

function onWidthChanged(): void {
  if (preserveRatio) {
    currentHeight = Math.ceil(
      (defaultHeight * currentWidth) / defaultWidth
    );
  }
  node.attrs.currentWidth = currentWidth;
  node.attrs.currentHeight = currentHeight;
}

function onHeightChanged(): void {
  if (preserveRatio) {
    currentWidth = Math.ceil(
      (defaultWidth * currentHeight) / defaultHeight
    );
  }
  node.attrs.currentWidth = currentWidth;
  node.attrs.currentHeight = currentHeight;
}

function deleteImage(): void {
  editor.extensionStorage.hpfImage.images.splice(
    editor.extensionStorage.hpfImage.images.findIndex(
      (item: ImageHPFData) => item.index === image?.index
    ),
    1
  );
  if (deleteNode != null) deleteNode();
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
#warning {
  width: 1rem;
  height: 1rem;
  margin-top: 7px;
  //color: var(--primary);
}

#handle {
  color: var(--primary);
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
  border: 2px solid var(--scheme-main) !important;
  border-radius: 0.75rem !important;
  margin: 0.25rem 0;
  position: relative;
  min-height: 50px;
  width: 100%;
  padding: 0.25rem 0.25rem;
}

.image-editor-hover {
  border: 2px solid var(--primary-light) !important;
  border-radius: 0.75rem !important;
  background: var(--whitesmoke);
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
  color: var(--primary);
  cursor: pointer;
}
.vertical-line {
  border-radius: 0.75rem !important;
  border-left: 2px solid var(--primary-light);
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
