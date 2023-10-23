<template>
  <footer class="footer">
    <div class="container is-fluid">
      <div id="footer-background-image-wrapper">
        <img
          src='@/assets/img/logo_forum_horizontal_300.png'
          alt="Logo forum HPF"
        >
      </div>
      <div id="footer-content" class="outlined">
        <div
          class="
            is-flex
            is-flex-direction-row
            is-align-items-center
            is-flex-wrap-wrap
          "
        >
          <a
            class="mr-auto"
            href="#"
          >Harry Potter Fanfiction</a>
          <div
            class="is-flex
            is-flex-direction-row is-flex-wrap-wrap"
          >
            <a href="#">Administration</a>
            <a href="#">Modération</a>
            <a href="#">Mentions légales</a>
          </div>
        </div>
        <div class="is-flex is-justify-content-center has-text-centered pb-1">
          <p>
            Tous droits réservés @Association Héros de Papiers Froissés | Site
            réalisé par Pierre, SUZYftr, Tsilla Aumigny
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "Footer"
})
export default class Footer extends Vue {}
</script>

<style scoped>
a {
  color: #ffffff !important;
  padding: 10px;
}
a:hover {
  color: #ffffff;
  background-color: #f07800;
}

#footer-background-image-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

#footer-background-image-wrapper img {
  max-height: 90%;
  width: auto;
  opacity: 0.6;
}

#footer-content a,p {
  z-index: 1 !important;
}

.outlined {
  color: white;
  text-shadow:
    -1px -1px 0 #000,
     0   -1px 0 #000,
     1px -1px 0 #000,
     1px  0   0 #000,
     1px  1px 0 #000,
     0    1px 0 #000,
    -1px  1px 0 #000,
    -1px  0   0 #000;
}
</style>
