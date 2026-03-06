<template>
  <article class="media mt-0 mb-3">
    <figure class="media-left mx-2 mb-5">
      <p class="image is-48x48">
        <img src="https://bulma.io/assets/images/placeholders/96x96.png" />
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
        <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
          <div class="is-flex-grow-5">
            <div class="mr-3 white-space-nowrap">
              <template v-for="(author, index) in review.authors" :key="'author_' + author.userId.toString()">
                <template v-if="index > 0"> , </template>
                <!-- <NuxtLink
                  class="is-size-7 has-text-weight-normal"
                  :to="{ name: 'auteurs-id', params: { id: author.userId } }"
                > -->
                {{ author.username }}
                <!-- </NuxtLink> -->
              </template>
            </div>
          </div>
          <span class="has-text-weight-bold">{{ review.grading }}</span>
          <BRate v-if="review.grading" v-model="reviewGrading" icon-pack="fas" :disabled="true" :max="1" :rtl="true" />
        </div>

        <!-- <div class="is-flex is-flex-direction-row is-justify-content-space-between">
          <NuxtLink :to="{ name: 'auteurs-id', params: { id: review.authors?.user_id } }">
            <strong>{{ review.authors?.username }}</strong>
          </NuxtLink>
          <small>{{ review.post_date != null ? (review.post_date.toLocaleDateString() + " à " + review.post_date.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })) : "" }}</small>
        </div> -->
        <p>
          <RichtextReader :text="review.text" />
        </p>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { ReviewModel } from "~/models";
interface Props {
  review: ReviewModel;
}
const { review } = defineProps<Props>();
const reviewGrading = ref<number>((review.grading || 0) / 10);
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
</style>
