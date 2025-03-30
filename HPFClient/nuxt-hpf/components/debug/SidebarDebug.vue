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
    <b-button @click="open = true"> Debug panel </b-button>
  </section>
</template>

<script setup lang="ts">
//#region Datas
const open = ref(false);
const connectedValue = ref(false);
//#endregion

//#region Methods
const connectedChanged = (): void => {
  // if (connectedValue.value) {
  //   const user = {
  //     username: "SUZYtfr"
  //   };
  //   $auth.setUser(user);
  //   $auth.$storage.setUniversal("loggedIn", true);
  // } else {
  //   $auth.setUser(null);
  //   $auth.$storage.setUniversal("loggedIn", false);
  // }
  // console.log(connectedValue.value);
  // console.log($auth.loggedIn);
  // console.log($auth.user);
};
//#endregion
</script>

<style lang="scss" scoped>
.p-1 {
  padding: 1em;
}
</style>
