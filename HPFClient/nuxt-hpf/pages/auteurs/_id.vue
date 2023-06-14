<template>
  <div id="main-container" class="container px-5">
    <!-- Author row -->
    <div id="author-container" class="columns mt-2">
      <div id="author-info" class="column is-4">
        <div class="card">
          <header class="card-header">
            <!-- Infos auteur skeleton -->
            <div v-if="userLoading || user == undefined" class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <b-skeleton width="48px" height="48px" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">
                  <b-skeleton size="is-large" />
                </p>
                <p class="subtitle is-7">
                  <b-skeleton width="40%" />
                </p>
                <p class="subtitle is-7">
                  <b-skeleton width="55%" />
                </p>
              </div>
            </div>
            <!-- Infos auteur -->
            <div v-else class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img
                    src="https://bulma.io/images/placeholders/96x96.png"
                    alt="Placeholder image"
                  >
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">
                  {{ user.username }}
                </p>
                <p class="subtitle is-7">
                  {{ user.profile?.realname }}
                </p>
                <p v-if="user.first_seen" class="subtitle is-7">
                  Inscrit le
                  <strong>{{ user.first_seen.toLocaleDateString() }}</strong>
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
                    />
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
                  <b-skeleton />
                </b-taglist>
                <!-- Tag list auteur -->
                <b-taglist v-else>
                  <b-tag v-if="user.is_premium" type="is-primary">
                    <strong class="has-text-light">Adhérent</strong>
                  </b-tag>
                  <b-tag v-if="user.is_beta" type="is-info">
                    <strong class="has-text-light">Betareader</strong>
                  </b-tag>
                </b-taglist>
              </section>
              <section class="author-contact-link">
                <!-- Contact link auteur skeleton -->
                <div
                  v-if="userLoading || user == undefined"
                  class="columns is-mobile is-multiline pt-2"
                >
                  <div v-for="t in 6" :key="t" class="column is-4 py-1">
                    <b-skeleton circle width="32px" height="32px" />
                  </div>
                </div>
                <!-- Contact link auteur -->
                <div
                  v-else-if="user != undefined && (user?.links?.length ?? 0) > 0"
                  class="
                    is-flex
                    is-flex-direction-row
                    is-align-content-space-around
                    is-align-items-center
                  "
                >
                  <UserLink
                    v-for="(link, innerindex) of user.links"
                    :key="innerindex"
                    :link="link"
                    :full-length="innerindex < 2"
                  />
                </div>
                <!-- <div
                  class="
                    columns
                    is-mobile is-multiline is-centered is-vcentered
                    pt-2
                    is-fullheight
                  "
                  v-else-if="user != undefined && user.links.length > 0"
                >
                  <div
                    class="column is-4 py-1"
                    v-for="(link, innerindex) of user.links"
                    :key="innerindex"
                  >
                    <UserLink
                      :link="link"
                      :fullLength="innerindex < 2"
                    ></UserLink>
                  </div>
                </div> -->
              </section>
              <section class="author-stats mt-2">
                <!-- Stats auteur skeleton -->
                <div
                  v-if="userLoading || user == undefined"
                  class="columns is-mobile is-multiline is-centered"
                >
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <b-skeleton
                            position="is-centered"
                            width="35px"
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
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
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
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
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
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
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
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
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
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
                          />
                        </p>
                        <p class="heading">
                          <b-skeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Stats auteur -->
                <div v-else class="columns is-mobile is-multiline is-centered">
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.fiction_count ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Fanfiction" +
                              ((user?.stats?.fiction_count ?? 0) > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.chapter_count ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Chapitre" + ((user?.stats?.chapter_count ?? 0) > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.word_count ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Mot" + ((user?.stats?.word_count ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.collection_count ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Série" + ((user?.stats?.collection_count ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.challenges ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{
                            "Challenge" + ((user?.stats?.challenges ?? 0) > 1 ? "s" : "")
                          }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ (user?.stats?.review_count ?? 0) | numberToString }}
                        </p>
                        <p class="heading">
                          {{ "Review" + ((user?.stats?.review_count ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
          <footer class="card-footer">
            <a
              href="#"
              class="card-footer-item"
            ><b-icon icon="envelope" type="is-dark" /><span>Contacter</span></a>
            <a
              href="#"
              class="card-footer-item"
            ><b-icon icon="exclamation-triangle" type="is-dark" /><span>Signaler</span></a>
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
                  v-if="userLoading || user == undefined"
                  :is-full-page="false"
                  :model="true"
                />
                <span v-else v-html="user.profile?.bio" />
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
                  <b-icon icon="broom" />
                  <span>
                    Fanfictions<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded>
                      {{ user?.stats?.fiction_count }}
                    </b-tag>
                  </span>
                </template>
                <FanfictionFiltersSmall :fanfiction-filters="fanfictionFilters" />
                <div class="columns mt-2">
                  <div class="column is-12">
                    <FanfictionList
                      :is-card="false"
                      :fanfiction-filters="fanfictionFilters"
                    />
                  </div>
                </div>
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="book" />
                  <span>
                    Séries
                    <b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded> {{ user?.stats?.collection_count }} </b-tag>
                  </span>
                </template>
                2
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="feather" />
                  <span>
                    Reviews<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded> {{ user?.stats?.review_count }} </b-tag>
                  </span>
                </template>
                3
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="trophy" />
                  <span>
                    Challenges<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded> {{ user?.stats?.challenges }} </b-tag>
                  </span>
                </template>
                4
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star" />
                  <span>
                    Fanfictions favorites<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded>
                      {{ user?.stats?.favorites_fanfictions }}
                    </b-tag>
                  </span>
                </template>
                5
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star" />
                  <span>
                    Séries favorites<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded>
                      {{ user?.stats?.favorites_series }}
                    </b-tag>
                  </span>
                </template>
                6
              </b-tab-item>
              <b-tab-item>
                <template #header>
                  <b-icon icon="star" />
                  <span>
                    Auteurs favoris<b-loading
                      v-if="userLoading || user == undefined"
                      :is-full-page="false"
                      :model="true"
                    /><b-tag v-else rounded>
                      {{ user?.stats?.favorites_author }}
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
import { SerialiseClass } from "@/serialiser-decorator";
import UserLink from "@/components/UserLink.vue";
import FanfictionFiltersSmall from "~/components/filters/fanfictions/FanfictionFiltersSmall.vue";
import { UserModel } from "@/models/users";
import { IFanfictionFilters } from "@/types/fanfictions";
import { getUser } from "@/api/users";
import FanfictionList from "~/components/list/fanfictions/FanfictionList.vue";
import { SortByEnum } from "~/types/basics";

@Component({
  name: "Author",
  components: {
    simplebar,
    UserLink,
    FanfictionFiltersSmall,
    FanfictionList
  },
  filters: {
    parseTime: (timestamp: string) => {
      return new Date(timestamp).toLocaleDateString();
    },
    numberToString: (number: number) => {
      if (number > 9999) return (number / 1000).toString() + " K";
      else return number.toString();
    }
  }
})
export default class extends Vue {
  // #region  Data
  @SerialiseClass(UserModel)
  public user: UserModel | null = null;

  public userLoading = false;

  // Filtres de recherche
  public fanfictionFilters: IFanfictionFilters = {
    searchTerm: "",
    searchAuthor: "",
    searchAuthorId: Number(this.$route.params.id),
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
    page: 1,
    pageSize: 10,
    totalPages: true,
    sortOn: "last_update_date",
    sortBy: SortByEnum.Descending
  };

  // #endregion

  // #region Hooks
  mounted(): void {
    const tabs = document.getElementsByClassName("tabs is-boxed")[0];
    console.log(tabs);
    tabs.insertAdjacentHTML(
      "beforebegin",
      '<div class="custom-scrollbar-tabs"></div>'
    );
    const scrollbarTabs = document.getElementsByClassName(
      "custom-scrollbar-tabs"
    )[0];
    scrollbarTabs.appendChild(tabs);
    new SimpleBar(
      document.getElementsByClassName(
        "custom-scrollbar-tabs"
      )[0] as HTMLElement,
      {
        autoHide: false,
        forceVisible: true
      }
    );
  }

  private async fetch(): Promise<void> {
    this.userLoading = true;
    try {
      this.user = (await getUser(parseInt(this.$route.params.id)));
    } catch (error) {
      if (process.client) {
        this.$buefy.snackbar.open({
          duration: 5000,
          message: "Une erreur s'est produite lors de la récupération de l'utilisateur",
          type: "is-danger",
          position: "is-bottom-right",
          actionText: null,
          pauseOnHover: true,
          queue: true
        });
      } else {
        console.log(error);
      }
    } finally {
      this.userLoading = false;
    }
  }
  // #endregion

  // #region Computed
  // #endregion

  // #region Methods
  // #endregion
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
