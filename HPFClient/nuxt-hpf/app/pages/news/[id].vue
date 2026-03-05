<template>
  <div id="main-container" class="container px-5">
    <NewsEntity v-if="news" class="mt-2 is-color-odd" :news="news" />
    <br />
    <div>
      <CommentList v-if="news" :comments="news.comments" :post-comment />
    </div>
    <br />
  </div>
</template>

<script setup lang="ts">
import type { NewsArticleType } from "#gql";
import { plainToInstance } from "class-transformer";
import { NewsModel } from "~/models";
import type { ReviewState } from "~/types/other";

definePageMeta({
  auth: false,
});

const route = useRoute();

// TODO - erreur si l'élément n'est pas récupéré
const { data: news } = await useAsyncGql(
  "getNewsDetails",
  {
    newsId: route.params.id as string,
  },
  {
    transform: (input: { newsArticle: NewsArticleType }) => {
      return plainToInstance(NewsModel, input.newsArticle);
    },
  },
);

if (!news.value) {
  navigateTo("/");
}

const commentState = useState<ReviewState>("commentState");

async function postComment(): Promise<void> {
  await GqlPostComment({
    newsArticleId: route.params.id as string,
    commentData: {
      text: commentState.value.content,
    },
  });
}

useHead({
  title: "HPF - " + news.value.title,
});
</script>

<style lang="scss" scoped></style>
