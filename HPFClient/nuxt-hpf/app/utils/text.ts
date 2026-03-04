import { convert } from "html-to-text";

export function convertToPlainText(html: string): string {
  return convert(html, {
    selectors: [{ selector: "a", options: { ignoreHref: true } }],
  });
}
