// TODO - ces extensions ne sont jamais utilisées hors de l'éditeur Tiptap
// Les importer directement là où elles seront utiles ?
// Ou les ajouter aux auto-imports ?

export { BubbleMenu as TiptapBubbleMenu } from "@tiptap/extension-bubble-menu";
export { Underline as TiptapUnderline } from "@tiptap/extension-underline";
export { TextAlign as TiptapTextAlign } from "@tiptap/extension-text-align";
// export { BlockQuote as TiptapBlockQuote } from "@tiptap/extension-blockquote";
export { CharacterCount as TiptapCharacterCount, Placeholder as TiptapPlaceholder } from "@tiptap/extensions";
export {
  TextStyle as TiptapTextStyle,
  FontSize as TiptapFontSize,
  FontFamily as TiptapFontFamily,
} from "@tiptap/extension-text-style";
export {
  Table as TiptapTable,
  TableRow as TiptapTableRow,
  TableCell as TiptapTableCell,
  TableHeader as TiptapTableHeader,
} from "@tiptap/extension-table";

export { LimitedSelection as TiptapLimitedSelection } from "./limited-selection";
export { Quote as TiptapQuote } from "./quote";
export { Indent as TiptapIndent } from "./indent";
