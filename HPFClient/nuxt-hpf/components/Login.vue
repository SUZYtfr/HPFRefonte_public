<template>
  <b-modal v-model="modalActive" width="300px" scroll="keep">
    <form ref="loginForm">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Connexion</p>
          <button type="button" class="delete" @click="modalActive = false" />
        </header>
        <section class="modal-card-body">
          <b-field label="Identifiant">
            <b-input
              type="text"
              v-model="loginForm.username"
              placeholder="Votre pseudo"
              required
            >
            </b-input>
          </b-field>
          <b-field label="Mot de passe">
            <b-input
              type="password"
              v-model="loginForm.password"
              password-reveal
              placeholder="Votre mot de passe"
              required
            >
            </b-input>
          </b-field>
          <b-checkbox>Se souvenir de moi</b-checkbox>
        </section>
        <footer class="modal-card-foot">
          <b-button
            :disabled="!formIsValid"
            :expanded="true"
            label="Se connecter"
            type="is-primary"
            :loading="loading"
            @click="checkAndSubmitForm()"
          />
        </footer>
      </div>
    </form>
  </b-modal>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "nuxt-property-decorator";
import { login } from "@/api/users";
import { VForm, OpenToast } from "@/utils/formHelper";
import { UserLoginData } from "@/types/users";

@Component({
  name: "Connexion",
})
export default class extends Vue {
  //#region Props
  @Prop() private active!: boolean;
  //#endregion

  //#region Data
  private loginForm: UserLoginData = {
    username: "",
    password: "",
  };

  private formIsValid: boolean = false;

  private loading: boolean = false;
  //#endregion

  //#region Computed
  get modalActive() {
    return this.active;
  }

  set modalActive(value) {
    this.$emit("change", value);
  }

  get form(): VForm {
    return this.$refs["loginForm"] as VForm;
  }
  //#endregion

  //#region Watchers
  @Watch("loginForm", { deep: true })
  private onFormChanged() {
    this.formIsValid = this.form.checkValidity();
  }
  //#endregion

  //#region Methods
  // Vérifier le formulaire avant l'envoi
  private checkAndSubmitForm() {
    if (this.form.checkValidity()) this.login();
  }

  // Envoyer le formulaire
  private async login() {
    this.loading = true;
    try {
      const { data } = await login(this.loginForm);
    } catch (exception) {
      console.log(exception);
      OpenToast("Erreur", "is-danger", 5000, false, true, "is-bottom");
    } finally {
      this.loading = false;
    }
  }
  //#endregion
}
</script>

<style lang="scss" scoped>
@import "~/assets/scss/custom.scss";
</style>