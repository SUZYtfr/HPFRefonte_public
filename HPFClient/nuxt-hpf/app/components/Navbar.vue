<template>
  <div>
    <!-- Navbar -->
    <BNavbar active :fixed-top="true">
      <template #brand>
        <BNavbarItem>
          <img src="~/assets/img/logo_hpfanfic_court_300.png" width="56" height="36" alt="Logo forum HPF" />
        </BNavbarItem>
        <div class="is-hidden-desktop" style="margin-left: auto">
          <BNavbarItem v-if="isAuthenticated" tag="div">
            <BDropdown aria-role="list">
              <template #trigger>
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
            </BDropdown>
            <BDropdown aria-role="list">
              <template #trigger="{ active }">
                <button type="button" class="button is-light" style="padding-left: 8px">
                  <BImage
                    :src="
                      accountData?.profile?.profilePicture ?? 'https://bulma.io/assets/images/placeholders/24x24.png'
                    "
                    alt="Image de profil"
                    style="width: 22px; height: 22px; margin-left: -8px"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span class="username-visibility" style="margin-left: 5px">{{ accountData?.username }}</span>
                  <BIcon :icon="active ? 'angle-up' : 'angle-down'" />
                </button>
              </template>
              <BDropdownItem aria-role="listitem"> Mon compte </BDropdownItem>
              <BDropdownItem aria-role="listitem" @click="logout"> Se déconnecter </BDropdownItem>
            </BDropdown>
          </BNavbarItem>
          <BNavbarItem v-else tag="div">
            <div class="buttons">
              <a class="button is-light" @click="modalsStateStore.setLoginModalActive(true)"> Se connecter </a>
              <a class="button" @click="modalsStateStore.setRegisterModalActive(true)"> S'inscrire </a>
            </div>
          </BNavbarItem>
        </div>
      </template>
      <template #start>
        <BNavbarItem active tag="router-link" to="/"> Accueil </BNavbarItem>
        <BNavbarDropdown :collapsible="true" label="Association HPF">
          <BNavbarItem href="#"> Link 1 </BNavbarItem>
          <BNavbarItem href="#"> Link 2 </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarDropdown :collapsible="true" label="Lecture">
          <BNavbarItem href="#"> Link 1 </BNavbarItem>
          <BNavbarItem href="#"> Link 2 </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarDropdown :collapsible="true" label="Ecriture">
          <BNavbarItem href="#"> Link 1 </BNavbarItem>
          <BNavbarItem href="#"> Link 2 </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarDropdown :collapsible="true" label="Top fanfictions">
          <BNavbarItem href="#"> Link 1 </BNavbarItem>
          <BNavbarItem href="#"> Link 2 </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarDropdown :collapsible="true" label="Nos sites">
          <BNavbarItem href="#"> L'appli HPF </BNavbarItem>
          <BNavbarItem href="#"> Le Héron </BNavbarItem>
          <BNavbarItem href="#"> Les éditions HPF </BNavbarItem>
          <BNavbarItem href="#"> L'association </BNavbarItem>
          <BNavbarItem href="#"> Le blog HPF </BNavbarItem>
          <BNavbarItem href="#"> Le forum </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarDropdown :collapsible="true" label="Boutique">
          <BNavbarItem href="#"> Link 1 </BNavbarItem>
          <BNavbarItem href="#"> Link 2 </BNavbarItem>
        </BNavbarDropdown>
        <BNavbarItem active href="#"> Partenaires </BNavbarItem>
        <BNavbarItem active href="#" @click="modalsStateStore.setContactModalActive(true)"> Contact </BNavbarItem>
        <BNavbarItem v-if="isStaff" active tag="router-link" to="/settings"> Administration </BNavbarItem>
      </template>

      <template #end>
        <div class="is-hidden-touch">
          <BNavbarItem v-if="isAuthenticated" tag="div">
            <BDropdown aria-role="list">
              <template #trigger>
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
            </BDropdown>
            <BDropdown aria-role="list">
              <template #trigger="{ active }">
                <button type="button" class="button is-light" style="padding-left: 8px">
                  <BImage
                    :src="
                      accountData?.profile?.profilePicture ?? 'https://bulma.io/assets/images/placeholders/24x24.png'
                    "
                    alt="Image de profil"
                    style="width: 22px; height: 22px; margin-left: -8px"
                    :rounded="true"
                    :responsive="true"
                  />
                  <span style="margin-left: 5px">{{ accountData?.username }}</span>
                  <BIcon :icon="active ? 'angle-up' : 'angle-down'" />
                </button>
              </template>
              <BDropdownItem aria-role="listitem">Mon compte</BDropdownItem>
              <BDropdownItem aria-role="listitem" has-link>
                <NuxtLink class="dropdown-item" :to="{ name: 'compte-fictions' }" no-prefetch>Mes fictions</NuxtLink>
              </BDropdownItem>
              <BDropdownItem aria-role="listitem" has-link>
                <NuxtLink class="dropdown-item" :to="{ name: 'compte-fictions-écritoire' }" no-prefetch
                  >Nouvelle fiction</NuxtLink
                >
              </BDropdownItem>
              <BDropdownItem aria-role="listitem" has-link>
                <NuxtLink class="dropdown-item" :to="{ name: 'compte-séries' }" no-prefetch>Mes séries</NuxtLink>
              </BDropdownItem>
              <BDropdownItem aria-role="listitem" has-link>
                <NuxtLink class="dropdown-item" :to="{ name: 'compte-séries-écritoire' }" no-prefetch
                  >Nouvelle série</NuxtLink
                >
              </BDropdownItem>
              <BDropdownItem aria-role="listitem" @click="logout">Se déconnecter</BDropdownItem>
            </BDropdown>
          </BNavbarItem>
          <BNavbarItem v-else tag="div">
            <div class="buttons">
              <a class="button is-light" @click="modalsStateStore.setLoginModalActive(true)"> Se connecter </a>
              <a class="button" @click="modalsStateStore.setRegisterModalActive(true)"> S'inscrire </a>
            </div>
          </BNavbarItem>
        </div>
      </template>
    </BNavbar>
    <!-- Modal de contact -->
    <!-- <Contact /> -->
    <!-- Modal de connexion -->
    <Login />
    <!-- Modal d'inscription -->
    <!-- <Register /> -->
  </div>
</template>

<script setup lang="ts">
const { accountData, isAuthenticated, isStaff, signOut } = useCustomAuth();

const modalsStateStore = useModalsStateStore();
const logout = async (): Promise<void> => {
  await signOut();
};
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
