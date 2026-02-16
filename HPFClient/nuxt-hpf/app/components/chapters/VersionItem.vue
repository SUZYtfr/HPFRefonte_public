<template>
  <div :class="['is-flex', 'is-flex-direction-column', 'chapter-validation', { 'item-selected': isSelected }]">
    <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
      <div class="is-flex-grow-5">
        <span class="is-size-7">
          {{ version.versionDate?.toLocaleDateString() + " à " + version.versionDate?.toLocaleTimeString("fr-FR") }}
        </span>
      </div>
    </div>
    <div
      v-if="version.invalidationReasonIds?.length ?? 0 > 0"
      class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center"
    >
      <b-icon icon="warning" size="is-small" type="is-danger" />

      <span class="has-text-danger is-size-7 has-text-weight-semibold">
        {{
          configStore.invalidationReasons.find(
            (t) =>
              t.invalidationReasonId == (version.invalidationReasonIds != null ? version.invalidationReasonIds[0] : 0),
          )?.reason
        }}
      </span>
    </div>
    <div class="is-flex is-flex-direction-row is-flex-wrap-nowrap is-justify-content-start is-align-items-center">
      <div class="is-flex-grow-5">
        <div class="mr-3 white-space-nowrap">
          <template v-for="(author, index) in version.authors" :key="'author_' + author.userId.toString()">
            <template v-if="index > 0"> , </template>
            <b-tooltip v-if="author.watched" label="Auteur à surveiller" :append-to-body="true" position="is-left">
              <b-icon icon="warning" size="is-small" type="is-danger" />
            </b-tooltip>
            <!-- TODO span à reconvertir en NuxtLink -->
            <span class="is-size-7 has-text-weight-bold" :to="{ name: 'auteurs-id', params: { id: author.userId } }">
              {{ author.username }}
            </span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
//#region Imports
import type { VersionModel } from "~/models";
//#endregion

//#region Store
const configStore = useConfigStore();
//#endregion

//#region Props
defineProps<{ version: VersionModel; isSelected: boolean }>();
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
