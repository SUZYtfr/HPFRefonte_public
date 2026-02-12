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
          <CommentsEntity v-for="(item, innerindex) of comments" :key="'comment_' + item.commentId.toString()" :index="innerindex" :comment="item" />
        </div>
        <p v-else class="has-text-centered">
          Aucun commentaire
        </p>
      </div>
      <!-- <div v-if="$auth.loggedIn">
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
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CommentModel } from '~/models';

const { comments, newsId } = defineProps<{
    comments: CommentModel[] | null;
    newsId: number,
}>()

/* const editorContent = ref<TipTapEditorContent | null>(null);

const tiptapConfig: TipTapEditorConfig = {
showFooter: false,
placeholder: "Ecrire un commentaire",
readOnly: false,
fixedHeight: true,
defaultValue: "",
canQuote: false,
quoteLimit: 0,
fontSize: 100,
height: 150,
oneLineToolbar: false,
canUseImage: false
};
*/

const ModalStatesModule = useModalsStateStore()

  // #region Methods
/*   public async PostComment(): Promise<void> {
if (this.news_id === null) return;
if ((this.editorContent?.wordcount ?? 0) < 3) return;
if (this.editorContent?.content == null) return;
try {
    let comment: CommentModel = new CommentModel();
    comment.content = this.editorContent?.content;
    comment.contentImages = this.editorContent?.content_images;
    comment = (await postComment((this.news_id as number), comment)).items;
    if (comment != null) this.comments?.push(comment);
} catch (error) {
    console.log(error);
}
} */
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

</style>