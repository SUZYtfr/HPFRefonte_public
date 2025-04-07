<template>
  <b-modal v-model="ModalStatesModule.loginModalActive" width="300px" scroll="keep">
    <form ref="html-login-form">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Connexion
          </p>
          <button type="button" class="delete" @click="ModalStatesModule.setLoginModalActive(false)" />
        </header>
        <section class="modal-card-body">
          <b-field label="Identifiant">
            <b-input
              v-model="loginForm.username"
              type="text"
              placeholder="Votre pseudo"
              required
            />
          </b-field>
          <b-field label="Mot de passe">
            <b-input
              v-model="loginForm.password"
              type="password"
              password-reveal
              placeholder="Votre mot de passe"
              required
              @keydown.native.enter="checkAndSubmitForm()"
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
            :loading="status === 'pending'"
            @click="checkAndSubmitForm()"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script setup lang="ts">
import { UserLoginData } from "@/types/users";
import { ColorSchemeEnum } from "~/types/themes";

const ModalStatesModule = ModalsStates();

// Le formulaire en tant qu'élément HTML
const htmlLoginForm = useTemplateRef("html-login-form");

// L'objet lié des informations du formulaire
const loginForm = reactive<UserLoginData>({
  username: "",
  password: ""
});

// Si les informations changent, utiliser la validation de l'élément HTML
const formIsValid = ref(false);
watch(loginForm, () => { formIsValid.value = htmlLoginForm.value.checkValidity() });

// TODO réparer les toasts !
const { status, execute: submitForm, error } = await useFetch("http://localhost:8585/api/account/", { immediate: false });
watch(status, () => {
  if (status.value === "success") {
    OpenToast("Envoi réussi", "is-primary", 5000, false, true, "is-bottom");
  }
  else if (status.value === "error") {
    console.log("essai");
    OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
  }
});

// Vérifier le formulaire avant l'envoi
function checkAndSubmitForm(): void {
  // if (formIsValid) submitForm();
  $auth.loginWith();
  changeTheme(Config().currentTheme?.details?.find((t) => { return t.colorScheme === (($auth?.user?.preferences as any)?.color_scheme ?? ColorSchemeEnum.Light); }) ?? null);
}
</script>

<style lang="scss" scoped>
@use "~/assets/scss/custom.scss";
</style>
