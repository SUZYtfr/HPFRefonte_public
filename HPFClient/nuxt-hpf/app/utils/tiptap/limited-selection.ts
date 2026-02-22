// Pour l'apparence de la sélection, cette extension est une copie de l'extension Selection
// https://tiptap.dev/docs/editor/extensions/functionality/selection
// https://github.com/ueberdosis/tiptap/blob/main/packages/extensions/src/selection/selection.ts
// L'extension est copiée plutôt qu'étendue pour deux raisons :
// L'extension originelle ne se permet pas de fonctionner lorsque l'éditeur est inactif (condition commentée ci-dessous)
// L'extension originelle décore le texte sélectionné par une balise avec la classe css passée,
// or ça ne semble pas fonctionner, possiblement à cause de notre construction de editor content
// à la place d'une classe css, on passe un style à apposer directement à la balise

import { Extension, isNodeSelection } from "@tiptap/core";
import { Plugin, PluginKey } from "@tiptap/pm/state";
import { Decoration, DecorationSet } from "prosemirror-view";

interface LimitedSelectionOptions {
  maxSelection: number;
  style: string;
  isActive: boolean;
  //   class: string
}

export const LimitedSelection = Extension.create<LimitedSelectionOptions>({
  name: "limitedSelection",
  addOptions() {
    return {
      maxSelection: 250,
      style: "background-color: #ef476f",
      isActive: false,
    };
  },
  addProseMirrorPlugins() {
    const { editor, options } = this;

    return [
      new Plugin({
        key: new PluginKey("limitedSelection"),
        props: {
          decorations(state) {
            if (
              !options.isActive ||
              state.selection.empty ||
              editor.isFocused ||
              // !editor.isEditable ||  // On veut activer cette fonctionnalité en mode lecture
              isNodeSelection(state.selection) ||
              editor.view.dragging
            ) {
              return null;
            }

            return DecorationSet.create(state.doc, [
              Decoration.inline(state.selection.from, state.selection.to, {
                style: options.style,
                // class: "animate__animated animate__fast animate__flash",  // FIXME - flash au début de l'action de sélection
              }),
            ]);
          },
        },
      }),
    ];
  },
  onSelectionUpdate() {
    if (!this.options.isActive) return;
    const { from, to } = this.editor.state.selection;
    const selectedText = this.editor.state.doc.textBetween(from, to);
    if (selectedText.length > this.options.maxSelection) {
      this.editor
        .chain()
        .blur() // évite le clignotement de la sélection
        .focus(from, { scrollIntoView: true })
        .setTextSelection({ from: from, to: from + this.options.maxSelection })
        .run();
    }
  },
});
