<template>
  <b-modal v-model="modalsStateStore.loginModalActive" width="300px" scroll="keep">
    <form>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Connexion</p>
          <button type="button" class="delete" @click="modalsStateStore.setLoginModalActive(false)"></button>
        </header>
        <section class="modal-card-body">
          <b-field label="Identifiant">
            <b-input v-model="loginForm.username" type="text" placeholder="Votre pseudo" required />
          </b-field>
          <b-field label="Mot de passe">
            <b-input
              v-model="loginForm.password"
              type="password"
              password-reveal
              placeholder="Votre mot de passe"
              required
              @keydown.enter="login()"
            />
          </b-field>
          <b-checkbox>Se souvenir de moi</b-checkbox>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="Se connecter"
            type="is-primary"
            :loading="isLoading"
            @click="login"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script setup lang="ts">
//#region Imports
import type { UserLoginData } from "~/types/users";
import { useChangeTheme } from "~/composables/useTheme";
import { ColorSchemeEnum } from "~/types/themes";
//#endregion

//#region Usings
const { data, signIn } = useAuth();
// #endregion

// #region Stores
const modalsStateStore = useModalsStateStore();
const configStore = useConfigStore();
// #endregion

//#region Ref
const isLoading = ref(false);
const loginForm: Ref<UserLoginData> = ref({ username: "", password: "" });
//#endregion

//#region Computed
const formIsValid = computed(() => {
  return (loginForm.value?.username?.length ?? 0) > 0 && (loginForm.value?.password?.length ?? 0) > 0;
});
//#endregion

//#region Functions
const login = async (): Promise<void> => {
  isLoading.value = true;
  try {
    await signIn(loginForm.value, { redirect: false });
    // Mettre le thème de l'utilisateur
    useChangeTheme(
      configStore.currentTheme?.details?.find((t) => {
        return t.colorScheme === ((data.value?.preferences.colorScheme as ColorSchemeEnum) ?? ColorSchemeEnum.Light);
      }) ?? null,
    );
    modalsStateStore.setLoginModalActive(false);
  } catch (error) {
    if (import.meta.server) {
      console.log(error);
    }
  } finally {
    isLoading.value = false;
  }
};
//#endregion
</script>

<style lang="scss" scoped></style>
