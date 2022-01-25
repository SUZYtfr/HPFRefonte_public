<template>
  <div
    class="quill-editor"
    :content="editorContent"
    v-quill:myQuillEditor="editorOption"
    @change="onEditorChange($event)"
  ></div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
if (process.browser) {
  const VueQuillEditor = require("vue-quill-editor/dist/ssr");
  Vue.use(VueQuillEditor /* { default global options } */);
}
@Component({
  name: "Editor",
})
export default class extends Vue {
  //#region Props
  @Prop() private placeholder!: string;
  //#endregion

  //#region Data
  private editorContent: string = "";
  private editorOption: object = {
    theme: "snow",
    placeholder: this.placeholder,
    modules: {
      toolbar: [
        [
          { size: [] },
          {
            header: [1, 2, 3, 4, 5, 6],
          },
          { font: [] },
          "bold",
          "italic",
          "underline",
          "strike",
          { list: "ordered" },
          { list: "bullet" },
          { align: [] },
          { indent: "-1" },
          { indent: "+1" },
          { color: [] },
          { background: [] },
          "image",
        ],
      ],
    },
  };
  //#endregion

  //#region Methods
  private onEditorChange({ quill, html, text }) {
    this.editorContent = html;
    this.$emit("change", this.editorContent);
  }
  //#endregion
}
</script>

<style lang="scss">
.ql-toolbar,
.quill-editor {
  background-color: #f0f0f0;
}
.ql-toolbar {
  height: auto;
}
.quill-editor {
  height: 383px;
  max-height: 383px;
}
</style>