<template>
  <div id="main-container" class="container px-5">
    <News_2 v-if="news != null" class="mt-2" :news="news" :active-color="'#f0f0f0'" />
    <br>
    <div>
      <!-- <CommentList v-if="news != null" :news_id="news?.id" :comments="news?.comments" /> -->
    </div>
    <br>
  </div>
</template>

<script setup lang="ts">
// import { SerialiseClass } from "@/serialiser-decorator";
import { getNews } from "~/api/news";
import { NewsModel } from "~/models/news";
import News_2 from "~/components/News_2.vue";
import CommentList from "~/components/list/comments/CommentList.vue";

const route = useRoute();

const { data: news } = await getNews(parseInt(route.params.id as string));

// let newsLoading = false;
// async function fetch(): Promise<void> {
//   this.newsLoading = true;
//   try {
//     this.news = (await getNews(parseInt(this.$route.params.id)));
//   } catch (error) {
//     if (process.client) {
//       this.$buefy.snackbar.open({
//         duration: 5000,
//         message: "Une erreur s'est produite lors de la récupération de l'actualité",
//         type: "is-danger",
//         position: "is-bottom-right",
//         actionText: null,
//         pauseOnHover: true,
//         queue: true
//       });
//     } else {
//       console.log(error);
//     }
//   } finally {
//     this.newsLoading = false;
//   }
// }
</script>

<style lang="scss" scoped>

</style>
