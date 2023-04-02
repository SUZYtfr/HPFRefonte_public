import { Heading } from "@tiptap/extension-heading";

export const CustomHeading = Heading.extend({
  addAttributes() {
    return {
      color: {
        default: null,
        // Take the attribute values
        renderHTML: (attributes) => {
          // … and return an object with HTML attributes.
          return {
            style: `color: ${attributes.color}`
          };
        }
      }
    };
  }
});
