<template>
  <div :class="[((config?.fixedHeight ?? true) ? 'editor-height' : '')]">
    <!-- Editor -->
    <div
      v-if="editor"
      id="editor"
      :class="['is-flex', 'is-flex-direction-column', 'is-justify-content-flex-start', ((config?.readOnly == false) ? 'editor-borders' : '')]"
    >
      <!-- Toolbar -->
      <div
        v-if="(config?.readOnly ?? false) == false"
        id="editor-header"
        :class="[
          'is-flex',
          'is-flex-direction-row',
          'is-justify-content-flex-start',
          'is-flex-wrap-wrap',
          { 'editor-disabled': linkEditorModalActive },
          { 'one-line-toolbar': (config?.oneLineToolbar ?? false) }
        ]"
      >
        <!-- Menu burger regroupant toutes les fonctionnalités masqués dans le tooltip -->
        <b-tooltip
          v-if="(config?.oneLineToolbar ?? false) == true"
          type="is-light"
          :triggers="['click']"
          :auto-close="['outside', 'escape']"
          position="is-left"
          style="position: absolute; left: 21px;"
        >
          <template #content>
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Bold"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="bold"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
              @click="editor?.chain().focus().toggleBold().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Bold"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="italic"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
              @click="editor?.chain().focus().toggleItalic().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Underline"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="underline"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
              @click="editor?.chain().focus().toggleUnderline().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Strikethrough"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="strikethrough"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.strike }"
              @click="editor?.chain().focus().toggleStrike().run()"
            />
            <div v-if="ToolBarButtonsTooltipVisibility.Strikethrough" class="py-1">
              <div class="vertical-line" />
            </div>
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.AlignLeft"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="align-left"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
              @click="editor?.chain().focus().setTextAlign('left').run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.AlignCenter"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="align-center"
              :class="{
                'is-hovered': editorFunctionsActiveStatuses.textAlignCenter,
              }"
              @click="editor?.chain().focus().setTextAlign('center').run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.AlignRight"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="align-right"
              :class="{
                'is-hovered': editorFunctionsActiveStatuses.textAlignRight,
              }"
              @click="editor?.chain().focus().setTextAlign('right').run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.AlignJustify"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="align-justify"
              :class="{
                'is-hovered': editorFunctionsActiveStatuses.textAlignJustified,
              }"
              @click="editor?.chain().focus().setTextAlign('justify').run()"
            />
            <div v-if="ToolBarButtonsTooltipVisibility.AlignJustify" class="py-1">
              <div class="vertical-line" />
            </div>
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Indent"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="indent"
              @click="editor?.chain().focus().indent().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Outdent"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="outdent"
              @click="editor?.chain().focus().outdent().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.ListUl"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="list-ul"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.bulletList }"
              @click="editor?.chain().focus().toggleBulletList().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.ListOl"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="list-ol"
              :class="{ 'is-hovered': editorFunctionsActiveStatuses.orderedList }"
              @click="editor?.chain().focus().toggleOrderedList().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Undo"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="undo"
              :disabled="!editorFunctionsActiveStatuses.undo"
              @click="editor?.chain().focus().undo().run()"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Redo"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="redo"
              :disabled="!editorFunctionsActiveStatuses.redo"
              @click="editor?.chain().focus().redo().run()"
            />
            <div v-if="ToolBarButtonsTooltipVisibility.Redo" class="py-1">
              <div class="vertical-line" />
            </div>
            <b-dropdown v-if="ToolBarButtonsTooltipVisibility.TextStyle" aria-role="list" :mobile-modal="false">
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
                  <b-icon class="media-left" :icon="menu.icon" />
                  <div class="media-content">
                    <h3>{{ menu.text }}</h3>
                  </div>
                </div>
              </b-dropdown-item>
            </b-dropdown>
            <b-dropdown v-if="ToolBarButtonsTooltipVisibility.TextHeight" aria-role="list" :mobile-modal="false">
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
                    editor?.chain().focus().setFontSize(fontSize + 'px').run()
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
            <b-dropdown v-if="ToolBarButtonsTooltipVisibility.Font" aria-role="list" :mobile-modal="false">
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
            <div v-if="ToolBarButtonsTooltipVisibility.Font" class="py-1">
              <div class="vertical-line" />
            </div>
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Image && (config?.canUseImage ?? false)"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="image"
              @click="addHPFImage(null, null, null, null)"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.Link"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="link"
              @click="linkEditorModalActive = true"
            />
            <b-button
              v-if="ToolBarButtonsTooltipVisibility.GripLines"
              type="is-primary"
              outlined
              size="is-small"
              icon-pack="fas"
              icon-left="grip-lines"
              @click="editor?.chain().focus().setHorizontalRule().run()"
            />
          </template>
          <b-button
            type="is-primary"
            outlined
            size="is-small"
            icon-pack="fas"
            icon-left="bars"
            :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
            @click="editor?.chain().focus().setTextAlign('left').run()"
          />
        </b-tooltip>
        <!-- Toolbar, sur une ou plusieurs lignes selon la largeur -->
        <b-button
          ref="btn-bold"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="bold"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
          @click="editor?.chain().focus().toggleBold().run()"
        />
        <b-button
          ref="btn-italic"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="italic"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
          @click="editor?.chain().focus().toggleItalic().run()"
        />
        <b-button
          ref="btn-underline"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="underline"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
          @click="editor?.chain().focus().toggleUnderline().run()"
        />
        <b-button
          ref="btn-strikethrough"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="strikethrough"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.strike }"
          @click="editor?.chain().focus().toggleStrike().run()"
        />
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-button
          ref="btn-align-left"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-left"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.textAlignLeft }"
          @click="editor?.chain().focus().setTextAlign('left').run()"
        />
        <b-button
          ref="btn-align-center"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-center"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignCenter,
          }"
          @click="editor?.chain().focus().setTextAlign('center').run()"
        />
        <b-button
          ref="btn-align-right"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-right"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignRight,
          }"
          @click="editor?.chain().focus().setTextAlign('right').run()"
        />
        <b-button
          ref="btn-align-justify"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="align-justify"
          :class="{
            'is-hovered': editorFunctionsActiveStatuses.textAlignJustified,
          }"
          @click="editor?.chain().focus().setTextAlign('justify').run()"
        />
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-button
          ref="btn-indent"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="indent"
          @click="editor?.chain().focus().indent().run()"
        />
        <b-button
          ref="btn-outdent"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="outdent"
          @click="editor?.chain().focus().outdent().run()"
        />
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-button
          ref="btn-list-ul"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="list-ul"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.bulletList }"
          @click="editor?.chain().focus().toggleBulletList().run()"
        />
        <b-button
          ref="btn-list-ol"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="list-ol"
          :class="{ 'is-hovered': editorFunctionsActiveStatuses.orderedList }"
          @click="editor?.chain().focus().toggleOrderedList().run()"
        />
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-button
          ref="btn-undo"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="undo"
          :disabled="!editorFunctionsActiveStatuses.undo"
          @click="editor?.chain().focus().undo().run()"
        />
        <b-button
          ref="btn-redo"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="redo"
          :disabled="!editorFunctionsActiveStatuses.redo"
          @click="editor?.chain().focus().redo().run()"
        />
        <div class="py-1">
          <div class="vertical-line" />
        </div>
        <b-dropdown aria-role="list" :mobile-modal="false">
          <template #trigger="{ active }">
            <b-button
              ref="btn-textstyle"
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
              <b-icon class="media-left" :icon="menu.icon" />
              <div class="media-content">
                <h3>{{ menu.text }}</h3>
              </div>
            </div>
          </b-dropdown-item>
        </b-dropdown>
        <b-dropdown aria-role="list" :mobile-modal="false">
          <template #trigger="{ active }">
            <b-button
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
          <b-dropdown-item
            v-for="(fontSize, index) in menusFontSize"
            :key="index"
            :value="fontSize"
            aria-role="listitem"
          >
            <div
              class="media"
              @click="
                editor?.chain().focus().setFontSize(fontSize + 'px').run()
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
          v-if="(config?.canUseImage ?? false)"
          ref="btn-image"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="image"
          @click="addHPFImage(null, null, null, null)"
        />
        <b-button
          ref="btn-link"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="link"
          @click="linkEditorModalActive = true"
        />
        <b-button
          ref="btn-gripLines"
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="grip-lines"
          @click="editor?.chain().focus().setHorizontalRule().run()"
        />
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
        id="editor-content"
        class="
          is-flex-grow-5
          is-flex
          is-flex-direction-row
          is-justify-content-flex-start
        "
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
            :should-show="bubbleMenuShouldShow"
          >
            <div v-if="(config?.readOnly ?? false) == false">
              <b-button
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="bold"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.bold }"
                @click="editor?.chain().focus().toggleBold().run()"
              />
              <b-button
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="italic"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.italic }"
                @click="editor?.chain().focus().toggleItalic().run()"
              />
              <b-button
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="underline"
                :class="{ 'is-hovered': editorFunctionsActiveStatuses.underline }"
                @click="editor?.chain().focus().toggleUnderline().run()"
              />
              <b-button
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="link"
                @click="linkEditorModalActive = true"
              />
            </div>
            <div v-else-if="((config?.canQuote ?? false) === true)">
              <b-button
                type="is-primary"
                outlined
                size="is-small"
                icon-pack="fas"
                icon-left="quote-right"
                @click="emitQuote()"
              />
            </div>
          </bubble-menu>
          <!-- END: Bubble menu -->

          <!-- Modal Editor Link -->
          <div v-if="linkEditorModalActive" class="editor-modal-container">
            <div class="editor-modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">
                  Insérer un lien hypertexte
                </p>
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
                    v-model="linkEditorTextHolder"
                    type="text"
                    size="is-small"
                    placeholder="Texte du lien"
                  />
                </b-field>

                <b-field
                  label="Adresse"
                  label-position="on-border"
                  custom-class="has-text-primary"
                >
                  <b-input
                    v-model="linkEditorLinkHolder"
                    type="text"
                    size="is-small"
                    placeholder="Adresse du lien"
                  />
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
                />
                <b-button
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
          <editor-content
            id="editor-content-main-pane"
            :editor="editor"
            :class="[
              'is-flex-grow-5',
              { 'editor-disabled': linkEditorModalActive },
              ((config?.fixedHeight ?? true) ? 'editor-content-main-pane-height' : ''),
              { 'disable-text-selection' : (((config?.readOnly ?? false) == true) && ((config.canQuote ?? false) == false)) }
            ]"
            :style="{
              height: ((config?.fixedHeight ?? true) ? ((config?.height ?? 125).toString() + 'px') : ''),
              fontSize: (config?.fontSize ?? 100) + '%',
            }"
          />
          <!-- END: Editor -->

          <!-- Footer -->
          <div
            v-if="config?.showFooter"
            id="editor-content-footer-pane"
            :class="[
              'is-flex',
              'is-flex-direction-row',
              'is-justify-content-flex-start',
              { 'editor-disabled': linkEditorModalActive },
            ]"
          >
            <span class="ml-2">{{ editorFunctionsCharacterStatuses.wordCount }} mot{{
              editorFunctionsCharacterStatuses.wordCount > 1 ? "s" : ""
            }}</span>
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
import { Editor, EditorContent, BubbleMenu } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import { Underline } from "@tiptap/extension-underline";
import { TextAlign } from "@tiptap/extension-text-align";
import { TextStyle } from "@tiptap/extension-text-style";
import { FontFamily } from "@tiptap/extension-font-family";
import { CharacterCount } from "@tiptap/extension-character-count";
import { Table } from "@tiptap/extension-table";
import { TableRow } from "@tiptap/extension-table-row";
import { TableCell } from "@tiptap/extension-table-cell";
import { TableHeader } from "@tiptap/extension-table-header";
import { Link } from "@tiptap/extension-link";
import { Placeholder } from "@tiptap/extension-placeholder";
import ImageSmallEditor from "~/components/hpf_image/ImageSmallEditor.vue";
import { Indent } from "~/utils/tiptap_extensions/tiptap_indent";
import { FontSize } from "~/utils/tiptap_extensions/tiptap_font_size";
import { ImageHPFData } from "@/types/images";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";
import TipTapImageEditor from "~/utils/tiptap_extensions/tiptap_node_image_hpf";
import { LimitedSelection } from "~/utils/tiptap_extensions/tiptap_limit_selection_mark";
import { BButton } from "buefy";

const { config } = defineProps<{
  config?: TipTapEditorConfig;
}>();

function toggleForbiddenDropAlert(): void {
  // TODO
  // this.$buefy.toast.open({
  //   duration: 5000,
  //   message: "Non supporté par l'éditeur",
  //   position: "is-bottom",
  //   type: "is-danger"
  // });
}

// Ajout d'une image HPF
function addHPFImage(
  url: string | null,
  width: number | null,
  height: number | null,
  pos: any | null
): void {
  if ((config?.canUseImage ?? false) === false) return;
  editor.value.commands.insertContentAt(
    pos != null ? pos : editor.value.view.state.selection.$anchor.pos,
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

// let editor: Editor | null = null;
let images: ImageHPFData[] = [];
// Timer Editor update
let timerThrottleId: number = 0;

// Timer resize
let timerThrottleResizeId: number = 0;

function emitQuote() {}

// #region Toolbar
let ToolBarButtonsTooltipVisibility = {
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
  GripLines: true
};

let menusStyle: any = [
  { icon: "heading", text: "Titre 1", action: "h1" },
  { icon: "heading", text: "Titre 2", action: "h2" },
  { icon: "heading", text: "Titre 3", action: "h3" },
  { icon: "heading", text: "Titre 4", action: "h4" },
  { icon: "heading", text: "Titre 5", action: "h5" },
  { icon: "heading", text: "Titre 6", action: "h6" },
  { icon: "paragraph", text: "Paragraphe", action: "p" }
];

let menusFontSize: number[] = [8, 10, 12, 14, 16, 18, 24, 36];
let menusFontFamily: string[] = [
  "Arial",
  "Calibri",
  "Tahoma",
  "Times new roman"
];

const linkEditorModalActive = ref(false);
let linkEditorTextHolder: string = "";
let linkEditorLinkHolder: string = "";

// Cache des status de l'éditeur (actives)
let editorFunctionsActiveSettings: { [key: string]: Function } = {
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
  redo: (editor: Editor): boolean => editor.can().redo()
};

// Cache des status de l'éditeur (Font)
let editorFunctionsTextStyleSettings: { [key: string]: Function } = {
  fontSize: (editor: Editor): string => {
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
  fontFamily: (editor: Editor): string => {
    if (editor?.getAttributes("textStyle").fontFamily !== undefined) {
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
  }
};

// Cache des status de l'éditeur (Link)
let editorFunctionsMiscSettings: { [key: string]: Function } = {
  link: (editor: Editor): string => {
    return editor?.isActive("link") ? editor?.getAttributes("link").href : "";
  }
};

// Cache des status de l'éditeur (Character count extension)
let editorFunctionsCharacterSettings: { [key: string]: Function } = {
  wordCount: (editor: Editor): number =>
    editor.storage.characterCount.words(),
  characterCount: (editor: Editor): number =>
    editor.storage.characterCount.characters()
};

// Cache des status de l'éditeur (Tableau)
let tableFunctionsActiveSettings: { [key: string]: Function } = {
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
    editor.can().toggleHeaderCell()
};

// Cache des status de l'éditeur (actives)
let editorFunctionsActiveStatuses = reactive<Record<string, boolean>>({
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
  redo: false
});

// Cache des status de l'éditeur (Font) Status
const editorFunctionsTextStyleStatuses = reactive<Record<string, string>>({
  fontFamily: "Arial",
  fontSize: "12px"
});

// Cache des status de l'éditeur (Character count extension) Status
const editorFunctionsMiscStatuses = reactive<Record<string, string>>({
  link: ""
});

// Cache des status de l'éditeur (Font) Status
const editorFunctionsCharacterStatuses = reactive<Record<string, number>>({
  wordCount: 0,
  characterCount: 0
});

const editor = useEditor({
  content: config?.defaultValue,
  extensions: [
      StarterKit,
      TextStyle,
      // Image,
      Underline,
      TextAlign.configure({
        types: ["heading", "paragraph"]
      }),
      Indent,
      TipTapImageEditor,
      FontSize,
      FontFamily,
      Link.configure({
        openOnClick: false
      }),
      CharacterCount,
      Table.configure({
        resizable: true
      }),
      TableRow,
      TableHeader,
      TableCell,
      Placeholder.configure({
        placeholder: config?.placeholder
      }),
      LimitedSelection.configure({
        HTMLAttributes: {
          class: "animate__animated animate__fast animate__flash"
        }
      })
    ],
    editorProps: {
      attributes: {
        spellcheck: "true"
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
                top: e.clientY
              });
              addHPFImage(
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
            toggleForbiddenDropAlert();
            return true;
          }
        }
      }
    }
})

onMounted(() => {
  // Configuration par défaut

  editor.value?.setEditable((config?.readOnly ?? false) === false);
  
  // Bind custom update function
  editor.value?.on("update", () => onEditorUpdated());
  editor.value?.on("selectionUpdate", () => onEditorUpdated());

  // Evénement pour gérer la selection limitée
  editor.value.view.dom.addEventListener("mouseup", () => {
    if ((config?.canQuote ?? false) === false) return;
    if (editor != null) {
      const selection = editor.value.state.selection;
      const maxSelectionLength = (config?.quoteLimit ?? 250);
      if (selection.empty) return; // La sélection est vide, aucune action nécessaire
      const { view } = editor.value;
      const { from, to } = view.state.selection;
      if ((to - from) > maxSelectionLength) {
        const newTo = from + maxSelectionLength;
        editor.value.chain().setTextSelection({ from: newTo, to: to }).focus().toggleLimitedSelection().setTextSelection({ from: from, to: newTo }).focus().run();
        const element = document.querySelector("limitedselection");
        element?.addEventListener("animationend", () => {
          editor.value.chain().setTextSelection({ from: newTo, to: to }).focus().toggleLimitedSelection().setTextSelection({ from: from, to: newTo }).focus().run();
        });
      }
    }
  });

  editor.value?.chain().focus().setParagraph().setFontFamily("Arial").run();

  // window.addEventListener("resize", this.detectWrappedItems);
  // this.detectWrappedItems();
})

onBeforeUnmount(() => {
  // window.removeEventListener("resize", this.detectWrappedItems);
  unref(editor).destroy();
});

const currentStyle = computed(() => {
  if (editorFunctionsActiveStatuses.h1)
    return { icon: "heading", text: "Titre 1", action: "h1" };
  else if (editorFunctionsActiveStatuses.h2)
    return { icon: "heading", text: "Titre 2", action: "h2" };
  else if (editorFunctionsActiveStatuses.h3)
    return { icon: "heading", text: "Titre 3", action: "h3" };
  else if (editorFunctionsActiveStatuses.h4)
    return { icon: "heading", text: "Titre 4", action: "h4" };
  else if (editorFunctionsActiveStatuses.h5)
    return { icon: "heading", text: "Titre 5", action: "h5" };
  else if (editorFunctionsActiveStatuses.h6)
    return { icon: "heading", text: "Titre 6", action: "h6" };
  else return { icon: "paragraph", text: "Paragraphe", action: "p" };
})

  // // Ouverture de la modal-homemade
  // @Watch("linkEditorModalActive")
  // private onlinkEditorModalActiveChanged(): void {
  //   if (this.linkEditorModalActive) {
  //     if (this.editor != null) {
  //       this.editor.chain().focus().extendMarkRange("link").run();
  //       const { view, state } = this.editor;
  //       const { from, to } = view.state.selection;
  //       const text = state.doc.textBetween(from, to, "");
  //       this.linkEditorTextHolder = text;
  //       this.linkEditorLinkHolder = this.editorFunctionsMiscStatuses.link;
  //     }
  //   }
  // }

  // // #region Public Methods
  // // Changer le contenu de l'éditeur
  // public setContent(tiptapContent: TipTapEditorContent | null): void {
  //   if (tiptapContent != null)
  //     this.editor?.commands.setContent(tiptapContent.content);
  //   else
  //     this.editor?.commands.setContent("");
  //   // this.editor?.extensionStorage.hpfImage.images = tiptapContent.content_images;
  // }

  // // Ajouter une quote
  // public setQuote(quote: string): void {
  //   // this.editor?.chain().focus().insertContent("[...] " + quote + "[...]").setBlockquote().enter().focus("end").run();
  //   this.editor?.chain().focus().enter().insertContent(quote).setBlockquote().run();
  //   this.editor?.commands.enter();
  //   this.editor?.commands.enter();
  // }

  // // #region Private Methods
  // // Toggle Alert Drop interdit
  // private toggleForbiddenDropAlert(): void {
  //   this.$buefy.toast.open({
  //     duration: 5000,
  //     message: "Non supporté par l'éditeur",
  //     position: "is-bottom",
  //     type: "is-danger"
  //   });
  // }

  // // #region Emit Function
  // public emitQuote(): void {
  //   if (this.editor != null) {
  //     const { view, state } = this.editor;
  //     const { from, to } = view.state.selection;
  //     // On check la longueur max émise
  //     let newTo = to;
  //     const maxSelectionLength = (this.config?.quoteLimit ?? 250);
  //     if ((to - from) > maxSelectionLength) newTo = from + maxSelectionLength;
  //     // Emet l'évènement quote
  //     this.$emit("quote", state.doc.textBetween(from, newTo, ""));
  //     this.editor.commands.setTextSelection(to);
  //     window?.getSelection()?.empty();
  //   }
  // }
  // // #endregion

// Actualisation de status en cache de l'éditeur, actualisation du contenu
function calcEditorButtonsActiveStatuses(): void {
  // Cache des status de l'éditeur (actives)
  // const objectToReturn: Record<string, boolean> = {};
  for (const key in editorFunctionsActiveSettings) {
    if (key)
    editorFunctionsActiveStatuses[key] = editorFunctionsActiveSettings[key](
        editor.value
      );
  }
  // Cache des status de l'éditeur (Table)
  if (tableFunctionsActiveSettings.deleteTable(editor)) {
    editorFunctionsActiveStatuses.deleteTable = true;
    for (const key in tableFunctionsActiveSettings) {
      if (key)
      editorFunctionsActiveStatuses[key] = tableFunctionsActiveSettings[key](
          editor
        );
    }
  } else {
    for (const key in tableFunctionsActiveSettings) {
      if (key) editorFunctionsActiveStatuses[key] = false;
    }
  }
  // editorFunctionsActiveStatuses = objectToReturn;

  // Cache des status de l'éditeur (Font)
  // const textStyleToReturn: Record<string, string> = {};
  for (const key in editorFunctionsTextStyleSettings) {
    if (key)
    editorFunctionsTextStyleStatuses[key] = editorFunctionsTextStyleSettings[key](
        editor
      );
  }
  // editorFunctionsTextStyleStatuses = textStyleToReturn;

  // Cache des status de l'éditeur (Link)
  // const miscToReturn: Record<string, string> = {};
  for (const key in editorFunctionsMiscSettings) {
    if (key)
    editorFunctionsMiscStatuses[key] = editorFunctionsMiscSettings[key](editor.value);
  }
  // editorFunctionsMiscStatuses = miscToReturn;

  // Cache des status de l'éditeur (Character count extension)
  // const characterToReturn: Record<string, number> = {};
  for (const key in editorFunctionsCharacterSettings) {
    if (key)
    editorFunctionsCharacterStatuses[key] = editorFunctionsCharacterSettings[key](
        editor
      );
  }
  // editorFunctionsCharacterStatuses = characterToReturn;

  // Emet l'évènement change
  // TODO utiliser useEmits
  // $emit("change", new TipTapEditorContent({
  //   content: this.editor?.getHTML(),
  //   wordcount: this.editorFunctionsCharacterStatuses.wordCount,
  //   content_images: this.editor?.extensionStorage.hpfImage.images
  // }));
}

// Déclenche l'actualisation du cache via un timer
function onEditorUpdated(): void {
  clearTimeout(timerThrottleId);
  timerThrottleId = window.setTimeout(
    calcEditorButtonsActiveStatuses,
    100
  );
}

// Mise en forme d'un style dans l'éditeur
function toggleStyle(action: string): void {
  switch (action) {
    case "h1":
      editor.value.chain().focus().toggleHeading({ level: 1 }).run();
      break;
    case "h2":
      editor.value.chain().focus().toggleHeading({ level: 2 }).run();
      break;
    case "h3":
      editor.value.chain().focus().toggleHeading({ level: 3 }).run();
      break;
    case "h4":
      editor.value.chain().focus().toggleHeading({ level: 4 }).run();
      break;
    case "h5":
      editor.value.chain().focus().toggleHeading({ level: 5 }).run();
      break;
    case "h6":
      editor.value.chain().focus().toggleHeading({ level: 6 }).run();
      break;
    case "p":
      editor.value.chain().focus().setParagraph().run();
      break;
  }
}

// Mise à jour d'une taille de police dans l'éditeur
function toggleFontSize(fontSize: number): void {
  editor.value
    .chain()
    .focus()
    .setFontSize(fontSize + "px")
    .run();
  calcEditorButtonsActiveStatuses();
}

// Mise à jour d'une police dans l'éditeur
function toggleFontFamily(fontFamily: string): void {
  editor.value.chain().focus().setFontFamily(fontFamily).run();
  calcEditorButtonsActiveStatuses();
}

// Ajout d'un lien hypertexte
function validateLinkEdit(): void {
  linkEditorModalActive.value = false;
  if (editor.value != null) {
    const { view } = editor.value;
    const { from, to } = view.state.selection;
    editor.value
      .chain()
      .focus()
      .extendMarkRange("link")
      .setLink({ href: linkEditorLinkHolder })
      .command(({ tr }) => {
        tr.insertText(linkEditorTextHolder, from, to);
        return true;
      })
      .run();
  }
}

// Suppression du lien hypertexte
function deleteLinkEdit(): void {
  linkEditorModalActive.value = false;
  editor.value.chain().focus().extendMarkRange("link").unsetLink().run();
}

// Où doit apparaitre le Bubble Menu
function bubbleMenuShouldShow(): boolean {
  if (editor != null) {
    if ((config?.readOnly ?? false) === true && (config?.canQuote ?? false) === false) return false;

    const { view, state } = editor.value;
    const { from, to } = view.state.selection;
    const text = state.doc.textBetween(from, to, "");
    return (
      !linkEditorModalActive.value &&
      text.length > 0 &&
      (editorFunctionsActiveStatuses.h1 ||
        editorFunctionsActiveStatuses.h2 ||
        editorFunctionsActiveStatuses.h3 ||
        editorFunctionsActiveStatuses.h4 ||
        editorFunctionsActiveStatuses.h5 ||
        editorFunctionsActiveStatuses.h6 ||
        editorFunctionsActiveStatuses.paragraph ||
        editorFunctionsActiveStatuses.link)
    );
  }
  return false;
}

const btnBold = useTemplateRef("btn-bold")
const btnItalic = useTemplateRef("btn-italic")
const btnUnderline = useTemplateRef("btn-underline")
const btnStrikethrough = useTemplateRef("btn-strikethrough")
const btnAlignLeft = useTemplateRef("btn-align-left")
const btnAlignCenter = useTemplateRef("btn-align-center")
const btnAlignRight = useTemplateRef("btn-align-right")
const btnAlignJustify = useTemplateRef("btn-align-justify")
const btnIndent = useTemplateRef("btn-indent")
const btnOutdent = useTemplateRef("btn-outdent")
const btnListUl = useTemplateRef("btn-list-ul")
const btnListOl = useTemplateRef("btn-list-ol")
const btnUndo = useTemplateRef("btn-undo")
const btnRedo = useTemplateRef("btn-redo")
const btnTextstyle = useTemplateRef("btn-textstyle")
const btnTextheight = useTemplateRef("btn-textheight")
const btnFont = useTemplateRef("btn-font")
const btnImage = useTemplateRef("btn-image")
const btnLink = useTemplateRef("btn-link")
// const btnGripLines = useTemplateRef("btn-grip-lines")


// Détecter le wrap des button de l'éditeur
function detectWrappedItems():void {
  clearTimeout(timerThrottleResizeId);
  timerThrottleResizeId = window.setTimeout(
    () => {
      console.log("Je doit passer une seule fois");
      const container = document.querySelector("#editor-header");
      const containerBottom = (container?.getBoundingClientRect()?.bottom ?? 0);
      if (container == null) return;
      ToolBarButtonsTooltipVisibility.Bold = (btnBold.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Italic = (btnItalic.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Underline = (btnUnderline.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Strikethrough = (btnStrikethrough.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.AlignLeft = (btnAlignLeft.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.AlignCenter = (btnAlignCenter.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.AlignRight = (btnAlignRight.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.AlignJustify = (btnAlignJustify.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Indent = (btnIndent.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Outdent = (btnOutdent.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.ListUl = (btnListUl.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.ListOl = (btnListOl.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Undo = (btnUndo.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Redo = (btnRedo.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.TextStyle = (btnTextstyle.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.TextHeight = (btnTextheight.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Font = (btnFont.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Image = (btnImage.value.$el.getBoundingClientRect()?.top > containerBottom);
      ToolBarButtonsTooltipVisibility.Link = (btnLink.value.$el.getBoundingClientRect()?.top > containerBottom);
      // ToolBarButtonsTooltipVisibility.GripLines = (btnGripLines.value.$el.getBoundingClientRect()?.top > containerBottom);
    },
    300
  );
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom_bulma_core.scss";

/* Basic editor styles */
.editor-height{
  height: 100%;
}
.editor-borders{
    border: 3px solid var(--primary) !important;
    border-radius: 0.75rem !important;
  // border: 1px solid #CCCCCC !important;
  // border-radius: 0rem !important;
  }
#editor {
  background-color: var(--scheme-main);
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
    //border-bottom: 1px solid #DBDBDB !important;
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
        blockquote {
          padding-left: 1rem;
          border-left: 3px solid rgba(#0D0D0D, 0.1);
        }
        limitedselection {
          background-color: #ef476f;
        }
        p {
          margin-bottom: 0px !important;
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
    .disable-text-selection {
          user-select: none; /* Désactiver la sélection de texte */
          pointer-events: none; /* Désactiver les interactions de pointeur */
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
</style>
