<template>
  <div id="main-container" class="container px-5">
    <News_2 v-if="news !== null" :news="news" :active-color="'#f0f0f0'" />
    <br>
    <div class="mx-2">
      <CommentList :news_id="news?.id" :comments="news?.comments" />
    </div>
    <br>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { SerialiseClass } from "@/serialiser-decorator";
import { getNews } from "~/api/news";
import { NewsModel } from "~/models/news";
import News_2 from "~/components/News_2.vue";
import CommentList from "~/components/list/comments/CommentList.vue";

@Component({
  name: "News",
  components: {
    News_2,
    CommentList
  },
  fetchOnServer: true,
  fetchKey: "news-page"
})
export default class extends Vue {
  // #region  Data
  @SerialiseClass(NewsModel)
  public news: NewsModel | null = null;

  private newsLoading = false;
  // #endregion

  // #region Hooks
  private async fetch(): Promise<void> {
    this.newsLoading = true;
    try {
      this.news = (await getNews(parseInt(this.$route.params.id))).items;
    } catch (error) {
      console.log(error);
    } finally {
      this.newsLoading = false;
    }
  }
  // #endregion
}
</script>

<style lang="scss" scoped>

</style>
