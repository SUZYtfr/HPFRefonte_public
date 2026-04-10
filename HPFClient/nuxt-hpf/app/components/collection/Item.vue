<template>
  <div>
    Série par {{ collection.authors?.map((a) => a.username).join(",") }} contenant {{ collection.itemCount }} élément{{
      collection.itemCount! > 1 ? "s" : ""
    }}
  </div>
  <BButton size="is-small" icon-right="up-right-from-square" icon-pack="fas">Voir</BButton>
  <div>Caractéristiques: --, --, --, -- Fandoms: --, --, --, --</div>
</template>

<script setup lang="ts">
import { BButton } from "buefy";
import type { CollectionModel } from "~/models";

interface Props {
  collection: CollectionModel;
}

defineProps<Props>();
</script>
