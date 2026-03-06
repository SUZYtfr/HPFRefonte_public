<template>
  <div :class="[config.fixedHeight ? 'editor-height' : '']">
    <!-- Editor -->
    <div
      v-if="editor"
      id="editor"
      :class="['is-flex', 'is-flex-direction-column', 'is-justify-content-flex-start', 'editor-borders']"
    >
      <!-- Toolbar -->
      <Transition>
        <div
          v-if="config.fixedHeight || text || editorIsFocused"
          id="editor-header"
          :class="[
            'is-flex',
            'is-flex-direction-row',
            'is-justify-content-flex-start',
            'is-flex-wrap-wrap',
            { 'editor-disabled': linkEditorModalActive },
            { 'one-line-toolbar': config.oneLineToolbar },
          ]"
        >
          <!-- Menu burger regroupant toutes les fonctionnalités masqués dans le tooltip -->
          <BTooltip
            v-if="config.oneLineToolbar"
            type="is-light"
            :triggers="['click']"
            :auto-close="['outside', 'escape']"
            position="is-left"
            style="position: absolute; left: 21px"
          >
            <template #content>
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Bold"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="bold"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
                @click="editor.chain().focus().toggleBold().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Bold"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="italic"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
                @click="editor.chain().focus().toggleItalic().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Underline"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="underline"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
                @click="editor.chain().focus().toggleUnderline().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Strikethrough"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="strikethrough"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.strike }"
                @click="editor.chain().focus().toggleStrike().run()"
              />
              <div v-if="toolBarButtonsTooltipVisibility.Strikethrough" class="py-1">
                <div class="vertical-line"></div>
              </div>
              <BButton
                v-if="toolBarButtonsTooltipVisibility.AlignLeft"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="align-left"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
                @click="editor.chain().focus().setTextAlign('left').run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.AlignCenter"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="align-center"
                :class="{
                  'is-hovered': editorFunctionsActiveStatuses.textAlignCenter,
                }"
                @click="editor.chain().focus().setTextAlign('center').run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.AlignRight"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="align-right"
                :class="{
                  'is-hovered': editorFunctionsActiveStatuses.textAlignRight,
                }"
                @click="editor.chain().focus().setTextAlign('right').run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.AlignJustify"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="align-justify"
                :class="{
                  'is-hovered': editorFunctionsActiveStatuses.textAlignJustified,
                }"
                @click="editor.chain().focus().setTextAlign('justify').run()"
              />
              <div v-if="toolBarButtonsTooltipVisibility.AlignJustify" class="py-1">
                <div class="vertical-line"></div>
              </div>
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Indent"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="indent"
                @click="editor.chain().focus().indent().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Outdent"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="outdent"
                @click="editor.chain().focus().outdent().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.ListUl"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="list-ul"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.bulletList }"
                @click="editor.chain().focus().toggleBulletList().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.ListOl"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="list-ol"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.orderedList }"
                @click="editor.chain().focus().toggleOrderedList().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Undo"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="undo"
                :disabled="!editorFunctionsActiveStatuses.undo"
                @click="editor.chain().focus().undo().run()"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Redo"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="redo"
                :disabled="!editorFunctionsActiveStatuses.redo"
                @click="editor.chain().focus().redo().run()"
              />
              <div v-if="toolBarButtonsTooltipVisibility.Redo" class="py-1">
                <div class="vertical-line"></div>
              </div>
              <BDropdown v-if="toolBarButtonsTooltipVisibility.TextStyle" aria-role="list" :mobile-modal="false">
                <template #trigger="{ active }">
                  <BButton
                    type="is-primary"
                    outlined
                    size="is-small"
                    icon-pack="fas"
                    :icon-left="currentStyle().icon"
                    :label="currentStyle().text"
                    :icon-right="active ? 'angle-up' : 'angle-down'"
                  />
                </template>
                <BDropdownItem v-for="(menu, index) in menusStyle" :key="index" :value="menu" aria-role="listitem">
                  <div class="media" @click="toggleStyle(menu.action)">
                    <BIcon class="media-left" :icon="menu.icon" />
                    <div class="media-content">
                      <h3>{{ menu.text }}</h3>
                    </div>
                  </div>
                </BDropdownItem>
              </BDropdown>
              <BDropdown v-if="toolBarButtonsTooltipVisibility.TextHeight" aria-role="list" :mobile-modal="false">
                <template #trigger="{ active }">
                  <BButton
                    type="is-primary"
                    outlined
                    size="is-small"
                    icon-pack="fas"
                    icon-left="text-height"
                    :label="editorFunctionsTextStyleStatuses.fontSize"
                    :icon-right="active ? 'angle-up' : 'angle-down'"
                  />
                </template>
                <BDropdownItem
                  v-for="(fontSize, index) in menusFontSize"
                  :key="index"
                  :value="fontSize"
                  aria-role="listitem"
                >
                  <div class="media" @click="changeFontSize(fontSize)">
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
                </BDropdownItem>
              </BDropdown>
              <BDropdown v-if="toolBarButtonsTooltipVisibility.Font" aria-role="list" :mobile-modal="false">
                <template #trigger="{ active }">
                  <BButton
                    type="is-primary"
                    outlined
                    size="is-small"
                    icon-pack="fas"
                    icon-left="font"
                    :label="editorFunctionsTextStyleStatuses.fontFamily"
                    :icon-right="active ? 'angle-up' : 'angle-down'"
                  />
                </template>
                <BDropdownItem
                  v-for="(fontFamily, index) in menusFontFamily"
                  :key="index"
                  :value="fontFamily"
                  aria-role="listitem"
                >
                  <div class="media" @click="changeFontFamily(fontFamily)">
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
                </BDropdownItem>
              </BDropdown>
              <div v-if="toolBarButtonsTooltipVisibility.Font" class="py-1">
                <div class="vertical-line"></div>
              </div>
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Image && config.canUseImage"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="image"
                @click="addHPFImage(null, null, null, null)"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.Link"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="link"
                @click="linkEditorModalActive = true"
              />
              <BButton
                v-if="toolBarButtonsTooltipVisibility.GripLines"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="grip-lines"
                @click="editor.chain().focus().setHorizontalRule().run()"
              />
            </template>
            <BButton
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="bars"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
              @click="editor.chain().focus().setTextAlign('left').run()"
            />
          </BTooltip>
          <!-- Toolbar, sur une ou plusieurs lignes selon la largeur -->
          <BButton
            ref="btn-bold"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="bold"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
            @click="editor.chain().focus().toggleBold().run()"
          />
          <BButton
            ref="btn-italic"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="italic"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
            @click="editor.chain().focus().toggleItalic().run()"
          />
          <BButton
            ref="btn-underline"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="underline"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
            @click="editor.chain().focus().toggleUnderline().run()"
          />
          <BButton
            ref="btn-strikethrough"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="strikethrough"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.strike }"
            @click="editor.chain().focus().toggleStrike().run()"
          />
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BButton
            ref="btn-align-left"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="align-left"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
            @click="editor.chain().focus().setTextAlign('left').run()"
          />
          <BButton
            ref="btn-align-center"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="align-center"
            :class="{
              'is-hovered': editorFunctionsActiveStatuses.textAlignCenter,
            }"
            @click="editor.chain().focus().setTextAlign('center').run()"
          />
          <BButton
            ref="btn-align-right"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="align-right"
            :class="{
              'is-hovered': editorFunctionsActiveStatuses.textAlignRight,
            }"
            @click="editor.chain().focus().setTextAlign('right').run()"
          />
          <BButton
            ref="btn-align-justify"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="align-justify"
            :class="{
              'is-hovered': editorFunctionsActiveStatuses.textAlignJustified,
            }"
            @click="editor.chain().focus().setTextAlign('justify').run()"
          />
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BButton
            ref="btn-indent"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="indent"
            @click="editor.chain().focus().indent().run()"
          />
          <BButton
            ref="btn-outdent"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="outdent"
            @click="editor.chain().focus().outdent().run()"
          />
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BButton
            ref="btn-list-ul"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="list-ul"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.bulletList }"
            @click="editor.chain().focus().toggleBulletList().run()"
          />
          <BButton
            ref="btn-list-ol"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="list-ol"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.orderedList }"
            @click="editor.chain().focus().toggleOrderedList().run()"
          />
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BButton
            ref="btn-undo"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="undo"
            :disabled="!editorFunctionsActiveStatuses.undo"
            @click="editor.chain().focus().undo().run()"
          />
          <BButton
            ref="btn-redo"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="redo"
            :disabled="!editorFunctionsActiveStatuses.redo"
            @click="editor.chain().focus().redo().run()"
          />
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BDropdown aria-role="list" :mobile-modal="false">
            <template #trigger="{ active }">
              <BButton
                ref="btn-textstyle"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                :icon-left="currentStyle().icon"
                :label="currentStyle().text"
                :icon-right="active ? 'angle-up' : 'angle-down'"
              />
            </template>
            <BDropdownItem v-for="(menu, index) in menusStyle" :key="index" :value="menu" aria-role="listitem">
              <div class="media" @click="toggleStyle(menu.action)">
                <BIcon class="media-left" :icon="menu.icon" />
                <div class="media-content">
                  <h3>{{ menu.text }}</h3>
                </div>
              </div>
            </BDropdownItem>
          </BDropdown>
          <BDropdown aria-role="list" :mobile-modal="false">
            <template #trigger="{ active }">
              <BButton
                ref="btn-textheight"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="text-height"
                :label="editorFunctionsTextStyleStatuses.fontSize"
                :icon-right="active ? 'angle-up' : 'angle-down'"
              />
            </template>
            <BDropdownItem
              v-for="(fontSize, index) in menusFontSize"
              :key="index"
              :value="fontSize"
              aria-role="listitem"
            >
              <div class="media" @click="changeFontSize(fontSize)">
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
            </BDropdownItem>
          </BDropdown>
          <BDropdown aria-role="list" :mobile-modal="false">
            <template #trigger="{ active }">
              <BButton
                ref="btn-font"
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="font"
                :label="editorFunctionsTextStyleStatuses.fontFamily"
                :icon-right="active ? 'angle-up' : 'angle-down'"
              />
            </template>
            <BDropdownItem
              v-for="(fontFamily, index) in menusFontFamily"
              :key="index"
              :value="fontFamily"
              aria-role="listitem"
            >
              <div class="media" @click="changeFontFamily(fontFamily)">
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
            </BDropdownItem>
          </BDropdown>
          <div class="py-1">
            <div class="vertical-line"></div>
          </div>
          <BButton
            v-if="config.canUseImage"
            ref="btn-image"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="image"
            @click="addHPFImage(null, null, null, null)"
          />
          <BButton
            ref="btn-link"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="link"
            @click="linkEditorModalActive = true"
          />
          <BButton
            ref="btn-grip-lines"
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="grip-lines"
            @click="editor.chain().focus().setHorizontalRule().run()"
          />
          <!-- <div class="py-1">
            <div class="vertical-line" />
          </div>
          <div class="py-1">
            <div class="vertical-line" />
          </div>
          <BButton
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="code"
            @click="test()"
          ></BButton> -->
        </div>
      </Transition>
      <!-- END: ToolBar -->
      <div id="editor-content" class="is-flex-grow-5 is-flex is-flex-direction-row is-justify-content-flex-start">
        <div class="is-flex-grow-5 is-flex is-flex-direction-column is-justify-content-flex-start is-relative">
          <!-- Bubble menu -->
          <TiptapBubbleMenu
            id="editor-bubble-menu"
            :editor="editor"
            :tippy-options="{ duration: 100, placement: 'bottom' }"
            :should-show="bubbleMenuShouldShow"
          >
            <div>
              <BButton
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="bold"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
                @click="editor.chain().focus().toggleBold().run()"
              />
              <BButton
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="italic"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
                @click="editor.chain().focus().toggleItalic().run()"
              />
              <BButton
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="underline"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
                @click="editor.chain().focus().toggleUnderline().run()"
              />
              <BButton
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="link"
                @click="linkEditorModalActive = true"
              />
            </div>
          </TiptapBubbleMenu>
          <!-- END: Bubble menu -->

          <!-- Modal Editor Link -->
          <div v-if="linkEditorModalActive" class="editor-modal-container">
            <div class="editor-modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Insérer un lien hypertexte</p>
                <button type="button" class="delete" @click="linkEditorModalActive = false"></button>
              </header>
              <section class="modal-card-body">
                <BField label="Texte à afficher" label-position="on-border" custom-class="has-text-primary">
                  <BInput v-model="linkEditorTextHolder" type="text" size="is-small" placeholder="Texte du lien" />
                </BField>

                <BField label="Adresse" label-position="on-border" custom-class="has-text-primary">
                  <BInput v-model="linkEditorLinkHolder" type="text" size="is-small" placeholder="Adresse du lien" />
                </BField>
              </section>
              <footer class="modal-card-foot is-flex is-flex-direction-row is-justify-content-space-between">
                <BButton size="is-small" label="Valider" type="is-primary" @click="validateLinkEdit()" />
                <BButton
                  v-if="!editorFunctionsActiveStatuses.link"
                  size="is-small"
                  label="Annuler"
                  type="is-danger"
                  outlined
                  @click="linkEditorModalActive = false"
                />
                <BButton
                  v-else
                  size="is-small"
                  label="Supprimer le lien"
                  type="is-danger"
                  outlined
                  @click="deleteLinkEdit()"
                />
              </footer>
            </div>
          </div>
          <!-- END: Modal Editor Link -->

          <!-- Editor -->
          <TiptapEditorContent
            id="editor-content-main-pane"
            :editor
            :class="[
              'is-flex-grow-5',
              { 'editor-disabled': linkEditorModalActive },
              config.fixedHeight ? 'editor-content-main-pane-height' : '',
            ]"
            :style="{
              height: config.fixedHeight ? config.height.toString() + 'px' : '',
            }"
          />
          <!-- END: Editor -->

          <!-- Footer -->
          <div
            v-if="config.showFooter"
            id="editor-content-footer-pane"
            :class="[
              'is-flex',
              'is-flex-direction-row',
              'is-justify-content-flex-start',
              { 'editor-disabled': linkEditorModalActive },
            ]"
          >
            <span class="ml-2">{{ wordCount }} mot{{ wordCount || 0 > 1 ? "s" : "" }}</span>
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

<script setup lang="ts">
import type { TiptapEditor } from "#imports";
import type { ImageHPFData } from "@/types/images";
import type { TipTapEditorConfig } from "@/types/other";

// import ImageSmallEditor from "~/components/hpf_image/ImageSmallEditor.vue";
// import TipTapImageEditor from "~/utils/tiptap_extensions/tiptap_node_image_hpf";

interface Props {
  config?: TipTapEditorConfig;
}

const {
  config = {
    showFooter: false,
    fixedHeight: true,
    oneLineToolbar: false,
    canUseImage: false,
    height: 200,
    fontSize: 100,
    placeholder: "Écrire ici",
  },
} = defineProps<Props>();

const text = defineModel<string | null>("text");
const wordCount = defineModel<number>("wordCount", { default: 0 });

// NOTE editor.isFocused n'est pas réactif
// https://github.com/ueberdosis/tiptap/discussions/4971
const editorIsFocused = ref<boolean>(false);

// TODO finir d'installer et remettre les extensions en place
// et de ceci:
// handleDOMEvents: {
//     drop: (view, e) => {
//     // Drop des images seulement autorisé
//     if (
//         e.dataTransfer &&
//         e?.dataTransfer
//         ?.getData("text/plain")
//         .match(
//             /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*\.(jpeg|jpg|png)$)/
//         )
//     ) {
//         if (e.preventDefault) e.preventDefault();
//         if (e.stopPropagation) e.stopPropagation();
//         const imgURL = e?.dataTransfer?.getData("text/plain");
//         const img = new Image();
//         img.addEventListener("load", () => {
//         const coordinates = view.posAtCoords({
//             left: e.clientX,
//             top: e.clientY
//         });
//         this.addHPFImage(
//             imgURL,
//             img.naturalWidth,
//             img.naturalHeight,
//             coordinates?.pos
//         );
//         });
//         img.src = imgURL;
//         return true;
//     }
//     // Drag and Drop à l'intérieur de tiptap (sur les hpf_images, sur le texte)
//     else if (
//         e.dataTransfer &&
//         (e?.dataTransfer?.getData("text/html").match(/^<hpf-image/) ||
//         e?.dataTransfer
//             ?.getData("text/plain")
//             .match(/^(?!https?:\/\/)(?!file:\/\/).+$/))
//     ) {
//         return false;
//     } else {
//         this.toggleForbiddenDropAlert();
//         return true;
//     }
//     }
// }
// }
// TODO et de ceci ? (était désactivé)
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
const editor = useEditor({
  content: text.value,
  extensions: [
    TiptapStarterKit.configure({
      link: {
        openOnClick: false,
      },
    }),
    TiptapTextStyle,
    // Image,  // désactivé à l'origine
    TiptapTextAlign.configure({
      types: ["heading", "paragraph"],
    }),
    TiptapIndent,
    // TipTapImageEditor,
    TiptapFontSize,
    TiptapFontFamily,
    TiptapCharacterCount,
    TiptapTable.configure({
      resizable: true,
    }),
    TiptapTableRow,
    TiptapTableHeader,
    TiptapTableCell,
    TiptapPlaceholder.configure({
      placeholder: config.placeholder,
    }),
    TiptapQuote,
  ],
  editorProps: {
    attributes: {
      spellcheck: "true",
    },
  },
  onUpdate: ({ editor }) => {
    // Déclenche l'actualisation du cache via un timer
    clearTimeout(timerThrottleId.value);
    timerThrottleId.value = window.setTimeout(calcEditorButtonsActiveStatuses, 100);
    text.value = editor.getHTML();
    wordCount.value = editor.storage.characterCount.words();
  },
  onFocus: () => (editorIsFocused.value = true),
  onBlur: () => (editorIsFocused.value = false),
});

defineExpose({ editor: editor });

onBeforeUnmount(() => {
  unref(editor)?.destroy();
});

const images = ref<ImageHPFData[]>([]);
// Timer Editor update
const timerThrottleId = ref<number>(0);

const toolBarButtonsTooltipVisibility = ref({
  Bold: true,
  Italic: true,
  Underline: true,
  Strikethrough: true,
  AlignLeft: true,
  AlignCenter: true,
  AlignRight: true,
  AlignJustify: true,
  Indent: true,
  Outdent: true,
  ListUl: true,
  ListOl: true,
  Undo: true,
  Redo: true,
  TextStyle: true,
  TextHeight: true,
  Font: true,
  Image: true,
  Link: true,
  GripLines: true,
});

const menusStyle: { icon: string; text: string; action: string }[] = [
  { icon: "heading", text: "Titre 1", action: "h1" },
  { icon: "heading", text: "Titre 2", action: "h2" },
  { icon: "heading", text: "Titre 3", action: "h3" },
  { icon: "heading", text: "Titre 4", action: "h4" },
  { icon: "heading", text: "Titre 5", action: "h5" },
  { icon: "heading", text: "Titre 6", action: "h6" },
  { icon: "paragraph", text: "Paragraphe", action: "p" },
];

const menusFontSize: number[] = [8, 10, 12, 14, 16, 18, 24, 36];
const menusFontFamily: string[] = ["Arial", "Calibri", "Tahoma", "Times new roman"];

const linkEditorModalActive = ref<boolean>(false);
const linkEditorTextHolder = ref<string>("");
const linkEditorLinkHolder = ref<string>("");

// Cache des status de l'éditeur (actives)
const editorFunctionsActiveSettings: { [key: string]: (editor: TiptapEditor) => boolean } = {
  h1: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 1 }),
  h2: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 2 }),
  h3: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 3 }),
  h4: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 4 }),
  h5: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 5 }),
  h6: (editor: TiptapEditor): boolean => editor.isActive("heading", { level: 6 }),
  paragraph: (editor: TiptapEditor): boolean => editor.isActive("paragraph"),

  bold: (editor: TiptapEditor): boolean => editor.isActive("bold"),
  italic: (editor: TiptapEditor): boolean => editor.isActive("italic"),
  underline: (editor: TiptapEditor): boolean => editor.isActive("underline"),
  strike: (editor: TiptapEditor): boolean => editor.isActive("strike"),

  link: (editor: TiptapEditor): boolean => editor.isActive("link"),

  textAlignLeft: (editor: TiptapEditor): boolean => editor.isActive({ textAlign: "left" }),
  textAlignCenter: (editor: TiptapEditor): boolean => editor.isActive({ textAlign: "center" }),
  textAlignRight: (editor: TiptapEditor): boolean => editor.isActive({ textAlign: "right" }),
  textAlignJustified: (editor: TiptapEditor): boolean => editor.isActive({ textAlign: "justify" }),

  bulletList: (editor: TiptapEditor): boolean => editor.isActive("bulletList"),
  orderedList: (editor: TiptapEditor): boolean => editor.isActive("orderedList"),

  undo: (editor: TiptapEditor): boolean => editor.can().undo(),
  redo: (editor: TiptapEditor): boolean => editor.can().redo(),
};

// Cache des status de l'éditeur (Font)
const editorFunctionsTextStyleSettings: { [key: string]: (editor: TiptapEditor) => string } = {
  fontSize: (editor: TiptapEditor): string => {
    if (editor?.getAttributes("textStyle").fontSize !== undefined) {
      return editor?.getAttributes("textStyle").fontSize;
    } else if (editor.isActive("heading", { level: 1 })) return "32px";
    else if (editor.isActive("heading", { level: 2 })) return "24px";
    else if (editor.isActive("heading", { level: 3 })) return "18px";
    else if (editor.isActive("heading", { level: 4 })) return "16px";
    else if (editor.isActive("heading", { level: 5 })) return "14px";
    else if (editor.isActive("heading", { level: 6 })) return "12px";
    else if (editor.isActive("paragraph")) return "16px";
    else return "16px";
  },
  fontFamily: (editor: TiptapEditor): string => {
    if (editor?.getAttributes("textStyle").fontFamily !== undefined) {
      return editor?.getAttributes("textStyle").fontFamily;
    } else {
      if (editor.isActive("textStyle", { fontFamily: "Arial" })) return "Arial";
      if (editor.isActive("textStyle", { fontFamily: "Calibri" })) return "Calibri";
      if (editor.isActive("textStyle", { fontFamily: "Tahoma" })) return "Tahoma";
      if (editor.isActive("textStyle", { fontFamily: "Times new roman" })) return "Times new roman";
      else return "Arial";
    }
  },
};

// Cache des status de l'éditeur (Link)
const editorFunctionsMiscSettings: { [key: string]: (editor: TiptapEditor) => string } = {
  link: (editor: TiptapEditor): string => {
    return editor?.isActive("link") ? editor?.getAttributes("link").href : "";
  },
};

// Cache des status de l'éditeur (Character count extension)
const editorFunctionsCharacterSettings: { [key: string]: (editor: TiptapEditor) => number } = {
  wordCount: (editor: TiptapEditor): number => editor.storage.characterCount.words(),
  characterCount: (editor: TiptapEditor): number => editor.storage.characterCount.characters(),
};

// Cache des status de l'éditeur (Tableau)
const tableFunctionsActiveSettings: { [key: string]: (editor: TiptapEditor) => boolean } = {
  deleteTable: (editor: TiptapEditor): boolean => editor.can().deleteTable(),
  addColumnBefore: (editor: TiptapEditor): boolean => editor.can().addColumnBefore(),
  addColumnAfter: (editor: TiptapEditor): boolean => editor.can().addColumnAfter(),
  deleteColumn: (editor: TiptapEditor): boolean => editor.can().deleteColumn(),
  addRowBefore: (editor: TiptapEditor): boolean => editor.can().addRowBefore(),
  addRowAfter: (editor: TiptapEditor): boolean => editor.can().addRowAfter(),
  deleteRow: (editor: TiptapEditor): boolean => editor.can().deleteRow(),
  mergeCells: (editor: TiptapEditor): boolean => editor.can().mergeCells(),
  splitCell: (editor: TiptapEditor): boolean => editor.can().splitCell(),
  toggleHeaderColumn: (editor: TiptapEditor): boolean => editor.can().toggleHeaderColumn(),
  toggleHeaderRow: (editor: TiptapEditor): boolean => editor.can().toggleHeaderRow(),
  toggleHeaderCell: (editor: TiptapEditor): boolean => editor.can().toggleHeaderCell(),
};

// Cache des status de l'éditeur (actives)
const editorFunctionsActiveStatuses = ref<Record<string, boolean>>({
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
});

// Cache des status de l'éditeur (Font) Status
const editorFunctionsTextStyleStatuses = ref<Record<string, string>>({
  fontFamily: "Arial",
  fontSize: "12px",
});

// Cache des status de l'éditeur (Character count extension) Status
const editorFunctionsMiscStatuses = ref<Record<string, string>>({
  link: "",
});

// Cache des status de l'éditeur (Font) Status
const editorFunctionsCharacterStatuses = ref<Record<string, number>>({
  wordCount: 0,
  characterCount: 0,
});

//     // Configuration par défaut
//     this.editor?.chain().focus().setParagraph().setFontFamily("Arial").run();

const currentStyle = (): { icon: string; text: string; action: string } => {
  if (editorFunctionsActiveStatuses.value.h1) return { icon: "heading", text: "Titre 1", action: "h1" };
  else if (editorFunctionsActiveStatuses.value.h2) return { icon: "heading", text: "Titre 2", action: "h2" };
  else if (editorFunctionsActiveStatuses.value.h3) return { icon: "heading", text: "Titre 3", action: "h3" };
  else if (editorFunctionsActiveStatuses.value.h4) return { icon: "heading", text: "Titre 4", action: "h4" };
  else if (editorFunctionsActiveStatuses.value.h5) return { icon: "heading", text: "Titre 5", action: "h5" };
  else if (editorFunctionsActiveStatuses.value.h6) return { icon: "heading", text: "Titre 6", action: "h6" };
  else return { icon: "paragraph", text: "Paragraphe", action: "p" };
};

// #region Watchers
// Ouverture de la modal-homemade
watch(linkEditorModalActive, () => {
  if (linkEditorModalActive.value) {
    editor.value!.chain().focus().extendMarkRange("link").run();
    const { view, state } = editor.value!;
    const { from, to } = view.state.selection;
    const text = state.doc.textBetween(from, to, "");
    linkEditorTextHolder.value = text;
    linkEditorLinkHolder.value = editorFunctionsMiscStatuses.value.link || "";
  }
});

// // #region Public Methods
// // Changer le contenu de l'éditeur
// public setContent(tiptapContent: TipTapEditorContent | null): void {
// if (tiptapContent != null)
//     this.editor?.commands.setContent(tiptapContent.content);
// else
//     this.editor?.commands.setContent("");
// // this.editor?.extensionStorage.hpfImage.images = tiptapContent.content_images;
// }

// // #region Private Methods
// // Toggle Alert Drop interdit
// private toggleForbiddenDropAlert(): void {
// this.$buefy.toast.open({
//     duration: 5000,
//     message: "Non supporté par l'éditeur",
//     position: "is-bottom",
//     type: "is-danger"
// });
// }

// TODO
// Ajout d'une image HPF
function addHPFImage(url: string | null, width: number | null, height: number | null, pos: any | null): void {
  // if ((this.config?.canUseImage ?? false) === false) return;
  // this.editor?.commands.insertContentAt(
  //     pos != null ? pos : this.editor.view.state.selection.$anchor.pos,
  //     "<hpf-image " +
  //     (url != null ? 'url="' + url + '"' : "") +
  //     (width != null
  //         ? 'defaultWidth="' + width + '" currentWidth="' + width + '" '
  //         : "") +
  //     (height != null
  //         ? 'defaultHeight="' + height + '" currentHeight="' + height + '" '
  //         : "") +
  //     'data-type="draggable-item"></hpf-image>'
  // );
}

// Actualisation de status en cache de l'éditeur, actualisation du contenu
function calcEditorButtonsActiveStatuses(): void {
  // Cache des status de l'éditeur (actives)
  const objectToReturn: Record<string, boolean> = {};
  for (const key in editorFunctionsActiveSettings) {
    if (key) objectToReturn[key] = editorFunctionsActiveSettings[key]!(editor.value!)!;
  }
  // Cache des status de l'éditeur (Table)
  if (tableFunctionsActiveSettings.deleteTable!(editor.value!)) {
    objectToReturn.deleteTable = true;
    for (const key in tableFunctionsActiveSettings) {
      if (key) objectToReturn[key] = tableFunctionsActiveSettings[key]!(editor.value!);
    }
  } else {
    for (const key in tableFunctionsActiveSettings) {
      if (key) objectToReturn[key] = false;
    }
  }
  editorFunctionsActiveStatuses.value = objectToReturn;

  // Cache des status de l'éditeur (Font)
  const textStyleToReturn: Record<string, string> = {};
  for (const key in editorFunctionsTextStyleSettings) {
    if (key) textStyleToReturn[key] = editorFunctionsTextStyleSettings[key]!(editor.value!);
  }
  editorFunctionsTextStyleStatuses.value = textStyleToReturn;

  // Cache des status de l'éditeur (Link)
  const miscToReturn: Record<string, string> = {};
  for (const key in editorFunctionsMiscSettings) {
    if (key) miscToReturn[key] = editorFunctionsMiscSettings[key]!(editor.value!);
  }
  editorFunctionsMiscStatuses.value = miscToReturn;

  // Cache des status de l'éditeur (Character count extension)
  const characterToReturn: Record<string, number> = {};
  for (const key in editorFunctionsCharacterSettings) {
    if (key) characterToReturn[key] = editorFunctionsCharacterSettings[key]!(editor.value!);
  }
  editorFunctionsCharacterStatuses.value = characterToReturn;
}

// Mise en forme d'un style dans l'éditeur
function toggleStyle(action: string): void {
  switch (action) {
    case "h1":
      editor?.value?.chain().focus().toggleHeading({ level: 1 }).run();
      break;
    case "h2":
      editor?.value?.chain().focus().toggleHeading({ level: 2 }).run();
      break;
    case "h3":
      editor?.value?.chain().focus().toggleHeading({ level: 3 }).run();
      break;
    case "h4":
      editor?.value?.chain().focus().toggleHeading({ level: 4 }).run();
      break;
    case "h5":
      editor?.value?.chain().focus().toggleHeading({ level: 5 }).run();
      break;
    case "h6":
      editor?.value?.chain().focus().toggleHeading({ level: 6 }).run();
      break;
    case "p":
      editor?.value?.chain().focus().setParagraph().run();
      break;
  }
}

// Mise à jour d'une taille de police dans l'éditeur
function changeFontSize(fontSize: number): void {
  editor.value
    ?.chain()
    .focus()
    .setFontSize(fontSize + "px")
    .run();
  calcEditorButtonsActiveStatuses();
}

// Mise à jour d'une police dans l'éditeur
function changeFontFamily(fontFamily: string): void {
  editor.value?.chain().focus().setFontFamily(fontFamily).run();
  calcEditorButtonsActiveStatuses();
}

// Ajout d'un lien hypertexte
function validateLinkEdit(): void {
  linkEditorModalActive.value = false;
  const { view } = editor.value!;
  const { from, to } = view.state.selection;
  editor.value
    ?.chain()
    .focus()
    .extendMarkRange("link")
    .setLink({ href: linkEditorLinkHolder.value })
    .command(({ tr }) => {
      tr.insertText(linkEditorTextHolder.value, from, to);
      return true;
    })
    .run();
}

// Suppression du lien hypertexte
function deleteLinkEdit(): void {
  linkEditorModalActive.value = false;
  editor?.value?.chain().focus().extendMarkRange("link").unsetLink().run();
}

// Où doit apparaitre le Bubble Menu
const bubbleMenuShouldShow = (): boolean => {
  return (
    !linkEditorModalActive.value &&
    (editorFunctionsActiveStatuses.value.h1 ||
      editorFunctionsActiveStatuses.value.h2 ||
      editorFunctionsActiveStatuses.value.h3 ||
      editorFunctionsActiveStatuses.value.h4 ||
      editorFunctionsActiveStatuses.value.h5 ||
      editorFunctionsActiveStatuses.value.h6 ||
      editorFunctionsActiveStatuses.value.paragraph ||
      editorFunctionsActiveStatuses.value.link ||
      false)
  );
};
</script>

<style lang="scss" scoped>
@use "@/assets/scss/custom_bulma_core.scss";

/* Basic editor styles */
.editor-height {
  height: 100%;
}
.editor-borders {
  border: 3px solid var(--primary) !important;
  border-radius: 0.75rem !important;
  // border: 1px solid #CCCCCC !important;
  // border-radius: 0rem !important;
}
#editor {
  background-color: #fff;
  height: 100%;
  width: 100%;
  min-width: 180px;
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
  .one-line-toolbar {
    height: 38px;
    overflow-y: hidden;
    padding-left: 41px !important;
  }
  #editor-header {
    border-bottom: 3px solid var(--primary) !important;
    // border-bottom: 1px solid #DBDBDB !important;
    background-color: #f5f5f5;
    padding: 4px 6px;
    border-top-left-radius: 0.57rem !important;
    border-top-right-radius: 0.57rem !important;
    gap: 5px;
    .vertical-line {
      border-radius: 0.75rem !important;
      border-left: 2px solid var(--primary-light);
      height: 100%;
    }
  }
  #editor-content {
    max-height: 100%;
    #editor-bubble-menu {
      background: #f5f5f5;
      border: 2px solid var(--primary) !important;
      border-radius: 0.57rem !important;
      padding: 3px;
    }
    .editor-content-main-pane-height {
      overflow-y: auto;
      height: 125px;
    }
    #editor-content-main-pane {
      :deep(.ProseMirror) {
        // background-color: #f3e5a9;
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
        blockquote {
          padding-left: 1rem;
          border-left: 3px solid rgba(#0d0d0d, 0.1);
        }
        p {
          margin-bottom: 0px !important;
        }
        p.is-editor-empty:first-child::before {
          content: attr(data-placeholder);
          float: left;
          color: #adb5bd;
          pointer-events: none;
          height: 0;
        }
      }
    }
    #editor-content-footer-pane {
      //border-top: 1px solid #dbdbdb !important;
      border-top: 2px solid var(--primary-light) !important;
      border-bottom-left-radius: 0.57rem !important;
      border-bottom-right-radius: 0.57rem !important;
      background: #f5f5f5;
    }
    #editor-content-right-pane {
      border-left: 3px solid var(--primary) !important;
      background-color: #ffffff;
      border-bottom-right-radius: 0.75rem;
      #editor-content-right-pane-content {
        padding: 4px;
        overflow-y: auto;
        height: 0px;
      }
      #editor-content-right-pane-footer {
        border-top: 3px dashed var(--primary) !important;
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
  border: 3px solid var(--primary) !important;
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

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
