<template>
  <div id="container">
    <!-- Debug sidebar -->
    <!-- <SidebarDebug v-if="false" /> -->
    <!-- Header -->
    <Navbar />
    <!-- Bannière -->
    <div id="banner" class="hero">
      <div class="hero-body">
        <div class="container">
          <h1>Harry Potter Fanfiction</h1>
        </div>
      </div>
    </div>
    <div id="wrapper">
      <!-- Main Content -->
      <slot />
    </div>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
// import SidebarDebug from "@/components/SidebarDebug.vue";
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom_bulma_core.scss";

#container {
  background-color: var(--primary-light);
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
#wrapper {
  flex-grow: 5;
  // display: flex;
  // flex-direction: column
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

.hero-body {
  background-image: var(--hpf-banner);
}
#banner h1 {
  font-size: 50px;
  background-color: rgba(255, 255, 255, 0.6);
  font-family: "Amiri", serif;
  text-transform: uppercase;
  text-align: center;
  padding: 0px 20px;
}

</style>
