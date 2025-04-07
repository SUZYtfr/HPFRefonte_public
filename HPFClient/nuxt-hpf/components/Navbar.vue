<template>
  <div>
    <!-- Navbar -->
    <b-navbar active :fixed-top="true">
      <template #brand>
        <b-navbar-item>
          <img
            src="@/assets/img/logo_hpfanfic_court_300.png"
            width="56"
            height="36"
            alt="Logo forum HPF"
          >
        </b-navbar-item>
        <div class="is-hidden-desktop" style="margin-left: auto">
          <b-navbar-item v-if="$auth.loggedIn" tag="div">
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
                      />
                    </svg>
                  </span>
                  <span><span class="badge">8</span></span>
                </button>
              </template>
            </b-dropdown>
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <button
                  type="button"
                  class="button is-light"
                  style="padding-left: 8px"
                >
                  <b-image
                    :src="$auth.user?.profile.profile_picture ?? 'https://bulma.io/assets/images/placeholders/24x24.png'"
                    alt="Image de profil"
                    style="width: 22px; height: 22px; margin-left: -8px;"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span
                    class="username-visibility"
                    style="margin-left: 5px"
                  >{{ $auth.user?.username }}</span>
                  <b-icon :icon="active ? 'angle-up' : 'angle-down'" />
                </button>
              </template>
              <b-dropdown-item aria-role="listitem">
                Mon compte
              </b-dropdown-item>
              <b-dropdown-item aria-role="listitem" @click="logout">
                Se déconnecter
              </b-dropdown-item>
            </b-dropdown>
          </b-navbar-item>
          <b-navbar-item v-else tag="div">
            <div class="buttons">
              <a class="button is-light" @click="ModalsStatesModule.setLoginModalActive(true)">
                Se connecter
              </a>
              <a class="button" @click="ModalsStatesModule.setRegisterModalActive(true)">
                S'inscrire
              </a>
            </div>
          </b-navbar-item>
        </div>
      </template>
      <template #start>
        <b-navbar-item active tag="router-link" to="/">
          Accueil
        </b-navbar-item>
        <b-navbar-dropdown :collapsible="true" label="Association HPF">
          <b-navbar-item href="#">
            Link 1
          </b-navbar-item>
          <b-navbar-item href="#">
            Link 2
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Lecture">
          <b-navbar-item href="#">
            Link 1
          </b-navbar-item>
          <b-navbar-item href="#">
            Link 2
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Ecriture">
          <b-navbar-item href="#">
            Link 1
          </b-navbar-item>
          <b-navbar-item href="#">
            Link 2
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Top fanfictions">
          <b-navbar-item href="#">
            Link 1
          </b-navbar-item>
          <b-navbar-item href="#">
            Link 2
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Nos sites">
          <b-navbar-item href="#">
            L'appli HPF
          </b-navbar-item>
          <b-navbar-item href="#">
            Le Héron
          </b-navbar-item>
          <b-navbar-item href="#">
            Les éditions HPF
          </b-navbar-item>
          <b-navbar-item href="#">
            L'association
          </b-navbar-item>
          <b-navbar-item href="#">
            Le blog HPF
          </b-navbar-item>
          <b-navbar-item href="#">
            Le forum
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-dropdown :collapsible="true" label="Boutique">
          <b-navbar-item href="#">
            Link 1
          </b-navbar-item>
          <b-navbar-item href="#">
            Link 2
          </b-navbar-item>
        </b-navbar-dropdown>
        <b-navbar-item href="#">
          Partenaires
        </b-navbar-item>
        <b-navbar-item href="#" @click="ModalsStatesModule.setContactModalActive(true)">
          Contact
        </b-navbar-item>
        <b-navbar-item active tag="router-link" to="/settings">
          Administration
        </b-navbar-item>
      </template>

      <template #end>
        <div class="is-hidden-touch">
          <b-navbar-item v-if="$auth.loggedIn" tag="div">
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
                      />
                    </svg>
                  </span>
                  <span><span class="badge">8</span></span>
                </button>
              </template>
            </b-dropdown>
            <b-dropdown aria-role="list">
              <template #trigger="{ active }">
                <button
                  type="button"
                  class="button is-light"
                  style="padding-left: 8px"
                >
                  <b-image
                    :src="$auth.user?.profile.profile_picture ?? 'https://bulma.io/assets/images/placeholders/24x24.png'"
                    alt="Image de profil"
                    style="width: 22px; height: 22px; margin-left: -8px;"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span style="margin-left: 5px">{{ $auth.user?.username }}</span>
                  <b-icon :icon="active ? 'angle-up' : 'angle-down'" />
                </button>
              </template>
              <b-dropdown-item aria-role="listitem">
                Mon compte
              </b-dropdown-item>
              <b-dropdown-item aria-role="listitem" @click="logout">
                Se déconnecter
              </b-dropdown-item>
            </b-dropdown>
          </b-navbar-item>
          <b-navbar-item v-else tag="div">
            <div class="buttons">
              <a class="button is-light" @click="ModalsStatesModule.setLoginModalActive(true)">
                Se connecter
              </a>
              <a class="button" @click="ModalsStatesModule.setRegisterModalActive(true)">
                S'inscrire
              </a>
            </div>
          </b-navbar-item>
        </div>
      </template>
    </b-navbar>
    <!-- Modal de contact -->
    <Contact />
    <!-- Modal de connexion -->
    <Login />
    <!-- Modal d'inscription -->  
    <Register />
  </div>
</template>

<script setup lang="ts">
const ModalsStatesModule = ModalsStates();

async function logout(): Promise<void> {
  // Remettre le thème par défaut
  await $auth.logout();
  changeTheme(Config().currentTheme?.details[0] ?? null);
}
</script>

<style lang="css" scoped>
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
