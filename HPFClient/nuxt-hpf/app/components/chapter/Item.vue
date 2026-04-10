<template>
  <div>
    Chapitre {{ chapter.order! + 1 }} de la fiction {{ chapter.fiction!.title }} par
    {{ chapter.authors?.map((a) => a.username).join(",") }}
    <NuxtLink
      :to="{
        name: 'fictions-fictionId-fictionTitle-chapitres-chapterId-chapterTitle',
        params: {
          fictionId: chapter.fiction!.fanfictionId,
          fictionTitle: chapter.fiction!.titleAsSlug,
          chapterId: chapter.chapterId,
          chapterTitle: chapter.titleAsSlug,
        },
      }"
      no-prefetch
      target="_blank"
    >
      <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { BButton } from "buefy";
import type { ChapterModel } from "~/models";

interface Props {
  chapter: ChapterModel;
}

defineProps<Props>();
</script>
