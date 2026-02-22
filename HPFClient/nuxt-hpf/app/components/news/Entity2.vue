<template>
  <div :class="['news', 'px-3']">
    <!-- Header -->
    <div class="columns is-vcentered is-mobile mb-1">
      <div class="column">
        <h3 class="h3 is-inline">
          <NuxtLink class="pl-0" :to="{ name: 'news-id', params: { id: news.newsId } }">
            {{ news.title }}
          </NuxtLink>
        </h3>
        <BButton
          class="news_comment_button"
          type="is-primary"
          size="is-small"
          icon-pack="fas"
          icon-left="comment-alt"
          tag="nuxt-link"
          :to="{ name: 'actualites-id', params: { id: news.newsId } }"
        >
          <span class="badge">{{ news.commentCount }}</span>
        </BButton>
        <hr />
      </div>
    </div>
    <!-- Content -->
    <div class="columns mb-0">
      <div id="content-container" class="column is-full py-0">
        <span :id="'news-' + news.newsId" class="max-lines" v-html="news.content"></span>
      </div>
    </div>
    <!-- Footer -->
    <div class="columns is-vcentered is-mobile mt-1 mb-0">
      <div class="column pt-2 pb-1">
        <span>Le </span>
        <span class="has-text-weight-semibold">
          {{
            news.postDate != null
              ? news.postDate.toLocaleDateString("fr-FR") +
                " à " +
                news.postDate.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })
              : ""
          }}
        </span>
        <span> par </span>
        <span v-for="(author, index) in news.authors" :key="author.userId" class="has-text-weight-semibold">
          {{ author.username + (index != (news.authors?.length ?? 0) - 1 ? ", " : "") }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewsModel } from "@/models";

defineProps<{
  news: NewsModel;
}>();
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
hr {
  background-color: var(--primary);
  margin-top: 5px;
  margin-bottom: 5px;
  margin-right: 80px;
}
.news_comment_button {
  margin-right: 8px;
  float: right;
}
.news {
  //background-color: #ffffff;
  padding: 10px 5px 5px 5px;
  border-radius: 10px !important;
}

.news-hover {
  /*background-color: #f6f6f6 !important;*/
  //border: 1px solid #f6f6f6 !important;
  // border-radius: 10px 10px 0px 0px !important;
}

.fanfiction {
  /*background-color: #ffffff;
  border-bottom: 2px solid var(--primary);*/
}
</style>
