<template>
  <section>
    <b-sidebar
      v-model="open"
      type="is-light"
      :fullheight="true"
      :overlay="true"
      :right="true"
    >
      <div class="p-1">
        <b-menu>
          <b-menu-list>
            <b-switch v-model="connectedValue" @input="connectedChanged()">
              Connecté
            </b-switch>
          </b-menu-list>
        </b-menu>
      </div>
    </b-sidebar>
    <b-button @click="open = true">
      Debug panel
    </b-button>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "SidebarDebug"
})
export default class SidebarDebug extends Vue {
  public open: boolean = false;
  public connectedValue: boolean = false;

  public connectedChanged(): void {
    if (this.connectedValue) {
      const user = {
        username: "SUZYtfr"
      };
      this.$auth.setUser(user);
      this.$auth.$storage.setUniversal("loggedIn", true);
    } else {
      this.$auth.setUser(null);
      this.$auth.$storage.setUniversal("loggedIn", false);
    }
    console.log(this.connectedValue);
    console.log(this.$auth.loggedIn);
    console.log(this.$auth.user);
  }
}
</script>

<style lang="scss" scoped>
.p-1 {
  padding: 1em;
}
</style>
