<template>
  <div style="height: 500px; width: 70%;">
    <client-only>
      <TipTapEditor class="m-5" />
    </client-only>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import TipTapEditor from "~/components/TipTapEditor.vue";

@Component({
  components: {
    TipTapEditor,
  },
})
export default class extends Vue {}
</script>

<style lang="scss">
//@import "~/assets/scss/custom.scss";
</style>