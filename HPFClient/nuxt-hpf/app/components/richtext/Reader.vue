<template>
  <!-- Rendu final quand le lecteur Tiptap est monté sur le client -->
  <div id="editor-content-main-pane">
    <TiptapBubbleMenu
      v-if="editor && config.quoteCharacterLimit"
      id="editor-bubble-menu"
      :editor="editor"
      :tippy-options="{ duration: 100, placement: 'bottom' }"
      :should-show="bubbleMenuShouldShow"
    >
      <div v-if="config.quoteCharacterLimit">
        <BButton
          type="is-primary"
          outlined
          size="is-small"
          icon-pack="fas"
          icon-left="quote-right"
          @click="emitQuote"
        />
      </div>
    </TiptapBubbleMenu>
    <TiptapEditorContent
      v-if="editor"
      :editor
      :class="[{ 'disable-text-selection': !config.canSelect }]"
      :style="{
        // height: (config?.fixedHeight ?? true) ? (config?.height ?? 125).toString() + 'px' : '',
        fontSize: config.fontSize + '%',
      }"
    />
    <!-- Rendu sur le serveur et temporairement sur le client avant le montage du lecteur -->
    <!-- NOTE <p> est défectueux et l'hydration ne passe pas avec cette balise, c'est un bug connu en cours de correction -->
    <!-- FIXME le style scoped css n'est pas appliqué sur les balises gérées par v-html, d'où shift visuel après montage sur le lecteur -->
    <div v-else v-html="text"></div>
  </div>
</template>

<script setup lang="ts">
import type { TipTapReaderConfig } from "~/types/other";

interface Props {
  text: string;
  config?: TipTapReaderConfig;
}
const {
  text,
  config = {
    canSelect: true,
    quoteCharacterLimit: 0,
    fontSize: 100,
  },
} = defineProps<Props>();

const emit = defineEmits(["quote"]);

const editor = useEditor({
  editable: false,
  content: text,
  extensions: [
    TiptapStarterKit,
    TiptapTextStyle,
    TiptapIndent,
    TiptapTextAlign.configure({
      types: ["heading", "paragraph"],
    }),
    TiptapFontSize,
    TiptapFontFamily,
    TiptapLimitedSelection.configure({
      isActive: Boolean(config.quoteCharacterLimit),
      maxSelection: config.quoteCharacterLimit,
    }),
  ],
});
onBeforeUnmount(() => unref(editor)?.destroy());

const bubbleMenuShouldShow = (): boolean => {
  if (!config.quoteCharacterLimit) return false;

  const { from, to } = editor.value!.view.state.selection;
  const text = editor.value!.state.doc.textBetween(from, to, "");
  return text.length > 0;
};

// TODO depuis le storage
function emitQuote(): void {
  if (!config.quoteCharacterLimit) {
    return;
  }
  const { view, state } = editor.value!;
  const { from, to } = view.state.selection;
  // On check la longueur max émise
  let newTo = to;
  const maxSelectionLength = config.quoteCharacterLimit;
  if (to - from > maxSelectionLength) newTo = from + maxSelectionLength;
  const quoteText = state.doc.textBetween(from, newTo, "");
  // Emet l'évènement quote
  emit("quote", quoteText);
  editor.value!.commands.setTextSelection(to);
  window.getSelection()?.empty();
}
</script>

<style lang="scss" scoped>
#editor-content-main-pane {
  #editor-bubble-menu {
    background: #f5f5f5;
    border: 2px solid var(--primary) !important;
    border-radius: 0.57rem !important;
    padding: 3px;
  }
  .disable-text-selection {
    user-select: none; /* Désactiver la sélection de texte */
    pointer-events: none; /* Désactiver les interactions de pointeur */
  }
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
  }
}
</style>
