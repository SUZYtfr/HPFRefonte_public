<template>
  <article class="media mt-0 mb-3">
    <figure class="media-left mx-2 mb-5">
      <p class="image is-48x48">
        <img :src="comment.author?.avatar ?? 'https://bulma.io/images/placeholders/96x96.png'">
        <!-- <img src="https://bulma.io/images/placeholders/96x96.png"> -->
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <div class="is-flex is-flex-direction-row is-justify-content-space-between">
          <NuxtLink :to="{ name: 'auteurs-id', params: { id: comment.author?.user_id } }">
            <strong>{{ comment.author?.username }}</strong>
          </NuxtLink>
          <small>{{ comment.post_date != null ? (comment.post_date.toLocaleDateString() + " à " + comment.post_date.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })) : "" }}</small>
        </div>
        <p>
          <span
            v-html="comment.content"
          />
        </p>
      </div>
    </div>
  </article>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { CommentModel } from "~/models/news";

@Component({ name: "Comment" })
export default class Comment extends Vue {
  // #region Props
  @Prop() public comment!: CommentModel;
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>
