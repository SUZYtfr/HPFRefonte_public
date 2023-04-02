<template>
  <a
    ref="mainElement"
    :class="[
      { 'tag-hover': hover },
      'tag p-2 is-relative',
      getCaracteristicTypeColor(characteristic_type_id),
    ]"
    @mouseover="hover = true"
    @mouseleave="hover = false"
    @click="$emit('click', characteristic_type_id, characteristic_id)"
  >
    <div
      id="tag-wrapper"
      class="
        is-flex
        is-flex-direction-column
        is-justify-content-center
        is-align-items-center
      "
    >
      <div class="has-text-centered">
        <label
          ref="lblCharName"
          :class="[
            'is-block',
            'is-clickable',
            { 'has-text-weight-bold': hover },
            { 'has-text-weight-semibold': !hover },
          ]"
        >{{ characteristic_name }}</label>
      </div>
      <div
        class="has-text-centered"
        style="
          width: 100%;
          max-height: 50%;
          padding: 0px 5px;
          overflow-x: auto;
          overflow-y: hidden;
        "
      >
        <label
          v-if="characteristic_description !== undefined"
          ref="lblCharDescription"
          :class="[
            'is-block',
            'has-text-centered',
            'is-clickable',
            'has-text-weight-semibold',
          ]"
        >{{ characteristic_description }}</label>
      </div>
    </div>
    <label
      v-if="characteristic_count !== undefined"
      :class="[
        'is-size-7',
        'is-clickable',
        'is-italic',
        { 'absolute-count': !hover },
        { 'absolute-count-hover': hover },
        { 'has-text-weight-bold': hover },
        { 'has-text-weight-semibold': !hover },
      ]"
    >{{ characteristic_count }}</label>
  </a>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "nuxt-property-decorator";
import { getCaracteristicTypeColor } from "@/utils/characteristics";
@Component({
  name: "TagPanel"
})
export default class extends Vue {
  // #region Props
  @Prop() public characteristic_type_id!: number | undefined;
  @Prop() public characteristic_id!: number | undefined;
  @Prop() public characteristic_name!: string | undefined;
  @Prop() public characteristic_description!: string | undefined;
  @Prop() public characteristic_count!: number | undefined;
  // #endregion

  // #region Datas
  public hover: boolean = false;
  private transform: string = "";
  private fontSize: string = "";
  private ro: ResizeObserver | null = null;
  private timerResize: number = -1;
  // #endregion

  // #region Hooks
  mounted(): void {
    this.resizeTag();
    this.ro = new ResizeObserver(this.onResize);
    this.ro.observe(this.$refs.mainElement as HTMLElement);
  }

  beforeDestroy(): void {
    this.ro?.unobserve(this.$refs.mainElement as HTMLElement);
  }
  // #endregion

  // #region Methods
  // Récupération couleur du tag
  public getCaracteristicTypeColor(characteristic_type_id: number | undefined): string {
    if (characteristic_type_id === undefined) return "";
    return getCaracteristicTypeColor(characteristic_type_id);
  }

  // Lors du resize de l'élément
  private onResize(): void {
    clearTimeout(this.timerResize);
    this.timerResize = window.setTimeout(this.resizeTag, 100);
  }

  // Vérifier si un élément overflow son parent
  private isOverflown(
    clientWidth: number,
    scrollWidth: number,
    clientHeight: number,
    scrollHeight: number
  ): boolean {
    return scrollWidth > clientWidth || scrollHeight > clientHeight;
  }

  // Resizer un élément
  private resizeText(
    element: HTMLElement,
    minSize: number = 8,
    maxSize: number = 20,
    step: number = 1,
    unit: string = "px"
  ): void {
    if (element === null || element === undefined) return;
    let i = minSize;
    let overflow = false;
    const parent = element.parentNode as HTMLElement;

    while (!overflow && i < maxSize) {
      element.style.fontSize = `${i}${unit}`;
      overflow = this.isOverflown(
        parent.clientWidth,
        parent.scrollWidth,
        parent.clientHeight,
        parent.scrollHeight
      );
      if (!overflow) i += step;
    }
    // revert to last state where no overflow happened:
    element.style.fontSize = `${i - step}${unit}`;
  }

  // Resize Name + Description
  private resizeTag(): void {
    this.resizeText(this.$refs.lblCharName as HTMLElement);
    this.resizeText(this.$refs.lblCharDescription as HTMLElement, 6, 12);
  }
  // #endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";

a {
  height: 100px !important;
  width: 100% !important;
  text-decoration: none !important;
  #tag-wrapper {
    width: 100% !important;
    height: 100% !important;
    div {
      width: 100%;
      max-height: 50%;
      padding: 0px 5px;
      overflow-x: auto;
      overflow-y: hidden;
    }
  }
  label {
    white-space: normal;
  }
  .absolute-count {
    display: block;
    position: absolute;
    z-index: 2;
    top: 80px;
    right: 5px;
  }

  .absolute-count-hover {
    display: block;
    position: absolute;
    z-index: 2;
    top: 74px;
    right: 5px;
  }
}

.tag-hover {
  border: 5px solid $primary-light !important;
  border-radius: 10px !important;
}
</style>
