<template>
  <div id="main-container" class="container px-5">
    <!-- Author row -->
    <div id="author-container" class="columns mt-2">
      <div id="author-info" class="column is-4">
        <div class="card">
          <header class="card-header">
            <!-- Infos auteur skeleton -->
            <div v-if="userLoading" class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <BSkeleton width="48px" height="48px" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">
                  <BSkeleton size="is-large" />
                </p>
                <p class="subtitle is-7">
                  <BSkeleton width="40%" />
                </p>
                <p class="subtitle is-7">
                  <BSkeleton width="55%" />
                </p>
              </div>
            </div>
            <!-- Infos auteur -->
            <div v-else class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img src="https://bulma.io/assets/images/placeholders/96x96.png" alt="Placeholder image" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">
                  {{ user.username }}
                </p>
                <p class="subtitle is-7">
                  {{ user.profile?.realname }}
                </p>
                <p class="subtitle is-7">
                  Inscrit le
                  <strong>{{ user.firstSeen?.toLocaleDateString("fr-FR") }}</strong>
                </p>
              </div>
              <div class="media-right">
                <div class="block favorite-rate">
                  <BTooltip label="Ajouter aux favoris" position="is-right" append-to-body>
                    <BRate
                      icon-pack="fas"
                      icon="star"
                      :max="1"
                      size="is-medium"
                      locale="fr-FR"
                      :show-score="false"
                      :show-text="false"
                    />
                  </BTooltip>
                </div>
              </div>
            </div>
          </header>
          <div class="card-content">
            <div class="content is-flex is-flex-direction-column is-justify-content-space-between">
              <section>
                <!-- Tag list auteur skeleton -->
                <BTaglist v-if="userLoading">
                  <BSkeleton />
                </BTaglist>
                <!-- Tag list auteur -->
                <BTaglist v-else>
                  <BTag v-if="user.isPremium" type="is-primary">
                    <strong class="has-text-light">Adhérent</strong>
                  </BTag>
                  <BTag v-if="user.isBeta" type="is-info">
                    <strong class="has-text-light">Betareader</strong>
                  </BTag>
                </BTaglist>
              </section>
              <section class="author-contact-link">
                <!-- Contact link auteur skeleton -->
                <div v-if="userLoading" class="columns is-mobile is-multiline pt-2">
                  <div v-for="t in 6" :key="t" class="column is-4 py-1">
                    <BSkeleton circle width="32px" height="32px" />
                  </div>
                </div>
                <!-- Contact link auteur -->
                <div
                  v-else-if="user.profile?.links?.length"
                  class="is-flex is-flex-direction-row is-align-content-space-around is-align-items-center"
                >
                  <!-- <UserLink
                    v-for="(link, innerindex) of user.profile.links"
                    :key="innerindex"
                    :link="link"
                    :full-length="innerindex < 2"
                  /> -->
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
                <div v-if="userLoading" class="columns is-mobile is-multiline is-centered">
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          <BSkeleton position="is-centered" width="35px" />
                        </p>
                        <p class="heading">
                          <BSkeleton width="70px" />
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
                          {{ numberToString(user.stats?.fictionCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Fanfiction" + ((user.stats?.fictionCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ numberToString(user.stats?.chapterCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Chapitre" + ((user.stats?.chapterCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ numberToString(user.stats?.wordCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Mot" + ((user.stats?.wordCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ numberToString(user.stats?.collectionCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Série" + ((user.stats?.collectionCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ numberToString(user.stats?.challengeCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Challenge" + ((user.stats?.challengeCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="column is-4">
                    <div class="level-item has-text-centered">
                      <div>
                        <p class="is-size-6 has-text-weight-semibold">
                          {{ numberToString(user.stats?.reviewCount ?? 0) }}
                        </p>
                        <p class="heading">
                          {{ "Review" + ((user.stats?.reviewCount ?? 0) > 1 ? "s" : "") }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
          <footer class="card-footer">
            <a href="#" class="card-footer-item"><BIcon icon="envelope" type="is-dark" /><span>Contacter</span></a>
            <a href="#" class="card-footer-item"
              ><BIcon icon="exclamation-triangle" type="is-dark" /><span>Signaler</span></a
            >
          </footer>
        </div>
      </div>
      <div id="author-bio" class="column is-8">
        <div class="card">
          <div class="card-content p-0">
            <Simplebar class="custom-scrollbar-bio" data-simplebar-auto-hide="false">
              <div class="content">
                <BLoading v-if="userLoading" :is-full-page="false" :model="true" />
                <RichtextReader v-else :text="user.profile?.bio || ''" />
              </div>
            </Simplebar>
          </div>
        </div>
      </div>
    </div>
    <!-- Author detail -->
    <div class="columns mt-2 mb-2">
      <div class="column is-12">
        <div id="author-detail" class="card">
          <div class="card-content pt-3 pb-0">
            <BTabs type="is-boxed">
              <BTabItem>
                <template #header>
                  <BIcon icon="broom" />
                  <span>
                    Fanfictions<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag v-else rounded>
                      {{ user.stats?.fictionCount }}
                    </BTag>
                  </span>
                </template>
                <FictionFilters :filters="fanfictionFilters" :search-fictions />
                <div class="columns mt-2">
                  <div class="column is-12">
                    <FictionList
                      :is-card="false"
                      :paginated-fanfictions
                      :search-fictions
                      :fanfiction-filters
                      :order="fictionOrder"
                      :pagination="fictionPagination"
                    />
                  </div>
                </div>
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="book" />
                  <span>
                    Séries
                    <BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag v-else rounded>
                      {{ user.stats?.collectionCount }}
                    </BTag>
                  </span>
                </template>
                2
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="feather" />
                  <span>
                    Reviews<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag v-else rounded>
                      {{ user.stats?.reviewCount }}
                    </BTag>
                  </span>
                </template>
                3
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="trophy" />
                  <span>
                    Challenges<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag v-else rounded>
                      {{ user.stats?.challengeCount }}
                    </BTag>
                  </span>
                </template>
                4
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="star" />
                  <span>
                    Fanfictions favorites<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag
                      v-else
                      rounded
                    >
                      {{ user.stats?.favoriteFictionCount }}
                    </BTag>
                  </span>
                </template>
                5
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="star" />
                  <span>
                    Séries favorites<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag
                      v-else
                      rounded
                    >
                      {{ user.stats?.favoriteCollectionCount }}
                    </BTag>
                  </span>
                </template>
                6
              </BTabItem>
              <BTabItem>
                <template #header>
                  <BIcon icon="star" />
                  <span>
                    Auteurs favoris<BLoading v-if="userLoading" :is-full-page="false" :model="true" /><BTag
                      v-else
                      rounded
                    >
                      {{ user.stats?.favoriteAuthorCount }}
                    </BTag>
                  </span>
                </template>
                7
              </BTabItem>
            </BTabs>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BSkeleton, BLoading, BTabs, BTabItem, BIcon, BTaglist, BTag } from "buefy";
import { plainToInstance } from "class-transformer";
import { UserData } from "~/types/users";
import SimpleBar from "simplebar-vue";
import type { FictionFilters, FictionOrder, OffsetPaginationInput } from "#gql";
import { Ordering } from "#gql/default";
import { FanfictionModel } from "~/models";

const { params } = useRoute();

const { data: user, status: userStatus } = await useAsyncGql(
  "getUser",
  {
    userId: params.userId as string,
  },
  {
    transform: (input) => {
      return plainToInstance(UserData, input.user);
    },
  },
);
const userLoading = computed(() => userStatus.value == "pending");

const fictionOrder = ref<FictionOrder>({
  lastUpdateDate: Ordering.DESC,
});
const fictionPagination = ref<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});

const fanfictionFilters = ref<FictionFilters>({
  creationUser: {
    id: {
      exact: params.userId as string,
    },
  },
});
const { data: paginatedFanfictions, execute: searchFictions } = await useAsyncGql(
  "searchAuthorFictions",
  {
    pagination: fictionPagination,
    order: fictionOrder,
    filters: fanfictionFilters,
  },
  {
    lazy: true,
    transform: (input) => {
      return {
        ...input.fictions,
        results: plainToInstance(FanfictionModel, input.fictions.results),
      };
    },
  },
);

const numberToString = (number: number): string => {
  if (number > 9999) return (number / 1000).toString() + " K";
  else return number.toString();
};

onMounted(() => {
  const tabs = document.getElementsByClassName("tabs is-boxed")[0];
  const scrollbarTabs = document.getElementsByClassName("custom-scrollbar-tabs")[0];
  if (tabs && scrollbarTabs) {
    tabs.insertAdjacentHTML("beforebegin", '<div class="custom-scrollbar-tabs"></div>');
    scrollbarTabs.appendChild(tabs);
    new SimpleBar(document.getElementsByClassName("custom-scrollbar-tabs")[0] as HTMLElement, {
      autoHide: false,
      forceVisible: true,
    });
  }
});
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";

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
  color: var(--primary) !important;
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
