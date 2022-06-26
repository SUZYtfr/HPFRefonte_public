<template>
  <div id="main-container" class="container px-5">
    <!-- Author row -->
    <div id="author-container" class="columns mt-2">
      <div id="author-info" class="column is-4">
        <div class="card">
          <header class="card-header">
            <!-- Infos auteur skeleton -->
            <div class="media" v-if="userLoading || user == undefined">
              <div class="media-left">
                <figure class="image is-48x48">
                  <b-skeleton width="48px" height="48px"></b-skeleton>
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">
                  <b-skeleton size="is-large"></b-skeleton>
                </p>
                <p class="subtitle is-7">
                  <b-skeleton width="40%"></b-skeleton>
                </p>
                <p class="subtitle is-7">
                  <b-skeleton width="55%"></b-skeleton>
                </p>
              </div>
            </div>
            <!-- Infos auteur -->
            <div class="media" v-else>
              <div class="media-left">
                <figure class="image is-48x48">
                  <img
                    src="https://bulma.io/images/placeholders/96x96.png"
                    alt="Placeholder image"
                  />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">{{ user.nickname }}</p>
                <p class="subtitle is-7">{{ user.realname }}</p>
                <p class="subtitle is-7">
                  Inscrit le
                  <strong>{{ user.creation_date | parseTime }}</strong>
                </p>
              </div>
              <div class="media-right">
                <div class="block favorite-rate">
                  <b-tooltip
                    label="Ajouter aux favoris"
                    position="is-right"
                    append-to-body
                  >
                    <b-rate
                      icon-pack="fas"
                      icon="star"
                      :max="1"
                      size="is-medium"
                      locale="fr-FR"
                      :show-score="false"
                      :show-text="false"
                    >
                    </b-rate>
                  </b-tooltip>
                </div>
              </div>
            </div>
          </header>
          <div class="card-content">
            <div
              class="
                content
                is-flex
                is-flex-direction-column
                is-justify-content-space-between
              "
            >
              <section>
                <!-- Tag list auteur skeleton -->
                <b-taglist v-if="userLoading || user == undefined">
                  <b-skeleton></b-skeleton>
                </b-taglist>
                <!-- Tag list auteur -->
                <b-taglist v-else>
                  <b-tag type="is-primary" v-if="user.is_premium"
                    ><strong class="has-text-light">Adhérent</strong></b-tag
                  >
                  <b-tag type="is-info" v-if="user.is_beta"
                    ><strong class="has-text-light">Betareader</strong></b-tag
                  >
                </b-taglist>
              </section>
              <section class="author-contact-link">
                <!-- Contact link auteur skeleton -->
                <div
                  class="columns is-mobile is-multiline pt-2"
                  v-if="userLoading || user == undefined"
                >
                  <div class="column is-4 py-1" v-for="t in 6" v-bind:key="t">
                    <b-skeleton circle width="32px" height="32px"></b-skeleton>
                  </div>
                </div>
                <!-- Contact link auteur -->
                <div
                  class="
                    columns
                    is-mobile is-multiline is-centered is-vcentered
                    pt-2
                    is-fullheight
                  "
                  v-else-if="user != undefined && user.links.length > 0"
                >
                  <div
                    class="column is-narrow py-1"
                    v-for="(link, innerindex) of user.links"
                    :key="innerindex"
                  >
                    <UserLink
                      :link="link"
                      :fullLength="innerindex < 2"
                    ></UserLink>
                  </div>
                </div>
              </section>
              <section class="author-stats mt-2">
                <!-- Stats auteur skeleton -->
                <div
                  class="columns is-mobile is-multiline is-centered"
                  v-if="userLoading || user == undefined"
                >
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          ></b-skeleton>
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px"></b-skeleton>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Stats auteur -->
                <div class="columns is-mobile is-multiline is-centered" v-else>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.fanfictions | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Fanfiction" +
                            (user.stats.fanfictions > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.chapters | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Chapitre" + (user.stats.chapters > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.words | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Mot" + (user.stats.words > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.series | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Série" + (user.stats.series > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.challenges | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Challenge" + (user.stats.challenges > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ user.stats.reviews | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Review" + (user.stats.reviews > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
          <footer class="card-footer">
            <a href="#" class="card-footer-item"
              ><b-icon icon="envelope" type="is-dark"></b-icon
              ><span>Contacter</span></a
            >
            <a href="#" class="card-footer-item"
              ><b-icon icon="exclamation-triangle" type="is-dark"></b-icon
              ><span>Signaler</span></a
            >
          </footer>
        </div>
      </div>
      <div id="author-bio" class="column is-8">
        <div class="card">
          <div class="card-content p-0">
            <simplebar
              class="custom-scrollbar-bio"
              data-simplebar-auto-hide="false"
            >
              <div class="content">
                <b-loading
                  :is-full-page="false"
                  :model="true"
                  v-if="userLoading || user == undefined"
                ></b-loading>
                <span v-else v-html="user.bio"></span>
              </div>
            </simplebar>
          </div>
        </div>
      </div>
    </div>
    <!-- Author detail -->
    <div class="columns mt-2 mb-2">
      <div class="column is-12">
        <div id="author-detail" class="card">
          <div class="card-content pt-3 pb-0">
            <b-tabs type="is-boxed">
              <b-tab-item>
                <template #header>
                  <b-icon icon="broom"></b-icon>
                  <span>
                    Fanfictions<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded>
                      {{ user.stats.fanfictions }}
                    </b-tag>
                  </span>
                </template>
                <FanfictionFilters
                  :fanfictionFilters="fanfictionFilters"
                />
                <div class="columns mt-2">
                  <div class="column is-12">
                    <FanfictionList
                      :isCard="false"
                      :fanfictionFilters="fanfictionFilters"
                    />
                  </div>
                </div>
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="book"></b-icon>
                  <span>
                    Séries
                    <b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded> {{ user.stats.series }} </b-tag>
                  </span>
                </template>
                2
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="feather"></b-icon>
                  <span>
                    Reviews<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded> {{ user.stats.reviews }} </b-tag>
                  </span>
                </template>
                3
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="trophy"></b-icon>
                  <span>
                    Challenges<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded> {{ user.stats.challenges }} </b-tag>
                  </span>
                </template>
                4
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star"></b-icon>
                  <span>
                    Fanfictions favorites<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded>
                      {{ user.stats.favorites_fanfictions }}
                    </b-tag>
                  </span>
                </template>
                5
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star"></b-icon>
                  <span>
                    Séries favorites<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded>
                      {{ user.stats.favorites_series }}
                    </b-tag>
                  </span>
                </template>
                6
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star"></b-icon>
                  <span>
                    Auteurs favoris<b-loading
                      :is-full-page="false"
                      :model="true"
                      v-if="userLoading || user == undefined"
                    ></b-loading
                    ><b-tag v-else rounded>
                      {{ user.stats.favorites_author }}
                    </b-tag>
                  </span>
                </template>
                7
              </b-tab-item>
            </b-tabs>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import simplebar from "simplebar-vue";
import "simplebar/dist/simplebar.min.css";
import "simplebar/dist/simplebar.min.js";
import SimpleBar from "simplebar";
import UserLink from "@/components/UserLink.vue";
import FanfictionFilters from "~/components/filters/fanfictions/FanfictionFiltersSmall.vue";
import { UserData } from "@/types/users";
import { FanfictionFiltersData } from "@/types/fanfictions";
import { getUser } from "@/api/users";
import FanfictionList from "~/components/list/fanfictions/FanfictionList.vue";

@Component({
  name: "Author",
  components: {
    simplebar,
    UserLink,
    FanfictionFilters,
    FanfictionList,
  },
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    },
    numberToString: (number: number) => {
      if (number > 9999) return (number / 1000).toString() + " K";
      else return number.toString();
    },
  },
})
export default class extends Vue {
  //#region  Data
  private user!: UserData;
  private userLoading = false;

  // Filtres de recherche
  private fanfictionFilters: FanfictionFiltersData = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: 0,
    sortBy: "most_recent",
    multipleAuthors: null,
    status: null,
    minWords: null,
    maxWords: null,
    includedTags: [],
    excludedTags: [],
    customTags: [],
    featured: false,
    inclusive: false,
    fromDate: null,
    toDate: null,
    currentPage: 1,
    perPage: 10,
  };

  //#endregion

  //#region Hooks
  created() {
    this.user = null!;
  }

  mounted() {
    let tabs = document.getElementsByClassName("tabs is-boxed")[0];
    console.log(tabs);
    tabs.insertAdjacentHTML(
      "beforebegin",
      '<div class="custom-scrollbar-tabs"></div>'
    );
    let scrollbarTabs = document.getElementsByClassName(
      "custom-scrollbar-tabs"
    )[0];
    scrollbarTabs.appendChild(tabs);
    new SimpleBar(
      document.getElementsByClassName(
        "custom-scrollbar-tabs"
      )[0] as HTMLElement,
      {
        autoHide: false,
        forceVisible: true,
      }
    );
  }

  async asyncData() {
    console.log("asyncData");
  }

  async fetch() {
    this.userLoading = true;
    console.log("fetch");
    try {
      this.user = (await getUser(this.$route.params.id)).data.items.user;
      console.log(this.user);
    } catch (error) {
      console.log(error);
    } finally {
      console.log("finally");
      this.userLoading = false;
    }
  }
  //#endregion

  //#region Computed
  //#endregion

  
  //#region Methods
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

#main-container {
  min-height: 100vh;
}

#author-bio .card {
  height: 20rem;
}

.custom-scrollbar-bio {
  height: 20rem;
  padding: 1.5rem;
}

#author-info .card {
  height: 20rem;
  display: flex;
  flex-direction: column;
}

#author-info .card .card-footer {
  margin-top: auto;
}

#author-info .card .card-header {
  padding: 10px;
}

#author-info .card .card-header .media-content .title {
  /*margin-bottom: 1.2rem;*/
  /*margin-top: 0.3rem;*/
  margin-bottom: 0rem;
  margin-top: -0.3rem;
}

#author-info .card .card-header .media-content .subtitle {
  margin: 0rem;
}

#author-info .card .card-header .media {
  width: 100%;
  display: flex;
  flex-direction: row;
}

#author-info .card .card-header .media-right {
  margin-left: auto;
  height: 100%;
  display: flex;
  flex-direction: row;
}

#author-info .card .card-header .media-right .block {
  margin-bottom: auto;
  margin-top: auto;
}

#author-info .level-item .heading {
  margin-bottom: 0px;
}

.custom-scrollbar-tabs {
  min-width: 100%;
}

.block.favorite-rate {
  margin-right: 5px;
}
.block.contact button {
  font-size: 0.9rem;
  border-radius: 4px;
}

#author-info .card .card-footer .card-footer-item .icon {
  margin-bottom: -0.1rem;
  margin-right: 0.2rem;
}
#author-info .card .card-footer .card-footer-item .icon:hover {
  color: $primary !important;
}
#author-info .card .card-content .level-item .has-text-weight-semibold {
  margin-bottom: 0rem !important;
}
#author-info .card .card-content {
  padding-top: 0.5rem;
  padding-bottom: 0rem;
}
#author-info .card .card-content .level {
  margin-bottom: 0rem;
}
#author-info .card .card-content .author-contact-link {
  height: 5.8rem;
  /*background-color: red;*/
  padding-top: 0.6rem;
  padding-bottom: 0.4rem;
}

.author-stats .column {
  padding-top: 0rem;
  padding-bottom: 2px;
}

#author-info .card-content .content {
  height: 175px;
}

#author-detail {
  overflow: visible;
}

.characteristic-bg-litteraire {
  background: #e6ccb2 !important;
}
.characteristic-bg-genre {
  background: #fec5bb !important;
}
.characteristic-bg-langue {
  background: #74c69d !important;
}
.characteristic-bg-warning {
  /*background: #e63946 !important;*/
  background: #fcbf49 !important;
}
.characteristic-bg-rating {
  background: #e0aaff !important;
}
.characteristic-bg-epoque {
  background: #4a4e69 !important;
  color: whitesmoke !important;
}
.characteristic-bg-personnage {
  background: #1d3557 !important;
  color: whitesmoke !important;
}
.characteristic-bg-relation {
  background: #a8dadc !important;
}

.characteristic-bg-excluded {
  background: #e63946 !important;
  color: whitesmoke !important;
}
</style>

<style lang="scss">
nav.tabs.is-boxed {
  width: 100% !important;
  display: block !important;
  overflow: visible !important;
  padding-bottom: 10px;
}
</style>