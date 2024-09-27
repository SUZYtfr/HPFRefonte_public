<template>
  <div class="container is-fluid py-5 is-flex is-flex-direction-column">
    <div class="columns is-flex-grow-5">
      <div class="column is-narrow">
        <div class="card fullheight">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">
              Réglages
            </p>
          </header>
          <div class="card-content px-0 py-3">
            <b-input
              placeholder="Filtrer"
              type="search"
              icon="search"
              class="mx-2 mb-2"
              @input="filterChanged"
            />
            <b-menu>
              <b-menu-list>
                <b-menu-item
                  v-for="(item, index) in filteredMenuItems"
                  :key="index"
                  :label="item.label"
                  :icon="item.icon"
                  :tag="item.tag"
                  :to="item.to"
                  :active.sync="item.isactive"
                  @click.native="handleMenuItemClick(item)"
                >
                  <b-menu-item
                    v-for="(subitem, subindex) in item.subitems"
                    :key="subindex"
                    :label="subitem.label"
                    :icon="subitem.icon"
                    :tag="subitem.tag"
                    :to="subitem.to"
                  />
                </b-menu-item>
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
            <NuxtChild class="px-3" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
@Component({
  layout: "settings",
  components: {
  },
  fetchOnServer: true,
  fetchKey: "settings"
})
export default class extends Vue {
  // #region Data
  // Menu actif
  public activeItem: string = "";

  // Filtre
  private filter: string = "";

  // Tous les menus disponibles
  private menuItems: any = [
    { label: "Modération des fictions", icon: "book", tag: "nuxt-link", to: "/settings/fictions", keywords: "moderation fictions", isactive: false },
    { label: "Modération des news", icon: "newspaper", tag: "nuxt-link", to: "/settings/news", keywords: "moderation news", isactive: false },
    { label: "Modération des sélections", icon: "trophy", tag: "nuxt-link", to: "/settings/selections", keywords: "moderation selections podiums", isactive: false },
    { label: "Modération des utilisateurs", icon: "users", tag: "nuxt-link", to: "/settings/users", keywords: "moderation utilisateurs users", isactive: false },
    { label: "Modération des reviews", icon: "comments", tag: "nuxt-link", to: "/settings/reviews", keywords: "moderation commentaires reviews", isactive: false },
    { label: "Gestion des catégories", icon: "list-alt", tag: "nuxt-link", to: "/settings/characteristics", keywords: "gestion categories", isactive: false },
    { label: "Gestion des images", icon: "images", tag: "nuxt-link", to: "/settings/", keywords: "gestion images", isactive: false },
    { label: "Administration des pages", icon: "columns", tag: "nuxt-link", to: "/settings/", keywords: "page personalisees", isactive: false },
    { label: "Statistiques", icon: "chart-pie", tag: "nuxt-link", to: "/settings/", keywords: "stats statistiques graph", isactive: false },
    { label: "Thèmes et charte graphique", icon: "paint-brush", tag: "nuxt-link", to: "/settings/themes", keywords: "design charte graphique themes", isactive: false },
    { label: "Signalements", icon: "exclamation-triangle", tag: "nuxt-link", to: "/settings/", keywords: "moderation signalements", isactive: false },
    { label: "Administration", icon: "tools", keywords: "admin", isactive: false, subitems: [{ label: "", icon: "", tag: null, to: null, keywords: "" }, { label: "", icon: "", tag: null, to: null, keywords: "" }] }
  ];

  // Timer de debounce sur le filtre
  private timerThrottleFilter: number = 0;
  // #endregion

  // #region Computed
  // Menus affichés, éventuellement filtrés
  public get filteredMenuItems(): any {
    if (this.filter.length > 0) {
      return this.menuItems.filter((item: any) => item.keywords.includes(this.filter.trim().toLowerCase().normalize("NFD").replace(/[\u0300-\u036F]/g, "")));
    } else {
      return this.menuItems;
    }
  }
  // #endregion

  // #region Methods
  // Changement de menu à la main
  public handleMenuItemClick(event: any): void {
    this.menuItems.forEach((item: any) => {
      item.isactive = false;
    });
    event.isactive = true;
    this.activeItem = event.label;
  }

  // Filtre de recherche modifié
  public filterChanged(e : string) : void {
    clearTimeout(this.timerThrottleFilter);
    this.timerThrottleFilter = window.setTimeout(
      () => { this.filter = e; },
      300
    );
  }
  // #endregion
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";
.fullheight {
  height: 100%;
}

@media screen and (max-width: 768px) {
  li:not(.is-active) > a > span:not(.icon) {
    visibility: visible !important;
  }
}
</style>
