<template>
  <div class="news" v-bind:style="{ backgroundColor: activeColor }">
    <!-- Header -->
    <div class="columns is-vcentered is-mobile mb-1">
      <div class="column">
        <h3 class="h3 is-inline">
          <a class="pl-0" href="viewstory.php?sid=37709">{{ news.title }}</a>
        </h3>
        <b-button
          class="news_comment_button"
          type="is-primary"
          size="is-small"
          icon-pack="fas"
          icon-left="comment-alt"
          ><span class="badge">{{ news.comments.length }}</span></b-button
        >
        <hr />
      </div>
    </div>
    <!-- Content -->
    <div class="columns mb-0">
      <div id="content-container" class="column is-full py-0">
        <span
          class="max-lines"
          v-bind:id="'news-' + news.news_id"
          v-html="news.content"
        ></span>
      </div>
    </div>
    <!-- Footer -->
    <div class="columns is-vcentered is-mobile mt-1 mb-0">
      <div class="column pt-2 pb-1">
        <span>Le </span>
        <span class="has-text-weight-semibold">
          {{ news.post_date | parseTime }}
        </span>
        <span> par </span>
        <span
          class="has-text-weight-semibold"
          v-for="author in news.authors"
          v-bind:key="author.id"
        >
          {{ author.nickname }}
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { NewsData } from "@/api/news";

@Component({
  name: "News_2",
  filters: {
    parseTime: (timestamp: string) => {
      const dt = new Date(timestamp);
      return (
        dt.toLocaleDateString() + " à " + dt.getHours() + ":" + dt.getMinutes()
      );
    },
  },
})
export default class News_2 extends Vue {
  @Prop() private news!: NewsData;
  @Prop() private activeColor!: string;
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
  padding: 10px 5px 5px 5px;
}
</style>
