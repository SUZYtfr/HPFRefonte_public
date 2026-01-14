<template>
  <div id="container">
    <!-- Header -->
    <Navbar />
    <div id="wrapper">
      <!-- Main Content -->
      <NuxtPage />
    </div>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup lang="ts">
//#region Imports
//#endregion

//#region Hooks
onMounted(() => {
  // Fix buefy il faut ajouter la class has-navbar-fixed-top. En csr elle n'est pas ajoutée
  if (document.body.classList.contains("has-navbar-fixed-top") == false) {
    document.body.classList.add("has-navbar-fixed-top");
  }
});

onBeforeUnmount(() => {
  document.body.classList.remove("has-navbar-fixed-top");
});
//#endregion
</script>

<style lang="scss" scoped>
//@use "~/assets/scss/custom_bulma_core.scss";

#container {
  background-color: var(--primary-light);
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
#wrapper {
  flex-grow: 5;
  display: flex;
  flex-direction: column;
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
  //outline: 1px solid #0f0 !important;
}
</style>
