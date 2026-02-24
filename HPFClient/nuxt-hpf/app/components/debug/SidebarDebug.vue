<template>
  <section>
    <BSidebar v-model="open" type="is-light" :fullheight="true" :overlay="true" :right="true">
      <div class="p-1">
        <BMenu>
          <BMenuList>
            <BSwitch v-model="connectedValue" @input="connectedChanged()"> Connecté </BSwitch>
          </BMenuList>
        </BMenu>
      </div>
    </BSidebar>
    <BButton @click="open = true"> Debug panel </BButton>
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
