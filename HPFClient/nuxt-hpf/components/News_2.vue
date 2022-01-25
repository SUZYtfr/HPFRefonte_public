<template>
  <div
    v-bind:style="{ backgroundColor: activeColor }"
    style="
      padding: 10px 5px 5px 5px;"
  >
    <!-- Header -->
    <div class="columns is-vcentered is-mobile mb-1">
      <div class="column">
        <h3 class="h3 is-inline">
          <a href="viewstory.php?sid=37709" style="padding-left: 0px">{{
            news.title
          }}</a>
        </h3>
        <b-button
          type="is-primary"
          size="is-small"
          icon-pack="fas"
          icon-left="comment-alt"
          style="margin-right: 8px; float: right"
          ><span class="badge">{{ news.comments.length }}</span></b-button
        >
        <hr />
      </div>
    </div>
    <!-- Content -->
    <div
      class="columns mb-0"
    >
      <div
        id="content-container"
        class="column is-full py-0"
      >
        <span
          class="max-lines"
          v-bind:id="'news-' + news.news_id"
          v-html="news.content"
        ></span>
      </div>
    </div>
    <!-- Footer -->
    <div
      class="columns is-vcentered is-mobile mt-1"
      style="margin-bottom: 0px;"
    >
      <div class="column pt-2 pb-1">
        <span>Le </span>
        <span class="has-text-weight-semibold"> {{ news.post_date | parseTime }} </span>
        <span> par </span>
        <span class="has-text-weight-semibold" v-for="author in news.authors" v-bind:key="author.id">
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
      return dt.toLocaleDateString() + " à " + dt.getHours() + ":" + dt.getMinutes();
    },
  },
})
export default class News_2 extends Vue {
  @Prop() private news!: NewsData;
  @Prop() private activeColor!: string;
  //private visibility: boolean = true;

  mounted() {
    // let news_content = document.getElementById(
    //   "news-" + this.news.news_id.toString()
    // );
    // this.visibility = news_content != null && news_content.offsetHeight >= 168;
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
</style>
