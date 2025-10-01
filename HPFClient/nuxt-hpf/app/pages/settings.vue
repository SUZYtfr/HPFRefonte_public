<template>
  <div class="container is-fluid py-5 is-flex is-flex-direction-column">
    <div class="columns is-flex-grow-5">
      <div class="column is-narrow">
        <div class="card fullheight">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Réglages</p>
          </header>
          <div class="card-content px-0 py-3">
            <b-input placeholder="Filtrer" type="search" icon="search" class="mx-2 mb-2" @input="filterChanged" />
            <b-menu>
              <b-menu-list>
                <!-- Override la template défault pour fix le bug des nuxt-link plus reconnu -->
                <template #default>
                  <li v-for="(item, index) in filteredMenuItems" :key="index" @click="() => handleMenuItemClick(item)">
                    <NuxtLink
                      :class="['icon-text', { 'is-active': item.isActive }]"
                      prefetch-on="interaction"
                      :to="item.to"
                    >
                      <b-icon pack="fas" :icon="item.icon" size="is-small" /><span>{{ item.label }}</span>
                    </NuxtLink>
                  </li>
                </template>
              </b-menu-list>
            </b-menu>
          </div>
        </div>
      </div>
      <div v-show="activeItem != ''" class="column is-auto">
        <div class="card fullheight">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              {{ activeItem }}
            </p>
          </header>
          <div class="card-content px-0 py-3">
            <!-- Administration -->
            <NuxtPage class="px-3" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MenuItem } from "~/types/other.ts";

// Metadata, SEO et droits d'accès à la page
definePageMeta({
  auth: true,
  requireStaff: true,
  layout: "settings",
});

//#region Reactive
// Menu actif
const activeItem = ref<string>("");
// Filtre
const filter = ref<string>("");
// Timer de debounce sur le filtre
const timerThrottleFilter = ref<number>(0);
// Menus
const menuItems = ref<MenuItem[]>([
  {
    label: "Validation des chapitres",
    icon: "book",
    tag: "nuxt-link",
    to: "/settings/chapters-batch",
    keywords: "moderation fictions",
    isActive: false,
  },
  {
    label: "Modération des news",
    icon: "newspaper",
    tag: "nuxt-link",
    to: "/settings/news",
    keywords: "moderation news",
    isActive: false,
  },
  {
    label: "Modération des sélections",
    icon: "trophy",
    tag: "nuxt-link",
    to: "/settings/selections",
    keywords: "moderation selections podiums",
    isActive: false,
  },
  {
    label: "Modération des utilisateurs",
    icon: "users",
    tag: "nuxt-link",
    to: "/settings/users",
    keywords: "moderation utilisateurs users",
    isActive: false,
  },
  {
    label: "Modération des reviews",
    icon: "comments",
    tag: "nuxt-link",
    to: "/settings/reviews",
    keywords: "moderation commentaires reviews",
    isActive: false,
  },
  {
    label: "Gestion des catégories",
    icon: "list-alt",
    tag: "nuxt-link",
    to: "/settings/characteristics",
    keywords: "gestion categories",
    isActive: false,
  },
  {
    label: "Gestion des images",
    icon: "images",
    tag: "nuxt-link",
    to: "/settings/",
    keywords: "gestion images",
    isActive: false,
  },
  {
    label: "Administration des pages",
    icon: "columns",
    tag: "nuxt-link",
    to: "/settings/",
    keywords: "page personalisees",
    isActive: false,
  },
  {
    label: "Statistiques",
    icon: "chart-pie",
    tag: "nuxt-link",
    to: "/settings/",
    keywords: "stats statistiques graph",
    isActive: false,
  },
  {
    label: "Thèmes et charte graphique",
    icon: "paint-brush",
    tag: "a",
    to: "/settings/themes",
    keywords: "design charte graphique themes",
    isActive: false,
  },
  {
    label: "Signalements",
    icon: "exclamation-triangle",
    tag: "a",

    to: "/settings/",
    keywords: "moderation signalements",
    isActive: false,
  },
  {
    label: "Administration",
    icon: "tools",
    keywords: "admin",
    isActive: false,
    subItems: [
      { label: "", icon: "", keywords: "", isActive: false },
      { label: "", icon: "", keywords: "", isActive: false },
    ],
  },
]);
//#endregion

//#region Computed
const filteredMenuItems = computed(() => {
  if (filter.value.length > 0) {
    return menuItems.value.filter((item: MenuItem) =>
      item.keywords.includes(
        filter.value
          .trim()
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036F]/g, ""),
      ),
    );
  } else {
    return menuItems.value;
  }
});
//#endregion

//#region Methods
// Clic sur un menu -> affichage dans le volet du milieu
const handleMenuItemClick = (clickedMenu: MenuItem): void => {
  menuItems.value.forEach((item: MenuItem) => {
    item.isActive = false;
  });
  clickedMenu.isActive = true;
  activeItem.value = clickedMenu.label;
};

// Filtrer les menus
const filterChanged = (e: InputEvent): void => {
  clearTimeout(timerThrottleFilter.value);
  timerThrottleFilter.value = window.setTimeout(() => {
    filter.value = (e.target as HTMLInputElement).value ?? "";
  }, 300);
};
//#endregion
</script>

<style lang="scss">
//@import "~/assets/scss/custom.scss";
.fullheight {
  height: 100%;
}

@media screen and (max-width: 768px) {
  li:not(.is-active) > a > span:not(.icon) {
    visibility: visible !important;
  }
}
</style>
