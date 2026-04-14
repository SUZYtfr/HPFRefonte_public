<template>
  <NuxtLayout
    :class="[
      'grayscale-overlay',
      { 'grayscale-overlay-mounted': isMounted == true },
      { 'fix-container-height': isMounted == true },
    ]"
  >
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
const isMounted = ref(false);

onMounted(() => {
  requestAnimationFrame(() => {
    isMounted.value = true;
  });
});
</script>

<style lang="scss">
// Overlay gris avant mounted pour une transition plus douce entre le thème codé (violet) => thème de l'utilisateur / thème par défaut
.grayscale-overlay::before {
  content: "";
  position: fixed;
  inset: 0;
  background: #aaa;
  mix-blend-mode: color;
  pointer-events: none;
  z-index: 9998;
  opacity: 1;
  transition: opacity 0.6s;
}
.grayscale-overlay.grayscale-overlay-mounted::before {
  opacity: 0;
}
</style>
