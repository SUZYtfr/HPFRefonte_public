<template>
  <div id="main-container" class="container px-5">
    <News_2 :news="news" :active-color="'#f0f0f0'" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { getNews } from "~/api/news";
import { NewsModel } from "~/models/news";
import News_2 from "~/components/News_2.vue";

@Component({
  name: "News",
  components: {
    News_2
  }
})
export default class extends Vue {
  // #region  Data
  public news!: NewsModel;
  private newsLoading = false;
  // #endregion

  // #region Hooks
  created(): void {
    this.news = null!;
  }

  mounted(): void {}

  async asyncData(): Promise<void> {
    await console.log("asyncData");
  }

  async fetch(): Promise<void> {
    this.newsLoading = true;
    console.log("fetch");
    try {
      this.news = (await getNews(parseInt(this.$route.params.id))).data.items.user;
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
