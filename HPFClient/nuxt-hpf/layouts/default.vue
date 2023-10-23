<template>
  <div id="container">
    <!-- Debug sidebar -->
    <SidebarDebug />
    <!-- Header -->
    <Navbar />
    <div id="wrapper">
      <!-- Main Content -->
      <slot />
    </div>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import SidebarDebug from "@/components/SidebarDebug.vue";

@Component({
  components: {
    Navbar,
    Footer,
    SidebarDebug
  }
})
export default class Layout extends Vue {}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom_bulma_core.scss";

#container {
  background-color: $primary-light;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
#wrapper {
  flex-grow: 5;
}

body,
html {
  //overflow-x: hidden;
}

html {
  //height: 100%;
}
body {
  //min-height: 100%;
}

* {
  // outline: 1px solid #0f0 !important;
}
</style>
