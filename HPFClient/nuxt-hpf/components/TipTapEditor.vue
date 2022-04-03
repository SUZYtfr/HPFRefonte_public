<template>
  <div
    id="editor"
    class="is-flex is-flex-direction-column is-justify-content-flex-start"
    v-if="editor != null"
  >
    <div
      id="editor-header"
      class="
        is-flex
        is-flex-direction-row
        is-justify-content-flex-start
        is-flex-wrap-wrap
      "
      style="gap: 5px"
    >
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="bold"
        :class="{ 'is-hovered': editor.isActive('bold') }"
        @click="editor.chain().focus().toggleBold().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="italic"
        :class="{ 'is-hovered': editor.isActive('italic') }"
        @click="editor.chain().focus().toggleItalic().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="underline"
        :class="{ 'is-hovered': editor.isActive('underline') }"
        @click="editor.chain().focus().toggleUnderline().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="strikethrough"
        :class="{ 'is-hovered': editor.isActive('strike') }"
        @click="editor.chain().focus().toggleStrike().run()"
      ></b-button>
      <div class="py-1">
        <div class="vertical-line" />
      </div>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="align-left"
        :class="{ 'is-hovered': editor.isActive({ textAlign: 'left' }) }"
        @click="editor.chain().focus().setTextAlign('left').run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="align-center"
        :class="{ 'is-hovered': editor.isActive({ textAlign: 'center' }) }"
        @click="editor.chain().focus().setTextAlign('center').run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="align-right"
        :class="{ 'is-hovered': editor.isActive({ textAlign: 'right' }) }"
        @click="editor.chain().focus().setTextAlign('right').run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="align-justify"
        :class="{ 'is-hovered': editor.isActive({ textAlign: 'justify' }) }"
        @click="editor.chain().focus().setTextAlign('justify').run()"
      ></b-button>
      <div class="py-1">
        <div class="vertical-line" />
      </div>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="indent"
        @click="editor.chain().focus().indent().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="outdent"
        @click="editor.chain().focus().outdent().run()"
      ></b-button>
      <div class="py-1">
        <div class="vertical-line" />
      </div>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="list-ul"
        :class="{ 'is-hovered': editor.isActive('bulletList') }"
        @click="editor.chain().focus().toggleBulletList().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="list-ol"
        :class="{ 'is-hovered': editor.isActive('orderedList') }"
        @click="editor.chain().focus().toggleOrderedList().run()"
      ></b-button>
      <div class="py-1">
        <div class="vertical-line" />
      </div>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="undo"
        :disabled="!editor.can().undo()"
        @click="editor.chain().focus().undo().run()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="redo"
        :disabled="!editor.can().redo()"
        @click="editor.chain().focus().redo().run()"
      ></b-button>
      <div class="py-1">
        <div class="vertical-line" />
      </div>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="image"
        @click="addHPFImage()"
      ></b-button>
      <b-button
        type="is-primary"
        outlined
        size="is-small"
        icon-pack="fas"
        icon-left="code"
        @click="test()"
      ></b-button>
    </div>
    <div
      class="
        is-flex-grow-5
        is-flex
        is-flex-direction-row
        is-justify-content-flex-start
      "
      id="editor-content"
    >
      <!-- <div id="editor-content-main-pane" class="is-flex-grow-5"> -->
      <editor-content
        id="editor-content-main-pane"
        :editor="editor"
        class="is-flex-grow-5"
      />
      <!-- </div> -->
      <!-- <div
        id="editor-content-right-pane"
        class="is-flex is-flex-direction-column is-justify-content-flex-start"
      >
        <div id="editor-content-right-pane-content" class="is-flex-grow-5">
          <ImageSmallEditor
            class="mb-2"
            v-for="(image, innerindex) of images"
            :image="image"
            v-bind:index="innerindex"
            v-bind:key="innerindex"
            @remove="RemoveImage"
          ></ImageSmallEditor>
        </div>
        <div id="editor-content-right-pane-footer">
          <button @click="addImages()">Ajout image</button>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "nuxt-property-decorator";
import { Editor, EditorContent } from "@tiptap/vue-2";
import ImageSmallEditor from "~/components/hpf_image/ImageSmallEditor.vue";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import TextAlign from "@tiptap/extension-text-align";
//import Image from "@tiptap/extension-image";
import { Indent } from "~/utils/tiptap_extensions/tiptap_indent";
import { ImageHPFData } from "@/types/images";
import TipTapImageEditor from "~/utils/tiptap_extensions/tiptap_node_image_hpf";

@Component({
  name: "TipTapEditor",
  components: {
    EditorContent,
    ImageSmallEditor,
  },
})
export default class extends Vue {
  //#region Datas
  private editor: Editor | null = null;
  private images: ImageHPFData[] = [];
  //#endregion

  //#region Hooks
  mounted() {
    this.editor = new Editor({
      content: "",
      extensions: [
        StarterKit,
        //Image,
        Underline,
        TextAlign.configure({
          types: ["heading", "paragraph"],
        }),
        Indent,
        TipTapImageEditor,
      ],
      editorProps: {
        // handleDrop: function(view, event, slice, moved) {
        //     if (!moved && event.dataTransfer && event.dataTransfer.files) { // if dropping external files
        //         // the addImage function checks the files are an image upload, and returns the url
        //         addImage(event.dataTransfer.files[0], function(url) {
        //             // this inserts the image with src url into the editor at the position of the drop
        //             const { schema } = view.state;
        //             const coordinates = view.posAtCoords({ left: event.clientX, top: event.clientY });
        //             const node = schema.nodes.image.create({ src: url });
        //             const transaction = view.state.tr.insert(coordinates.pos, node);
        //             return view.dispatch(transaction);
        //         });
        //         return true; // drop is handled don't do anything else
        //     }
        //     return false; // not handled as wasn't dragging a file so use default behaviour
        // },
        handleDOMEvents: {
          drop: (view, e) => {
            if (
              e.dataTransfer &&
              e?.dataTransfer
                ?.getData("text/plain")
                .match(
                  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*\.(jpeg|jpg|png)$)/
                )
            ) {
              if (e.preventDefault) {
                e.preventDefault();
              }
              if (e.stopPropagation) {
                e.stopPropagation();
              }
              const imgURL = e?.dataTransfer?.getData("text/plain");
              const img = new Image();
              img.addEventListener("load", () => {
                const coordinates = view.posAtCoords({
                  left: e.clientX,
                  top: e.clientY,
                });
                this.addHPFImage(
                  imgURL,
                  img.naturalWidth,
                  img.naturalHeight,
                  coordinates?.pos
                );
              });
              img.src = imgURL;

              // if dropping external files

              // // the addImage function checks the files are an image upload, and returns the url
              // addImage(event.dataTransfer.files[0], function(url) {
              //     // this inserts the image with src url into the editor at the position of the drop
              //     const { schema } = view.state;
              //     const coordinates = view.posAtCoords({ left: event.clientX, top: event.clientY });
              //     const node = schema.nodes.image.create({ src: url });
              //     const transaction = view.state.tr.insert(coordinates.pos, node);
              //     return view.dispatch(transaction);
              // });
              return true;
            }
            // Drag and Drop à l'intérieur de tiptap (sur les hpf_images)
            else if (
              e.dataTransfer &&
              e?.dataTransfer?.items?.length == 2 &&
              e?.dataTransfer?.getData("text/plain").length == 0 &&
              e?.dataTransfer?.getData("text/html").match(/^<hpf-image/)
            ) {
              return false;
            } else {
              alert("Non autorisé");
              // TODO MessageBox non autorisé
              return true;
            }
            return false;
          },
        },
      },
    });
    // this.images.push({
    //   image_id: null,
    //   item_id: null,
    //   item_type: null,
    //   id_in_text: 1,
    //   url: "https://nsa39.casimages.com/img/2018/02/16/mini_180216012732482019.jpg",
    //   credit: "Test crédit",
    //   alt: "ahahahaha",
    //   age_restricted: false,
    // });
  }

  beforeDestroy() {
    this.editor?.destroy();
  }
  //#endregion

  //#region Methods
  // private addImages() {
  //   this.images.push(
  //     new ImageHPFData(
  //       null,
  //       null,
  //       null,
  //       this.images.length + 1,
  //       null,
  //       null,
  //       null,
  //       false
  //     )
  //   );
  // }

  private RemoveImage(id_in_text: number | undefined) {
    if (id_in_text !== undefined) {
      this.images = this.images.filter(
        (t: ImageHPFData) => t.id_in_text !== id_in_text
      );
    }
  }

  private test() {
    console.log(this.editor?.getHTML());
  }

  private addHPFImage(
    url: string | null,
    width: number | null,
    height: number | null,
    pos: any | null
  ) {
    this.editor?.commands.insertContentAt(
      pos != null ? pos : this.editor.view.state.selection.$anchor.pos,
      "<hpf-image " +
        (url != null ? 'url="' + url + '"' : "") +
        (width != null
          ? 'defaultWidth="' + width + '" currentWidth="' + width + '" '
          : "") +
        (height != null
          ? 'defaultHeight="' + height + '" currentHeight="' + height + '" '
          : "") +
        'data-type="draggable-item"></hpf-image>'
    );
  }
  //#endregion
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";

/* Basic editor styles */
#editor {
  border: 3px solid $primary !important;
  border-radius: 0.75rem !important;
  background-color: #fff;
  height: 100%;
  width: 100%;
  #editor-header {
    border-bottom: 3px solid $primary !important;
    padding: 4px 6px;
    .vertical-line {
      border-radius: 0.75rem !important;
      border-left: 2px solid $primary-light;
      height: 100%;
    }
    .button.is-primary {
      border-radius: 0.5rem !important;
    }
    .button.is-primary:not(.is-hovered) {
      border-color: transparent !important;
    }
  }
  #editor-content {
    max-height: 100%;
    #editor-content-main-pane {
      overflow-y: auto;
      height: 553px;
      .ProseMirror {
        //background-color: #f3e5a9;
        min-height: 553px;
        padding: 4px;
        border-bottom-left-radius: 0.75rem !important;
        ul,
        ol {
          padding: 0 1rem;
        }
      }
    }
    #editor-content-right-pane {
      border-left: 3px solid $primary !important;
      background-color: #ffffff;
      border-bottom-right-radius: 0.75rem;
      #editor-content-right-pane-content {
        padding: 4px;
        overflow-y: auto;
        height: 0px;
      }
      #editor-content-right-pane-footer {
        border-top: 3px dashed $primary !important;
        height: 50px;
      }
    }
  }
}
</style>