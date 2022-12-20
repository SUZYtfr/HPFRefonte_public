<template>
  <div id="main-container" class="container px-5">
    <News_2 :news="news" :activeColor="'#f0f0f0'"></News_2>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { getNew, getNews } from "~/api/news";
import { NewsData, NewsResponse } from "@/types/news";
import News_2 from "~/components/News_2.vue";

@Component({
  name: "News",
  components: {
    News_2,
  },
})
export default class extends Vue {
  //#region  Data
  private news!: NewsData;
  private newsLoading = false;
  //#endregion

  //#region Hooks
  created() {
    this.news = null!;
  }

  mounted() {}

  async asyncData() {
    console.log("asyncData");
  }

  async fetch() {
    this.newsLoading = true;
    console.log("fetch");
    try {
      this.news = (await getNew(this.$route.params.id)).data as NewsData;
    } catch (error) {
      console.log(error);
    } finally {
      this.newsLoading = false;
    }
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
</style>