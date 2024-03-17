// Importez les éléments nécessaires de Tiptap
import { Mark, mergeAttributes } from "@tiptap/core";

declare module "@tiptap/core" {
  interface Commands<ReturnType> {
    limitedSelection: {
      /**
       * Toggle a limited selection mark
       */
      toggleLimitedSelection: () => ReturnType,
    }
  }
}

export const LimitedSelection = Mark.create({
  name: "limitedSelection",

  addOptions() {
    return {
      HTMLAttributes: {}
    };
  },

  parseHTML() {
    return [
      {
        tag: "limitedSelection"
      }
    ];
  },
  renderHTML({ HTMLAttributes }) {
    return ["limitedSelection", mergeAttributes(this.options.HTMLAttributes, HTMLAttributes), 0];
  },

  addCommands() {
    return {
      toggleLimitedSelection: () => ({ commands }) => {
        return commands.toggleMark(this.name);
      }
    };
  }
});
