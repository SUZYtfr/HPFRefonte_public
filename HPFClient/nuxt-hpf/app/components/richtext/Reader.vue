<template>
  <TiptapEditorContent v-if="editor" :editor />
  <p v-else v-html="text"></p>
</template>

<script setup lang="ts">
const { text } = defineProps<{ text: string; plaintext?: boolean }>();
const editor = useEditor({
  editable: false,
  content: text,
  extensions: [TiptapStarterKit],
});

onBeforeUnmount(() => unref(editor)?.destroy());
</script>
