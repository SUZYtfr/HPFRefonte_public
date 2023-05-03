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
      <div v-if="ConnectedVisibility">
        <client-only>
          <TipTapEditor ref="commentEditor" :show-footer="false" :placeholder="'Ecrire un commentaire'" @change="(value) => (editorContent = value)" />
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

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import Comment from "~/components/entities/comment.vue";
import { CommentModel } from "@/models/news";
import { postComment } from "~/api/news";
import { UserModule, ModalsStatesModule } from "@/utils/store-accessor";
import TipTapEditor from "~/components/TipTapEditor.vue";
import { TipTapEditorContent } from "@/types/tiptap";
import ModalsStates from "~/store/modules/ModalsStates";

@Component({ name: "CommentList", components: { Comment, TipTapEditor } })
export default class CommentList extends Vue {
  // #region Props
  @Prop({ default: [] }) public comments!: CommentModel[];
  @Prop({ default: null }) public news_id!: number;
  // #endregion

  // #region Datas
  public editorContent: TipTapEditorContent | null = null;
  // #endregion

  // #region Computed
  get ConnectedVisibility(): boolean {
    return UserModule.token.length > 0;
  }

  get ModalsStatesModule(): ModalsStates {
    return ModalsStatesModule;
  }
  // #endregion

  // #region Methods
  public async PostComment(): Promise<void> {
    if (this.news_id === null) return;
    if ((this.editorContent?.wordcount ?? 0) < 3) return;
    if (this.editorContent?.content == null) return;
    try {
      let comment: CommentModel = new CommentModel();
      comment.content = this.editorContent?.content;
      comment = (await postComment(this.news_id, comment)).items;
      if (comment != null) this.comments?.push(comment);
    } catch (error) {
      console.log(error);
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

</style>
