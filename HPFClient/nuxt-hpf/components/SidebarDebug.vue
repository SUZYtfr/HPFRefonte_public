<template>
  <section>
    <b-sidebar
      type="is-light"
      :fullheight="true"
      :overlay="true"
      :right="true"
      v-model="open"
    >
      <div class="p-1">
        <b-menu>
          <b-menu-list>
            <b-switch v-model="connectedValue" @input="connectedChanged()">Connecté</b-switch>
          </b-menu-list>
        </b-menu>
      </div>
    </b-sidebar>
    <b-button @click="open = true">Debug panel</b-button>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { UserModule } from '@/utils/store-accessor'

@Component({
  name: "SidebarDebug",
})
export default class extends Vue {
  private open: boolean = false;
  private connectedValue: boolean = false;

  private connectedChanged(){
      console.log(this.connectedValue);
    UserModule.SET_TOKEN(this.connectedValue ? "AAAAA" : "");
    console.log(UserModule.token);
  }
  
}
</script>

<style lang="scss" scoped>
.p-1 {
  padding: 1em;
}
</style>