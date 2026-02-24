<template>
  <BModal v-model="modalsStateStore.loginModalActive" width="300px" scroll="keep" @after-enter="modalEntered">
    <form>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Connexion</p>
          <button type="button" class="delete" @click="modalsStateStore.setLoginModalActive(false)"></button>
        </header>
        <section class="modal-card-body">
          <BField label="Identifiant">
            <BInput ref="txtUsername" v-model="loginForm.username" type="text" placeholder="Votre pseudo" required />
          </BField>
          <BField label="Mot de passe">
            <BInput
              v-model="loginForm.password"
              type="password"
              password-reveal
              placeholder="Votre mot de passe"
              required
              @keydown.enter="login()"
            />
          </BField>
          <BCheckbox>Se souvenir de moi</BCheckbox>
        </section>
        <footer class="modal-card-foot">
          <BButton
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
  </BModal>
</template>

<script setup lang="ts">
//#region Imports
import type { UserLoginData } from "~/types/users";
import { useChangeTheme } from "~/composables/useTheme";
import { ColorSchemeEnum } from "~/types/themes";
import { snackbar } from "~/composables/useBuefy";
//#endregion

//#region Usings
const { data, signIn } = useCustomAuth();
// #endregion

// #region Stores
const modalsStateStore = useModalsStateStore();
const configStore = useConfigStore();
// #endregion

//#region Ref
const isLoading = ref(false);
const loginForm: Ref<UserLoginData> = ref({ username: "", password: "" });
//#endregion

//#region Reférences de la template
const userNameInput = useTemplateRef<HTMLElement>("txtUsername");
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
    await signIn(loginForm.value);
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
    } else {
      snackbar.open({
        duration: 5000,
        message: "Une erreur s'est produite lors de la tentative de connexion",
        type: "is-danger",
        position: "is-bottom-right",
        actionText: undefined,
        pauseOnHover: true,
        queue: true,
      });
    }
  } finally {
    isLoading.value = false;
  }
};

// Focus le champ identifiant à l'ouverture de la modale
const modalEntered = (): void => {
  userNameInput.value?.focus();
};
//#endregion
</script>

<style lang="scss" scoped></style>
