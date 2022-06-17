<template>
  <div style="height: 100%;">
    <!-- Editor -->
    <div
      id="editor"
      class="is-flex is-flex-direction-column is-justify-content-flex-start"
      v-if="editor != null"
    >
      <!-- Toolbar -->
      <div
        id="editor-header"
        :class="[
          'is-flex',
          'is-flex-direction-row',
          'is-justify-content-flex-start',
          'is-flex-wrap-wrap',
          { 'editor-disabled': linkEditorModalActive },
        ]"
      >
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="bold"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
          @click="editor.chain().focus().toggleBold().run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="italic"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
          @click="editor.chain().focus().toggleItalic().run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="underline"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
          @click="editor.chain().focus().toggleUnderline().run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="strikethrough"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.strike }"
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
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
          @click="editor.chain().focus().setTextAlign('left').run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-center"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignCenter,
          }"
          @click="editor.chain().focus().setTextAlign('center').run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-right"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignRight,
          }"
          @click="editor.chain().focus().setTextAlign('right').run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-justify"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignJustified,
          }"
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
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.bulletList }"
          @click="editor.chain().focus().toggleBulletList().run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="list-ol"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.orderedList }"
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
          :disabled="!editorFunctionsActiveStatuses.undo"
          @click="editor.chain().focus().undo().run()"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="redo"
          :disabled="!editorFunctionsActiveStatuses.redo"
          @click="editor.chain().focus().redo().run()"
        ></b-button>
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-dropdown aria-role="list" :mobile-modal="false">
          <template #trigger="{ active }">
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              :icon-left="currentStyle.icon"
              :label="currentStyle.text"
              :icon-right="active ? 'angle-up' : 'angle-down'"
            />
          </template>
          <b-dropdown-item
            v-for="(menu, index) in menusStyle"
            :key="index"
            :value="menu"
            aria-role="listitem"
          >
            <div class="media" @click="toggleStyle(menu.action)">
              <b-icon class="media-left" :icon="menu.icon"></b-icon>
              <div class="media-content">
                <h3>{{ menu.text }}</h3>
              </div>
            </div>
          </b-dropdown-item>
        </b-dropdown>

        <b-dropdown aria-role="list" :mobile-modal="false">
          <template #trigger="{ active }">
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="text-height"
              :label="editorFunctionsTextStyleStatuses.fontSize"
              :icon-right="active ? 'angle-up' : 'angle-down'"
            />
          </template>
          <b-dropdown-item
            v-for="(fontSize, index) in menusFontSize"
            :key="index"
            :value="fontSize"
            aria-role="listitem"
          >
            <div
              class="media"
              @click="
                editor
                  .chain()
                  .focus()
                  .setFontSize(fontSize + 'px')
                  .run()
              "
            >
              <div class="media-content">
                <h3
                  :style="{
                    fontSize: fontSize + 'px',
                  }"
                >
                  {{ fontSize + " px" }}
                </h3>
              </div>
            </div>
          </b-dropdown-item>
        </b-dropdown>
        <b-dropdown aria-role="list" :mobile-modal="false">
          <template #trigger="{ active }">
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="font"
              :label="editorFunctionsTextStyleStatuses.fontFamily"
              :icon-right="active ? 'angle-up' : 'angle-down'"
            />
          </template>
          <b-dropdown-item
            v-for="(fontFamily, index) in menusFontFamily"
            :key="index"
            :value="fontFamily"
            aria-role="listitem"
          >
            <div class="media" @click="toggleFontFamily(fontFamily)">
              <div class="media-content">
                <h3
                  :style="{
                    fontFamily: fontFamily,
                  }"
                >
                  {{ fontFamily }}
                </h3>
              </div>
            </div>
          </b-dropdown-item>
        </b-dropdown>
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
          icon-left="link"
          @click="linkEditorModalActive = true"
        ></b-button>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="grip-lines"
          @click="editor.chain().focus().setHorizontalRule().run()"
        ></b-button>
        <!-- <div class="py-1">
          <div class="vertical-line" />
        </div>
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-button
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="code"
          @click="test()"
        ></b-button> -->
      </div>
      <!-- END: ToolBar -->

      <div
        class="
          is-flex-grow-5
          is-flex
          is-flex-direction-row
          is-justify-content-flex-start
        "
        id="editor-content"
      >
        <div
          class="
            is-flex-grow-5
            is-flex
            is-flex-direction-column
            is-justify-content-flex-start
            is-relative
          "
        >
          <!-- Bubble menu -->
          <bubble-menu
            id="editor-bubble-menu"
            :editor="editor"
            :tippy-options="{ duration: 100, placement: 'bottom' }"
            :shouldShow="bubbleMenuShouldShow"
          >
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="bold"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
              @click="editor.chain().focus().toggleBold().run()"
            ></b-button>
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="italic"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
              @click="editor.chain().focus().toggleItalic().run()"
            ></b-button>
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="underline"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
              @click="editor.chain().focus().toggleUnderline().run()"
            ></b-button>
            <b-button
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="link"
              @click="linkEditorModalActive = true"
            ></b-button>
          </bubble-menu>
          <!-- END: Bubble menu -->

          <!-- Modal Editor Link -->
          <div class="editor-modal-container" v-if="linkEditorModalActive">
            <div class="editor-modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Insérer un lien hypertexte</p>
                <button
                  type="button"
                  class="delete"
                  @click="linkEditorModalActive = false"
                />
              </header>
              <section class="modal-card-body">
                <b-field
                  label="Texte à afficher"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-input
                    type="text"
                    v-model="linkEditorTextHolder"
                    size="is-small"
                    placeholder="Texte du lien"
                  >
                  </b-input>
                </b-field>

                <b-field
                  label="Adresse"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-input
                    type="text"
                    v-model="linkEditorLinkHolder"
                    size="is-small"
                    placeholder="Adresse du lien"
                  >
                  </b-input>
                </b-field>
              </section>
              <footer
                class="
                  modal-card-foot
                  is-flex is-flex-direction-row is-justify-content-space-between
                "
              >
                <b-button
                  size="is-small"
                  label="Valider"
                  type="is-primary"
                  @click="validateLinkEdit()"
                />
                <b-button
                  v-if="!editorFunctionsActiveStatuses.link"
                  size="is-small"
                  label="Annuler"
                  type="is-danger"
                  outlined
                  @click="linkEditorModalActive = false"
                ></b-button>
                <b-button
                  v-else
                  size="is-small"
                  label="Supprimer le lien"
                  type="is-danger"
                  outlined
                  @click="deleteLinkEdit()"
                ></b-button>
              </footer>
            </div>
          </div>
          <!-- END: Modal Editor Link -->

          <!-- Editor -->
          <editor-content
            id="editor-content-main-pane"
            :editor="editor"
            :class="[
              'is-flex-grow-5',
              { 'editor-disabled': linkEditorModalActive },
            ]"
          />
          <!-- END: Editor -->

          <!-- Footer -->
          <div
            v-if="showFooter"
            id="editor-content-footer-pane"
            :class="[
              'is-flex',
              'is-flex-direction-row',
              'is-justify-content-flex-start',
              { 'editor-disabled': linkEditorModalActive },
            ]"
          >
            <span class="ml-2"
              >{{ this.editorFunctionsCharacterStatuses.wordCount }} mot{{
                this.editorFunctionsCharacterStatuses.wordCount > 1 ? "s" : ""
              }}</span
            >
          </div>
          <!-- END: Footer -->
        </div>
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "nuxt-property-decorator";
import { Editor, EditorContent, BubbleMenu } from "@tiptap/vue-2";
import ImageSmallEditor from "~/components/hpf_image/ImageSmallEditor.vue";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import TextAlign from "@tiptap/extension-text-align";
import TextStyle from "@tiptap/extension-text-style";
import FontFamily from "@tiptap/extension-font-family";
import CharacterCount from "@tiptap/extension-character-count";
import Table from "@tiptap/extension-table";
import TableRow from "@tiptap/extension-table-row";
import TableCell from "@tiptap/extension-table-cell";
import TableHeader from "@tiptap/extension-table-header";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";
import { Indent } from "~/utils/tiptap_extensions/tiptap_indent";
import { FontSize } from "~/utils/tiptap_extensions/tiptap_font_size";
import { ImageHPFData } from "@/types/images";
import TipTapImageEditor from "~/utils/tiptap_extensions/tiptap_node_image_hpf";

@Component({
  name: "TipTapEditor",
  components: {
    EditorContent,
    ImageSmallEditor,
    BubbleMenu,
  },
})
export default class extends Vue {
  //#region Props
  @Prop({ default: true }) private showFooter!: boolean;
  @Prop({ default: "" }) private placeholder!: string;
  //#endregion

  //#region Datas

  private editor: Editor | null = null;
  private images: ImageHPFData[] = [];
  // Timer Editor update
  private timerThrottleId: number = 0;

  //#region Toolbar
  private menusStyle: any = [
    { icon: "heading", text: "Titre 1", action: "h1" },
    { icon: "heading", text: "Titre 2", action: "h2" },
    { icon: "heading", text: "Titre 3", action: "h3" },
    { icon: "heading", text: "Titre 4", action: "h4" },
    { icon: "heading", text: "Titre 5", action: "h5" },
    { icon: "heading", text: "Titre 6", action: "h6" },
    { icon: "paragraph", text: "Paragraphe", action: "p" },
  ];
  private menusFontSize: number[] = [8, 10, 12, 14, 16, 18, 24, 36];
  private menusFontFamily: string[] = [
    "Arial",
    "Calibri",
    "Tahoma",
    "Times new roman",
  ];
  //#endregion

  //#region Editor Link Modal
  private linkEditorModalActive: boolean = false;
  private linkEditorTextHolder: string = "";
  private linkEditorLinkHolder: string = "";
  //#endregion

  //#region Editor status
  // Cache des status de l'éditeur (actives)
  private editorFunctionsActiveSettings: { [key: string]: Function } = {
    h1: (editor: Editor): boolean => editor.isActive("heading", { level: 1 }),
    h2: (editor: Editor): boolean => editor.isActive("heading", { level: 2 }),
    h3: (editor: Editor): boolean => editor.isActive("heading", { level: 3 }),
    h4: (editor: Editor): boolean => editor.isActive("heading", { level: 4 }),
    h5: (editor: Editor): boolean => editor.isActive("heading", { level: 5 }),
    h6: (editor: Editor): boolean => editor.isActive("heading", { level: 6 }),
    paragraph: (editor: Editor): boolean => editor.isActive("paragraph"),

    bold: (editor: Editor): boolean => editor.isActive("bold"),
    italic: (editor: Editor): boolean => editor.isActive("italic"),
    underline: (editor: Editor): boolean => editor.isActive("underline"),
    strike: (editor: Editor): boolean => editor.isActive("strike"),

    link: (editor: Editor): boolean => editor.isActive("link"),

    textAlignLeft: (editor: Editor): boolean =>
      editor.isActive({ textAlign: "left" }),
    textAlignCenter: (editor: Editor): boolean =>
      editor.isActive({ textAlign: "center" }),
    textAlignRight: (editor: Editor): boolean =>
      editor.isActive({ textAlign: "right" }),
    textAlignJustified: (editor: Editor): boolean =>
      editor.isActive({ textAlign: "justify" }),

    bulletList: (editor: Editor): boolean => editor.isActive("bulletList"),
    orderedList: (editor: Editor): boolean => editor.isActive("orderedList"),

    undo: (editor: Editor): boolean => editor.can().undo(),
    redo: (editor: Editor): boolean => editor.can().redo(),
  };

  // Cache des status de l'éditeur (Font)
  private editorFunctionsTextStyleSettings: { [key: string]: Function } = {
    fontSize: (editor: Editor): string => {
      if (editor?.getAttributes("textStyle").fontSize != undefined) {
        return editor?.getAttributes("textStyle").fontSize;
      } else {
        if (editor.isActive("heading", { level: 1 })) return "32px";
        else if (editor.isActive("heading", { level: 2 })) return "24px";
        else if (editor.isActive("heading", { level: 3 })) return "18px";
        else if (editor.isActive("heading", { level: 4 })) return "16px";
        else if (editor.isActive("heading", { level: 5 })) return "14px";
        else if (editor.isActive("heading", { level: 6 })) return "12px";
        else if (editor.isActive("paragraph")) return "16px";
        else return "16px";
      }
    },
    fontFamily: (editor: Editor): string => {
      if (editor?.getAttributes("textStyle").fontFamily != undefined) {
        return editor?.getAttributes("textStyle").fontFamily;
      } else {
        if (editor.isActive("textStyle", { fontFamily: "Arial" }))
          return "Arial";
        if (editor.isActive("textStyle", { fontFamily: "Calibri" }))
          return "Calibri";
        if (editor.isActive("textStyle", { fontFamily: "Tahoma" }))
          return "Tahoma";
        if (editor.isActive("textStyle", { fontFamily: "Times new roman" }))
          return "Times new roman";
        else return "Arial";
      }
    },
  };

  // Cache des status de l'éditeur (Link)
  private editorFunctionsMiscSettings: { [key: string]: Function } = {
    link: (editor: Editor): string => {
      return editor?.isActive("link") ? editor?.getAttributes("link").href : "";
    },
  };

  // Cache des status de l'éditeur (Character count extension)
  private editorFunctionsCharacterSettings: { [key: string]: Function } = {
    wordCount: (editor: Editor): number =>
      editor.storage.characterCount.words(),
    characterCount: (editor: Editor): number =>
      editor.storage.characterCount.characters(),
  };

  // Cache des status de l'éditeur (Tableau)
  private tableFunctionsActiveSettings: { [key: string]: Function } = {
    deleteTable: (editor: Editor): boolean => editor.can().deleteTable(),
    addColumnBefore: (editor: Editor): boolean =>
      editor.can().addColumnBefore(),
    addColumnAfter: (editor: Editor): boolean => editor.can().addColumnAfter(),
    deleteColumn: (editor: Editor): boolean => editor.can().deleteColumn(),
    addRowBefore: (editor: Editor): boolean => editor.can().addRowBefore(),
    addRowAfter: (editor: Editor): boolean => editor.can().addRowAfter(),
    deleteRow: (editor: Editor): boolean => editor.can().deleteRow(),
    mergeCells: (editor: Editor): boolean => editor.can().mergeCells(),
    splitCell: (editor: Editor): boolean => editor.can().splitCell(),
    toggleHeaderColumn: (editor: Editor): boolean =>
      editor.can().toggleHeaderColumn(),
    toggleHeaderRow: (editor: Editor): boolean =>
      editor.can().toggleHeaderRow(),
    toggleHeaderCell: (editor: Editor): boolean =>
      editor.can().toggleHeaderCell(),
  };

  // Cache des status de l'éditeur (actives)
  private editorFunctionsActiveStatuses: Record<string, boolean> = {
    h1: false,
    h2: false,
    h3: false,
    h4: false,
    h5: false,
    h6: false,
    paragraph: false,

    bold: false,
    italic: false,
    underline: false,
    strike: false,

    link: false,

    textAlignLeft: false,
    textAlignCenter: false,
    textAlignRight: false,
    textAlignJustified: false,

    bulletList: false,
    orderedList: false,

    deleteTable: false,
    addColumnBefore: false,
    addColumnAfter: false,
    deleteColumn: false,
    addRowBefore: false,
    addRowAfter: false,
    deleteRow: false,
    mergeCells: false,
    splitCell: false,
    toggleHeaderColumn: false,
    toggleHeaderRow: false,
    toggleHeaderCell: false,

    undo: false,
    redo: false,
  };

  // Cache des status de l'éditeur (Font) Status
  private editorFunctionsTextStyleStatuses: Record<string, string> = {
    fontFamily: "Arial",
    fontSize: "12px",
  };

  // Cache des status de l'éditeur (Character count extension) Status
  private editorFunctionsMiscStatuses: Record<string, string> = {
    link: "",
  };

  // Cache des status de l'éditeur (Font) Status
  private editorFunctionsCharacterStatuses: Record<string, number> = {
    wordCount: 0,
    characterCount: 0,
  };

  //#endregion

  //#endregion

  //#region Hooks
  mounted() {
    this.editor = new Editor({
      content: "",
      extensions: [
        StarterKit,
        TextStyle,
        //Image,
        Underline,
        TextAlign.configure({
          types: ["heading", "paragraph"],
        }),
        Indent,
        TipTapImageEditor,
        FontSize,
        FontFamily,
        Link.configure({
          openOnClick: false,
        }),
        CharacterCount,
        Table.configure({
          resizable: true,
        }),
        TableRow,
        TableHeader,
        TableCell,
        Placeholder.configure({
          placeholder: this.placeholder,
        }),
      ],
      editorProps: {
        attributes: {
          spellcheck: "true",
        },
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
            // Drop des images seulement autorisé
            if (
              e.dataTransfer &&
              e?.dataTransfer
                ?.getData("text/plain")
                .match(
                  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*\.(jpeg|jpg|png)$)/
                )
            ) {
              if (e.preventDefault) e.preventDefault();
              if (e.stopPropagation) e.stopPropagation();
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
              return true;
            }
            // Drag and Drop à l'intérieur de tiptap (sur les hpf_images, sur le texte)
            else if (
              e.dataTransfer &&
              (e?.dataTransfer?.getData("text/html").match(/^<hpf-image/) ||
                e?.dataTransfer
                  ?.getData("text/plain")
                  .match(/^(?!https?:\/\/)(?!file:\/\/).+$/))
            ) {
              return false;
            } else {
              this.toggleForbiddenDropAlert();
              return true;
            }
          },
        },
      },
    });

    // Bind custom update function
    this.editor.on("update", () => this.onEditorUpdated());
    this.editor.on("selectionUpdate", () => this.onEditorUpdated());

    // Configuration par défaut
    this.editor?.chain().focus().setParagraph().setFontFamily("Arial").run();
  }

  beforeDestroy() {
    this.editor?.destroy();
  }
  //#endregion

  //#region Computed
  get currentStyle() {
    if (this.editorFunctionsActiveStatuses.h1)
      return { icon: "heading", text: "Titre 1", action: "h1" };
    else if (this.editorFunctionsActiveStatuses.h2)
      return { icon: "heading", text: "Titre 2", action: "h2" };
    else if (this.editorFunctionsActiveStatuses.h3)
      return { icon: "heading", text: "Titre 3", action: "h3" };
    else if (this.editorFunctionsActiveStatuses.h4)
      return { icon: "heading", text: "Titre 4", action: "h4" };
    else if (this.editorFunctionsActiveStatuses.h5)
      return { icon: "heading", text: "Titre 5", action: "h5" };
    else if (this.editorFunctionsActiveStatuses.h6)
      return { icon: "heading", text: "Titre 6", action: "h6" };
    else return { icon: "paragraph", text: "Paragraphe", action: "p" };
  }
  //#endregion

  //#region Watchers
  // Ouverture de la modal-homemade
  @Watch("linkEditorModalActive")
  private async onlinkEditorModalActiveChanged() {
    if (this.linkEditorModalActive) {
      if (this.editor != null) {
        this.editor.chain().focus().extendMarkRange("link").run();
        const { view, state } = this.editor;
        const { from, to } = view.state.selection;
        const text = state.doc.textBetween(from, to, "");
        this.linkEditorTextHolder = text;
        this.linkEditorLinkHolder = this.editorFunctionsMiscStatuses.link;
      }
    }
  }
  //#endregion

  //#region Methods
  // Toggle Alert Drop interdit
  private toggleForbiddenDropAlert() {
    this.$buefy.toast.open({
      duration: 5000,
      message: `Non supporté par l'éditeur`,
      position: "is-bottom",
      type: "is-danger",
    });
  }

  private test() {
    console.log(this.editor?.getHTML());
  }

  // Ajout d'une image HPF
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

  // Actualisation de status en cache de l'éditeur, actualisation du contenu
  private calcEditorButtonsActiveStatuses() {

    // Emet l'évènement change
    this.$emit("change", this.editor?.getHTML());

    // Cache des status de l'éditeur (actives)
    const objectToReturn: Record<string, boolean> = {};
    for (const key in this.editorFunctionsActiveSettings) {
      if (key)
        objectToReturn[key] = this.editorFunctionsActiveSettings[key](
          this.editor
        );
    }
    // Cache des status de l'éditeur (Table)
    if (this.tableFunctionsActiveSettings.deleteTable(this.editor)) {
      objectToReturn.deleteTable = true;
      for (const key in this.tableFunctionsActiveSettings) {
        if (key)
          objectToReturn[key] = this.tableFunctionsActiveSettings[key](
            this.editor
          );
      }
    } else {
      for (const key in this.tableFunctionsActiveSettings) {
        if (key) objectToReturn[key] = false;
      }
    }
    this.editorFunctionsActiveStatuses = objectToReturn;

    // Cache des status de l'éditeur (Font)
    const textStyleToReturn: Record<string, string> = {};
    for (const key in this.editorFunctionsTextStyleSettings) {
      if (key)
        textStyleToReturn[key] = this.editorFunctionsTextStyleSettings[key](
          this.editor
        );
    }
    this.editorFunctionsTextStyleStatuses = textStyleToReturn;

    // Cache des status de l'éditeur (Link)
    const miscToReturn: Record<string, string> = {};
    for (const key in this.editorFunctionsMiscSettings) {
      if (key)
        miscToReturn[key] = this.editorFunctionsMiscSettings[key](this.editor);
    }
    this.editorFunctionsMiscStatuses = miscToReturn;

    // Cache des status de l'éditeur (Character count extension)
    const characterToReturn: Record<string, number> = {};
    for (const key in this.editorFunctionsCharacterSettings) {
      if (key)
        characterToReturn[key] = this.editorFunctionsCharacterSettings[key](
          this.editor
        );
    }
    this.editorFunctionsCharacterStatuses = characterToReturn;
  }

  // Déclenche l'actualisation du cache via un timer
  private onEditorUpdated() {
    clearTimeout(this.timerThrottleId);
    this.timerThrottleId = window.setTimeout(
      this.calcEditorButtonsActiveStatuses,
      100
    );
  }

  // Mise en forme d'un style dans l'éditeur
  private toggleStyle(action: string) {
    switch (action) {
      case "h1":
        this.editor?.chain().focus().toggleHeading({ level: 1 }).run();
        break;
      case "h2":
        this.editor?.chain().focus().toggleHeading({ level: 2 }).run();
        break;
      case "h3":
        this.editor?.chain().focus().toggleHeading({ level: 3 }).run();
        break;
      case "h4":
        this.editor?.chain().focus().toggleHeading({ level: 4 }).run();
        break;
      case "h5":
        this.editor?.chain().focus().toggleHeading({ level: 5 }).run();
        break;
      case "h6":
        this.editor?.chain().focus().toggleHeading({ level: 6 }).run();
        break;
      case "p":
        this.editor?.chain().focus().setParagraph().run();
        break;
    }
  }

  // Mise à jour d'une taille de police dans l'éditeur
  private toggleFontSize(fontSize: number) {
    this.editor
      ?.chain()
      .focus()
      .setFontSize(fontSize + "px")
      .run();
    this.calcEditorButtonsActiveStatuses();
  }

  // Mise à jour d'une police dans l'éditeur
  private toggleFontFamily(fontFamily: string) {
    this.editor?.chain().focus().setFontFamily(fontFamily).run();
    this.calcEditorButtonsActiveStatuses();
  }

  // Ajout d'un lien hypertexte
  private validateLinkEdit() {
    this.linkEditorModalActive = false;
    if (this.editor != null) {
      const { view } = this.editor;
      const { from, to } = view.state.selection;
      this.editor
        ?.chain()
        .focus()
        .extendMarkRange("link")
        .setLink({ href: this.linkEditorLinkHolder })
        .command(({ tr }) => {
          tr.insertText(this.linkEditorTextHolder, from, to);
          return true;
        })
        .run();
    }
  }

  // Suppression du lien hypertexte
  private deleteLinkEdit() {
    this.linkEditorModalActive = false;
    this.editor?.chain().focus().extendMarkRange("link").unsetLink().run();
  }

  // Où doit apparaitre le Bubble Menu
  private bubbleMenuShouldShow() {
    if (this.editor != null) {
      const { view, state } = this.editor;
      const { from, to } = view.state.selection;
      const text = state.doc.textBetween(from, to, "");
      return (
        !this.linkEditorModalActive &&
        text.length > 0 &&
        (this.editorFunctionsActiveStatuses.h1 ||
          this.editorFunctionsActiveStatuses.h2 ||
          this.editorFunctionsActiveStatuses.h3 ||
          this.editorFunctionsActiveStatuses.h4 ||
          this.editorFunctionsActiveStatuses.h5 ||
          this.editorFunctionsActiveStatuses.h6 ||
          this.editorFunctionsActiveStatuses.paragraph ||
          this.editorFunctionsActiveStatuses.link)
      );
    }
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
  // border: 1px solid #CCCCCC !important;
  // border-radius: 0rem !important;
  background-color: #fff;
  height: 100%;
  width: 100%;
  min-width: 300px;
  .button.is-primary,
  .button.is-danger {
    border-radius: 0.5rem !important;
  }
  .button.is-primary:not(.is-hovered) {
    border-color: transparent !important;
  }
  .editor-disabled {
    background-color: rgba(10, 10, 10, 0.7) !important;
    pointer-events: none !important;
    cursor: not-allowed !important;
  }
  #editor-header {
    border-bottom: 3px solid $primary !important;
    //border-bottom: 1px solid #DBDBDB !important;
    background-color: #f5f5f5;
    padding: 4px 6px;
    border-top-left-radius: 0.57rem !important;
    border-top-right-radius: 0.57rem !important;
    gap: 5px;
    .vertical-line {
      border-radius: 0.75rem !important;
      border-left: 2px solid $primary-light;
      height: 100%;
    }
  }
  #editor-content {
    max-height: 100%;
    #editor-bubble-menu {
      background: #f5f5f5;
      border: 2px solid $primary !important;
      border-radius: 0.57rem !important;
      padding: 3px;
    }
    #editor-content-main-pane {
      overflow-y: auto;
      height: 250px;
      .ProseMirror {
        //background-color: #f3e5a9;
        min-height: 100%;
        padding: 4px;
        //border-bottom-left-radius: 0.75rem !important;
        ul,
        ol {
          padding: 0 1rem;
        }
        ul {
          list-style-type: disc !important;
        }
        hr {
          margin: 1rem 2rem;
          background-color: #4a4a4a;
          height: 2px;
        }
        h1 {
          display: block;
          font-size: 2em;
          margin-top: 0.67em;
          margin-bottom: 0.67em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
        h2 {
          display: block;
          font-size: 1.5em;
          margin-top: 0.83em;
          margin-bottom: 0.83em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
        h3 {
          display: block;
          font-size: 1.125em;
          margin-top: 1em;
          margin-bottom: 1em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
        h4 {
          display: block;
          margin-top: 1.33em;
          margin-bottom: 1.33em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
        h5 {
          display: block;
          font-size: 0.875em;
          margin-top: 1.67em;
          margin-bottom: 1.67em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
        h6 {
          display: block;
          font-size: 0.75em;
          margin-top: 2.33em;
          margin-bottom: 2.33em;
          margin-left: 0;
          margin-right: 0;
          font-weight: bold;
        }
      }
      .ProseMirror p.is-editor-empty:first-child::before {
        content: attr(data-placeholder);
        float: left;
        color: #adb5bd;
        pointer-events: none;
        height: 0;
      }
    }
    #editor-content-footer-pane {
      //border-top: 1px solid #dbdbdb !important;
      border-top: 2px solid $primary-light !important;
      border-bottom-left-radius: 0.57rem !important;
      border-bottom-right-radius: 0.57rem !important;
      background: #f5f5f5;
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
.editor-modal-container {
  width: 100%;
  height: 96%;
  position: absolute;
  text-align: center;
}
.editor-modal-card {
  display: inline-block;
  border: 3px solid $primary !important;
  border-radius: 0.75rem !important;
  width: 90%;
  max-width: 350px;
  margin-top: 40px;
  .modal-card-title {
    font-size: 0.95rem;
  }
  .modal-card-head,
  .modal-card-body,
  .modal-card-foot {
    padding: 10px;
  }
  .modal-card-head {
    border-top-left-radius: 0.6rem !important;
    border-top-right-radius: 0.6rem !important;
  }
  .modal-card-foot {
    border-bottom-left-radius: 0.6rem !important;
    border-bottom-right-radius: 0.6rem !important;
  }
}
</style>