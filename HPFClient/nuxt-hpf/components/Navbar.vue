<template>
  <div>
    <!-- Navbar -->
    <b-navbar active :fixed-top="true">
      <template #brand>
        <b-navbar-item>
          <img
            :src="require('@/assets/img/logo_hpfanfic_court_300.png')"
            width="56"
            height="36"
            alt="Logo forum HPF"
          />
        </b-navbar-item>
        <div class="is-hidden-desktop" style="margin-left: auto">
          <b-navbar-item tag="div" v-if="ConnectedVisibility">
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <button type="button" class="button is-light">
                  <span class="icon is-small" style="margin-right: -8px">
                    <svg
                      aria-hidden="true"
                      focusable="false"
                      data-prefix="fas"
                      data-icon="bell"
                      role="img"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 448 512"
                      class="svg-inline--fa fa-bell fa-w-14"
                    >
                      <path
                        fill="currentColor"
                        d="M224 512c35.32 0 63.97-28.65 63.97-64H160.03c0 35.35 28.65 64 63.97 64zm215.39-149.71c-19.32-20.76-55.47-51.99-55.47-154.29 0-77.7-54.48-139.9-127.94-155.16V32c0-17.67-14.32-32-31.98-32s-31.98 14.33-31.98 32v20.84C118.56 68.1 64.08 130.3 64.08 208c0 102.3-36.15 133.53-55.47 154.29-6 6.45-8.66 14.16-8.61 21.71.11 16.4 12.98 32 32.1 32h383.8c19.12 0 32-15.6 32.1-32 .05-7.55-2.61-15.27-8.61-21.71z"
                        class=""
                      ></path>
                    </svg>
                  </span>
                  <span><span class="badge">8</span></span>
                </button>
              </template>
            </b-dropdown>
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <!-- <b-button
                  type="is-light"
                  :icon-right="active ? 'angle-up' : 'angle-down'"
                >
                  <img
                    src="https://nsa39.casimages.com/img/2018/02/16/mini_180216012732482019.jpg"
                    width="22"
                    height="22"
                    alt="Logo forum HPF"
                    style="
                      margin-left: -8px;
                      vertical-align: middle;
                      margin-bottom: 2px;
                    "
                  />
                  <span class="username-visibility">SUZYftr</span>
                </b-button> -->
                <button
                  type="button"
                  class="button is-light"
                  style="padding-left: 8px"
                >
                  <b-image
                    src="https://nsa39.casimages.com/img/2018/02/16/mini_180216012732482019.jpg"
                    alt="Logo forum HPF"
                    style="width: 22px; height: 22px: margin-left: -8px;"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span class="username-visibility" style="margin-left: 5px"
                    >SUZYftr</span
                  >
                  <b-icon :icon="active ? 'angle-up' : 'angle-down'"> </b-icon>
                </button>
              </template>
              <b-dropdown-item aria-role="listitem">Mon compte</b-dropdown-item>
              <b-dropdown-item aria-role="listitem"
                >Se déconnecter</b-dropdown-item
              >
            </b-dropdown>
          </b-navbar-item>
          <b-navbar-item tag="div" v-else>
            <div class="buttons">
              <a class="button is-light" @click="loginModalActive = true">
                Se connecter
              </a>
              <a class="button" @click="registerModalActive = true">
                S'inscrire
              </a>
            </div>
          </b-navbar-item>
        </div>
      </template>
      <template #start>
        <b-navbar-item active tag="router-link" target="_blank" to="/">
          Accueil
        </b-navbar-item>
        <b-navbar-dropdown :collapsible="true" label="Association HPF">
          <b-navbar-item href="#"> Link 1 </b-navbar-item>
          <b-navbar-item href="#"> Link 2 </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Lecture">
          <b-navbar-item href="#"> Link 1 </b-navbar-item>
          <b-navbar-item href="#"> Link 2 </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Ecriture">
          <b-navbar-item href="#"> Link 1 </b-navbar-item>
          <b-navbar-item href="#"> Link 2 </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Top fanfictions">
          <b-navbar-item href="#"> Link 1 </b-navbar-item>
          <b-navbar-item href="#"> Link 2 </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Nos sites">
          <b-navbar-item href="#"> L'appli HPF </b-navbar-item>
          <b-navbar-item href="#"> Le Héron </b-navbar-item>
          <b-navbar-item href="#"> Les éditions HPF </b-navbar-item>
          <b-navbar-item href="#"> L'association </b-navbar-item>
          <b-navbar-item href="#"> Le blog HPF </b-navbar-item>
          <b-navbar-item href="#"> Le forum </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Boutique">
          <b-navbar-item href="#"> Link 1 </b-navbar-item>
          <b-navbar-item href="#"> Link 2 </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-item href="#"> Partenaires </b-navbar-item>
        <b-navbar-item href="#" @click="contactModalActive = true"> Contact </b-navbar-item>
      </template>

      <template #end>
        <div class="is-hidden-touch">
          <b-navbar-item tag="div" v-if="ConnectedVisibility">
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <button type="button" class="button is-light">
                  <span class="icon is-small" style="margin-right: -8px">
                    <svg
                      aria-hidden="true"
                      focusable="false"
                      data-prefix="fas"
                      data-icon="bell"
                      role="img"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 448 512"
                      class="svg-inline--fa fa-bell fa-w-14"
                    >
                      <path
                        fill="currentColor"
                        d="M224 512c35.32 0 63.97-28.65 63.97-64H160.03c0 35.35 28.65 64 63.97 64zm215.39-149.71c-19.32-20.76-55.47-51.99-55.47-154.29 0-77.7-54.48-139.9-127.94-155.16V32c0-17.67-14.32-32-31.98-32s-31.98 14.33-31.98 32v20.84C118.56 68.1 64.08 130.3 64.08 208c0 102.3-36.15 133.53-55.47 154.29-6 6.45-8.66 14.16-8.61 21.71.11 16.4 12.98 32 32.1 32h383.8c19.12 0 32-15.6 32.1-32 .05-7.55-2.61-15.27-8.61-21.71z"
                        class=""
                      ></path>
                    </svg>
                  </span>
                  <span><span class="badge">8</span></span>
                </button>
              </template>
            </b-dropdown>
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <!--<b-button
                  type="is-light"
                  label="SUZYtfr"
                  :icon-right="active ? 'angle-up' : 'angle-down'"
                  icon-left="bell"
                >-->
                <!-- <div style="/*background-color: red;*/ width: 22px; height: 22px">
                  <b-image
                    src="https://nsa39.casimages.com/img/2018/02/16/mini_180216012732482019.jpg"
                    alt="Logo forum HPF"
                    style="width: 22px; height: 22px"
                    :rounded="true"
                    :responsive="true"
                  /> 
                </div>-->
                <!-- SUZYtfr -->
                <!--</b-button>-->
                <button
                  type="button"
                  class="button is-light"
                  style="padding-left: 8px"
                >
                  <b-image
                    src="https://nsa39.casimages.com/img/2018/02/16/mini_180216012732482019.jpg"
                    alt="Logo forum HPF"
                    style="width: 22px; height: 22px: margin-left: -8px;"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span style="margin-left: 5px">SUZYftr</span>
                  <b-icon :icon="active ? 'angle-up' : 'angle-down'"> </b-icon>
                </button>
              </template>
              <b-dropdown-item aria-role="listitem">Mon compte</b-dropdown-item>
              <b-dropdown-item aria-role="listitem"
                >Se déconnecter</b-dropdown-item
              >
            </b-dropdown>
          </b-navbar-item>
          <b-navbar-item tag="div" v-else>
            <div class="buttons">
              <a class="button is-light" @click="loginModalActive = true">
                Se connecter
              </a>
              <a class="button" @click="registerModalActive = true">
                S'inscrire
              </a>
            </div>
          </b-navbar-item>
        </div>
      </template>
    </b-navbar>
    <!-- Bannière -->
    <section id="banner" class="hero">
      <div class="hero-body">
        <div class="container">
          <h1>Harry Potter Fanfiction</h1>
        </div>
      </div>
    </section>
    <!-- Modal de contact -->
    <Contact
      :active="contactModalActive"
      @change="(value) => (contactModalActive = value)"
    />
    <!-- Modal de connexion -->
    <Login
      :active="loginModalActive"
      @change="(value) => (loginModalActive = value)"
    />
    <!-- Modal d'inscription -->
    <Register
      :active="registerModalActive"
      @change="(value) => (registerModalActive = value)"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { UserModule } from "@/utils/store-accessor";
import Login from "~/components/Login.vue";
import Register from "~/components/Register.vue";
import Contact from "~/components/Contact.vue";

@Component({
  name: "Navbar",
  components: {
    Login,
    Register,
    Contact
  },
})
export default class extends Vue {
  //#region Data
  private loginModalActive: boolean = false;
  private registerModalActive: boolean = false;
  private contactModalActive: boolean = false;
  //#endregion

  //#region Computed
  get ConnectedVisibility() {
    return UserModule.token.length > 0;
  }
  //#endregion
}
</script>

<style lang="css" scoped>
.hero-body {
  background-image: url("https://cdn.pixabay.com/photo/2017/02/04/04/56/hogwarts-2036645_960_720.jpg");
}
#banner h1 {
  font-size: 50px;
  background-color: rgba(255, 255, 255, 0.6);
  font-family: "Amiri", serif;
  text-transform: uppercase;
  text-align: center;
  padding: 0px 20px;
}

@media screen and (max-width: 450px) {
  .username-visibility {
    display: none;
  }
}
@media screen and (min-width: 450px) {
  .username-visibility {
    display: inline;
  }
}
</style>