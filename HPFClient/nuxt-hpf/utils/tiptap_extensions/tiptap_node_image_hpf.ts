import { Node, mergeAttributes } from '@tiptap/core'
import { VueNodeViewRenderer } from '@tiptap/vue-2'
import ImageEditor from "~/components/hpf_image/ImageEditor.vue";

export default Node.create({
  name: 'hpfImage',

  group: 'block',

  atom: true,

  draggable: true,

  addAttributes() {
    return {
      url: {
        default: "https://bulma.io/images/placeholders/32x32.png",
      },
      currentWidth:{
        default: 32,
      },
      currentHeight:{
        default: 32,
      },
      defaultWidth:{
        default: 32,
      },
      defaultHeight:{
        default: 32,
      },
      id_in_text:{
        default: 0,
      },
      editing:{
        default: true,
      },
      preserveRatio:{
        default: true,
      }
    }
  },

  parseHTML() {
    return [
      {
        tag: 'hpf-image[data-type="draggable-item"]',
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['hpf-image', mergeAttributes({ 'id_in_text': HTMLAttributes['id_in_text'], 'width': HTMLAttributes['currentWidth'], 'height': HTMLAttributes['currentHeight'] }) ];
    //return ['hpf-image', mergeAttributes(HTMLAttributes, { 'data-type': 'draggable-item' })]
  },

  addNodeView() {
    return VueNodeViewRenderer(ImageEditor)
  },
})