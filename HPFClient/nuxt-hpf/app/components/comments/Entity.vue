<template>
  <article class="media mt-0 mb-3">
    <figure class="media-left mx-2 mb-5">
      <p class="image is-48x48">
        <img src="https://bulma.io/assets/images/placeholders/96x96.png"/>
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <div class="is-flex is-flex-direction-row is-justify-content-space-between">
          <!-- <NuxtLink :to="{ name: 'auteurs-id', params: { id: comment.author?.userId } }"> -->
            <strong>{{ comment.author?.username }}</strong>
          <!-- </NuxtLink> -->
          <small>{{ comment.postDate != null ? (comment.postDate.toLocaleDateString("fr-FR") + " à " + comment.postDate.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })) : "" }}</small>
        </div>
        <p>
          <span
            v-html="comment.content"
          ></span>
        </p>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { CommentModel } from "~/models/";

const { comment } = defineProps<{
    comment: CommentModel;
}>();
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
</style>