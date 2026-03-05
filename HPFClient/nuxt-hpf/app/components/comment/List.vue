<template>
  <div class="card">
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">Commentaires</p>
    </header>
    <div class="card-content">
      <div class="content">
        <div v-if="(comments?.length ?? 0) > 0">
          <CommentEntity
            v-for="(item, innerindex) of comments"
            :key="'comment_' + item.commentId.toString()"
            :index="innerindex"
            :comment="item"
          />
        </div>
        <p v-else class="has-text-centered">Aucun commentaire</p>
      </div>
      <div v-if="isAuthenticated">
        <RichtextEditor ref="comment-editor" :config="tiptapConfig" />
        <div class="buttons mt-1">
          <BButton
            :disabled="commentState.wordCount < 3"
            :expanded="false"
            label="Poster un commentaire"
            type="is-primary"
            @click="postComment"
          />
        </div>
      </div>
      <div v-else class="buttons mt-1 is-centered">
        <BButton
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser un commentaire"
          type="is-primary"
          @click="() => setLoginModalActive(true)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CommentModel } from "~/models";
import type { TipTapEditorConfig, ReviewState } from "~/types/other";
import type { TiptapEditor } from "#imports";

const { comments } = defineProps<{
  comments: CommentModel[] | null;
  postComment: () => Promise<void>;
}>();

const { isAuthenticated } = useCustomAuth();
const { setLoginModalActive } = useModalsStateStore();

const tiptapConfig: TipTapEditorConfig = {
  showFooter: false,
  placeholder: "Laissez un commentaire",
  fixedHeight: true,
  height: 150,
  oneLineToolbar: false,
  canUseImage: false,
};

const editorComponent = useTemplateRef("comment-editor");
const editor = computed<TiptapEditor | undefined>(() => editorComponent.value?.editor);

const commentState = useState<ReviewState>("commentState", () => {
  return {
    content: "",
    wordCount: 0,
    canGrade: false,
    grading: undefined,
  };
});
watch(
  () => editor.value?.getHTML(),
  () => {
    commentState.value.content = editor.value?.getHTML() || "";
    commentState.value.wordCount = editor.value?.extensionStorage.characterCount.words() || 0;
  },
);
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
</style>
