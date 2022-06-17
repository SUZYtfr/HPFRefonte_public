<template>
  <div class="container px-5">
    <br />
    <div class="columns is-reversed-mobile">
      <div class="column is-7-tablet is-8-desktop is-9-widescreen">
        <!-- Nouveautés fanfictions -->
        <div class="card">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Nouveautés</p>
          </header>
          <div class="card-content">
            <div
              class="
                p-2
                columns
                is-variable
                is-1-mobile
                is-2-tablet
                is-3-desktop
                is-3-widescreen
                is-2-fullhd
                is-multiline
              "
            >
              <div
                class="column is-half py-2"
                v-for="(fanfiction, innerindex) of fanfictions"
                :key="'ff_recent_' + fanfiction.fanfiction_id.toString()"
              >
                <FanfictionThumbnail
                  :fanfiction="fanfiction"
                  v-bind:index="innerindex"
                  v-bind:key="fanfiction.fanfiction_id"
                ></FanfictionThumbnail>
              </div>
            </div>
          </div>
          <footer class="card-footer">
            <p class="card-footer-item py-2">
              <span>
                <a href="">Plus de nouveautés</a>
              </span>
            </p>
          </footer>
        </div>
        <br />
        <!-- Sélections fanfictions -->
        <div class="card">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Sélections du mois</p>
          </header>
          <div class="card-content">
            <div
              class="
                p-2
                columns
                is-variable
                is-1-mobile
                is-2-tablet
                is-3-desktop
                is-3-widescreen
                is-2-fullhd
                is-multiline
              "
            >
              <div
                class="column is-half py-2"
                v-for="(fanfiction, innerindex) of fanfictions"
                :key="'ff_selection_' + fanfiction.fanfiction_id.toString()"
              >
                <FanfictionThumbnail
                  :fanfiction="fanfiction"
                  v-bind:index="innerindex"
                  v-bind:key="fanfiction.fanfiction_id"
                ></FanfictionThumbnail>
              </div>
            </div>
          </div>
          <footer class="card-footer">
            <p class="card-footer-item py-2">
              <span>
                <a href="">Plus de sélections</a>
              </span>
            </p>
            <p class="card-footer-item py-2">
              <span>
                <a href="">Votez pour les sélections</a>
              </span>
            </p>
          </footer>
        </div>
      </div>
      <div class="column is-5-tablet is-4-desktop is-3-widescreen">
        <!-- News -->
        <div class="card">
          <header class="card-header sub-title">
            <p class="card-header-title is-centered">Actualités</p>
          </header>
          <div class="card-content">
            <News_2
              v-for="(item, innerindex) of news"
              :key="'news_' + item.news_id.toString()"
              :news="item"
              :activeColor="innerindex % 2 != 0 ? '#e8d7e0' : '#f0f0f0'"
              :class="[{ 'is-hidden-mobile': innerindex > 0 }]"
              v-bind:index="innerindex"
            ></News_2>
          </div>
          <footer class="card-footer">
            <p class="card-footer-item py-2">
              <span>
                <a href="">Plus d'actualités</a>
              </span>
            </p>
          </footer>
        </div>
      </div>
    </div>

    <br />

    <br />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "nuxt-property-decorator";
import { NewsData, getNews } from "@/api/news";
import { getFanfictions } from "@/api/fanfictions";
import { FanfictionData } from "@/types/fanfictions";
import News_2 from "@/components/News_2.vue";
import FanfictionThumbnail from "~/components/FanfictionThumbnail.vue";

@Component({
  components: {
    News_2,
    FanfictionThumbnail,
  },
})
export default class extends Vue {
  private fFByRow = 2;
  private news: NewsData[] = [];
  private fanfictions: FanfictionData[] = [];
  private listLoading = false;
  private listQuery = {
    page: 1,
    limit: 20,
  };

  created() {
    console.log("created");
  }

  async asyncData() {
    console.log("asyncData");
  }

  async fetch() {
    console.log("fetch");
    // let { data } = await getNews(this.listQuery);
    // this.news = data.items;
    this.news = (await getNews(this.listQuery)).data.items;
    // console.log(await getFanfictions(this.listQuery));
    // console.log((await getFanfictions(this.listQuery)).data);
    // console.log((await getFanfictions(this.listQuery)).data.items);
    this.fanfictions = (await getFanfictions(this.listQuery)).data.items;
    // let { data } = await getFanfictions(this.listQuery);
    // this.fanfictions = data.items;
    // this.getNews();
    // this.getFanfictions();
    console.log(this.news.length);
    console.log(this.fanfictions.length);
  }

  private async getNews() {
    this.listLoading = true;
    try {
      const { data } = await getNews(this.listQuery);
      this.news = data.items;
    } catch {
    } finally {
      this.listLoading = false;
    }
  }

  private async getFanfictions() {
    this.listLoading = true;
    try {
      const { data } = await getFanfictions(this.listQuery);
      this.fanfictions = data.items;
    } catch {
    } finally {
      this.listLoading = false;
    }
  }
  beforeMount() {
    console.log("beforemount");
  }
  mouted() {
    console.log("mounted");
  }
}
</script>

<style lang="scss">
@import "~/assets/scss/custom.scss";

.sub-title {
  background-color: $primary;
}
.sub-title .card-header-title {
  color: white;
  text-transform: uppercase;
}
.card-content {
  padding: 0px;
}

@media (max-width: $desktop) {
  .columns.is-reversed-touch {
    flex-direction: column-reverse;
    display: flex;
  }
}

@media (max-width: $tablet) {
  .columns.is-reversed-mobile {
    flex-direction: column-reverse;
    display: flex;
  }
}
</style>