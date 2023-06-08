<template>
  <div
    :class="['news', 'px-3']"
    :style="{ backgroundColor: activeColor }"
  >
    <!-- Header -->
    <div class="columns is-vcentered is-mobile mb-1">
      <div class="column">
        <h3 class="h3 is-inline">
          <NuxtLink
            class="pl-0"
            :to="{ name: 'actualites-id', params: { id: news.news_id } }"
          >
            {{ news.title }}
          </NuxtLink>
        </h3>
        <b-button
          class="news_comment_button"
          type="is-primary"
          size="is-small"
          icon-pack="fas"
          icon-left="comment-alt"
          tag="nuxt-link"
          :to="{ name: 'actualites-id', params: { id: news.news_id } }"
        >
          <span class="badge">{{ news.comment_count }}</span>
        </b-button>
        <hr>
      </div>
    </div>
    <!-- Content -->
    <div class="columns mb-0">
      <div id="content-container" class="column is-full py-0">
        <span
          :id="'news-' + news.news_id"
          class="max-lines"
          v-html="news.content"
        />
      </div>
    </div>
    <!-- Footer -->
    <div class="columns is-vcentered is-mobile mt-1 mb-0">
      <div class="column pt-2 pb-1">
        <span>Le </span>
        <span class="has-text-weight-semibold">
          {{ news.post_date != null ? (news.post_date.toLocaleDateString() + " à " + news.post_date.getHours() + ":" + news.post_date.getMinutes()) : "" }}
        </span>
        <span> par </span>
        <span v-for="(author, index) in news.authors" :key="author.id" class="has-text-weight-semibold">
          {{ author.username + (index != ((news.authors?.length ?? 0) - 1) ? ", " : "") }}
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { NewsModel } from "~/models/news";

@Component({
  name: "News_2"
})
export default class News_2 extends Vue {
  // #region Props
  @Prop() public news!: NewsModel;
  @Prop() public activeColor!: string;
  // #endregion

  public mounted(): void {
    // console.log("News type: " + (this.news instanceof NewsModel));
    // console.log("Date type: " + ((new Date()) instanceof Date));
    // console.log("Creation date type: " + (this.news?.creation_date instanceof Date));
    // console.log("Last update date type: " + (this.news?.post_date instanceof Date));
    // console.log(this.news);
    // console.log(this.news?.post_date?.toLocaleDateString());
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
hr {
  background-color: $primary;
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
  border-bottom: 2px solid $primary;*/
}
</style>
