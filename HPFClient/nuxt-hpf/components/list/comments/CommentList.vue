<template>
  <div class="card">
    <header class="card-header sub-title">
      <p class="card-header-title is-centered">
        Commentaires
      </p>
    </header>
    <div class="card-content">
      <div class="content">
        <div v-if="(comments?.length ?? 0) > 0 ">
          <Comment v-for="(item, innerindex) of comments" :key="'comment_' + item.comment_id.toString()" :index="innerindex" :comment="item" />
        </div>
        <p v-else class="has-text-centered">
          Aucun commentaire
        </p>
      </div>
      <div v-if="$auth.loggedIn">
        <client-only>
          <TipTapEditor ref="commentEditor" :config="tiptapConfig" @change="(value) => (editorContent = value)" />
        </client-only>
        <div class="buttons mt-1">
          <b-button
            :disabled="(editorContent?.wordcount ?? 0) < 3"
            :expanded="false"
            label="Poster un commentaire"
            type="is-primary"
            @click="PostComment"
          />
        </div>
      </div>
      <div v-else class="buttons mt-1 is-centered">
        <b-button
          :disabled="false"
          :expanded="false"
          label="Se connecter pour laisser un commentaire"
          type="is-primary"
          @click="ModalsStatesModule.setLoginModalActive(true)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getModule } from "vuex-module-decorators";
import Comment from "~/components/entities/comment.vue";
import { CommentModel } from "@/models/news";
import { postComment } from "~/api/news";
import TipTapEditor from "~/components/TipTapEditor.vue";
import { TipTapEditorContent, TipTapEditorConfig } from "@/types/tiptap";
import ModalsStates from "~/store/modules/ModalsStates";
import { useStore } from "vuex";

interface commentListProps {
  comments?: CommentModel[]
  news_id?: number
}

const { comments, news_id } = withDefaults(defineProps<commentListProps>(), {
  comments: [],
  news_id: null
})
let { value: localComments } = ref(comments);

let editorContent: TipTapEditorContent | null = null;

const tiptapConfig: TipTapEditorConfig = {
  showFooter: false,
  placeholder: "Ecrire un commentaire",
  readOnly: false,
  fixedHeight: true
};

const ModalsStatesModule = (): ModalsStates => {
  const store = useStore()
  return getModule(ModalsStates, store)
}

// TODO tester ça quand auth et store sont réparés
const PostComment = (): void => {
  if (news_id === null) return;
  if ((editorContent?.wordcount ?? 0) < 3) return;
  if (editorContent?.content == null) return;
  try {
    let comment: CommentModel = new CommentModel();
    comment.content = editorContent?.content;
    comment.content_images = editorContent?.content_images;
    comment = (postComment(news_id, comment)).items;
    if (comment != null) localComments?.push(comment);
  } catch (error) {
    console.log(error);
  }
}

</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

</style>
