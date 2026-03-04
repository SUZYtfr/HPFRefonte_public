<template>
  <div :class="['is-flex', 'is-flex-direction-column', 'chapter-validation', { 'item-selected': isSelected }]">
    <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
      <div class="is-flex-grow-5">
        <h3 class="h3 has-text-weight-semibold text-ellipsis-one-line">
          {{ chapter.title }}
        </h3>
      </div>
      <BTooltip
        v-if="chapter.validationStatus == ChapterValidationStatusEnum.AwaitingDiscussion"
        label="à discuter"
        :append-to-body="true"
        position="is-right"
      >
        <BIcon icon="comment-alt" size="is-small" />
      </BTooltip>
    </div>
    <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
      <BTooltip
        v-if="chapter.fictionMetadata?.watched"
        label="Fiction à surveiller"
        :append-to-body="true"
        position="is-left"
      >
        <BIcon icon="warning" size="is-small" type="is-danger" />
      </BTooltip>
      <span class="is-size-7 has-text-italic">{{ chapter.fictionMetadata?.title }}</span>
    </div>
    <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
      <div class="is-flex-grow-5">
        <div class="mr-3 white-space-nowrap">
          <template v-for="(author, index) in chapter.authors" :key="'author_' + author.userId.toString()">
            <template v-if="index > 0"> , </template>
            <BTooltip v-if="author.watched" label="Auteur à surveiller" :append-to-body="true" position="is-left">
              <BIcon icon="warning" size="is-small" type="is-danger" />
            </BTooltip>
            <!-- TODO span à reconvertir en NuxtLink -->
            <span class="is-size-6 has-text-weight-normal" :to="{ name: 'auteurs-id', params: { id: author.userId } }">
              {{ author.username }}
            </span>
          </template>
        </div>
      </div>
      <span class="is-size-7">{{ chapter.submissionDate?.toLocaleDateString() }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
//#region Imports
import type { ChapterModel } from "~/models";
import { ChapterValidationStatusEnum } from "~/types/fanfictions";
//#endregion

//#region Props
defineProps<{ chapter: ChapterModel; isSelected: boolean }>();
//#endregion
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
.chapter-validation {
  padding: 5px 5px 5px 5px;
  border-radius: 10px;
  border: 1px solid transparent;
}
.chapter-validation:not(.item-selected):hover {
  cursor: pointer;
  border: 1px solid var(--primary-light) !important;
}
</style>
