import { Extension } from "@tiptap/core";

declare module "@tiptap/core" {
  interface Commands<ReturnType> {
    customCommands: {
      insertQuote: (quote: string) => ReturnType;
    };
  }
}

export const Quote = Extension.create({
  name: "quote",

  addCommands() {
    return {
      ...this.parent?.(),
      insertQuote:
        (quote: string) =>
        ({ chain }) => {
          // TODO - insérer à la dernière position connue du curseur
          return chain()
            .focus("end", { scrollIntoView: true })
            .enter() // FIXME - seulement si un contenu existe préalablement
            .insertContent(quote)
            .setBlockquote()
            .enter()
            .unsetBlockquote()
            .run();
        },
    };
  },
});
