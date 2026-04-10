<template>
  <div id="main-container" class="container pt-3 is-flex is-flex-direction-column is-flex-grow-5 px-3">
    <BLoading v-model="isLoading" :is-full-page="false" />
    <section>
      <div class="card">
        <header class="card-header sub-title">
          <p class="card-header-title is-centered has-text-centered">
            {{ collection.title }}
          </p>
        </header>
        <div class="card-content" style="padding: 5px; padding-top: 2px; padding-bottom: 0px">
          <div class="is-flex is-flex-direction-row is-align-items-center">
            <div class="is-flex-grow-5">
              <span class="is-size-6"
                ><strong>{{ "Auteur" + ((collection.authors?.length ?? 0) > 1 ? "s" : "") + " : " }}</strong></span
              >
              <template v-for="(author, index) in collection.authors" :key="'author_' + author.userId.toString()">
                <template v-if="index > 0"> , </template>
                <!-- <a class="is-size-6-5 has-text-weight-normal" :href="'auteurs/' + author.userId" -->
                {{ author.username }}
                <!-- </a> -->
              </template>
            </div>
            <div class="">
              <a class="is-size-6 has-text-weight-normal" href="#reviews" @click="reviewSectionVisible = true"
                >{{
                  collection.reviewCount != null
                    ? collection.reviewCount + " review" + (collection.reviewCount > 1 ? "s" : "")
                    : "aucune review"
                }}<BIcon class="ml-1" icon="comments" />
              </a>
            </div>
          </div>
          <div class="is-flex is-flex-direction-row is-align-items-center">
            <div class="is-flex-grow-5">
              <span class="is-size-6"
                ><strong>{{ "Fandom" + ((collection.fandoms?.length ?? 0) > 1 ? "s" : "") + " : " }}</strong></span
              >
              <template v-for="(fandom, index) in collection.fandoms" :key="'author_' + fandom.id.toString()">
                <template v-if="index > 0">, </template>
                <NuxtLink
                  class="is-size-6-5 has-text-weight-normal"
                  :to="{ name: 'fandomSlug', params: { fandomSlug: fandom.slug } }"
                  >{{ fandom.name }}</NuxtLink
                >
              </template>
            </div>
          </div>
          <BTaglist class="mb-0">
            <span
              v-for="characteristic in collection.characteristics"
              :key="'tag_' + characteristic.characteristicId.toString()"
              ><BTag :class="[getClassType(characteristic), 'mt-0  mb-1 mr-2 is-size-8']" type="is-info">{{
                characteristic.name
              }}</BTag></span
            >
          </BTaglist>
          <div class="columns mb-0 mx-0 mt-0">
            <div class="column py-0 pl-0">
              <RichtextReader :text="collection.summary || ''" />
            </div>
          </div>
          <div
            v-if="useCustomAuth().isAuthenticated"
            class="is-flex is-flex-direction-row is-justify-content-space-evenly"
          >
            <span
              v-if="Object.fromEntries(Object.entries(CollectionAccess))[collection.access!] == CollectionAccess.CLOSED"
              >Cette série est fermée aux ajouts</span
            >
            <span
              v-else-if="
                Object.fromEntries(Object.entries(CollectionAccess))[collection.access!] == CollectionAccess.MODERATED
              "
              >Cette série est modérée et
              <NuxtLink :to="{ name: 'compte-séries-écritoire', query: { série: collection.collectionId } }"
                >accepte les suggestions</NuxtLink
              ></span
            >
            <span
              v-else-if="
                Object.fromEntries(Object.entries(CollectionAccess))[collection.access!] == CollectionAccess.OPEN
              "
              >Cette série est
              <NuxtLink :to="{ name: 'compte-séries-écritoire', query: { série: collection.collectionId } }">
                ouverte aux ajouts</NuxtLink
              ></span
            >
          </div>
        </div>
      </div>
    </section>

    <!-- Élements de série -->
    <section>
      <BCollapse
        v-for="(item, index) in collection.items"
        :key="index"
        class="card m-3"
        animation="slide"
        :model-value="openItemIndex == index"
        :aria-id="'contentIdForA11y5-' + index"
        @open="openItemIndex = index"
      >
        <template #trigger="props">
          <div
            class="card-header"
            role="button"
            :aria-controls="'contentIdForA11y5-' + index"
            :aria-expanded="props.open"
          >
            <p class="card-header-title">
              <span>
                {{ item.title }}
              </span>
              <BTag class="is-pulled-right">{{ item.itemType }}</BTag>
            </p>
            <a class="card-header-icon">
              <BIcon :icon="props.open ? 'caret-down' : 'caret-up'" />
            </a>
          </div>
        </template>
        <div class="card-content">
          <div class="content">
            <ChapterItem v-if="item.chapter" :chapter="item.chapter" />
            <FictionItem v-else-if="item.fiction" :fiction="item.fiction" />
            <CollectionItem v-else-if="item.collection" :collection="item.collection" />
          </div>
        </div>
      </BCollapse>
    </section>

    <!-- Reviews -->
    <section id="reviews">
      <BCollapse v-model="reviewSectionVisible" class="card" animation="slide" aria-id="fictionReviews">
        <template #trigger="props">
          <div class="card-header sub-title" role="button" aria-controls="fictionReviews" :aria-expanded="props.open">
            <p class="card-header-title is-unselectable">
              {{ "Reviews (" + (paginatedReviews.totalCount || 0).toString() + ")" }}
            </p>
            <a class="card-header-icon">
              <BIcon class="is-clickable" :icon="props.open ? 'caret-up' : 'caret-down'" />
            </a>
          </div>
        </template>

        <div class="card-content pb-0">
          <div class="content p-2">
            <ReviewList
              ref="review-list"
              :review-list-type="ReviewItemTypeEnum.Collection"
              :paginated-reviews
              :pagination="reviewPagination"
              :is-loading="reviewsStatus === 'pending'"
              :post-review
              @pagination-change="(pagination: OffsetPaginationInput) => (reviewPagination = pagination)"
            />
          </div>
        </div>
      </BCollapse>
      <br />
    </section>
  </div>
</template>

<script setup lang="ts">
import { BLoading, BCollapse, BTag, BTaglist, BIcon } from "buefy";
import { plainToInstance } from "class-transformer";
import { CollectionModel, ReviewModel } from "~/models";
import { getClassTypeColor as getClassType } from "#imports";
import { CollectionAccess, ReviewItemTypeEnum } from "~/types/fanfictions";
import type { OffsetPaginationInput, ReviewInput } from "#gql";

const { params, hash } = useRoute();

const { data: collection, status } = useAsyncGql(
  "getCollection",
  {
    collectionId: params.collectionId as string,
  },
  {
    transform: (input) => {
      return plainToInstance(CollectionModel, input.collection);
    },
  },
);
const isLoading = computed<boolean>(() => status.value == "pending");

const reviewSectionVisible = ref<boolean>(false);
const openItemIndex = ref<number>(0);

const reviewPagination = ref<OffsetPaginationInput>({
  limit: 10,
  offset: 0,
});

const { data: paginatedReviews, status: reviewsStatus } = await useAsyncGql(
  "getCollectionReviews",
  {
    filters: {
      collection: {
        id: {
          exact: params.collectionId as string,
        },
      },
    },
    pagination: reviewPagination,
  },
  {
    lazy: false,
    transform: (input) => {
      return {
        ...input.collectionReviews,
        results: plainToInstance(ReviewModel, input.collectionReviews.results),
      };
    },
  },
);

async function postReview(reviewData: ReviewInput): Promise<void> {
  await GqlCreateCollectionReview({
    collectionId: params.collectionId as string,
    collectionReviewData: {
      text: reviewData.text,
      grading: reviewData.grading,
    },
  });
}

useHead({
  title: "HPF - " + collection.value?.title,
});

onMounted(() => {
  if (hash == "#reviews") {
    reviewSectionVisible.value = true;
  }
});
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom_bulma_core.scss";
#main-container {
  background-color: var(--hpf-primary-lighter);
}

section {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
