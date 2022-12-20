<template>
  <div
    v-bind:style="{ backgroundColor: activeColor }"
    style="
      padding: 10px 5px 5px 5px;
      display: flex;
      flex-flow: column;
      height: 250px;
    "
  >
    <!-- Header -->
    <div class="columns is-vcentered is-mobile mb-1" style="flex: 0 1 auto">
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
        <hr class="mr-4" />
      </div>
    </div>
    <!-- Content -->
    <div
      class="columns mb-0"
      style="flex: 1 1 auto; max-height: 176px; position: relative"
    >
      <div
        id="content-container"
        class="column is-full py-0"
        style="overflow-y: hidden"
      >
        <span
          class="max-lines"
          v-bind:id="'news-' + news.id"
          v-html="news.content"
        ></span>
      </div>
      <div v-if="visibility" v-bind:style="styleFadeDiv">
        <b-button
          type="is-primary"
          size="is-small"
          label="Lire la suite"
        ></b-button>
      </div>
    </div>
    <!-- Footer -->
    <div
      class="columns is-vcentered is-mobile"
      style="flex: 0 1 auto; max-height: auto; margin-bottom: 0px;"
    >
      <div class="column pt-2 pb-1">
        <span>Le {{ news.post_date | parseTime }} par </span>
        <span v-for="author in news.authors" v-bind:key="author.id">
          {{ author.nickname }}
        </span>
      </div>
    </div>
    <!-- <div
      class="columns is-vcentered"
      style="flex: 0 1 auto; max-height: auto"
    >
      <div class="column">
        <hr class="mx-4 my-0" />
      </div>
    </div> -->
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { NewsData } from "@/types/news";

@Component({
  name: "News",
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    },
  },
})
export default class News extends Vue {
  @Prop() private news!: NewsData;
  @Prop() private activeColor!: string;
  private visibility: boolean = true;
  private styleFadeDiv = {
    content: "",
    position: "absolute",
    zIndex: 1,
    backgroundImage:
      "linear-gradient(to bottom,rgba(255, 255, 255, 0)," +
      (this.activeColor == "#B3829A"
        ? "rgba(179, 130, 154, 1)"
        : "rgba(240, 240, 240, 1)") +
      " 90%)",
    height: "60px",
    width: "97%",
    left: 0,
    bottom: 0,
    textAlign: "center",
    marginLeft: "7px",
    paddingTop: "28px",
  };

  mounted() {
    let news_content = document.getElementById(
      "news-" + this.news.id!.toString()
    );
    this.visibility = news_content != null && news_content.offsetHeight >= 168;
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
}

.max-lines {
  display: block;
  text-overflow: ellipsis;
  word-wrap: break-word;
  overflow: hidden;
  max-height: 10.5em;
  line-height: 1.5em;
}

.blur-content {
  -webkit-filter: url(#svg-blur);
  filter: url(#svg-blur);
}
</style>
