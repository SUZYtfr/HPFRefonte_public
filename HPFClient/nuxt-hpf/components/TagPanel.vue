<template>
  <a
    :class="[
      { 'tag-hover': hover },
      'tag p-2 is-relative',
      getCaracteristicTypeColor(characteristic_type_id),
    ]"
    @mouseover="hover = true"
    @mouseleave="hover = false"
    @click="$emit('click', characteristic_type_id, characteristic_id)"
    style="height: 100px; width: 100%; text-decoration: none"
  >
    <div
      class="
        is-flex
        is-flex-direction-column
        is-justify-content-center
        is-align-items-center
      "
    >
      <!-- <div style="background-color: #ffffff; opacity: 0.10;"> -->
      <!--<div style="display: block; overflow: hidden; position: absolute; inset: 0px; box-sizing: border-box; margin: 0px;">
			 <img alt="" src="https://image.tmdb.org/t/p/w1280_filter(duotone,991B1B,FCA5A5)/eNI7PtK6DEYgZmHWP9gQNuff8pv.jpg" decoding="async" data-nimg="fill" style="position: absolute; inset: 0px; box-sizing: border-box; padding: 0px; border: medium none; margin: auto; display: block; width: 0px; height: 0px; min-width: 100%; max-width: 100%; min-height: 100%; max-height: 100%; object-fit: cover;">
				<noscript/>
			</div>-->
      <!--<div class="absolute z-10 inset-0 w-full h-full transition duration-300 bg-gray-800 bg-opacity-30"/>-->
      <!-- <div class="relative z-20 w-full text-2xl font-bold text-center text-white truncate whitespace-normal sm:text-3xl">Action</div> -->
      <label
        :class="[
          'is-size-5',
          'is-clickable',
          { 'has-text-weight-bold': hover },
          { 'has-text-weight-semibold': !hover },
        ]"
        >{{ characteristic_name }}</label
      >
      <label
        v-if="characteristic_description !== undefined"
        :class="[
          'is-size-7',
          'has-text-centered',
          'is-clickable',
          'has-text-weight-semibold',
        ]"
        >{{ characteristic_description }}</label
      >
    </div>
    <label
      v-if="characteristic_id !== undefined"
      :class="[
        'is-size-7',
        'is-clickable',
        'is-italic',
        { 'absolute-count': !hover },
        { 'absolute-count-hover': hover },
        { 'has-text-weight-bold': hover },
        { 'has-text-weight-semibold': !hover },
      ]"
      >1258</label
    >

    <!-- </div> -->
  </a>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { getCaracteristicTypeColor } from "@/utils/characteristics";
@Component({
  name: "TagPanel",
})
export default class extends Vue {
  //#region Props
  @Prop() private characteristic_type_id!: number | undefined;
  @Prop() private characteristic_id!: number | undefined;
  @Prop() private characteristic_name!: string | undefined;
  @Prop() private characteristic_description!: string | undefined;
  @Prop() private characteristic_count!: number | undefined;
  //#endregion

  //#region Datas
  private hover: boolean = false;
  //#endregion

  //#region Methods
  private getCaracteristicTypeColor(characteristic_type_id: number) {
    return getCaracteristicTypeColor(characteristic_type_id);
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

.overflow-hidden {
  overflow: hidden;
}

.tag-hover {
  border: 5px solid $primary-light !important;
  border-radius: 10px !important;
}
a label {
  white-space: normal;
}

.absolute-count {
  display: block;
  position: absolute;
  z-index: 2;
  //background: blue;
  top: 80px;
  right: 5px;
}

.absolute-count-hover {
  display: block;
  position: absolute;
  z-index: 2;
  //background: blue;
  top: 74px;
  right: 5px;
}
</style>