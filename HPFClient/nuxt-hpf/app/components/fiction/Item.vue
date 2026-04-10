<template>
  <div>
    Fiction de {{ fiction.chapterCount }} chapitre{{ fiction.chapterCount! > 1 ? "s" : "" }} par
    {{ fiction.authors?.map((a) => a.username).join(",") }}
    <NuxtLink
      :to="{
        name: 'fictions-fictionId-fictionTitle-sommaire',
        params: {
          fictionId: fiction.fanfictionId,
          fictionTitle: fiction.titleAsSlug,
        },
      }"
      no-prefetch
      target="_blank"
    >
      <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
    </NuxtLink>
  </div>
  <div>Caractéristiques: --, --, --, -- Fandoms: --, --, --, --</div>
</template>

<script setup lang="ts">
import { BButton } from "buefy";
import type { FanfictionModel } from "~/models";

interface Props {
  fiction: FanfictionModel;
}

defineProps<Props>();
</script>
